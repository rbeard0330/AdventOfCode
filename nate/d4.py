minpw = 353096
maxpw = 843212

def isSixDigit(n):
    return n >= 100000 and n <= 999999

def hasAdjacency(n):
    n = str(n)
    curr = n[0]
    for char in n[1:]:
        if char == curr:
            return True
        curr = char
    return False

def hasSpecialAdjacency(n):
    padded = '#' + str(n) + '#'
    for ix in range(len(str(n))-1):
        temp = padded[ix:ix+4]
        if (temp[1] == temp[2] and temp[1] != temp[0] and temp[1] != temp[3]):
            return True
    return False

def isMonotonic(n):
    n = str(n)
    curr = n[0]
    for char in n[1:]:
        if char < curr: #comparison works on chars also
            return False
        curr = char
    return True

def passesTestsA(n):
    return isSixDigit(n) and hasAdjacency(n) and isMonotonic(n)

def passesTestsB(n):
    return isSixDigit(n) and hasSpecialAdjacency(n) and isMonotonic(n)

assert not hasSpecialAdjacency(123444)
assert hasSpecialAdjacency(111122)
assert passesTestsB(112233)
assert not passesTestsB(123444)
assert passesTestsB(111122)

print(sum(map(passesTestsA, range(minpw, maxpw+1))))
print(sum(map(passesTestsB, range(minpw, maxpw+1))))