# Data Tugas 1

## Dataset yang Dipilih

Isi informasi berikut sebelum Milestone 1.

| Item                    | Isi                                                                          |
| ----------------------- | ---------------------------------------------------------------------------- |
| Nama dataset            | Data cuaca historis per jam 34 ibu kota provinsi Indonesia                   |
| Sumber                  | Open-Meteo Historical Weather API (reanalisis ERA5): https://open-meteo.com/ |
| Lisensi/ketentuan pakai | CC BY 4.0, atribusi ke Open-Meteo; gratis untuk penggunaan non-komersial     |
| Ukuran                  | 3.278.688 baris (> 1 juta), 8 kolom; 17 MB dalam format Parquet terkompresi  |
| Periode data            | 1 Januari 2015 - 31 Desember 2025 (zona waktu Asia/Jakarta)                  |
| Unit analisis           | Satu baris = satu ibu kota provinsi pada satu jam                            |

Kolom: time, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m, kota, lat, lon.

Catatan: data berasal dari reanalisis ERA5 (model grid), bukan observasi stasiun BMKG. Koordinat adalah titik pusat kota.

Cara memperoleh data: jalankan `python src/download_cuaca.py` dari root repo. Skrip mengunduh per kota ke `data/raw/kota/`, lalu menggabungkannya menjadi `data/raw/cuaca_indonesia_2015_2025.parquet`.

| Situs | Kegunaan |
|---|---|
| [Satu Data Indonesia](https://data.go.id/) | Portal data terbuka lintas instansi pemerintah Indonesia. |
| [Badan Pusat Statistik](https://www.bps.go.id/) | Statistik sosial, ekonomi, kependudukan, dan data wilayah. |
| [BMKG Data Online](https://dataonline.bmkg.go.id/) | Data cuaca, iklim, gempa bumi, dan observasi meteorologi. |
| [Hugging Face Datasets](https://huggingface.co/datasets) | Dataset publik yang dapat dicari berdasarkan topik, bahasa, atau ukuran. |
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Katalog dataset publik; periksa lisensi dan dokumentasi pembuatnya. |
| [Google Dataset Search](https://datasetsearch.research.google.com/) | Mesin pencari untuk menemukan dataset dari berbagai portal. |

## Cara Memperoleh Data

1. Buka URL sumber di atas.
2. Unduh file ke folder `data/raw/` tanpa mengubah data mentah.
3. Catat nama file dan checksum bila tersedia.
4. Ubah variabel `DATA_PATH` pada `notebooks/01_data_profiling.ipynb` agar menunjuk ke file tersebut.

## Aturan Penyimpanan

- Jangan commit dataset mentah atau hasil olahan berukuran besar ke Git.
- File pada `data/raw/` adalah data asli dan tidak boleh diubah.
- Simpan hasil transformasi yang dapat direproduksi pada `data/processed/`.
