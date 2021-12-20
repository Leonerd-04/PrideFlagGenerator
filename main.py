from PIL import Image
from generator import rainbow, bi, trans, pan

if __name__ == '__main__':
    width, height = 1920, 200

    gay_flag = rainbow(width, height)
    trans_flag = trans(width, height)
    bi_flag = bi(width, height)
    pan_flag = pan(width, height)

    flags = Image.new('RGB', (width, 4 * height))
    flags.paste(gay_flag, (0, 0))
    flags.paste(bi_flag, (0, height))
    flags.paste(pan_flag, (0, 2 * height))
    flags.paste(trans_flag, (0, 3 * height))

    flags.show('Flags')

