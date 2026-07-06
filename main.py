# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.3.5.0
# Company: May Roga LLC
# File: main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random

app = FastAPI()
if not os.path.exists("static"): os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
            {"titulo": "Sombra de árbol", "porque": "Mente frita por luz artificial.", "que_hacer": "Toca corteza de árbol, siente su textura. Quédate bajo sombra densa.", "donde": "Parque grande.", "gps": "parks+with+shade+"}
        ],
        "estresado": [
            {"titulo": "Resistencia de colina", "porque": "Cortisol bloqueando hombros.", "que_hacer": "Sube rampa o escalera a paso firme. Usa la gravedad para soltar tensión.", "donde": "Escalera pública.", "gps": "public+stairs+"}
        ],
        "aburrido": [
            {"titulo": "Colores urbanos", "porque": "Piloto automático gris.", "que_hacer": "Mira murales. Encuentra tres detalles pequeños. Asómbrate.", "donde": "Calle con murales.", "gps": "street+art+"}
        ]
    }
}
@app.get("/")
async def index(): return FileResponse('static/session.html')

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    p = await request.json()
    m = str(p.get("modo", "")).upper()
    mente = str(p.get("mente", "aburrido")).lower()
    desahogo = str(p.get("desahogo", "")).lower()
    
    if m == "CASA":
        misiones = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        return JSONResponse({"DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", "misiones": misiones})
    
    info = random.choice(BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"]))
    
    # Lógica de supervivencia
    if any(pal in desahogo for pal in ["trabajo", "biles", "deudas"]):
        guia = "DESTINO: Staffing. QUÉ HACER: Ve directo con ID. CUÁNDO: Ya. PARA QUÉ: Ganar dinero."
        gps = "staffing+agencies"
    else:
        guia = f"DESTINO: {info['titulo']}. QUÉ HACER: {info['que_hacer']} PARA QUÉ: {info['porque']}"
        gps = info["gps"]

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": info["titulo"].upper(),
        "destino_entorno": info["donde"],
        "destino_instruccion": guia,
        "destino_coordenadas_gps": f"https://www.google.com/maps/search/?api=1&query={gps}+in+{p.get('zip', '33167')}"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
