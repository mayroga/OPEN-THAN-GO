# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.5.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 3 (NÚCLEO Y MITAD MISIONES CASA)

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

# Diccionario Estructural Absoluto de la Infraestructura Biopsicosocial
BASE_MISIONES = {
    "CASA": [
        {"id": 1, "titulo": "Corta el piloto automático.", "descripcion": "Siente tus pies en el suelo. Respira hondo. Estás vivo."},
        {"id": 2, "titulo": "Desconexión de biles.", "descripcion": "El piso sostiene tu peso gratis. Suelta tus hombros."},
        {"id": 3, "titulo": "Aislamiento de pantalla.", "descripcion": "Voltea el teléfono boca abajo. Mira el techo 30 segundos."},
        {"id": 4, "titulo": "Soltar la carga.", "descripcion": "Deja caer la mochila de deudas. Hombros libres ahora."},
        {"id": 5, "titulo": "El reset del agua.", "descripcion": "Bebe un trago de agua fría. Siente el líquido entrar."},
        {"id": 6, "titulo": "Liberación de nudos.", "descripcion": "Aprieta puños 3 segundos. Abre de golpe. Suelta todo."},
        {"id": 7, "titulo": "El aire de la calle.", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara."},
        {"id": 8, "titulo": "Rotación de energía.", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo hoy."},
        {"id": 9, "titulo": "Anclaje del presente.", "descripcion": "Cierra los ojos. Di una sola cosa buena fuerte."},
        {"id": 10, "titulo": "Orden de tu espacio.", "descripcion": "Alinea tres objetos de tu mesa. Orden dentro ahora."},
        {"id": 11, "titulo": "Pies en la tierra.", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente frío."},
        {"id": 12, "titulo": "Estiramiento al cielo.", "descripcion": "Brazos arriba. Toca el techo. Mantén. Suelta de golpe."},
        {"id": 13, "titulo": "Foco en lo olvidado.", "descripcion": "Elige una tarea mínima ignorada. Hazla ahora mismo."},
        {"id": 14, "titulo": "Columna recta.", "descripcion": "Endereza la espalda. Respira profundo desde el abdomen."},
        {"id": 15, "titulo": "Contacto frío.", "descripcion": "Toca una superficie fría. Siente la temperatura real."},
        {"id": 16, "titulo": "Ventilación total.", "descripcion": "Abre la puerta principal. Deja entrar el aire nuevo."},
        {"id": 17, "titulo": "Sacudida de estrés.", "descripcion": "Sacude manos y piernas como quitándote agua 10 segundos."},
        {"id": 18, "titulo": "Mirada lejana.", "descripcion": "Mira el objeto más lejano por la ventana. Descansa."},
        {"id": 19, "titulo": "Memoria feliz.", "descripcion": "Cierra los ojos. Recuerda un momento libre de la niñez."},
        {"id": 20, "titulo": "Sonrisa forzada.", "descripcion": "Sonríe 15 segundos seguidos. Cambia tu química mental."},
        {"id": 21, "titulo": "Agradecimiento.", "descripcion": "Cierra los ojos. Piensa una cosa buena de esta semana."},
        {"id": 22, "titulo": "Relaja ojos.", "descripcion": "Tápate los ojos con palmas templadas un minuto."},
        {"id": 23, "titulo": "Ritmo cardíaco.", "descripcion": "Mano derecha en el pecho. Siente tu motor vivo."},
        {"id": 24, "titulo": "Suelta cuello.", "descripcion": "Círculos lentos de cabeza. Libera peso de la pantalla."},
        {"id": 25, "titulo": "Ejercicio de palmas.", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros."}
    ],
# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.5.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 2 DE 3 (MISIONES EXTRA Y FILTROS DE CAMPO)

    "CASA_EXTRA": [
        {"id": 26, "titulo": "Sonidos lejanos.", "descripcion": "Identifica el sonido más lejano fuera de casa."},
        {"id": 27, "titulo": "Estiramiento lateral.", "descripcion": "Inclina el cuerpo suavemente a cada lado."},
        {"id": 28, "titulo": "El vaso vacío.", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto."},
        {"id": 29, "titulo": "Suelta mandíbula.", "descripcion": "Abre grande la boca, mueve mandíbula a los lados."},
        {"id": 30, "titulo": "Pasos lentos.", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto."},
        {"id": 31, "titulo": "Masaje suave.", "descripcion": "Yemas en las sienes. Círculos muy lentos."},
        {"id": 32, "titulo": "Conciencia aire.", "descripcion": "Siente el aire frío entrar, el cálido salir."},
        {"id": 33, "titulo": "Espalda firme.", "descripcion": "Omóplatos atrás, abre el pecho."},
        {"id": 34, "titulo": "Apoyo total.", "descripcion": "Siente la silla sosteniendo tu peso total."},
        {"id": 35, "titulo": "Cuenta atrás.", "descripcion": "Del 20 al 1. Despacio. Calma el ruido."},
        {"id": 36, "titulo": "Toca textura.", "descripcion": "Pasa dedos por una textura real. Madera o tela."},
        {"id": 37, "titulo": "Estira dedos.", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta."},
        {"id": 38, "titulo": "Sonido interno.", "descripcion": "Escucha tu respiración. No la fuerces."},
        {"id": 39, "titulo": "Mirada fija.", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear."},
        {"id": 40, "titulo": "Suelta brazos.", "descripcion": "Cuelga brazos. Sacúdelos suavemente."},
        {"id": 41, "titulo": "Contacto ropa.", "descripcion": "Nota el peso de la ropa sobre tu piel."},
        {"id": 42, "titulo": "Aire profundo.", "descripcion": "Infla vientre, retén 3 segundos, suelta lento."},
        {"id": 43, "titulo": "Rotación hombros.", "descripcion": "Hombros a orejas, cae de golpe."},
        {"id": 44, "titulo": "Escucha silencio.", "descripcion": "Busca el silencio entre respiraciones."},
        {"id": 45, "titulo": "Mirada techo.", "descripcion": "Mira techo. Estira cuello sin mover hombros."},
        {"id": 46, "titulo": "Siente base.", "descripcion": "Contacto firme de piernas con silla."},
        {"id": 47, "titulo": "Puños firmes.", "descripcion": "Puños con fuerza 3 segundos, abre rápido."},
        {"id": 48, "titulo": "Limpieza mental.", "descripcion": "Exhala preocupación aburrida. Fuera de ti."},
        {"id": 49, "titulo": "Toca mesa.", "descripcion": "Palmas en mesa. Nota la estabilidad."},
        {"id": 50, "titulo": "Presencia total.", "descripcion": "Estás aquí. Estás a salvo. Tienes el control."}
    ],
    "SALIR": {
        "agotado": [
            {"titulo": "Sombra de árbol.", "porque": "Mente frita por luz artificial.", "que_hacer": "Toca la corteza. Quédate bajo la sombra.", "donde": "Parque grande.", "gps": "parks+with+shade+", "peso_algoritmo": 0.95}
        ],
        "estresado": [
            {"titulo": "Resistencia de colina.", "porque": "Cortisol bloqueando tus hombros.", "que_hacer": "Sube rampas o escaleras a paso firme.", "donde": "Escalera pública.", "gps": "public+stairs+", "peso_algoritmo": 0.98}
        ],
        "aburrido": [
            {"titulo": "Colores urbanos.", "porque": "Tu rutina se volvió gris.", "que_hacer": "Mira murales en silencio. Encuentra detalles ocultos.", "donde": "Calle con arte urbano.", "gps": "street+art+", "peso_algoritmo": 0.93}
        ]
    }
}

# Canales multimedia libres y de uso satelital que secuestramos de forma directa
BIG_TECH_RESOURCES = {
    "naturaleza_audio": "https://spotify.com",
    "frecuencia_cerebral": "https://youtube.com",
    "caminata_guia": "https://google.com+",
    "staffing_directo": "https://google.com+"
}
# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.5.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 3 DE 3 (ENDPOINT MAESTRO Y UVICORN)

@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    p = await request.json()
    m = str(p.get("modo", "")).upper()
    mente = str(p.get("mente", "aburrido")).lower()
    desahogo = str(p.get("desahogo", "")).lower()
    lang = str(p.get("lang", "es")).lower()
    zip_code = str(p.get("zip", "")).strip()
    
    # FÓRMULA GEOGRÁFICA UNIVERSAL: Asume el ZIP ingresado, si está vacío apunta a todo USA
    anclaje_geo = zip_code if zip_code else "United+States"

    if m == "CASA":
        misiones_completas = BASE_MISIONES["CASA"] + BASE_MISIONES["CASA_EXTRA"]
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA", 
            "misiones": misiones_completas
        })

    # ALGORITMO DE ROTACIÓN ANTIPREDECIBLE: Elección cruzada de canales para romper la monotonía
    canales_disponibles = ["SPOTIFY", "YOUTUBE", "MAPS"]
    canal_elegido = random.choice(canales_disponibles)

    # El detector intercepta el bucle de adicción de consumo de USA
    bucle_consumo = ["amazon", "walmart", "costco", "fresco", "tienda", "comprar", "biles", "deudas", "dinero", "miseria", "explotacion"]
    
    if any(pal in desahogo for pal in bucle_consumo):
        # Si la mente sufre por compras o deudas, se desvía a Spotify o a buscar empleo en Maps
        if canal_elegido == "SPOTIFY":
            titulo = "RESET AUDITIVO" if lang == "es" else "AUDIO RESET"
            guia = "DESTINO: Spotify Gratis.\nACCION: Escucha el audio de choque.\nOBJETIVO: Frenar la ansiedad de comprar." if lang == "es" else "TARGET: Free Spotify.\nDO: Listen to the shock audio.\nGOAL: Stop the urge to buy."
            link_final = BIG_TECH_RESOURCES["frecuencia_cerebral"] if random.choice([True, False]) else BIG_TECH_RESOURCES["naturaleza_audio"]
        else:
            titulo = "ACTIVACIÓN ECONÓMICA" if lang == "es" else "ECONOMIC ACTION"
            guia = "DESTINO: Google Maps.\nACCION: Ve con tu identificación física.\nOBJETIVO: Conseguir empleo ya." if lang == "es" else "TARGET: Google Maps.\nDO: Go out with your physical ID.\nGOAL: Get a quick job now."
            link_final = f"{BIG_TECH_RESOURCES['staffing_directo']}{anclaje_geo}"
    else:
        # Rutas de campo estándar mutables sin repetir patrones monótonos
        opciones_salir = BASE_MISIONES["SALIR"].get(mente, BASE_MISIONES["SALIR"]["aburrido"])
        
        # El algoritmo predictivo evalúa pesos antes del despacho final
        candidatos = []
        for opc in opciones_salir:
            score = 0.5
            if p.get("budget") == "0": score += 0.2
            if p.get("perfil") == "solo": score += 0.2
            prob_final = score * opc.get("peso_algoritmo", 0.90)
            c = opc.copy()
            c["p_clic"] = min(prob_final, 1.0)
            candidatos.append(c)
            
        candidatos.sort(key=lambda x: x["p_clic"], reverse=True)
        info = candidatos[0]

        if canal_elegido == "YOUTUBE":
            titulo = "SHOCK VISUAL" if lang == "es" else "VISUAL SHOCK"
            guia = "DESTINO: YouTube.\nACCION: Pon el video en pantalla completa.\nOBJETIVO: Romper el bucle gris de tu mente." if lang == "es" else "TARGET: YouTube.\nDO: Play full screen video.\nGOAL: Break your mind's gray loop."
            link_final = BIG_TECH_RESOURCES["frecuencia_cerebral"]
        elif canal_elegido == "SPOTIFY":
            titulo = "FRECUENCIA TERAPÉUTICA" if lang == "es" else "THERAPEUTIC FREQUENCY"
            guia = "DESTINO: Spotify.\nACCION: Cierra los ojos y escucha.\nOBJETIVO: Apagar el ruido del día." if lang == "es" else "TARGET: Spotify.\nDO: Close your eyes and listen.\nGOAL: Turn off daily noise."
            link_final = BIG_TECH_RESOURCES["naturaleza_audio"]
        else:
            titulo = "ESCAPE DE CAMPO" if lang == "es" else "FIELD ESCAPE"
            guia = f"DESTINO: {info['donde']}.\nQUÉ HACER: {info['que_hacer']}\nPARA QUÉ: {info['porque']}" if lang == "es" else f"TARGET: {info['donde']}.\nDO: {info['que_hacer']}\nWHY: Reset your focus."
            link_final = f"https://google.com{info['gps']}+in+{anclaje_geo}"

    # Limpieza final del enlace satelital URL antes del despacho
    link_final_formateado = link_final.replace(" ", "+")

    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "destino_titulo": titulo,
        "destino_entorno": "Infraestructura Big Tech Secuestrada",
        "destino_instruccion": guia,
        "destino_coordenadas_gps": link_final_formateado
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
