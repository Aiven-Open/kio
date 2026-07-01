use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::PyModule;

static INTROSPECT_CACHE: PyOnceLock<IntrospectRefs> = PyOnceLock::new();

pub(crate) struct IntrospectRefs {
    pub PrimitiveField: Py<PyAny>,
    pub PrimitiveTupleField: Py<PyAny>,
    pub EntityField: Py<PyAny>,
    pub EntityTupleField: Py<PyAny>,
    pub get_schema_field_type: Py<PyAny>,
    pub classify_field: Py<PyAny>,
    pub is_optional: Py<PyAny>,
    pub get_field_tag: Py<PyAny>,
}

pub(crate) fn introspect(py: Python<'_>) -> PyResult<&'static IntrospectRefs> {
    INTROSPECT_CACHE.get_or_try_init(py, || {
        let module = PyModule::import(py, "kio.serial._introspect")?;
        Ok(IntrospectRefs {
            PrimitiveField: module.getattr("PrimitiveField")?.unbind(),
            PrimitiveTupleField: module.getattr("PrimitiveTupleField")?.unbind(),
            EntityField: module.getattr("EntityField")?.unbind(),
            EntityTupleField: module.getattr("EntityTupleField")?.unbind(),
            get_schema_field_type: module.getattr("get_schema_field_type")?.unbind(),
            classify_field: module.getattr("classify_field")?.unbind(),
            is_optional: module.getattr("is_optional")?.unbind(),
            get_field_tag: module.getattr("get_field_tag")?.unbind(),
        })
    })
}
