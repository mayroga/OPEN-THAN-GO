# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.5.5.0
# Company: May Roga LLC
# File: main.py

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

# Tu base de misiones original completa sin recortes
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo."},
        {"id": 2, "titulo": "Desconexión de biles", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer."},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle."},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Deja caer la mochila de deudas. Siente tus hombros libres. Ya no está."},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando."},
        {"id": 6, "titulo": "Liberación de nudos", "descripcion": "Aprieta los puños 3 segundos. Abre de golpe. Suéltalo todo."},
        {"id": 7, "titulo": "El aire de la calle", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior."},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor."},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte."},
        {"id": 10, "titulo": "Orden de tu espacio", "descripcion": "Alinea tres objetos de tu mesa. Orden fuera es orden dentro."},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate."},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe."},
        {"id": 13, "titulo": "Foco en lo olvidado", "descripcion": "Elige una tarea mínima que ignorabas. Hazla ahora. Termínala."},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira."},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza."},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la puerta principal. Deja que el aire ruede. Huele el cambio."},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos."},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque."},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real of calma en tu niñez."},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora."},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana."},
        {"id": 22, "titulo": "Relaja ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad."},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor."},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla."},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."}
    ],
    "CASA_EXTRA": [
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa."},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado."},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto."},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados."},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto."},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos."},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir."},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho."},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total."},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            {"titulo": "Sombra de árbol", "porque": "Tu mente necesita descansar de las luces de la pantalla.", "que_hacer": "Busca un árbol grande. Toca su madera y quédate un rato bajo su sombra fresca.", "donde": "Un parque verde.", "gps": "parks+with+shade+"}
        ],
        "estresado": [
            {"titulo": "Caminata en subida", "porque": "Tu cuerpo acumuló cansancio y necesitas soltarlo caminando.", "que_hacer": "Busca una rampa o escalera pública. Sube a paso firme usando tu fuerza.", "donde": "Escalera pública.", "gps": "public+stairs+"}
        ],
        "aburrido": [
            {"titulo": "Paseo de colores", "porque": "Estás repitiendo los mismos días y necesitas ver cosas nuevas.", "que_hacer": "Camina despacio por la calle. Encuentra dibujos grandes en las paredes de tu zona.", "donde": "Calle con murales.", "gps": "street+art+"}
        ]
    }
}

# Plataformas multimedia de las Big Tech secuestradas con un clic
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://spotify.com",
    "youtube_audio": "https://youtube.com",
    "staffing_agencies": "staffing+agencies"
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    p = await request.json()
    m = str(p.get("modo", "")).upper()
    mente = str(p.get("mente", "aburrido")).lower()
    desahogo = str(p.get("desahogo", "")).lower()
    lang = str(p.get("lang", "es")).lower()
    
    zip_code = str(p.get("zip", "")).strip()
    region = str(p.get("region", "Florida")).strip()
    estado = str(p.get("estado", "FL")).strip()

    # 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
    if m == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        random.shuffle(misiones)  # Rompe la monotonía barajando las misiones locales
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})

    # 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR DE SELECCIÓN ANTI-REPETICIÓN)
    opciones_salir = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
    info = random.choice(opciones_salir)

    # Interceptor de deudas y marcas de consumo de USA
    interceptores_compra = ["amazon", "walmart", "costco", "fresco", "tienda", "comprar", "biles", "deudas", "dinero", "miseria", "trabajo", "explotacion"]
    canal_multimedia = random.choice(["SPOTIFY", "YOUTUBE", "MAPS"])

    if any(pal in desahogo for pal in interceptores_compra):
        if canal_multimedia == "SPOTIFY":
            titulo_ganador = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            entorno_ganador = "Zona Libre de Consumo" if lang == "es" else "Store-Free Zone"
            guia = "DESTINO: Spotify Gratis.\nQUÉ HACER: Escucha los sonidos naturales en silencio.\nPARA QUÉ: Detener el impulso de gastar dinero en cosas innecesarias hoy." if lang == "es" else "TARGET: Free Spotify.\nWHAT TO DO: Listen to nature sounds in silence.\nWHY: Stop the urge to buy unnecessary items today."
            link_base = BIG_TECH_RESOURCES["spotify_audio"]
            gps_query = ""
        elif canal_multimedia == "YOUTUBE"
    titulo_ganador = "REINICIO VISUAL" if lang == "es" else "VISUAL SHOCK"

    entorno_ganador = (
        "Frecuencia de Alivio"
        if lang == "es"
        else "Relief Frequency"
    )

    guia = (
        "DESTINO: Video en YouTube.\n"
        "QUÉ HACER: Pon el video en pantalla completa.\n"
        "PARA QUÉ: Calmar los pensamientos rápidos del día."
        if lang == "es"
        else
        "TARGET: YouTube Video.\n"
        "WHAT TO DO: Play the video in full screen.\n"
        "WHY: Calm your racing thoughts right now."
    )

    link_base = BIG_TECH_RESOURCES["youtube_audio"]
    gps_query = ""

