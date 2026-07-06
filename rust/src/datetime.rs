//! Construct `datetime.datetime` and `datetime.timedelta` via the C API.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDateTime, PyDelta, PyTzInfo};

const MICROSECONDS_PER_SECOND: i64 = 1_000_000;
const MICROSECONDS_PER_DAY: i64 = 86_400 * MICROSECONDS_PER_SECOND;

fn timedelta_component_i32(value: i64, component: &str) -> PyResult<i32> {
    i32::try_from(value)
        .map_err(|_| PyValueError::new_err(format!("timedelta {component} overflow")))
}

pub(crate) fn timedelta_from_milliseconds(
    py: Python<'_>,
    milliseconds: i64,
) -> PyResult<Py<PyAny>> {
    let mut microseconds = milliseconds
        .checked_mul(1_000)
        .ok_or_else(|| PyValueError::new_err("timedelta milliseconds overflow"))?;
    let days = timedelta_component_i32(microseconds.div_euclid(MICROSECONDS_PER_DAY), "days")?;
    microseconds = microseconds.rem_euclid(MICROSECONDS_PER_DAY);
    let seconds =
        timedelta_component_i32(microseconds.div_euclid(MICROSECONDS_PER_SECOND), "seconds")?;
    microseconds = microseconds.rem_euclid(MICROSECONDS_PER_SECOND);
    let microseconds = timedelta_component_i32(microseconds, "microseconds")?;
    Ok(PyDelta::new(py, days, seconds, microseconds, true)?
        .into_any()
        .unbind())
}

pub(crate) fn datetime_from_timestamp_milliseconds(
    py: Python<'_>,
    timestamp_ms: i64,
) -> PyResult<Py<PyAny>> {
    let timestamp_seconds = (timestamp_ms as f64) / 1000.0;
    let utc = PyTzInfo::utc(py)?;
    Ok(
        PyDateTime::from_timestamp(py, timestamp_seconds, Some(&utc))?
            .into_any()
            .unbind(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use pyo3::types::PyDict;
    use std::ffi::CString;

    fn with_python<F>(f: F)
    where
        F: for<'py> FnOnce(Python<'py>),
    {
        Python::initialize();
        Python::attach(f);
    }

    fn assert_eq_timedelta_milliseconds(py: Python<'_>, delta: &Bound<'_, PyAny>, ms: i64) {
        let code = CString::new(format!(
            "import datetime; assert delta == datetime.timedelta(milliseconds={ms})"
        ))
        .expect("test code should not contain nul bytes");
        let locals = PyDict::new(py);
        locals.set_item("delta", delta).expect("locals setup");
        py.run(code.as_c_str(), None, Some(&locals))
            .expect("timedelta should match Python constructor");
    }

    fn assert_eq_datetime_from_timestamp_milliseconds(
        py: Python<'_>,
        dt: &Bound<'_, PyAny>,
        timestamp_ms: i64,
    ) {
        let code = CString::new(format!(
            "import datetime; \
             assert dt == datetime.datetime.fromtimestamp({} / 1000, datetime.UTC)",
            timestamp_ms
        ))
        .expect("test code should not contain nul bytes");
        let locals = PyDict::new(py);
        locals.set_item("dt", dt).expect("locals setup");
        py.run(code.as_c_str(), None, Some(&locals))
            .expect("datetime should match Python fromtimestamp");
    }

    #[test]
    fn timedelta_from_milliseconds_matches_python() {
        with_python(|py| {
            for ms in [
                0,
                1,
                -1,
                1_500,
                -1_500,
                86_400_000,
                -86_400_000,
                200_000_000_000_000,
                -200_000_000_000_000,
            ] {
                let delta = timedelta_from_milliseconds(py, ms)
                    .expect("timedelta construction should succeed");
                let delta = delta.bind(py);
                assert_eq_timedelta_milliseconds(py, &delta, ms);
            }
        });
    }

    #[test]
    fn timedelta_from_milliseconds_rejects_overflow() {
        with_python(|py| {
            let err = timedelta_from_milliseconds(py, i64::MAX)
                .expect_err("extreme milliseconds should fail");
            assert!(err.to_string().contains("overflow"));
        });
    }

    #[test]
    fn datetime_from_timestamp_milliseconds_matches_python() {
        with_python(|py| {
            for timestamp_ms in [0, 1, 1_500, 1_672_531_200_000] {
                let dt = datetime_from_timestamp_milliseconds(py, timestamp_ms)
                    .expect("datetime construction should succeed");
                let dt = dt.bind(py);
                assert_eq_datetime_from_timestamp_milliseconds(py, &dt, timestamp_ms);
            }
        });
    }
}
