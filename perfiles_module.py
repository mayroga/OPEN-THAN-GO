# ==========================================================================================
# OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Backend Core - Edición Comercial v6.0)
# Company: May Roga LLC - Version: 6.0.0 - Control de Homeostasis de Alta Velocidad
# Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
# ==========================================================================================
import re
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/perfiles-especiales")

# Matrices de Sintonizadores de Alta Visibilidad y Misiones Contextuales Premium por Perfil
DATA_PERFILES = {
    "veterano": {
        "es": {
            "keywords": ["ANCLAJE", "TACTICA", "TERRITORIO", "DISCIPLINA", "HONOR", "SILENCIO PROTECTOR", "ENFOQUE", "PROPÓSITO", "FUERZA INTERNA", "PAUSA SERENA"],
            "misiones": [
                {"id": 901, "titulo": "OPERACIÓN ANCLAJE TERRITORIAL", "descripcion": "Establece tu posición actual de forma consciente. Camina de forma pausada diez pasos firmes sintiendo la solidez del suelo. Eres el guardián de tu propia paz en este rincón seguro.", "vector": {"movimiento": 85, "silencio": 95, "contemplacion": 90}},
                {"id": 902, "titulo": "ESTRATEGIA DEL VIENTO FRESCO", "descripcion": "Busca un espacio abierto al aire libre o acércate a una ventana amplia. Inhala la frescura del entorno durante cuatro tiempos exactos, sosteniendo tu fortaleza interna.", "vector": {"aire_fresco": 100, "naturaleza": 90, "descanso": 80}}
            ],
            "youtube_id": "4_Zcc9v7b8E"
        },
        "en": {
            "keywords": ["ANCHORING", "TACTICS", "TERRITORY", "DISCIPLINE", "HONOR", "PROTECTIVE SILENCE", "FOCUS", "PURPOSE", "INNER STRENGTH", "SERENE PAUSE"],
            "misiones": [
                {"id": 901, "titulo": "TERRITORIAL ANCHORING OPERATION", "descripcion": "Consciously establish your current position. Walk ten firm steps feeling the solidity of the ground. You are the guardian of your own peace in this safe space.", "vector": {"movimiento": 85, "silencio": 95, "contemplacion": 90}},
                {"id": 902, "titulo": "FRESH BREEZE STRATEGY", "descripcion": "Find an open space outdoors or approach a window. Inhale the freshness of the environment for four exact counts, sustaining your inner strength.", "vector": {"aire_fresco": 100, "naturaleza": 90, "descanso": 80}}
            ],
            "youtube_id": "4_Zcc9v7b8E"
        }
    },
    "adulto_mayor": {
        "es": {
            "keywords": ["SABIDURÍA", "TRAYECTORIA", "CALMA", "PAZ FAMILIAR", "LEGADO VIVO", "TIEMPO SERENO", "RAÍCES", "BIENESTAR", "GRATITUD PLENA", "ASOMBRO SUTIL"],
            "misiones": [
                {"id": 911, "titulo": "RITUAL DE LA MIRADA LEJANA", "descripcion": "Toma asiento en un lugar cómodo con la espalda recta y relajada. Diríge tu mirada al punto más distante en el horizonte exterior, permitiendo que tus ojos descansen en total tranquilidad.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "SINTONÍA DE MANOS CONSECUENTES", "descripcion": "Frota suavemente las palmas de tus manos hasta percibir un agradable calor biológico. Colócalas sobre tus hombros regalándote un abrazo reconfortante cargado de agradecimiento.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 95}}
            ],
            "youtube_id": "lE6RYpe9IT0"
        },
        "en": {
            "keywords": ["WISDOM", "PATHWAY", "CALM", "FAMILY PEACE", "LIVING LEGACY", "SERENE TIME", "ROOTS", "WELLBEING", "FULL GRATITUDE", "SUBTLE WONDER"],
            "misiones": [
                {"id": 911, "titulo": "DISTANT GAZE RITUAL", "descripcion": "Take a seat in a comfortable spot with a straight, relaxed spine. Direct your gaze to the furthest point on the outer horizon, allowing your eyes to rest in total tranquility.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "MINDFUL HANDS HARMONY", "descripcion": "Gently rub the palms of your hands until you feel biological warmth. Place them on your shoulders giving yourself a comforting hug filled with gratitude.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 95}}
            ],
            "youtube_id": "lE6RYpe9IT0"
        }
    },
    "gubernamental": {
        "es": {
            "keywords": ["DESCONEXIÓN", "ESTRUCTURA", "ORDEN VITAL", "PAUSA DE GESTIÓN", "CLARIDAD MENTAL", "ENFOQUE HUMANO", "HOMEOSTASIS", "SINTONÍA", "RESETEO", "EQUILIBRIO"],
            "misiones": [
                {"id": 921, "titulo": "DESFRAGMENTACIÓN DE BUCLE DIARIO", "descripcion": "Coloca tu pantalla hacia abajo en absoluto reposo. Dedica sesenta segundos a escuchar los sonidos ambientales más sutiles e imperceptibles de tu espacio físico actual.", "vector": {"silencio": 100, "organizacion": 85, "descanso": 90}},
                {"id": 922, "titulo": "MAPEO DE ESTABILIDAD SOMÁTICA", "descripcion": "Apoya ambos pies firmes sobre el piso en un ángulo recto perfecto. Siente cómo la estructura del suelo sostiene tu peso de manera gratuita, liberando la carga acumulada.", "vector": {"descanso": 95, "organizacion": 95, "contemplacion": 80}}
            ],
            "youtube_id": "wjX9f5J3zHk"
        },
        "en": {
            "keywords": ["DISCONNECT", "STRUCTURE", "VITAL ORDER", "MANAGEMENT PAUSE", "MENTAL CLARITY", "HUMAN FOCUS", "HOMEOSTASIS", "TUNING", "RESET", "EQUILIBRIUM"],
            "misiones": [
                {"id": 921, "titulo": "DAILY LOOP DEFRAGMENTATION", "descripcion": "Turn your screen face down into absolute rest. Spend sixty seconds listening to the most subtle and imperceptible ambient sounds of your current physical space.", "vector": {"silencio": 100, "organizacion": 85, "descanso": 90}},
                {"id": 922, "titulo": "SOMATIC STABILITY MAPPING", "descripcion": "Place both feet firmly on the floor at a perfect right angle. Feel how the structure of the ground supports your weight for free, releasing the built-up load.", "vector": {"descanso": 95, "organizacion": 95, "contemplacion": 80}}
            ],
            "youtube_id": "wjX9f5J3zHk"
        }
    }
}

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
    
    # Enrutamiento geográfico enfocado a parajes de naturaleza protectora
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
            "destino_entorno": f"ZONA DE HOMEOCINESIS PARA {p_lower.upper()}",
            "destino_instruccion": mision["descripcion"],
            "destino_instruccion_en": mision["descripcion"],
            # Enrutamiento nativo limpio en Iframe embebido oficial sin requerir API key
            "destino_coordenadas_gps": f"https://google.com{q_maps}&t=&z=14&ie=UTF8&iwloc=&output=embed",
            "vector_entorno_seleccionado": mision["vector"],
            "enlace_youtube": f"https://youtube.com{config_perfil['youtube_id']}?autoplay=1&mute=0",
            "enlace_spotify": "https://spotify.com"
        })
    
    # Banco de Frases Exclusivas para interceptar la Mesa de Relojes Doméstica de 15 Minutos (900s)
    FRASES_CASA = {
        "veterano": {
            "antes": "Establece tu posición actual de anclaje, soldado de tu propia paz. Coloca tu cuerpo firme e inhala profundamente para iniciar el ciclo biológico de quince minutos.",
            "despues": "Misión completada con éxito. Has mantenido tu posición y modulado tu ritmo respiratorio. Tu entorno interior se encuentra seguro y en equilibrio."
        },
        "adulto_mayor": {
            "antes": "Acomoda tu cuerpo en un espacio lleno de calma. Respira con lentitud, sintiendo la paz de este momento. Vamos a iniciar el círculo elástico a tu propio ritmo biológico.",
            "despues": "Ciclo completado con total serenidad. Tu pulso y tu respiración se encuentran en armonía. Siente la calidez del descanso recorriendo tu cuerpo de forma gentil."
        },
        "gubernamental": {
            "antes": "Pausa de gestión obligatoria activada. Apaga las alertas mentales de la rutina de oficina. Pon tus pies firmes en el suelo e inicia el reseteo somático de quince minutos.",
            "despues": "Bucle diario desfragmentado de forma eficiente. Has liberado la carga invisible acumulada en tu jornada. Recupera tu enfoque con una mente despejada."
        }
    }
    
    calidez = {
        "es": f"Entorno especial activo para {p_lower.upper()}. Tu recorrido de desconexión interactiva y modulación de aire fresco de 15 minutos ha comenzado. Sigue las pautas en pantalla.",
        "en": f"Special environment active for {p_lower.upper()}. Your interactive disconnection and fresh air modulation journey has begun. Follow the onscreen guidelines."
    }
    
    return JSONResponse({
        "status": "success",
        "calidez_humana": calidez[l_lower],
        "misiones": misiones_sugeridas,
        "forced_recovery": False,
        "frases_respiracion": FRASES_CASA.get(p_lower, {"antes": "Inicia tu pausa.", "despues": "Pausa concluida."})
    })

