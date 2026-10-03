# -*- coding: utf-8 -*-
"""PDF laporan temuan SQLi — format laporan bug bounty profesional."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, Preformatted)
from reportlab.lib.enums import TA_LEFT

OUT = r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/LAPORAN-TEMUAN-SQLI.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=17, spaceAfter=2,
                    textColor=colors.HexColor("#0f172a"))
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontSize=10,
                     textColor=colors.HexColor("#64748b"), alignment=TA_LEFT)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12.5,
                    spaceBefore=10, spaceAfter=4,
                    textColor=colors.HexColor("#1e3a8a"))
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontSize=9.5, leading=13.5)
CODE = ParagraphStyle("CODE", parent=styles["Code"], fontName="Courier",
                      fontSize=8.5, leading=11.5,
                      backColor=colors.HexColor("#f1f5f9"))
SEV = ParagraphStyle("SEV", parent=BODY, textColor=colors.HexColor("#b91c1c"),
                     fontName="Helvetica-Bold")

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=16*mm, bottomMargin=16*mm,
                        leftMargin=18*mm, rightMargin=18*mm,
                        title="Laporan Temuan: SQL Injection - Filter Kategori")
story = []

# ================= HEADER =================
story.append(Paragraph("LAPORAN TEMUAN KEAMANAN", H1))
story.append(Paragraph("SQL Injection pada filter kategori — membocorkan produk tersembunyi", SUB))
story.append(Spacer(1, 6))

meta = Table([
    ["ID", "web-001", "Tanggal", "3 Oktober 2026"],
    ["Target", "Aplikasi lab milik sendiri (localhost:8010)", "Penguji", "Aldi + Hermes Agent"],
    ["Kelas", "SQL Injection (CWE-89)", "Status", "CONFIRMED (diverifikasi)"],
    ["Severity", "MEDIUM", "Skor CVSS", "5.3 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)"],
], colWidths=[22*mm, 62*mm, 24*mm, 62*mm])
meta.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e7ff")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(meta)

# ================= 1. RINGKASAN =================
story.append(Paragraph("1. Ringkasan Eksekutif", H2))
story.append(Paragraph(
    "Parameter <b>kategori</b> pada endpoint <b>GET /filter</b> digabungkan langsung "
    "(string concatenation) ke dalam query SQL tanpa parameterisasi. Penyerang dapat "
    "menyuntik payload <b>Gifts' OR 1=1--</b> untuk mematikan filter <b>released = 1</b>, "
    "sehingga seluruh produk — termasuk yang dirahasiakan/belum dirilis — ikut "
    "ditampilkan tanpa autentikasi.", BODY))

# ================= 2. KOMPONEN =================
story.append(Paragraph("2. Komponen Terdampak", H2))
story.append(Paragraph("Endpoint: <b>GET /filter?kategori=&lt;input&gt;</b>", BODY))
story.append(Paragraph("File rentan: <b>sqli_app.py</b> → fungsi <b>query_products()</b>", BODY))
story.append(Spacer(1, 3))
story.append(Preformatted(
    "SELECT * FROM products\nWHERE kategori = '<INPUT_USER>' AND released = 1", CODE))

# ================= 3. POC =================
story.append(Paragraph("3. Bukti Konsep (PoC)", H2))
story.append(Paragraph("<b>Request (URL-encoded):</b>", BODY))
story.append(Spacer(1, 2))
story.append(Preformatted(
    "GET /filter?kategori=Gifts%27%20OR%201=1-- HTTP/1.1\n"
    "Host: 127.0.0.1:8010", CODE))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Query yang terbentuk di server:</b>", BODY))
story.append(Spacer(1, 2))
story.append(Preformatted(
    "SELECT * FROM products WHERE kategori = 'Gifts' OR 1=1--' AND released = 1\n"
    "                                            ^^^^^^^^^\n"
    "                            kondisi SELALU benar; '--' mematikan sisa query", CODE))
story.append(Spacer(1, 4))

tbl = Table([
    ["Kondisi", "Request", "Produk tampil"],
    ["Baseline (normal)", "kategori=Gifts", "2 produk"],
    ["Setelah SQLi", "kategori=Gifts' OR 1=1--", "9 produk (semua)"],
], colWidths=[38*mm, 70*mm, 32*mm])
tbl.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(tbl)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Response dengan payload memuat <b>3 produk tersembunyi</b> yang tidak pernah "
    "muncul di UI normal, termasuk flag <b>Flag{sql_injection_pemula}</b> — bukti "
    "penembusan data yang seharusnya difilter.", BODY))

# ================= 4. DAMPAK =================
story.append(Paragraph("4. Dampak", H2))
story.append(Paragraph(
    "• <b>Terbukti:</b> kebocoran data tersembunyi (voucher internal, prototipe produk, "
    "flag) kepada siapa pun tanpa akun.<br/>"
    "• <b>Potensi (belum didemonstrasikan):</b> pola yang sama lazim dapat dikembangkan "
    "menjadi pembacaan tabel lain (pengguna, hash kata sandi) atau modifikasi data — "
    "belum diuji pada lab ini.", BODY))

# ================= 5. REKOMENDASI =================
story.append(Paragraph("5. Rekomendasi Perbaikan", H2))
story.append(Paragraph(
    "1. Gunakan <b>parameterized query</b> (prepared statement) — jangan merangkai string:<br/>"
    "<font face='Courier' size='8.5'>cur.execute(\"SELECT * FROM products WHERE kategori = ? AND released = 1\", (kategori,))</font><br/>"
    "2. Validasi input dengan <b>whitelist</b> kategori yang diizinkan.<br/>"
    "3. Terapkan <b>least-privilege</b>: akun DB aplikasi cukup baca.", BODY))

# ================= 6. RENCANA =================
story.append(Paragraph("6. Tindak Lanjut (rencana)", H2))
story.append(Paragraph(
    "• Uji payload UNION untuk membaca tabel lain (di lab, bukan sistem nyata)<br/>"
    "• Buat versi aplikasi yang telah diperbaiki sebagai perbandingan<br/>"
    "• Ulangi pola laporan ini untuk lab PortSwigger/HTB berikutnya", BODY))

story.append(Spacer(1, 10))
foot = ParagraphStyle("F", parent=SUB, fontSize=8)
story.append(Paragraph(
    "Dokumen edukasi internal — lab berjalan di localhost (aplikasi milik sendiri). "
    "Tidak ada sistem pihak ketiga yang diuji. Terinspirasi lab PortSwigger Web "
    "Security Academy: \"SQL injection vulnerability in WHERE clause allowing "
    "retrieval of hidden data\".", foot))

doc.build(story)
print("PDF tersimpan:", OUT)
