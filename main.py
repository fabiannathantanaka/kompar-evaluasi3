import queue
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from sensor import baca_sensor, DataSensor, KONFIGURASI_SENSOR


def proses_data(antrian_data, total_data):
    stats = defaultdict(lambda: {"total_nilai": 0, "all_count": 0, "valid_count": 0, "errors": 0})
    semua_data = []
    jumlah_data = 0

    print("=" * 100)
    print(f"{'No':<4} {'Sensor':<12} {'Jenis':<14} {'Nilai':<10} {'Status':<14} {'Satuan':<12} {'Delay':<8} {'Error':<6}")
    print("-" * 100)

    while jumlah_data < total_data:
        data = antrian_data.get()
        semua_data.append(data)
        jumlah_data += 1

        jenis = data.jenis
        nilai_str = f"{data.nilai}" if data.nilai is not None else "-"
        error_str = "YA" if data.error else "-"

        s = stats[jenis]
        s["all_count"] += 1
        if data.error:
            s["errors"] += 1
        else:
            s["valid_count"] += 1
            s["total_nilai"] += data.nilai

        print(f"{jumlah_data:<4} {data.id_sensor:<12} {jenis:<14} {nilai_str:<10} {data.status:<14} {data.satuan:<12} {data.delay:<8.2f} {error_str:<6}")

    print("=" * 100)

    print(f"\n{'=' * 100}")
    print(f"{'S U M M A R Y   P E R   K A T E G O R I':^100}")
    print(f"{'=' * 100}")

    for jenis, konfig in KONFIGURASI_SENSOR.items():
        s = stats[jenis]
        rata2 = s["total_nilai"] / s["valid_count"] if s["valid_count"] > 0 else 0
        pct_error = (s["errors"] / s["all_count"] * 100) if s["all_count"] > 0 else 0
        print(f"\n  [{jenis}]")
        print(f"    Data total       : {s['all_count']}")
        print(f"    Data valid       : {s['valid_count']}")
        print(f"    Error            : {s['errors']} ({pct_error:.1f}%)")
        print(f"    Rata-rata nilai  : {rata2:.1f} {konfig['satuan']}")

    print(f"\n{'=' * 100}")
    print(f"{'Total data diproses':<40} {jumlah_data:>8}")

    return semua_data


def main():
    antrian_data = queue.Queue()
    event_stop = threading.Event()

    DAFTAR_SENSOR = [
        ("LLA-A", "Lalu Lintas"),
        ("LLA-B", "Lalu Lintas"),
        ("SUH-A", "Suhu"),
        ("SUH-B", "Suhu"),
        ("KLM-A", "Kelembaban"),
        ("KLM-B", "Kelembaban"),
        ("POL-A", "Polusi"),
        ("POL-B", "Polusi"),
        ("GTR-A", "Getaran"),
        ("GTR-B", "Getaran"),
    ]

    SIKLUS_PER_SENSOR = 8
    TOTAL_DATA = len(DAFTAR_SENSOR) * SIKLUS_PER_SENSOR

    print("\n")
    print("=" * 100)
    print(f"{'SIMULASI SMART CITY - MULTI JENIS SENSOR IoT':^100}")
    print(f"{'Komputasi Paralel & Sistem Terdistribusi':^100}")
    print("=" * 100)
    print(f"\n  [INFO] {len(DAFTAR_SENSOR)} sensor dari 5 jenis berjalan paralel")
    print(f"  [INFO] Setiap sensor mengirim {SIKLUS_PER_SENSOR} data")
    print(f"  [INFO] Total data yang akan diproses: {TOTAL_DATA}")
    print(f"  [INFO] Tingkat error: 5-12% per jenis sensor\n")

    waktu_mulai = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for id_sensor, jenis in DAFTAR_SENSOR:
            executor.submit(baca_sensor, id_sensor, jenis, antrian_data, event_stop)

        print(f"\n  {'[STATUS] Semua sensor berjalan PARALEL...':^100}\n")

        semua_data = proses_data(antrian_data, TOTAL_DATA)

        event_stop.set()

    durasi = time.time() - waktu_mulai

    print(f"\n{'[WAKTU EKSEKUSI]':^100}")
    print(f"{'Total waktu':<40} {durasi:>8.2f} detik")
    print(f"{'Rata-rata per data':<40} {durasi / TOTAL_DATA:>8.3f} detik")
    print(f"{'Throughput':<40} {TOTAL_DATA / durasi:>8.1f} data/detik")
    print("\n" + "=" * 100)
    print(f"{'SIMULASI SELESAI':^100}")
    print("=" * 100)


if __name__ == "__main__":
    main()
