import os.path
import collections
import itertools

file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "inputs", "d2.txt")

input_list = []
with open(file_name, "r") as f:
    for line in f.readlines():
        input_list.append(line.strip())


def parse_id(word):
    "Determine whether id has 2x or 3x char. Returns a tuple of bools."
    count = collections.Counter()
    for char in word:
        count[char] += 1
    return 2 in count.values(), 3 in count.values()


twos, threes = 0, 0
for word in input_list:
    two, three = parse_id(word)
    twos += int(two)
    threes += int(three)


print("Part 1:")
print(twos * threes)


def count_diffs(word1, word2):
    assert len(word1) == len(word2)
    count = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            count += 1
            diff = i
            if count > 1:
                return 2, diff    # Greater numbers don't matter
    if count == 1:
        return 1, diff
    else:
        print(word2)
        print(word1)
        raise Exception


for word1, word2 in itertools.combinations(input_list, 2):
    count, index = count_diffs(word1, word2)
    if count == 1:
        answer = word1[:index] + word1[index + 1:]
        assert answer == word2[:index] + word2[index + 1:]
        break

print(f"Part 2:\n{answer}")
