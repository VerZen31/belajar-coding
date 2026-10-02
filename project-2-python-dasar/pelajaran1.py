# Pelajaran 1: Variabel, if, dan loop

# 1) VARIABEL — seperti kotak berlabel untuk menyimpan data
nama = "Gilang"
umur = 25
pekerjaan = "Driver shopeefood"

print("Halo, nama saya", nama)
print("Umur saya", umur, "tahun")

# 2) IF — komputer mengambil keputusan
jam = 19   # coba ganti angka ini

if jam < 12:
    print("Sekarang masih pagi")
elif jam < 18:
    print("Sekarang siang/sore")
else:
    print("Sekarang malam — waktunya belajar coding!")

# 3) LOOP — mengulang perintah tanpa nulis berkali-kali
print("\nDaftar skill saya:")
skills = ["Networking", "Python", "HTML/CSS", "Git"]

for s in skills:
    print("-", s)

# 4) FUNGSI — blok perintah yang bisa dipakai berulang
def sapa(nama_orang):
    return "Hai " + nama_orang + ", semangat belajar!"

print()
print(sapa("gilang"))
print(sapa("Teman"))
