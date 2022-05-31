from generator import *
import os


# The main script just generates all the flags and saves them to a folder
if __name__ == '__main__':
    width, height = 1920, 1080

    print("Creating out directory...")

    try:
        os.mkdir("out")  # os.mkdir("out") tries to make the directory "out" wherever this script was run
        print("Directory created.")
    except FileExistsError:
        print("Directory already exists. Continuing...\n")
        pass

    print("Generating LGBTQ+ pride flag...")
    gen_pride_flag(width, height).save("out/lgbtq_pride.png", "PNG")

    print("Generating gay (mlm) pride flag...")
    gen_gay_flag(width, height).save("out/gay_pride.png", "PNG")

    print("Generating lesbian (wlw) pride flag...")
    gen_lesbian_flag(width, height).save("out/lesbian_pride.png", "PNG")

    print("Generating bi pride flag...")
    gen_bi_flag(width, height).save("out/bi_pride.png", "PNG")

    print("Generation complete. The images can be found in <project directory>/out/")
