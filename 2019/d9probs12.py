from util.intcode import AdvancedIntcoder, parse_input


tape = parse_input("d9.txt")
a = AdvancedIntcoder(tape, [1])
print("Part 1:")
a.run()
a.reset([2], clear_tape=True)
print("Part 2:")
a.run()
