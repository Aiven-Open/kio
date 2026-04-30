//! Entity and array reader callables exposed to Python.

use std::collections::HashMap;
use std::sync::{Arc, LazyLock, Mutex};

use pyo3::prelude::*;
use pyo3::types::{PyModule, PyTuple, PyType};

use crate::schema::{
    EntitySchema, FieldSchema, build_field_schema, get_or_compile_schema, parse_entity, read_field,
};

/// Cached `entity_reader(...)` callables (same identity semantics as `functools.cache`).
type ReaderCache = Mutex<HashMap<(usize, bool), Py<PyAny>>>;

static ENTITY_READER_CACHE: LazyLock<ReaderCache> = LazyLock::new(|| Mutex::new(HashMap::new()));

#[pyclass(name = "CompactArrayReader", frozen)]
struct CompactArrayReader {
    item_reader: Py<PyAny>,
}

#[pymethods]
impl CompactArrayReader {
    #[pyo3(signature = (buffer, offset))]
    fn __call__(
        &self,
        py: Python<'_>,
        buffer: Py<PyAny>,
        offset: usize,
    ) -> PyResult<(Py<PyAny>, usize)> {
        let slice = crate::readers::data_from_input(py, buffer.clone_ref(py), offset)?;
        let (length_opt, length_size) = crate::readers::internal_read_compact_array_length(slice)?;
        let Some(length) = length_opt else {
            return Ok((py.None().into_pyobject(py)?.into_any().into(), length_size));
        };
        let mut pos = length_size;
        let mut items = Vec::with_capacity(length);
        for _ in 0..length {
            let out = self
                .item_reader
                .call1(py, (buffer.clone_ref(py), offset + pos))?;
            let bound = out.bind(py);
            let tup = bound.cast::<PyTuple>()?;
            if tup.len() != 2 {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "item reader must return (value, size)",
                ));
            }
            let val: Py<PyAny> = tup.get_item(0)?.into();
            let consumed: usize = tup.get_item(1)?.extract()?;
            items.push(val);
            pos += consumed;
        }
        let tuple = PyTuple::new(py, items)?;
        Ok((tuple.into_any().into(), pos))
    }
}

#[pyclass(name = "LegacyArrayReader", frozen)]
struct LegacyArrayReader {
    item_reader: Py<PyAny>,
}

#[pymethods]
impl LegacyArrayReader {
    #[pyo3(signature = (buffer, offset))]
    fn __call__(
        &self,
        py: Python<'_>,
        buffer: Py<PyAny>,
        offset: usize,
    ) -> PyResult<(Py<PyAny>, usize)> {
        let slice = crate::readers::data_from_input(py, buffer.clone_ref(py), offset)?;
        let (length_i32, length_size) = crate::readers::internal_read_int32(slice)?;
        if length_i32 == -1 {
            return Ok((py.None().into_pyobject(py)?.into_any().into(), length_size));
        }
        if length_i32 < 0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "negative array length",
            ));
        }
        let length = length_i32 as usize;
        let mut pos = length_size;
        let mut items = Vec::with_capacity(length);
        for _ in 0..length {
            let out = self
                .item_reader
                .call1(py, (buffer.clone_ref(py), offset + pos))?;
            let bound = out.bind(py);
            let tup = bound.cast::<PyTuple>()?;
            if tup.len() != 2 {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "item reader must return (value, size)",
                ));
            }
            let val: Py<PyAny> = tup.get_item(0)?.into();
            let consumed: usize = tup.get_item(1)?.extract()?;
            items.push(val);
            pos += consumed;
        }
        let tuple = PyTuple::new(py, items)?;
        Ok((tuple.into_any().into(), pos))
    }
}

#[pyfunction]
#[pyo3(signature = (item_reader))]
pub fn compact_array_reader(py: Python<'_>, item_reader: Py<PyAny>) -> PyResult<Py<PyAny>> {
    Ok(Py::new(py, CompactArrayReader { item_reader })?.into_any())
}

#[pyfunction]
#[pyo3(signature = (item_reader))]
pub fn legacy_array_reader(py: Python<'_>, item_reader: Py<PyAny>) -> PyResult<Py<PyAny>> {
    Ok(Py::new(py, LegacyArrayReader { item_reader })?.into_any())
}

#[pyclass(name = "EntityReader", frozen)]
struct EntityReader {
    schema: Arc<EntitySchema>,
}

#[pymethods]
impl EntityReader {
    #[pyo3(signature = (buffer, offset))]
    fn __call__(
        &self,
        py: Python<'_>,
        buffer: Py<PyAny>,
        offset: usize,
    ) -> PyResult<(Py<PyAny>, usize)> {
        let data = crate::readers::data_from_input(py, buffer, offset)?;
        parse_entity(py, &self.schema, data, 0)
    }
}

#[pyclass(name = "FieldReader", frozen)]
struct FieldReader {
    schema: Arc<FieldSchema>,
}

#[pymethods]
impl FieldReader {
    #[pyo3(signature = (buffer, offset))]
    fn __call__(
        &self,
        py: Python<'_>,
        buffer: Py<PyAny>,
        offset: usize,
    ) -> PyResult<(Py<PyAny>, usize)> {
        let data = crate::readers::data_from_input(py, buffer, offset)?;
        read_field(py, &self.schema, data, 0)
    }
}

fn entity_reader_impl(
    py: Python<'_>,
    entity_type: &Bound<'_, PyType>,
    nullable: bool,
) -> PyResult<Py<PyAny>> {
    let key = (entity_type.as_ptr() as usize, nullable);
    {
        let guard = ENTITY_READER_CACHE
            .lock()
            .expect("entity reader cache poisoned");
        if let Some(cached) = guard.get(&key) {
            return Ok(cached.clone_ref(py));
        }
    }
    let schema = get_or_compile_schema(py, entity_type, nullable)?;
    let reader = Py::new(py, EntityReader { schema })?.into_any();
    ENTITY_READER_CACHE
        .lock()
        .expect("entity reader cache poisoned")
        .insert(key, reader.clone_ref(py));
    Ok(reader)
}

#[pyfunction]
#[pyo3(signature = (entity_type, nullable=false))]
pub fn entity_reader(
    py: Python<'_>,
    entity_type: Bound<PyType>,
    nullable: bool,
) -> PyResult<Py<PyAny>> {
    entity_reader_impl(py, &entity_type, nullable)
}

#[pyfunction]
pub fn get_field_reader(
    py: Python<'_>,
    entity_type: Bound<PyType>,
    field: Bound<PyAny>,
    is_request_header: bool,
    is_tagged_field: bool,
) -> PyResult<Py<PyAny>> {
    let introspect = PyModule::import(py, "kio.serial._introspect")?;
    let prim_field = introspect.getattr("PrimitiveField")?;
    let prim_tuple_field = introspect.getattr("PrimitiveTupleField")?;
    let ent_field = introspect.getattr("EntityField")?;
    let ent_tuple_field = introspect.getattr("EntityTupleField")?;
    let get_schema_field_type = introspect.getattr("get_schema_field_type")?;
    let classify_field = introspect.getattr("classify_field")?;
    let is_optional_fn = introspect.getattr("is_optional")?;
    let flexible: bool = entity_type.getattr("__flexible__")?.extract()?;
    let field_schema = build_field_schema(
        py,
        &entity_type,
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
    Ok(Py::new(
        py,
        FieldReader {
            schema: field_schema,
        },
    )?
    .into_any())
}
