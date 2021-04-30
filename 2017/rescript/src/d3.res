let input = 277678
type point = (int, int)

let correct_ring = (target) => {
    let ceil = Js.Math.ceil_int(Js.Math.sqrt(target))
    if mod(ceil, 2) == 0 {
        ceil + 1
    } else {
        ceil
    }
}

assert(correct_ring(1.0) == 1)
assert(correct_ring(4.0) == 3)
assert(correct_ring(10.0) == 5)

let ring_number = (ring_size) => (ring_size - 1) / 2

assert(ring_number(3) == 1)
assert(ring_number(7) == 3)

let ring_coordinates: int => point = (target) => {
    let size = correct_ring(Belt.Float.fromInt(target))
    let corner_offset = ring_number(size)
    let steps = target - (size - 2) * (size - 2)
    let full_sides = steps / (size - 1)
    let additional_steps = mod(steps, size - 1)
    switch full_sides {
        | 0 => (corner_offset, -corner_offset + additional_steps )
        | 1 => (corner_offset - additional_steps, corner_offset)
        | 2 => (-corner_offset, corner_offset - additional_steps)
        | 3 => (-corner_offset + additional_steps, -corner_offset)
        | 4 => (corner_offset, -corner_offset)
        | _ => (0, 0)
    }
}

assert(ring_coordinates(2) == (1, 0))
assert(ring_coordinates(14) == (1, 2))
assert(ring_coordinates(17) == (-2, 2))
assert(ring_coordinates(23) == (0, -2))
assert(ring_coordinates(25) == (2, -2))

let manhattan_distance = ((x, y): point) => abs(x) + abs(y)

let solve_1 = target => target -> ring_coordinates -> manhattan_distance

assert(solve_1(12) == 3)
assert(solve_1(23) == 2)
assert(solve_1(1024) == 31)
Js.log(solve_1(input))

open Belt.HashMap
module PointHash = Belt.Id.MakeHashable({
  type t = point
  let hash: point => int = ((x, y)) => x + y
  let eq = (a, b) => a == b
})

let cart_prod: (array<int>, array<int>) => array<(int, int)> = (arr1, arr2) => {
    arr1
    -> Js.Array2.map(item1 => arr2 -> Js.Array2.map(item2 => (item1, item2)))
    -> Js.Array2.reduce((acc, item) => Js.Array2.concat(acc, item), [])
}

let cells = cart_prod([-1, 0, 1], [-1, 0, 1])
let candidates = ((x, y)) => {
    cells
    -> Js.Array2.filter(((x, y)) => x != 0 || y != 0)
    -> Js.Array2.map(((dx, dy)) => (x + dx, y + dy))
}

let stored = make(~hintSize=100, ~id=module(PointHash))
set(stored, (0, 0), 1)
let get_stored = pair => get(stored, pair) -> Belt.Option.getWithDefault(0)
let rec first_larger_value = (target, current) => {
    let coords = ring_coordinates(current)
    let next_value: int = coords
    -> candidates
    -> Js.Array2.map(get_stored)
    -> Js.Array2.reduce((x, y) => x + y, 0)
    if next_value > target {
        next_value
    } else {
        set(stored, coords, next_value)
        first_larger_value(target, current + 1)
    }
}

Js.log(first_larger_value(input, 2))
