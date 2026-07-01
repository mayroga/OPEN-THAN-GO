from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI(title="OPEN THAN GO CORE")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================
# CACHE
# =========================
CACHE = {
    "missions": None
}

# =========================
# LOAD JSON SAFE
# =========================
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# =========================
# MISSIONS ORDERED (1 → N LOOP)
# =========================
def load_missions():
    if CACHE["missions"]:
        return CACHE["missions"]

    files = sorted([
        f for f in os.listdir(BASE_DIR)
        if f.startswith("missions_") and f.endswith(".json")
    ])

    all_missions = []

    for file in files:
        data = load_json(os.path.join(BASE_DIR, file))
        if not data:
            continue

        missions = data.get("missions", []) if isinstance(data, dict) else data

        for m in missions:
            if isinstance(m, dict) and "id" in m:
                all_missions.append(m)

    all_missions = sorted(all_missions, key=lambda x: x["id"])

    CACHE["missions"] = {
        "missions": all_missions,
        "total": len(all_missions)
    }

    return CACHE["missions"]

# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

@app.get("/api/missions")
def missions():
    return load_missions()

@app.get("/api/missions/{mission_id}")
def mission_by_id(mission_id: int):
    data = load_missions()["missions"]

    for m in data:
        if m["id"] == mission_id:
            return m

    raise HTTPException(status_code=404, detail="Not found")

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# RUN
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
