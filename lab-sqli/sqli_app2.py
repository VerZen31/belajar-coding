# -*- coding: utf-8 -*-
# ============================================================
# LAB 2 (MEDIUM): SQL Injection — UNION Attack
# Tiruan konsep lab PortSwigger: "SQL injection UNION attack,
# extracting multiple values in a single column" (level menengah)
#
# CARA JALAN:
#   python sqli_app2.py        -> http://127.0.0.1:8011
#
# TUJUAN PESERTA:
#   Temukan password 'administrator' dari tabel users (tersembunyi)
#   memakai serangan UNION. Tidak boleh nebak-nebak!
#
# CATATAN KEAMANAN: lab edukasi, jalan di localhost, milik sendiri.
# ============================================================
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB = sqlite3.connect(":memory:", check_same_thread=False)
DB.executescript("""
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT,
  harga INTEGER, released INTEGER);
INSERT INTO products VALUES
 (1,'Kucing Goyang Hoki','Gifts',25000,1),
 (2,'Mug Kopi Ojol','Gifts',45000,1),
 (3,'Kaos Python','Apparel',99000,1),
 (4,'Topi Networking','Apparel',55000,1),
 (5,'Sticker Pack Hacker','Accessories',15000,1),
 (6,'Gantungan Kunci USB','Accessories',35000,1),
 (7,'Voucher Tak Terbatas (RAHASIA)','Gifts',0,0);
DROP TABLE IF EXISTS users;
CREATE TABLE users (username TEXT, password TEXT);
INSERT INTO users VALUES
 ('administrator','Flag{union_attack_medium}'),
 ('wiener','PeterW1ener'),
 ('carlos','Montoya123');
""")
DB.commit()

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>Toko Latihan 2</title>
<style>body{{font-family:Arial;margin:30px}} table{{border-collapse:collapse}}
td,th{{border:1px solid #999;padding:6px 14px}} th{{background:#1e3a8a;color:#fff}}
.err{{color:#b91c1c;font-weight:bold}}</style></head><body>{body}</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _render(self, body, status=200):
        data = PAGE.format(body=body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            self._render("""
<h1>&#128722; Toko Latihan 2 &mdash; UNION Attack (MEDIUM)</h1>
<p><b>Misi kamu:</b> halaman ini punya tabel <code>users</code> tersembunyi
(username + password). Dapatkan password <b>administrator</b> lewat celah
SQL injection di parameter <code>kategori</code>.</p>
<p>Perhatikan: judul &quot;Kategori: ...&quot; di halaman filter berasal dari
<b>kolom pertama query</b> &mdash; itu petunjuk penting.</p>
<p>Coba mulai dari: <a href="/filter?kategori=Gifts">/filter?kategori=Gifts</a></p>
<p><i>Petunjuk metodologi: ORDER BY dulu, baru UNION SELECT.</i></p>""")
            return

        if u.path == "/filter":
            qs = parse_qs(u.query)
            kategori = qs.get("kategori", [""])[0]
            # !!! CELAH: input user digabung langsung ke SQL (tanpa parameterisasi)
            sql = ("SELECT nama, harga FROM products "
                   f"WHERE kategori = '{kategori}' AND released = 1")
            print(f"[QUERY] {sql}")
            try:
                rows = DB.execute(sql).fetchall()
            except Exception as e:
                print(f"[ERROR] {e}")
                self._render(f"<h1>Oops</h1><p class='err'>Query gagal. "
                             f"(detail ada di log server)</p>", status=500)
                return
            head = rows[0][0] if rows else "(kosong)"

            def fmt(v):
                try:
                    return f"Rp {int(v):,}".replace(",", ".")
                except (ValueError, TypeError):
                    return str(v)

            trs = "".join(
                f"<tr><td>{r[0]}</td><td>{fmt(r[1])}</td></tr>" for r in rows)
            self._render(f"""
<h1>&#128722; Toko Latihan 2 &mdash; Filter Kategori</h1>
<p><b>Kategori: {head}</b></p>
<table><tr><th>Nama</th><th>Harga</th></tr>{trs}</table>
<p><a href="/">&#8592; beranda</a></p>""")
            return

        self._render("<h1>404</h1>", status=404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Lab 2 (UNION) jalan di http://127.0.0.1:8011  (Ctrl+C untuk stop)")
    HTTPServer(("127.0.0.1", 8011), Handler).serve_forever()
