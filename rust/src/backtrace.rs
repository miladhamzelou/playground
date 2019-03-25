extern crate backtrace;

fn main() {
    let mut depth = 3;
    backtrace::trace(|frame| {
        let ip = frame.ip();
        backtrace::resolve(ip, |symbol| {

            if let Some(filename) = symbol.filename() {
                if let Some(lineno) = symbol.lineno() {
                    if let Some(name) = symbol.name() {
                        println!("{} {}:{}", name, filename.display(), lineno);
                    }
                }
            }
        });
        depth -= 1;
        depth>0
    });
}
