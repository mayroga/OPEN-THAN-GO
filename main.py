# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.4.0.0
# Company: May Roga LLC
# File: main.py
# Propósito: Motor Predictivo de Activación Humana (Secuestro de Algoritmos Big Tech)

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

# Diccionario Estructural de Infraestructura Física y Psicológica de USA
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
            {"titulo": "Sombra de árbol", "porque": "Mente frita por luz artificial.", "que_hacer": "Toca corteza de árbol, siente su textura. Quédate bajo sombra densa.", "donde": "Parque grande.", "gps": "parks+with+shade+", "peso_prediccion": 0.95},
            {"titulo": "Silencio de pradera", "porque": "Saturación por ruido urbano continuo.", "que_hacer": "Camina despacio mirando solo el suelo natural. Respira el vacío.", "donde": "Área verde abierta.", "gps": "open+green+space+", "peso_prediccion": 0.91}
        ],
        "estresado": [
            {"titulo": "Resistencia de colina", "porque": "Cortisol bloqueando hombros y respiración.", "que_hacer": "Sube rampa o escalera a paso firme. Usa la gravedad para soltar tensión.", "donde": "Escalera pública.", "gps": "public+stairs+", "peso_prediccion": 0.98},
            {"titulo": "Anclaje de agua viva", "porque": "Pensamientos acelerados y repetitivos.", "que_hacer": "Observa el flujo constante del agua 5 minutos sin mirar el teléfono.", "donde": "Lago o muelle público.", "gps": "lakes+or+waterfronts+", "peso_prediccion": 0.94}
        ],
        "aburrido": [
            {"titulo": "Colores urbanos", "porque": "Piloto automático gris y falta de estímulo real.", "que_hacer": "Mira murales. Encuentra tres detalles pequeños. Asómbrate.", "donde": "Calle con murales.", "gps": "street+art+", "peso_prediccion": 0.92},
            {"titulo": "Análisis Arquitectónico", "porque": "Pérdida de la capacidad de observación fina.", "que_hacer": "Rastrea patrones geométricos en fachadas antiguas. Obliga al ojo a buscar asimetrías.", "donde": "Biblioteca o edificio histórico.", "gps": "historical+facades+", "peso_prediccion": 0.89}
        ]
    }
}

def calcular_probabilidad_engache(datos_usuario: dict, opcion_destino: dict) -> float:
    """
    ENGINE BIG TECH: Similitud Predictiva por Emparejamiento de Características Vectoriales.
    Calcula la probabilidad exacta (P(clic)) de que el perfil acepte el destino para romper su inercia.
    """
    score = 0.0
    
    # Coincidencia con el perfil social (Solo, Familia, Desahogo)
    if opcion_destino.get("perfil") == datos_usuario.get("perfil"):
        score += 0.4
    else:
        score += 0.2  # Coincidencia parcial por contingencia urbana
        
    # Coincidencia de viabilidad presupuestaria
    if datos_usuario.get("presupuesto") == "Cero Gastos":
        score += 0.3
    else:
        score += 0.1
        
    # Multiplicador predictivo basado en la efectividad biopsicosocial del nodo
    probabilidad_final = score * opcion_destino.get("peso_prediccion", 0.90)
    return min(probabilidad_final, 1.0)

@app.get("/")
async def index():
    return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    p = await request.json()
    m = str(p.get("modo", "")).upper()
    mente = str(p.get("mente", "aburrido")).lower()
    desahogo = str(p.get("desahogo", "")).lower()
    codigo_postal = str(p.get("zip", "33167"))
    
    # Simulación del Factor de Estancamiento (Sf) a partir del estado mental reportado
    stagnation_weights = {"agotado": 0.75, "estresado": 0.60, "aburrido": 0.90}
# ---------------------------------------------------------
# SIMULACIÓN DEL FACTOR DE ESTANCAMIENTO (Sf)
# ---------------------------------------------------------
stagnation_weights = {
    "agotado": 0.75,
    "estresado": 0.60,
    "aburrido": 0.90
}

sf = stagnation_weights.get(mente.lower(), 0.50)

# ---------------------------------------------------------
# 1. INTERVENCIÓN DOMÉSTICA (MODO CASA)
# ---------------------------------------------------------
if m == "CASA":
    misiones = (
        BASE_MISIONES["CASA"] +
        BASE_MISIONES["CASA_EXTRA"]
    )

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
        "stagnation_factor": sf,
        "misiones": misiones
    })

# ---------------------------------------------------------
# 2. ACCIÓN DE CAMPO (MODO SALIR)
# ---------------------------------------------------------
opciones_disponibles = BASE_MISIONES["SALIR"].get(
    mente.lower(),
    BASE_MISIONES["SALIR"]["aburrido"]
)

# Ejecutar algoritmo predictivo Big Tech
candidatos_puntuados = []

for opc in opciones_disponibles:
    p_clic = calcular_probabilidad_engache(p, opc)

    candidato = opc.copy()
    candidato["p_clic"] = p_clic
    candidatos_puntuados.append(candidato)

# Clasificación en tiempo real
candidatos_puntuados.sort(
    key=lambda x: x["p_clic"],
    reverse=True
)

# Destino ganador
info = candidatos_puntuados[0]

# ---------------------------------------------------------
# INTERCEPCIÓN CRÍTICA
# ---------------------------------------------------------
desahogo_lower = desahogo.lower()

if any(
    pal in desahogo_lower
    for pal in [
        "trabajo",
        "biles",
        "deudas",
        "dinero",
        "miseria",
        "explotacion"
    ]
):
    guia = (
        "DESTINO: Oficina de Reclutamiento Corporativo. "
        "QUÉ HACER: Entra con tu ID física, solicita entrevista "
        "inmediata de contingencia laboral. "
        "CUÁNDO: Ya. "
        "PARA QUÉ: Romper el ahogo financiero y recuperar "
        "el mando económico."
    )

    gps = "staffing+agencies"
    titulo_ganador = "ACTIVACIÓN ECONÓMICA EXPRESS"
    entorno_ganador = "Agencia Corporativa de Empleo"
    p_clic_final = 0.99

else:
    guia = (
        f"DESTINO: {info['titulo']}. "
        f"QUÉ HACER: {info['que_hacer']} "
        f"PARA QUÉ: {info['porque']}"
    )

    gps = info["gps"]
    titulo_ganador = info["titulo"].upper()
    entorno_ganador = info["donde"]
    p_clic_final = info["p_clic"]

# ---------------------------------------------------------
# RESPUESTA FINAL
# ---------------------------------------------------------
return JSONResponse({
    "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
    "stagnation_factor": sf,
    "probability_activation": p_clic_final,
    "algoritmo_origen": "Predictive_Dopamine_Loop_V4",
    "destino_titulo": titulo_ganador,
    "destino_entorno": entorno_ganador,
    "destino_instruccion": guia,
    "destino_coordenadas_gps":
        f"https://www.google.com/maps/search/?api=1&query={gps}+in+{codigo_postal}"
})

# ---------------------------------------------------------
# INICIO DEL SERVIDOR
# ---------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
