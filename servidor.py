import io
import os
from contextlib import redirect_stdout
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from json import dumps
from urllib.parse import urlparse, parse_qs
import afd
import pruebas
from orquestador import simular

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
CAMPOS = ("t", "de", "expr", "simbolo", "a", "n")


def api(ruta, q):
    if ruta == "/api/modelo":
        return {"Q": afd.Q, "SIGMA": afd.SIGMA, "q0": afd.Q0, "F": sorted(afd.F),
                "qr": afd.QR, "tabla": afd.TABLA}
    if ruta == "/api/procesar":
        return afd.procesar(q.get("cadena", [""])[0])
    if ruta == "/api/simular":
        t0 = int(q.get("t", ["0"])[0])
        d = q.get("desde", [""])[0]
        V = q.get("v", ["1"])[0] == "1"
        o = simular(t0, (lambda t: t >= int(d)) if d else False, V)
        return {"log": [dict(zip(CAMPOS, e)) for e in o.log], "cadena": o.cadena,
                "resultado": afd.procesar(o.cadena)}
    if ruta == "/api/pruebas":
        b = io.StringIO()
        with redirect_stdout(b):
            ok = pruebas.main()
        return {"salida": b.getvalue(), "ok": ok,
                "coinciden": sum(pruebas.res), "total": len(pruebas.res)}


class H(SimpleHTTPRequestHandler):
    def __init__(s, *a, **k):
        super().__init__(*a, directory=WEB, **k)

    def do_GET(s):
        u = urlparse(s.path)
        if not u.path.startswith("/api/"):
            return super().do_GET()
        try:
            r = api(u.path, parse_qs(u.query))
            code = 200 if r is not None else 404
            r = r if r is not None else {"error": "ruta inexistente"}
        except Exception as e:
            code, r = 400, {"error": str(e)}
        b = dumps(r, ensure_ascii=False).encode()
        s.send_response(code)
        s.send_header("Content-Type", "application/json; charset=utf-8")
        s.send_header("Content-Length", str(len(b)))
        s.end_headers()
        s.wfile.write(b)


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", 8000), H)
    print("Servidor en http://localhost:8000 (Ctrl+C para detener)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.server_close()