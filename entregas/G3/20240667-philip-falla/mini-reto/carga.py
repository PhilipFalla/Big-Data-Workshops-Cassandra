"""Carga del mini-reto G3 (Discord) en discord_20240667.

Hace en Python los JOIN que Cassandra no tiene: genera un CSV por tabla
de Cassandra, lo copia al contenedor y lo carga con COPY.

Uso, desde la raiz del repo y con modelo.cql ya creado:
    python3 entregas/G3/20240667-philip-falla/mini-reto/carga.py
"""
import csv
import subprocess
import tempfile
from pathlib import Path

NODO = "cassandra1"
KEYSPACE = "discord_20240667"
ORIGEN = Path(__file__).resolve().parents[4] / "data" / "mini-reto" / "G3-discord"


def leer(nombre):
    with open(ORIGEN / f"{nombre}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def utc(ts):
    # Las horas de los CSV estan en UTC; se marcan asi para que COPY no las interprete en otra zona.
    return ts + "+0000"


servidores = {s["servidor_id"]: s["nombre"] for s in leer("servidores")}
canales = {c["canal_id"]: c for c in leer("canales")}
usuarios = leer("usuarios")
nombre_de = {u["usuario_id"]: u["nombre_usuario"] for u in usuarios}
mensajes = leer("mensajes")

tablas = {
    "usuarios_por_id": (
        ["usuario_id", "nombre_usuario", "creado_en"],
        [[u["usuario_id"], u["nombre_usuario"], utc(u["creado_en"])] for u in usuarios],
    ),
    "mensajes_por_canal": (
        ["canal_id", "enviado_en", "mensaje_id", "usuario_id", "nombre_usuario", "contenido"],
        [[m["canal_id"], utc(m["enviado_en"]), m["mensaje_id"], m["usuario_id"],
          nombre_de[m["usuario_id"]], m["contenido"]] for m in mensajes],
    ),
    "mensajes_por_usuario": (
        ["usuario_id", "enviado_en", "mensaje_id", "canal_id", "nombre_canal", "nombre_servidor", "contenido"],
        [[m["usuario_id"], utc(m["enviado_en"]), m["mensaje_id"], m["canal_id"],
          canales[m["canal_id"]]["nombre"], servidores[canales[m["canal_id"]]["servidor_id"]],
          m["contenido"]] for m in mensajes],
    ),
    "mensajes_por_canal_dia": (
        ["canal_id", "dia", "enviado_en", "mensaje_id"],
        [[m["canal_id"], m["enviado_en"][:10], utc(m["enviado_en"]), m["mensaje_id"]] for m in mensajes],
    ),
}

with tempfile.TemporaryDirectory() as tmp:
    for tabla, (columnas, filas) in tablas.items():
        archivo = Path(tmp) / f"{tabla}.csv"
        with open(archivo, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(columnas)
            w.writerows(filas)
        subprocess.run(["docker", "cp", str(archivo), f"{NODO}:/tmp/{tabla}.csv"], check=True)
        copy = (f"COPY {KEYSPACE}.{tabla} ({', '.join(columnas)}) "
                f"FROM '/tmp/{tabla}.csv' WITH HEADER = true;")
        subprocess.run(["docker", "exec", NODO, "cqlsh", "-e", copy], check=True)
        print(f"{tabla}: {len(filas)} filas enviadas")
