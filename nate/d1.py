with open('inputs/in1.txt', 'r') as f:
    modules = [int(l.strip()) for l in f.readlines()]

def fuel(module):
    return max(0, int(module / 3) - 2)

def fuel_extended(module):
    total = 0
    temp = fuel(module)
    total += temp
    while temp > 0:
        total += (temp := fuel(temp))
    return total

assert fuel(100756) == 33583 # given
assert (t2 := fuel_extended(100756)) == 50346, str(t2) # also given

print(sum(map(fuel_extended, modules)))