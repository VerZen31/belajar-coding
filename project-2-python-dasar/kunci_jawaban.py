# ============================================================
# KUNCI JAWABAN — coba kerjakan soal_latihan.py DULU sebelum buka ini!
# ============================================================

print("=== KUNCI JAWABAN ===\n")


# ------------------------------------------------------------
# SOAL 1 — Variabel
# ------------------------------------------------------------
print("--- Soal 1 ---")
nama = "Aldi"
kota = "Medan"
penghasilan_harian = 150000

print(f"Saya {nama} dari {kota}, penghasilan saya Rp {penghasilan_harian}/hari")
# CATATAN: f"..." = f-string, cara modern menyisipkan variabel ke teks.
# Alternatif: print("Saya", nama, "dari", kota, ...)


# ------------------------------------------------------------
# SOAL 2 — If
# ------------------------------------------------------------
print("\n--- Soal 2 ---")

def kategori_jarak(jarak):
    if jarak <= 3:
        return "Dekat"
    elif jarak <= 10:
        return "Sedang"
    else:
        return "Jauh"

for j in [2, 7, 20]:
    print(f"Jarak {j} km -> {kategori_jarak(j)}")


# ------------------------------------------------------------
# SOAL 3 — Loop dengan nomor
# ------------------------------------------------------------
print("\n--- Soal 3 ---")
rute = ["Pasar", "Kampus", "Mall", "Terminal"]

# Cara 1: pakai enumerate (start=1 supaya mulai dari 1, bukan 0)
for nomor, tempat in enumerate(rute, start=1):
    print(f"{nomor}. {tempat}")

# Cara 2 (manual, tanpa enumerate):
# nomor = 1
# for tempat in rute:
#     print(f"{nomor}. {tempat}")
#     nomor = nomor + 1


# ------------------------------------------------------------
# SOAL 4 — Fungsi dengan diskon
# ------------------------------------------------------------
print("\n--- Soal 4 ---")

def hitung_tarif(jarak):
    tarif = jarak * 2000
    if jarak > 10:
        tarif = tarif * 0.9      # diskon 10% (bayar 90%)
    return int(tarif)

print(f"Jarak 5 km  -> Rp {hitung_tarif(5)}")
print(f"Jarak 15 km -> Rp {hitung_tarif(15)}  (diskon 10%)")


# ------------------------------------------------------------
# SOAL 5 — Tantangan: gabungan semuanya
# ------------------------------------------------------------
print("\n--- Soal 5 ---")

def cek_target(ip):
    bagian = ip.split(".")          # "192.168.1.1" -> ["192","168","1","1"]
    depan = bagian[0]               # ambil bagian pertama = "192"

    if depan == "192" or depan == "10":
        return "IP Lokal (aman)"
    elif depan == "8":
        return "IP Publik Google"
    else:
        return "IP tidak dikenal"

for alamat in ["192.168.1.1", "10.0.0.5", "8.8.8.8", "1.2.3.4"]:
    print(f"{alamat:<15} -> {cek_target(alamat)}")


print("\n=== Selesai! ===")
