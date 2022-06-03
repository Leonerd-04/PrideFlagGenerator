from color_math import *
from PIL import Image


# Generates an image based on a function defining the color of each pixel
# generator: function used to generate the color of a pixel; takes coordinates as parameters and returns a color (tuple)
def generate(width: int, height: int, generator: Callable[[float, float], tuple[int, int, int]]) -> Image:
    image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            image.putpixel((x, y), generator(x, y))

    return image


# Generates a flag with stripes, like a lot of (okay pretty much all) pride flags consist of. Will be used for flags
# with colors that don't have a simple mathematical way of generating, like the trans pride flag.
# could also be used to generate flags of countries like germany and france ig
# the fit parameter scales the image; smaller = zoomed in, larger = zoomed out
def gen_striped_flag(width: int, height: int, colors: list[tuple[int, int, int]], interp=cuberp, fit=1.0) -> Image:
    def get_color(z: float) -> tuple:
        length = len(colors)

        x = z * (length - 1) % length
        i = int(x)

        # The modulos serve to let the flag loop around itself because why not
        color0 = colors[i % length]
        color1 = colors[(i + 1) % length]
        x %= 1

        return to_int(interp_color(x, color0, color1, interp))

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


def gen_progress_flag(width: int, height: int) -> Image:
    # Colors used
    # Rainbow is generated using the lineless hsv from the pride flag
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252
    brown = 97, 57, 21
    black = 0, 0, 0

    colors = [white, pink, blue, brown, black]

    def get_color(z: int) -> tuple[float, float, float]:
        x = z * 9 % 10

        if x < 4:
            i = int(x)
            return interp_color(x % 1, colors[i], colors[i + 1], cuberp)

        rainbow_x = 2 * z
        rainbow = hsv_lineless(360 * rainbow_x - 30, 0.8, 0.94, 256, lerp)  # The calculated rainbow color

        if x < 5:
            return interp_color(x % 1, black, rainbow, cuberp)
        if x < 9:
            return rainbow
        return interp_color(x % 1, rainbow, white, cuberp)

    return generate(width, height, lambda x, y: to_int(get_color((x + y / 2 - width / 2 - height / 4) / width + 0.5)))


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


# Bisexual pride flag gradient
def gen_bi_flag(width: int, height: int) -> Image:
    def get_hue(x, y):
        z = (x + y / 2 - height / 4) / width  # Maps the screen to values from 0 to 1, with a slant
        if z < 2 / 5:
            return lerp(2.5 * z, 342, 304)  # First third of the flag is interpolation between magenta and purple
        return lerp(1.67 * (z - 0.4), 304, 240)  # Interpolation between purple and blue

    return generate(width, height, lambda x, y: to_int(
        hsv_lineless(get_hue(x, y),
                     sine_bump(1.4 / width * (x + y / 2 - width / 2 - height / 4) + 0.5, 0.72, 0.90),
                     cuberp(1.8 / width * (x + y / 2 - width / 2 - height / 4) + 0.5, 0.72, 0.80),
                     256,
                     lerp
                     )))


# Pansexual pride flag gradient
def gen_pan_flag(width: int, height: int) -> Image:
    magenta = 255, 33, 142
    yellow = 252, 216, 0
    blue = 1, 148, 252

    colors = [magenta, yellow, blue]

    return gen_striped_flag(width, height, colors)


# Polysexual pride flag gradient
def gen_poly_flag(width: int, height: int) -> Image:
    magenta = 230, 18, 170
    green = 7, 213, 105
    blue = 28, 146, 246

    colors = [magenta, green, blue]

    def get_color(z: float) -> tuple:
        length = len(colors)

        x = z * (length - 1) % length
        i = int(x)

        color0 = colors[i % length]
        color1 = colors[(i + 1) % length]

        color = interp_color(x % 1, color0, color1, cuberp)

        # Smoothens the gap between the magenta and green of this flag
        # Otherwise there's an ugly dark grey line
        if x < 1:
            factor = sine_bump(x % 1, 0, 0.14)
            color = desaturate(1 - factor, scale(1 + factor, color))

        return to_int(color)

    return generate(width, height, lambda x, y: get_color((x + y / 2 - height / 4 - width / 2) / width + 0.5))


# Ace pride flag gradient
def gen_ace_flag(width: int, height: int) -> Image:
    # Black to white are generated using a linear gradient
    white = 255, 255, 255
    black = 0, 0, 0
    purple = 128, 0, 128

    def get_color(z: float) -> tuple[int, int, int]:
        x = z * 3 % 4

        if x < 2:
            return to_int(interp_color(x / 2, white, black, lerp))
        if x < 3:
            return to_int(interp_color(x - 2, black, purple, lerp))
        return to_int(interp_color(x - 3, purple, white, cuberp))

    return generate(width, height, lambda x, y: get_color((x + y / 2 - height / 4 - width / 2) / width + 0.5))


# Trans pride flag gradient
def gen_trans_flag(width: int, height: int) -> Image:
    white = 255, 255, 255
    pink = 247, 168, 184
    blue = 85, 205, 252

    colors = [blue, pink, white, pink, blue]

    return gen_striped_flag(width, height, colors, fit=0.83)


# Non-binary pride flag gradient
def gen_nb_flag(width: int, height: int) -> Image:
    yellow = 255, 244, 48
    white = 255, 255, 255
    purple = 156, 89, 209
    black = 0, 0, 0

    colors = [yellow, white, purple, black]

    return gen_striped_flag(width, height, colors, fit=0.9)


# Runs a smaller scale test of just one of the flags
if __name__ == "__main__":
    width, height = 640, 360
    gen_poly_flag(width, height).show()
