// SPDX-License-Identifier: (Apache-2.0 OR MIT)

use crate::exc::*;
use crate::ffi::PyDict_GET_SIZE;
use crate::opt::*;
use crate::serialize::encode::*;
use crate::typeref::*;
use crate::unicode::*;

use serde::ser::{Serialize, SerializeMap, Serializer};

use std::ptr::NonNull;

pub struct DataclassSerializer {
    ptr: *mut pyo3::ffi::PyObject,
    opts: Opt,
    default_calls: u8,
    recursion: u8,
    default: Option<NonNull<pyo3::ffi::PyObject>>,
}

impl DataclassSerializer {
    pub fn new(
        ptr: *mut pyo3::ffi::PyObject,
        opts: Opt,
        default_calls: u8,
        recursion: u8,
        default: Option<NonNull<pyo3::ffi::PyObject>>,
    ) -> Self {
        DataclassSerializer {
            ptr: ptr,
            opts: opts,
            default_calls: default_calls,
            recursion: recursion,
            default: default,
        }
    }
}

impl<'p> Serialize for DataclassSerializer {
    #[inline(never)]
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let fields = ffi!(PyObject_GetAttr(self.ptr, DATACLASS_FIELDS_STR));
        ffi!(Py_DECREF(fields));
        let len = unsafe { PyDict_GET_SIZE(fields) as usize };
        if unlikely!(len == 0) {
            return serializer.serialize_map(Some(0)).unwrap().end();
        }
        let mut map = serializer.serialize_map(None).unwrap();
        let mut pos = 0isize;
        let mut str_size: pyo3::ffi::Py_ssize_t = 0;
        let mut attr: *mut pyo3::ffi::PyObject = std::ptr::null_mut();
        let mut field: *mut pyo3::ffi::PyObject = std::ptr::null_mut();
        for _ in 0..=len - 1 {
            unsafe {
                pyo3::ffi::_PyDict_Next(
                    fields,
                    &mut pos,
                    &mut attr,
                    &mut field,
                    std::ptr::null_mut(),
                )
            };
            let field_type = ffi!(PyObject_GetAttr(field, FIELD_TYPE_STR));
            ffi!(Py_DECREF(field_type));
            if unsafe { field_type != FIELD_TYPE.as_ptr() } {
                continue;
            }
            {
                let data = read_utf8_from_str(attr, &mut str_size);
                if unlikely!(data.is_null()) {
                    err!(INVALID_STR);
                }
                let key_as_str = str_from_slice!(data, str_size);
                if key_as_str.as_bytes()[0] == b'_' {
                    continue;
                }
                map.serialize_key(key_as_str).unwrap();
            }

            let value = ffi!(PyObject_GetAttr(self.ptr, attr));
            ffi!(Py_DECREF(value));

            map.serialize_value(&SerializePyObject::new(
                value,
                self.opts,
                self.default_calls,
                self.recursion + 1,
                self.default,
            ))?
        }
        map.end()
    }
}
