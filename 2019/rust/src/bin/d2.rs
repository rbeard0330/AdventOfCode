use rust::{Intcoder, Interrupt};
// 190643 too low
const INPUT: &'static str = include_str!("../../inputs/d2.txt");

fn main() {
    let mut coder = Intcoder::new(INPUT.trim());
    initialize(&mut coder, 1, 12);
    println!("Part 1: {:?}", coder.run());
    let (noun, verb) = find_noun_and_verb(19690720);
    println!("Part 2: {:?}", 100 * noun + verb);
    initialize(&mut coder, noun, verb);
    assert_eq!(coder.run(), Interrupt::Halt(19690720));
}

fn initialize(coder: &mut Intcoder, noun: i32, verb: i32) {
    coder.initialize(|c| {
        c.write_absolute(1, noun);
        c.write_absolute(2, verb);
    });
}

fn find_noun_and_verb(target: i32) -> (i32, i32) {
    let mut coder = Intcoder::new(INPUT.trim());
    for noun in 0..100 {
        for verb in 0..100 {
            initialize(&mut coder, noun, verb);
            if let Interrupt::Halt(value) = coder.run() {
                if value == target {return (noun, verb)} }
        }
    }
    panic!("No value found!")
}