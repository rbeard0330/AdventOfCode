use rust::{Intcoder};
use itertools::{Itertools};
use std::cell::Cell;

const INPUT: &'static str = include_str!("../../inputs/d7.txt");

type CoderArray = Vec<Intcoder>;

fn main() {
    let mut coders = coders_from_input(INPUT.trim());
    println!("Part 1: {}", find_serial_max(&mut coders));
    println!("Part 2: {}", find_looped_max(&mut coders));
}

fn coders_from_input(data: &str) -> CoderArray {
    (0..5).into_iter().map(|_| Intcoder::new(data)).collect()
}

fn find_serial_max(coders: &mut CoderArray) -> i32 {
    (0..5_i32).into_iter()
        .permutations(5)
        .map(|settings| {
            set_phases(coders, settings);
            run_serially(coders)
        })
        .max()
        .unwrap()
}

fn find_looped_max(coders: &mut CoderArray) -> i32 {
    (5..10_i32).into_iter()
        .permutations(5)
        .map(|settings| {
            set_phases(coders, settings);
            run_looped(coders)
        })
        .max()
        .unwrap()
}

fn set_phases(coders: &mut CoderArray, phases: Vec<i32>) {
    coders.iter_mut()
        .zip(phases)
        .for_each(|(coder, phase)| {
            coder.reset();
            coder.push_input(phase);
        })
}

fn run_serially(coders: &mut CoderArray) -> i32 {
    match coders[0..5] {
        [ref mut c1, ref mut c2, ref mut c3, ref mut c4, ref mut c5] => {
            c1.push_input(0);
            let output1 = c1.run_without_input();
            let output2 = c2.run_from_stored_input(output1);
            let output3 = c3.run_from_stored_input(output2);
            let output4 = c4.run_from_stored_input(output3);
            c5.run_from_stored_input(output4).next().unwrap()
        },
        ref other => unreachable!("{:?}", other)
    }
}

fn run_looped(coders: &mut CoderArray) -> i32 {
    let mut next_input = Cell::new(0);
    match coders[0..5] {
        [ref mut c1, ref mut c2, ref mut c3, ref mut c4, ref mut c5] => {
            let output1 = c1.run_interactively(|out| {
                match out {
                    Some(_) => None,
                    None => Some(next_input.take())
                }
            });
            let output2 = c2.run_from_stored_input(output1);
            let output3 = c3.run_from_stored_input(output2);
            let mut output4 = c4.run_from_stored_input(output3);
            let output5 = c5.run_interactively(|out| {
                match out {
                    Some(val) => { next_input.set(val); None },
                    None => output4.next()
                }
            });
            for v in output5 {}
        },
        ref other => unreachable!("{:?}", other)
    };
    next_input.take()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_1() {
        let mut coders = coders_from_input("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0");
        assert_eq!(find_serial_max(&mut coders), 43210)
    }

    #[test]
    fn test_2() {
        let mut coders = coders_from_input("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0");
        assert_eq!(find_serial_max(&mut coders), 54321)
    }

    #[test]
    fn test_3() {
        let mut coders = coders_from_input("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0");
        assert_eq!(find_serial_max(&mut coders), 65210)
    }

    #[test]
    fn test_4() {
        let mut coders = coders_from_input("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5");
        assert_eq!(find_looped_max(&mut coders), 139629729)
    }

    #[test]
    fn test_5() {
        let mut coders = coders_from_input("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10");
        assert_eq!(find_looped_max(&mut coders), 18216);
    }
}