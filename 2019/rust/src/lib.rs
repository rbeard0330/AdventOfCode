const TAPE_LENGTH: usize = 50_000;

type Int = i32;

#[derive(Debug)]
pub struct Intcoder {
    pub position: usize,
    relative_base: usize,
    tape: [Int; TAPE_LENGTH],
    inputs: Vec<i32>,
    initial_data: Vec<i32>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Interrupt {
    Halt(i32),
    InputRequired,
    Output(i32),
    SegmentationFault(isize),
    InvalidOpcode(i32),
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Mode {
    Immediate,
    Position,
    Relative,
}

impl Intcoder {
    pub fn new<T>(data: T) -> Intcoder
        where T: AsRef<str>
    {
        let tape = [0i32; TAPE_LENGTH];
        let numbers = data.as_ref()
            .split(",")
            .map(|value| value.parse::<i32>().unwrap())
            .collect::<Vec<_>>();
        let mut result = Intcoder {
            position: 0,
            relative_base: 0,
            tape,
            inputs: Vec::new(),
            initial_data: numbers.clone(),
        };
        result.reset();
        result
    }

    pub fn reset(&mut self) {
        self.position = 0;
        self.initial_data.clone().iter().enumerate()
            .for_each(|(i, value)| self.write_offset(i, *value));
        self.inputs = Vec::new();
    }

    pub fn initialize<Init>(&mut self, initializer: Init)
        where Init: Fn(&mut Self) -> ()
    {
        self.reset();
        initializer(self);
    }

    pub fn load_from(&self, offset: usize) -> Int {
        let target = self.read_offset(offset);
        self.read_absolute(target as usize)
    }

    pub fn push_input(&mut self, input: i32) {
        self.inputs.push(input)
    }

    pub fn get_input(&mut self) -> Option<i32> {
        if self.inputs.len() == 0 {
            None
        } else {
            Some(self.inputs.remove(0))
        }
    }

    pub fn load(&self, offset: usize, mode: Mode) -> Int {
        match mode {
            Mode::Immediate => self.read_offset(offset),
            Mode::Position => self.load_from(offset),
            Mode::Relative => self.load_from(self.relative_base + offset),
        }
    }

    pub fn store(&mut self, offset: usize, mode: Mode, value: Int) {
        let target = self.read_offset(offset) as usize;
        match mode {
            Mode::Immediate => panic!("Attempted to store in immediate mode"),
            Mode::Position => self.write_absolute(target, value),
            Mode::Relative => self.write_absolute(self.relative_base + target, value),
        }
    }

    pub fn read_offset(&self, offset: usize) -> Int {
        return self.read_absolute(self.position + offset)
    }

    pub fn read_absolute(&self, position: usize) -> Int {

        return self.tape[position];
    }

    pub fn write_offset(&mut self, offset: usize, value: Int) {
        self.write_absolute(self.position  + offset, value)
    }

    pub fn write_absolute(&mut self, position: usize, value: Int) {
        self.tape[position] = value;
    }

    fn tick(&mut self) -> Option<Interrupt> {
        dbg!(self.position, self.read_offset(0));
        println!("{:?}", &self.tape[..30]);
        match self.read_offset(0) {
            99 => {
                Some(Interrupt::Halt(self.read_absolute(0)))
            }
            inst if inst % 100 == 1 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);
                self.store(3, modes.next().unwrap(), v1 + v2);
                self.position += 4;
                None
            }
            inst if inst % 100 == 2 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);
                self.store(3, modes.next().unwrap(), v1 * v2);
                self.position += 4;
                None
            }
            inst if inst % 100 == 3 => {
                let mut modes = Modes::new(inst);
                match self.get_input() {
                    Some(value) => {
                        self.store(1, modes.next().unwrap(), value);
                        self.position += 2;
                        None
                    }
                    None => Some(Interrupt::InputRequired)
                }
            }
            inst if inst % 100 == 4 => {
                let mut modes = Modes::new(inst);
                let [value] = read_args(self, &mut modes);
                self.position += 2;
                Some(Interrupt::Output(value))
            }
            inst if inst % 100 == 5 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);
                if v1 != 0 {
                    self.position = v2 as usize;
                } else {
                    self.position += 3;
                }
                None
            }

            inst if inst % 100 == 6 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);
                if v1 == 0 {
                    self.position = v2 as usize;
                } else {
                    self.position += 3;
                }
                None
            }
            inst if inst % 100 == 7 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);

                let value = if v1 < v2 { 1 } else { 0 };
                self.store(3, modes.next().unwrap(), value);
                self.position += 4;
                None
            }
            inst if inst % 100 == 8 => {
                let mut modes = Modes::new(inst);
                let [v1, v2] = read_args(self, &mut modes);

                let value = if v1 == v2 { 1 } else { 0 };
                self.store(3, modes.next().unwrap(), value);
                self.position += 4;
                None
            }
            unknown => Some(Interrupt::InvalidOpcode(unknown)),
        }
    }

    pub fn run(&mut self) -> Interrupt
    {
        loop {
            match self.tick() {
                Some(Interrupt::Output(v)) => println!("Output: {}", v),
                Some(interrupt) => return interrupt,
                _ => {}
            }
        }
    }

    pub fn run_without_input<'a>(&'a mut self) -> impl Iterator<Item=i32> + 'a {
        OutputStream { coder: self, input_source: vec![].into_iter() }
    }

    pub fn run_from_stored_input<'a>(&'a mut self, input_source: impl Iterator<Item=i32> + 'a) -> impl Iterator<Item=i32> + 'a {
        OutputStream { coder: self, input_source }
    }

    pub fn run_interactively<'a>(&'a mut self, user: impl FnMut(Option<Int>) -> Option<Int> + 'a) -> impl Iterator<Item=i32> + 'a {
        InteractiveOutputStream { coder: self, user: Box::new(user) }
    }
}

