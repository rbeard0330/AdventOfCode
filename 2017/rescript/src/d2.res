@bs.module external fs: 'a = "fs"
open Js
open Belt.Array

let testInput = `5\t1\t9\t5
7\t5\t3
2\t4\t6\t8`
let input: string = fs["readFileSync"]("src/data/d2.txt", {"encoding": "utf-8"})

let splitLines = (s) => String.split("\n", s)
let splitTabs = (s) => String.split("\t", s)
let parseInt = (s) => Float.fromString(s) -> Belt.Float.toInt
let parseLine = (line) => line -> splitTabs -> map(s => parseInt(s))

let firstOrZero = arr => switch Belt.Array.get(arr, 0) {
    | None => 0
    | Some(n) => n
}
let arrayMax = (arr) => reduce(arr, firstOrZero(arr), max)
let arrayMin = (arr) => reduce(arr, firstOrZero(arr), min)
let checkSum = (line) => {
    let maxValue = line -> arrayMax
    let minValue = line -> arrayMin
    maxValue - minValue
}



let firstAnswer = (input: string): int => {
    input
        -> splitLines
        -> map(String.trim)
        -> map((s) => splitTabs(s) -> map(parseInt))
        -> map(checkSum)
        -> reduce(0, (a, b) => a + b)
}

assert(firstAnswer(testInput) == 18)
let answer1 = firstAnswer(input)
Console.log(answer1) // 39319 too high


let first = (arr, testFn) => reduce(arr, None, (acc, next) => switch acc {
    |Some(value) => Some(value)
    |None => testFn(next) ? Some(next) : None
})
let divides = (x, y) => x != 0 && mod(y, x) == 0
let numberDividedByX = (x, restLine) => first(restLine, y => divides(x, y) && x != y )
assert(numberDividedByX(2, []) == None)
assert(numberDividedByX(2, [1, 3, 5]) == None)
assert(numberDividedByX(2, [3, 4, 5]) == Some(4))

let numbersDivided = arr => arr
    -> map(num => numberDividedByX(num, arr))

assert(numbersDivided([3, 4, 5]) == [None, None, None])
assert(numbersDivided([2, 4, 5]) == [Some(4), None, None])

let dividingPair = arr => arr
    -> Belt.Array.zip(numbersDivided(arr))
    -> Array2.filter(((_, divided)) => Option.isSome(divided))
    -> map(((a, b)) => (a, Option.getExn(b)))

assert(dividingPair([2, 4, 5]) == [(2, 4)])

let divResult = (a, b) => a > b ? a / b: b / a
let checksum2 = arr => arr
    -> dividingPair
    -> map(((a, b)) => divResult(a, b))
    -> firstOrZero

assert(checksum2([2, 4, 5]) == 2)
assert(checksum2([2, 8, 5]) == 4)

let testInput = `5\t9\t2\t8\n9\t4\t7\t3\n3\t8\t6\t5`

let secondAnswer = (input: string) => {
    input
        -> splitLines
        -> map(String.trim)
        -> map((s) => splitTabs(s) -> map(parseInt))
        -> map(checksum2)
        -> reduce(0, (a, b) => a + b)
}
assert(secondAnswer(testInput) == 9)
Console.log(secondAnswer(input))