# SIMD - Single Instruction, Multiple Data
# Menggunakan NumPy (vectorized operation)

import numpy as np

def simd_example(data):
    array = np.array(data)
    result = array * 2  # satu instruksi untuk semua data
    return result


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    output = simd_example(data)
    print("Input  :", data)
    print("Output :", output.tolist())