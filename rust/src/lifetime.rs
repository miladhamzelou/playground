#![allow(warnings)]

struct S{
}

fn main() {

    let mut a: Option<(S, S)> = None;
    let s1 = S{};
    let s2 = S{};
    a = Some((s1, s2));

}
