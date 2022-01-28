use rust::{Interrupt, Intcoder, Modes, read_args};
use std::io;

const INPUT: &'static str = include_str!("../../inputs/prog.txt");

fn main() {
    let mut coder = Intcoder::new(INPUT.trim());
    let mut input = None;
    while input == None {
        println!("Enter an input");
        let mut buffer = String::new();
        io::stdin().read_line(&mut buffer).unwrap();
        input = match buffer.trim().parse() {
            Ok(v) => Some(v),
            Err(err) => {
                println!("{:?}", err);
                None
            }
        }
    }

    for output in coder.run_from_stored_input(vec![input.unwrap()].into_iter()) {
        println!("Output = {}", output)
    }

}