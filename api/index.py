# Vercel Python entrypoint: expose the Flask application defined in main.py.
from urllib.parse import parse_qs

from main import app

_original_wsgi_app = app.wsgi_app

def _restore_vercel_path(environ, start_response):
    # vercel.json forwards the requested path in the __path query parameter.
    forwarded_path = parse_qs(environ.get("QUERY_STRING", "")).get("__path", [None])[0]
    if forwarded_path is not None:
        environ["PATH_INFO"] = "/" + forwarded_path.lstrip("/")
    return _original_wsgi_app(environ, start_response)

app.wsgi_app = _restore_vercel_path
