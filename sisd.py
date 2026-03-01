# SISD - Single Instruction, Single Data
# Proses sequential biasa

def sisd_example(data):
    result = []
    for x in data:
        result.append(x * 2)  # satu instruksi, satu data tiap waktu
    return result


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    output = sisd_example(data)
    print("Input  :", data)
    print("Output :", output)