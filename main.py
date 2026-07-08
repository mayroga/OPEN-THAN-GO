# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.5.5.0
# Company: May Roga LLC
# File: main.py - CODIGO COMPLETO UNIFICADO Y BLINDADO

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

# Tu base de misiones original completa + Inyección Vectorial de 19 Necesidades Humanas
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
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez."},
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
        {"id": 32, "conciencia": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir."},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho."},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total."},
        {"id": 35, "cuenta": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "aire": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "siente": "Siente base", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "presencia": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            {
                "titulo": "Sombra de árbol",
                "porque": "Tu mente necesita descansar de las luces de la pantalla.",
                "que_hacer": "Busca un árbol grande. Toca su madera y quédate un rato bajo su sombra fresca.",
                "donde": "Un parque verde.",
                "gps": "parks+with+shade+",
                "vector_necesidades": {
                    "movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 20, "sol": 40,
                    "sombra": 100, "aire_fresco": 100, "creatividad": 30, "comunidad": 20, "aprendizaje": 40,
                    "juego": 30, "contemplacion": 95, "trabajo": 10, "descanso": 90, "organizacion": 20,
                    "alimentacion": 0, "musica": 10, "risa": 30, "esperanza": 85
                }
            }
        ],
        "estresado": [
            {
                "titulo": "Caminata en subida",
                "porque": "Tu cuerpo acumuló cansancio y necesitas soltarlo caminando.",
                "que_hacer": "Busca una rampa o escalera pública. Sube a paso firme usando tu fuerza.",
                "donde": "Escalera pública.",
                "gps": "public+stairs+",
                "vector_necesidades": {
                    "movimiento": 100, "naturaleza": 30, "silencio": 50, "agua": 10, "sol": 70,
                    "sombra": 20, "aire_fresco": 85, "creatividad": 10, "comunidad": 30, "aprendizaje": 10,
                    "juego": 20, "contemplacion": 60, "trabajo": 20, "descanso": 10, "organizacion": 30,
                    "alimentacion": 0, "musica": 20, "risa": 20, "esperanza": 75
                }
            }
        ],
        "aburrido": [
            {
                "titulo": "Paseo de colores",
                "porque": "Estás repitiendo los mismos días y necesitas ver cosas nuevas.",
                "que_hacer": "Camina despacio por la calle. Encuentra dibujos grandes en las paredes de tu zona.",
                "donde": "Calle con murales.",
                "gps": "street+art+",
                "vector_necesidades": {
                    "movimiento": 80, "naturaleza": 20, "silencio": 40, "agua": 10, "sol": 80,
                    "sombra": 50, "aire_fresco": 90, "creatividad": 100, "comunidad": 60, "aprendizaje": 70,
                    "juego": 55, "contemplacion": 85, "trabajo": 10, "descanso": 30, "organizacion": 20,
                    "alimentacion": 20, "musica": 30, "risa": 60, "esperanza": 95
                }
            }
        ]
    }
}

# Recursos de infraestructura trillonaria secuestrados para romper la monotonía
BIG_TECH_RESOURCES = {
    "spotify_audio": "https://spotify.com",
    "youtube_audio": "https://youtube.com"
}

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "agotado")).lower()
    budget = str(payload.get("budget", "0"))
perfil=str(payload.get("perfil","solo")).lower()
desahogo=str(payload.get("desahogo","")).lower()
lang=str(payload.get("lang","es")).lower()
perfil_local=payload.get("perfil_local",{})

# PRIORIDAD ABSOLUTA DEL CAJÓN: Si escribe en el cajón, nada está por encima
if desahogo.strip():
    opcion_usuario="MANDO_LIBRE"

# 1. INTERVENCIÓN DOMÉSTICA (MODO CASA ORIGINAL INTACTO)
if opcion_usuario=="CASA":
    misiones=BASE_MISIONES["CASA"]+BASE_MISIONES["CASA_EXTRA"]
    random.shuffle(misiones)
    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER":"INTERVENCION_DOMESTICA",
        "misiones":misiones
    })

# 2. ACCIÓN DE CAMPO (MODO SALIR CON MOTOR DE SELECCIÓN ANTI-REPETICIÓN)
opciones_salir=BASE_MISIONES["SALIR"].get(mente,BASE_MISIONES["SALIR"]["aburrido"])
random.shuffle(opciones_salir)

