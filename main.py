from typing import Callable

from generator import *
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
if __name__ == '__main__':
    width, height = 192, 108

    flags = [
        lambda: gen_pride_flag(width, height),
        lambda: gen_gay_flag(width, height),
        lambda: gen_lesbian_flag(width, height),
        lambda: gen_bi_flag(width, height),
    ]
    names = [
        "LGBTQ+",
        "gay (mlm)",
        "lesbian (wlw)",
        "bi"
    ]
    filenames = [
        "lgbtq_pride",
        "gay_pride",
        "lesbian_pride",
        "bi_pride"
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
        time.sleep(1)

    total_time /= 1000.0

    print(f"Generation took {total_time:.2f} s.")
    print("The generated images can be found in <project directory>/out/")
