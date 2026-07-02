// OPEN THAN GO SYSTEM - Frontend Engine v4 FINAL (FIXED)
// Company: May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

// ------------------------------
// SAFE GET
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// TITLE GLOBAL FIX
// ------------------------------
function setTitle(type, emotion = "neutral") {
    const el = get("interactive-title");
    if (!el) return;

    if (tipoEscapeGlobal === "Casa") {
        el.innerText = "OPEN ◯ THAN GO";
        return;
    }

    if (emotion === "stress") el.innerText = "OPEN ◉ THAN GO";
    else if (emotion === "monotony") el.innerText = "OPEN — THAN GO";
    else if (emotion === "low") el.innerText = "OPEN ○ THAN GO";
    else el.innerText = type === "Salida" ? "OPEN ◎ THAN GO" : "OPEN ◯ THAN GO";
}

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = get("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ------------------------------
// MODOS
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;

    get("m-salir")?.classList.toggle("active", esSalir);
    get("m-casa")?.classList.toggle("active", !esSalir);

    setTitle(esSalir ? "Salida" : "Casa");
}

// ------------------------------
// PRESUPUESTO
// ------------------------------
function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        const el = get(`b-${v}`);
        if (el) el.classList.toggle("active", v === opcion);
    });
}

// ------------------------------
// LANGUAGE SAFE
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;
    get("lang-es")?.classList.toggle("active", lang === "es");
    get("lang-en")?.classList.toggle("active", lang === "en");
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function solicitarEscape() {

    const estadoRaw = (get("inp-state")?.value || "FL").toUpperCase();
    const zip = (get("inp-zip")?.value || "").trim();

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: zip,
        estado: estadoRaw,
        region: get("inp-region")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";

    const res = await fetch("/api/open-than-go", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    get("wrapper-loader").style.display = "none";
    get("wrapper-interactive").style.display = "block";

    // 🔥 FIX CRÍTICO: backend manda "mision" no "mission"
    pasosMisionGlobal = data.mision?.b || [];
    datosLugarGlobal = data.lugar || null;
    tipoEscapeGlobal = data.tipo || "Salida";

    indicePasoActual = 0;

    setTitle(data.tipo, detectEmotion(payload.desahogo));

    render();
}

// ------------------------------
// EMOTION FIX (IMPORTANTE PARA TU BUG FL/INDIANAPOLIS)
// ------------------------------
function detectEmotion(text = "") {
    text = text.toLowerCase();

    if (text.includes("estres") || text.includes("trabajo")) return "stress";
    if (text.includes("aburrido") || text.includes("rutina")) return "monotony";
    if (text.includes("cansado") || text.includes("energia")) return "low";

    return "neutral";
}

// ------------------------------
// RENDER CORE
// ------------------------------
function render() {

    const cont = get("step-content");

    if (indicePasoActual >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
            get("btn-maps-action").style.display = "block";
            get("btn-maps-action").href = datosLugarGlobal.gps_link || "#";

            cont.innerHTML = `
                <div>
                    <h3>Tu destino</h3>
                    <p>${datosLugarGlobal.name}</p>
                    <p>${datosLugarGlobal.address}</p>
                </div>
            `;
        }

        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    const text = paso?.story?.es || paso?.tx || "";

    cont.innerHTML = `<div>${text}</div>`;

    if ("speechSynthesis" in window) {
        speechSynthesis.cancel();
        speechSynthesis.speak(new SpeechSynthesisUtterance(text));
    }

    get("btn-next").style.display = "block";
    get("btn-next").onclick = () => {
        indicePasoActual++;
        render();
    };
}
