
#![allow(warnings)]
use std::thread;

trait Foo {
    fn foo(&self);
}

struct Baz {
    pub data : Box<Foo + Send>
}

fn Bar(baz : Baz) {
    thread::spawn(move || {baz.data.foo()});
}

fn main() {

}