else:

    titulo_ganador = (
        "ACTIVACIÓN LABORAL"
        if lang == "es"
        else "ECONOMIC ACTION"
    )

    entorno_ganador = (
        "Agencia Corporativa de Empleo"
        if lang == "es"
        else "Employment Agency"
    )

    guia = (
        "DESTINO: Google Maps.\n"
        "QUÉ HACER: Camina directo con tu identificación física.\n"
        "PARA QUÉ: Buscar una salida económica limpia y ganar dinero ya."
        if lang == "es"
        else
        "TARGET: Google Maps.\n"
        "WHAT TO DO: Go out straight with your physical ID.\n"
        "WHY: Look for a quick job and get cash now."
    )

    link_base = "https://www.google.com/maps/search/?api=1&query="
    gps_query = BIG_TECH_RESOURCES["staffing_agencies"]

else:

    # Rutas bilingües de texto plano sencillas (nivel niño de 9 años)

    link_base = "https://www.google.com/maps/search/?api=1&query="
    gps_query = info["gps"]

    if lang == "en":

        traducciones_guia = {

            "Sombra de árbol":
                "TARGET: Tree Shade.\n"
                "WHAT TO DO: Touch the bark. Stay under its fresh shade.\n"
                "WHY: Your eyes need a rest from screen lights.",

            "Caminata en subida":
                "TARGET: Public Stairs.\n"
                "WHAT TO DO: Walk up firmly using your strength.\n"
                "WHY: Release the physical stress from your body.",

            "Paseo de colores":
                "TARGET: Street Art.\n"
                "WHAT TO DO: Look at murals in silence. Find hidden details.\n"
                "WHY: Break your daily routine with something new."
        }

        guia = traducciones_guia.get(
            info["titulo"],
            f"TARGET: {info['donde']}.\n"
            f"WHAT TO DO: {info['que_hacer']}\n"
            f"WHY: {info['porque']}"
        )

        titulo_ganador = info["titulo"].upper()
        entorno_ganador = info["donde"]

    else:

        guia = (
            f"DESTINO: {info['titulo']}.\n"
            f"QUÉ HACER: {info['que_hacer']}\n"
            f"PARA QUÉ: {info['porque']}"
        )

        titulo_ganador = info["titulo"].upper()
        entorno_ganador = info["donde"]

# FÓRMULA GEOGRÁFICA UNIVERSAL FIJA RESTAURADA AL 100%
# SIN ALTERAR UN SOLO CARÁCTER

anclaje_geografico = (
    zip_code
    if zip_code
    else f"{region}+{estado}"
)


if gps_query:

    link_google_maps_vivo = (
        f"{link_base}{gps_query}+in+{anclaje_geografico}"
        .replace(" ", "+")
    )

else:

    link_google_maps_vivo = (
        link_base.replace(" ", "+")
    )

return JSONResponse({

    "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",

    "destino_titulo": titulo_ganador,

    "destino_entorno": entorno_ganador,

    "destino_instruccion": guia,

    "destino_coordenadas_gps": link_google_maps_vivo

})

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
