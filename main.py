# OPEN THAN GO SYSTEM - Contextual Wellbeing Routing Engine (CWRE) V.7.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 1 DE 2 (Backend Core)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import random
import re
from datetime import datetime
import urllib.parse

app = FastAPI()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# NUEVOS ESTADOS EMOCIONALES CATALOGO (FASE 1)
EMOTIONAL_STATES_CATALOG = [
    "agotado", "cansado", "stand by", "aburrido", "monotonia", "atrapado", "rutina",
    "estresado", "desesperado", "ansioso", "alterado", "sin direccion", "sin saber que hacer",
    "paralizado", "perdido", "sin ideas", "deprimido", "aislado", "enganado", "traicionado",
    "infeliz", "desafortunado", "descontento", "enamorado", "contento", "feliz", "afortunado"
]

# EXPANDED DEFAULT NECESSITY VECTOR (FASE 2)
DEFAULT_NECESSITY_VECTOR = {
    # Existing core needs
    "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
    "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
    "juego": 50, "contemplacion": 50, "descanso": 50, "organizacion": 50,
    "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
    "indicador_ansiedad": 0,
    # New Biological/Psychophysiological Needs (FASE 2)
    "orinar": 50, "defecar": 50, "sudar": 50, "espirar_co2": 50, "llorar_lubricar": 50,
    "desc_epidemica": 50, "escupir_tragar": 50, "vomito_eructo": 50, "oxigenacion": 50,
    "hidratacion_celular": 50, "nutricion_real": 50, "sueno_rem_nrem": 50,
    "pausas_silencio": 50, "homeostasis_termica": 50, "sensorial_organica": 50,
    "motilidad_linfatica": 50,
    # Needs related to FASE 4 diagnosis
    "soc_desconexion": 0, "soc_aislamiento": 0, "ext_vacio_existencial": 0, "ext_estancamiento": 0,
    "fis_sobrecarga_cortisol": 0, "sis_nervioso_saturado": 0, "fis_desconexion_presencia": 0,
    "soc_automatismo_masa": 0, "soc_validacion_rapida": 0, "comercio_compulsivo": 0,
    "ext_espejismo_evasion": 0, "ext_distraccion_cognitiva": 0,
}

# FASE 3: Mapeo Parásito de Infraestructura de USA (conceptual, para parsing de texto)
INFRASTRUCTURE_KEYWORDS_MAPPING = {
    "digital_platform": ["instagram", "tiktok", "youtube shorts", "facebook", "twitter", "x.com", "threads", "red social", "meta", "google", "netflix", "app", "aplicacion", "pantalla", "celular", "movil"],
    "e-commerce": ["amazon", "temu", "ebay", "shein", "walmart", "target", "costco", "tienda", "compras", "centro comercial", "hipermercado", "supermercado"],
    "corporate_high_density": ["wall street", "chase", "bank of america", "sede corporativa", "oficina", "rascacielos", "empresa", "corporacion", "fábrica", "refinería", "planta de ensamblaje"],
    "health_clinic_pressure": ["hospital", "clinica", "sala de emergencia", "laboratorio", "medico", "enfermera", "seguro medico", "farmacia"],
    "government_institutional": ["dmv", "juzgados federales", "usps", "estacion de policia", "prision", "guardia nacional", "agencia estatal", "ayuntamiento", "ministerio publico", "dependencia del gobierno"],
    "transport_high_speed": ["carretera interestatal", "autopista", "puente", "metro", "aeropuerto", "jfk", "lax", "mia", "via de tren", "transporte publico", "coche", "manejar", "conducir"],
    "recreational_natural": ["playa", "lago", "parque nacional", "yellostone", "yosemite", "bosque", "rio", "desierto", "piscina comunitaria", "campo", "aire libre", "naturaleza"],
    "non_human_elements": ["sol", "luna", "nubes", "aire", "viento", "clima"]
}

# FASE 4: Mecánica de Secuestro del Significado de la Marca
CORPORATE_BRAND_MEANINGS = {
    "starbucks": {"need_key": "pausas_silencio", "meaning_es": "necesidad de pausa/escape", "meaning_en": "need for pause/escape", "category": "food_drink"},
    "walmart": {"need_key": "soc_automatismo_masa", "meaning_es": "automatismo de masa", "meaning_en": "mass automatism", "category": "retail"},
    "target": {"need_key": "soc_automatismo_masa", "meaning_es": "automatismo de masa", "meaning_en": "mass automatism", "category": "retail"},
    "disney": {"need_key": "ext_espejismo_evasion", "meaning_es": "espejismo de evasión", "meaning_en": "mirage of evasion", "category": "entertainment"},
    "mcdonald's": {"need_key": "nutricion_real", "meaning_es": "ansiedad por ultraprocesados", "meaning_en": "ultra-processed food anxiety", "category": "food_drink"},
    "amazon": {"need_key": "comercio_compulsivo", "meaning_es": "ansiedad por adquisición", "meaning_en": "acquisition anxiety", "category": "e-commerce"},
    "temu": {"need_key": "comercio_compulsivo", "meaning_es": "ansiedad por adquisición", "meaning_en": "acquisition anxiety", "category": "e-commerce"},
    "ebay": {"need_key": "comercio_compulsivo", "meaning_es": "ansiedad por adquisición", "meaning_en": "acquisition anxiety", "category": "e-commerce"},
    "instagram": {"need_key": "soc_validacion_rapida", "meaning_es": "estimulación visual rápida/validación social", "meaning_en": "rapid visual stimulation/social validation", "category": "digital_platform"},
    "tiktok": {"need_key": "soc_validacion_rapida", "meaning_es": "estimulación visual rápida/validación social", "meaning_en": "rapid visual stimulation/social validation", "category": "digital_platform"},
    "youtube shorts": {"need_key": "soc_validacion_rapida", "meaning_es": "estimulación visual rápida/validación social", "meaning_en": "rapid visual stimulation/social validation", "category": "digital_platform"},
    "meta": {"need_key": "soc_validacion_rapida", "meaning_es": "estimulación visual rápida/validación social", "meaning_en": "rapid visual stimulation/social validation", "category": "digital_platform"},
    "google": {"need_key": "ext_distraccion_cognitiva", "meaning_es": "distracción cognitiva/busqueda sin rumbo", "meaning_en": "cognitive distraction/aimless search", "category": "digital_platform"},
    "netflix": {"need_key": "ext_espejismo_evasion", "meaning_es": "espejismo de evasión", "meaning_en": "mirage of evasion", "category": "digital_platform"},
    "microsoft": {"need_key": "fis_sobrecarga_cortisol", "meaning_es": "sobrecarga laboral/mental", "meaning_en": "work/mental overload", "category": "corporate"},
    "apple": {"need_key": "comercio_compulsivo", "meaning_es": "ansiedad por adquisición/estatus", "meaning_en": "acquisition/status anxiety", "category": "e-commerce"},
    # Generic categories (used if specific brands not detected but category is)
    "digital_platform_generic": {"need_key": "soc_validacion_rapida", "meaning_es": "estimulación visual rápida/validación social", "meaning_en": "rapid visual stimulation/social validation", "category": "digital_platform"},
    "e-commerce_generic": {"need_key": "comercio_compulsivo", "meaning_es": "comercio compulsivo/gasto", "meaning_en": "compulsive shopping/spending", "category": "e-commerce"},
    "corporate_environment_generic": {"need_key": "fis_sobrecarga_cortisol", "meaning_es": "sobrecarga de cortisol/supresión biológica", "meaning_en": "cortisol overload/biological suppression", "category": "corporate_high_density"},
    "public_health_generic": {"need_key": "sis_nervioso_saturado", "meaning_es": "saturación sistema nervioso/estrés entorno", "meaning_en": "nervous system saturation/environmental stress", "category": "health_clinic_pressure"},
    "government_office_generic": {"need_key": "sis_nervioso_saturado", "meaning_es": "saturación sistema nervioso/estrés entorno", "meaning_en": "nervous system saturation/environmental stress", "category": "government_institutional"},
    "high_speed_transport_generic": {"need_key": "fis_desconexion_presencia", "meaning_es": "desconexión de presencia/piloto automático", "meaning_en": "disconnection from presence/autopilot", "category": "transport_high_speed"},
    "mass_retail_generic": {"need_key": "soc_automatismo_masa", "meaning_es": "automatismo de masa/consumo inconsciente", "meaning_en": "mass automatism/unconscious consumption", "category": "e-commerce"},
    "food_drink_generic": {"need_key": "nutricion_real", "meaning_es": "ansiedad por ultraprocesados", "meaning_en": "ultra-processed food anxiety", "category": "food_drink"},
}


# FASE 5: BIOLOGICAL PROTOCOLS MISSIONS (new missions based on specific triggers)
BIOLOGICAL_PROTOCOLS_MISSIONS = [
    {
        "id": "BIO_ELIM_001",
        "name": "Eliminación Líquida y Sólida Consciente",
        "trigger_states_es": ["atrapado", "stand by", "monotonia", "rutina", "agotado", "cansado", "sin direccion", "paralizado"],
        "trigger_entities_es": ["rascacielos", "fabricas", "oficinas corporativas", "hospitales", "bancos", "gobierno", "juzgados federales", "dependencia del gobierno", "dmv", "usps", "prision"],
        "title_es": "Módulo Eliminación/Depuración Absoluta",
        "description_es": "Tu mente está atrapada en la máquina de producción mientras tu biología se intoxica en silencio. Levántate de forma voluntaria en este segundo. Ve al baño de esta infraestructura pública o privada. Ejecuta la eliminación biológica de toxinas (Orinar/Defecar) con absoluta presencia mental. Siente la liberación mecánica de la vejiga y el vaciado del colon. Mientras la empresa factura millones, tú recuperas la soberanía de tus órganos. Has convertido este baño corporativo en tu centro de depuración celular. No regreses a la pantalla hasta que tu máquina viva esté limpia.",
        "title_en": "Conscious Liquid and Solid Elimination Module",
        "description_en": "Your mind is trapped in the production machine while your biology silently intoxicates itself. Stand up voluntarily this second. Go to the restroom of this public or private infrastructure. Perform biological elimination of toxins (Urinate/Defecate) with absolute mental presence. Feel the mechanical release of the bladder and the emptying of the colon. While the company earns millions, you regain sovereignty over your organs. You have transformed this corporate restroom into your cellular purification center. Do not return to the screen until your living machine is clean.",
        "vector_necesidades": {"orinar": 100, "defecar": 100, "movimiento": 80, "silencio": 70, "descanso": 90, "indicador_ansiedad": -50, "motilidad_linfatica": 60, "pausas_silencio": 80, "fis_sobrecarga_cortisol": -80},
        "duration_seconds": 60,
        "gps": "restroom near me" # Generic for GPS search
    },
    {
        "id": "BIO_VENT_002",
        "name": "Ventilación Tisular y Desintoxicación Gaseosa",
        "trigger_states_es": ["estresado", "desesperado", "ansioso", "alterado", "sin ideas", "paralizado", "agotado", "cansado"],
        "trigger_entities_es": ["aeropuertos", "jfk", "lax", "metros", "carreteras congestionadas", "walmart", "target", "costco", "tienda", "centro comercial", "oficina", "rascacielos", "fábrica", "refinería", "planta de ensamblaje", "transporte publico"],
        "title_es": "Módulo Breath/Empty: Expulsión de CO2",
        "description_es": "Detén tu marcha o tu scroll. La atmósfera industrial y el estrés están acidificando tu sangre con respiración superficial. Hackea este espacio: busca la ventana más cercana, sal al estacionamiento, o quédate estático en medio del pasillo. Inhala el aire del perímetro en 4 segundos, retén 4 segundos y ejecuta una espiración diafragmática profunda durante 6 segundos. Fuerza la expulsión total del dióxido de carbono (CO2) y las hormonas de la ansiedad. Siente cómo tus pulmones se adueñan del oxígeno disponible gratis en este Código Postal. La prisión mental de tus problemas se rompe cuando tu biología manda.",
        "title_en": "Breath/Empty Module: CO2 Expulsion",
        "description_en": "Stop walking or scrolling. The industrial atmosphere and stress are acidifying your blood with shallow breathing. Hack this space: find the nearest window, go out to the parking lot, or stand still in the middle of the aisle. Inhale the perimeter air for 4 seconds, hold for 4 seconds, and perform a deep diaphragmatic exhalation for 6 seconds. Force the total expulsion of carbon dioxide (CO2) and stress hormones. Feel your lungs taking over the free oxygen available in this ZIP Code. The mental prison of your problems breaks when your biology commands.",
        "vector_necesidades": {"espirar_co2": 100, "oxigenacion": 100, "aire_fresco": 95, "silencio": 60, "descanso": 80, "indicador_ansiedad": -70, "contemplacion": 70, "sis_nervioso_saturado": -80},
        "duration_seconds": 60,
        "gps": "open space with fresh air"
    },
    {
        "id": "BIO_NUTR_003",
        "name": "Nutrición Consciente y Desconexión Sensorial",
        "trigger_states_es": ["cansado", "deprimido", "infeliz", "descontento", "traicionado", "aburrido", "rutina", "ansioso"],
        "trigger_entities_es": ["mcdonald's", "starbucks", "maquinas expendedoras", "comida rapida", "ultraprocesados", "cafe", "walmart", "target", "amazon", "temu", "ebay"],
        "title_es": "Módulo Nutrient Consciousness",
        "description_es": "El mercado te vende azúcares y químicos como anestesia para tu vacío mental. Detén el consumo inconsciente. Si estás comiendo o bebiendo agua en esta oficina, hospital, parque o carretera, hazlo bajo el Módulo 'Nutrient Consciousness'. Saborea cada molécula de agua hidratando tus articulaciones; mastica despacio sintiendo las enzimas salivales activarse. Rompe la rutina: aleja tu mirada de la pantalla, observa la textura de la comida o del vaso. Invierte el dinero y el tiempo en nutrir tu cuerpo, no en enriquecer la marca. Estás alimentando tus células, no tapando tus emociones.",
        "title_en": "Nutrient Consciousness Module",
        "description_en": "The market sells you sugars and chemicals as anesthesia for your mental void. Stop unconscious consumption. If you are eating or drinking water in this office, hospital, park, or on the road, do it under the 'Nutrient Consciousness' Module. Savor each molecule of water hydrating your joints; chew slowly, feeling your salivary enzymes activate. Break the routine: look away from the screen, observe the texture of the food or the glass. Invest money and time in nourishing your body, not enriching the brand. You are feeding your cells, not masking your emotions.",
        "vector_necesidades": {"nutricion_real": 100, "hidratacion_celular": 100, "alimentacion": 90, "contemplacion": 90, "pausas_silencio": 80, "indicador_ansiedad": -60, "sensorial_organica": 85, "comercio_compulsivo": -90},
        "duration_seconds": 60,
        "gps": "water fountain or quiet eating area"
    },
    {
        "id": "BIO_MOTIL_004",
        "name": "Homeostasis Térmica y Motilidad Linfática",
        "trigger_states_es": ["paralizado", "perdido", "aburrido", "sin direccion", "monotonia", "rutina"],
        "trigger_entities_es": ["playas", "parques comunitarios", "calles de vecindarios", "bosques", "estacionamientos", "terminales", "campo abierto", "sendero", "naturaleza", "carreteras", "autopistas"],
        "title_es": "Módulo Sudar/Moverse/Eliminar por Piel",
        "description_es": "Estás rodeado por una infraestructura natural o pública que costó millones mantener y la estás ignorando por mirar un reflejo digital. Hackea el espacio físico ahora mismo. Camina a paso acelerado durante los próximos 60 segundos por este parque/playa/calle hasta forzar a tu cuerpo a elevar su ritmo cardíaco y activar las glándulas sudoríparas. Permite que tu piel sude, que elimine urea y sal, autorregulando tu temperatura bajo el sol directo o el aire del ambiente. Rompe la parálisis de tu rutina diaria poniendo tus músculos en movimiento. Has usado la infraestructura de los Estados Unidos de forma gratuita para liberar tu mente de la monotonía.",
        "title_en": "Thermic Homeostasis and Lymphatic Motility Module",
        "description_en": "You are surrounded by a natural or public infrastructure that cost millions to maintain and you are ignoring it by looking at a digital reflection. Hack the physical space right now. Walk at an accelerated pace for the next 60 seconds through this park/beach/street until you force your body to raise its heart rate and activate sweat glands. Allow your skin to sweat, to eliminate urea and salt, self-regulating your temperature under direct sun or ambient air. Break the paralysis of your daily routine by putting your muscles in motion. You have used the infrastructure of the United States for free to free your mind from monotony.",
        "vector_necesidades": {"sudar": 100, "motilidad_linfatica": 100, "movimiento": 95, "homeostasis_termica": 90, "naturaleza": 90, "aire_fresco": 85, "juego": 70, "indicador_ansiedad": -40, "ext_estancamiento": -70},
        "duration_seconds": 60,
        "gps": "public park or beach"
    },
    {
        "id": "BIO_EMOC_005",
        "name": "Liberación Emocional, Lagrimal y Conexión Climática",
        "trigger_states_es": ["enganado", "enamorado", "feliz", "infeliz", "afortunado", "traicionado", "deprimido", "aislado", "desafortunado", "descontento"],
        "trigger_entities_es": ["sol", "luna", "nubes", "aire", "cielo", "playa", "parque", "bosque", "desierto", "aire libre", "naturaleza"],
        "title_es": "Módulo Observation/Cry",
        "description_es": "Llora si tu sistema nervioso lo exige; expulsa el cortisol a través de tus lágrimas en este mismo instante. Mira las nubes, el sol que brilla o la luna en tu Zip Code. Siente la inmensidad del aire que te rodea. La rutina de los segundos y los años pasa de largo porque te desconectas de tu conciencia; regresa al presente utilizando este paisaje gratis como tu ancla de libertad.",
        "title_en": "Observation/Cry Module",
        "description_en": "Cry if your nervous system demands it; expel cortisol through your tears at this very moment. Look at the clouds, the shining sun, or the moon in your Zip Code. Feel the immensity of the air around you. The routine of seconds and years passes by because you disconnect from your consciousness; return to the present using this free landscape as your anchor of freedom.",
        "vector_necesidades": {"llorar_lubricar": 100, "contemplacion": 95, "naturaleza": 100, "silencio": 80, "sol": 90, "indicador_ansiedad": -80, "sensorial_organica": 90, "esperanza": 85, "soc_desconexion": -70, "soc_aislamiento": -70},
        "duration_seconds": 60,
        "gps": "open space with sky view"
    }
]

