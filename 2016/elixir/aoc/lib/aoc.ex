defmodule Aoc do
end

d1_input = File.read!("data/d1.txt")
IO.puts("D1, part 1")
IO.puts(D1.solve_part_1(d1_input))
IO.puts("D1, part 2")
IO.puts(D1.solve_part_2(d1_input))
d2_input = File.read!("data/d2.txt")
IO.puts("D2, part 1")
IO.puts(D2.solve_part_1(d2_input))
IO.puts(D2.solve_part_2(d2_input))
d3_input = File.read!("data/d3.txt")
IO.puts("D3, part 1")
IO.puts(D3.solve_part_1(d3_input))