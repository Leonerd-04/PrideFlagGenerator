from generator import *


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

    flags.append(gen_pride_flag(width, height))
    flags.append(gen_gay_flag(width, height))
    flags.append(gen_lesbian_flag(width, height))
    flags.append(gen_trans_flag(width, height))
    flags.append(gen_bi_flag(width, height))
    flags.append(gen_pan_flag(width, height))
    flags.append(gen_ace_flag(width, height))
    flags.append(gen_enby_flag(width, height))
    flags.append(gen_progress_flag(width, height))

    flags_image = combine_flags(width, height, flags)

    flags_image.show('Flags')
