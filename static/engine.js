/* =========================================================
   OPEN THAN GO ENGINE vFINAL CLEAN
   SINGLE BRAIN + LINEAR FLOW 1 → 27
========================================================= */

const state = {
    missions: [],
    i: 0,
    b: 0,
    lang: "es",
    running: false,
    params: {} // Guarda los datos del formulario
};

window.addEventListener("load", async () => {
    await boot();
});

async function boot() {
    try {
        const response = await fetch("/api/missions");
        const data = await response.json();
        state.missions = (data.missions || []).sort((a, b) => a.id - b.id);
        intro();
    } catch (e) {
        document.getElementById("app").innerHTML = "<h1>Error de conexión</h1>";
    }
}

/* =========================
   UI FORMULARIO (INTRO)
========================= */
function intro() {
    document.getElementById("app").innerHTML = `
        <div class="header-app">
            <div class="lang-bar">
                <button class="btn-lang ${state.lang === 'es' ? 'active' : ''}" onclick="setLang('es')">ES</button>
                <button class="btn-lang ${state.lang === 'en' ? 'active' : ''}" onclick="setLang('en')">EN</button>
            </div>
            <h1>OPEN THAN GO</h1>
            <p>Tu escape emocional inteligente</p>
        </div>
        <div class="form-group">
            <label>Estado</label>
            <select id="inp-state"><option value="FL">Florida</option><option value="TX">Texas</option><option value="CA">California</option></select>
        </div>
        <div class="form-group">
            <label>ZIP Code</label>
            <input id="inp-zip" maxlength="5" placeholder="Ej: 33101">
        </div>
        <button class="btn-trigger" onclick="startEngine()">GENERAR ESCAPE</button>
    `;
}

function startEngine() {
    state.params = { state: document.getElementById("inp-state").value, zip: document.getElementById("inp-zip").value };
    state.running = true;
    render();
}

/* =========================
   RENDER CENTRAL
========================= */
function render() {
    if (!state.running) return intro();

    const app = document.getElementById("app");
    const mission = state.missions[state.i];
    if (!mission) return reset();

    const block = mission.b[state.b];
    if (!block) { nextMission(); return; }

    app.innerHTML = `
        <div class="topbar">
            <button onclick="reset()">X</button>
            <span>Misión ${mission.id}</span>
        </div>
        <div class="card">
            ${block.t === 'v' ? `<h2>${T(block.tx)}</h2>` : ''}
            ${block.story ? `<p>${T(block.story)}</p>` : ''}
            ${block.t === 'd' ? `
                <h3>${T(block.q)}</h3>
                ${block.op.map((o, idx) => `<button class="btn-next-step" onclick="answer(${idx}, ${block.c}, '${encodeURIComponent(JSON.stringify(block.ex))}')">${T(o)}</button>`).join('')}
            ` : `<button class="btn-next-step" onclick="nextBlock()">CONTINUAR</button>`}
        </div>
    `;
}

function T(obj) {
    if (typeof obj === "string") return obj;
    return obj[state.lang] || obj.en || "";
}

function setLang(l) { state.lang = l; render(); }

function nextBlock() { state.b++; render(); }

function nextMission() { state.i++; state.b = 0; render(); }

function reset() { state.running = false; state.i = 0; state.b = 0; intro(); }

function answer(idx, correct, ex) {
    const isCorrect = idx === correct;
    const explanation = JSON.parse(decodeURIComponent(ex));
    alert(isCorrect ? "¡BIEN!" : "Intenta de nuevo");
    nextBlock();
}
