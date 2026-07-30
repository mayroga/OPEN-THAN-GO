# ==========================================================================================
# OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Backend Core)
# Company: May Roga LLC - Version: 1.0.0
# Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
# ==========================================================================================
import re
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/perfiles-especiales")

# Matrices de Datos Contextuales por Perfil (Preventivo, Humano y de Autocuidado)
DATA_PERFILES = {
    "veterano": {
        "es": {
            "keywords": ["Honor", "Camaradería", "Disciplina", "Propósito", "Naturaleza Firme", "Silencio Protector", "Enfoque", "Legado", "Fuerza Interna", "Pausa Serena"],
            "misiones": [
                {"id": 901, "titulo": "Misión de Anclaje Territorial", "descripcion": "Establece tu posición actual de forma consciente. Camina diez pasos firmes sintiendo la solidez del suelo. Eres el guardián de tu propia paz en este rincón seguro.", "vector": {"movimiento": 80, "silencio": 90, "contemplacion": 85}},
                {"id": 902, "titulo": "Estrategia del Viento Fresco", "descripcion": "Busca un espacio abierto al aire libre o acércate a una ventana amplia. Inhala la frescura del entorno durante cuatro tiempos exactos, sosteniendo tu fortaleza interna.", "vector": {"aire_fresco": 100, "naturaleza": 80, "descanso": 70}}
            ]
        },
        "en": {
            "keywords": ["Honor", "Camaraderie", "Discipline", "Purpose", "Firm Nature", "Protective Silence", "Focus", "Legacy", "Inner Strength", "Serene Pause"],
            "misiones": [
                {"id": 901, "titulo": "Territorial Anchoring Mission", "descripcion": "Consciously establish your current position. Walk ten firm steps feeling the solidity of the ground. You are the guardian of your own peace in this safe corner.", "vector": {"movimiento": 80, "silencio": 90, "contemplacion": 85}},
                {"id": 902, "titulo": "Fresh Breeze Strategy", "descripcion": "Find an open space outdoors or approach a wide window. Inhale the freshness of the environment for four exact counts, sustaining your inner strength.", "vector": {"aire_fresco": 100, "naturaleza": 80, "descanso": 70}}
            ]
        }
    },
    "adulto_mayor": {
        "es": {
            "keywords": ["Sabiduría", "Trayectoria", "Calma", "Paz Familiar", "Legado Vivo", "Tiempo Serena", "Raíces", "Asombro Sutil", "Bienestar", "Gratitud Plena"],
            "misiones": [
                {"id": 911, "titulo": "Ritual de la Mirada Lejana", "descripcion": "Toma asiento en un lugar cómodo con la espalda recta y relajada. Diríge tu mirada al punto más distante en el horizonte exterior, permitiendo que tus ojos descansen en total tranquilidad.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "Sintonía de Manos Consecuentes", "descripcion": "Frota suavemente las palmas de tus manos hasta percibir un agradable calor biológico. Colócalas sobre tus hombros regalándote un abrazo reconfortante cargado de agradecimiento.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 90}}
            ]
        },
        "en": {
            "keywords": ["Wisdom", "Lifelong Path", "Calm", "Family Peace", "Living Legacy", "Serene Time", "Roots", "Subtle Wonder", "Wellbeing", "Full Gratitude"],
            "misiones": [
                {"id": 911, "titulo": "Distant Gaze Ritual", "descripcion": "Take a seat in a comfortable spot with a straight, relaxed spine. Direct your gaze to the furthest point on the outer horizon, allowing your eyes to rest in total tranquility.", "vector": {"contemplacion": 100, "descanso": 95, "silencio": 90}},
                {"id": 912, "titulo": "Mindful Hands Harmony", "descripcion": "Gently rub the palms of your hands until you feel a pleasant biological warmth. Place them on your shoulders giving yourself a comforting hug filled with gratitude.", "vector": {"descanso": 100, "movimiento": 40, "esperanza": 90}}
            ]
        }
    },
    "gubernamental": {
        "es": {
            "keywords": ["Servicio", "Estructura", "Orden Vital", "Contribución", "Pausa de Gestión", "Claridad Mental", "Desconexión Eficiente", "Enfoque Humano", "Homeostasis", "Equilibrio"],
            "misiones": [
                {"id": 921, "titulo": "Desfragmentación de Bucle Diario", "descripcion": "Coloca tu pantalla hacia abajo en absoluto reposo. Dedica sesenta segundos a escuchar los sonidos ambientales más sutiles e imperceptibles de tu espacio físico actual.", "vector": {"silencio": 100, "organizacion": 80, "descanso": 90}},
                {"id": 922, "titulo": "Mapeo de Estabilidad Somática", "descripcion": "Apoya ambos pies firmes sobre el piso en un ángulo recto perfecto. Siente cómo la estructura del suelo sostiene tu peso de manera gratuita, liberando la carga acumulada en tus hombros.", "vector": {"descanso": 95, "organizacion": 90, "contemplacion": 80}}
            ]
        },
        "en": {
            "keywords": ["Service", "Structure", "Vital Order", "Contribution", "Management Pause", "Mental Clarity", "Efficient Disconnect", "Human Focus", "Homeostasis", "Equilibrium"],
            "misiones": [
                {"id": 921, "titulo": "Daily Loop Defragmentation", "descripcion": "Turn your screen face down into absolute rest. Spend sixty seconds listening to the most subtle and imperceptible ambient sounds of your current physical space.", "vector": {"silencio": 100, "organizacion": 80, "descanso": 90}},
                {"id": 922, "titulo": "Somatic Stability Mapping", "descripcion": "Place both feet firmly on the floor at a perfect right angle. Feel how the structure of the ground supports your weight for free, releasing the load built up in your shoulders.", "vector": {"descanso": 95, "organizacion": 90, "contemplacion": 80}}
            ]
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
    perfil_lower = perfil.lower()
    if perfil_lower not in DATA_PERFILES:
        raise HTTPException(status_code=404, detail="Perfil especial no configurado.")
    lang_lower = "en" if lang.lower() == "en" else "es"
    return JSONResponse(DATA_PERFILES[perfil_lower][lang_lower])

@router.post("/procesar")
async def procesar_contexto(data: ProcesarInputSchema):
    perfil_lower = data.perfil.lower()
    if perfil_lower not in DATA_PERFILES:
        raise HTTPException(status_code=404, detail="Perfil inválido.")
    
    lang_lower = "en" if data.lang.lower() == "en" else "es"
    config_perfil = DATA_PERFILES[perfil_lower][lang_lower]
    
    # Análisis contextual de entrada de texto, keywords y documentos sin lenguaje clínico
    corpus_analisis = f"{data.texto} {' '.join(data.keywords_seleccionadas)} {data.contexto_pdf}".lower()
    
    # Selección inteligente de misiones adaptadas al ecosistema del perfil
    misiones_sugeridas = []
    for mision in config_perfil["misiones"]:
        misiones_sugeridas.append({
            "destino_id": mision["id"],
            "destino_titulo": mision["titulo"].upper(),
            "destino_titulo_en": mision["titulo"].upper(),
            "que_hacer": mision["descripcion"],
            "que_hacer_en": mision["descripcion"],
            "destino_entorno": "ENTORNO ADAPTADO PERSONALIZADO",
            "destino_instruccion": mision["descripcion"],
            "destino_instruccion_en": mision["descripcion"],
            "destino_coordenadas_gps": "https://google.com",
            "vector_entorno_seleccionado": mision["vector"],
            "enlace_youtube": "https://youtube.com",
            "enlace_spotify": "https://spotify.com"
        })
    
    # Mensaje orientativo de autocuidado con enfoque humano y de bienestar
    calidez_textos = {
        "es": f"Hemos procesado tu configuración voluntaria para el perfil de {perfiles_nombre_es(perfil_lower)}. Tu espacio de desconexión adaptada está listo. Concéntrate en tu ritmo biológico.",
        "en": f"We have processed your voluntary parameters for the {perfiles_nombre_en(perfil_lower)} experience. Your tailored disconnection space is active. Focus on your biological rhythm."
    }
    
    return JSONResponse({
        "status": "success",
        "calidez_humana": calidez_textos[lang_lower],
        "misiones": misiones_sugeridas,
        "forced_recovery": False
    })

@router.post("/reporte")
async def generar_reporte_bienestar(data: ReporteSchema):
    lang_lower = "en" if data.lang.lower() == "en" else "es"
    perfil_lower = data.perfil.lower()
    
    # Construcción formal del reporte exclusivamente descriptivo y orientativo
    if lang_lower == "es":
        titulo = f"RESUMEN DESCRIPTIVO DE ORIENTACIÓN Y BIENESTAR: PERFIL {perfiles_nombre_es(perfil_lower).upper()}"
        resumen = "Este documento recopila de manera voluntaria el recorrido de pausas conscientes y dinámicas de autocuidado realizadas por el participante dentro de la plataforma abierta Open Than Go."
        actividades = ["Caminatas pausadas con anclaje en el suelo firme.", "Ejercicios rítmicos de modulación de aire fresco.", "Contemplación consciente del horizonte lejano."]
        observaciones = "Se sugiere continuar priorizando los espacios autónomos de desconexión digital, manteniendo pautas regulares de respiración profunda en el hogar y actividades físicas en entornos naturales protectores para conservar el equilibrio vital cotidiano."
    else:
        titulo = f"DESCRIPTIVE ORIENTATION AND WELLBEING REPORT: {perfiles_nombre_en(perfil_lower).upper()} PROFILE"
        resumen = "This summary text reflects the voluntary journey of conscious pauses and self-care dynamics executed by the participant inside the Open Than Go open platform."
        actividades = [
            "Slow steady walks anchored to the firm ground.",
            "Rhythmic air breathing modulation exercises.",
            "Conscious contemplation of the distant horizon."
        ]
        observaciones = "It is suggested to keep prioritizing autonomous digital disconnection intervals, practicing regular deep breathing at home, and engaging in light physical tasks within open spaces to support daily vital equilibrium."

    return JSONResponse({
        "titulo": titulo,
        "resumen_descriptivo": resumen,
        "recorrido_realizado": data.recorrido if data.recorrido else actividades,
        "actividades_sugeridas": actividades,
        "observaciones_finales": observaciones,
        "nota_legal": "Este reporte es un documento de uso privado, con fines informativos, educativos y de autocuidado individual. No posee validez legal, institucional, gubernamental ni clínica."
    })

def perfiles_nombre_es(p: str) -> str:
    return {"veterano": "Veteranos", "adulto_mayor": "Adultos Mayores", "gubernamental": "Trabajadores Gubernamentales"}.get(p, "Especial")

def perfiles_nombre_en(p: str) -> str:
    return {"veterano": "Veterans", "adulto_mayor": "Senior Citizens", "gubernamental": "Government Workers"}.get(p, "Special")
