# ==========================================================================================
# OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Backend Core - Producción Blindada)
# Company: May Roga LLC - Version: 4.0.0 - Foco en Veteranos, Adultos y Gobierno
# Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
# ==========================================================================================
import re
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/perfiles-especiales")

# Matrices de Sintonizadores con Enfoque de Autocuidado y Alta Visibilidad
DATA_PERFILES = {
    "veterano": {
        "es": {
            "keywords": ["ANCLAJE", "TACTICA", "TERRITORIO", "DISCIPLINA", "HONOR", "SILENCIO PROTECTOR", "ENFOQUE", "PROPÓSITO", "FUERZA INTERNA", "PAUSA SERENA"],
            "misiones": [
                {"id": 901, "titulo": "OPERACIÓN ANCLAJE TERRITORIAL", "descripcion": "Establece tu posición actual de forma consciente. Camina diez pasos firmes sintiendo la solidez del suelo. Eres el guardián de tu propia paz en este espacio seguro.", "vector": {"movimiento": 85, "silencio": 95, "contemplacion": 90}},
                {"id": 902, "titulo": "ESTRATEGIA DEL VIENTO FRESCO", "descripcion": "Busca un espacio abierto al aire libre o acércate a una ventana amplia. Inhala la frescura del entorno durante cuatro tiempos exactos, sosteniendo tu fortaleza interna.", "vector": {"aire_fresco": 100, "naturaleza": 90, "descanso": 80}},
                {"id": 903, "titulo": "OPERACIÓN SILENCIO MENTAL", "descripcion": "Sienta tu cuerpo en una postura firme y erguida. Cierra los ojos por sesenta segundos y concéntrate únicamente en el eco de tu respiración profunda.", "vector": {"silencio": 100, "descanso": 80, "contemplacion": 90}},
                {"id": 904, "titulo": "PATRULLA DEL HORIZONTE VERDE", "descripcion": "Dirígete visualmente hacia el árbol o planta más cercana. Observa la rigidez de su tronco y la flexibilidad de sus hojas. Sincroniza tu ritmo con la quietud natural.", "vector": {"naturaleza": 95, "aire_fresco": 90, "movimiento": 50}}
            ]
        },
        "en": {
            "keywords": ["ANCHORING", "TACTICS", "TERRITORY", "DISCIPLINE", "HONOR", "PROTECTIVE SILENCE", "FOCUS", "PURPOSE", "INNER STRENGTH", "SERENE PAUSE"],
            "misiones": [
                {"id": 901, "titulo": "TERRITORIAL ANCHORING OPERATION", "descripcion": "Consciously establish your current position. Walk ten firm steps feeling the solidity of the ground. You are the guardian of your own peace in this safe space.", "vector": {"movimiento": 85, "silencio": 95, "contemplacion": 90}},
                {"id": 902, "titulo": "FRESH BREEZE STRATEGY", "descripcion": "Find an open space outdoors or approach a window. Inhale the freshness of the environment for four exact counts, sustaining your inner strength.", "vector": {"aire_fresco": 100, "naturaleza": 90, "descanso": 80}},
                {"id": 903, "titulo": "OPERATION MENTAL SILENCE", "descripcion": "Sit your body in a firm and upright posture. Close your eyes for sixty seconds and focus solely on the echo of your deep breath.", "vector": {"silencio": 100, "descanso": 80, "contemplacion": 90}},
                {"id": 904, "titulo": "GREEN HORIZON PATROL", "descripcion": "Visually direct yourself towards the nearest tree or plant. Observe the rigidity of its trunk and the flexibility of its leaves. Synchronize your rhythm with natural stillness.", "vector": {"naturaleza": 95, "aire_fresco": 90, "movimiento": 50}}
            ]
        }
    },
    "adulto_mayor": {
        "es": {
            "keywords": ["SABIDURÍA", "TRAYECTORIA", "CALMA", "PAZ FAMILIAR", "LEGADO VIVO", "TIEMPO SERENO", "RAÍCES", "BIENESTAR", "GRATITUD PLENA", "ASOMBRO SUTIL"],
            "misiones": [
                {"id": 911, "titulo": "RITUAL DE LA MIRADA LEJANA", "descripcion": "Toma asiento en un lugar cómodo con la espalda recta y relajada. Diríge tu mirada al punto más distante en el horizonte exterior, permitiendo que tus ojos descansen en total tranquilidad.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "SINTONÍA DE MANOS CONSECUENTES", "descripcion": "Frota suavemente las palmas de tus manos hasta percibir un agradable calor biológico. Colócalas sobre tus hombros regalándote un abrazo reconfortante cargado de agradecimiento.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 95}},
                {"id": 913, "titulo": "EL ECO DEL AGUA SERENA", "descripcion": "Sirve un vaso con agua fresca de forma muy pausada. Observa los reflejos de la luz en el líquido durante un minuto en absoluto silencio antes de tomar un sorbo lento y consciente.", "vector": {"agua": 100, "contemplacion": 90, "silencio": 85}},
                {"id": 914, "titulo": "COMPÁS DE MOVIMIENTO GENTIL", "descripcion": "Dibuja círculos muy suaves y lentos en el aire con tus muñecas y tobillos. Siente cómo la energía natural fluye libremente por tus articulaciones a tu propio ritmo.", "vector": {"movimiento": 70, "descanso": 80, "salud": 85}}
            ]
        },
        "en": {
            "keywords": ["WISDOM", "PATHWAY", "CALM", "FAMILY PEACE", "LIVING LEGACY", "SERENE TIME", "ROOTS", "WELLBEING", "FULL GRATITUDE", "SUBTLE WONDER"],
            "misiones": [
                {"id": 911, "titulo": "DISTANT GAZE RITUAL", "descripcion": "Take a seat in a comfortable spot with a straight, relaxed spine. Direct your gaze to the furthest point on the outer horizon, allowing your eyes to rest in total tranquility.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "MINDFUL HANDS HARMONY", "descripcion": "Gently rub the palms of your hands until you feel biological warmth. Place them on your shoulders giving yourself a comforting hug filled with gratitude.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 95}},
                {"id": 913, "titulo": "THE ECHO OF SERENE WATER", "descripcion": "Pour a glass of fresh water very slowly. Observe the reflections of light on the liquid for one minute in absolute silence before taking a slow, conscious sip.", "vector": {"agua": 100, "contemplacion": 90, "silencio": 85}},
                {"id": 914, "titulo": "GENTLE MOTION CADENCE", "descripcion": "Draw very soft and slow circles in the air with your wrists and ankles. Feel how natural energy flows freely through your joints at your own pace.", "vector": {"movimiento": 70, "descanso": 80, "salud": 85}}
            ]
        }
    },
    "gubernamental": {
        "es": {
            "keywords": ["DESCONEXIÓN", "ESTRUCTURA", "ORDEN VITAL", "PAUSA DE GESTIÓN", "CLARIDAD MENTAL", "ENFOQUE HUMANO", "HOMEOSTASIS", "SINTONÍA", "RESETEO", "EQUILIBRIO"],
            "misiones": [
                {"id": 921, "titulo": "DESFRAGMENTACIÓN DE BUCLE DIARIO", "descripcion": "Coloca tu pantalla hacia abajo en absoluto reposo. Dedica sesenta segundos a escuchar los sonidos ambientales más sutiles e imperceptibles de tu espacio físico actual.", "vector": {"silencio": 100, "organizacion": 85, "descanso": 90}},
                {"id": 922, "titulo": "MAPEO DE ESTABILIDAD SOMÁTICA", "descripcion": "Apoya ambos pies firmes sobre el piso en un ángulo recto perfecto. Siente cómo la estructura del suelo sostiene tu peso de manera gratuita, liberando la carga acumulada.", "vector": {"descanso": 95, "organizacion": 95, "contemplacion": 80}},
                {"id": 923, "titulo": "RESETEO DE ENFOQUE ÓPTICO", "descripcion": "Aparta tu mirada de cualquier documento o pantalla ahora mismo. Busca un objeto de color azul o verde a tu alrededor y observa sus detalles geométricos durante 30 segundos.", "vector": {"contemplacion": 95, "silencio": 90, "organizacion": 70}},
                {"id": 924, "titulo": "AISLAMIENTO DE CARGA INVISIBLE", "descripcion": "Endereza tu columna de forma recta y cómoda. Eleva tus hombros suavemente hacia tus orejas, retén la energía por tres segundos y déjalos caer de golpe, liberando la rutina.", "vector": {"movimiento": 85, "descanso": 90, "salud": 80}}
            ]
        },
        "en": {
            "keywords": ["DISCONNECT", "STRUCTURE", "VITAL ORDER", "MANAGEMENT PAUSE", "MENTAL CLARITY", "HUMAN FOCUS", "HOMEOSTASIS", "TUNING", "RESET", "EQUILIBRIUM"],
            "misiones": [
                {"id": 921, "titulo": "DAILY LOOP DEFRAGMENTATION", "descripcion": "Turn your screen face down into absolute rest. Spend sixty seconds listening to the most subtle and imperceptible ambient sounds of your current physical space.", "vector": {"silencio": 100, "organizacion": 85, "descanso": 90}},
                {"id": 922, "titulo": "SOMATIC STABILITY MAPPING", "descripcion": "Place both feet firmly on the floor at a perfect right angle. Feel how the structure of the ground supports your weight for free, releasing the built-up load.", "vector": {"descanso": 95, "organizacion": 95, "contemplacion": 80}},
                {"id": 923, "titulo": "OPTICAL FOCUS RESET", "descripcion": "Take your eyes off any document or screen right now. Look for a blue or green object around you and observe its geometric details for 30 seconds.", "vector": {"contemplacion": 95, "silencio": 90, "organizacion": 70}},
                {"id": 924, "titulo": "INVISIBLE LOAD ISOLATION", "descripcion": "Straighten your spine comfortably. Raise your shoulders gently toward your ears, hold for three seconds, and drop them suddenly, releasing the routine.", "vector": {"movimiento": 85, "descanso": 90, "salud": 80}}
            ]
        }
    }
}

