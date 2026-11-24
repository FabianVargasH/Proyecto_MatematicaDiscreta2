# Simulador del AFD: atención de solicitudes web

Proyecto final de Matemática Discreta II (Grupo D). Este programa es una simulación del autómata finito determinista (AFD) del subsistema de atención de solicitudes web, con la misma definición matemática del informe: Q, Σ, δ, q₀ y F.

Tiene tres formas de usarse, todas con el mismo núcleo:

- **Interfaz web** (la más fácil): se abre en el navegador, con el diagrama de estados.
- **Consola**: un menú de texto.
- **Pruebas automáticas**: comprueban que el programa coincide con el modelo matemático.

No necesita internet, cuentas, ni instalar paquetes adicionales. Solo necesita **Python**.

---

## 1. Lo que necesita

- Un computador con **Python 3.8 o más reciente**.
- Un navegador web (Chrome, Edge, Firefox o Safari).

### ¿Ya tengo Python?

1. Abra la terminal (se explica en el paso 3).
2. Escriba `python --version` y pulse Enter.
3. Si aparece algo como `Python 3.12.1`, ya lo tiene y puede ir al paso 2.
4. Si aparece un error, instálelo:
   - Entre a https://www.python.org/downloads/ y descargue la versión más reciente.
   - **En Windows, al abrir el instalador, marque la casilla "Add python.exe to PATH"** (aparece abajo, en la primera pantalla) y luego pulse "Install Now". Este paso es el que más se olvida.
   - Cierre y vuelva a abrir la terminal antes de continuar.

---

## 2. Preparar la carpeta

1. En el caso de que lo descargue como un **.zip**, haga clic derecho sobre él y elija **"Extraer todo..."** (en Windows) o haga doble clic (en Mac). **No ejecute el programa desde dentro del .zip.**
2. Abra la carpeta extraída. Debe contener estos archivos:

```
afd.py              núcleo del autómata (Q, Σ, δ, q₀, F)
orquestador.py      decisiones booleanas y revisión periódica t ≡ 2 (mod 5)
consola.py          menú por consola
pruebas.py          pruebas automáticas (conjuntos A, B y C)
servidor.py         conecta la interfaz web con el programa
web/index.html      la interfaz web
README.md           este archivo
```

El archivo `index.html` debe estar dentro de la carpeta `web`. Si no es así, la interfaz no abrirá.

---

## 3. Abrir la terminal dentro de la carpeta

**Windows:**
1. Abra la carpeta del proyecto en el Explorador de archivos.
2. Haga clic en la barra de direcciones (donde se ve la ruta de la carpeta), escriba `cmd` y pulse Enter.
3. Se abre una ventana negra. Esa es la terminal, ya ubicada en la carpeta correcta.

**Mac:**
1. Abra la aplicación **Terminal**.
2. Escriba `cd ` (con un espacio al final), arrastre la carpeta del proyecto hasta la ventana y pulse Enter.

**Linux:** clic derecho dentro de la carpeta y "Abrir en terminal".

> En Mac y Linux, escriba `python3` en lugar de `python` en todos los comandos de abajo.

---

## 4. Iniciar la interfaz web (recomendado)

1. En la terminal del sistema operativo o en la terminal de VsCode escriba:

```
python servidor.py
```

2. Debe aparecer este mensaje:

```
Servidor en http://localhost:8000 (Ctrl+C para detener)
```

3. **Deje esa ventana abierta**. Si la cierra, la interfaz deja de funcionar.
4. Abra su navegador y escriba en la barra de direcciones:

```
http://localhost:8000
```

5. Debe ver la interfaz con el diagrama de estados.
6. Cuando termine, vuelva a la ventana negra y pulse **Ctrl + C** para detener el programa.

---

## 5. Cómo usar la interfaz

Hay dos formas de probar, que se eligen con las pestañas de la sección 1:

**Pestaña A, escribir los eventos uno mismo.** Se escribe una cadena de eventos, por ejemplo `srsrdf`, y se pulsa **Ejecutar cadena**. Los eventos son:

| Letra | Significado |
|---|---|
| d | hay capacidad, se asigna el servicio |
| s | saturación, no hay capacidad |
| r | reintento autorizado |
| f | fin de la atención |
| x | rechazo o cancelación |

**Pestaña B, dejar que el orquestador decida.** El orquestador es el componente que traduce las condiciones booleanas (V, C, L) a eventos. Hay que indicar:

