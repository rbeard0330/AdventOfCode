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

assert (fuel_required := fuel(100756)) == 33583, str(fuel_required) # given
assert (fuel_required := fuel_extended(100756)) == 50346, str(fuel_required) # also given

print(sum(map(fuel, modules))) #This gives part 1's answer.
print(sum(map(fuel_extended, modules))) #This gives part 2's answer.
