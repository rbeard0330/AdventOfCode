defmodule D4 do


  def solve_part_1(input) do
    re = ~r/^([a-z-]*)-([0-9]*)\[([a-z]{5})]/
    String.split(input)
    |> Enum.map(&(Regex.run(re, &1)))
    |> Enum.map(&process/1)
    |> Enum.sum
  end

  def process([_, s, code, checksum]) do
    expected = top_5_as_string(s)
    if expected == checksum do
      elem(Integer.parse(code), 0)
    else
      0
    end
  end

  def count_letters(s) do
    do_count_letters(s, %{})
  end

  defp do_count_letters(<<first :: bytes-size(1)>> <> "", map) do
    case first do
      "-" -> map
      char -> count_character(map, char)
    end
  end

  defp do_count_letters(<<first :: bytes-size(1)>> <> rest, map) do
    updated_map = case first do
                             "-" -> map
      char -> count_character(map, char)
    end
    do_count_letters(rest, updated_map)
  end


  defp count_character(counter, character) do
    current_count = Map.get(counter, character, 0)
    Map.put(counter, character, current_count + 1)
  end

  defp top_5_as_string(string) do
    string
    |> count_letters
    |> Map.to_list
    |> List.keysort(0)
    |> Enum.reverse
    |> List.keysort(1)
    |> Enum.reverse
    |> Enum.take(5)
    |> Enum.map(&(elem(&1, 0)))
    |> List.to_string

  end

end
