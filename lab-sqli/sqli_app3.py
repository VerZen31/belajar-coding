# -*- coding: utf-8 -*-
"""
Lab 3 (HARD): Blind SQL injection - conditional response.
Endpoint /track?TrackingId=...
- Query: SELECT tracking_id FROM tracking WHERE tracking_id = '<input>'
- Row ketemu  -> banner "Selamat datang kembali!"
- Tidak/Error -> banner TIDAK muncul (error TIDAK pernah ditampilkan,
  data hasil query juga tidak pernah dirender - hanya perilaku halaman)
Misi: ekstrak password administrator karakter demi karakter.
"""
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

DB = sqlite3.connect(":memory:", check_same_thread=False)
DB.executescript("""
DROP TABLE IF EXISTS tracking;
DROP TABLE IF EXISTS users;
CREATE TABLE tracking (tracking_id TEXT PRIMARY KEY);
CREATE TABLE users (username TEXT, password TEXT);
INSERT INTO tracking VALUES ('abc123');
INSERT INTO tracking VALUES ('xyz789');
INSERT INTO users VALUES ('administrator','Flag{blind_is_fun}');
INSERT INTO users VALUES ('carlos','Montoya123');
INSERT INTO users VALUES ('wiener','PeterW1ener');
""")


class Handler(BaseHTTPRequestHandler):
    def _page(self, welcome):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        banner = "<p><b>Selamat datang kembali!</b></p>" if welcome else ""
        html = ("<!doctype html><html><head><title>Toko Latihan 3</title>"
                "<style>body{font-family:Segoe UI;background:#f5f5f5;margin:2rem}"
                "b{color:#111}</style></head><body>"
                "<h1>Toko Latihan 3 &mdash; Pelacakan Pesanan</h1>"
                + banner +
                "<p>Masukkan TrackingId-mu untuk melacak pesanan.</p>"
                "<p><a href=\"/\">beranda</a></p></body></html>")
        self.wfile.write(html.encode())

    def do_GET(self):
        u = urlparse(self.path)
        if u.path != "/track":
            return self._page(False)
        q = parse_qs(u.query)
        tid = unquote(q.get("TrackingId", [""])[0])
        sql = "SELECT tracking_id FROM tracking WHERE tracking_id = '" + tid + "'"
        print("[QUERY]", sql, flush=True)
        try:
            row = DB.execute(sql).fetchone()
        except Exception as e:
            # PENTING: error hanya dicatat di server, TIDAK PERNAH tampil ke user
            print("[ERROR-diam-diam]", str(e), flush=True)
            row = None
        self._page(row is not None)

    def log_message(self, *a):
        pass


print("Lab 3 (BLIND) jalan di http://127.0.0.1:8012/track?TrackingId=abc123  (Ctrl+C untuk stop)", flush=True)
HTTPServer(("127.0.0.1", 8012), Handler).serve_forever()
