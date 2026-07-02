// OPEN THAN GO SYSTEM - Frontend Engine v6 (STABLE + UX FIX)
// May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let intervaloRespiracion = null;
let intervaloTimer = null;
let tiempoRestante = 0;

// ----------------------------------------------------
// SAFE GET
// ----------------------------------------------------
const get = (id) => document.getElementById(id);

// ----------------------------------------------------
// VOZ CONTROL (SIN ESPANGLISH)
// ----------------------------------------------------
function hablar(texto) {
    try {
        window.speechSynthesis.cancel();

        const u = new SpeechSynthesisUtterance(texto);
        u.lang = idiomaActual === "es" ? "es-ES" : "en-US";

        // voz masculina si existe
        const voices = speechSynthesis.getVoices();
        const match = voices.find(v =>
            v.lang.startsWith(u.lang) && v.name.toLowerCase().includes("male")
        );

        if (match) u.voice = match;

        window.speechSynthesis.speak(u);
    } catch (e) {
        console.warn("Voice error:", e);
    }
}

// ----------------------------------------------------
// TRADUCCIÓN UI (NO ESPANGLISH)
// ----------------------------------------------------
const UI = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        state: "Estado",
        region: "Región",
        zip: "ZIP",
        budget: "Presupuesto",
        mode: "Modo",
        desahogo: "Cómo te sientes...",
        btn: "GENERAR ESCAPE",
        loader: "Procesando tu estado emocional...",
        inhale: "Inhala",
        exhale: "Exhala",
        breath_intro:
            "Vamos a hacer una respiración guiada para ayudarte a calmar tu mente. Inhala y exhala lentamente.",
        house_intro:
            "Has elegido quedarte en casa. Este modo está diseñado para bajar estrés en 10 minutos guiados.",
        exit_intro:
            "Te guiaremos a un lugar recomendado según tu estado emocional actual."
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State",
        region: "Region",
        zip: "ZIP",
        budget: "Budget",
        mode: "Mode",
        desahogo: "How do you feel...",
        btn: "GENERATE ESCAPE",
        loader: "Processing your emotional state...",
        inhale: "Inhale",
        exhale: "Exhale",
        breath_intro:
            "We will guide you through a breathing exercise to calm your mind. Inhale and exhale slowly.",
        house_intro:
            "You chose to stay home. This mode is designed to reduce stress in a 10-minute guided session.",
        exit_intro:
            "We will guide you to a recommended place based on your emotional state."
    }
};

// ----------------------------------------------------
// IDIOMA GLOBAL (UI + VOZ)
// ----------------------------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    const esBtn = get("lang-es");
    const enBtn = get("lang-en");

    if (esBtn && enBtn) {
        esBtn.classList.toggle("active", lang === "es");
        enBtn.classList.toggle("active", lang === "en");
    }

    const map = {
        "txt-subtitle": "subtitle",
        "lbl-state": "state",
        "lbl-region": "region",
        "lbl-zip": "zip"
    };

    Object.keys(map).forEach(id => {
        const el = get(id);
        if (el) el.innerText = UI[lang][map[id]];
    });

    const input = get("inp-text");
    if (input) input.placeholder = UI[lang].desahogo;

    const loader = get("txt-loader");
    if (loader) loader.innerText = UI[lang].loader;
}

// ----------------------------------------------------
// PRESUPUESTO
// ----------------------------------------------------
function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        const el = get(`b-${v}`);
        if (el) el.classList.toggle("active", v === opcion);
    });
}

// ----------------------------------------------------
// MODALIDAD
// ----------------------------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;

    const salir = get("m-salir");
    const casa = get("m-casa");

    if (salir && casa) {
        salir.classList.toggle("active", esSalir);
        casa.classList.toggle("active", !esSalir);
    }
}

// ----------------------------------------------------
// REGIONES DINÁMICAS (FIX CRÍTICO)
// ----------------------------------------------------
const regionesPorEstado = {
    FL: ["South Florida", "Central Florida", "North Florida"],
    TX: ["North Texas", "Central Texas", "South Texas"],
    CA: ["Northern California", "Central California", "Southern California"]
};

