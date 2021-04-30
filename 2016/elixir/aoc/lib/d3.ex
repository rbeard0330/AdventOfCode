defmodule D3 do
  def solve_part_1(input) do
    input
    |> input_to_lines
    |> Enum.map(&Enum.sort/1)
    |> Enum.filter(&is_valid/1)
    |> Enum.count()
  end

  def solve_part_2(input) do
    input
    |> input_to_lines
    |> Enum.chunk_every(3)
    |> Enum.flat_map(&read_columns/1)
    |> Enum.map(&Enum.sort/1)
    |> Enum.filter(&is_valid/1)
    |> IO.inspect
    |> Enum.count()
  end

  def input_to_lines(lines) do
    lines
    |> String.split("\n")
    |> Enum.map(&line_to_ints/1)
  end

  def line_to_ints(line) do
    line
    |> String.split()
    |> Enum.map(&Integer.parse/1)
    |> Enum.map(&(elem(&1, 0)))
  end

  def is_valid([s1, s2, s3]) do
    s1 + s2 > s3
  end

  def is_valid([]) do
    false
  end

  def read_columns([[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]) do
    [[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]]
  end

  def read_columns(_) do
    []
  end


end
