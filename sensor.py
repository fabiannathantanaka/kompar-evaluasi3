import random
import time
from collections import namedtuple


DataSensor = namedtuple('DataSensor', [
    'id_sensor', 'jenis', 'nilai', 'status', 'satuan', 'delay', 'error'
])


KONFIGURASI_SENSOR = {
    "Lalu Lintas": {
        "satuan": "kendaraan",
        "range_nilai": (5, 120),
        "range_delay": (0.5, 2.0),
        "tingkat_error": 0.10,
    },
    "Suhu": {
        "satuan": "\u00b0C",
        "range_nilai": (25.0, 45.0),
        "range_delay": (1.0, 4.0),
        "tingkat_error": 0.10,
    },
    "Kelembaban": {
        "satuan": "%",
        "range_nilai": (30.0, 95.0),
        "range_delay": (2.0, 5.0),
        "tingkat_error": 0.05,
    },
    "Polusi": {
        "satuan": "\u00b5g/m\u00b3",
        "range_nilai": (10, 200),
        "range_delay": (1.0, 3.0),
        "tingkat_error": 0.08,
    },
    "Getaran": {
        "satuan": "mm/s",
        "range_nilai": (0.0, 50.0),
        "range_delay": (0.2, 1.0),
        "tingkat_error": 0.12,
    },
}


def _status_lalu_lintas(n):
    if n < 20: return "Sepi"
    if n <= 50: return "Lancar"
    if n <= 80: return "Padat"
    return "Macet"


def _status_suhu(n):
    if n < 28: return "Dingin"
    if n <= 35: return "Normal"
    if n <= 40: return "Panas"
    return "Berbahaya"


def _status_kelembaban(n):
    if n < 40: return "Kering"
    if n <= 70: return "Normal"
    return "Lembab"


def _status_polusi(n):
    if n < 50: return "Sehat"
    if n <= 100: return "Sedang"
    if n <= 150: return "Tidak Sehat"
    return "Berbahaya"


def _status_getaran(n):
    if n < 10: return "Aman"
    if n <= 25: return "Waspada"
    if n <= 40: return "Bahaya"
    return "Kritis"


FUNGSI_STATUS = {
    "Lalu Lintas": _status_lalu_lintas,
    "Suhu": _status_suhu,
    "Kelembaban": _status_kelembaban,
    "Polusi": _status_polusi,
    "Getaran": _status_getaran,
}


def baca_sensor(id_sensor, jenis, antrian_data, event_stop):
    konfig = KONFIGURASI_SENSOR[jenis]
    range_min, range_max = konfig["range_nilai"]
    delay_min, delay_max = konfig["range_delay"]
    satuan = konfig["satuan"]
    tingkat_error = konfig["tingkat_error"]
    fungsi_status = FUNGSI_STATUS[jenis]
    is_float = isinstance(range_min, float)

    while not event_stop.is_set():
        if random.random() < tingkat_error:
            delay = round(random.uniform(delay_min, delay_max), 2)
            time.sleep(delay)
            antrian_data.put(DataSensor(
                id_sensor, jenis, None, "ERROR", satuan, delay, True
            ))
            continue

        if is_float:
            nilai = round(random.uniform(range_min, range_max), 1)
        else:
            nilai = random.randint(range_min, range_max)

        status = fungsi_status(nilai)
        delay = round(random.uniform(delay_min, delay_max), 2)
        time.sleep(delay)

        antrian_data.put(DataSensor(
            id_sensor, jenis, nilai, status, satuan, delay, False
        ))
