from PIL import Image, ImageFilter
from numpy import abs, exp


def lerp(x: float, x0: float, x1: float) -> float:
    return x0 + x * (x1 - x0)


def lerp_color(x: float, color1: tuple, color2: tuple) -> tuple:
    return lerp(x, color1[0], color2[0]), lerp(x, color1[1], color2[1]), lerp(x, color1[2], color2[2])


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
    curve_magenta = lambda x: -40 / (1 + exp(-0.02 * (x - center + 200)))
    curve_blue = lambda x: -40 / (1 + exp(-0.04 * (x - center - 140)))
    curve_total = lambda x: curve_magenta(x) + curve_blue(x)

    return generate(image, lambda x, y: hsv(320 + curve_total(x + y / 2), 0.85, 0.88 - x / 7680))


def trans(image: Image):
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252

    def get_color(x: int, center: int, width: int):
        delta = abs(x - center)
        if delta < width / 2: return to_int(lerp_color(min(1, max(0, delta - width / 2)), white, pink))
        if delta < 3/2 * width: return to_int(lerp_color(min(1, max(0, delta - 3/2 * width)), pink, blue))
        return blue

    center = image.size[0] / 2 + image.size[1] / 2
    generate(image, lambda x, y: get_color(x + y / 2, center, 500))
    return image.filter(ImageFilter.GaussianBlur(12))

