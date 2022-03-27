from PIL import Image
from numpy import abs, exp
from color_math import to_int, interp_color, lerp, cuberp, hsv, rainbow_gen, sine_bump, hsv_lineless


# Generates an image based on a function defining the color of each pixel
# generator: function used to generate the color of a pixel; takes coordinates as parameters and returns a color (tuple)
def generate(width: int, height: int, generator) -> Image:
    image = Image.new("RGB", (width, height))
    px = image.load()

    for x in range(width):
        for y in range(height):
            px[x, y] = generator(x, y)

    return image


# Gay pride flag gradient
def gen_gay_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(rainbow_gen(360 * (0.8 * (x + y / 2) / width + 0.03), lerp)))


# Gay man (mlm) pride flag gradient
def gen_mlm_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(92/width * (x + y/2 - height/4) + 150,
            sine_bump(2 / width * (x + y/2 - width/2 - height/4) + 0.5, 0.83, 0.15),
            sine_bump(1 / width * (x + y/2 - width/2 - height/4) + 0.5, 0.78, 0.93)
            )))


# Lesbian (wlw) pride flag gradient
def gen_lesbian_flag(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(64/width * (x + y/2 - height/4) + 324,
            sine_bump(2 / width * (x + y/2 - width/2 - height/4) + 0.5, 0.83, 0.15),
            sine_bump(1 / width * (x + y/2 - width/2 - height/4) + 0.5, 0.64, 0.93)
            )))


# Gay pride flag gradient, but using traditional hsv
# Doesn't look quite as good imo
def gen_gay_flag_hsv(width: int, height: int) -> Image:
    return generate(width, height, lambda x, y: hsv(x / 7 + y / 14, 0.8, 0.95))


# Bi pride flag gradient, but using logistical curves
# No longer used as it's pretty slow and the cubic interpolated one looks better imo
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
def gen_bi_flag(width: int, height: int) -> Image:
    # Colors used for the flag
    magenta = 214, 2, 112
    purple = 155, 79, 150
    blue = 0, 56, 168

    def get_color(x: int, center: float, width: int) -> tuple:
        delta = x - center
        blur = 320
        if delta < -width / 2:
            return to_int(interp_color((-width / 2 - delta) / blur, purple, magenta,  cuberp))
        if delta > width / 2:
            return to_int(interp_color(0.6 * (delta - width / 2) / blur, purple, blue, cuberp))
        return purple

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 60))


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
        if delta < 3/2 * width + 30:
            return to_int(interp_color((3 * width / 2 - delta) / 120, blue, pink, cuberp))
        return blue

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 500))


# Enby pride flag gradient
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
            return to_int(interp_color((delta + 0.5 * width) / blur + 0.5, black, hsv(54 * delta / width + 24, 0.8, 0.95), cuberp))
        return hsv(54 * delta / width + 24, 0.8, 0.95)

    center = (width + height / 2) / 2
    return generate(width, height, lambda x, y: get_color(x + y / 2, center, 200))


# Runs a smaller scale test of just one of the flags
if __name__ == "__main__":
    gen_mlm_flag(1920, 1080).show()