struct OutputStream<'a, Input: Iterator<Item=Int> + 'a> {
    coder: &'a mut Intcoder,
    input_source: Input,
}

impl<'a, Input: Iterator<Item=Int> + 'a> Iterator for OutputStream<'a, Input> {
    type Item = Int;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            match self.coder.tick() {
                Some(Interrupt::Output(v)) => return Some(v),
                Some(Interrupt::InputRequired) => {
                    if let Some(next_input) = self.input_source.next() {
                        self.coder.push_input(next_input);
                    } else {
                        panic!("Input source terminated while input was still required")
                    }
                }
                Some(Interrupt::Halt(_)) => return None,
                Some(interrupt) => panic!("Unhandled interrupt {:?}", interrupt),
                None => {}
            }
        }
    }
}

struct InteractiveOutputStream<'a, User: FnMut(Option<Int>) -> Option<Int>> {
    coder: &'a mut Intcoder,
    user: Box<User>,
}

impl<'a, User: FnMut(Option<Int>) -> Option<Int>> Iterator for InteractiveOutputStream<'a, User> {
    type Item = Int;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            match self.coder.tick() {
                Some(Interrupt::Output(v)) => {
                    if let Some(next_input) = (self.user)(Some(v)) {
                        self.coder.push_input(next_input);
                    }
                    return Some(v);
                }
                Some(Interrupt::InputRequired) => {
                    if let Some(next_input) = (self.user)(None) {
                        self.coder.push_input(next_input);
                    } else {
                        panic!("Input source terminated while input was still required")
                    }
                }
                Some(Interrupt::Halt(_)) => return None,
                Some(interrupt) => panic!("Unhandled interrupt {:?}", interrupt),
                None => {}
            }
        }
    }
}

#[derive(Debug)]
pub struct Modes(i32);

impl Modes {
    pub fn new(value: i32) -> Self {
        return Modes(value / 100);
    }
}

impl Iterator for Modes {
    type Item = Mode;

    fn next(&mut self) -> Option<Self::Item> {
        let remainder = self.0 % 10;
        self.0 /= 10;
        match remainder {
            0 => Some(Mode::Position),
            1 => Some(Mode::Immediate),
            2 => Some(Mode::Relative),
            _ => unreachable!("Illegal mode: {:?}", remainder)
        }
    }
}

pub fn read_args<const N: usize>(coder: &mut Intcoder, modes: &mut Modes) -> [Int; N] {
    let mut result = [0; N];
    (0..N).into_iter().for_each(|i| result[i] = coder.load(i + 1, modes.next().unwrap()));
    result
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn can_write() {
        let mut coder = Intcoder::new("1,2,3,4");
        coder.write_offset(1, 100);
        assert_eq!(coder.read_offset(1), 100);
    }

    #[test]
    fn can_read() {
        let coder = Intcoder::new("1,2,3,4");
        assert_eq!(coder.read_offset(0), 1);
        assert_eq!(coder.read_offset(3), 4);
        assert_eq!(coder.read_offset(110), 0);
    }

    #[test]
    fn loads() {
        let coder = Intcoder::new("4,2,0,1,100");
        assert_eq!(coder.load_from(0), 100);
        assert_eq!(coder.load_from(1), 0);
        assert_eq!(coder.load_from(2), 4);
        assert_eq!(coder.load_from(3), 2);
        assert_eq!(coder.load_from(4), 0);
    }

    #[test]
    fn full_test() {
        let mut coder = Intcoder::new("1,9,10,3,2,3,11,0,99,30,40,50");
        //assert_eq!(coder.run(|_| {}, default_isa), Interrupt::Halt(3500));

        assert_eq!(Intcoder::new("1,1,1,4,99,5,6,0,99").run(), Interrupt::Halt(30))
    }
}