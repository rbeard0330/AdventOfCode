defmodule D2 do
  def solve_part_1(input) do
    resolve_instructions(input)
      |> Enum.map(&Integer.to_string/1)
      |> Enum.reduce("", &(&1 <> &2))
  end

  def solve_part_2(input) do
    resolve_instructions_var(input)
      |> Enum.map(&encode/1)
      |> Enum.reduce("", &(&1 <> &2))
  end

  def encode(num) do
    case num do
      num when num < 10 -> Integer.to_string(num)
      num -> <<?A + num - 10>>
    end
  end

  def resolve_instructions(instructions) do
    do_resolve_next(instructions, 5, [])
  end

  def do_resolve_next("", key, pressed) do
    [key | pressed ]
  end

  def do_resolve_next("\n" <> tail, key, pressed) do
    do_resolve_next(tail, key, [key | pressed])
  end

  def do_resolve_next(<<head::bytes-size(1)>> <> tail, key, pressed) do
    do_resolve_next(tail, take_step(key, head), pressed)
  end

  def resolve_instructions_var(instructions) do
    do_resolve_next_var(instructions, 5, [])
  end

  def do_resolve_next_var("", key, pressed) do
    [key | pressed ]
  end

  def do_resolve_next_var("\n" <> tail, key, pressed) do
    do_resolve_next_var(tail, key, [key | pressed])
  end

  def do_resolve_next_var(<<head::bytes-size(1)>> <> tail, key, pressed) do
    do_resolve_next_var(tail, take_step_variant(key, head), pressed)
  end

  def take_step(current_key, "U") do
    case current_key do
      key when key < 4 -> key
      key -> key - 3
    end
  end

  def take_step(current_key, "D") do
    case current_key do
      key when key > 6 -> key
      key -> key + 3
    end
  end

  def take_step(current_key, "L") do
    case current_key do
      key when rem(key, 3) == 1 -> key
      key -> key - 1
    end
  end

  def take_step(current_key, "R") do
    case current_key do
      key when rem(key, 3) == 0 -> key
      key -> key + 1
    end
  end

  def take_step_variant(current_key, "U") do
    case current_key do
      key when key in [5, 2, 1, 4, 9] -> key
      3 -> 1
      13 -> 11
      key -> key - 4
    end
  end

  def take_step_variant(current_key, "D") do
    case current_key do
      key when key in [5, 10, 13, 12, 9] -> key
      1 -> 3
      11 -> 13
      key -> key + 4
    end
  end

  def take_step_variant(current_key, "R") do
    case current_key do
      key when key in [1, 4, 9, 12, 13] -> key
      key -> key + 1
    end
  end

  def take_step_variant(current_key, "L") do
    case current_key do
      key when key in [1, 2, 5, 10, 13] -> key
      key -> key - 1
    end
  end
end
