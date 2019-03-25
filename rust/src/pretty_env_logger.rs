#[macro_use]
extern crate log;
extern crate pretty_env_logger;
use chrono::Utc;

// RUST_LOG=info pretty_env_logger
pub fn main() {
    pretty_env_logger::init();
    info!("now: {} ", Utc::now());
}
