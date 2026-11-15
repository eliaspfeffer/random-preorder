import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


class WaitlistTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        server.STATE = Path(self.directory.name)
        server.CONFIG = server.STATE / 'config.json'
        server.initialize()
        self.http = server.Server(('127.0.0.1', 0), server.Handler)
        self.url = f'http://127.0.0.1:{self.http.server_port}'
        server.ORIGIN = self.url
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        self.directory.cleanup()

    def enable(self):
        server.CONFIG.write_text(json.dumps({'address': 'Testanbieter\nTeststraße 1\n12345 Testort', 'waitlist': True}))

    def request(self, path, data=None, origin=None):
        headers = {'Origin': origin or self.url, 'Content-Type': 'application/json'}
        req = Request(self.url + path, data=json.dumps(data).encode() if data is not None else None, headers=headers)
        try:
            response = urlopen(req)
        except HTTPError as error:
            response = error
        return response.status, response.read(), response.headers

    def post(self, email='qa@example.invalid', **extra):
        return self.request('/api/waitlist', {'email': email, 'consent': True, **extra})

    def test_closed_until_legal_identity_is_configured(self):
        self.assertEqual(self.post()[0], 503)
        server.CONFIG.write_text('{"waitlist":true,"address":""}')
        self.assertEqual(self.post()[0], 503)
        server.CONFIG.write_text('{broken')
        self.assertEqual(self.post()[0], 503)

    def test_unique_normalized_email_and_private_storage(self):
        self.enable()
        self.assertEqual(self.post('QA@example.invalid')[0], 200)
        self.assertEqual(self.post('qa@example.invalid')[0], 200)
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT email FROM waitlist').fetchall(), [('qa@example.invalid',)])
        self.assertEqual((server.STATE / 'waitlist.sqlite').stat().st_mode & 0o777, 0o600)

    def test_validation_and_cross_site_denial(self):
        self.enable()
        for payload in [[], {'email': 12, 'consent': True}, {'email': 'wrong', 'consent': True}, {'email': 'qa@example.invalid', 'consent': 'true'}, {'email': 'qa@example.invalid', 'consent': True, 'website': 'bot'}]:
            self.assertEqual(self.request('/api/waitlist', payload)[0], 400)
        self.assertEqual(self.request('/api/waitlist', {'email':'qa@example.invalid','consent':True}, origin='https://evil.invalid')[0], 403)

    def test_rate_limit_and_no_public_data_or_checkout(self):
        self.enable()
        for _ in range(5):
            self.assertEqual(self.post()[0], 200)
        self.assertEqual(self.post()[0], 429)
        for path in ['/waitlist.sqlite', '/config.json', '/server.py', '/../server.py', '/api/orders', '/api/waitlist']:
            self.assertEqual(self.request(path)[0], 404)
        status, _, headers = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])

    def test_retention(self):
        with server.connect() as db:
            db.execute('INSERT INTO waitlist VALUES (?, ?, ?)', ('old@example.invalid', '2020-01-01', 'old'))
            db.execute('INSERT INTO limits VALUES (?, ?, ?)', ('old', '2020-01-01', 1))
        server.prune()
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM waitlist').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT count(*) FROM limits').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