# Inyección silenciosa adaptativa para Poblaciones Especiales de USA
if perfil=="veterano":
    perfil_local["silencio"]=perfil_local.get("silencio",50)+40
    perfil_local["contemplacion"]=perfil_local.get("contemplacion",50)+30
elif perfil in ["adulto_mayor","accessible"]:
    perfil_local["sombra"]=perfil_local.get("sombra",50)+50
    perfil_local["descanso"]=perfil_local.get("descanso",50)+30
elif perfil in ["gobierno","empresario","directivo","trabajador"]:
    perfil_local["aire_fresco"]=perfil_local.get("aire_fresco",50)+40
    perfil_local["creatividad"]=perfil_local.get("creatividad",50)+30

# Motor de puntuación CWRE: Pondera los lugares de campo de mayor a menor coincidencia
lugares_puntuados=[]
for opc in opciones_salir:
    vector_lugar=opc.get("vector_necesidades",{})
    score=0
    for necesidad,peso_usuario in perfil_local.items():
        if isinstance(peso_usuario,(int,float)):
            score+=vector_lugar.get(necesidad,50)*peso_usuario
    lugares_puntuados.append((score,opc))

# Ordena de mayor a menor y extrae las 3 mejores opciones distintas (REGLA DE 3 OPCIONES)
lugares_puntuados.sort(key=lambda x:x[0],reverse=True)
tres_mejores=[item[1] for item in lugares_puntuados[:3]]

while len(tres_mejores)<3 and opciones_salir:
    tres_mejores.append(random.choice(opciones_salir))

# Filtros de precio real en palabras cortas de acción
precio_real="GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if budget=="0" else "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if budget=="1" else "GASTO: Libre. El dinero es tu herramienta de escape hoy."

# Tratamiento bilingüe e inyecciones de acompañantes según perfil de población
if perfil=="veterano":
    quienes_van="ACOMPAÑAMIENTO: Entorno de respeto para tu descanso interior." if lang=="es" else "ACCOMPANIMENT: Honorable environment for your inner peace."
    tratamiento_especial="Territorio seguro. Desconéctate con total libertad." if lang=="es" else "Safe territory. Disconnect with complete freedom."
elif perfil=="adulto_mayor":
    quienes_van="ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad." if lang=="es" else "ACCOMPANIMENT: Flat route with full accessibility for your comfort."
    tratamiento_especial="Desplázate a ritmo lento. Áreas sombreadas disponibles." if lang=="es" else "Move at a slow pace. Shaded areas available."
elif perfil in ["gobierno","empresario","directivo","trabajador"]:
    quienes_van="ACOMPAÑAMIENTO: Desconexión radical del tiempo corporativo." if lang=="es" else "ACCOMPANIMENT: Radical disconnection from corporate schedule."
    tratamiento_especial="Fuera del sistema por los próximos 60 minutos. No mires pantallas." if lang=="es" else "Outside the system for the next 60 minutes. Do not look at screens."
else:
    quienes_van="ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if lang=="es" else "ACCOMPANIMENT: You go alone with yourself to recover your center."
    tratamiento_especial=""

# FILTRO INTERCEPTOR SIN TRABAJO NI STAFFING
palabras_criticas=["trabajo","empleo","compañia","compañía","job","biles","deudas","bills","miseria","explotacion","amazon","walmart","costco","fresco","tienda","comprar","dinero","gastar","compras"]

opciones_de_salida=[]

for i,info in enumerate(tres_mejores):
    if any(p in desahogo for p in palabras_criticas) or opcion_usuario=="MANDO_LIBRE":
        canal_multimedia=["SPOTIFY","YOUTUBE","MAPS"][i%3]
        if canal_multimedia=="SPOTIFY":
    titulo_ganador="RESET AUDITIVO" if lang=="es" else "AUDIO RESET"
    donde_base="Zona Libre de Consumo" if lang=="es" else "Store-Free Zone"
    guia_masticada="DESTINO: Spotify Gratis.\nQUÉ HACER: Escucha los sonidos naturales en silencio.\nPARA QUÉ: Detener el impulso de gastar dinero en cosas innecesarias hoy." if lang=="es" else "TARGET: Free Spotify.\nWHAT TO DO: Listen to nature sounds in silence.\nWHY: Stop the urge to buy unnecessary items today."
    link_base=BIG_TECH_RESOURCES["spotify_audio"]
    gps_query=""

