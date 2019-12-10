from intcode import IntcodeProgram
import unittest

class TestJumps(unittest.TestCase):
    def test1(self):
        seq = [int(i) for i in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(',')]
        program = IntcodeProgram(seq, [0])
        program.runUntilStop()
        self.assertEqual(program.outputStream[0], 0)
    
    def test2(self):
        seq = [int(i) for i in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(',')]
        program = IntcodeProgram(seq, [36])
        program.runUntilStop()
        self.assertEqual(program.outputStream[0], 1)

class TestDay9Examples(unittest.TestCase):
    def test1(self):
        seq = [104,1125899906842624,99]
        program = IntcodeProgram(seq)
        program.runUntilStop()
        self.assertEqual(program.outputStream[0], 1125899906842624)

    def test2(self):
        seq = [1102,34915192,34915192,7,4,7,99,0]
        program = IntcodeProgram(seq)
        program.runUntilStop()
        self.assertLess(1e15, program.outputStream[0]) #"should output a 16-digit number"
    
    def test3(self):
        seq = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        program = IntcodeProgram(seq)
        program.runUntilStop()
        self.assertEqual(program.outputStream, seq)

class TestDay9A(unittest.TestCase):
    def test1(self):
        with open('nate/inputs/in9.txt', 'r') as f:
            code = [int(i) for i in f.readline().strip().split(',')]
        program = IntcodeProgram(code, [1])
        program.runUntilOutput()
        self.assertEqual(program.outputStream[0], 3013554615)

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()