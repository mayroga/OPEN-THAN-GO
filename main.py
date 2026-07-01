import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)


# ===============================
# CARGADOR TVID INTELIGENTE
# ===============================
def cargar_mision_tvid_desde_archivos(categoria_emocional, bolsillo_usuario):
    archivos_kamizen = [
        'missions_01_07.json',
        'missions_08_14.json',
        'missions_15_21.json'
    ]

    todas_las_tvid = []

    for nombre_archivo in archivos_kamizen:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for m in data.get("missions", []):
                    if m.get("id", 0) >= 1:
                        todas_las_tvid.append(m)
        except Exception as e:
            print(f"Error cargando {nombre_archivo}: {e}")

    filtradas = [
        m for m in todas_las_tvid
        if m.get("cat") == categoria_emocional
        and bolsillo_usuario in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]

    if filtradas:
        return random.choice(filtradas)

    if todas_las_tvid:
        return random.choice(todas_las_tvid)

    return None


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
# DETECTOR EMOCIONAL KAMIZEN
# ===============================
def detectar_categoria(texto):
    texto = texto.lower()

    if any(x in texto for x in ["biles", "dinero", "deuda", "cuenta", "estrés", "mal"]):
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

    categoria = detectar_categoria(texto_libre)

    mision_tvid = cargar_mision_tvid_desde_archivos(categoria, bolsillo)

    if not mision_tvid:
        return jsonify({"error": "No hay misiones disponibles"})

    # ===============================
    # TRADUCCIÓN DE BLOQUES TVID
    # ===============================
    bloques_processed = []

    for comando in mision_tvid.get("b", []):
        bloque = comando.copy()

        for campo in ["tx", "inf", "story", "c"]:
            if campo in bloque and isinstance(bloque[campo], dict):
                bloque[campo] = bloque[campo].get(idioma, bloque[campo].get('es', ''))

        if bloque.get("t") == "d":
            if isinstance(bloque.get("q"), dict):
                bloque["q"] = bloque["q"].get(idioma, bloque["q"].get('es', ''))

            if "op" in bloque:
                bloque["op"] = [
                    op.get(idioma, op.get('es', '')) if isinstance(op, dict) else op
                    for op in bloque["op"]
                ]

            if "ex" in bloque:
                bloque["ex"] = [
                    ex.get(idioma, ex.get('es', '')) if isinstance(ex, dict) else ex
                    for ex in bloque["ex"]
                ]

        bloques_processed.append(bloque)


    # ===============================
    # RAMA 1: NO SALE DE CASA (KAMIZEN HOME MODE)
    # ===============================
    if not puedes_salir:

        titulo = (
            "Modo Interior: Reconstrucción Emocional"
            if idioma == 'es'
            else "Indoor Mode: Emotional Reset"
        )

        # 👉 aquí puedes conectar tus TVid casa 10 min sin llamar terapia
        return jsonify({
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": "Tu espacio personal de equilibrio",
            "bloques_interactivos": bloques_processed,
            "url_maps": None
        })


    # ===============================
    # RAMA 2: SALE DE CASA (ESCAPE MODE)
    # ===============================
    if not zip_code or len(zip_code) != 5:
        zip_code = "33101"

    tipo_mapa = "parks"

    if categoria == "nino":
        tipo_mapa = "parks+playgrounds+family"
    elif categoria == "mal":
        tipo_mapa = "nature+reserves+quiet+parks"

    # 🔥 GOOGLE MAPS REAL (CORREGIDO)
    query = f"{tipo_mapa} {zip_code} {estado} USA"
    url_maps_gratis = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    titulo_out = (
        "Plan de Escape Activo"
        if idioma == 'es'
        else "Active Escape Plan"
    )

    instruccion_viaje = {
        "t": "h",
        "tx": (
            f"Dirígete a tu zona recomendada en {zip_code}. "
            f"Cuando llegues, comienza la secuencia de liberación."
            if idioma == 'es'
            else f"Go to your recommended area in {zip_code}. Start your reset sequence upon arrival."
        )
    }

    bloques_processed.insert(0, instruccion_viaje)

    return jsonify({
        "modalidad": "outdoor",
        "titulo": titulo_out,
        "lugar": f"Zona activa en {zip_code}, {estado}",
        "bloques_interactivos": bloques_processed,
        "url_maps": url_maps_gratis
    })


# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
