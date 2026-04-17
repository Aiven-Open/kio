//! Native parse schema: wire-format → Python values without per-field PyObject callables.
//!
//! All Kafka nominal types (BrokerId, TopicName, …) are now phantom types whose
//! `isinstance(x, T)` check passes for any value of the underlying wire type, so the
//! parse loop never needs a wrapping callable: every `PrimitiveKind` variant already
//! produces the right Python type directly (plain `int`, `str`, `bytes`, `uuid.UUID`,
//! `ErrorCode`, …).

use std::collections::HashMap;
use std::sync::{Arc, LazyLock, Mutex};

use pyo3::BoundObject;
use pyo3::exceptions::{PyKeyError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyModule, PyString, PyTuple, PyType};

use crate::readers::{
    self, as_datetime, instantiate_timedelta, instantiate_uuid,
    internal_nullable_read_legacy_string, internal_read_boolean,
    internal_read_compact_array_length, internal_read_compact_string,
    internal_read_compact_string_as_bytes_nullable, internal_read_compact_string_nullable,
    internal_read_datetime_i64, internal_read_error_code, internal_read_float64,
    internal_read_int8, internal_read_int16, internal_read_int32, internal_read_int64,
    internal_read_legacy_bytes, internal_read_legacy_string, internal_read_nullable_datetime_i64,
    internal_read_nullable_legacy_bytes, internal_read_timedelta_i32, internal_read_timedelta_i64,
    internal_read_uint8, internal_read_uint16, internal_read_uint32, internal_read_uint64,
    tz_aware_from_i64,
};

/// Return `data[cursor..]`, or an empty slice when `cursor` is past the end.
/// All internal readers return `BufferUnderflow` for an empty / too-short slice,
/// so this safely converts the out-of-bounds case into the right error.
#[inline(always)]
fn slice_from(data: &[u8], cursor: usize) -> &[u8] {
    data.get(cursor..).unwrap_or(&[])
}

#[derive(Clone, Copy, Debug)]
pub(crate) enum PrimitiveKind {
    Int8,
    Int16,
    Int32,
    Int64,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    Float64,
    Bool,
    CompactString,
    CompactStringNull,
    CompactBytes,
    CompactBytesNull,
    LegacyString,
    NullableLegacyString,
    LegacyBytes,
    NullableLegacyBytes,
    Uuid,
    ErrorCode,
    TimedeltaI32,
    TimedeltaI64,
    DatetimeI64,
    DatetimeI64Null,
}

/// Schema for reading one field or array element (`Arc` for sharing tagged vs regular lists).
pub(crate) enum FieldSchema {
    Primitive(PrimitiveKind),
    Entity { schema: Arc<EntitySchema> },
    CompactArray(Arc<FieldSchema>),
    LegacyArray(Arc<FieldSchema>),
}

pub(crate) struct EntitySchema {
    pub entity_type: Py<PyType>,
    pub flexible: bool,
    pub nullable: bool,
    /// Non-tagged fields in dataclass declaration order.
    /// Field name is stored as an interned `Py<PyString>` so it can be reused across
    /// every parse call without re-allocating a Python string.
    pub field_schemas: Vec<(Py<PyString>, Arc<FieldSchema>)>,
    /// Maps wire tag-number → (index into `tagged_field_defaults`, field schema).
    /// Using an index avoids storing a duplicate name string and avoids a secondary
    /// dict allocation at parse time.
    pub tagged_field_schemas: HashMap<u64, (usize, Arc<FieldSchema>)>,
    /// Tagged fields in declaration order: (interned name, implicit default value).
    pub tagged_field_defaults: Vec<(Py<PyString>, Py<PyAny>)>,
}

type SchemaCache = Mutex<HashMap<(usize, bool), Arc<EntitySchema>>>;

static SCHEMA_CACHE: LazyLock<SchemaCache> = LazyLock::new(|| Mutex::new(HashMap::new()));

