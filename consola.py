from afd import procesar, SIGMA
from orquestador import simular, mostrar


def ver(c):
    r = procesar(c)
    print(f"\ncadena: {c!r}")
    if not r["valida"]:
        S = ", ".join(SIGMA)
        for i, ch in r["invalidos"]:
            print(f"  entrada inválida: {ch!r} en posición {i} (no pertenece a Σ = {{{S}}})")
        return
    print("  inicial:  ", r["inicial"])
    print("  recorrido:", " → ".join(r["recorrido"]))
    print("  final:    ", r["final"])
    print("  decisión: ", "ACEPTADA" if r["aceptada"] else "NO ACEPTADA", f"({r['clasificacion']})")


def escenario(t0, C):
    o = simular(t0, C)
    print()
    mostrar(o)
    ver(o.cadena)


def libre():
    ver(input("Cadena de eventos (ε = vacía): "))


def personalizado():
    t0 = pedir_entero("Instante de llegada t: ")
    while True:
        tc = input("Hay capacidad desde t = (vacío = nunca): ").strip()
        if tc == "" or tc.lstrip("-").isdigit():
            break
        print("  Debe ser un número entero o dejarse vacío.")
    escenario(t0, (lambda t: t >= int(tc)) if tc else False)

def pedir_entero(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Debe ser un número entero (por ejemplo 8).")

MENU = {
    "1": ("Ciclo de reintento (srsrdf)", lambda: escenario(8, lambda t: t >= 17)),
    "2": ("Rechazo absorbente (srsrsrsx, L=1)", lambda: escenario(8, False)),
    "3": ("Símbolo ajeno a Σ (sdy)", lambda: ver("sdy")),
    "4": ("Cadena libre", libre),
    "5": ("Escenario del orquestador", personalizado),
}

if __name__ == "__main__":
    while True:
        print("\n=== Simulador AFD: atención de solicitudes web ===")
        for k, (n, _) in MENU.items():
            print(f" {k}. {n}")
        print(" 0. Salir")
        op = input("> ").strip()
        if op == "0":
            break
        if op in MENU:
            MENU[op][1]()