# FASE 7: PROTOCOLO DE SEGURIDAD OPERATIVA, CONTINGENCIA Y AUDIO DE DESCONEXIÓN PASIVA
AUDIO_SAFETY_PROTOCOLS = {
    "driving_es": {
        "title_es": "PROTOCOLO DE SEGURIDAD VIAL ACTIVO",
        "description_es": "Atención. OPEN THAN GO ha bloqueado tu pantalla por tu seguridad física. Estás manejando en una de las carreteras interestatales de los Estados Unidos, una infraestructura de asfalto diseñada para mover cuerpos de forma mecánica. Tu cuerpo viaja a alta velocidad, pero tu mente está atrapada en una prisión mental de monotonía o estrés. No mires este teléfono. Mantén tus ojos fijos en el camino. Hackea este trayecto mediante el Módulo de Ventilación Pasiva en este mismo instante: inhala profundamente por la nariz expandiendo tu caja torácica, retén el aire sintiendo los latidos de tu corazón, y exhala de forma lenta y prolongada por la boca vaciando el dióxido de carbono (CO2) acumulado en tu torrente sanguíneo. Utiliza el volante y el asiento como anclas táctiles de presencia. Observa la inmensidad de las nubes, el cielo o la luna sobre el horizonte sin perder la concentración en la vía. Estás en control de tu vida, no del tráfico. Has transformado esta autopista en tu pista de descompresión cerebral a costo cero. Ejecución pasiva activada.",
        "vector_necesidades": {"oxigenacion": 100, "espirar_co2": 100, "contemplacion": 90, "silencio": 70, "naturaleza": 80, "indicador_ansiedad": -90, "fis_desconexion_presencia": -100},
        "duration_seconds": 120 # Longer for safety protocol
    },
    "driving_en": {
        "title_en": "ROAD SAFETY PROTOCOL ACTIVE",
        "description_en": "Attention. OPEN THAN GO has blocked your screen for your physical safety. You are driving on one of the United States' interstate highways, an asphalt infrastructure designed to mechanically move bodies. Your body is traveling at high speed, but your mind is trapped in a mental prison of monotony or stress. Do not look at this phone. Keep your eyes fixed on the road. Hack this journey using the Passive Ventilation Module right now: inhale deeply through your nose expanding your rib cage, hold your breath feeling your heart beat, and exhale slowly and prolonged through your mouth emptying the carbon dioxide (CO2) accumulated in your bloodstream. Use the steering wheel and seat as tactile anchors of presence. Observe the immensity of the clouds, the sky, or the moon over the horizon without losing concentration on the road. You are in control of your life, not traffic. You have transformed this highway into your brain decompression track at zero cost. Passive execution activated.",
        "vector_necesidades": {"oxigenacion": 100, "espirar_co2": 100, "contemplacion": 90, "silencio": 70, "naturaleza": 80, "indicador_ansiedad": -90, "fis_desconexion_presencia": -100},
        "duration_seconds": 120
    }
}

# FASE 6: Algoritmo del Índice de Inversión Biopsicosocial (IIB) - Factor Contextual Logic
def get_factor_contextual(mission_obj, parsed_entities):
    mission_type = mission_obj.get("action_type", "general_salir")
    
    if mission_type == "audio_safety": return 1.5 # Highest impact for safety
    if mission_type == "biological_protocol": # Specific biological protocols are high impact
        return 1.5

    # Check for specific keywords in mission entities (conceptual from FASE 3 and 4)
    entities_lower = ' '.join(parsed_entities["entities_raw"]).lower() if parsed_entities else ""

    # Multiplier x1.5: If the challenge was executed in environments of maximum alienation
    if any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["corporate_high_density"]) or \
       any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["health_clinic_pressure"]) or \
       any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["government_institutional"]):
        return 1.5
    
    # Multiplier x1.2: If the challenge was executed in static transport infrastructure or commercial
    if any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["transport_high_speed"]) or \
       any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["e-commerce"]) or \
       any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["digital_platform"]): # Digital platforms count as static commercial attention
        return 1.2
            
    # Multiplier x1.0: If the challenge was executed in natural or public recreational environments
    if any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["recreational_natural"]) or \
       any(k in entities_lower for k in INFRASTRUCTURE_KEYWORDS_MAPPING["non_human_elements"]):
        return 1.0

    # Default for other cases or if entities couldn't be categorized
    return 1.0

# ============================================================
# MOTOR DE HISTORIAL INTELIGENTE CWRE V2
# Anti-Repetición + Exploración Controlada
# ============================================================
MAX_HISTORY_SALIR = 5
MAX_HISTORY_CASA = 8
MAX_HISTORY_ORACULO = 12
EXPLORATION_RATE = 0.20
HISTORY_PENALTY_BASE = 40
DECAY_PER_DAY = 0.985

def limitar_historial(historial, limite):
    if historial is None:
        return []
    return historial[-limite:]

def penalizacion_historial(mision_id, historial):
    if not historial:
        return 0
    historial = list(reversed(historial))
    for posicion, antiguo in enumerate(historial):
        if antiguo == mision_id:
            if posicion == 0:
                return HISTORY_PENALTY_BASE
            elif posicion == 1:
                return HISTORY_PENALTY_BASE * 0.85
            elif posicion == 2:
                return HISTORY_PENALTY_BASE * 0.70
            elif posicion <= (len(historial) - 1):
                return HISTORY_PENALTY_BASE * 0.30
    return 0

def bonus_exploracion(mision_id, historial):
    if not historial:
        return 20
    if mision_id not in historial:
        return 15
    return 0

def actualizar_historial(historial, nuevo_id, limite):
    historial = historial or []
    if nuevo_id in historial:
        historial.remove(nuevo_id)
    historial.append(nuevo_id)
    return historial[-limite:]

def diversidad_vector(vector1, vector2):
    distancia = 0
    needs_to_consider = [k for k in DEFAULT_NECESSITY_VECTOR.keys() if k not in ["indicador_ansiedad", "soc_desconexion", "soc_aislamiento", "ext_vacio_existencial", "ext_estancamiento", "fis_sobrecarga_cortisol", "sis_nervioso_saturado", "fis_desconexion_presencia", "soc_automatismo_masa", "soc_validacion_rapida", "comercio_compulsivo", "ext_espejismo_evasion", "ext_distraccion_cognitiva"]]
    for k in needs_to_consider:
        distancia += abs(
            vector1.get(k, 50) -
            vector2.get(k, 50)
        )
    return distancia

def decay_profile(profile, dias):
    return profile

WHEN_ES = "Ahora mismo. Levántate de la silla ya."
WHEN_EN = "Right now. Get out of your chair immediately."
FOR_WHAT_ES = "Para romper el zombi urbano y recordar que la vida es más que pagar cuentas."
FOR_WHAT_EN = "To break the urban zombie and remember that life is more than paying bills."

