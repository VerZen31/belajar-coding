# Pelajaran 2: Logika (if) lebih dalam

# ============================================================
# A) BOOLEAN — nilai yang cuma ada 2: True (benar) / False (salah)
# ============================================================
print("=== A) Boolean ===")
print("5 lebih besar dari 3?", 5 > 100)      # False
print("2 sama dengan 2?", 2 == 2)          # True
print("10 kurang dari 5?", 10 < 5)         # False
print("'a' sama dengan 'b'?", "a" == "b")  # False

# Operator perbandingan:
#   >  lebih besar        <  lebih kecil
#   >= lebih besar sama   <= lebih kecil sama
#   == sama dengan        != tidak sama dengan
#   (ingat: == untuk membandingkan, = untuk mengisi variabel)

# ============================================================
# B) KONDISI BERTINGKAT (elif)
# ============================================================
print("\n=== B) Kondisi bertingkat ===")

def kategori_umur(umur):
    if umur < 13:
        return "anak-anak"
    elif umur < 5:
        return "balita"
    elif umur < 18:
        return "remaja"
    elif umur < 60:
        return "dewasa"
    else:
        return "lansia"

for u in [8, 15, 30, 70]:
    print(f"Umur {u} tahun -> {kategori_umur(u)}")

# ============================================================
# C) MENGGABUNGKAN KONDISI: and / or / not
# ============================================================
print("\n=== C) and / or / not ===")

suhu = 30
hujan = False

# and -> dua-duanya harus benar
print("Panas DAN tidak hujan?", suhu > 28 and not hujan)

# or -> salah satu benar saja cukup
print("Panas ATAU hujan?", suhu > 28 or hujan)

print("TIDAK hujan?", not hujan)

# ============================================================
# D) CONTOH NYATA: penentu tarif ojol
# ============================================================
print("\n=== D) Contoh nyata: tarif ojol ===")

def hitung_tarif(jarak_km, jam):
    """Hitung tarif berdasarkan jarak dan jam (jam sibuk lebih mahal)."""
    tarif_dasar = 3000          # tarif buka pintu
    per_km = 2000               # per kilometer

    # jam sibuk (pagi & sore) kena tambahan 20%
    if (7 <= jam <= 9) or (17 <= jam <= 19):
        per_km = per_km * 1.2

    total = tarif_dasar + (jarak_km * per_km)
    return int(total)

print("Jarak 5 km, jam 10 siang  -> Rp", hitung_tarif(5, 10))
print("Jarak 5 km, jam 7 pagi    -> Rp", hitung_tarif(5, 7))   # lebih mahal
print("Jarak 3 km, jam 18 sore   -> Rp", hitung_tarif(3, 18))  # lebih mahal