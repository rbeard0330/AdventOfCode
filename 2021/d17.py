X_MIN = 70
X_MAX = 125
Y_MIN = -159
Y_MAX = -121


def hits_y_range(dy_init):
    dy_current = dy_init
    y_current = 0
    while True:
        y_current += dy_current
        dy_current -= 1
        if y_current < Y_MIN:
            return False
        if y_current <= Y_MAX:
            return True


def hits_x_range(dx_init):
    dx_current = dx_init
    x_current = 0
    while True:
        x_current += dx_current
        if dx_current > 0:
            dx_current -= 1
        if x_current > X_MAX:
            return False
        if x_current >= X_MIN:
            return True
        if dx_current == 0:
            return False


def test_trajectory(dx, dy):
    init_dx = dx
    init_dy = dy
    x = y = y_max = 0
    hit_zone = False
    while True:
        y += dy
        x += dx
        # print(x, y)
        dy -= 1
        if dx > 0:
            dx -= 1
        if y > y_max:
            y_max = y
        if X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX:
            hit_zone = True
        if (x < X_MIN and dx == 0) or x > X_MAX or y < Y_MIN:
            return hit_zone and y_max

def part_1():
    y_candidates = list(i for i in range(1000) if hits_y_range(i))[::-1]
    x_candidates = list(i for i in range(1000) if hits_x_range(i))
    best_y = 0
    for dy in y_candidates[:10]:
        for dx in x_candidates:
            if (result := test_trajectory(dx, dy)):
                if result > best_y:
                    best_y = result
                break
    return best_y

print(part_1())


def part_2():
    y_candidates = list(i for i in range(-500, 1000) if hits_y_range(i))[::-1]
    x_candidates = list(i for i in range(1000) if hits_x_range(i))
    return sum(test_trajectory(dx, dy) is not False for dx in x_candidates for dy in y_candidates)

print(part_2())