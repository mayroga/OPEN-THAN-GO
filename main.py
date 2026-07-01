from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI(title="OPEN THAN GO SYSTEM")

# =========================================================
# 🔒 CORS (EVITA BLOQUEOS FRONTEND / FREEZES)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 📁 PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# =========================================================
# 🧠 LOAD JSON (SOURCE OF TRUTH - NO LOGIC HERE)
# =========================================================
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("JSON ERROR:", file_path, e)
        return None


def load_system():
    path = os.path.join(BASE_DIR, "system.json")  # tu JSON principal
    return load_json(path)


SYSTEM = load_system()


# =========================================================
# 🎯 MISSIONS (STRICT ORDER 1 → N, NO RANDOM, NO SKIP)
# =========================================================
def get_missions():
    if not SYSTEM:
        return {"missions": [], "total": 0}

    missions = SYSTEM.get("missions", [])

    # FILTRO + ORDEN ABSOLUTO
    missions = sorted(
        [m for m in missions if isinstance(m, dict) and "id" in m],
        key=lambda x: x["id"]
    )

    return {
        "missions": missions,
        "total": len(missions),
        "range": SYSTEM.get("rng", "1-N")
    }


# =========================================================
# 📖 STORIES (SI EXISTEN EN JSON)
# =========================================================
def get_stories():
    if not SYSTEM:
        return {"stories": [], "total": 0}

    stories = SYSTEM.get("stories", [])

    if isinstance(stories, dict):
        stories = stories.get("stories", [])

    stories = sorted(
        [s for s in stories if isinstance(s, dict) and "id" in s],
        key=lambda x: x["id"]
    )

    return {
        "stories": stories,
        "total": len(stories)
    }


# =========================================================
# 🌐 FRONTEND
# =========================================================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))


@app.get("/session")
def session():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))


# =========================================================
# 📡 API - MISSIONS (SOURCE OF TRUTH)
# =========================================================
@app.get("/api/missions")
def api_missions():
    return get_missions()


# =========================================================
# 📡 API - STORIES
# =========================================================
@app.get("/api/stories")
def api_stories():
    return get_stories()


# =========================================================
# 🎯 GET SINGLE MISSION (DIRECT ACCESS)
# =========================================================
@app.get("/api/missions/{mission_id}")
def mission_by_id(mission_id: int):
    data = get_missions()["missions"]

    for m in data:
        if m["id"] == mission_id:
            return m

    raise HTTPException(status_code=404, detail="Mission not found")


# =========================================================
# 🧪 HEALTH CHECK
# =========================================================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": SYSTEM.get("sys") if SYSTEM else None
    }
