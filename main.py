from generator import *
from typing import Callable
import os
import time


# Times the amount of time it takes for a certain function to run
# returns in milliseconds (ms)
def benchmark(function: Callable) -> float:
    start = time.time_ns()
    function()
    end = time.time_ns()

    return (end - start) / 1000000.0


# The main script just generates all the flags and saves them to a folder
def main():
    width, height = 1920, 1080

    flags = [
        lambda: gen_pride_flag(width, height),
        lambda: gen_progress_flag(width, height),
        lambda: gen_gay_flag(width, height),
        lambda: gen_lesbian_flag(width, height),
        lambda: gen_bi_flag(width, height),
        lambda: gen_pan_flag(width, height),
        lambda: gen_poly_flag(width, height),
        lambda: gen_ace_flag(width, height),
        lambda: gen_trans_flag(width, height),
        lambda: gen_nonbinary_flag(width, height),
        lambda: gen_genderfluid_flag(width, height)
    ]
    names = [
        "LGBTQ+",
        "LGBTQ+ progress",
        "gay (mlm)",
        "lesbian (wlw)",
        "bi",
        "pan",
        "poly",
        "ace",
        "trans",
        "nonbinary",
        "genderfluid"
    ]
    filenames = [
        "lgbtq_pride",
        "lgbtq_progress",
        "gay_pride",
        "lesbian_pride",
        "bi_pride",
        "pan_pride",
        "poly_pride",
        "ace_pride",
        "trans_pride",
        "nonbinary_pride",
        "genderfluid-pride"
    ]

    print("Creating out directory...")

    try:
        os.mkdir("out")  # os.mkdir("out") tries to make the directory "out" wherever this script was run
        print("Directory created.")
    except FileExistsError:
        print("Directory already exists.")
        time.sleep(0.3)
        print("Continuing...\n")
        time.sleep(0.5)
        pass

    total_time = 0

    for name, filename, generator in zip(names, filenames, flags):
        print(f"Generating {name} pride flag...")
        time_elapsed = benchmark(lambda: generator().save(f"out/{filename}.png", "PNG"))
        total_time += time_elapsed

        if time_elapsed > 1000:
            time_elapsed /= 1000.0
            print(f"Took {time_elapsed:.2f} s.\n")
        else:
            print(f"Took {time_elapsed:.2f} ms.\n")

    total_time /= 1000.0

    print(f"Generation took {total_time:.2f} s.")
    print("The generated images can be found in <project directory>/out/")


if __name__ == '__main__':
    main()
