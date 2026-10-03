# ============================================================
# RANGKUMAN PYTHON DASAR (CHEAT SHEET)
# Referensi belajar — buka file ini kapan saja saat lupa!
# Jalankan: python rangkuman_python.py
# ============================================================


# ============================================================
# 1. VARIABEL & TIPE DATA
# ============================================================
# Tipe data dasar:
nama = "Aldi"            # str   (teks, harus pakai tanda kutip)
umur = 25                # int   (bilangan bulat)
tinggi = 170.5           # float (desimal)
sudah_menikah = False    # bool  (True / False)

# Cek tipe data:
print(type(nama))        # <class 'str'>
print(type(umur))        # <class 'int'>

# Konversi tipe (casting):
angka_teks = "100"
angka = int(angka_teks)      # teks -> bilangan bulat
desimal = float("3.14")      # teks -> desimal
teks = str(99)               # angka -> teks

print("\n=== 1. VARIABEL ===")
print("Nama:", nama, "| Umur:", umur, "| Tinggi:", tinggi)
print("Casting:", angka + 1, desimal, teks)


# ============================================================
# 2. OPERATOR
# ============================================================
# Aritmatika:
#   +  tambah        -  kurang         *  kali
#   /  bagi (hasil desimal)    //  bagi bulat
#   %  sisa bagi (modulus)     **  pangkat
print("\n=== 2. OPERATOR ===")
print("10 / 3  =", 10 / 3)      # 3.333... (hasil desimal)
print("10 // 3 =", 10 // 3)     # 3 (dibulatkan ke bawah)
print("10 % 3  =", 10 % 3)      # 1 (sisa pembagian)
print("2 ** 3  =", 2 ** 3)      # 8 (2 pangkat 3)

# Perbandingan: ==  !=  >  <  >=  <=
# Logika: and  or  not


# ============================================================
# 3. INPUT DARI USER
# ============================================================
# name = input("Siapa namamu? ")           # input selalu str!
# umur = int(input("Umurmu? "))            # ubah ke angka pakai int()
# print(f"Halo {name}, umurmu {umur}")
# (BARIS DI ATAS di-comment biar file ini jalan otomatis)


# ============================================================
# 4. F-STRING (menyisipkan variabel ke teks) — PALING SERING DIPAKAI
# ============================================================
print("\n=== 4. F-STRING ===")
harga = 50000
print(f"Total belanja: Rp {harga:,}")     # Rp 50,000 (pemisah ribuan)
print(f"Setengahnya: {harga / 2:.2f}")    # 25000.00 (2 angka di belakang koma)


# ============================================================
# 5. IF / ELIF / ELSE — keputusan
# ============================================================
print("\n=== 5. IF/ELIF/ELSE ===")
nilai = 75

if nilai >= 85:
    print("Nilai: A")
elif nilai >= 70:
    print("Nilai: B")
elif nilai >= 60:
    print("Nilai: C")
else:
    print("Nilai: D")

# Singkat (ternary):
status = "LULUS" if nilai >= 60 else "TIDAK LULUS"
print("Status:", status)


# ============================================================
# 6. LOOP — pengulangan
# ============================================================
print("\n=== 6. LOOP ===")

# for: mengulang isi list
for buah in ["apel", "mangga", "jeruk"]:
    print("-", buah)

# range(): mengulang angka
# range(5)        -> 0,1,2,3,4
# range(1, 6)     -> 1,2,3,4,5
# range(0, 10, 2) -> 0,2,4,6,8 (langkah 2)
for i in range(1, 4):
    print("putaran", i)

# while: mengulang SELAMA kondisi benar
hitung = 3
while hitung > 0:
    print("hitung mundur:", hitung)
    hitung = hitung - 1    # lupa baris ini = loop tak berujung!

# break = keluar paksa dari loop
# continue = lompat ke putaran berikutnya
for i in range(5):
    if i == 3:
        break          # berhenti saat i == 3
    print("i =", i)


# ============================================================
# 7. LIST — kumpulan data (bisa diubah)
# ============================================================
print("\n=== 7. LIST ===")
skills = ["Networking", "Python", "HTML/CSS"]

skills.append("Git")          # tambah di akhir
skills[0]                     # ambil item pertama (mulai dari 0!)
skills[-1]                    # ambil item terakhir
len(skills)                   # hitung jumlah item (4)
"Python" in skills            # True — cek anggota

print("Jumlah skill:", len(skills))
print("Item pertama:", skills[0], "| Terakhir:", skills[-1])
print("Punya Python?", "Python" in skills)

# Loop dengan nomor
for i, skill in enumerate(skills, start=1):
    print(f"{i}. {skill}")


# ============================================================
# 8. STRING — teks dan operasinya
# ============================================================
print("\n=== 8. STRING ===")
kalimat = "Belajar Python itu menyenangkan"

print(kalimat.upper())        # HURUF BESAR SEMUA
print(kalimat.lower())        # huruf kecil semua
print(kalimat.replace("menyenangkan", "mudah"))
print(kalimat.split())        # pisah jadi list kata
print(kalimat[0:7])           # "Belajar" — ambil sebagian (slice)
print(len(kalimat))           # panjang teks
print("Python" in kalimat)    # True — cek kata ada di dalam


# ============================================================
# 9. DICTIONARY — data pasangan kunci:nilai
# ============================================================
print("\n=== 9. DICTIONARY ===")
siswa = {
    "nama": "Aldi",
    "umur": 25,
    "kota": "Medan",
}

print("Nama:", siswa["nama"])
siswa["pekerjaan"] = "ojol"          # tambah pasangan baru
for kunci, nilai in siswa.items():
    print(f"- {kunci}: {nilai}")


# ============================================================
# 10. FUNGSI
# ============================================================
print("\n=== 10. FUNGSI ===")

# def = definisikan fungsi; return = hasil yang dikembalikan
def luas_persegi(sisi):
    return sisi * sisi

def sapa(nama, ucapan="Hai"):          # parameter punya nilai default
    return f"{ucapan}, {nama}!"

print("Luas persegi 5x5 =", luas_persegi(5))
print(sapa("Aldi"))
print(sapa("Aldi", "Selamat malam"))


# ============================================================
# 11. ERROR HANDLING — antisipasi program crash
# ============================================================
print("\n=== 11. TRY/EXCEPT ===")

try:
    hasil = 10 / 0
except ZeroDivisionError:
    print("Error: tidak bisa dibagi nol!")
finally:
    print("Blok ini selalu jalan")


# ============================================================
# 12. CARA MINTA BANTUAN DI PYTHON
# ============================================================
# help(len)           -> bantu penjelasan fungsi len
# dir("teks")         -> daftar semua kemampuan string
# type(x)             -> cek tipe data
# print(dir(str))     -> semua method string (upper, lower, dll)


print("\n=== SELESAI — simpan file ini, baca ulang kapan saja! ===")
