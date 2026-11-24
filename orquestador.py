from afd import Q0, QR, F, delta, procesar

PERIODO, RESIDUO, LIMITE = 5, 2, 3


def es_revision(t):
    return t % PERIODO == RESIDUO


def siguiente_revision(t):
    t += 1
    while not es_revision(t):
        t += 1
    return t


class Orquestador:
    def __init__(s):
        s.q, s.n, s.log = Q0, 0, []

    @property
    def L(s):
        return s.n >= LIMITE

    def decidir(s, t, V, C):
        """Devuelve (expresión, símbolo) o None si no hay evento."""
        if s.q in ("q0", "q3"):
            if V and C:
                return "A", "d"
            if V and not C:
                return "N", "s"
            return "X1", "x"
        if s.q == "q2" and es_revision(t):
            return ("P", "r") if V and not s.L else ("X2", "x")
        if s.q == "q1" and not V:
            return "X1", "x"
        return None

    def emitir(s, t, expr, a):
        ant = s.q
        s.q = delta(ant, a)
        if a == "r":
            s.n += 1
        s.log.append((t, ant, expr, a, s.q, s.n))

    @property
    def cadena(s):
        return "".join(e[3] for e in s.log)


def simular(t0, C, V=True):
    """C: bool o función t -> bool. La solicitud llega en t0."""
    cap = C if callable(C) else (lambda t: C)
    o, t = Orquestador(), t0
    while o.q != QR and o.q not in F:
        if o.q == "q1" and V:
            o.emitir(t, "fin", "f")
            continue
        if o.q == "q2":
            t = siguiente_revision(t)
        o.emitir(t, *o.decidir(t, V, cap(t)))
    return o


def mostrar(o):
    for t, ant, expr, a, nue, n in o.log:
        print(f"t={t:>2}  {ant} --{expr}:{a}--> {nue}   n={n}")
    r = procesar(o.cadena)
    print("cadena:", o.cadena, "| final:", r["final"], "|", r["clasificacion"])


if __name__ == "__main__":
    print("t=12:", es_revision(12), "| t=13:", es_revision(13))
    print("\n-- ciclo de reintento --")
    mostrar(simular(8, lambda t: t >= 17))
    print("\n-- reintentos agotados (C=0 siempre) --")
    mostrar(simular(8, False))
    print("\n-- revisión forzada en q2 con n=3 --")
    o = Orquestador()
    o.q, o.n = "q2", 3
    print(o.decidir(12, True, False))