- El instante en que llega la solicitud (t).
- Desde qué instante hay capacidad (vacío significa que nunca hay).
- Si la solicitud es válida.

Luego se pulsa **Simular**.

En ambos casos, el diagrama muestra el camino recorrido en naranja, y debajo aparece una explicación de cada paso. Los botones **Paso siguiente / Paso anterior** permiten recorrerlo paso a paso. La sección 3 muestra la tabla δ con las celdas usadas, y la sección 4 ejecuta las pruebas automáticas.

### Tres ejemplos para empezar

| Qué probar | Cómo | Resultado |
|---|---|---|
| Aceptación con reintentos | Pestaña A, cadena `srsrdf` | Termina en q4, **ACEPTADA** |
| Rechazo absorbente | Pestaña B, llega en 8, capacidad vacía | Cadena `srsrsrsx`, termina en qr, **NO ACEPTADA** |
| Símbolo ajeno al alfabeto | Pestaña A, cadena `sdy` | Aviso de **entrada inválida** en la posición 2 |

---

## 6. Alternativa: usar el menú por consola

```
python consola.py
```

Aparece un menú numerado. Escriba el número de la opción y pulse Enter:

| Opción | Qué hace |
|---|---|
| 1 | Ciclo de reintento (`srsrdf`) |
| 2 | Rechazo absorbente (`srsrsrsx`, límite alcanzado) |
| 3 | Símbolo ajeno a Σ (`sdy`) |
| 4 | Cadena libre (usted escribe los eventos) |
| 5 | Escenario del orquestador (usted indica t y la capacidad) |
| 0 | Salir |

---

## 7. Ejecutar las pruebas automáticas

```
python pruebas.py
```

Tarda unos segundos. Si todo está bien, todas las líneas empiezan con `OK` y la última dice:

```
13 de 13 pruebas coincidieron
```

Las pruebas comprueban tres cosas:

- **Conjunto A:** δ está definida en los 30 pares de Q × Σ, no hay estados inalcanzables, qr es absorbente, y δ* coincide con el lenguaje L(M) en las 488 281 cadenas de largo hasta 8.
- **Conjunto B:** el orquestador nunca emite un cuarto reintento (la cadena `srsrsrsrdf` nunca se produce).
- **Conjunto C:** la traducción de las condiciones booleanas a eventos y la congruencia t ≡ 2 (mod 5).

---

## 8. Si algo no funciona

| Qué ve | Qué hacer |
|---|---|
| `'python' no se reconoce como un comando` | Python no está instalado, o no se marcó "Add python.exe to PATH". Reinstálelo marcando esa casilla. En Windows también puede probar con `py servidor.py`. |
| `command not found: python` (Mac/Linux) | Use `python3` en lugar de `python`. |
| El navegador dice "no se puede conectar" | El servidor no está corriendo. Revise que la ventana negra siga abierta y muestre el mensaje del paso 4. |
| La página se abre pero los botones dan error | Mismo caso: el servidor se detuvo. Vuelva a ejecutar `python servidor.py`. |
| `Address already in use` o `Errno 10048` | Ya hay un servidor abierto. Cierre la otra ventana negra o espere un minuto e intente de nuevo. |
| `No module named 'afd'` | La terminal no está en la carpeta del proyecto. Repita el paso 3. |
| La página se ve en blanco o sin formato | Falta la carpeta `web` o el archivo `index.html` está fuera de ella. Revise el paso 2. |

---

## 9. Relación con el informe

| En el informe | En el programa |
|---|---|
| Q, Σ, q₀, F (Tablas 3 y 4) | `afd.py`: `Q`, `SIGMA`, `Q0`, `F` |
| Tabla de transición δ (Tabla 5) | `afd.py`: `TABLA` y `DELTA` (30 pares) |
| Extensión δ* y aceptación | `afd.py`: función `procesar` |
| Condiciones booleanas A, N, X₁, P, X₂ (Tabla 7) | `orquestador.py`: función `decidir` |
| Límite de 3 reintentos (R4) | `orquestador.py`: contador `n` y `L = (n >= 3)` |
| Revisión periódica t ≡ 2 (mod 5) | `orquestador.py`: función `es_revision` |
| Pruebas y matriz de validación | `pruebas.py` |

---

### Espero le guste el programa :)