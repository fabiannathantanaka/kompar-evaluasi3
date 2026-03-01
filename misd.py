# MISD - Multiple Instruction, Single Data
# Satu data diproses dengan instruksi berbeda

def misd_example(data):
    result = {
        "double": data * 2,
        "square": data ** 2,
        "cube": data ** 3,
        "half": data / 2
    }
    return result


if __name__ == "__main__":
    data = 5
    output = misd_example(data)
    print("Input  :", data)
    print("Output :", output)