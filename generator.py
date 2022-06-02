from concurrent.futures import ThreadPoolExecutor

from color_math import *
from PIL import Image


# Generates an image based on a function defining the color of each pixel
# generator: function used to generate the color of a pixel; takes coordinates as parameters and returns a color (tuple)
def generate(width: int, height: int, generator: Callable[[float, float], tuple[int, int, int]]) -> Image:
    image = Image.new("RGB", (width, height))
    px = image.load()

    for x in range(width):
        for y in range(height):
            px[x, y] = generator(x, y)

    return image


# Generates a flag with stripes, like a lot of (okay pretty much all) pride flags consist of. Will be used for flags
# with colors that don't have a simple mathematical way of generating, like the trans pride flag.
# could also be used to generate flags of countries like germany and france ig
# the fit parameter scales the image; smaller = zoomed in, larger = zoomed out
def gen_striped_flag(width: int, height: int, fit: int, colors: list[tuple[int, int, int]]) -> Image:
    def get_color(z: int) -> tuple:
        z %= 1
        x = z * len(colors)
        i = int(x)

        color0 = colors[i]
        color1 = colors[(i + 1) % len(colors)]  # The modulo serves to let the flag loop around itself because why not
        x %= 1

        return to_int(interp_color(x, color0, color1, cuberp))

    return generate(width, height, lambda x, y: get_color(fit * (x + y / 2 - height / 4 - width / 2) / width + 0.5))


# LGBT pride flag gradient (rainbow).
# Ngl getting the colors to not look terrible and not make annoying lines at specific hues was hell.
def gen_pride_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(
            360 * (0.95 * (x + y / 2 - height / 4) / width - 0.06),
            0.8,
            0.94,
            256,
            lerp
        )))


# Gay (mlm) pride flag gradient
def gen_gay_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(108 / width * (x + y / 2 - height / 4) + 156,
                     cuberp(4 / width * (x + y / 2 - width / 2 - height / 4) + 1, 0.64, 0.15)
                     + cuberp(4 / width * (x + y / 2 - width / 2 - height / 4), 0.00, 0.70),
                     cuberp(1 / width * (x + y / 2 - width / 2 - height / 4) + 1, 0.67, 0.90)
                     + cuberp(1 / width * (x + y / 2 - width / 2 - height / 4), 0.00, -0.32),
                     256,
                     lerp
                     )))


# Lesbian (wlw) pride flag gradient
def gen_lesbian_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(57 / width * (x + y / 2 - height / 4) + 324,
                     sine_bump(2 / width * (x + y / 2 - width / 2 - height / 4) + 0.5, 0.73, 0.15),
                     cuberp(1.6 / width * (x + y / 2 - width / 2 - height / 4) + 1, 0.73, 0.90) +
                     cuberp(1.6 / width * (x + y / 2 - width / 2 - height / 4), 0.00, -0.23),
                     256,
                     lerp
                     )))


# Bi pride once again, with improved hsv generation rather than cubic
# Increases compute times, but looks better imo
def gen_bi_flag(width: int, height: int) -> Image:
    def get_hue(x, y):
        z = (x + y / 2 - height / 4) / width  # Maps the screen to values from 0 to 1, with a slant
        if z < 2 / 5:
            return lerp(2.5 * z, 342, 304)  # First third of the flag is interpolation between magenta and purple
        return lerp(1.67 * (z - 0.4), 304, 240)  # Interpolation between purple and blue

    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(get_hue(x, y),
                     sine_bump(1.4 / width * (x + y / 2 - width / 2 - height / 4) + 0.5, 0.72, 0.90),
                     cuberp(1.8 / width * (x + y / 2 - width / 2 - height / 4) + 0.5, 0.67, 0.80),
                     256,
                     lerp
                     )))


# Pan pride flag gradient
def gen_pan_flag(width: int, height: int) -> Image:
    # Colors used for the flag
    magenta = 255, 33, 142
    yellow = 252, 216, 0
    blue = 1, 148, 252

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        if delta < -width / 2:
            return to_int(interp_color((-width / 2 - delta) / 400, yellow, magenta, cuberp))
        if delta > width / 2:
            return to_int(interp_color((delta - width / 2) / 400, yellow, blue, cuberp))
        return yellow

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 640))


# Ace pride flag gradient
def gen_ace_flag(width: int, height: int) -> Image:
    # Black to white are generated using a hsv gradient instead of color literals
    purple = 128, 0, 128
    white = 255, 255, 255

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        if delta < width / 2:
            return hsv(0, 0, cuberp(0.8 + delta / width / 3, 0, 1))
        return to_int(interp_color((delta - width) / 384 + 0.3, white, purple, cuberp))

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 500))


# Trans pride flag gradient
def gen_trans_flag(width: int, height: int) -> Image:
    # Colors used for the flag
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252

    # Specifies how to interpolate those colors
    def get_color(x: int, center: float, width: int) -> tuple:
        delta = abs(x - center)
        if delta < width / 2 + 30:
            return to_int(interp_color((width / 2 - delta) / 80, pink, white, cuberp))
        if delta < 3 / 2 * width + 30:
            return to_int(interp_color((3 * width / 2 - delta) / 120, blue, pink, cuberp))
        return blue

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 500))


# Non-binary pride flag gradient
def gen_enby_flag(width: int, height: int) -> Image:
    # Colors to be used
    yellow = 255, 244, 48
    white = 255, 255, 255
    purple = 156, 89, 209
    black = 0, 0, 0

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        blur = 200
        if delta < - width / 2:
            return to_int(interp_color((delta + width) / blur + 0.5, yellow, white, cuberp))
        if delta < width / 2:
            return to_int(interp_color(delta / blur + 0.5, white, purple, cuberp))
        return to_int(interp_color(0.4 * (delta - width) / blur + 0.5, purple, black, cuberp))

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 600))


def gen_progress_flag(width: int, height: int) -> Image:
    # Colors used
    # Rainbow is generated using hsv
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252
    brown = 97, 57, 21
    black = 0, 0, 0

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        blur = 144
        if delta < -4 * width:
            return to_int(interp_color((delta + 4.5 * width) / blur + 0.5, white, pink, cuberp))
        if delta < -3 * width:
            return to_int(interp_color((delta + 3.5 * width) / blur + 0.5, pink, blue, cuberp))
        if delta < -2 * width:
            return to_int(interp_color((delta + 2.5 * width) / blur + 0.5, blue, brown, cuberp))
        if delta < -1 * width:
            return to_int(interp_color((delta + 1.5 * width) / blur + 0.5, brown, black, cuberp))
        if delta < 0:
            return to_int(
                interp_color((delta + 0.5 * width) / blur + 0.5, black, hsv(54 * delta / width + 24, 0.8, 0.95),
                             cuberp))
        return hsv(54 * delta / width + 24, 0.8, 0.95)

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 200))


# Runs a smaller scale test of just one of the flags
if __name__ == "__main__":
    width, height = 960, 540
    gen_bi_flag(width, height).show()
