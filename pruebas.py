import re
import sys
import random
from itertools import product
from afd import Q, SIGMA, Q0, QR, F, DELTA, delta, verificar
from orquestador import Orquestador, simular, es_revision

res = []
LM = re.compile(r"(d|s(s|rs)*rd)f")


def chk(nombre, cond):
    res.append(bool(cond))
    print("OK   " if cond else "FALLA", nombre)


def final(w):
    q = Q0
    for a in w:
        q = delta(q, a)
    return q


def vfy():
    try:
        return verificar()
    except AssertionError:
        return False


def conjunto_a():
    print("\n-- Conjunto A: δ para cualquier cadena --")
    chk("δ total: 30 pares con destino en Q", len(DELTA) == 30 and all(t in Q for t in DELTA.values()))
    chk("dominio de δ = Q × Σ (un destino por par)", set(DELTA) == set(product(Q, SIGMA)))
    chk("6 estados alcanzables, qr absorbente, 7 transiciones fuera de qr", vfy())
    n = sum(5 ** k for k in range(9))
    mal = [w for k in range(9) for t in product(SIGMA, repeat=k)
           for w in ["".join(t)] if (final(w) in F) != bool(LM.fullmatch(w))]
    chk(f"δ* = L(M) en las {n} cadenas de largo ≤ 8", not mal)


def conjunto_b():
    print("\n-- Conjunto B: el orquestador nunca emite un cuarto reintento --")
    o = simular(8, False)
    chk("t=8, C=0 siempre: emite srsrsrsx y termina en qr", o.cadena == "srsrsrsx" and o.q == QR)
    chk("en t=27 se emite x porque L=1", o.log[-1] == (27, "q2", "X2", "x", "qr", 3))
    o = Orquestador()
    o.q, o.n = "q2", 3
    chk("revisión forzada en q2 con n=3: x y no r", o.decidir(12, True, False) == ("X2", "x"))
    o = simular(8, True, V=False)
    chk("V=0 al llegar: x y rechazo", o.cadena == "x" and o.q == QR)
    rnd = random.Random(0)
    ok = True
    for _ in range(20000):
        tab = [rnd.random() < 0.3 for _ in range(200)]
        o = simular(rnd.randrange(30), lambda t: tab[t])
        ok &= o.cadena.count("r") <= 3 and final(o.cadena) == o.q and o.q in F | {QR}
    chk("20000 escenarios aleatorios: nunca más de 3 r (srsrsrsrdf no se produce)", ok)


def conjunto_c():
    print("\n-- Conjunto C: condición booleana y congruencia --")
    exp = {(1, 1): "d", (1, 0): "s", (0, 1): "x", (0, 0): "x"}
    ok = True
    for q in ("q0", "q3"):
        for (V, C), e in exp.items():
            o = Orquestador()
            o.q = q
            ok &= o.decidir(0, bool(V), bool(C))[1] == e
    chk("q0 y q3: (V,C) → d, s, x según la Tabla 7", ok)
    ok = True
    for n, V, e in [(0, 1, "r"), (2, 1, "r"), (3, 1, "x"), (0, 0, "x"), (3, 0, "x")]:
        o = Orquestador()
        o.q, o.n = "q2", n
        ok &= o.decidir(12, bool(V), False)[1] == e
    chk("q2 en t=12: r si V∧¬L, x en los demás casos", ok)
    o = Orquestador()
    o.q = "q2"
    chk("q2 en t=13: sin evento", o.decidir(13, True, False) is None)
    chk("12 ≡ 2 (mod 5) sí; 13 no", es_revision(12) and not es_revision(13))


def main():
    res.clear()
    conjunto_a()
    conjunto_b()
    conjunto_c()
    print(f"\n{sum(res)} de {len(res)} pruebas coincidieron")
    return all(res)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)