#![allow(warnings)]
use std::ops::Deref;
use std::sync::{Mutex, MutexGuard, PoisonError};

fn with_mutex<T, F, O>(mutex: &Mutex<T>, f: F) -> Result<O, PoisonError<MutexGuard<T>>>
where
    F: FnOnce(&mut T) -> O,
{
    mutex.lock().map(|mut x| {
        f(&mut x)
    })
}

fn main() {
    let mutex = Mutex::new(2);
    //with_mutex(&mutex, |&mut x| println!("{}", x + 2));
    mutex.lock().map(|mut x| {

        x.deref()+ 3
    });
}
