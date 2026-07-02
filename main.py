```python
# OPEN THAN GO SYSTEM - Main Backend Engine
# Company: May Roga LLC
# File: main.py

from flask import Flask, request, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder="static")

# ----------------------------------------------------
# RUTAS ABSOLUTAS (IMPORTANTE PARA RENDER)
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")

# ----------------------------------------------------
# CARGA DE ARCHIVOS AL INICIAR
# ----------------------------------------------------

def cargar_json(ruta):
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error leyendo {ruta}: {e}")

    return {"missions": []}


DATA_01 = cargar_json(MISSIONS_01)
DATA_08 = cargar_json(MISSIONS_08)
DATA_15 = cargar_json(MISSIONS_15)

# ----------------------------------------------------
# CARGADOR DE MISIONES
# ----------------------------------------------------

def cargar_mision_por_bloque(decision, pocket_tier):

    try:

        # ----------------------------------
        # PROTOCOLO CASA
        # ----------------------------------

        if decision == "casa":

            if not DATA_01["missions"]:
                return {
                    "id": 1,
                    "cat": "bien",
                    "b": [
                        {
                            "story": {
                                "es": "Falta el archivo missions_01_07.json en el servidor.",
                                "en": "Missing missions_01_07.json file."
                            }
                        }
                    ]
                }

            return random.choice(DATA_01["missions"])

        # ----------------------------------
        # PROTOCOLO SALIDA
        # ----------------------------------

        bloque = random.choice([DATA_08, DATA_15])

        if not bloque["missions"]:
            bloque = DATA_01

        if not bloque["missions"]:
            return {
                "id": 1,
                "cat": "bien",
                "b": [
                    {
                        "story": {
                            "es": "Sube tus archivos de misiones a GitHub.",
                            "en": "Upload your mission files to GitHub."
                        }
                    }
                ]
            }

        misiones_filtradas = [
            m for m in bloque["missions"]
            if pocket_tier in m.get("pocket_match", [])
        ]

        if misiones_filtradas:
            return random.choice(misiones_filtradas)

        return random.choice(bloque["missions"])

    except Exception as e:
        print(f"Error cargando misión: {e}")
        return None


# ----------------------------------------------------
# FRONTEND
# ----------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(
        app.static_folder,
        "session.html"
    )


# ----------------------------------------------------
# API PRINCIPAL
# ----------------------------------------------------

@app.route("/api/open-than-go", methods=["POST"])
def procesar_sistema_bienestar():

    try:

        data = request.get_json(silent=True) or {}

        decision = data.get("decision", "salir")

        # ==================================
        # PROTOCOLO CASA
        # ==================================

        if decision == "casa":

            mision = cargar_mision_por_bloque(
                "casa",
                "cero"
            )

            if not mision:
                return jsonify({
                    "status": "error",
                    "message": "No se pudo generar la misión."
                }), 500

            return jsonify({
                "status": "success",
                "tipo": "Casa",
                "mision": mision
            })

        # ==================================
        # DATOS DEL USUARIO
        # ==================================

        zip_code = data.get("zip_code", "").strip()
        region = data.get("region", "").strip()
        estado = data.get("estado", "FL").strip()
        pocket = data.get("budget_level", "cero")
        desahogo = data.get("desahogo", "").lower()

        # ==================================
        # CATEGORÍAS
        # ==================================

        categorias_por_bolsillo = {
            "cero": [
                "parques naturales publicos",
                "playas publicas",
                "senderos para caminar",
                "miradores gratis"
            ],
            "minimo": [
                "cafeterias economicas",
                "mercados locales al aire libre",
                "zonas de recreacion comunitarias"
            ],
            "moderado": [
                "restaurantes familiares",
                "centros de diversion",
                "pistas de baile",
                "centros recreativos"
            ],
            "libre": [
                "hoteles resorts",
                "discotecas club",
                "restaurantes premium",
                "centros de entretenimiento"
            ]
        }

        # ==================================
        # FILTRO DE EMPLEO
        # ==================================

        palabras_empleo = [
            "trabajo",
            "empleo",
            "job",
            "company",
            "compañia",
            "compañía"
        ]

        if any(p in desahogo for p in palabras_empleo):
            termino_busqueda = (
                "compañias agencias de trabajo y empleo"
            )
        else:
            termino_busqueda = random.choice(
                categorias_por_bolsillo.get(
                    pocket,
                    ["parques"]
                )
            )

        # ==================================
        # UBICACIÓN
        # ==================================

        if zip_code:
            ubicacion_destino = zip_code
        elif region:
            ubicacion_destino = f"{region} {estado}"
        else:
            ubicacion_destino = estado

        # ==================================
        # GOOGLE MAPS
        # ==================================

        query_mapa = (
            f"{termino_busqueda} en {ubicacion_destino}"
            .replace(" ", "+")
        )

        link_google_maps_vivo = (
            f"https://www.google.com/maps/search/?api=1&query={query_mapa}"
        )

        # ==================================
        # MISIÓN
        # ==================================

        mision = cargar_mision_por_bloque(
            "salir",
            pocket
        )

        if not mision:
            return jsonify({
                "status": "error",
                "message": "No se pudo generar la misión."
            }), 500

        return jsonify({
            "status": "success",
            "tipo": "Salida",
            "lugar": {
                "name": f"Exploración de {termino_busqueda.title()}",
                "address": f"Cerca de tu área ({ubicacion_destino})",
                "region": region,
                "gps_link": link_google_maps_vivo
            },
            "mision": mision
        })

    except Exception as e:
        print(f"ERROR API: {e}")

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ----------------------------------------------------
# INICIO
# ----------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )

