from generator import *


# Combines all the flags in the list of flags
def combine_flags(width: int, height: int, flags: list) -> Image:
    image = Image.new('RGB', (width, len(flags) * height))

    for index, flag in enumerate(flags):
        image.paste(flag, (0, height * index))

    return image


# The main script just generates an image with the flags stacked on top of one another
if __name__ == '__main__':
    print("Generating mlm flag...")
    gen_gay_flag(width, height).save("out/gay_pride.png", "PNG")

#
    # print("Generating wlw flag...")
    # gen_lesbian_flag(width, height).save("out/lesbian_pride.png", "PNG")
#
    # print("Generating bisexual flag...")
    # gen_bi_flag_hsv(width, height).save("out/bi_pride.png", "PNG")
#
    # print("Generation complete.")
