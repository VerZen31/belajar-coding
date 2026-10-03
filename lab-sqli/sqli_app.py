# ============================================================
# LAB LOKAL: SQL Injection — tiruan lab PortSwigger
# "SQL injection vulnerability in WHERE clause allowing
#  retrieval of hidden data"
#
# Tujuan edukasi: berjalan HANYA di localhost (127.0.0.1).
# Ini aplikasi buatan sendiri — menguji aplikasi sendiri itu legal.
#
# Jalankan:  python sqli_app.py
# Buka:      http://127.0.0.1:8010/
# ============================================================
import sqlite3
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = "toko.db"


def init_db():
    """Buat database toko + isi produk (ada yang dirahasiakan!)."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("""
        CREATE TABLE products (
            id       INTEGER PRIMARY KEY,
            nama     TEXT,
            kategori TEXT,
            harga    INTEGER,
            released INTEGER          -- 1 = boleh tampil, 0 = TERSEMBUNYI
        )
    """)
    data = [
        # --- produk yang BOLEH tampil (released = 1) ---
        (1,  "Kucing Goyang Hoki",      "Gifts",     25000, 1),
        (2,  "Mug Kopi Ojol",           "Gifts",     45000, 1),
        (3,  "Kaos Python",             "Apparel",   99000, 1),
        (4,  "Topi Networking",         "Apparel",   55000, 1),
        (5,  "Sticker Pack Hacker",     "Accessories", 15000, 1),
        (6,  "Gantungan Kunci USB",     "Accessories", 35000, 1),
        # --- produk TERSEMBUNYI (belum rilis / rahasia) ---
        (7,  "Voucher Tak Terbatas (RAHASIA)",  "Gifts",       0,      0),
        (8,  "Prototipe Hoodie Dev",            "Apparel",     199000, 0),
        (9,  "Flag{sql_injection_pemula}",      "Accessories", 0,      0),
    ]
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", data)
    con.commit()
    con.close()


def query_products(kategori_input: str):
    """⚠️ RENTAN! Input user digabung langsung ke query (string concat).
    INI PERSIS celah yang ada di lab PortSwigger."""
    sql = ("SELECT * FROM products "
           f"WHERE kategori = '{kategori_input}' AND released = 1")
    print(f"[QUERY] {sql}")                      # jejak di terminal server
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(sql).fetchall()
    con.close()
    return rows, sql


def render(rows):
    """Bungkus hasil query jadi halaman HTML sederhana."""
    item = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td>"
        f"<td>Rp {r[3]:,}</td></tr>"
        for r in rows
    ) or "<tr><td colspan=4><i>Tidak ada produk</i></td></tr>"
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Toko Latihan</title>
<style>
 body {{ font-family: 'Segoe UI', Arial; background:#0f172a; color:#e2e8f0;
        padding: 30px; }}
 table {{ border-collapse: collapse; background:#1e293b; width: 100%; }}
 th, td {{ border: 1px solid #334155; padding: 10px 14px; text-align: left; }}
 th {{ background:#334155; }}
 h1 {{ color:#38bdf8; }}
 .note {{ color:#94a3b8; font-size: 13px; }}
</style></head>
<body>
<h1>🛒 Toko Latihan — Filter Kategori</h1>
<p class="note">Coba link:
 <a style="color:#38bdf8" href="/filter?kategori=Gifts">Gifts</a> ·
 <a style="color:#38bdf8" href="/filter?kategori=Apparel">Apparel</a></p>
<table>
<tr><th>ID</th><th>Nama</th><th>Kategori</th><th>Harga</th></tr>
{item}
</table>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/":
            self._html(render(query_products("Gifts")[0]))

        elif parsed.path == "/filter":
            qs = urllib.parse.parse_qs(parsed.query)
            kategori = qs.get("kategori", [""])[0]
            rows, sql = query_products(kategori)
            self._html(render(rows))

        else:
            self._html("<h1>404</h1>", status=404)

    def _html(self, body, status=200):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):        # sunyikan log default
        pass


if __name__ == "__main__":
    init_db()
    print("Lab toko jalan di http://127.0.0.1:8010/  (Ctrl+C untuk stop)")
    HTTPServer(("127.0.0.1", 8010), Handler).serve_forever()