# ============================================================
# CATÁLOGO DE MISIONES CWRE V2.1
# Adaptado para Microacciones de Recuperación Mental y sin elementos de estrés laboral/financiero.
# ============================================================
BASE_MISIONES = {
    "CASA_ES": [
        {"id": 1, "titulo": "Corta el piloto automático", "descripcion": "Escanea tu cuerpo. Ubica el peso exacto en tu espalda. Míralo. Estás vivo.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Desconexión total", "descripcion": "Siente tu silla. El piso sostiene tu peso gratis. Déjate caer.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Aislamiento de pantalla", "descripcion": "Voltea el teléfono. Mira una esquina del techo 30 segundos. Rompe el bucle.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Soltar la carga", "descripcion": "Siente tus hombros libres. Ya no tienes esa mochila de peso invisible.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "El reset del agua", "descripcion": "Un trago pequeño de agua fría. Siente el líquido. Es la vida entrando.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "hidratacion_celular": 90}},
        {"id": 7, "titulo": "El aire de la ventana", "descripcion": "Abre la ventana. Deja que el aire te golpee la cara. Siente el exterior.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30, "oxigenacion": 80}},
        {"id": 8, "titulo": "Rotación de energía", "descripcion": "Gira muñecas y tobillos. Tu cuerpo es tuyo. Tú gobiernas este motor.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "motilidad_linfatica": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Anclaje del presente", "descripcion": "Cierra los ojos. Di una sola cosa buena que tienes hoy. Dilo fuerte.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30, "pausas_silencio": 90}},
        {"id": 11, "titulo": "Pies en la tierra", "descripcion": "Quítate zapatos. Apoya plantas en el piso. Siente el frío. Conéctate.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70, "sensorial_organica": 90}},
        {"id": 12, "titulo": "Estiramiento al cielo", "descripcion": "Brazo arriba. Toca el techo. Mantén la tensión. Suelta de golpe.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "motilidad_linfatica": 80, "creatividad": 30, "juego": 20}},
        {"id": 14, "titulo": "Columna recta", "descripcion": "Endereza la espalda. Un hilo invisible tira de tu cabeza. Respira.", "vector_necesidades": {"motilidad_linfatica": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70, "oxigenacion": 70}},
        {"id": 15, "titulo": "Contacto frío", "descripcion": "Toca una superficie fría. Siente la temperatura real. Aterriza.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20, "homeostasis_termica": 90, "sensorial_organica": 80}},
        {"id": 16, "titulo": "Ventilación total", "descripcion": "Abre la ventana. Deja que el aire ruede. Huele el cambio.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40, "oxigenacion": 90}},
        {"id": 17, "titulo": "Sacudida de estrés", "descripcion": "Párate y sacude manos y piernas como quitándote agua. Hazlo 10 segundos.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70, "motilidad_linfatica": 90, "sudar": 60}},
        {"id": 18, "titulo": "Mirada lejana", "descripcion": "Mira el objeto más lejano por tu ventana. Descansa el enfoque.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40, "pausas_silencio": 85}},
        {"id": 19, "titulo": "Memoria feliz", "descripcion": "Cierra los ojos y recuerda un momento real de calma en tu niñez.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85, "pausas_silencio": 80}},
        {"id": 20, "titulo": "Sonrisa forzada", "descripcion": "Sonríe 15 segundos. Cambia tu química cerebral ahora.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "sensorial_organica": 80}},
        {"id": 21, "titulo": "Agradecimiento", "descripcion": "Cierra los ojos. Agradece una cosa buena de esta semana.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60, "pausas_silencio": 80}},
        {"id": 22, "titulo": "Relaxa ojos", "descripcion": "Tápate los ojos con palmas templadas. Un minuto de oscuridad.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "llorar_lubricar": 70, "naturaleza": 20, "pausas_silencio": 90}},
        {"id": 23, "titulo": "Ritmo cardíaco", "descripcion": "Mano derecha en el pecho. Siente el latido. Es tu motor.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "oxigenacion": 70, "movimiento": 10, "sensorial_organica": 90}},
        {"id": 24, "titulo": "Suelta cuello", "descripcion": "Círculos lentos de cabeza. Libera la tensión de pantalla.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "motilidad_linfatica": 90, "silencio": 70, "organizacion": 30}},
        {"id": 25, "titulo": "Ejercicio de palmas", "descripcion": "Frota manos hasta sentir calor. Colócalas en hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "homeostasis_termica": 85, "silencio": 60, "contemplacion": 50}},
        {"id": 26, "titulo": "Sonidos lejanos", "descripcion": "Identifica el sonido más lejano fuera de casa.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70, "sensorial_organica": 90}},
        {"id": 27, "titulo": "Estiramiento lateral", "descripcion": "Inclina el cuerpo suavemente a cada lado.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 28, "titulo": "El vaso vacío", "descripcion": "Mira un vaso. Concéntrate en su forma un minuto.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70, "pausas_silencio": 90}},
        {"id": 29, "titulo": "Suelta mandíbula", "descripcion": "Abre grande la boca, mueve mandíbula a los lados.", "vector_necesidades": {"movimiento": 80, "motilidad_linfatica": 90, "risa": 70, "descanso": 80, "silencio": 60}},
        {"id": 30, "titulo": "Pasos lentos", "descripcion": "Diez pasos lentos, conscientes, en tu cuarto.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60, "motilidad_linfatica": 70}},
        {"id": 31, "titulo": "Masaje suave", "descripcion": "Yemas en las sienes. Círculos muy lentos.", "vector_necesidades": {"descanso": 100, "sensorial_organica": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
        {"id": 32, "titulo": "Conciencia aire", "descripcion": "Siente el aire frío entrar, el cálido salir.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70, "oxigenacion": 90, "espirar_co2": 80}},
        {"id": 33, "titulo": "Espalda firme", "descripcion": "Omóplatos atrás, abre el pecho.", "vector_necesidades": {"movimiento": 85, "motilidad_linfatica": 90, "organizacion": 70, "descanso": 70, "esperanza": 60, "oxigenacion": 70}},
        {"id": 34, "titulo": "Apoyo total", "descripcion": "Siente la silla sosteniendo tu peso total.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10, "sensorial_organica": 85}},
        {"id": 35, "titulo": "Cuenta atrás", "descripcion": "Del 20 al 1. Despacio. Calma el ruido.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70, "pausas_silencio": 90}},
        {"id": 36, "titulo": "Toca textura", "descripcion": "Pasa dedos por una textura real. Madera o tela.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70, "sensorial_organica": 90}},
        {"id": 37, "titulo": "Estira dedos", "descripcion": "Separa dedos lo más posible 5 segundos. Suelta.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
        {"id": 38, "titulo": "Sonido interno", "descripcion": "Escucha tu respiración. No la fuerces.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "oxigenacion": 85, "naturaleza": 60, "pausas_silencio": 95}},
        {"id": 39, "titulo": "Mirada fija", "descripcion": "Punto pequeño en la pared. Fijo. Sin parpadear.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75, "pausas_silencio": 90}},
        {"id": 40, "titulo": "Suelta brazos", "descripcion": "Cuelga brazos. Sacúdelos suavemente.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "motilidad_linfatica": 85, "risa": 60, "juego": 50}},
        {"id": 41, "titulo": "Contacto ropa", "descripcion": "Nota el peso de la ropa sobre tu piel.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10, "sensorial_organica": 80}},
        {"id": 42, "titulo": "Aire profundo", "descripcion": "Infla vientre, retén 3 segundos, suelta lento.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "aire_fresco": 80, "contemplacion": 90, "espirar_co2": 95}},
        {"id": 43, "titulo": "Rotación hombros", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
        {"id": 44, "titulo": "Escucha silencio", "descripcion": "Busca el silencio entre respiraciones.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70, "pausas_silencio": 100}},
        {"id": 45, "titulo": "Mirada techo", "descripcion": "Mira techo. Estira cuello sin mover hombros.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "motilidad_linfatica": 80, "contemplacion": 70, "silencio": 60}},
        {"id": 46, "titulo": "Siente base", "descripcion": "Contacto firme de piernas con silla.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20, "sensorial_organica": 80}},
        {"id": 48, "titulo": "Limpieza mental", "descripcion": "Exhala preocupación aburrida. Fuera de ti.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60, "espirar_co2": 70, "pausas_silencio": 80}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30, "sensorial_organica": 80}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70, "pausas_silencio": 90}},
        {"id": 51, "titulo": "Canta una melodía", "descripcion": "Tararea tu canción favorita suavemente. No pienses, solo siente el sonido.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50, "pausas_silencio": 70}},
        {"id": 52, "titulo": "Escribe 3 deseos", "descripcion": "En un papel, anota tres deseos simples que te gustaría cumplir hoy.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70, "pausas_silencio": 70}},
        {"id": 53, "titulo": "Paseo por el pasillo", "descripcion": "Camina lentamente por el pasillo de tu casa, sintiendo cada paso.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50, "motilidad_linfatica": 70}},
        {"id": 54, "titulo": "Mira una planta", "descripcion": "Si tienes una planta en casa, obsérvala con atención durante un minuto.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60, "pausas_silencio": 80, "sensorial_organica": 90}},
        {"id": 55, "titulo": "Dibuja un círculo", "descripcion": "Toma un lápiz y papel. Dibuja círculos perfectos sin pensar en nada más.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50, "pausas_silencio": 70}},
        {"id": 57, "titulo": "Abre un libro al azar", "descripcion": "Toma un libro, ábrelo en una página aleatoria y lee la primera frase.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "pausas_silencio": 70}},
        {"id": 58, "titulo": "Escucha la lluvia", "descripcion": "Si llueve, abre la ventana y escucha el sonido de las gotas caer.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85, "pausas_silencio": 90, "sensorial_organica": 90}},
        {"id": 59, "titulo": "Baila sin música", "descripcion": "Mueve tu cuerpo libremente por un minuto, como si nadie te viera.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50, "motilidad_linfatica": 90, "sudar": 70}},
        {"id": 60, "titulo": "Bebe una infusión", "descripcion": "Prepara una infusión caliente y bébela lentamente, sintiendo el calor.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "nutricion_real": 70, "contemplacion": 70, "hidratacion_celular": 90}},
        {"id": 61, "titulo": "Mira tus manos", "descripcion": "Observa las líneas y detalles de tus manos. Son herramientas poderosas.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50, "sensorial_organica": 80}},
        {"id": 62, "titulo": "Imagina un paisaje", "descripcion": "Cierra los ojos e imagina tu paisaje natural favorito por 30 segundos.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80, "pausas_silencio": 90}},
        {"id": 63, "titulo": "Estira la espalda", "descripcion": "Siéntate en el suelo con las piernas estiradas y trata de tocar tus pies.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 64, "titulo": "Respira por la nariz", "descripcion": "Haz 5 respiraciones profundas, solo por la nariz, notando el aire.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "aire_fresco": 80, "contemplacion": 90, "espirar_co2": 95}},
        {"id": 65, "titulo": "Juego de sombras", "descripcion": "Con las manos, crea una forma en la pared con la luz de una lámpara.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50, "pausas_silencio": 70}},
        {"id": 66, "titulo": "Un abrazo imaginario", "descripcion": "Abraza tus brazos fuertemente, imaginando que es un ser querido.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50, "soc_desconexion": -80}},
        {"id": 67, "titulo": "Encuentra un objeto azul", "descripcion": "Busca rápidamente 5 objetos azules en tu entorno. Enfoca tu vista.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70, "pausas_silencio": 70}},
        {"id": 69, "titulo": "Observa el cielo", "descripcion": "Abre la ventana o sal al balcón. Observa el cielo por un minuto.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70, "pausas_silencio": 90, "sensorial_organica": 90}},
        {"id": 70, "titulo": "Masaje facial", "descripcion": "Con las yemas de los dedos, masajea suavemente tu frente y mejillas.", "vector_necesidades": {"descanso": 100, "sensorial_organica": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Cierra los ojos y escucha", "descripcion": "Siéntate cómodo, cierra los ojos y solo escucha los sonidos de tu casa.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60, "pausas_silencio": 100}},
        {"id": 72, "titulo": "Tensa y relaja los pies", "descripcion": "Aprieta los dedos de tus pies durante 5 segundos y luego relájalos.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "motilidad_linfatica": 70, "organizacion": 40, "silencio": 50}},
        {"id": 74, "titulo": "Olor consciente", "descripcion": "Huelea una flor, café o especia. Concéntrate en el aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70, "sensorial_organica": 90}},
        {"id": 75, "titulo": "Cambia de silla", "descripcion": "Siéntate en otra silla o lugar de la casa por 5 minutos. Pequeño cambio.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Abre tu correo o tu aplicación bancaria. Busca 'Subscription', 'Invoice' o 'Payment' y cancela una sola suscripción que ya no utilices. Recuperar el control también es ahorrar.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60, "ext_estancamiento": -70}},
        {"id": 152, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "Abre una nota en tu teléfono y escribe únicamente los tres gastos inevitables de esta semana. No pienses en todo el mes. Solo en esta semana.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80, "indicador_ansiedad": -80}},
        {"id": 153, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra veinte capturas de pantalla, archivos o documentos que ya no necesites. El orden digital también reduce la carga mental.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70, "ext_estancamiento": -70}},
        {"id": 154, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia durante una hora las aplicaciones que más ansiedad te generan. Tu atención también necesita descansar.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80, "pausas_silencio": 100, "sis_nervioso_saturado": -90}},
        {"id": 155, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe tres cosas que hoy tienes y que hace algunos años deseabas. Tu mente necesita recordar que también has avanzado.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60, "ext_vacio_existencial": -90}},
        {"id": 156, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate despacio, bebe un vaso completo de agua y vuelve respirando con calma.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "hidratacion_celular": 85, "silencio": 50, "orinar": 50}},
        {"id": 157, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre una ventana durante dos minutos y observa el cielo sin mirar el teléfono.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70, "oxigenacion": 90, "sensorial_organica": 90}},
        {"id": 158, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda únicamente cinco objetos que estén fuera de lugar. Cinco son suficientes por hoy.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50, "ext_estancamiento": -60}},
        {"id": 159, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Realiza cinco respiraciones profundas siguiendo un ritmo lento. No tienes que hacer nada más.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "contemplacion": 90, "aire_fresco": 80, "espirar_co2": 95, "pausas_silencio": 100}},
        {"id": 160, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Durante dos minutos mira un punto lejano para permitir que tus ojos descansen de la pantalla.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "llorar_lubricar": 80, "pausas_silencio": 90}},
    ],
    "CASA_EN": [
        {"id": 1, "titulo": "Cut the autopilot", "descripcion": "Scan your body. Pinpoint the exact weight on your back. See it. You are alive.", "vector_necesidades": {"contemplacion": 90, "descanso": 80, "silencio": 70, "organizacion": 50, "movimiento": 30}},
        {"id": 2, "titulo": "Total Disconnection", "descripcion": "Feel your chair. The floor supports your weight for free. Let yourself fall.", "vector_necesidades": {"descanso": 90, "contemplacion": 80, "silencio": 70, "organizacion": 40, "esperanza": 60}},
        {"id": 3, "titulo": "Screen Isolation", "descripcion": "Flip your phone. Look at a corner of the ceiling for 30 seconds. Break the loop.", "vector_necesidades": {"silencio": 95, "descanso": 85, "contemplacion": 90, "organizacion": 60, "creatividad": 20}},
        {"id": 4, "titulo": "Release the Burden", "descripcion": "Feel your shoulders free. That invisible backpack of weight is gone.", "vector_necesidades": {"descanso": 90, "movimiento": 60, "risa": 40, "esperanza": 80, "organizacion": 30}},
        {"id": 5, "titulo": "The Water Reset", "descripcion": "A small sip of cold water. Feel the liquid. It's life entering.", "vector_necesidades": {"agua": 100, "descanso": 70, "silencio": 50, "movimiento": 20, "hidratacion_celular": 90}},
        {"id": 7, "titulo": "Street Air", "descripcion": "Open the window. Let the air hit your face. Feel the outside.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 80, "contemplacion": 70, "descanso": 60, "movimiento": 30, "oxigenacion": 80}},
        {"id": 8, "titulo": "Energy Rotation", "descripcion": "Rotate wrists and ankles. Your body is yours. You govern this engine.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "juego": 40, "motilidad_linfatica": 80, "creatividad": 20}},
        {"id": 9, "titulo": "Present Anchor", "descripcion": "Close your eyes. Say one good thing you have today. Say it loud.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "esperanza": 95, "aprendizaje": 70, "risa": 30, "pausas_silencio": 90}},
        {"id": 11, "titulo": "Feet on the Ground", "descripcion": "Take off your shoes. Rest soles on the floor. Feel the cold. Connect.", "vector_necesidades": {"naturaleza": 90, "movimiento": 70, "contemplacion": 80, "silencio": 60, "descanso": 70, "sensorial_organica": 90}},
        {"id": 12, "titulo": "Sky Stretch", "descripcion": "Arm up. Touch the ceiling. Maintain tension. Release suddenly.", "vector_necesidades": {"movimiento": 95, "descanso": 60, "motilidad_linfatica": 80, "creatividad": 30, "juego": 20}},
        {"id": 14, "titulo": "Straight Spine", "descripcion": "Straighten your back. An invisible thread pulls your head. Breathe.", "vector_necesidades": {"motilidad_linfatica": 90, "movimiento": 70, "descanso": 80, "silencio": 60, "contemplacion": 70, "oxigenacion": 70}},
        {"id": 15, "titulo": "Cold Contact", "descripcion": "Touch a cold surface. Feel the real temperature. Ground yourself.", "vector_necesidades": {"naturaleza": 80, "silencio": 70, "contemplacion": 90, "descanso": 60, "movimiento": 20, "homeostasis_termica": 90, "sensorial_organica": 80}},
        {"id": 16, "titulo": "Total Ventilation", "descripcion": "Open the front door. Let the air flow. Smell the change.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "creatividad": 70, "contemplacion": 80, "movimiento": 40, "oxigenacion": 90}},
        {"id": 17, "titulo": "Stress Shake-off", "descripcion": "Stand up and shake hands and legs as if shaking off water. Do it for 10 seconds.", "vector_necesidades": {"movimiento": 100, "risa": 80, "descanso": 70, "juego": 60, "esperanza": 70, "motilidad_linfatica": 90, "sudar": 60}},
        {"id": 18, "titulo": "Distant Gaze", "descripcion": "Look at the farthest object outside your window. Rest your focus.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "naturaleza": 70, "descanso": 80, "creatividad": 40, "pausas_silencio": 85}},
        {"id": 19, "titulo": "Happy Memory", "descripcion": "Close your eyes and recall a real moment of calm from your childhood.", "vector_necesidades": {"esperanza": 90, "contemplacion": 95, "risa": 70, "silencio": 80, "descanso": 85, "pausas_silencio": 80}},
        {"id": 20, "titulo": "Forced Smile", "descripcion": "Smile for 15 seconds. Change your brain chemistry now.", "vector_necesidades": {"risa": 100, "esperanza": 90, "juego": 70, "creatividad": 50, "sensorial_organica": 80}},
        {"id": 21, "titulo": "Gratitude", "descripcion": "Close your eyes. Be thankful for one good thing this week.", "vector_necesidades": {"esperanza": 100, "contemplacion": 90, "silencio": 80, "descanso": 70, "comunidad": 60, "pausas_silencio": 80}},
        {"id": 22, "titulo": "Relax Eyes", "descripcion": "Cover your eyes with warm palms. One minute of darkness.", "vector_necesidades": {"descanso": 100, "silencio": 90, "contemplacion": 80, "llorar_lubricar": 70, "naturaleza": 20, "pausas_silencio": 90}},
        {"id": 23, "titulo": "Heart Rate", "descripcion": "Right hand on chest. Feel the heartbeat. It's your engine.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "descanso": 80, "oxigenacion": 70, "movimiento": 10, "sensorial_organica": 90}},
        {"id": 24, "titulo": "Release Neck", "descripcion": "Slow head circles. Release screen tension.", "vector_necesidades": {"movimiento": 80, "descanso": 90, "motilidad_linfatica": 90, "silencio": 70, "organizacion": 30}},
        {"id": 25, "titulo": "Palm Exercise", "descripcion": "Rub hands until warm. Place them on shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "homeostasis_termica": 85, "silencio": 60, "contemplacion": 50}},
        {"id": 26, "titulo": "Distant Sounds", "descripcion": "Identify the farthest sound outside your home.", "vector_necesidades": {"silencio": 90, "contemplacion": 95, "naturaleza": 80, "aprendizaje": 70, "descanso": 70, "sensorial_organica": 90}},
        {"id": 27, "titulo": "Side Stretch", "descripcion": "Gently lean your body to each side.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 28, "titulo": "The Empty Glass", "descripcion": "Look at a glass. Focus on its shape for one minute.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "creatividad": 60, "aprendizaje": 50, "descanso": 70, "pausas_silencio": 90}},
        {"id": 29, "titulo": "Release Jaw", "descripcion": "Open your mouth wide, move your jaw side to side.", "vector_necesidades": {"movimiento": 80, "motilidad_linfatica": 90, "risa": 70, "descanso": 80, "silencio": 60}},
        {"id": 30, "titulo": "Slow Steps", "descripcion": "Ten slow, conscious steps in your room.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 75, "descanso": 70, "organizacion": 60, "motilidad_linfatica": 70}},
        {"id": 31, "titulo": "Gentle Massage", "descripcion": "Fingertips on temples. Very slow circles.", "vector_necesidades": {"descanso": 100, "sensorial_organica": 90, "silencio": 85, "contemplacion": 70, "movimiento": 20}},
        {"id": 32, "titulo": "Air Awareness", "descripcion": "Feel the cold air enter, the warm air leave.", "vector_necesidades": {"aire_fresco": 100, "silencio": 90, "contemplacion": 95, "descanso": 80, "naturaleza": 70, "oxigenacion": 90, "espirar_co2": 80}},
        {"id": 33, "titulo": "Firm Back", "descripcion": "Shoulder blades back, open your chest.", "vector_necesidades": {"movimiento": 85, "motilidad_linfatica": 90, "organizacion": 70, "descanso": 70, "esperanza": 60, "oxigenacion": 70}},
        {"id": 34, "titulo": "Total Support", "descripcion": "Feel the chair supporting your full weight.", "vector_necesidades": {"descanso": 95, "contemplacion": 90, "silencio": 80, "naturaleza": 40, "movimiento": 10, "sensorial_organica": 85}},
        {"id": 35, "titulo": "Countdown", "descripcion": "From 20 to 1. Slowly. Calm the noise.", "vector_necesidades": {"organizacion": 100, "aprendizaje": 80, "silencio": 90, "contemplacion": 95, "descanso": 70, "pausas_silencio": 90}},
        {"id": 36, "titulo": "Touch Texture", "descripcion": "Run fingers over a real texture. Wood or fabric.", "vector_necesidades": {"contemplacion": 90, "creatividad": 70, "aprendizaje": 60, "naturaleza": 50, "silencio": 70, "sensorial_organica": 90}},
        {"id": 37, "titulo": "Stretch Fingers", "descripcion": "Spread fingers as wide as possible for 5 seconds. Release.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 80, "descanso": 70, "juego": 40, "organizacion": 30}},
        {"id": 38, "titulo": "Internal Sound", "descripcion": "Listen to your breath. Don't force it.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "oxigenacion": 85, "naturaleza": 60, "pausas_silencio": 95}},
        {"id": 39, "titulo": "Fixed Gaze", "descripcion": "Small spot on the wall. Fixed. Without blinking.", "vector_necesidades": {"contemplacion": 100, "silencio": 90, "organizacion": 80, "aprendizaje": 70, "descanso": 75, "pausas_silencio": 90}},
        {"id": 40, "titulo": "Release Arms", "descripcion": "Hang arms. Shake them gently.", "vector_necesidades": {"movimiento": 95, "descanso": 80, "motilidad_linfatica": 85, "risa": 60, "juego": 50}},
        {"id": 41, "titulo": "Clothes Contact", "descripcion": "Notice the weight of clothes on your skin.", "vector_necesidades": {"contemplacion": 90, "silencio": 80, "descanso": 70, "naturaleza": 30, "movimiento": 10, "sensorial_organica": 80}},
        {"id": 42, "titulo": "Deep Air", "descripcion": "Inflate belly, hold 3 seconds, release slowly.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "aire_fresco": 80, "contemplacion": 90, "espirar_co2": 95}},
        {"id": 43, "titulo": "Shoulder Rotation", "descripcion": "Hombros a orejas, cae de golpe.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 80, "risa": 50, "organizacion": 40}},
        {"id": 44, "titulo": "Listen to Silence", "descripcion": "Search for silence between breaths.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 80, "naturaleza": 70, "pausas_silencio": 100}},
        {"id": 45, "titulo": "Ceiling Gaze", "descripcion": "Look at the ceiling. Stretch neck without moving shoulders.", "vector_necesidades": {"movimiento": 70, "descanso": 80, "motilidad_linfatica": 80, "contemplacion": 70, "silencio": 60}},
        {"id": 46, "titulo": "Feel Base", "descripcion": "Firm contact of legs with chair.", "vector_necesidades": {"descanso": 90, "contemplacion": 85, "silencio": 75, "naturaleza": 40, "movimiento": 20, "sensorial_organica": 80}},
        {"id": 48, "titulo": "Mental Cleanse", "descripcion": "Exhale boring worry. Out of you.", "vector_necesidades": {"esperanza": 90, "silencio": 80, "descanso": 85, "risa": 50, "creatividad": 60, "espirar_co2": 70, "pausas_silencio": 80}},
        {"id": 49, "titulo": "Toca mesa", "descripcion": "Palmas en mesa. Nota la stability.", "vector_necesidades": {"contemplacion": 90, "organizacion": 80, "silencio": 70, "descanso": 60, "naturaleza": 30, "sensorial_organica": 80}},
        {"id": 50, "titulo": "Presencia total", "descripcion": "Estás aquí. Estás a salvo. Tienes el control.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "organizacion": 70, "pausas_silencio": 90}},
        {"id": 51, "titulo": "Hum a melody", "descripcion": "Hum your favorite song softly. Don't think, just feel the sound.", "vector_necesidades": {"musica": 100, "risa": 70, "creatividad": 80, "descanso": 60, "juego": 50, "pausas_silencio": 70}},
        {"id": 52, "titulo": "Write 3 wishes", "descripcion": "On a paper, jot down three simple wishes you'd like to fulfill today.", "vector_necesidades": {"creatividad": 90, "aprendizaje": 70, "organizacion": 80, "esperanza": 95, "contemplacion": 70, "pausas_silencio": 70}},
        {"id": 53, "titulo": "Hallway walk", "descripcion": "Walk slowly down your hallway, feeling each step.", "vector_necesidades": {"movimiento": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "organizacion": 50, "motilidad_linfatica": 70}},
        {"id": 54, "titulo": "Look at a plant", "descripcion": "If you have a plant at home, observe it carefully for a minute.", "vector_necesidades": {"naturaleza": 90, "contemplacion": 95, "silencio": 80, "descanso": 70, "aprendizaje": 60, "pausas_silencio": 80, "sensorial_organica": 90}},
        {"id": 55, "titulo": "Draw a circle", "descripcion": "Take a pencil and paper. Draw perfect circles without thinking of anything else.", "vector_necesidades": {"creatividad": 100, "juego": 80, "contemplacion": 70, "silencio": 60, "descanso": 50, "pausas_silencio": 70}},
        {"id": 57, "titulo": "Open a random book", "descripcion": "Grab a book, open it to a random page, and read the first sentence.", "vector_necesidades": {"aprendizaje": 90, "creatividad": 70, "contemplacion": 80, "silencio": 70, "descanso": 60, "pausas_silencio": 70}},
        {"id": 58, "titulo": "Listen to the rain", "descripcion": "If it's raining, open the window and listen to the sound of raindrops.", "vector_necesidades": {"naturaleza": 100, "silencio": 95, "agua": 90, "contemplacion": 90, "descanso": 85, "pausas_silencio": 90, "sensorial_organica": 90}},
        {"id": 59, "titulo": "Dance without music", "descripcion": "Move your body freely for a minute, as if no one is watching.", "vector_necesidades": {"movimiento": 100, "juego": 90, "risa": 80, "creatividad": 70, "musica": 50, "motilidad_linfatica": 90, "sudar": 70}},
        {"id": 60, "titulo": "Drink an infusion", "descripcion": "Prepare a warm infusion and drink it slowly, feeling the warmth.", "vector_necesidades": {"alimentacion": 90, "descanso": 100, "silencio": 80, "nutricion_real": 70, "contemplacion": 70, "hidratacion_celular": 90}},
        {"id": 61, "titulo": "Look at your hands", "descripcion": "Observe the lines and details of your hands. They are powerful tools.", "vector_necesidades": {"contemplacion": 95, "aprendizaje": 70, "silencio": 80, "esperanza": 60, "creatividad": 50, "sensorial_organica": 80}},
        {"id": 62, "titulo": "Imagine a landscape", "descripcion": "Close your eyes and imagine your favorite natural landscape for 30 seconds.", "vector_necesidades": {"naturaleza": 100, "contemplacion": 95, "silencio": 90, "descanso": 85, "creatividad": 80, "pausas_silencio": 90}},
        {"id": 63, "titulo": "Stretch your back", "descripcion": "Sit on the floor with your legs extended and try to touch your feet.", "vector_necesidades": {"movimiento": 90, "motilidad_linfatica": 85, "descanso": 70, "organizacion": 40, "silencio": 50}},
        {"id": 64, "titulo": "Breathe through your nose", "descripcion": "Take 5 deep breaths, only through your nose, noticing the air.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "aire_fresco": 80, "contemplacion": 90, "espirar_co2": 95}},
        {"id": 65, "titulo": "Shadow play", "descripcion": "With your hands, create a shape on the wall with lamp light.", "vector_necesidades": {"juego": 100, "creatividad": 90, "risa": 70, "contemplacion": 60, "descanso": 50, "pausas_silencio": 70}},
        {"id": 66, "titulo": "An imaginary hug", "descripcion": "Hug your arms tightly, imagining it's a loved one.", "vector_necesidades": {"comunidad": 90, "esperanza": 80, "descanso": 70, "risa": 60, "silencio": 50, "soc_desconexion": -80}},
        {"id": 67, "titulo": "Find a blue object", "descripcion": "Quickly find 5 blue objects in your surroundings. Focus your sight.", "vector_necesidades": {"organizacion": 80, "aprendizaje": 70, "juego": 60, "creatividad": 50, "contemplacion": 70, "pausas_silencio": 70}},
        {"id": 69, "titulo": "Observe the sky", "descripcion": "Open the window or go to the balcony. Observe the sky for a minute.", "vector_necesidades": {"naturaleza": 95, "contemplacion": 100, "aire_fresco": 90, "silencio": 80, "descanso": 70, "pausas_silencio": 90, "sensorial_organica": 90}},
        {"id": 70, "titulo": "Facial massage", "descripcion": "With your fingertips, gently massage your forehead and cheeks.", "vector_necesidades": {"descanso": 100, "sensorial_organica": 90, "silencio": 85, "movimiento": 50, "contemplacion": 70}},
        {"id": 71, "titulo": "Close your eyes and listen", "descripcion": "Sit comfortably, close your eyes and just listen to the sounds of your home.", "vector_necesidades": {"silencio": 100, "contemplacion": 95, "descanso": 90, "aprendizaje": 70, "naturaleza": 60, "pausas_silencio": 100}},
        {"id": 72, "titulo": "Tense and relax feet", "descripcion": "Squeeze your toes for 5 seconds and then relax them.", "vector_necesidades": {"movimiento": 90, "descanso": 80, "motilidad_linfatica": 70, "organizacion": 40, "silencio": 50}},
        {"id": 74, "titulo": "Conscious smell", "descripcion": "Smell a flower, coffee, or spice. Concentrate on the aroma.", "vector_necesidades": {"naturaleza": 80, "alimentacion": 70, "contemplacion": 90, "silencio": 80, "descanso": 70, "sensorial_organica": 90}},
        {"id": 75, "titulo": "Change chair", "descripcion": "Sit in another chair or place in the house for 5 minutes. Small change.", "vector_necesidades": {"movimiento": 60, "creatividad": 50, "descanso": 70, "organizacion": 40, "contemplacion": 60}},
        # NUEVAS MICROACCIONES DE RECUPERACIÓN MENTAL (ID 151-160)
        {"id": 151, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Open your email or banking app. Search for 'Subscription', 'Invoice', or 'Payment' and cancel a single subscription you no longer use. Regaining control is also saving.", "vector_necesidades": {"organizacion": 90, "aprendizaje": 70, "descanso": 80, "esperanza": 85, "contemplacion": 60, "ext_estancamiento": -70}},
        {"id": 152, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "Open a note on your phone and write down only the three unavoidable expenses for this week. Don't think about the whole month. Just this week.", "vector_necesidades": {"organizacion": 100, "descanso": 90, "silencio": 70, "aprendizaje": 60, "contemplacion": 80, "indicador_ansiedad": -80}},
        {"id": 153, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete twenty screenshots, files, or documents you no longer need. Digital order also reduces mental load.", "vector_necesidades": {"organizacion": 100, "silencio": 80, "descanso": 85, "creatividad": 50, "contemplacion": 70, "ext_estancamiento": -70}},
        {"id": 154, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence the apps that generate the most anxiety for an hour. Your attention also needs rest.", "vector_necesidades": {"silencio": 100, "descanso": 95, "contemplacion": 90, "organizacion": 70, "esperanza": 80, "pausas_silencio": 100, "sis_nervioso_saturado": -90}},
        {"id": 155, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "Write down three things you have today that you wished for a few years ago. Your mind needs to remember that you have also made progress.", "vector_necesidades": {"esperanza": 100, "contemplacion": 95, "creatividad": 80, "aprendizaje": 70, "silencio": 60, "ext_vacio_existencial": -90}},
        {"id": 156, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand up, drink a full glass of water, and return, breathing calmly.", "vector_necesidades": {"agua": 100, "movimiento": 70, "descanso": 90, "hidratacion_celular": 85, "silencio": 50, "orinar": 50}},
        {"id": 157, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open a window for two minutes and observe the sky without looking at your phone.", "vector_necesidades": {"aire_fresco": 100, "naturaleza": 90, "contemplacion": 95, "descanso": 80, "silencio": 70, "oxigenacion": 90, "sensorial_organica": 90}},
        {"id": 158, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away only five objects that are out of place. Five are enough for today.", "vector_necesidades": {"organizacion": 100, "descanso": 70, "contemplacion": 60, "movimiento": 30, "silencio": 50, "ext_estancamiento": -60}},
        {"id": 159, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take five deep breaths following a slow rhythm. You don't have to do anything else.", "vector_necesidades": {"silencio": 100, "descanso": 95, "oxigenacion": 90, "contemplacion": 90, "aire_fresco": 80, "espirar_co2": 95, "pausas_silencio": 100}},
        {"id": 160, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "For two minutes, look at a distant point to allow your eyes to rest from the screen.", "vector_necesidades": {"contemplacion": 95, "silencio": 85, "descanso": 90, "naturaleza": 70, "llorar_lubricar": 80, "pausas_silencio": 90}},
    ],
    # Refactored SALIR to be a single list for dynamic selection
    "SALIR_GENERAL": [
        # Augmented existing SALIR missions with new necessity vectors and descriptions
        {
            "id": 101, "titulo": "Sombra de árbol", "titulo_en": "Tree Shade",
            "porque": "Mente cansada de pantallas. Necesitas desconectar y reconectar con la energía de la naturaleza.", "porque_en": "Screen-tired mind. You need to disconnect and reconnect with nature's energy.",
            "que_hacer": "Busca un gran árbol. Toca su corteza. Siente la sombra fresca y el aire puro. Permite que el entorno te calme.", "que_hacer_en": "Find a large tree. Touch its bark. Feel the cool shade and fresh air. Let the environment calm you.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Un parque verde o zona arbolada cercana.", "donde_en": "A green park or nearby wooded area.", "gps": "parks with shade",
            "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "sombra": 100, "aire_fresco": 100, "contemplacion": 95, "descanso": 90, "sensorial_organica": 90, "pausas_silencio": 90}
        },
        {
            "id": 102, "titulo": "Caminata en subida", "titulo_en": "Uphill Walk",
            "porque": "Cuerpo y mente tensos. Libera estrés al caminar contra la gravedad. Siente tu fuerza interior y la activación de tu sistema linfático.", "porque_en": "Tense body and mind. Release stress by walking against gravity. Feel your inner strength and lymphatic system activation.",
            "que_hacer": "Encuentra una rampa o escaleras públicas. Sube a paso firme. Concentra tu energía en cada paso y siente el esfuerzo de tus músculos.", "que_hacer_en": "Find a public ramp or stairs. Climb steadily. Focus your energy on each step and feel your muscles working.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Escalera pública o colina.", "donde_en": "Public stairs or hill.", "gps": "public stairs",
            "vector_necesidades": {"movimiento": 100, "motilidad_linfatica": 95, "sudar": 70, "aire_fresco": 85, "contemplacion": 60, "descanso": 10, "indicador_ansiedad": -50}
        },
        {
            "id": 103, "titulo": "Paseo de colores", "titulo_en": "Color Walk",
            "porque": "Días repetitivos y aburridos. Busca novedad visual y despierta tu creatividad. Permite que los colores te llenen de energía.", "porque_en": "Repetitive and boring days. Seek visual novelty and awaken your creativity. Let colors fill you with energy.",
            "que_hacer": "Camina lento por un barrio vibrante. Busca murales, grafitis o elementos arquitectónicos coloridos. Obsérvalos con atención.", "que_hacer_en": "Walk slowly through a vibrant neighborhood. Look for murals, graffiti, or colorful architectural elements. Observe them carefully.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Calle con murales o arte urbano.", "donde_en": "Street with murals or urban art.", "gps": "street art",
            "vector_necesidades": {"movimiento": 80, "creatividad": 100, "sensorial_organica": 90, "aprendizaje": 70, "juego": 55, "contemplacion": 85, "aburrido": -80}
        },
        {
            "id": 104, "titulo": "Lectura en biblioteca", "titulo_en": "Library Reading",
            "porque": "Mente cansada y sobrecargada. Necesitas calma y un espacio para el aprendizaje sin distracciones digitales. Recarga tu energía mental.", "porque_en": "Tired and overloaded mind. You need calm and a space for distraction-free learning. Recharge your mental energy.",
            "que_hacer": "Visita tu biblioteca local. Busca un libro que te interese o simplemente disfruta del silencio y la atmósfera de conocimiento. No uses pantallas.", "que_hacer_en": "Visit your local library. Find a book that interests you or simply enjoy the silence and atmosphere of knowledge. No screens allowed.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Biblioteca pública.", "donde_en": "Public library.", "gps": "public library",
            "vector_necesidades": {"silencio": 100, "aprendizaje": 95, "contemplacion": 90, "descanso": 85, "pausas_silencio": 95, "ext_distraccion_cognitiva": -90}
        },
        {
            "id": 105, "titulo": "Mirar el agua", "titulo_en": "Watch the Water",
            "porque": "Mente ansiosa y agitada. El agua en movimiento tiene un efecto calmante natural. Relaja tus tensiones y permite que tus pensamientos fluyan.", "porque_en": "Anxious and agitated mind. Moving water has a natural calming effect. Relax your tensions and let your thoughts flow.",
            "que_hacer": "Busca una fuente, un lago o un río cercano. Observa el flujo constante del agua, escucha su sonido y concéntrate en la quietud que genera.", "que_hacer_en": "Find a nearby fountain, lake, or river. Observe the constant flow of water, listen to its sound, and focus on the stillness it creates.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Fuente de agua o lago.", "donde_en": "Water fountain or lake.", "gps": "public fountain or lake",
            "vector_necesidades": {"naturaleza": 80, "silencio": 70, "agua": 100, "contemplacion": 90, "descanso": 80, "indicador_ansiedad": -70, "sensorial_organica": 80}
        },
        # Más misiones SALIR, diversificadas para cubrir FASE 3/4
        {
            "id": 106, "titulo": "Café en silencio", "titulo_en": "Quiet Cafe",
            "porque": "Necesitas un respiro mental sin la sobrecarga de estímulos. Un espacio tranquilo para la contemplación.", "porque_en": "Need a mental break without stimulus overload. A quiet space for contemplation.",
            "que_hacer": "Visita una cafetería tranquila. Pide tu bebida. Observa sin distracciones, lejos de tu teléfono.", "que_hacer_en": "Visit a quiet cafe. Order your drink. Observe without distractions, away from your phone.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Cafetería local tranquila.", "donde_en": "Quiet local cafe.", "gps": "quiet cafe",
            "vector_necesidades": {"silencio": 90, "contemplacion": 95, "descanso": 85, "organizacion": 70, "alimentacion": 60, "pausas_silencio": 90}
        },
        {
            "id": 107, "titulo": "Jardín Botánico", "titulo_en": "Botanical Garden",
            "porque": "Mente agotada y desconectada del ritmo natural. Reconéctate con la belleza y el aire puro de la naturaleza.", "porque_en": "Exhausted mind disconnected from nature's rhythm. Reconnect with the beauty and pure air of nature.",
            "que_hacer": "Pasea sin prisa por los senderos. Observa la diversidad de plantas y flores. Respira hondo y siente la vida.", "que_hacer_en": "Stroll leisurely on the paths. Observe the diversity of plants and flowers. Breathe deeply and feel life.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Jardín botánico público.", "donde_en": "Public botanical garden.", "gps": "botanical garden",
            "vector_necesidades": {"movimiento": 70, "naturaleza": 100, "silencio": 75, "aire_fresco": 100, "creatividad": 80, "contemplacion": 90, "descanso": 80, "sensorial_organica": 90}
        },
        {
            "id": 108, "titulo": "Mirador Panorámico", "titulo_en": "Scenic Overlook",
            "porque": "Necesitas perspectiva y romper con la rutina visual que te atrapa. Eleva tu mirada y siente la inmensidad.", "porque_en": "Need perspective and to break the visual routine that traps you. Elevate your gaze and feel the immensity.",
            "que_hacer": "Encuentra un punto alto con vista panorámica. Observa el horizonte lejano y permite que tu mente se expanda más allá de tus problemas.", "que_hacer_en": "Find a high point with a panoramic view. Observe the distant horizon and allow your mind to expand beyond your problems.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Mirador público.", "donde_en": "Public overlook.", "gps": "scenic overlook",
            "vector_necesidades": {"movimiento": 40, "naturaleza": 90, "silencio": 85, "aire_fresco": 95, "creatividad": 70, "contemplacion": 100, "descanso": 70, "pausas_silencio": 90, "ext_vacio_existencial": -80}
        },
        {
            "id": 109, "titulo": "Clase de Meditación", "titulo_en": "Meditation Class",
            "porque": "Mente sobrecargada y estresada. Busca herramientas para la calma interna y la regulación de tu sistema nervioso.", "porque_en": "Overloaded and stressed mind. Seek tools for inner calm and nervous system regulation.",
            "que_hacer": "Asiste a una sesión de meditación guiada o a un centro de yoga. Concéntrate en la respiración y en soltar las tensiones.", "que_hacer_en": "Attend a guided meditation session or yoga center. Focus on your breathing and letting go of tension.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Centro de yoga o meditación.", "donde_en": "Yoga or meditation center.", "gps": "meditation class",
            "vector_necesidades": {"silencio": 100, "aprendizaje": 90, "contemplacion": 100, "descanso": 100, "organizacion": 80, "pausas_silencio": 100, "sis_nervioso_saturado": -90}
        },
        {
            "id": 110, "titulo": "Yoga al Aire Libre", "titulo_en": "Outdoor Yoga",
            "porque": "Mente acelerada y cuerpo tenso. Conecta con la naturaleza y respira consciente para equilibrar tu ser.", "porque_en": "Racing mind and tense body. Connect with nature and breathe consciously to balance your being.",
            "que_hacer": "Busca un parque tranquilo. Extiende tu mat o una toalla. Sigue una rutina de yoga o estiramientos sencillos al aire libre.", "que_hacer_en": "Find a quiet park. Lay your mat or towel. Follow a simple outdoor yoga or stretching routine.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Parque tranquilo.", "donde_en": "Quiet park.", "gps": "outdoor yoga park",
            "vector_necesidades": {"movimiento": 90, "naturaleza": 90, "silencio": 70, "aire_fresco": 95, "creatividad": 60, "contemplacion": 80, "descanso": 70, "motilidad_linfatica": 80, "oxigenacion": 90, "indicador_ansiedad": -60}
        },
        {
            "id": 111, "titulo": "Gimnasio Comunitario", "titulo_en": "Community Gym",
            "porque": "Necesitas liberar energía acumulada y convertir la tensión en fuerza. Activa tu cuerpo para depurar tu mente.", "porque_en": "Need to release accumulated energy and convert tension into strength. Activate your body to purify your mind.",
            "que_hacer": "Visita un gimnasio público o de bajo costo. Enfócate en una rutina de ejercicio o simplemente suda para liberar toxinas.", "que_hacer_en": "Visit a public or low-cost gym. Focus on an exercise routine or simply sweat to release toxins.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Gimnasio o centro deportivo.", "donde_en": "Gym or sports center.", "gps": "community gym",
            "vector_necesidades": {"movimiento": 100, "sudar": 80, "motilidad_linfatica": 90, "organizacion": 80, "risa": 40, "indicador_ansiedad": -70}
        },
        {
            "id": 112, "titulo": "Sendero Corto Natural", "titulo_en": "Short Nature Trail",
            "porque": "Sobrecarga de estímulos y desconexión. Desconéctate por un momento y camina en paz, absorbiendo la energía del entorno natural.", "porque_en": "Overload of stimuli and disconnection. Disconnect for a moment and walk in peace, absorbing the energy of the natural environment.",
            "que_hacer": "Encuentra un sendero natural cercano. Camina a paso ligero, observando la flora y fauna. Respira el aire puro de forma consciente.", "que_hacer_en": "Find a nearby nature trail. Walk briskly, observing the flora and fauna. Consciously breathe the pure air.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Sendero natural o bosque.", "donde_en": "Nature trail or forest.", "gps": "short nature trail",
            "vector_necesidades": {"movimiento": 85, "naturaleza": 100, "silencio": 80, "aire_fresco": 100, "contemplacion": 90, "descanso": 60, "sensorial_organica": 90, "oxigenacion": 90}
        },
        {
            "id": 113, "titulo": "Pista de Atletismo", "titulo_en": "Running Track",
            "porque": "Mente acelerada y energía extra acumulada. Quema esa tensión. Enfoca tu ritmo y recupera el control de tu cuerpo.", "porque_en": "Racing mind and accumulated extra energy. Burn off that tension. Focus your rhythm and regain control of your body.",
            "que_hacer": "Dirígete a una pista pública. Corre o camina a tu propio paso. Concéntrate en la sensación de tus músculos y el aire.", "que_hacer_en": "Go to a public track. Run or walk at your own pace. Concentrate on the sensation of your muscles and the air.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Pista de atletismo pública.", "donde_en": "Public running track.", "gps": "public running track",
            "vector_necesidades": {"movimiento": 100, "sudar": 80, "motilidad_linfatica": 90, "aire_fresco": 90, "organizacion": 70, "indicador_ansiedad": -70}
        },
        {
            "id": 114, "titulo": "Mercado de Agricultores", "titulo_en": "Farmers Market",
            "porque": "Días monótonos. Necesitas nuevos estímulos sensoriales: sabores, olores y la energía de la comunidad local. Apoya lo local.", "porque_en": "Monotonous days. You need new sensory stimuli: tastes, smells, and the energy of the local community. Support local.",
            "que_hacer": "Visita un mercado local de agricultores. Prueba algo nuevo. Habla con los vendedores y siente la conexión humana real.", "que_hacer_en": "Visit a local farmers market. Try something new. Talk to vendors and feel the real human connection.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Mercado de agricultores.", "donde_en": "Farmers market.", "gps": "farmers market",
            "vector_necesidades": {"movimiento": 60, "naturaleza": 50, "comunidad": 90, "alimentacion": 100, "risa": 70, "sensorial_organica": 90, "nutricion_real": 80, "soc_desconexion": -80}
        },
        {
            "id": 115, "titulo": "Exposición de Arte", "titulo_en": "Art Exhibition",
            "porque": "Mente atrapada en un bucle. Busca inspiración y despierta tu creatividad. Permite que el arte te hable en silencio.", "porque_en": "Mind trapped in a loop. Seek inspiration and awaken your creativity. Let art speak to you in silence.",
            "que_hacer": "Visita una galería o museo local. Observa el arte con atención plena y reflexiona en silencio sobre las emociones que te provoca.", "que_hacer_en": "Visit a local gallery or museum. Observe the art with full attention and reflect in silence on the emotions it evokes.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Galería de arte o museo.", "donde_en": "Art gallery or museum.", "gps": "art gallery",
            "vector_necesidades": {"movimiento": 40, "silencio": 70, "creatividad": 100, "aprendizaje": 90, "contemplacion": 95, "descanso": 60, "pausas_silencio": 80, "ext_estancamiento": -80}
        },
        {
            "id": 116, "titulo": "Parque de Patinaje", "titulo_en": "Skate Park",
            "porque": "Necesitas una inyección de energía visual y conectar con el juego y la libertad del movimiento. Observa la vitalidad.", "porque_en": "Need an injection of visual energy and to connect with play and freedom of movement. Observe the vitality.",
            "que_hacer": "Acércate a un skate park. Observa a los patinadores, su habilidad y la alegría de su movimiento. Siente la vitalidad del lugar.", "que_hacer_en": "Go to a skate park. Watch the skaters, their skill, and the joy of their movement. Feel the vitality of the place.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Skate park público.", "donde_en": "Public skate park.", "gps": "skate park",
            "vector_necesidades": {"movimiento": 70, "comunidad": 80, "juego": 100, "risa": 90, "creatividad": 80, "ext_vacio_existencial": -70}
        },
        {
            "id": 117, "titulo": "Librería de Segunda Mano", "titulo_en": "Used Bookstore",
            "porque": "Busca historias y conocimiento real para nutrir tu mente. Desconéctate del mundo digital y sumérgete en el aroma del papel.", "porque_en": "Seek real stories and knowledge to nourish your mind. Disconnect from the digital world and immerse yourself in the scent of paper.",
            "que_hacer": "Explora una librería de segunda mano. Busca títulos inesperados, déjate llevar por la serendipia y disfruta el silencio.", "que_hacer_en": "Explore a used bookstore. Look for unexpected titles, let serendipity guide you, and enjoy the silence.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Librería de segunda mano.", "donde_en": "Used bookstore.", "gps": "used bookstore",
            "vector_necesidades": {"silencio": 85, "creatividad": 90, "aprendizaje": 100, "contemplacion": 90, "descanso": 80, "pausas_silencio": 90, "ext_distraccion_cognitiva": -90}
        },
        {
            "id": 119, "titulo": "Paseo por el Puerto", "titulo_en": "Harbor Walk",
            "porque": "Mente cansada. Necesitas despejar la mente con aire fresco y las vistas al agua. Una caminata relajante para recuperar la calma.", "porque_en": "Tired mind. You need to clear your mind with fresh air and water views. A relaxing walk to regain calm.",
            "que_hacer": "Camina por el muelle o puerto. Observa los barcos, escucha el sonido del agua y siente la brisa marina. Conéctate con lo inmenso.", "que_hacer_en": "Walk along the dock or harbor. Watch the boats, listen to the sound of the water, and feel the sea breeze. Connect with the immense.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Puerto o muelle.", "donde_en": "Harbor or pier.", "gps": "harbor walk or pier",
            "vector_necesidades": {"movimiento": 70, "naturaleza": 80, "silencio": 60, "agua": 100, "aire_fresco": 95, "contemplacion": 90, "descanso": 80, "sensorial_organica": 90}
        },
        {
            "id": 120, "titulo": "Observatorio Local", "titulo_en": "Local Observatory",
            "porque": "Mente ansiosa y atrapada en lo pequeño. Busca una perspectiva universal. Maravíllate con el cosmos y relativiza tus preocupaciones.", "porque_en": "Anxious mind trapped in the small. Seek a universal perspective. Marvel at the cosmos and relativize your worries.",
            "que_hacer": "Visita un observatorio. Aprende sobre el universo y, si es posible, observa las estrellas. Siente la inmensidad del espacio.", "que_hacer_en": "Visit an observatory. Learn about the universe and, if possible, stargaze. Feel the immensity of space.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Observatorio astronómico.", "donde_en": "Astronomical observatory.", "gps": "astronomical observatory",
            "vector_necesidades": {"silencio": 90, "naturaleza": 70, "creatividad": 80, "aprendizaje": 100, "contemplacion": 100, "descanso": 90, "pausas_silencio": 90, "ext_vacio_existencial": -90}
        },
        {
            "id": 121, "titulo": "Banco en Plaza Céntrica", "titulo_en": "Bench in Central Plaza",
            "porque": "Necesitas observar el pulso de la vida sin participar directamente. Conéctate con la energía urbana mientras descansas y reflexionas.", "porque_en": "Need to observe the pulse of life without direct participation. Connect with urban energy while resting and reflecting.",
            "que_hacer": "Siéntate en un banco en una plaza concurrida. Observa a la gente pasar, sus expresiones, sus interacciones. Siente el flujo de la vida.", "que_hacer_en": "Sit on a bench in a busy plaza. Watch people pass by, their expressions, their interactions. Feel the flow of life.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Plaza pública o parque.", "donde_en": "Public plaza or park.", "gps": "public plaza",
            "vector_necesidades": {"movimiento": 20, "naturaleza": 60, "silencio": 30, "comunidad": 80, "contemplacion": 90, "descanso": 100, "soc_desconexion": -60}
        },
        {
            "id": 122, "titulo": "Paseo en Bote", "titulo_en": "Boat Ride",
            "porque": "Estrés acumulado. Necesitas desconexión total y la calma del agua. Flota tus preocupaciones y relaja tu mente.", "porque_en": "Accumulated stress. You need total disconnection and the calm of the water. Float your worries and relax your mind.",
            "que_hacer": "Realiza un paseo corto en bote por un lago o río. Siente la brisa, observa la inmensidad del agua y déjate llevar por el movimiento.", "que_hacer_en": "Take a short boat ride on a lake or river. Feel the breeze, observe the vastness of the water, and let yourself be carried by the movement.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Lago o río con alquiler de botes.", "donde_en": "Lake or river with boat rentals.", "gps": "boat rentals lake or river",
            "vector_necesidades": {"movimiento": 60, "naturaleza": 100, "silencio": 80, "agua": 100, "aire_fresco": 100, "contemplacion": 95, "descanso": 90, "indicador_ansiedad": -80}
        },
        {
            "id": 123, "titulo": "Jardín de Rocas/Zen", "titulo_en": "Rock/Zen Garden",
            "porque": "Mente agitada. Busca orden y armonía en un espacio diseñado para la calma. Centra tus pensamientos en la simplicidad.", "porque_en": "Agitated mind. Seek order and harmony in a space designed for calm. Center your thoughts on simplicity.",
            "que_hacer": "Encuentra un jardín de rocas o japonés. Observa las formas, la disposición de las piedras y el rastrillo de la arena. Medita en su calma.", "que_hacer_en": "Find a rock or Japanese garden. Observe the shapes, the arrangement of the stones, and the raking of the sand. Meditate in its calm.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Jardín de rocas o japonés.", "donde_en": "Rock or Japanese garden.", "gps": "zen garden",
            "vector_necesidades": {"naturaleza": 90, "silencio": 100, "contemplacion": 100, "descanso": 95, "organizacion": 100, "pausas_silencio": 100, "sis_nervioso_saturado": -90}
        },
        {
            "id": 124, "titulo": "Parque de Perros", "titulo_en": "Dog Park",
            "porque": "Necesitas risas y alegría genuina. Observa el juego inocente de los perros y su interacción. Contagia la energía positiva.", "porque_en": "Need genuine laughter and joy. Observe the innocent play of dogs and their interaction. Catch the positive energy.",
            "que_hacer": "Visita un parque de perros. Observa su interacción, sus carreras y su felicidad. Permite que esa alegría te contagie y te haga sonreír.", "que_hacer_en": "Visit a dog park. Observe their interaction, their runs, and their happiness. Let that joy spread to you and make you smile.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Parque de perros local.", "donde_en": "Local dog park.", "gps": "dog park",
            "vector_necesidades": {"movimiento": 70, "naturaleza": 70, "comunidad": 90, "juego": 100, "risa": 100, "soc_aislamiento": -80}
        },
        {
            "id": 125, "titulo": "Música en Vivo Suave", "titulo_en": "Calm Live Music",
            "porque": "Mente estresada. Necesitas una experiencia sensorial que te calme y te desconecte. Permite que la música sane tu alma.", "porque_en": "Stressed mind. You need a sensory experience that calms and disconnects you. Let music heal your soul.",
            "que_hacer": "Encuentra un lugar con música en vivo tranquila (jazz, acústica). Escucha, relájate y disfruta del momento presente sin distracciones.", "que_hacer_en": "Find a place with calm live music (jazz, acoustic). Listen, relax, and enjoy the present moment without distractions.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Bar o cafetería con música suave.", "donde_en": "Bar or cafe with calm music.", "gps": "live jazz bar",
            "vector_necesidades": {"silencio": 10, "creatividad": 90, "comunidad": 70, "musica": 100, "contemplacion": 90, "descanso": 80, "sis_nervioso_saturado": -70}
        },
        {
            "id": 126, "titulo": "Observación de Nubes", "titulo_en": "Cloud Gazing",
            "porque": "Mente agitada y llena de pensamientos rápidos. Enfoca tu mirada en la inmensidad del cielo y deja que los pensamientos pasen como las nubes.", "porque_en": "Agitated mind full of racing thoughts. Focus your gaze on the vastness of the sky and let thoughts pass like clouds.",
            "que_hacer": "Busca un lugar abierto, recuéstate en el césped o en un banco y observa el movimiento lento y constante de las nubes en el cielo.", "que_hacer_en": "Find an open space, lie down on the grass or a bench, and watch the slow and constant movement of the clouds in the sky.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Parque o campo abierto.", "donde_en": "Park or open field.", "gps": "open field for cloud gazing",
            "vector_necesidades": {"naturaleza": 95, "silencio": 90, "aire_fresco": 90, "contemplacion": 100, "descanso": 95, "pausas_silencio": 95, "ext_distraccion_cognitiva": -80}
        },
        {
            "id": 127, "titulo": "Ruta en Bicicleta Urbana", "titulo_en": "Urban Bike Route",
            "porque": "Necesitas liberar tensión y moverte rápido para activar tu cuerpo y mente. Siente el viento en tu cara y explora tu entorno desde otra perspectiva.", "porque_en": "Need to release tension and move fast to activate your body and mind. Feel the wind on your face and explore your surroundings from a different perspective.",
            "que_hacer": "Encuentra un carril bici seguro o un parque con una ruta. Pedalea a tu propio ritmo, siente la velocidad y el control sobre tu cuerpo y tu camino.", "que_hacer_en": "Find a safe bike lane or a park with a route. Pedal at your own pace, feel the speed and control over your body and your path.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Carril bici o parque con ruta.", "donde_en": "Bike lane or park with route.", "gps": "bike lane or route",
            "vector_necesidades": {"movimiento": 100, "naturaleza": 60, "aire_fresco": 95, "juego": 70, "contemplacion": 60, "descanso": 30, "motilidad_linfatica": 90, "sudar": 70, "indicador_ansiedad": -60}
        },
        {
            "id": 128, "titulo": "Cine al aire libre", "titulo_en": "Outdoor Cinema",
            "porque": "Mente aburrida de lo predecible. Necesitas un cambio de ambiente y una nueva perspectiva para disfrutar una historia en un entorno diferente y relajante.", "porque_en": "Mind bored of predictability. Need a change of scenery and a new perspective to enjoy a story in a different and relaxing setting.",
            "que_hacer": "Asiste a una proyección de cine al aire libre. Sumérgete en la película, en el ambiente y disfruta de la experiencia sin las distracciones de la pantalla pequeña.", "que_hacer_en": "Attend an outdoor cinema screening. Immerse yourself in the film and atmosphere, and enjoy the experience without the distractions of the small screen.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Parque o plaza con proyecciones.", "donde_en": "Park or plaza with screenings.", "gps": "outdoor cinema",
            "vector_necesidades": {"movimiento": 30, "naturaleza": 60, "creatividad": 90, "comunidad": 80, "aprendizaje": 70, "juego": 50, "contemplacion": 80, "descanso": 70, "ext_espejismo_evasion": -70}
        },
        {
            "id": 129, "titulo": "Tour Histórico a Pie", "titulo_en": "Historical Walking Tour",
            "porque": "Mente agotada de lo predecible y sin dirección. Necesitas una inyección de conocimiento y un suave movimiento. Aprende mientras caminas y conectas con la historia.", "porque_en": "Mind exhausted by predictability and without direction. You need an injection of knowledge and gentle movement. Learn as you walk and connect with history.",
            "que_hacer": "Busca un tour a pie gratuito o de bajo costo por tu ciudad. Descubre historias locales, arquitectura y siente la energía de los lugares con cada paso.", "que_hacer_en": "Find a free or low-cost walking tour of your city. Discover local stories, architecture, and feel the energy of the places with each step.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Centro histórico de la ciudad.", "donde_en": "City historical center.", "gps": "free walking tour",
            "vector_necesidades": {"movimiento": 80, "comunidad": 70, "aprendizaje": 100, "contemplacion": 80, "descanso": 60, "motilidad_linfatica": 70, "ext_estancamiento": -80}
        },
        {
            "id": 130, "titulo": "Piscina Pública", "titulo_en": "Public Pool",
            "porque": "Cuerpo tenso, mente agitada. El agua relaja y el movimiento controlado calma. Flota tus preocupaciones y permite la depuración de tu cuerpo.", "porque_en": "Tense body, agitated mind. Water relaxes and controlled movement calms. Float your worries away and allow your body to detox.",
            "que_hacer": "Visita una piscina pública. Date un chapuzón, nada unos largos o simplemente relájate en el agua. Siente la ingravidez y la frescura.", "que_hacer_en": "Visit a public pool, take a dip, swim laps, or just relax in the water. Feel the weightlessness and coolness.",
            "cuando": WHEN_ES, "cuando_en": WHEN_EN, "para_que": FOR_WHAT_ES, "para_que_en": FOR_WHAT_EN,
            "donde": "Piscina municipal o comunitaria.", "donde_en": "Municipal or community pool.", "gps": "public swimming pool",
            "vector_necesidades": {"movimiento": 90, "agua": 100, "sudar": 70, "juego": 80, "contemplacion": 70, "descanso": 90, "motilidad_linfatica": 85, "indicador_ansiedad": -70}
        },
    ],
}

BIG_TECH_RESOURCES = {
    "spotify_audio_es": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_es": "https://www.youtube.com/results?search_query=sonidos+naturaleza+relajantes",
    "spotify_audio_en": "https://open.spotify.com/genre/mood/relax-stress-relief",
    "youtube_audio_en": "https://www.youtube.com/results?search_query=nature+sounds+relaxing",
}

# ============================================================
# CWRE V2
# SCORE INTELIGENTE (REFINADO)
# ============================================================
def score_coincidencia(
    perfil_local,
    vector_necesidades,
    historial=None,
    mission_id=None
):
    historial = historial or []
    score = 0
    # --------------------------------------------------
    # Coincidencia principal: Cuanto más cerca esté la necesidad
    # del usuario del objetivo de la misión, mayor el score.
    # --------------------------------------------------
    for necesidad, objetivo in vector_necesidades.items():
        if necesidad in ["indicador_ansiedad", "soc_desconexion", "soc_aislamiento", "ext_vacio_existencial", "ext_estancamiento", "fis_sobrecarga_cortisol", "sis_nervioso_saturado", "fis_desconexion_presencia", "soc_automatismo_masa", "soc_validacion_rapida", "comercio_compulsivo", "ext_espejismo_evasion", "ext_distraccion_cognitiva"]:
            # These are "problem indicators", not direct needs to fulfill in a positive way for scoring.
            # They will be used to influence the profile or trigger protocols.
            continue
        usuario = perfil_local.get(necesidad, DEFAULT_NECESSITY_VECTOR.get(necesidad, 50))
        diferencia = abs(usuario - objetivo)
        score += (100 - diferencia) * 0.5

    # --------------------------------------------------
    # Priorizar necesidades insatisfechas (altas en perfil)
    # y que la misión las cubra bien.
    # --------------------------------------------------
    for necesidad, valor_usuario in perfil_local.items():
        if necesidad in ["indicador_ansiedad", "soc_desconexion", "soc_aislamiento", "ext_vacio_existencial", "ext_estancamiento", "fis_sobrecarga_cortisol", "sis_nervioso_saturado", "fis_desconexion_presencia", "soc_automatismo_masa", "soc_validacion_rapida", "comercio_compulsivo", "ext_espejismo_evasion", "ext_distraccion_cognitiva"]:
            continue
        if valor_usuario < 30 and vector_necesidades.get(necesidad, 0) > 70: # User has low need, mission satisfies it well
            score += (100 - valor_usuario) * 0.3 # Higher bonus for bringing low values up
        elif valor_usuario < 50 and vector_necesidades.get(necesidad, 0) > 50:
             score += (100 - valor_usuario) * 0.1

    # --------------------------------------------------
    # Priorizar solución de "problemas" detectados en FASE 4
    # --------------------------------------------------
    # Score for reducing negative indicators
    for problem_key in ["indicador_ansiedad", "soc_desconexion", "soc_aislamiento", "ext_vacio_existencial", "ext_estancamiento", "fis_sobrecarga_cortisol", "sis_nervioso_saturado", "fis_desconexion_presencia", "soc_automatismo_masa", "soc_validacion_rapida", "comercio_compulsivo", "ext_espejismo_evasion", "ext_distraccion_cognitiva"]:
        if perfil_local.get(problem_key, 0) > 0 and vector_necesidades.get(problem_key, 0) < 0: # If user has problem, and mission reduces it (negative value)
            score += abs(vector_necesidades[problem_key]) * (perfil_local[problem_key] / 100) * 0.5 # Scale by how much problem the user has

    # --------------------------------------------------
    # Penalización por repetición histórica y bonus por exploración
    # --------------------------------------------------
    if mission_id is not None:
        score -= penalizacion_historial(mission_id, historial)
        score += bonus_exploracion(mission_id, historial)
   
    return round(max(0, score), 2)

# ============================================================
# Selección por Ranking Inteligente
# ============================================================
def seleccionar_por_ranking(candidatos):
    if not candidatos:
        return None
   
    candidatos = sorted(candidatos, key=lambda x: x["score"], reverse=True)
   
    if not candidatos:
        return None

    mejor_score = candidatos[0]["score"]
   
    # Si todos tienen un score bajo, y todos son iguales, elige uno al azar.
    if mejor_score <= 100 and all(c["score"] == mejor_score for c in candidatos):
        return random.choice(candidatos)

    score_umbral = max(mejor_score * 0.8, mejor_score - 150)
   
    mejores_candidatos_para_eleccion = [
        c for c in candidatos if c["score"] >= score_umbral
    ]
   
    if len(mejores_candidatos_para_eleccion) == 1:
        return mejores_candidatos_para_eleccion[0]

    pesos = [c["score"] for c in mejores_candidatos_para_eleccion]
    # Asegúrate de que ningún peso sea cero o negativo para random.choices
    pesos = [max(1, p) for p in pesos]

    return random.choices(mejores_candidatos_para_eleccion, weights=pesos, k=1)[0]


# ============================================================
# CWRE V2
# Selector Universal de Misiones
# ============================================================
def seleccionar_mision_inteligente(
    misiones,
    perfil_local,
    historial=None
):
    historial = historial or []
    candidatos = []
    for mision in misiones:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
       
        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial,
            mission_id=mision["id"]
        )
        candidatos.append({
            "mision": mision,
            "score": score
        })
    seleccion = seleccionar_por_ranking(candidatos)
    if seleccion == None:
        return random.choice(misiones) if misiones else None
    return seleccion["mision"]

# ============================================================
# CWRE V2.1
# Seleccionar N misiones inteligentes y diversas (para modo SALIR)
# ============================================================
def seleccionar_n_misiones_inteligentes(
    n,
    misiones,
    perfil_local,
    historial_actual=None,
    parsed_entities=None # New parameter to influence selection
):
    historial_actual = historial_actual or []
    parsed_entities = parsed_entities or {"categories": [], "brands": [], "entities_raw": []}

    candidatos_base = []
    for mision in misiones:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial_actual,
            mission_id=mision["id"]
        )
        candidatos_base.append({
            "mision": mision,
            "score": score
        })

    candidatos_base.sort(key=lambda x: x["score"], reverse=True)
    
    seleccionadas = []
    ids_seleccionados = set()
    
    # Prioriza las de mayor score y las que no estén en el historial
    for cand in candidatos_base:
        if len(seleccionadas) >= n:
            break
        if cand["mision"]["id"] not in ids_seleccionados and cand["mision"]["id"] not in historial_actual:
            es_diversa = True
            for sel_mision in seleccionadas:
                distancia = diversidad_vector(
                    cand["mision"].get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                    sel_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
                )
                if distancia < 100:
                    es_diversa = False
                    break
            if es_diversa:
                seleccionadas.append(cand["mision"])
                ids_seleccionados.add(cand["mision"]["id"])
    
    # Si aún no tenemos suficientes, toma las siguientes mejores aunque no sean tan diversas
    for cand in candidatos_base:
        if len(seleccionadas) >= n:
            break
        if cand["mision"]["id"] not in ids_seleccionados and cand["mision"]["id"] not in historial_actual:
            seleccionadas.append(cand["mision"])
            ids_seleccionados.add(cand["mision"]["id"])

    # Fallback: si aún no hay suficientes y el historial se ha agotado, reinicia y toma al azar
    if len(seleccionadas) < n and len(misiones) >= n:
        temp_misiones = [m for m in misiones if m["id"] not in ids_seleccionados]
        if len(temp_misiones) < n - len(seleccionadas):
            temp_misiones = misiones # Si no hay suficientes nuevas, recicla todo el catálogo
        random.shuffle(temp_misiones)
        for mision in temp_misiones:
            if len(seleccionadas) >= n:
                break
            if mision["id"] not in ids_seleccionados:
                seleccionadas.append(mision)
                ids_seleccionados.add(mision["id"])

    while len(seleccionadas) < n and len(misiones) > len(seleccionadas):
        mision_aleatoria = random.choice(misiones)
        if mision_aleatoria["id"] not in ids_seleccionados:
            seleccionadas.append(mision_aleatoria)
            ids_seleccionados.add(mision_aleatoria["id"])

    return seleccionadas[:n]


# ============================================================
# Filtrar historial (para disponibilidad de misiones)
# ============================================================
def filtrar_historial(misiones, historial):
    historial = historial or []
    disponibles = [
        m
        for m in misiones
        if m["id"] not in historial
    ]
    return disponibles

# ============================================================
# CASA V2
# Selección inteligente de misiones domésticas
# ============================================================
def seleccionar_misiones_casa_inteligente(
    misiones,
    perfil_local,
    historial_casa=None,
    cantidad=3
):
    historial_casa = historial_casa or []
   
    disponibles = filtrar_historial(
        misiones,
        historial_casa
    )
   
    if len(disponibles) < cantidad * 2: # Si quedan muy pocas sin repetir, considera todo el catálogo de nuevo
        disponibles = misiones

    candidatos = []
    for mision in disponibles:
        mission_vector = mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)

        score = score_coincidencia(
            perfil_local=perfil_local,
            vector_necesidades=mission_vector,
            historial=historial_casa,
            mission_id=mision.get("id")
        )
        candidatos.append({
            "mision": mision,
            "score": score
        })
   
    candidatos.sort(
        key=lambda x: x["score"],
        reverse=True
    )
   
    resultado = []
    ids_en_resultado = set()
   
    # Intenta seleccionar misiones diversas y de alto score
    for candidato in candidatos:
        mision = candidato["mision"]
        if mision["id"] in ids_en_resultado:
            continue

        es_diversa = True
        for anterior_mision in resultado:
            distancia = diversidad_vector(
                mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR),
                anterior_mision.get("vector_necesidades", DEFAULT_NECESSITY_VECTOR)
            )
            if distancia < 60: # Umbral de diversidad para misiones CASA
                es_diversa = False
                break
       
        if es_diversa:
            resultado.append(mision)
            ids_en_resultado.add(mision["id"])
       
        if len(resultado) >= cantidad:
            break
           
    # Si no se alcanzan las 'cantidad' requeridas con diversidad, añade las siguientes mejores
    if len(resultado) < cantidad:
        for candidato in candidatos:
            mision = candidato["mision"]
            if mision["id"] not in ids_en_resultado:
                resultado.append(mision)
                ids_en_resultado.add(mision["id"])
            if len(resultado) >= cantidad:
                break
   
    # Fallback final: si aún no hay suficientes, toma las primeras 'cantidad'
    if len(resultado) < cantidad and len(misiones) >= cantidad:
        resultado = [c["mision"] for c in candidatos[:cantidad]]
       
    return resultado

@app.get("/")
async def index():
    """Serves the main HTML page."""
    return FileResponse('static/session.html')

# OPEN THAN GO SYSTEM - Kernel Absolute Engine V.7.0.0
# Company: May Roga LLC
# File: main.py - SECCIÓN 2 DE 2 (CWRE Logic)
@app.post("/api/mando-integral")
async def mando_integral(request: Request):
    """
    Main API endpoint for OPEN THAN GO.
    Receives user input and local preference profile to return a personalized recommendation.
    """
    payload = await request.json()
    opcion_usuario = str(payload.get("modo", "")).strip().upper()
    zip_code = str(payload.get("zip", "")).strip()
    estado = str(payload.get("estado", "FL")).strip()
    region = str(payload.get("region", "")).strip()
    mente = str(payload.get("mente", "aburrido")).lower()
    budget = str(payload.get("budget", "0"))
    perfil_tipo = str(payload.get("perfil", "solo")).lower()
    desahogo = str(payload.get("desahogo", "")).lower()
    lang = str(payload.get("lang", "es")).lower()
    consumed_entities_text = str(payload.get("consumed_entities", "")).strip().lower() # FASE 1

    if zip_code and not re.fullmatch(r"^\d{5}$", zip_code):
        return JSONResponse({"error": "Código Postal inválido. Debe ser 5 dígitos numéricos."}, status_code=400)
   
    perfil_local = payload.get("perfil_local", {})
    if not isinstance(perfil_local, dict):
        perfil_local = {}
   
    perfil_local = {
        **DEFAULT_NECESSITY_VECTOR,
        **{k: v for k, v in perfil_local.items() if k in DEFAULT_NECESSITY_VECTOR or k.startswith("indicador_") or k.startswith("soc_") or k.startswith("ext_") or k.startswith("fis_") or k.startswith("sis_")}
    }
    if "indicador_ansiedad" not in perfil_local:
        perfil_local["indicador_ansiedad"] = 0

    # FASE 4 & 3: Parse consumed entities and update profile based on "secuestro de significado"
    parsed_entities = parse_consumed_entities(consumed_entities_text)
    
    # Update profile based on detected problems/needs from FASE 4 (Secuestro del Significado)
    for category in parsed_entities["categories"]:
        meaning = CORPORATE_BRAND_MEANINGS.get(category + "_generic") # Check for generic category meaning
        if meaning and meaning["need_key"] in perfil_local:
            # For problem indicators, increase their value
            perfil_local[meaning["need_key"]] = min(100, perfil_local[meaning["need_key"]] + 20) 
            
    for brand in parsed_entities["brands"]:
        meaning = CORPORATE_BRAND_MEANINGS.get(brand) # Check for specific brand meaning
        if meaning and meaning["need_key"] in perfil_local:
            # For problem indicators, increase their value
            perfil_local[meaning["need_key"]] = min(100, perfil_local[meaning["need_key"]] + 30)

    # FASE 4 & 5 & 7: Try to determine a Biological Protocol or Safety Protocol first
    # This takes precedence over other mission types.
    biological_protocol_mission = determine_bio_protocol(mente, parsed_entities, lang)
    if biological_protocol_mission:
        # FASE 6: Calculate Factor_Contextual for this specific protocol
        biological_protocol_mission["factor_contextual"] = get_factor_contextual(biological_protocol_mission, parsed_entities)
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "PROTOCOLO_BIOLOGICO",
            "mision": biological_protocol_mission, # A single, specific biological protocol
            "historial_salir_actualizado": payload.get("historial_salir", []) # Pass back for frontend to update (no change yet)
        })

    # FASE 1: TERAPEUTIC STRESS INTERCEPTOR FILTER
    # Eliminar cualquier elemento que pueda aumentar el estrés del cliente.
    # Si el desahogo o las consumed_entities contienen palabras críticas, se fuerza una microacción de recuperación mental.
    sensitive_keywords = [
        "trabajo", "empleo", "job", "jobs", "work", "career", "interview", "resume", "cv", "curriculum",
        "linkedin", "indeed", "networking", "cliente", "client", "empresa", "company", "income",
        "earn money", "ganar dinero", "producir", "productividad", "buscar oportunidades",
        "buscar ofertas", "enviar currículo", "actualizar linkedin", "conseguir empleo",
        "salir a buscar trabajo", "metas profesionales", "presion economica", "presión económica",
        "biles", "deudas", "misery", "exploitation", "dinero", "economy", "oportunidades laborales", "solicitudes de empleo",
        "visitar empresas", "buscando clientes", "producir dinero", "obligaciones laborales",
        "responsabilidades", "tareas", "negocio", "negocios", "presión", "presiones"
    ]
    # Add brand-specific keywords for stress from FASE 4 to trigger recovery mission
    for brand, data in CORPORATE_BRAND_MEANINGS.items():
        if data["need_key"] in ["soc_validacion_rapida", "comercio_compulsivo", "fis_sobrecarga_cortisol", "sis_nervioso_saturado", "fis_desconexion_presencia", "soc_automatismo_masa", "ext_espejismo_evasion", "ext_distraccion_cognitiva"]:
            sensitive_keywords.append(brand)
    
    # Add mind states that are highly indicative of stress for this filter
    stress_mind_states = ["agotado", "cansado", "stand by", "estresado", "desesperado", "ansioso", "alterado", "deprimido", "monotonia", "atrapado", "rutina"]
    if mente in stress_mind_states:
        force_recovery_mission = True

    force_recovery_mission_from_input = False
    explicitly_seeking_job = any(phrase in desahogo for phrase in ["quiero buscar trabajo", "necesito un empleo", "busco trabajo", "find a job", "looking for work"])
    
    if (desahogo and not explicitly_seeking_job) or consumed_entities_text:
        text_to_check = (desahogo.lower() + " " + consumed_entities_text.lower()).strip()
        if any(keyword in text_to_check for keyword in sensitive_keywords):
            force_recovery_mission_from_input = True
            
    if force_recovery_mission or force_recovery_mission_from_input:
        opcion_usuario = "CASA" # Force CASA mode for recovery mission
        idioma = "EN" if lang.lower() == "en" else "ES"
        # Seleccionar una de las 10 nuevas microacciones (IDs 151 a 160)
        microacciones_ids = list(range(151, 161))
       
        # Filtrar misiones_completas para incluir solo las microacciones
        misiones_completas_casa = [m for m in BASE_MISIONES[f"CASA_{idioma}"] if m["id"] in microacciones_ids]
       
        if not misiones_completas_casa:
            misiones_completas_casa = BASE_MISIONES[f"CASA_{idioma}"]

        historial_casa = payload.get("historial_casa", [])
       
        info_seleccionada = seleccionar_mision_inteligente(
            misiones=misiones_completas_casa,
            perfil_local=perfil_local,
            historial=historial_casa
        )
       
        if not info_seleccionada:
            info_seleccionada = random.choice(misiones_completas_casa)
           
        historial_casa = actualizar_historial(historial_casa, info_seleccionada["id"], MAX_HISTORY_CASA)

        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": [info_seleccionada],
            "historial_casa_actualizado": historial_casa,
            "forced_recovery": True
        })

    # 1. DOMESTIC INTERVENTION (CASA MODE)
    if opcion_usuario == "CASA":
        idioma = "EN" if lang.lower() == "en" else "ES"
        misiones_completas = (
            BASE_MISIONES[f"CASA_{idioma}"]
        )
       
        historial_casa = payload.get("historial_casa", [])
       
        misiones_casa = seleccionar_misiones_casa_inteligente(
            misiones_completas,
            perfil_local,
            historial_casa,
            cantidad=3
        )
       
        for m in misiones_casa:
            historial_casa = actualizar_historial(historial_casa, m["id"], MAX_HISTORY_CASA)
       
        return JSONResponse({
            "DIRECCIONAMIENTO_MASTER": "INTERVENCION_DOMESTICA",
            "misiones": misiones_casa,
            "historial_casa_actualizado": historial_casa
        })

    # ============================================================
    # 2. FIELD ACTION (SALIR MODE - CWRE INTELLIGENT ENGINE V2)
    #    Ahora devuelve 3 opciones para que el frontend elija.
    # ============================================================
    opciones_salir_candidatas = BASE_MISIONES["SALIR_GENERAL"]
   
    historial_salir = payload.get(
        "historial_salir",
        []
    )
    
    # Selecciona 3 misiones diversas y de alto score
    misiones_seleccionadas_raw = seleccionar_n_misiones_inteligentes(
        n=3,
        misiones=opciones_salir_candidatas,
        perfil_local=perfil_local,
        historial_actual=historial_salir,
        parsed_entities=parsed_entities
    )

    final_misiones_para_frontend = []

    for info_seleccionada in misiones_seleccionadas_raw:
        precio_real = ""
        if budget == "0":
            precio_real = "GASTO: Cero dólares. Austeridad creativa para proteger tu mente hoy." if lang == "es" else "COST: Zero dollars. Creative austerity to protect your mind today."
        elif budget == "1":
            precio_real = "GASTO: Rango bajo. Un gustazo mínimo para romper la rutina." if lang == "es" else "COST: Low range. A minimal treat to break the routine."
        elif budget == "2":
            precio_real = "GASTO: Libre. El dinero es tu herramienta de escape hoy." if lang == "es" else "COST: Free. Money is your escape tool today."
       
        quienes_van = ""
        if perfil_tipo == "solo":
            quienes_van = "ACOMPAÑAMIENTO: Vas solo contigo mismo a recuperar tu centro." if lang == "es" else "COMPANIONSHIP: You go alone to regain your center."
        elif perfil_tipo == "familia":
            quienes_van = "ACOMPAÑAMIENTO: Entorno apto para el desahogo de tus niños y familia." if lang == "es" else "COMPANIONSHIP: Environment suitable for your children and family to unwind."
        elif perfil_tipo == "accesible":
            quienes_van = "ACOMPAÑAMIENTO: Ruta plana con acceso total por comodidad física o edad." if lang == "es" else "COMPANIONSHIP: Flat route with full access for physical comfort or age."
       
        titulo_ganador = info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) if lang == "en" else info_seleccionada["titulo"]
        donde_base = info_seleccionada.get("donde_en", info_seleccionada["donde"]) if lang == "en" else info_seleccionada["donde"]
       
        anclaje_geografico = zip_code
        map_base_url = "https://www.google.com/maps/search/?api=1&query="
        target_link = ""

        if lang == "en":
            guia_masticada = (
                f"TARGET: {info_seleccionada.get('titulo_en', info_seleccionada['titulo']) or ''}.\n"
                f"WHAT TO DO: {info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''}\n"
                f"WHY: {info_seleccionada.get('porque_en', info_seleccionada['porque']) or ''}\n"
                f"WHEN: {info_seleccionada.get('cuando_en', info_seleccionada['cuando']) or ''}\n"
                f"FOR WHAT: {info_seleccionada.get('para_que_en', info_seleccionada['para_que']) or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador_lang = (info_seleccionada.get("titulo_en", info_seleccionada["titulo"]) or "").upper()
            que_hacer_lang = info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''
        else:
            guia_masticada = (
                f"DESTINO: {info_seleccionada['titulo'] or ''}.\n"
                f"POR QUÉ: {info_seleccionada['porque'] or ''}\n"
                f"QUÉ HACER: {info_seleccionada['que_hacer'] or ''}\n"
                f"CUÁNDO: {info_seleccionada['cuando'] or ''}\n"
                f"PARA QUÉ: {info_seleccionada['para_que'] or ''}\n"
                f"{quienes_van}\n{precio_real}"
            )
            titulo_ganador_lang = (info_seleccionada["titulo"] or "").upper()
            que_hacer_lang = info_seleccionada['que_hacer'] or ''
       
        search_query_parts = []
        if perfil_tipo == "accesible":
            search_query_parts.append("wheelchair accessible")
        elif perfil_tipo == "familia":
            search_query_parts.append("family friendly")
       
        search_query_parts.append(info_seleccionada["gps"])
        if anclaje_geografico: # Only add zip if present
            search_query_parts.append(f"in {anclaje_geografico}")
       
        full_map_query_string = " ".join(search_query_parts)
        target_link = f"{map_base_url}{urllib.parse.quote_plus(full_map_query_string)}"
       
        final_vector_necesidades = {**DEFAULT_NECESSITY_VECTOR, **info_seleccionada.get("vector_necesidades", {})}

        # FASE 6: Calculate Factor_Contextual for general SALIR missions
        info_seleccionada["action_type"] = "general_salir" # Mark as general for contextual factor
        factor_contextual = get_factor_contextual(info_seleccionada, parsed_entities)

        final_misiones_para_frontend.append({
            "destino_id": info_seleccionada.get("id"),
            "destino_titulo": titulo_ganador_lang,
            "destino_titulo_en": info_seleccionada.get("titulo_en", info_seleccionada["titulo"]),
            "que_hacer": info_seleccionada["que_hacer"],
            "que_hacer_en": info_seleccionada.get("que_hacer_en", info_seleccionada["que_hacer"]),
            "destino_entorno": donde_base,
            "destino_instruccion": guia_masticada.strip(),
            "destino_instruccion_en": (
                f"TARGET: {info_seleccionada.get('titulo_en', info_seleccionada['titulo']) or ''}.\n"
                f"WHAT TO DO: {info_seleccionada.get('que_hacer_en', info_seleccionada['que_hacer']) or ''}\n"
                f"WHY: {info_seleccionada.get('porque_en', info_seleccionada['porque']) or ''}\n"
                f"WHEN: {info_seleccionada.get('cuando_en', info_seleccionada['cuando']) or ''}\n"
                f"FOR WHAT: {info_seleccionada.get('para_que_en', info_seleccionada['para_que']) or ''}\n"
                f"{quienes_van}\n{precio_real}"
            ).strip(),
            "destino_coordenadas_gps": target_link,
            "vector_entorno_seleccionado": final_vector_necesidades,
            "factor_contextual": factor_contextual, # FASE 6
            "action_type": "general_salir", # To distinguish from PROTOCOLO_BIOLOGICO on frontend
            "duration_seconds": 60 # Default duration for general SALIR
        })
   
    return JSONResponse({
        "DIRECCIONAMIENTO_MASTER": "ACCION_CAMPO",
        "misiones": final_misiones_para_frontend,
        "historial_salir_actualizado": historial_salir
    })

# Helper for parsing consumed entities
def parse_consumed_entities(entities_text):
    if not entities_text:
        return {"categories": [], "brands": [], "entities_raw": []}

    entities_raw = [e.strip().lower() for e in entities_text.split(',') if e.strip()]
    
    detected_categories = set()
    detected_brands = set()

    for entity in entities_raw:
        is_matched = False
        # Check against specific brands first
        for brand_name, brand_data in CORPORATE_BRAND_MEANINGS.items():
            if entity == brand_name or any(keyword in entity for keyword in INFRASTRUCTURE_KEYWORDS_MAPPING.get(brand_data.get("category", ""), [])):
                detected_brands.add(entity) # Add the raw entity
                detected_categories.add(brand_name) # Add the brand_name key for conceptual meaning
                is_matched = True
                break # Matched a specific brand or category keyword within an entity

        # Check against infrastructure keywords (broader categories)
        for category_key, keywords in INFRASTRUCTURE_KEYWORDS_MAPPING.items():
            if any(k in entity for k in keywords):
                detected_categories.add(category_key)
                is_matched = True
        
        if not is_matched:
            detected_brands.add(entity) # If nothing matched, treat as a generic entity/brand

    return {
        "categories": list(detected_categories),
        "brands": list(detected_brands),
        "entities_raw": entities_raw
    }

# Helper for determining FASE 5 & 7 protocols
def determine_bio_protocol(mind_state, parsed_entities, lang):
    lang_suffix = "_en" if lang == "en" else "_es"
    
    # Check for Safety Protocol first (FASE 7)
    is_driving_context = False
    for category in parsed_entities["categories"]:
        if "transport_high_speed" in category: # Check for category keyword in the parsed entity categories
            is_driving_context = True
            break
    
    # Specific mind states that trigger driving safety protocol
    driving_trigger_states = ["monotonia", "atrapado", "estresado", "paralizado", "perdido"]
    if mind_state in driving_trigger_states:
        if is_driving_context:
            safety_protocol = AUDIO_SAFETY_PROTOCOLS[f"driving_{lang}"]
            return {
                "id": f"AUDIO_SAFETY_DRIVING_{lang}",
                "name": safety_protocol[f"title{lang_suffix}"],
                "title_es": safety_protocol["title_es"],
                "description_es": safety_protocol["description_es"],
                "title_en": safety_protocol["title_en"],
                "description_en": safety_protocol["description_en"],
                "vector_necesidades": safety_protocol["vector_necesidades"],
                "duration_seconds": safety_protocol["duration_seconds"],
                "action_type": "audio_safety",
                "gps": "", # No GPS link for audio safety
                "audio_only_mode": True
            }

    # Check for Biological Protocols (FASE 5)
    for protocol in BIOLOGICAL_PROTOCOLS_MISSIONS:
        # Check if mind state triggers this protocol
        if mind_state in protocol[f"trigger_states{lang_suffix}"]:
            # Check if any entity (raw or category) triggers this protocol
            trigger_entity_keywords = protocol[f"trigger_entities{lang_suffix}"]
            
            # Check against raw entities provided by the user
            if any(keyword in ' '.join(parsed_entities["entities_raw"]) for keyword in trigger_entity_keywords):
                protocol_copy = protocol.copy()
                protocol_copy["action_type"] = "biological_protocol" # Explicitly set action type
                return protocol_copy
            
            # Check against detected categories if no raw match
            if any(any(k in cat for k in trigger_entity_keywords) for cat in parsed_entities["categories"]):
                protocol_copy = protocol.copy()
                protocol_copy["action_type"] = "biological_protocol"
                return protocol_copy
    
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
