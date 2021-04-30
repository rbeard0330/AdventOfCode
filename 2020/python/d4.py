import re

REQUIRED_FIELDS = {
    'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'
}
HEIGHT_REGEX = re.compile(r'^([0-9]{2,3})(cm|in)$')
HAIR_COLOR_REGEX = re.compile(r'^#[0-9a-f]{6}$')
EYE_COLOR_REGEX = re.compile('^amb|blu|brn|gry|grn|hzl|oth$')
PID_REGEX = re.compile('^[0-9]{9}$')


def as_dict(line):
    result = {}
    for entry in line.split():
        key, value = entry.split(':')
        result[key] = value
    return result


def birth_year_valid(s):
    try:
        return 1920 <= int(s) <= 2002
    except:
        return False


assert birth_year_valid('2002')
assert not birth_year_valid('2003')


def issuance_year_valid(s):
    try:
        return 2010 <= int(s) <= 2020
    except:
        return False


def expiration_year_valid(s):
    try:
        return 2020 <= int(s) <= 2030
    except:
        return False


def height_valid(s):
    match = HEIGHT_REGEX.fullmatch(s)
    if match is None:
        return False
    height, unit = match.groups()
    return 150 <= int(height) <= 193 if unit == "cm" else 59 <= int(height) <= 76


assert height_valid('60in')
assert height_valid('190cm')
assert not height_valid('190in')
assert not height_valid('190')


def hair_color_valid(s):
    return HAIR_COLOR_REGEX.match(s) is not None


assert hair_color_valid('#123abc')
assert not hair_color_valid('#123abz')
assert not hair_color_valid('123abc')


def eye_color_valid(s):
    return EYE_COLOR_REGEX.match(s) is not None


assert eye_color_valid('brn')
assert not eye_color_valid('wat')


def pid_valid(s):
    return PID_REGEX.match(s) is not None


assert pid_valid('000000001')
assert not pid_valid('0123456789')


def first_answer(lines):
    return sum(REQUIRED_FIELDS <= set(as_dict(line).keys()) for line in lines)


def second_answer(lines):
    return sum('byr' in record and birth_year_valid(record['byr'])
               and 'iyr' in record and issuance_year_valid(record['iyr'])
               and 'eyr' in record and expiration_year_valid(record['eyr'])
               and 'hgt' in record and height_valid(record['hgt'])
               and 'hcl' in record and hair_color_valid(record['hcl'])
               and 'ecl' in record and eye_color_valid(record['ecl'])
               and 'pid' in record and pid_valid(record['pid'])
               for record in (as_dict(line) for line in lines))


PART1_TEST_DATA = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""


assert first_answer(PART1_TEST_DATA.split('\n\n')) == 2


INVALID_RECORDS = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""


VALID_RECORDS = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

assert second_answer(INVALID_RECORDS.split('\n\n')) == 0
assert second_answer(VALID_RECORDS.split('\n\n')) == len(INVALID_RECORDS.split('\n\n'))

DATA = open('data/d4.txt').read()

print(first_answer(open('data/d4.txt').read().split('\n\n')))
print(second_answer(DATA.split('\n\n')))


#189 too high