function actualizarRegiones() {
    const estado = get("inp-state")?.value || "FL";
    const regionSelect = get("inp-region");

    if (!regionSelect) return;

    regionSelect.innerHTML = "";

    (regionesPorEstado[estado] || []).forEach(r => {
        const opt = document.createElement("option");
        opt.value = r;
        opt.innerText = r;
        regionSelect.appendChild(opt);
    });
}

// ----------------------------------------------------
// INIT
// ----------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const state = get("inp-state");
    if (state) {
        state.onchange = actualizarRegiones;
        actualizarRegiones();
    }

    const btn = get("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ----------------------------------------------------
// MAIN CALL
// ----------------------------------------------------
async function solicitarEscape() {

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: get("inp-zip")?.value || "",
        estado: get("inp-state")?.value || "",
        region: get("inp-region")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!data || data.status !== "success") throw new Error("API error");

        setTimeout(() => {

            get("wrapper-loader").style.display = "none";
            get("wrapper-interactive").style.display = "block";

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            iniciarFlujo();

        }, 700);

    } catch (e) {
        console.error(e);
        get("wrapper-loader").style.display = "none";
        get("wrapper-form").style.display = "block";
        alert("Connection error");
    }
}

// ----------------------------------------------------
// FLUJO PRINCIPAL (CONTROLADO)
// ----------------------------------------------------
function iniciarFlujo() {

    limpiarTodo();

    const cont = get("step-content");

    if (tipoEscapeGlobal === "Casa") {
        hablar(UI[idiomaActual].house_intro);
        iniciarTimerCasa();
        mostrarRespiracion();
    } else {
        hablar(UI[idiomaActual].exit_intro);
        mostrarRespiracion();
    }

    siguientePaso();
}

// ----------------------------------------------------
// RESPIRACIÓN (1 SOLO CÍRCULO)
// ----------------------------------------------------
function mostrarRespiracion() {

    const circle = get("breathingCircle");
    if (!circle) return;

    clearInterval(intervaloRespiracion);

    let expand = false;

    hablar(UI[idiomaActual].breath_intro);

    intervaloRespiracion = setInterval(() => {
        expand = !expand;

        circle.style.transform = expand ? "scale(1.6)" : "scale(1)";
        circle.style.opacity = expand ? "0.9" : "0.6";

    }, 2500);
}

// ----------------------------------------------------
// TIMER CASA 10 MIN EXACTOS
// ----------------------------------------------------
function iniciarTimerCasa() {

    const timer = get("timer");
    if (!timer) return;

    tiempoRestante = 600;

    clearInterval(intervaloTimer);

    intervaloTimer = setInterval(() => {

        let min = Math.floor(tiempoRestante / 60);
        let sec = tiempoRestante % 60;

        timer.innerText = `${min}:${sec < 10 ? "0" : ""}${sec}`;

        tiempoRestante--;

        if (tiempoRestante <= 0) {
            clearInterval(intervaloTimer);
            finalizarSesion();
        }

    }, 1000);
}

// ----------------------------------------------------
// PASOS
// ----------------------------------------------------
function siguientePaso() {

    const cont = get("step-content");
    const btn = get("btn-next");

    if (indicePasoActual >= pasosMisionGlobal.length) {
        finalizarSesion();
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    cont.innerHTML = paso.story?.[idiomaActual] || "";

    btn.style.display = "block";

    btn.onclick = () => {
        indicePasoActual++;
        siguientePaso();
    };
}

// ----------------------------------------------------
// FINAL
// ----------------------------------------------------
function finalizarSesion() {

    limpiarTodo();

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="card-box">
            <h3>${idiomaActual === "es" ? "Sesión finalizada" : "Session completed"}</h3>
        </div>

        <div id="end-screen" class="end-buttons">
            <button class="btn-secondary" onclick="location.reload()">
                ${idiomaActual === "es" ? "Comenzar de nuevo" : "Restart"}
            </button>
        </div>
    `;

    hablar(idiomaActual === "es"
        ? "Sesión finalizada. Gracias."
        : "Session completed. Thank you."
    );
}

// ----------------------------------------------------
// CLEAN STATE
// ----------------------------------------------------
function limpiarTodo() {
    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);

    window.speechSynthesis.cancel();
}
