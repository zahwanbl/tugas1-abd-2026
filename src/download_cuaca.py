import os
import time
import requests
import polars as pl

KOTA = {
    "Banda Aceh": (5.55, 95.32), "Medan": (3.59, 98.67), "Padang": (-0.95, 100.35),
    "Pekanbaru": (0.51, 101.45), "Tanjungpinang": (0.92, 104.45), "Jambi": (-1.61, 103.61),
    "Palembang": (-2.98, 104.76), "Pangkal Pinang": (-2.13, 106.11), "Bengkulu": (-3.80, 102.26),
    "Bandar Lampung": (-5.43, 105.26), "Serang": (-6.12, 106.15), "Jakarta": (-6.21, 106.85),
    "Bandung": (-6.91, 107.61), "Semarang": (-6.97, 110.42), "Yogyakarta": (-7.80, 110.36),
    "Surabaya": (-7.25, 112.75), "Denpasar": (-8.65, 115.22), "Mataram": (-8.58, 116.12),
    "Kupang": (-10.18, 123.58), "Pontianak": (-0.03, 109.33), "Palangka Raya": (-2.21, 113.92),
    "Banjarmasin": (-3.32, 114.59), "Samarinda": (-0.50, 117.15), "Tanjung Selor": (2.84, 117.37),
    "Manado": (1.47, 124.84), "Gorontalo": (0.54, 123.06), "Palu": (-0.90, 119.87),
    "Mamuju": (-2.68, 118.89), "Makassar": (-5.15, 119.43), "Kendari": (-3.97, 122.51),
    "Ambon": (-3.70, 128.18), "Sofifi": (0.74, 127.57), "Manokwari": (-0.86, 134.06),
    "Jayapura": (-2.53, 140.72),
}
URL = "https://archive-api.open-meteo.com/v1/archive"
VARS = "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/raw/kota", exist_ok=True)

for nama, (lat, lon) in KOTA.items():
    path = f"data/raw/kota/{nama}.parquet"
    if os.path.exists(path):
        print(nama, "sudah ada, skip")
        continue

    for attempt in range(8):
        try:
            r = requests.get(URL, params={
                "latitude": lat, "longitude": lon,
                "start_date": "2015-01-01", "end_date": "2025-12-31",
                "hourly": VARS, "timezone": "Asia/Jakarta",
            }, timeout=120)
            if r.status_code == 200:
                break
            print(nama, "status", r.status_code, "- coba lagi")
        except requests.exceptions.RequestException as e:
            print(nama, "koneksi gagal:", type(e).__name__, "- coba lagi")
        time.sleep(20 * (attempt + 1))
    else:
        raise SystemExit(f"{nama} gagal setelah 8 percobaan")

    h = r.json()["hourly"]
    pl.DataFrame(h).with_columns(
        pl.lit(nama).alias("kota"), pl.lit(lat).alias("lat"), pl.lit(lon).alias("lon")
    ).write_parquet(path)
    print(nama, "OK")
    time.sleep(2)

df = pl.scan_parquet("data/raw/kota/*.parquet").collect()
df.write_parquet("data/raw/cuaca_indonesia_2015_2025.parquet")
print(df.shape)