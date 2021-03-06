from typing import Callable


# Changes a color's brightness
def scale(scalar: float, color: tuple[float, float, float]) -> tuple[float, float, float]:
    return scalar * color[0], scalar * color[1], scalar * color[2]


# Desaturates a color
def desaturate(sat: float, color: tuple[float, float, float]) -> tuple[float, float, float]:
    a = 255 * (1 - sat)
    return a + sat * color[0], a + sat * color[1], a + sat * color[2]


# Linear interpolation
# Does not necessarily restrict to values between 0 and 1
def lerp(x: float, x0: float, x1: float, restrict=False) -> float:
    if restrict:
        if x <= 0.0:
            return x0
        if x >= 1.0:
            return x1
    return x0 + x * (x1 - x0)


# Cubic interpolation using f(x) = 3x² - 2x³
# Has a gradual lead in/lead out for smoother transitions
# Always restricts to x between 0 and 1
def cuberp(x: float, x0: float, x1: float) -> float:
    if x <= 0.0:
        return x0
    if x >= 1.0:
        return x1
    return x0 + (x1 - x0) * (3 - 2 * x) * x ** 2


# Gives a smooth, cubic bump using two cubic interpolations
# Always restricts to x between 0 and 1
def cubic_bump_uneven(x: float, x0: float, x1: float, x2: float) -> float:
    if x < 0.5:
        return cuberp(2 * x, x0, x1)
    return cuberp(2 * x - 1, x1, x2)


# Same as above but with the two ends of the bump being at the same level.
def cubic_bump(x: float, x0: float, x1: float) -> float:
    return cubic_bump_uneven(x, x0, x1, x0)


# Interpolation of two colors
# interp parameter allows for the specification of the interpolation method as a lambda expression
def interp_color(x: float, color1: tuple[float, float, float], color2: tuple[float, float, float], interp) \
        -> tuple[float, float, float]:
    return interp(x, color1[0], color2[0]), interp(x, color1[1], color2[1]), interp(x, color1[2], color2[2])


# Casts a color to int values
def to_int(color: tuple[float, float, float]) -> tuple[int, int, int]:
    return int(color[0]), int(color[1]), int(color[2])


# Returns a tuple r, g, b calculated from the hsv values given
# i got the formulas from wikipedia i think
# has ugly lines at 60, 180, & 300 degrees so prolly won't be used anymore
def hsv(h: float, s: float, v: float) -> tuple[float, float, float]:
    if s == 0:
        v *= 255
        return to_int((v, v, v))

    h %= 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    e = int(m * 255)
    f = int((c + m) * 255)
    g = int((x + m) * 255)
    mode = h / 60

    if mode < 1:
        return f, g, e
    if mode < 2:
        return g, f, e
    if mode < 3:
        return e, f, g
    if mode < 4:
        return e, g, f
    if mode < 5:
        return g, e, f
    if mode < 6:
        return f, e, g

    return 0, 0, 0  # Will paint pixels with an erroneous mode as black


# Generates a rainbow gradient through interpolation, as specified by the interp parameter
# limit signifies a restriction on the correction factor used to brighten the darker colors
def rainbow_gen(hue: float, limit: float, interp: Callable[[float, float, float], float]) -> tuple[float, float, float]:
    hue %= 360  # Hue is always between 0 and 360
    section = int(hue / 120)

    # c represents a correction factor to brighten the darker colours
    if section == 0:
        r = interp(hue / 120, 255, 0)
        g = interp(hue / 120, 0, 255)
        c = r * g / limit
        return r + c, g + c, 0
    if section == 1:
        g = interp(hue / 120 - 1, 255, 0)
        b = interp(hue / 120 - 1, 0, 255)
        c = g * b / limit
        return 0, g + c, b + c
    else:
        b = interp(hue / 120 - 2, 255, 0)
        r = cuberp(hue / 120 - 2, 0, 255)
        c = b * r / limit
        return r + c, 0, b + c


# Uses the rainbow generator to improve upon traditional hsv in some ways for image generation
# This creates smoother hue transitions without those annoying lines at 60°, 180°, and 300°
def hsv_lineless(hue: float, sat: float, val: float, limit=256, interp=lerp) -> tuple[float, float, float]:
    return scale(val, desaturate(sat, rainbow_gen(hue, limit, interp)))
