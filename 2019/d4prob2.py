candidates = [str(n) for n in range(372304, 847061)]


def count_valid_pws(pw_list):
    return len([pw for pw in candidates if is_valid(pw)])


def is_valid(pw):
    bins = dict()
    for i in range(5):
        if pw[i + 1] < pw[i]:
            return False
        bins[pw[i]] = bins.get(pw[i], 0) + 1
    bins[pw[5]] = bins.get(pw[5], 0) + 1  # <----beautiful
    return 2 in bins.values()


assert is_valid("112233")
assert not is_valid("123444")
assert is_valid("111122")

print(count_valid_pws(candidates))
