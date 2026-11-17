"""Small waitlist service. Public checkout remains closed until separately implemented."""
import hashlib
import json
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
STATE = Path(os.environ.get('STATE_DIRECTORY', ROOT / 'output'))
ORIGIN = os.environ.get('PUBLIC_ORIGIN', 'http://127.0.0.1:8864')
CONFIG = Path(os.environ.get('RANDOM_CONFIG', ROOT / 'config.json'))
FILES = {'/': ('index.html', 'text/html; charset=utf-8'),
         '/style.css': ('style.css', 'text/css; charset=utf-8'),
         '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
         '/concept.jpg': ('concept.jpg', 'image/jpeg'),
         '/blueprint.png': ('blueprint.png', 'image/png'),
         '/countdown.mjs': ('countdown.mjs', 'text/javascript; charset=utf-8'),
         '/legal': ('legal.html', 'text/html; charset=utf-8'),
         '/legal.html': ('legal.html', 'text/html; charset=utf-8'),
         '/favicon.svg': ('favicon.svg', 'image/svg+xml')}


def config():
    settings = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
    address = settings.get('address', '')
    return {'address': address, 'waitlist': bool(address.strip()) and settings.get('waitlist') is True}


def connect():
    db = sqlite3.connect(STATE / 'waitlist.sqlite', timeout=5)
    db.execute('PRAGMA busy_timeout=5000')
    return db


def initialize():
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS waitlist (email TEXT PRIMARY KEY, created TEXT NOT NULL, consent TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS limits (key TEXT PRIMARY KEY, day TEXT NOT NULL, count INTEGER NOT NULL)')
    os.chmod(STATE / 'waitlist.sqlite', 0o600)


def prune():
    now = datetime.now(timezone.utc)
    with connect() as db:
        db.execute('DELETE FROM limits WHERE day < ?', ((now.date() - timedelta(days=1)).isoformat(),))
        db.execute('DELETE FROM waitlist WHERE created < ?', ((now - timedelta(days=365)).isoformat(),))


class Server(ThreadingHTTPServer):
    last_prune = 0

    def service_actions(self):
        if time.monotonic() - self.last_prune > 3600:
            try:
                prune()
                self.last_prune = time.monotonic()
            except sqlite3.Error:
                pass  # Retry next poll; a temporary database error must not stop HTTP.


class Handler(BaseHTTPRequestHandler):
    server_version = 'random'

    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, *args):
        # Personal data and user-controlled request paths never enter access logs.
        pass

    def reply(self, code, data, content_type='application/json; charset=utf-8'):
        if not isinstance(data, bytes):
            data = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store' if self.path.startswith('/api/') else 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/healthz':
            return self.reply(200, {'ok': True})
        if path == '/api/config':
            try:
                return self.reply(200, config())
            except (ValueError, OSError, AttributeError):
                return self.reply(503, {'error': 'Warteliste gerade nicht verfügbar.'})
        if path not in FILES:
            return self.reply(404, {'error': 'Nicht gefunden.'})
        filename, mime = FILES[path]
        try:
            self.reply(200, (PUBLIC / filename).read_bytes(), mime)
        except OSError:
            self.reply(503, {'error': 'Datei gerade nicht verfügbar.'})

    def do_POST(self):
        if self.path != '/api/waitlist':
            return self.reply(404, {'error': 'Nicht gefunden.'})
        if self.headers.get('Origin') != ORIGIN:
            return self.reply(403, {'error': 'Anfrage nicht erlaubt.'})
        if self.headers.get_content_type() != 'application/json':
            return self.reply(415, {'error': 'JSON erforderlich.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 2048 or self.headers.get('Transfer-Encoding'):
                return self.reply(413, {'error': 'Ungültige Anfragegröße.'})
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError()
            email = data.get('email')
            if not isinstance(email, str):
                raise ValueError()
            email = email.strip().lower()
            if len(email) > 254 or not re.fullmatch(r"[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,63}", email):
                raise ValueError()
            if data.get('consent') is not True or data.get('website'):
                raise ValueError()
        except (ValueError, UnicodeError, TimeoutError):
            return self.reply(400, {'error': 'Bitte gültige E-Mail und Einwilligung angeben.'})
        try:
            if not config()['waitlist']:
                return self.reply(503, {'error': 'Die Warteliste ist noch nicht geöffnet.'})
            now = datetime.now(timezone.utc)
            day = now.date().isoformat()
            # Only a dedicated loopback reverse proxy may supply the real client IP.
            ip = self.headers.get('X-Real-IP', self.client_address[0])
            key = hashlib.sha256((day + ip).encode()).hexdigest()
            with connect() as db:
                db.execute('BEGIN IMMEDIATE')
                count = db.execute('SELECT count FROM limits WHERE key=?', (key,)).fetchone()
                if count and count[0] >= 5:
                    return self.reply(429, {'error': 'Zu viele Anfragen. Bitte morgen erneut versuchen.'})
                db.execute('INSERT INTO limits VALUES (?, ?, 1) ON CONFLICT(key) DO UPDATE SET count=count+1', (key, day))
                db.execute('INSERT OR IGNORE INTO waitlist VALUES (?, ?, ?)', (email, now.isoformat(), 'launch-once-2026-11-15'))
            # Same response for existing addresses prevents membership lookup.
            return self.reply(200, {'ok': True})
        except (sqlite3.Error, OSError, ValueError, AttributeError):
            return self.reply(503, {'error': 'Speichern gerade nicht möglich. Bitte später erneut versuchen.'})


if __name__ == '__main__':
    os.umask(0o077)
    initialize()
    Server(('127.0.0.1', int(os.environ.get('PORT', '8864'))), Handler).serve_forever()
