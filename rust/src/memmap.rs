extern crate memmap;
use std::sync::mpsc;
use std::sync::mpsc::SyncSender;

use std::fs::File;
use memmap::{Mmap};
use std::str;

extern crate scoped_threadpool;
use scoped_threadpool::Pool;
use std::thread;
use std::thread::sleep;
use std::time::Duration;


const MESSAGE_BUF: usize = 20;


fn scan<'a> (mission: &Vec<&'a str>, input_slice: &'a  [u8], pool: &mut Pool,
             tx: &SyncSender<String>)  {
    pool.scoped(|scope| {
        for e in mission.iter().enumerate() {
            let tx = tx.clone();
            scope.execute(move || {
                if e.0 == 3 {
                    sleep(Duration::from_secs(1));
                }
                let m = std::str::from_utf8(input_slice).unwrap().to_string();
                //let m =  e.1;
                println!("{}",m);

                tx.send(m).unwrap();
            });
        }
    });
}


fn main() {
    let f = File::open("./scanme.txt").unwrap();
    let _l = f.metadata().unwrap().len() as usize;
    let mmap = unsafe { Mmap::map(&f).unwrap() };
    let mission = vec!["T0", "T1", "T2", "T3"];
    let n_threads = mission.len();
    let (tx, rx) = mpsc::sync_channel(MESSAGE_BUF);

    let merger = thread::spawn(move || {
        for i in 0..n_threads*4 {
            if i == 6 {
                sleep(Duration::from_secs(7));
            }
            println!("\tListening...");
            println!("\t\tGot: {:?}", rx.recv().expect("Err"));
        }
    });

    let mut pool = Pool::new(n_threads as u32); // no threads

    for i in 0..4 {
        let input = &mmap[10*i..10*(i+1)];
        scan(&mission, &input, &mut pool, &tx);
    }


    merger.join().unwrap();
    println!("All threads terminated.");

}
