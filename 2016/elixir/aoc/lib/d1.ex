defmodule Move do
  @enforce_keys [:direction, :steps]
  defstruct [:direction, :steps]

  def parse(<<direction :: bytes - size(1)>> <> steps) do
    {steps, _rest} = Integer.parse(steps)
    %Move{direction: direction, steps: steps}
  end

  def follow({start_x, start_y}, start_heading, %Move{direction: direction, steps: steps}) do
    {heading_x, heading_y} = do_new_heading(start_heading, direction)
    new_position = {start_x + heading_x * steps, start_y + heading_y * steps}
    {new_position, {heading_x, heading_y}}
  end

  def new_heading(start_heading, %Move{direction: direction}) do
    do_new_heading(start_heading, direction)
  end

  defp do_new_heading(heading, direction) do
    case {heading, direction} do
      {{0, y}, "L"} -> {-y, 0}
      {{x, 0}, "L"} -> {0, x}
      {{0, y}, "R"} -> {y, 0}
      {{x, 0}, "R"} -> {0, -x}
    end
  end
end

defmodule D1 do
  def solve_part_1(input) do
    {final_x, final_y} = follow_steps(input)
    abs(final_x) + abs(final_y)
  end

  def follow_steps(s) do
    steps = read_steps(s)
    do_follow_steps(steps, {0, 0}, {0, 1})
  end

  defp do_follow_steps([], position, _heading) do
    position
  end

  defp do_follow_steps([next | tail], position, heading) do
    {new_position, new_heading} = Move.follow(position, heading, next)
    do_follow_steps(tail, new_position, new_heading)
  end

  defp read_steps(s) do
    do_next_step String.split(s, ", ", [trim: true])
  end

  defp do_next_step([head]) do
    [Move.parse(head)]
  end

  defp do_next_step([head | tail]) do
    [Move.parse(head) | do_next_step(tail)]
  end

  def solve_part_2(input) do
    {final_x, final_y} = visit_location(input)
    abs(final_x) + abs(final_y)
  end

  defp visit_location(s) do
    do_visit_location(read_steps(s), {0, 0}, {0, 1}, MapSet.new())
  end

  def do_visit_location([next_move | tail], position, heading, visited) do
    new_heading = Move.new_heading(heading, next_move)
    walk_result = walk_to_next_location(position, new_heading, next_move.steps, visited)
    case walk_result do
      {:revisited, position} -> position
      {:done, new_position, new_visited} -> do_visit_location(tail, new_position, new_heading, new_visited)
    end
  end

  def walk_to_next_location(position, heading, steps_remaining, visited) do
    if MapSet.member?(visited, position) do
      {:revisited, position}
    else
      if steps_remaining == 0 do
        {:done, position, visited}
      else
        {current_x, current_y} = position
        {heading_x, heading_y} = heading
        walk_to_next_location(
          {
            current_x + heading_x,
            current_y + heading_y
          },
          heading,
          steps_remaining - 1,
          visited
          |> MapSet.put(position)
        )
      end
    end
  end
end
