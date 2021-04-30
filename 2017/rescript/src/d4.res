@bs.module external fs: 'a = "fs"

open Js
let input: string = fs["readFileSync"]("src/data/d4.txt", {"encoding": "utf-8"})
let splitLines = (s) => String.split("\n", s)

let splitAtSpaces = (s) => String.split(" ", s)
let validate_passphrase = phrase => {
    let words = splitAtSpaces(phrase)
    let word_counts = Dict.empty()
    words -> Array2.forEach(word => {
        let current_count = Dict.get(word_counts, word)
        let new_value = switch current_count {
            | None => 1
            | Some(x) => x + 1
        }
        Dict.set(word_counts, word, new_value)
    })
    Dict.values(word_counts) -> Array2.every(n => n == 1)
}

assert(validate_passphrase("aa bb cc dd ee"))
assert(!validate_passphrase("aa bb cc dd aa"))
assert(validate_passphrase("aa bb cc dd aaa"))

let words = input -> splitLines -> Array2.filter(s => String.trim(s) != "")
log(words -> Array2.filter(validate_passphrase) -> Array2.length) //387 too high

let validate_passphrase2 = phrase => {
    let words = splitAtSpaces(phrase)
    let word_counts = Dict.empty()
    words
    -> Array2.map(s => {
        s -> String.castToArrayLike -> Array2.from -> Array2.sortInPlace -> Array2.reduce(String.concat, "")
    })
    -> Array2.forEach(word => {
        let current_count = Dict.get(word_counts, word)
        let new_value = switch current_count {
            | None => 1
            | Some(x) => x + 1
        }
        Dict.set(word_counts, word, new_value)
    })
    Dict.values(word_counts) -> Array2.every(n => n == 1)
}

log(words -> Array2.filter(validate_passphrase2) -> Array2.length)