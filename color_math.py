

# Linear interpolation
def lerp(x: float, x0: float, x1: float) -> float:
    return x0 + x * (x1 - x0)


# Cubic interpolation
def cuberp(x: float, x0: float, x1: float) -> float:
    x = min(1.0, x)
    x = max(0.0, x)
    return x0 + (x1 - x0) * (3 * x ** 2 - 2 * x ** 3)


# Interpolation of two colors
# Formula parameter allows for the specification of the interpolation method as a lambda expression
def interp_color(x: float, color1: tuple, color2: tuple, formula) -> tuple:
    return formula(x, color1[0], color2[0]), formula(x, color1[1], color2[1]), formula(x, color1[2], color2[2])


# Casts a color to int values
def to_int(color: tuple) -> tuple:
    return int(color[0]), int(color[1]), int(color[2])


# Returns a tuple r, g, b calculated from the hsv values given
def hsv(h: float, s: float, v: float) -> tuple:
    h %= 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    e = int(m * 255)
    f = int((c + m) * 255)
    g = int((x + m) * 255)
    mode = h / 60

    if mode < 1: return f, g, e
    if mode < 2: return g, f, e
    if mode < 3: return e, f, g
    if mode < 4: return e, g, f
    if mode < 5: return g, e, f
    if mode < 6: return f, e, g

    return 0, 0, 0  # Will paint pixels with an erroneous mode as black