@router.post("/reporte")
async def generar_reporte_bienestar(data: ReporteSchema):
    l_lower = "en" if data.lang.lower() == "en" else "es"
    p_lower = data.perfil.lower()
    
    perfil_es = {"veterano": "Veteranos de Guerra", "adulto_mayor": "Adultos Mayores", "gubernamental": "Trabajadores Públicos"}.get(p_lower, "Especial")
    perfil_en = {"veterano": "War Veterans", "adulto_mayor": "Senior Citizens", "gubernamental": "Public Servants"}.get(p_lower, "Special")
    
    # Sanitización de strings informativos del buffer para el resumen
    inputs_limpios = [item for item in data.informacion_compartida if "Variables" not in item and "analizado" not in item]
    sintonizadores_txt = ", ".join(inputs_limpios) if inputs_limpios else "Modulación general activa"
    
    if l_lower == "es":
        titulo = f"REPORTE DESCRIPTIVO DE ORIENTACIÓN Y BIENESTAR: PORTAL {perfil_es.upper()}"
        resumen = f"Este documento recopila el recorrido voluntario de pausas conscientes y dinámicas de autocuidado realizadas por el participante dentro de la plataforma. Se procesaron los siguientes sintonizadores bio-ambientales compartidos de forma autónoma: [{sintonizadores_txt}]."
        observaciones = "VALORACIÓN COMERCIAL DE BIENESTAR: Se sugiere continuar priorizando los espacios autónomos de desconexión digital e intervalos de aislamiento de carga invisible en el hogar. Se recomienda de forma preventiva mantener pautas regulares de respiración profunda en un rincón seguro y actividades físicas ligeras en entornos naturales protectores para conservar el equilibrio vital cotidiano."
        nota = "Este reporte es un documento de uso privado, con fines informativos, educativos y de autocuidado individual. No posee validez legal, institucional, gubernamental ni clínica."
    else:
        titulo = f"DESCRIPTIVE ORIENTATION AND WELLBEING REPORT: {perfil_en.upper()} PORTAL"
        resumen = f"This document compiles the voluntary journey of conscious pauses and self-care dynamics executed by the participant within the platform. The following bio-environmental tuners were autonomously shared: [{sintonizadores_txt}]."
        observaciones = "COMMERCIAL WELLBEING ASSESSMENT: It is suggested to keep prioritizing autonomous digital disconnection intervals and invisible load isolation spaces at home. It is preventatively recommended to practice regular deep breathing guidelines in a safe corner and engage in light physical tasks within open natural spaces to support daily vital equilibrium."
        nota = "This report is strictly for private, informative, educational, and individual self-care purposes. It holds no legal, institutional, governmental, or clinical validity."

    return JSONResponse({
        "titulo": titulo,
        "resumen_descriptivo": resumen,
        "recorrido_realizado": data.recorrido if data.recorrido else ["Ciclo doméstico de respiración elástica de 15 minutos."],
        "observaciones_finales": observaciones,
        "nota_legal": nota
    })