fn read_primitive(
    py: Python<'_>,
    kind: PrimitiveKind,
    bytes: &[u8],
) -> PyResult<(Py<PyAny>, usize)> {
    let (value, size): (Bound<'_, PyAny>, usize) = match kind {
        PrimitiveKind::Int8 => {
            let (v, s) = internal_read_int8(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::Int16 => {
            let (v, s) = internal_read_int16(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::Int32 => {
            let (v, s) = internal_read_int32(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::Int64 => {
            let (v, s) = internal_read_int64(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::UInt8 => {
            let (v, s) = internal_read_uint8(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::UInt16 => {
            let (v, s) = internal_read_uint16(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::UInt32 => {
            let (v, s) = internal_read_uint32(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::UInt64 => {
            let (v, s) = internal_read_uint64(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::Float64 => {
            let (v, s) = internal_read_float64(bytes)?;
            (v.into_pyobject(py)?.into_any(), s)
        }
        PrimitiveKind::Bool => {
            let (v, s) = internal_read_boolean(bytes)?;
            let b = pyo3::types::PyBool::new(py, v);
            (b.to_owned().into_any(), s)
        }
        PrimitiveKind::CompactString => {
            let (s, sz) = internal_read_compact_string(bytes)?;
            (s.into_pyobject(py)?.into_any(), sz)
        }
        PrimitiveKind::CompactStringNull => {
            let (opt, sz) = internal_read_compact_string_nullable(bytes)?;
            match opt {
                Some(s) => (s.into_pyobject(py)?.into_any(), sz),
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
        PrimitiveKind::CompactBytes => {
            let (sl, sz) = crate::readers::internal_read_compact_string_as_bytes(bytes)?;
            let b = pyo3::types::PyBytes::new(py, sl);
            (b.into_any(), sz)
        }
        PrimitiveKind::CompactBytesNull => {
            let (opt, sz) = internal_read_compact_string_as_bytes_nullable(bytes)?;
            match opt {
                Some(sl) => {
                    let b = pyo3::types::PyBytes::new(py, sl);
                    (b.into_any(), sz)
                }
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
        PrimitiveKind::LegacyString => {
            let (s, sz) = internal_read_legacy_string(bytes)?;
            (s.into_pyobject(py)?.into_any(), sz)
        }
        PrimitiveKind::NullableLegacyString => {
            let (opt, sz) = internal_nullable_read_legacy_string(bytes)?;
            match opt {
                Some(s) => (s.into_pyobject(py)?.into_any(), sz),
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
        PrimitiveKind::LegacyBytes => {
            let (sl, sz) = internal_read_legacy_bytes(bytes)?;
            let b = pyo3::types::PyBytes::new(py, sl);
            (b.into_any(), sz)
        }
        PrimitiveKind::NullableLegacyBytes => {
            let (opt, sz) = internal_read_nullable_legacy_bytes(bytes)?;
            match opt {
                Some(sl) => {
                    let b = pyo3::types::PyBytes::new(py, sl);
                    (b.into_any(), sz)
                }
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
        PrimitiveKind::Uuid => {
            let opt = crate::readers::internal_read_uuid(bytes)?;
            let (py_opt, sz) = instantiate_uuid(py, opt)?;
            match py_opt {
                Some(p) => (p.into_bound(py).into_any(), sz),
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
        PrimitiveKind::ErrorCode => {
            let (code, sz) = internal_read_error_code(bytes)?;
            let v = crate::readers::wrap_error_code_value(py, code)?;
            (v.into_bound(py).into_any(), sz)
        }
        PrimitiveKind::TimedeltaI32 => {
            let (ms, sz) = internal_read_timedelta_i32(bytes)?;
            let v = instantiate_timedelta(py, ms)?;
            (v.into_bound(py).into_any(), sz)
        }
        PrimitiveKind::TimedeltaI64 => {
            let (ms, sz) = internal_read_timedelta_i64(bytes)?;
            let v = instantiate_timedelta(py, ms)?;
            (v.into_bound(py).into_any(), sz)
        }
        PrimitiveKind::DatetimeI64 => {
            let (ts, sz) = internal_read_datetime_i64(bytes)?;
            let v = tz_aware_from_i64(py, ts)?;
            (v.into_bound(py).into_any(), sz)
        }
        PrimitiveKind::DatetimeI64Null => {
            let (opt, sz) = internal_read_nullable_datetime_i64(bytes)?;
            match opt {
                Some(ts) => {
                    let dt = as_datetime(py, ts)?;
                    (dt.into_bound(py).into_any(), sz)
                }
                None => (py.None().into_pyobject(py)?.into_any(), sz),
            }
        }
    };
    Ok((value.unbind(), size))
}

/// Read the field described by `schema` from `data` starting at byte offset `cursor`.
/// Returns `(value, bytes_consumed)`.  `data` is the full input slice acquired once at the
/// call-site entry point; `cursor` is an absolute position within it.
pub(crate) fn read_field(
    py: Python<'_>,
    schema: &Arc<FieldSchema>,
    data: &[u8],
    cursor: usize,
) -> PyResult<(Py<PyAny>, usize)> {
    match schema.as_ref() {
        FieldSchema::Primitive(kind) => read_primitive(py, *kind, slice_from(data, cursor)),
        FieldSchema::Entity { schema } => parse_entity(py, schema, data, cursor),
        FieldSchema::CompactArray(inner) => {
            let (len_opt, mut pos) = internal_read_compact_array_length(slice_from(data, cursor))?;
            let Some(n) = len_opt else {
                return Ok((py.None().into_pyobject(py)?.into_any().into(), pos));
            };
            let mut items = Vec::with_capacity(n);
            for _ in 0..n {
                let (item, sz) = read_field(py, inner, data, cursor + pos)?;
                items.push(item);
                pos += sz;
            }
            let tuple = PyTuple::new(py, items)?;
            Ok((tuple.into_any().into(), pos))
        }
        FieldSchema::LegacyArray(inner) => {
            let (length_i32, mut pos) = internal_read_int32(slice_from(data, cursor))?;
            if length_i32 == -1 {
                return Ok((py.None().into_pyobject(py)?.into_any().into(), pos));
            }
            if length_i32 < 0 {
                return Err(PyValueError::new_err("negative array length"));
            }
            let n = length_i32 as usize;
            let mut items = Vec::with_capacity(n);
            for _ in 0..n {
                let (item, sz) = read_field(py, inner, data, cursor + pos)?;
                items.push(item);
                pos += sz;
            }
            let tuple = PyTuple::new(py, items)?;
            Ok((tuple.into_any().into(), pos))
        }
    }
}

/// Parse one entity from `data` starting at absolute byte offset `base`.
/// Returns `(entity, bytes_consumed)`.
pub(crate) fn parse_entity(
    py: Python<'_>,
    schema: &EntitySchema,
    data: &[u8],
    base: usize,
) -> PyResult<(Py<PyAny>, usize)> {
    let mut cursor: usize = base;

    if schema.nullable {
        let (marker, s) = internal_read_int8(slice_from(data, cursor))?;
        cursor += s;
        if marker == -1 {
            return Ok((
                py.None().into_pyobject(py)?.into_any().into(),
                cursor - base,
            ));
        }
    }

    // Allocate the entity via tp_alloc, bypassing the transient kwargs PyDict and
    // the Python-level __init__ call.  All Kafka schema dataclasses use slots=True
    // with no __post_init__, so PyObject_GenericSetAttr writes the same
    // member_descriptor slots that __init__ would have written, without the
    // overhead of dict creation, dict lookup, and Python function dispatch.
    // Slot memory is zeroed by PyType_GenericAlloc; NULL slots are safe for GC
    // traversal (Py_VISIT skips NULL), so partial initialisation during parsing is
    // safe even if a GC cycle runs between attribute writes.
    let obj = unsafe {
        let tp = schema.entity_type.as_ptr() as *mut pyo3::ffi::PyTypeObject;
        let raw = pyo3::ffi::PyType_GenericAlloc(tp, 0);
        if raw.is_null() {
            return Err(pyo3::PyErr::fetch(py));
        }
        Bound::from_owned_ptr(py, raw)
    };

    for (py_name, field_schema) in &schema.field_schemas {
        let (val, sz) = read_field(py, field_schema, data, cursor)?;
        unsafe {
            if pyo3::ffi::PyObject_GenericSetAttr(
                obj.as_ptr(),
                py_name.bind(py).as_ptr(),
                val.as_ptr(),
            ) < 0
            {
                return Err(pyo3::PyErr::fetch(py));
            }
        }
        cursor += sz;
    }

    if !schema.flexible {
        return Ok((obj.into_any().unbind(), cursor - base));
    }

    let (num_tagged, nsize) = readers::internal_read_unsigned_varint(slice_from(data, cursor))?;
    cursor += nsize;

    let mut tagged_vals: Vec<Option<Py<PyAny>>> = (0..schema.tagged_field_defaults.len())
        .map(|_| None)
        .collect();

    for _ in 0..num_tagged {
        let (field_tag, t1) = readers::internal_read_unsigned_varint(slice_from(data, cursor))?;
        cursor += t1;
        let (_, t2) = readers::internal_read_unsigned_varint(slice_from(data, cursor))?;
        cursor += t2;
        let key = field_tag as u64;
        let (idx, field_schema) = schema.tagged_field_schemas.get(&key).ok_or_else(|| {
            PyKeyError::new_err(format!("Unknown tagged field tag: {}", field_tag))
        })?;
        let (val, sz) = read_field(py, field_schema, data, cursor)?;
        tagged_vals[*idx] = Some(val);
        cursor += sz;
    }

    for (i, (py_name, implicit_default)) in schema.tagged_field_defaults.iter().enumerate() {
        let val = match tagged_vals[i].take() {
            Some(v) => v.into_bound(py).into_any(),
            None => implicit_default.bind(py).to_owned(),
        };
        unsafe {
            if pyo3::ffi::PyObject_GenericSetAttr(
                obj.as_ptr(),
                py_name.bind(py).as_ptr(),
                val.as_ptr(),
            ) < 0
            {
                return Err(pyo3::PyErr::fetch(py));
            }
        }
    }

    Ok((obj.into_any().unbind(), cursor - base))
}

fn primitive_kind_from_kafka(
    kafka_type: &str,
    flexible: bool,
    optional: bool,
) -> PyResult<PrimitiveKind> {
    let k = match (kafka_type, flexible, optional) {
        ("int8", _, false) => PrimitiveKind::Int8,
        ("int16", _, false) => PrimitiveKind::Int16,
        ("int32", _, false) => PrimitiveKind::Int32,
        ("int64", _, false) => PrimitiveKind::Int64,
        ("uint8", _, false) => PrimitiveKind::UInt8,
        ("uint16", _, false) => PrimitiveKind::UInt16,
        ("uint32", _, false) => PrimitiveKind::UInt32,
        ("uint64", _, false) => PrimitiveKind::UInt64,
        ("float64", _, false) => PrimitiveKind::Float64,
        ("string", true, false) => PrimitiveKind::CompactString,
        ("string", true, true) => PrimitiveKind::CompactStringNull,
        ("string", false, false) => PrimitiveKind::LegacyString,
        ("string", false, true) => PrimitiveKind::NullableLegacyString,
        ("bytes" | "records", true, false) => PrimitiveKind::CompactBytes,
        ("bytes" | "records", true, true) => PrimitiveKind::CompactBytesNull,
        ("bytes" | "records", false, false) => PrimitiveKind::LegacyBytes,
        ("bytes" | "records", false, true) => PrimitiveKind::NullableLegacyBytes,
        ("uuid", _, _) => PrimitiveKind::Uuid,
        ("bool", _, false) => PrimitiveKind::Bool,
        ("error_code", _, false) => PrimitiveKind::ErrorCode,
        ("timedelta_i32", _, false) => PrimitiveKind::TimedeltaI32,
        ("timedelta_i64", _, false) => PrimitiveKind::TimedeltaI64,
        ("datetime_i64", _, false) => PrimitiveKind::DatetimeI64,
        ("datetime_i64", _, true) => PrimitiveKind::DatetimeI64Null,
        _ => {
            return Err(pyo3::exceptions::PyNotImplementedError::new_err(format!(
                "Unsupported primitive for native parsing: kafka_type={} flexible={} optional={}",
                kafka_type, flexible, optional
            )));
        }
    };
    Ok(k)
}

#[allow(clippy::too_many_arguments)]
pub(crate) fn build_field_schema(
    py: Python<'_>,
    _entity_type: &Bound<'_, PyType>,
    field: &Bound<'_, PyAny>,
    is_request_header: bool,
    is_tagged_field: bool,
    classify_field: &Bound<'_, PyAny>,
    get_schema_field_type: &Bound<'_, PyAny>,
    is_optional_fn: &Bound<'_, PyAny>,
    prim_field: &Bound<'_, PyAny>,
    prim_tuple_field: &Bound<'_, PyAny>,
    ent_field: &Bound<'_, PyAny>,
    ent_tuple_field: &Bound<'_, PyAny>,
    flexible: bool,
) -> PyResult<Arc<FieldSchema>> {
    let name: String = field.getattr("name")?.extract()?;
    if is_request_header && name == "client_id" {
        return Ok(Arc::new(FieldSchema::Primitive(
            PrimitiveKind::NullableLegacyString,
        )));
    }

    let field_class = classify_field.call1((field,))?.into_bound();

    let inner = if field_class.is_instance(prim_field)? {
        let kafka_type: String = get_schema_field_type.call1((field,))?.extract()?;
        let optional: bool = is_optional_fn.call1((field,))?.extract::<bool>()? && !is_tagged_field;
        let kind = primitive_kind_from_kafka(&kafka_type, flexible, optional)?;
        Arc::new(FieldSchema::Primitive(kind))
    } else if field_class.is_instance(prim_tuple_field)? {
        let kafka_type: String = get_schema_field_type.call1((field,))?.extract()?;
        let kind = primitive_kind_from_kafka(&kafka_type, flexible, false)?;
        Arc::new(FieldSchema::Primitive(kind))
    } else if field_class.is_instance(ent_field)? {
        let nested_type: Py<PyType> = field_class.getattr("type_")?.extract()?;
        let inner_nullable: bool = is_optional_fn.call1((field,))?.extract()?;
        let bound = nested_type.bind(py);
        let schema = get_or_compile_schema(py, bound, inner_nullable)?;
        Arc::new(FieldSchema::Entity { schema })
    } else if field_class.is_instance(ent_tuple_field)? {
        let nested_type: Py<PyType> = field_class.getattr("type_")?.extract()?;
        let bound = nested_type.bind(py);
        let schema = get_or_compile_schema(py, bound, false)?;
        Arc::new(FieldSchema::Entity { schema })
    } else {
        return Err(PyValueError::new_err("unsupported field classification"));
    };

    let is_array =
        field_class.is_instance(prim_tuple_field)? || field_class.is_instance(ent_tuple_field)?;
    if is_array {
        Ok(if flexible {
            Arc::new(FieldSchema::CompactArray(inner))
        } else {
            Arc::new(FieldSchema::LegacyArray(inner))
        })
    } else {
        Ok(inner)
    }
}

pub(crate) fn compile_entity_schema(
    py: Python<'_>,
    entity_type: &Bound<'_, PyType>,
    nullable: bool,
) -> PyResult<Arc<EntitySchema>> {
    let flexible: bool = entity_type.getattr("__flexible__")?.extract()?;
    let introspect = PyModule::import(py, "kio.serial._introspect")?;
    let prim_field = introspect.getattr("PrimitiveField")?;
    let prim_tuple_field = introspect.getattr("PrimitiveTupleField")?;
    let ent_field = introspect.getattr("EntityField")?;
    let ent_tuple_field = introspect.getattr("EntityTupleField")?;
    let get_schema_field_type = introspect.getattr("get_schema_field_type")?;
    let classify_field = introspect.getattr("classify_field")?;
    let is_optional_fn = introspect.getattr("is_optional")?;
    let get_field_tag = introspect.getattr("get_field_tag")?;
    let implicit_defaults = PyModule::import(py, "kio.serial._implicit_defaults")?;
    let get_tagged_field_default = implicit_defaults.getattr("get_tagged_field_default")?;
    let dataclasses = PyModule::import(py, "dataclasses")?;
    let fields_fn = dataclasses.getattr("fields")?;
    let fields_obj = fields_fn.call1((entity_type,))?;

    let type_name: String = entity_type.getattr("__name__")?.extract()?;
    let is_request_header = type_name == "RequestHeader";

    let mut field_schemas: Vec<(Py<PyString>, Arc<FieldSchema>)> = Vec::new();
    let mut tagged_field_schemas: HashMap<u64, (usize, Arc<FieldSchema>)> = HashMap::new();
    let mut tagged_field_defaults: Vec<(Py<PyString>, Py<PyAny>)> = Vec::new();

    for field in fields_obj.try_iter()? {
        let field = field?;
        let tag_any = get_field_tag.call1((&field,))?;
        let tag_opt: Option<u64> = if tag_any.is_none() {
            None
        } else {
            Some(tag_any.extract::<u64>()?)
        };
        let is_tagged_field = tag_opt.is_some();
        let field_schema = build_field_schema(
            py,
            entity_type,
            &field,
            is_request_header,
            is_tagged_field,
            &classify_field,
            &get_schema_field_type,
            &is_optional_fn,
            &prim_field,
            &prim_tuple_field,
            &ent_field,
            &ent_tuple_field,
            flexible,
        )?;
        let field_name: String = field.getattr("name")?.extract()?;
        // Pre-allocate the Python string for this field name once at schema-compile
        // time so every subsequent parse reuses the same object.
        let py_name: Py<PyString> = PyString::new(py, &field_name).unbind();
        if let Some(tag) = tag_opt {
            let idx = tagged_field_defaults.len();
            tagged_field_schemas.insert(tag, (idx, Arc::clone(&field_schema)));
            let implicit_default = get_tagged_field_default.call1((&field,))?.into();
            tagged_field_defaults.push((py_name, implicit_default));
        } else {
            field_schemas.push((py_name, field_schema));
        }
    }

    if !tagged_field_schemas.is_empty() && !flexible {
        return Err(PyValueError::new_err(
            "Found tagged fields on a non-flexible model",
        ));
    }

    Ok(Arc::new(EntitySchema {
        entity_type: entity_type.clone().unbind(),
        flexible,
        nullable,
        field_schemas,
        tagged_field_schemas,
        tagged_field_defaults,
    }))
}

pub(crate) fn get_or_compile_schema(
    py: Python<'_>,
    entity_type: &Bound<'_, PyType>,
    nullable: bool,
) -> PyResult<Arc<EntitySchema>> {
    let key = (entity_type.as_ptr() as usize, nullable);
    {
        let guard = SCHEMA_CACHE.lock().expect("schema cache poisoned");
        if let Some(p) = guard.get(&key) {
            return Ok(p.clone());
        }
    }
    let schema = compile_entity_schema(py, entity_type, nullable)?;
    SCHEMA_CACHE
        .lock()
        .expect("schema cache poisoned")
        .insert(key, schema.clone());
    Ok(schema)
}
