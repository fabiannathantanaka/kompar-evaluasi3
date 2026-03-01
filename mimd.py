# MIMD - Multiple Instruction, Multiple Data
# Menggunakan multiprocessing

from multiprocessing import Process

def task_double(n):
    print(f"Double of {n} = {n * 2}")

def task_square(n):
    print(f"Square of {n} = {n ** 2}")

if __name__ == "__main__":
    p1 = Process(target=task_double, args=(5,))
    p2 = Process(target=task_square, args=(10,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Finished MIMD processing.")