# ==========================================================================================
# BLOQUE CORREGIDO: ESQUEMAS PYDANTIC Y ENDPOINTS DE CONFIGURACIÓN Y PROCESAMIENTO
# ==========================================================================================

class ProcesarInputSchema(BaseModel):
    perfil: str
    lang: str
    texto: str
    keywords_seleccionadas: List[str]
    contexto_pdf: Optional[str] = ""

class ReporteSchema(BaseModel):
    perfil: str
    lang: str
    recorrido: List[str]
    informacion_compartida: List[str]

@router.get("/config")
async def get_config(perfil: str, lang: str = "es"):
    p_lower = perfil.lower()
    if p_lower not in DATA_PERFILES:
        raise HTTPException(status_code=404, detail="Perfil no configurado.")
    l_lower = "en" if lang.lower() == "en" else "es"
    return JSONResponse(DATA_PERFILES[p_lower][l_lower])

@router.post("/procesar")
async def procesar_contexto(data: ProcesarInputSchema):
    p_lower = data.perfil.lower()
    if p_lower not in DATA_PERFILES:
        raise HTTPException(status_code=404, detail="Perfil inválido.")
    l_lower = "en" if data.lang.lower() == "en" else "es"
    config_perfil = DATA_PERFILES[p_lower][l_lower]
    
    # Enrutamiento inteligente y exclusivo de Google Maps Embebido para cada perfil
    QUERIES_MAPS = {
        "veterano": "quiet+nature+reserve+park",
        "adulto_mayor": "botanical+garden+walking+paths",
        "gubernamental": "open+scenic+viewpoint+nature"
    }
    q_maps = QUERIES_MAPS.get(p_lower, "quiet+nature+park")
    misiones_sugeridas = []
    
    for mision in config_perfil["misiones"]:
        misiones_sugeridas.append({
            "destino_id": mision["id"],
            "destino_titulo": mision["titulo"].upper(),
            "destino_titulo_en": mision["titulo"].upper(),
            "que_hacer": mision["descripcion"],
            "que_hacer_en": mision["descripcion"],
            "destino_entorno": f"ZONA DE CALMA {p_lower.upper()}",
            "destino_instruccion": mision["descripcion"],
            "destino_instruccion_en": mision["descripcion"],
            "destino_coordenadas_gps": f"google.com{q_maps}",
            "vector_entorno_seleccionado": mision["vector"],
            "enlace_youtube": "https://youtube.com",
            "enlace_spotify": "https://spotify.com"
        })
        
    calidez = {
        "es": f"Entorno especial activo para {p_lower.upper()}. Tu recorrido de desconexión interactiva y modulación de aire fresco ha comenzado. Sigue las pautas en pantalla.",
        "en": f"Special environment active for {p_lower.upper()}. Your interactive disconnection and fresh air modulation journey has begun. Follow the onscreen guidelines."
    }
    return JSONResponse({
        "status": "success",
        "calidez_humana": calidez[l_lower],
        "misiones": misiones_sugeridas,
        "forced_recovery": False
    })

