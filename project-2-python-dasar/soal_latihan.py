# ============================================================
# SOAL LATIHAN — Python Dasar (variabel, if, loop, fungsi)
# ============================================================
# Cara kerja:
#   1. Tulis jawabanmu DI BAWAH setiap soal
#   2. Jalankan:  python soal_latihan.py
#   3. Cek jawabanmu dengan file: kunci_jawaban.py
#
# Aturan: coba sendiri dulu minimal 10 menit sebelum lihat kunci.
# ============================================================

print("=== Menjalankan soal latihan ===\n")


# ------------------------------------------------------------
# SOAL 1 (mudah) — VARIABEL
# Bikin variabel: nama, kota, dan penghasilan_harian (angka).
# Lalu cetak jadi kalimat:
#   "Saya [nama] dari [kota], penghasilan saya Rp [penghasilan_harian]/hari"
# ------------------------------------------------------------

# TULIS JAWABANMU DI SINI:



# ------------------------------------------------------------
# SOAL 2 (mudah) — IF
# Bikin variabel `jarak` (angka km).
# Kalau jarak <= 3  -> cetak "Dekat"
# Kalau jarak <= 10 -> cetak "Sedang"
# Selain itu        -> cetak "Jauh"
# Lalu tes dengan 3 nilai berbeda.
# ------------------------------------------------------------

# TULIS JAWABANMU DI SINI:



# ------------------------------------------------------------
# SOAL 3 (sedang) — LOOP
# Kamu punya daftar rute perjalanan:
#   rute = ["Pasar", "Kampus", "Mall", "Terminal"]
# Cetak tiap rute dengan nomor:
#   1. Pasar
#   2. Kampus
#   ...
# PETUNJUK: pakai for + enumerate(), atau hitung manual pakai variabel
# ------------------------------------------------------------

# TULIS JAWABANMU DI SINI:



# ------------------------------------------------------------
# SOAL 4 (sedang) — FUNGSI
# Bikin fungsi `hitung_tarif(jarak)` yang:
#   - 2000 per km
#   - kalau jarak > 10 km, dapat DISKON 10%
#   - mengembalikan total (angka bulat)
# Tes: hitung_tarif(5) dan hitung_tarif(15)
# ------------------------------------------------------------

# TULIS JAWABANMU DI SINI:



# ------------------------------------------------------------
# SOAL 5 (tantangan) — GABUNGAN SEMUA
# Bikin fungsi `cek_target(ip)` yang menerima string IP seperti "192.168.1.1"
#   - Pisahkan jadi 4 bagian pakai .split(".")
#   - Kalau bagian pertama == "192" ATAU "10" -> "IP Lokal (aman)"
#   - Kalau bagian pertama == "8"             -> "IP Publik Google"
#   - Selain itu                              -> "IP tidak dikenal"
# Tes dengan: "192.168.1.1", "10.0.0.5", "8.8.8.8", "1.2.3.4"
# PETUNJUK: ip.split(".") menghasilkan list, ambil bagian pertama dengan [0]
# ------------------------------------------------------------

# TULIS JAWABANMU DI SINI:



print("\n=== Selesai! Sekarang cek kunci_jawaban.py ===")
