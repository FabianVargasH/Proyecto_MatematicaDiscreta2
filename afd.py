Q = ("q0", "q1", "q2", "q3", "q4", "qr")
SIGMA = ("d", "s", "r", "f", "x")
Q0 = "q0"
F = frozenset({"q4"})
QR = "qr"

# Tabla 5: columnas en el orden de SIGMA (d, s, r, f, x)
TABLA = {
    "q0": "q1 q2 qr qr qr",
    "q1": "qr qr qr q4 qr",
    "q2": "qr q2 q3 qr qr",
    "q3": "q1 q2 qr qr qr",
    "q4": "qr qr qr qr qr",
    "qr": "qr qr qr qr qr",
}
DELTA = {(q, a): t for q, fila in TABLA.items()
         for a, t in zip(SIGMA, fila.split())}


def delta(q, a):
    return DELTA[(q, a)]


def clasificar(q):
    if q in F:
        return "aceptada"
    if q == QR:
        return "rechazo definitivo"
    return "no concluida"


def procesar(cadena):
    cadena = cadena.strip().replace("ε", "")
    invalidos = [(i, c) for i, c in enumerate(cadena) if c not in SIGMA]
    if invalidos:
        return {"cadena": cadena, "valida": False, "invalidos": invalidos,
                "inicial": Q0, "recorrido": None, "final": None,
                "aceptada": False, "clasificacion": "entrada inválida"}
    rec = [Q0]
    for a in cadena:
        rec.append(delta(rec[-1], a))
    return {"cadena": cadena, "valida": True, "invalidos": [],
            "inicial": Q0, "recorrido": rec, "final": rec[-1],
            "aceptada": rec[-1] in F, "clasificacion": clasificar(rec[-1])}


def verificar():
    assert len(DELTA) == len(Q) * len(SIGMA) == 30
    assert all(t in Q for t in DELTA.values())
    vistos, pend = {Q0}, [Q0]
    while pend:
        q = pend.pop()
        for a in SIGMA:
            t = delta(q, a)
            if t not in vistos:
                vistos.add(t)
                pend.append(t)
    assert vistos == set(Q), "hay estados inalcanzables"
    assert all(delta(QR, a) == QR for a in SIGMA)
    assert sum(t != QR for t in DELTA.values()) == 7
    return True


if __name__ == "__main__":
    print("verificar():", verificar())
    for c in ["srdf", "dx", "sr", "", "sdy"]:
        r = procesar(c)
        print(repr(c), "->", " → ".join(r["recorrido"] or []) or r["invalidos"],
              "|", r["clasificacion"])