from PIL import Image
from generator import rainbow, bi, trans, pan, ace_flag

if __name__ == '__main__':
    width, height = 1920, 120

    gay_flag = rainbow(width, height)
    trans_flag = trans(width, height)
    bi_flag = bi(width, height)
    pan_flag = pan(width, height)
    ace_flag_image = ace_flag(width, height)

    flags = Image.new('RGB', (width, 5 * height))
    flags.paste(gay_flag, (0, 0))
    flags.paste(bi_flag, (0, height))
    flags.paste(pan_flag, (0, 2 * height))
    flags.paste(trans_flag, (0, 3 * height))
    flags.paste(ace_flag_image, (0, 4 * height))

    flags.show('Flags')