elif canal_multimedia=="YOUTUBE":
    titulo_ganador="REINICIO VISUAL" if lang=="es" else "VISUAL SHOCK"
    donde_base="Frecuencia de Alivio" if lang=="es" else "Relief Frequency"
    guia_masticada="DESTINO: Video en YouTube.\nQUÉ HACER: Pon el video en pantalla completa.\nPARA QUÉ: Calmar los pensamientos rápidos del día." if lang=="es" else "TARGET: YouTube Video.\nWHAT TO DO: Play the video in full screen.\nWHY: Calm your racing thoughts right now."
    link_base=BIG_TECH_RESOURCES["youtube_audio"]
    gps_query=""

else:
    titulo_ganador="EXPLORACIÓN DE AUSENCIA" if lang=="es" else "ABSENCE EXPLORATION"
    donde_base=info["donde"]
    guia_masticada=f"DESTINO: Un entorno natural o plaza al aire libre.\nQUÉ HACER: Camina despacio registrando el viento, el cielo y el flujo del entorno.\nPARA QUÉ: Romper la hipnosis del encierro sin gastar dinero.\n\n{quienes_van}\n{precio_real}" if lang=="es" else f"TARGET: Free Nature Trail or Open Plaza.\nWHAT TO DO: Walk slowly registering the wind, the sky, and the natural flow.\nWHY: Break the indoor hypnosis without spending money.\n\n{quienes_van}\n{precio_real}"
    link_base="google.com"
    gps_query=info["gps"]

else:
    link_base="google.com"
    gps_query=info["gps"]
    donde_base=info["donde"]
    titulo_ganador=info["titulo"].upper()

    if lang=="en":
        traducciones_guia={
            "Sombra de árbol":"TARGET: Tree Shade.\nWHAT TO DO: Touch the bark. Stay under its fresh shade.\nWHY: Your eyes need a rest from screen lights.",
            "Caminata en subida":"TARGET: Public Stairs.\nWHAT TO DO: Walk up firmly using your strength.\nWHY: Release the physical stress from your body.",
            "Paseo de colores":"TARGET: Street Art.\nWHAT TO DO: Look at murals in silence. Find hidden details.\nWHY: Break your daily routine with something new."
        }
        guia_masticada=traducciones_guia.get(info["titulo"],f"TARGET: {info['donde']}.\nWHAT TO DO: {info['que_hacer']}\nWHY: {info['porque']}")+f"\n\n{quienes_van}\n{precio_real}"
    else:
        guia_masticada=f"DESTINO: {info['titulo']}.\nPOR QUÉ: {info['porque']}\nQUÉ HACER: {info['que_hacer']}\nCUÁNDO: Ahora mismo. Levántate de la silla ya.\nPARA QUÉ: Para romper el zombi urbano y recordar que la vida es más que pagar cuentas.\n\n{quienes_van}\n{precio_real}"
        if tratamiento_especial:
    guia_masticada+=f"\n\n{tratamiento_especial}"

# Adaptabilidad del Perfil Biopsicosocial sin exclusión social
if perfil=="accessible":
    gps_query="wheelchair+accessible+"+gps_query
elif perfil=="family":
    gps_query="family+friendly+"+gps_query

# FÓRMULA GEOGRÁFICA UNIVERSAL FIJA ORIGINAL RESTAURADA SIN RECORTE NI ALTERACIONES
anclaje_geografico=zip_code if zip_code else f"{region}+{estado}"

if gps_query:
    if link_base.startswith("http"):
        link_google_maps_vivo=f"{link_base}{gps_query}+in+{anclaje_geografico}".replace(" ","+")
    else:
        link_google_maps_vivo=link_base.replace(" ","+")
else:
    link_google_maps_vivo=link_base.replace(" ","+")

opciones_de_salida.append({
    "destino_titulo":titulo_ganador,
    "destino_entorno":donde_base,
    "destino_instruccion":guia_masticada.strip(),
    "destino_coordenadas_gps":link_google_maps_vivo
})

return JSONResponse({
    "DIRECCIONAMIENTO_MASTER":opcion_usuario if opcion_usuario=="CASA" else "ACCION_CAMPO",
    "opciones":opciones_de_salida
})

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=int(os.environ.get("PORT",8000)))
