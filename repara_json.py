# -*- coding: utf-8 -*-
# Repara maestria-config.json: salto de línea/tabulación raw dentro de una
# cadena JSON no es válido; se escapan como \n y \t, y se reescribe normalizado.
import json

RUTA = "maestria-config.json"
src = open(RUTA, encoding="utf-8").read()

def repara(texto):
    out, in_str, esc = [], False, False
    for ch in texto:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            elif ch == "\n":
                out.append("\\n")
                continue
            elif ch == "\t":
                out.append("\\t")
                continue
            elif ch == "\r":
                continue
        else:
            if ch == '"':
                in_str = True
        out.append(ch)
    return "".join(out)

try:
    datos = json.loads(src)
    print("JSON ya era valido; reescribo normalizado")
except Exception as e:
    print("Error original:", e)
    datos = json.loads(repara(src))
    print("REPARADO")

open(RUTA, "w", encoding="utf-8", newline="\n").write(
    json.dumps(datos, ensure_ascii=False, indent=2) + "\n"
)
print("eventos =", len(datos["events"]))
print("fuentes =", len(datos["sources"]))
# muestro cuántos eventos cambiaron respecto al original embebido de index.html
html = open("index.html", encoding="utf-8").read()
import re
m = re.search(r"const ORIGINAL = (\{.*?\});\n\n/\*", html, re.S)
orig = json.loads(m.group(1))
dif = [ev["date"] for a, b in zip(orig["events"], datos["events"]) if a["description"] != b["description"]]
print("eventos editados:", dif if dif else "ninguno")