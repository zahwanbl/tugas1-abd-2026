# Tugas 1: Eksplorasi dan Analisis Dataset Besar Indonesia

Repository ini adalah pengerjaan Tugas 1 mata kuliah Analisis Big Data (UMM), dikerjakan dari template `UMM-GURU/tugas1-abd-2026`.

**Mahasiswa:** Siti Zahwa Nabila Putri | **NIM:** 202310370311417 | **GitHub:** [zahwanbl](https://github.com/zahwanbl)

---

## Ringkasan Proyek: Analisis Cuaca Per Jam 34 Ibu Kota Provinsi Indonesia (2015-2025)

**Dataset:** data cuaca per jam dari Open-Meteo Historical Weather API (reanalisis ERA5) untuk 34 ibu kota provinsi, periode 1 Januari 2015 sampai 31 Desember 2025. Total **3.278.688 baris** (memenuhi syarat lebih dari 1 juta baris) dan 8 kolom: `time`, `temperature_2m`, `relative_humidity_2m`, `precipitation`, `wind_speed_10m`, `kota`, `lat`, `lon`. Detail sumber dan cara unduh ada di [`data/README.md`](data/README.md).

### Alur pengerjaan

| Tahap | Notebook | Isi |
|---|---|---|
| Milestone 1 | `notebooks/01_data_profiling.ipynb` | Profiling dataset dengan Polars dan DuckDB `SUMMARIZE` |
| Milestone 2 | `notebooks/02_data_cleaning.ipynb` | Konversi tipe waktu, deteksi dan penanganan outlier (IQR + windsorization), cek duplikat dan kelengkapan, validasi data, simpan ke `data/processed/` |
| Milestone 3 | `notebooks/03_eda_and_insights.ipynb` | Analisis temporal (`group_by_dynamic`, `rolling_mean`, `shift`, DuckDB window function), 6 visualisasi interaktif Plotly, 5 insight |

### Ringkasan hasil pembersihan data (Milestone 2)

- Tidak ada missing values dan tidak ada duplikat berdasarkan kunci (`kota`, `time`); 34 kota x 96.432 jam lengkap.
- Outlier suhu dan kecepatan angin ditangani dengan IQR + windsorization pada kolom baru `*_winsor` (nilai asli dipertahankan). Curah hujan hanya ditandai (`hujan_ekstrem`, > 20 mm/jam) karena distribusinya sangat miring.
- Semua aturan validasi domain lolos. Jumlah baris sebelum dan sesudah cleaning sama (3.278.688).

### Ringkasan insight utama (Milestone 3)

1. **Tren dan musiman:** suhu rata-rata naik tipis dari 26,375 °C (2015) ke 26,624 °C (2025), tetapi fluktuasi antar tahun lebih besar daripada kenaikan tersebut. Curah hujan rata-rata tertinggi pada Januari (310,2 mm/bulan).
2. **Distribusi dan anomali:** curah hujan harian sangat condong ke nilai kecil. Hujan >= 50 mm hanya 0,62% kota-hari, dan 5 kota menyumbang sekitar 46% dari 487 jam hujan ekstrem.
3. **Korelasi:** suhu dan kelembapan berkorelasi negatif kuat (r = -0,80), sedangkan curah hujan hampir tidak berkorelasi linear dengan variabel lain.
4. **Perbedaan antar kota:** Bandung paling sejuk (23,06 °C), Surabaya paling panas (27,72 °C), Jayapura paling basah (4.989 mm/tahun), Kupang paling kering (1.391 mm/tahun).
5. **Rekomendasi:** peringatan dini hujan ekstrem diprioritaskan pada kota rawan, perencanaan musiman disesuaikan per wilayah, dan temuan divalidasi dengan data stasiun BMKG karena ERA5 adalah estimasi model, bukan pengamatan stasiun.

Grafik interaktif tersimpan di `output/figures/` (file HTML).

---

## Cara Menjalankan Ulang dari Awal

Pastikan Docker sudah terpasang, lalu jalankan dari folder repository:

```bash
docker build -t tugas1-bigdata .
docker run --rm -p 8888:8888 -v "$(pwd)":/home/jovyan/work tugas1-bigdata
```

Buka JupyterLab di `http://localhost:8888/lab`.

> Konfigurasi Docker ini menjalankan JupyterLab tanpa password atau token, sehingga hanya untuk penggunaan lokal. Jangan dipakai di server atau jaringan publik.

Langkah berikutnya di dalam JupyterLab:

1. **Unduh data.** Buka Terminal di JupyterLab, lalu jalankan `python src/download_cuaca.py`. Skrip mengunduh data tiap kota dari Open-Meteo dan menggabungkannya menjadi `data/raw/cuaca_indonesia_2015_2025.parquet`. Proses bisa memakan waktu karena ada batas laju (rate limit) API. Jika terhenti, jalankan lagi; kota yang sudah terunduh dilewati.
2. **Jalankan notebook berurutan:** `01_data_profiling.ipynb`, lalu `02_data_cleaning.ipynb`, lalu `03_eda_and_insights.ipynb` (menu Run, Run All Cells).
3. Hasil pembersihan tersimpan di `data/processed/cuaca_bersih.parquet`, dan grafik di `output/figures/`.

Data tidak ikut di-commit karena berukuran besar (`data/raw/` masuk `.gitignore`).

---

## Tentang Tugas

Setelah repository dibuat, nama repository sebaiknya diubah menjadi `tugas1-[username_github]`.

### Milestone

| Tahap | Target | Bukti yang dikumpulkan |
|---|---|---|
| Milestone 1 | Pertemuan 3 | Dataset >= 500 MB atau > 1 juta baris, `data/README.md`, `notebooks/01_data_profiling.ipynb` |
| Milestone 2 | Pertemuan 5 | Cleaning dengan Polars dan profiling DuckDB `SUMMARIZE` |
| Milestone 3 | Pertemuan 8 | Analisis temporal/ruang dan minimal 6 visualisasi interaktif |
| Final | Pertemuan 10 | Minimal 5 insight, Dockerfile, dan dokumentasi akhir |

### Output yang Diharapkan

Repository final harus dapat dijalankan ulang dari awal dan memuat:

- Dataset Indonesia yang terdokumentasi (minimal 500 MB atau 1 juta baris) beserta instruksi unduh.
- Notebook profiling, cleaning, dan EDA yang dapat dieksekusi berurutan.
- Cleaning dan validasi data: missing values, duplikasi, outlier, dan aturan kualitas.
- Analisis temporal atau spasial, minimal 6 visualisasi interaktif (Plotly atau Altair), dan minimal 5 insight.
- Environment yang dapat direproduksi: `Dockerfile`, `requirements.txt`, dan petunjuk eksekusi.
- Riwayat commit bertahap untuk setiap milestone.

### Kaitan dengan Materi Perkuliahan

| Materi | Pertemuan | Penerapan |
|---|---|---|
| Polars dan lazy evaluation | 2 | Profiling dan transformasi dengan `scan_*`, expressions, pipeline |
| DuckDB dan format data | 3 | Query analitik, `SUMMARIZE`, Parquet bila sesuai |
| Data quality dan cleaning | 4 | Missing values, duplikasi, outlier, validasi |
| EDA dan visualisasi | 5 | Visualisasi interaktif dan insight |
| Time series | 6 | Pola waktu atau spasial |
| Dask, NLP, dan ML | 7-9 | Opsional |
| Streamlit dan Docker | 10-11 | Dokumentasi Docker; dashboard Streamlit opsional |

### Ringkasan Penilaian (25% nilai akhir)

| Aspek | Bobot |
|---|---|
| Konsistensi commit dan GitHub workflow | 20% |
| Data handling dengan Polars dan DuckDB | 25% |
| Cleaning dan data quality | 15% |
| Visualisasi dan insight | 25% |
| Reproduktivitas dan Docker | 15% |

Target tertinggi adalah analisis yang efisien, terdokumentasi, dapat direproduksi, dan menunjukkan proses kerja yang konsisten.

### Struktur Repository

```
.
├── .github/workflows/lint_check.yml
├── data/README.md
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_eda_and_insights.ipynb
├── output/figures/
├── src/
├── Dockerfile
├── requirements.txt
└── README.md
```

### Aturan Teknis

- Gunakan Polars untuk manipulasi data dan DuckDB untuk analitik SQL.
- Dataset minimal 500 MB atau lebih dari 1 juta baris.
- Jangan commit file data besar; simpan instruksi unduh dan sumber data di `data/README.md`.
- Gunakan commit bertahap dengan pesan jelas, misalnya `feat: add initial dataset profiling`.

### Pengumpulan

1. Fork repository tugas (`UMM-GURU/tugas1-abd-2026`) ke akun GitHub sendiri, lalu clone hasil fork.
2. Kerjakan notebook secara berurutan dan simpan perubahan secara berkala.
3. Commit dengan pesan yang jelas, lalu push ke branch utama:
   ```bash
   git add <file yang diubah>
   git commit -m "pesan commit"
   git push origin main
   ```
4. Buka repository GitHub dan pastikan file sudah muncul serta ada commit hasil pekerjaan.
5. Salin URL repository untuk penilaian jika diminta dosen.

---

## Integritas Akademik dan Penggunaan AI

- Dilarang menyalin kode, laporan, atau visualisasi tanpa sitasi dan atribusi.
- Dilarang menggunakan jasa joki atau menyerahkan pekerjaan yang tidak dapat dijelaskan sendiri.
- AI boleh digunakan untuk belajar, mencari rujukan, menjelaskan konsep, dan debugging, tetapi tanggung jawab atas kebenaran dan kualitas tetap pada mahasiswa.
- Mahasiswa harus dapat menjelaskan setiap bagian kode serta memverifikasi hasilnya.
- Setiap penggunaan AI wajib dicantumkan di AI Disclosure Statement.
- Pelanggaran pertama bernilai 0 untuk tugas terkait; pelanggaran berikutnya dapat berakibat nilai E untuk mata kuliah.

## AI Disclosure Statement

- **Alat AI yang digunakan:** Claude (Anthropic).
- **Bagian yang dibantu:** pemecahan masalah setup (WSL2, Docker, Git/GitHub), penyusunan draf skrip unduh data dan draf kode notebook 01-03, penjelasan konsep (windsorization, window function, korelasi), serta penyusunan draf catatan milestone dan insight.
- **Verifikasi yang dilakukan:** menjalankan semua cell dari awal pada data asli, mencocokkan angka di catatan dan insight dengan output notebook, memeriksa grafik secara langsung, dan mempelajari setiap bagian kode agar dapat dijelaskan sendiri.