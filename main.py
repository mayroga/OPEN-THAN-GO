import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===============================
# MEMORIA LIGERA DE SESIÓN (NO PERSONAL)
# SOLO EVITA REPETICIÓN
# ===============================
session_memory = {}


# ===============================
# CARGADOR TVID INTELIGENTE
# ===============================
def cargar_mision_tvid_desde_archivos(categoria_emocional, bolsillo_usuario, session_id="anon"):

    archivos_kamizen = [
        'missions_01_07.json',
        'missions_08_14.json',
        'missions_15_21.json'
    ]

    todas_las_tvid = []

    # Cargar todas las misiones
    for nombre_archivo in archivos_kamizen:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for m in data.get("missions", []):
                    todas_las_tvid.append(m)
        except Exception as e:
            print(f"Error cargando {nombre_archivo}: {e}")

    # Filtrar por categoría y bolsillo
    filtradas = [
        m for m in todas_las_tvid
        if m.get("cat") == categoria_emocional
        and bolsillo_usuario in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]

    # ===============================
    # EVITAR REPETICIÓN POR SESIÓN
    # ===============================
    usados = session_memory.get(session_id, set())

    nuevas = [m for m in filtradas if m.get("id") not in usados]

    if nuevas:
        seleccionada = random.choice(nuevas)
    elif filtradas:
        # reset si ya se agotaron
        session_memory[session_id] = set()
        seleccionada = random.choice(filtradas)
    else:
        seleccionada = None

    if seleccionada:
        session_memory.setdefault(session_id, set()).add(seleccionada.get("id"))

    return seleccionada


# ===============================
# HOME
# ===============================
@app.route('/')
def home():
    try:
        return app.send_static_file('session.html')
    except Exception:
        with open('session.html', 'r', encoding='utf-8') as f:
            from flask import render_template_string
            return render_template_string(f.read())


# ===============================
# DETECTOR EMOCIONAL
# ===============================
def detectar_categoria(texto):
    texto = texto.lower()

    if any(x in texto for x in ["biles", "dinero", "deuda", "cuenta", "estrés", "mal", "factura"]):
        return "mal"

    if any(x in texto for x in ["niño", "hijo", "kids", "familia"]):
        return "nino"

    if any(x in texto for x in ["solo", "triste", "vacío", "aburrido", "monoton"]):
        return "bien"

    return "bien"


# ===============================
# MOTOR PRINCIPAL
# ===============================
@app.route('/diagnostico-kamizen', methods=['POST'])
def diagnostico_kamizen():

    datos = request.json

    puedes_salir = datos.get('puedes_salir', True)
    idioma = datos.get('idioma', 'es')

    zip_code = str(datos.get('zip_code', '')).strip()
    estado = str(datos.get('estado', 'FL')).strip()

    bolsillo = datos.get('bolsillo', 'cero')
    texto_libre = str(datos.get('texto_libre', ''))

    # ID de sesión (NO es identidad personal)
    session_id = datos.get("session_id", "anon")

    categoria = detectar_categoria(texto_libre)

    mision_tvid = cargar_mision_tvid_desde_archivos(
        categoria,
        bolsillo,
        session_id
    )

    if not mision_tvid:
        return jsonify({"error": "No hay misiones disponibles"}), 404

    # ===============================
    # TRADUCCIÓN DE BLOQUES
    # ===============================
    bloques_processed = []

    for bloque in mision_tvid.get("b", []):

        b = dict(bloque)

        # traducción general
        for campo in ["tx", "inf", "story"]:
            if campo in b and isinstance(b[campo], dict):
                b[campo] = b[campo].get(idioma, b[campo].get("es", ""))

        # decisión
        if b.get("t") == "d":

            if isinstance(b.get("q"), dict):
                b["q"] = b["q"].get(idioma, b["q"].get("es", ""))

            if "op" in b:
                b["op"] = [
                    op.get(idioma, op.get("es", "")) if isinstance(op, dict) else op
                    for op in b["op"]
                ]

            if "ex" in b:
                b["ex"] = [
                    ex.get(idioma, ex.get("es", "")) if isinstance(ex, dict) else ex
                    for ex in b["ex"]
                ]

        bloques_processed.append(b)


    # ===============================
    # RAMA INDOOR
    # ===============================
    if not puedes_salir:

        titulo = (
            "Modo Interior: Reconstrucción Emocional"
            if idioma == "es"
            else "Indoor Mode: Emotional Reset"
        )

        return jsonify({
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": "Tu espacio personal de equilibrio",
            "bloques_interactivos": bloques_processed,
            "url_maps": None
        })


    # ===============================
    # RAMA OUTDOOR
    # ===============================
    if not zip_code or len(zip_code) != 5:
        zip_code = "33101"

    tipo_mapa = "parks"

    if categoria == "nino":
        tipo_mapa = "parks+playgrounds+family"
    elif categoria == "mal":
        tipo_mapa = "nature+quiet+parks+reserves"

    query = f"{tipo_mapa} {zip_code} {estado} USA"
    url_maps = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    titulo_out = (
        "Plan de Escape Activo"
        if idioma == "es"
        else "Active Escape Plan"
    )

    instruccion = {
        "t": "h",
        "tx": (
            f"Dirígete a {zip_code}. Inicia la secuencia al llegar."
            if idioma == "es"
            else f"Go to {zip_code}. Start your sequence upon arrival."
        )
    }

    bloques_processed.insert(0, instruccion)

    return jsonify({
        "modalidad": "outdoor",
        "titulo": titulo_out,
        "lugar": f"Zona activa en {zip_code}, {estado}",
        "bloques_interactivos": bloques_processed,
        "url_maps": url_maps
    })


# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
