@bs.module external fs: 'a = "fs"

open Js
let splitLines = (s) => String.split("\n", s)
let parseInt = (s) => Float.fromString(s) -> Belt.Float.toInt
let input: array<int> = fs["readFileSync"]("src/data/d5.txt", {"encoding": "utf-8"})
    -> splitLines
    -> Array2.filter(s => String2.trim(s) != "")
    -> Array2.map(parseInt)

let testInput = [0, 3, 0, 1, -3]

let rec step_out_of_maze = (steps, index, instructions) => {
    if index >= Array2.length(instructions) {
        steps
    } else {
        let jump = Array2.unsafe_get(instructions, index)
        Array2.unsafe_set(instructions, index, jump + 1)
        step_out_of_maze(steps + 1, index + jump, instructions)
    }
}

assert(step_out_of_maze(0 ,0, Array.copy(testInput)) == 5)
log(step_out_of_maze(0, 0, Array.copy(input))) // too high 378982

let rec step_out_of_maze_2 = (steps, index, instructions) => {
    if index >= Array2.length(instructions) {
        steps
    } else {
        let jump = Array2.unsafe_get(instructions, index)
        let change = if jump >= 3 {
            -1
        } else {
            1
        }
        Array2.unsafe_set(instructions, index, jump + change)
        step_out_of_maze_2(steps + 1, index + jump, instructions)
    }
}

assert(step_out_of_maze_2(0 ,0, testInput) == 10)
log(step_out_of_maze_2(0, 0, input))