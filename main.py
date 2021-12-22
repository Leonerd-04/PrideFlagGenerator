from PIL import Image
from generator import gen_gay_flag, gen_bi_flag, gen_trans_flag, gen_pan_flag, gen_ace_flag


# Combines all the flags in the list of flags
def combine_flags(width: int, height: int, flags: list) -> Image:
    image = Image.new('RGB', (width, len(flags) * height))

    for index, flag in enumerate(flags):
        image.paste(flag, (0, height * index))

    return image


# The main script just generates an image with the flags stacked on top of one another
if __name__ == '__main__':
    flags = []
    width, height = 1920, 120

    flags.append(gen_gay_flag(width, height))
    flags.append(gen_trans_flag(width, height))
    flags.append(gen_bi_flag(width, height))
    flags.append(gen_pan_flag(width, height))
    flags.append(gen_ace_flag(width, height))

    flags_image = combine_flags(width, height, flags)

    flags_image.show('Flags')
