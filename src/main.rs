// Hopefully some functions and such to take over a few python things.

use cpython::{Python, PyDict, PyResult};

fn main() { 
    let gil = Python::acquire_gil();
    get_sys(gil.python()).unwrap();
}

pub fn get_py_path(py: Python) -> PyResult<()> {
    let locals = PyDict::new(py);
    locals.set_item(py, "sys", py.import("sys")?)?; 
    let path: String = py.eval("str(sys.path)", None, Some(&locals))?.extract(py)?;
    println!("Python path: {}", path);
    Ok(())
}

pub fn get_sys(py: Python) -> PyResult<()> {
    let sys = py.import("sys")?;
    let version: String = sys.get(py, "version")?.extract(py)?;

    let locals = PyDict::new(py);
    locals.set_item(py, "os", py.import("os")?)?;
    let user: String = py.eval("os.getenv('USER') or os.getenv('USERNAME')", None, Some(&locals))?.extract(py)?;
    println!("Hello {}, this is Python {}", user, version);
    Ok(())
}