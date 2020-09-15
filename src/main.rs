// Hopefully some functions and such to take over a few python things.

use cpython::{Python, PyDict, PyResult};

fn main() { 
    let gil = Python::acquire_gil();
    hello(gil.python()).unwrap();
}

pub fn hello(py: Python) -> PyResult<()> {
    let sys = py.import("sys")?;
    let version: String = sys.get(py, "version")?.extract(py)?;

    let locals = PyDict::new(py);
    locals.set_item(py, "os", py.import("os")?)?;
    let user: String = py.eval("os.getenv('USER') or os.getenv('USERNAME')", None, Some(&locals))?.extract(py)?;
    println!("Hello {}, this is Python {}", user, version);
    Ok(())
}