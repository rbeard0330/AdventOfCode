defmodule Utils do
  use ExUnit.Case
    def check_examples([], _f) do
    end

    def check_examples([example | tail], f) do
      {input, expected} = example
      assert f.(input) == expected
      check_examples(tail, f)
    end
  end

defmodule D1Test do
  use ExUnit.Case

  test "solves examples for first part" do
    examples = [{"R2, L3", 5}, {"R2, R2, R2", 2}, {"R2, R2, R2", 2}]
    Utils.check_examples(examples, &D1.solve_part_1/1)
  end

  test "solves examples for second part" do
    examples = [{"R8, R4, R4, R8", 4}]
    Utils.check_examples(examples, &D1.solve_part_2/1)
  end
end


defmodule D2Test do
  use ExUnit.Case

  test "solves examples for first part" do
    examples = [{~S"ULL
RRDDD
LURDL
UUUUD", "1985"}]
    Utils.check_examples(examples, &D2.solve_part_1/1)
  end

  test "solves examples for second part" do
    examples = [{~S"ULL
RRDDD
LURDL
UUUUD", "5DB3"}]
    Utils.check_examples(examples, &D2.solve_part_2/1)

  end
end

