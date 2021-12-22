from PIL import Image
from numpy import abs, exp, sqrt
from color_math import to_int, interp_color, cuberp, hsv


# Generates an image based on a function defining the color of each pixel
# image: image object to be drawn on
# generator: function used to generate the color of a pixel; takes coordinates as parameters and returns a color (tuple)
def generate(width: int, height: int, generator) -> Image:
    image = Image.new("RGB", (width, height))
    px = image.load()

    for x in range(width):
        for y in range(height):
            px[x, y] = generator(x, y)

    return image


# Gay pride flag gradient
def rainbow(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: hsv(x / 7 + y / 14, 0.8, 0.95))


# Bi pride flag gradient, but using logistical curves
# No longer used as it's pretty slow and the cubic interpolated one looks better.
def bi_logistical(width: int, height: int) -> Image:
    center = (width + height) / 2

    # Uses logistical curves to create a smooth transition from magenta to purple to blue
    # Takes a while to calculate, unfortunately
    curve_magenta = lambda x: -40 / (1 + exp(-0.02 * (x - center + 200)))
    curve_blue = lambda x: -40 / (1 + exp(-0.04 * (x - center - 140)))
    curve_total = lambda x: curve_magenta(x) + curve_blue(x)

    return generate(width, height, lambda x, y: hsv(320 + curve_total(x + y / 2), 0.85, 0.88 - x / 7680))


# Also bi pride, but this time with cubic interpolation rather than logistical
# Should reduce compute times
def bi(width: int, height: int) -> Image:
    magenta = 214, 2, 112
    purple = 155, 79, 150
    blue = 0, 56, 168

    def get_color(x: int, center: float, width: int):
        delta = x - center
        if delta < -width / 2:
            return to_int(interp_color((-width / 2 - delta) / 300, purple, magenta, lambda x, x0, x1: cuberp(x, x0, x1)))
        if delta > width / 2:
            return to_int(interp_color((delta - width / 2) / 600, purple, blue, lambda x, x0, x1: cuberp(x, x0, x1)))
        return purple

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 60))


# Pan pride flag gradient
def pan(width: int, height: int) -> Image:
    magenta = 255, 33, 142
    yellow = 252, 216, 0
    blue = 1, 148, 252

    def get_color(x: int, center: float, width: int):
        delta = x - center
        if delta < -width / 2:
            return to_int(interp_color((-width / 2 - delta) / 400, yellow, magenta, lambda x, x0, x1: cuberp(x, x0, x1)))
        if delta > width / 2:
            return to_int(interp_color((delta - width / 2) / 400, yellow, blue, lambda x, x0, x1: cuberp(x, x0, x1)))
        return yellow

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 640))


# Ace pride flag gradient
def ace_flag(width: int, height: int) -> Image:
    # Colors used for the flag
    # Black to white are generated using a hsv gradient instead
    purple = 128, 0, 128

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        if(delta < width): return hsv(0, 0, cuberp(0.7 + delta / width / 3, 0, 1))
        return to_int(interp_color((delta - width) / 540, (255, 255, 255), purple, lambda x, x0, x1: cuberp(x, x0, x1)))

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center - 100, 480))


# Trans pride flag gradient
def trans(width: int, height: int) -> Image:
    # Colors used for the flag
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252

    # Specifies how to interpolate those colors
    def get_color(x: int, center: float, width: int) -> tuple:
        delta = abs(x - center)
        if delta < width / 2 + 30:
            return to_int(interp_color((width / 2 - delta) / 80, pink, white, lambda x, x0, x1: cuberp(x, x0, x1)))
        if delta < 3/2 * width + 30:
            return to_int(interp_color((3 * width / 2 - delta) / 120, blue, pink, lambda x, x0, x1: cuberp(x, x0, x1)))
        return blue

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 500))
