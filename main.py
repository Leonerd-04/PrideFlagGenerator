from PIL import Image
from generator import rainbow, bi, trans

if __name__ == '__main__':
    image = Image.new("RGB", (1920, 150))
    trans(image).show()
