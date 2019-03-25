use std::thread;

trait Foo
{
    fn foo(&self);
}

struct Baz
{
    pub data : Box<Foo>
}

fn Bar(baz : Baz) {
    thread::spawn(move || {baz.data.foo()});
}

fn main(){}
