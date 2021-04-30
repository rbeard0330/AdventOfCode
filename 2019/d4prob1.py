candidates = [str(n) for n in range(372304, 847061)]


def count_valid_pws(pw_list):
    return len([pw for pw in candidates if is_valid(pw)])


def is_valid(pw):
    no_match = True
    for i in range(5):
        if pw[i + 1] < pw[i]:
            return False
        if no_match and pw[i] == pw[i + 1]:
            no_match = False
    return not no_match


assert is_valid("111111")
assert not is_valid("223450")
assert not is_valid("123789")

print(count_valid_pws(candidates))
