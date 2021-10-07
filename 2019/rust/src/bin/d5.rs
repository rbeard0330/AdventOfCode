use rust::{Interrupt, Intcoder, Modes, read_args};

const INPUT: &'static str = include_str!("../../inputs/d5.txt");
fn main() {
    let mut coder = Intcoder::new(INPUT.trim());
    println!("Part 1");

    for output in coder.run_from_stored_input(vec![1].into_iter()) {
        println!("Output = {}", output)
    }
    println!("Part 2");
    coder.reset();
    for output in coder.run_from_stored_input(vec![5].into_iter()) {
        println!("Output = {}", output)
    }

}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part_5_test() {
        let mut coder = Intcoder::new("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99");
        coder.push_input(7);
        println!("{:?}", coder.run())
    }
}