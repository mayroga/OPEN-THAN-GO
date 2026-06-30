import json
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Servir la carpeta static nativamente
app.mount("/static", StaticFiles(directory="static"), name="static")

class DiagnosticoPayload(BaseModel):
    puedes_salir: bool = True
    idioma: str = "es"
    zip_code: str = ""
    estado: str = "FL"
    bolsillo: str = "cero"
    texto_libre: str = ""

def cargar_mision_tvid_desde_archivos(categoria_emocional: str, bolsillo_usuario: str):
    archivos_kamizen = ['missions_01_07.json', 'missions_08_14.json', 'missions_15_21.json']
    todas_las_tvid = []
    
    for nombre_archivo in archivos_kamizen:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for m in data.get("missions", []):
                    if m.get("id", 0) >= 1:
                        todas_las_tvid.append(m)
        except Exception as e:
            print(f"Error cargando {nombre_archivo}: {e}")

    filtradas = [
        m for m in todas_las_tvid 
        if m.get("cat") == categoria_emocional and bolsillo_usuario in m.get("pocket_match", ["cero", "moderado", "libre"])
    ]
    
    if filtradas:
        return random.choice(filtradas)
    elif todas_las_tvid:
        return random.choice(todas_las_tvid)
    else:
        return None

@app.get("/")
async def home():
    return FileResponse("static/session.html")

@app.post("/diagnostico-kamizen")
async def diagnostico_kamizen(payload: DiagnosticoPayload):
    puedes_salir = payload.puedes_salir
    idioma = payload.idioma
    zip_code = payload.zip_code.strip()
    estado = payload.estado.strip()
    bolsillo = payload.bolsillo
    texto_libre = payload.texto_libre.lower()

    categoria_detectada = "bien"
    if any(x in texto_libre for x in ["error", "biles", "cuenta", "dinero", "mal"]):
        categoria_detectada = "mal"
    elif any(x in texto_libre for x in ["aburrid", "niñ", "hijo", "kid"]):
        categoria_detectada = "nino"

    mision_tvid = cargar_mision_tvid_desde_archivos(categoria_detectada, bolsillo)
    if not mision_tvid:
        return JSONResponse(status_code=400, content={"error": "No misiones disponibles"})

    bloques_processed = []
    for comando in mision_tvid.get("b", []):
        bloque_clon = comando.copy()
        
        for campo in ["tx", "inf", "story", "c"]:
            if campo in bloque_clon and isinstance(bloque_clon[campo], dict):
                bloque_clon[campo] = bloque_clon[campo].get(idioma, bloque_clon[campo].get('es', ''))
                
        if bloque_clon.get("t") == "d":
            if isinstance(bloque_clon.get("q"), dict):
                bloque_clon["q"] = bloque_clon["q"].get(idioma, bloque_clon["q"].get('es', ''))
            if "op" in bloque_clon:
                bloque_clon["op"] = [op.get(idioma, op.get('es', '')) if isinstance(op, dict) else op for op in bloque_clon["op"]]
            if "ex" in bloque_clon:
                bloque_clon["ex"] = [ex.get(idioma, ex.get('es', '')) if isinstance(ex, dict) else ex for ex in bloque_clon["ex"]]
                
        bloques_processed.append(bloque_clon)

    if not puedes_salir:
        titulo = "Escape de Interiores: OPEN THAN GO" if idioma == 'es' else "Indoor Escape: OPEN THAN GO"
        return JSONResponse(content={
            "modalidad": "indoor",
            "titulo": titulo,
            "lugar": "Tu espacio seguro en casa / Your home safe space",
            "bloques_interactivos": bloques_processed,
            "url_maps": None
        })
    else:
        if not zip_code or len(zip_code) != 5:
            zip_code = "33101"
            
        tipo_mapa = "parks"
        if categoria_detectada == "nino":
            tipo_mapa = "family+parks+playground"
        elif categoria_detectada == "mal":
            tipo_mapa = "nature+reserves+scenic"

        query_busqueda = f"{tipo_mapa}+in+{zip_code}+{estado}+USA"
        url_maps_gratis = f"https://google.com{query_busqueda}"
        
        titulo_out = "Plan de Escape Abierto: OPEN THAN GO" if idioma == 'es' else "Open Escape Plan: OPEN THAN GO"
        
        instruccion_viaje = {
            "t": "h",
            "tx": f"Dirígete al área abierta en tu zona postal {zip_code}. Al llegar, ejecuta tu secuencia:" if idioma == 'es' else f"Drive to the open space in your zip code {zip_code}. Upon arrival, start your sequence:"
        }
        bloques_processed.insert(0, instruccion_viaje)
        
        return JSONResponse(content={
            "modalidad": "outdoor",
            "titulo": titulo_out,
            "lugar": f"Zona de libertad recomendada en {zip_code}, {estado}",
            "bloques_interactivos": bloques_processed,
            "url_maps": url_maps_gratis
        })
