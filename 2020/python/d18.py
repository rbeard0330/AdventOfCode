def parse_expr(tokens, index):
    lhs, next_index = parse_operand(tokens, index)
    while next_index < len(tokens):
        operator = tokens[next_index]
        if operator == ')':
            return lhs
        rhs, next_index = parse_operand(tokens, next_index + 1)
        if operator == '+':
            lhs += rhs
        else:
            assert operator == '*', operator
            lhs *= rhs
    return lhs


def parse_operand(tokens, index):
    if tokens[index] == '(':
        subexpression = extract_parenthesized_expr(tokens, index)
        return parse_expr(subexpression, 0), index + len(subexpression) + 2
    return int(tokens[index]), index + 1


def parse_expr_with_precedence(tokens):
    while '(' in tokens:
        index = tokens.index('(')
        subexpression = extract_parenthesized_expr(tokens, index)
        tokens = tokens[:index] + [parse_expr_with_precedence(subexpression)] + tokens[index + len(subexpression) + 2:]

    while '+' in tokens:
        index = tokens.index('+')
        tokens = tokens[:index - 1] + [tokens[index - 1] + tokens[index + 1]] + tokens[index + 2:]

    while '*' in tokens:
        index = tokens.index('*')
        tokens = tokens[:index - 1] + [tokens[index - 1] * tokens[index + 1]] + tokens[index + 2:]

    assert len(tokens) == 1, tokens
    return tokens[0]


def extract_parenthesized_expr(tokens, start_index):
    assert tokens[start_index] == '('
    paren_depth = 1
    current_index = start_index
    while paren_depth:
        current_index += 1
        if tokens[current_index] == ')':
            paren_depth -= 1
        elif tokens[current_index] == '(':
            paren_depth += 1

    return tokens[start_index + 1:current_index]


def tokenize(text):
    return [int(token) if token.isnumeric() else token
            for token in text.replace(')', ' ) ').replace('(', ' ( ').split()]


def first_answer(text):
    return sum(parse_expr(tokenize(line), 0) for line in text.splitlines())


def second_answer(text):
    return sum(parse_expr_with_precedence(tokenize(line)) for line in text.splitlines())


assert first_answer("1 + 2 * 3 + 4 * 5 + 6") == 71
assert second_answer('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert first_answer('2 * 3 + (4 * 5)') == 26
assert first_answer('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert first_answer('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert first_answer('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

assert second_answer("1 + 2 * 3 + 4 * 5 + 6") == 231
assert second_answer('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert second_answer('2 * 3 + (4 * 5)') == 46
assert second_answer('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert second_answer('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert second_answer('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

real_data = open('data/d18.txt').read()

print(first_answer(real_data))
print(second_answer(real_data))
