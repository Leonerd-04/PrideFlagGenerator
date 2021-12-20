from PIL import Image
from numpy import abs, exp
from color_math import to_int, interp_color, cuberp, hsv


# Generates an image based on a function defining the color of each pixel
# image: image object to be drawn on
# generator: function used to generate the color of a pixel; takes coordinates as parameters and returns a color (tuple)
def generate(image: Image, generator):
    px = image.load()

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            px[x, y] = generator(x, y)

    return image


# Gay pride flag gradient
def rainbow(image: Image):
    return generate(image, lambda x, y: hsv(x / 7 + y / 14, 0.8, 0.95))


# Bi pride flag gradient
def bi(image: Image):
    center = image.size[0] / 2 + image.size[1] / 2

    # Uses logistical curves to create a smooth transition from magenta to purple to blue
    # Takes a while to calculate, unfortunately
    curve_magenta = lambda x: -40 / (1 + exp(-0.02 * (x - center + 200)))
    curve_blue = lambda x: -40 / (1 + exp(-0.04 * (x - center - 140)))
    curve_total = lambda x: curve_magenta(x) + curve_blue(x)

    return generate(image, lambda x, y: hsv(320 + curve_total(x + y / 2), 0.85, 0.88 - x / 7680))


# Trans pride flag gradient
def trans(image: Image):
    # Colors used for the flag
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252

    # Specifies how to interpolate those colors
    def get_color(x: int, center: int, width: int):
        delta = abs(x - center)
        if delta < width / 2:
            return to_int(interp_color((width / 2 - delta) / 60, pink, white, lambda x, x0, x1: cuberp(x, x0, x1)))
        if delta < 3/2 * width:
            return to_int(interp_color((3 * width / 2 - delta) / 60, blue, pink, lambda x, x0, x1: cuberp(x, x0, x1)))
        return blue

    center = image.size[0] / 2 + image.size[1] / 2
    return generate(image, lambda x, y: get_color(x + y / 2, center, 500))
