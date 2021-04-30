p = 20201227
base = 7


def first_answer(pair):
    door, key = pair

    product = base
    exponent = 1
    while product != door and product != key:
        product *= base
        product %= p
        exponent += 1
    other = door if product == key else key
    result = other
    print(result, exponent)
    for _ in range(exponent - 1):
        result *= other
        result %= p

    return result


TEST_DATA = (17807724, 5764801)

assert first_answer(TEST_DATA) == 14897079

real_data = (2959251, 4542595)

print(first_answer(real_data))