@router.post("/reporte")
async def generar_reporte_bienestar(data: ReporteSchema):
    l_lower = "en" if data.lang.lower() == "en" else "es"
    p_lower = data.perfil.lower()
    
    perfil_es = {"veterano": "Veteranos de Guerra", "adulto_mayor": "Adultos Mayores", "gubernamental": "Trabajadores Públicos"}.get(p_lower, "Especial")
    perfil_en = {"veterano": "War Veterans", "adulto_mayor": "Senior Citizens", "gubernamental": "Public Servants"}.get(p_lower, "Special")
    
    if l_lower == "es":
        titulo = f"REPORTE DESCRIPTIVO DE ORIENTACIÓN Y BIENESTAR: PERFIL {perfil_es.upper()}"
        resumen = "Este documento recopila el recorrido voluntario de pausas conscientes y dinámicas de autocuidado realizadas por el participante dentro de la plataforma."
        observaciones = "Se sugiere continuar priorizando los espacios autónomos de desconexión digital, practicando pautas de respiración profunda en el hogar y actividades físicas ligeras en entornos naturales protectores para conservar el equilibrio vital cotidiano."
        nota = "Este reporte es un documento de uso privado, con fines informativos, educativos y de autocuidado individual. No posee validez legal, institucional, ni clínica."
    else:
        titulo = f"DESCRIPTIVE ORIENTATION AND WELLBEING REPORT: {perfil_en.upper()} PROFILE"
        resumen = "This document compiles the voluntary journey of conscious pauses and self-care dynamics executed by the participant within the platform."
        observaciones = "It is suggested to keep prioritizing autonomous digital disconnection intervals, practicing deep breathing guidelines at home, and engaging in light physical tasks within open spaces to support daily vital equilibrium."
        nota = "This report is strictly for private, informative, educational, and individual self-care purposes. It holds no legal, institutional, or clinical validity."
        
    return JSONResponse({
        "titulo": titulo,
        "resumen_descriptivo": resumen,
        "recorrido_realizado": data.recorrido if data.recorrido else ["Dinámicas de modulación de aire."],
        "actividades_sugeridas": [
            "Dinámicas de modulación de aire." if l_lower == "es" else "Air modulation dynamics."
        ],
        "observaciones_finales": observaciones,
        "nota_legal": nota
    })

# ==========================================================================================
# FUNCIONES AUXILIARES DE TRADUCCIÓN SEMÁNTICA INDEPENDIENTE (Final de perfiles_module.py)
# ==========================================================================================

def perfiles_nombre_es(p: str) -> str:
    return {"veterano": "Veteranos de Guerra", "adulto_mayor": "Adultos Mayores", "gubernamental": "Trabajadores Públicos"}.get(p, "Especial")

def perfiles_nombre_en(p: str) -> str:
    return {"veterano": "War Veterans", "adulto_mayor": "Senior Citizens", "gubernamental": "Public Servants"}.get(p, "Special")
