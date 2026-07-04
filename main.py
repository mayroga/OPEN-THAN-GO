from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_MISIONES = {
    "CASA": [
        {"titulo": "Fase 1: Reconocimiento Somático", "descripcion": "Identifica tu tensión actual sin juzgarla. Escanea tu cuerpo en silencio."},
        {"titulo": "Fase 2: Regulación Pulmonar", "descripcion": "Inhala profundamente en 4 tiempos, mantén el aire por 2 tiempos y exhala en 6."},
        {"titulo": "Fase 3: Desapego Digital", "descripcion": "Deja tu teléfono boca abajo. Observa 3 objetos en tu habitación, nota sus texturas."},
        {"titulo": "Fase 4: Técnica de la Mochila", "descripcion": "Imagina que dejas caer al suelo una mochila pesada con todas tus deudas y biles. Siente tus hombros libres."},
        {"titulo": "Fase 5: Cierre de Autonomía", "descripcion": "Bebe un vaso de agua lentamente, sintiendo el recorrido del líquido. Agradece una sola cosa que lograste hoy."}
    ],
    "SALIR": {
        "agotado": [
            {"titulo": "Refugio Natural", "porque": "Tu sistema necesita reducir la sobreestimulación de las pantallas y el agobio diario.", "que_hacer": "Camina sin rumbo en zona verde.", "donde": "Parque plano de libre acceso.", "gps": "nature+parks+near+"},
            {"titulo": "Mirador de Horizonte", "porque": "Necesitas relajar tu vista y tu perspectiva diaria de la rutina.", "que_hacer": "Mira hacia la línea del horizonte.", "donde": "Punto alto o muelle de descanso.", "gps": "viewpoint+near+"}
        ],
        "estresado": [
            {"titulo": "Zona de Descarga", "porque": "Necesitas metabolizar el cortisol acumulado por el trabajo.", "que_hacer": "Caminata a ritmo firme y pesado.", "donde": "Pista pública o sendero lineal.", "gps": "recreation+centers+near+"},
            {"titulo": "Circuito de Movilidad", "porque": "Desbloquea las articulaciones donde guardas la tensión del dinero.", "que_hacer": "Camina activando el movimiento de tus hombros al aire.", "donde": "Parque lineal o camino peatonal.", "gps": "linear+park+near+"}
        ],
        "aburrido": [
            {"titulo": "Distrito de Estímulo", "porque": "La monotonía bloquea tu dopamina. Necesitas asombro e impacto visual.", "que_hacer": "Visita una zona de arte urbano, murales y flujo público.", "donde": "Plaza principal o distrito de diseño.", "gps": "arts+and+entertainment+near+"},
            {"titulo": "Mercado de Sabores", "porque": "La novedad sensorial despierta el interés por tu entorno urbano.", "que_hacer": "Huele los productos nuevos y observa los colores de los puestos.", "donde": "Mercado local o feria comunitaria.", "gps": "farmers+market+near+"}
        ]
    }
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    
    # DINAMISMO GEOGRÁFICO TOTAL: Captura el valor exacto enviado por el usuario en pantalla sin dejar nada fijo
    modo = str(payload.get("modo", "SALIR")).upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "agotado")).lower()
    budget = str(payload.get("budget", "0"))
    perfil = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    
    if modo == "CASA":
        misiones_dinamicas = list(BASE_MISIONES["CASA"])
        random.shuffle(misiones_dinamicas)
        return JSONResponse({"modo": "CASA", "misiones": misiones_dinamicas[:3]})
    
    else:
        info = random.choice(BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"]))
        
        # Filtro de supervivencia por desahogo emocional
        palabras_criticas = ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion"]
        if any(p in desahogo for p in palabras_criticas):
            gps_query = "agencias+de+empleo+staffings+corporations"
            que_hacer_base = "QUÉ: Localizar módulos de contratación rápida. CÓMO: Presenta tu identificación en recepción. CUÁNDO: Por la mañana de forma prioritaria. PARA QUÉ: Romper la parálisis del agobio económico."
            donde_base = "Agencias de reclutamiento laboral rápido en tu zona."
        else:
            # Filtro elástico por niveles de dinero
            if budget == "0":
                gps_query = "free+public+parks+and+beaches"
            elif budget == "1":
                gps_query = "low+cost+coffee+shops+and+local+markets"
            else:
                gps_query = info["gps"]
            
            que_hacer_base = f"QUÉ: {info['que_hacer']} CÓMO: Camina observando detalles. CUÁNDO: A partir de las 4:00 PM. PARA QUÉ: Romper tu piloto automático urbano."
            donde_base = info["donde"]

        # Adaptabilidad biopsicosocial de perfil físico y edad
        msg_adicional = ""
        if perfil == "accesible":
            msg_adicional = " (Ruta plana con prioridad de total accesibilidad física/edad)."
            gps_query = "wheelchair+accessible+" + gps_query
        elif perfil == "familia":
            msg_adicional = " (Entorno integrador apto para menores y niños)."
            gps_query = "family+friendly+" + gps_query

        # FÓRMULA GEOGRÁFICA UNIVERSAL: Usa el ZIP si existe, si no usa la combinación Región + Estado para todo USA
        anclaje_geografico = zip_code if zip_code else f"{region}+{estado}"
        link_maps = f"https://google.com{gps_query}+in+{anclaje_geografico}".replace(" ", "+")
        
        return JSONResponse({
            "modo": "SALIR",
            "titulo": info["titulo"].upper(),
            "porque": info["porque"],
            "que_hacer": que_hacer_base + msg_adicional,
            "donde": donde_base,
            "gps": link_maps
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
