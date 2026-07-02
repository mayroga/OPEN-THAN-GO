// OPEN THAN GO SYSTEM - Frontend Engine v6.5 (FUSED STABLE CORE)
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
// VOZ (FUSIONADO - SIN ESPANGLISH)
// ----------------------------------------------------
function hablar(texto) {
    if (!("speechSynthesis" in window)) return;
    if (!texto) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(texto);
    const voices = speechSynthesis.getVoices();

    let voice = null;

    if (idiomaActual === "es") {
        voice =
            voices.find(v => v.lang.startsWith("es") && v.name.toLowerCase().includes("male")) ||
            voices.find(v => v.lang.startsWith("es"));
    }

    if (idiomaActual === "en") {
        voice =
            voices.find(v => v.lang.startsWith("en") && v.name.toLowerCase().includes("male")) ||
            voices.find(v => v.lang.startsWith("en"));
    }

    if (voice) u.voice = voice;

    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;
    u.pitch = 1;

    window.speechSynthesis.speak(u);
}

// ----------------------------------------------------
// UI TEXTS (SIN ESPANGLISH)
// ----------------------------------------------------
const UI = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        breath_intro: "Vamos a hacer una respiración guiada para ayudarte a calmar tu mente.",
        house_intro: "Has elegido quedarte en casa. Sesión de 10 minutos guiada.",
        exit_intro: "Te guiaremos a un lugar recomendado según tu estado emocional.",
        inhale: "Inhala",
        exhale: "Exhala"
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        breath_intro: "We will guide you through breathing to calm your mind.",
        house_intro: "You chose to stay home. 10-minute guided session.",
        exit_intro: "We will guide you to a recommended place.",
        inhale: "Inhale",
        exhale: "Exhale"
    }
};

// ----------------------------------------------------
// IDIOMA
// ----------------------------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    get("lang-es")?.classList.toggle("active", lang === "es");
    get("lang-en")?.classList.toggle("active", lang === "en");

    const loader = get("txt-loader");
    if (loader) loader.innerText =
        lang === "es"
            ? "Procesando..."
            : "Processing...";
}

// ----------------------------------------------------
// REGIONES (FIX CRÍTICO MANTENIDO)
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

        if (!data || data.status !== "success") throw new Error();

        setTimeout(() => {

            get("wrapper-loader").style.display = "none";
            get("wrapper-interactive").style.display = "block";

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            iniciarFlujo();

        }, 500);

    } catch (e) {
        get("wrapper-form").style.display = "block";
        alert("Connection error");
    }
}

// ----------------------------------------------------
// FLUJO
// ----------------------------------------------------
function iniciarFlujo() {

    limpiar();

    if (tipoEscapeGlobal === "Casa") {
        hablar(UI[idiomaActual].house_intro);
        iniciarTimerCasa();
    } else {
        hablar(UI[idiomaActual].exit_intro);
    }

    iniciarRespiracion();
    siguientePaso();
}

// ----------------------------------------------------
// RESPIRACIÓN (MEJORADA - 1 SOLO CÍRCULO)
// ----------------------------------------------------
function iniciarRespiracion() {

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
// TIMER CASA (10 MIN EXACTOS)
// ----------------------------------------------------
function iniciarTimerCasa() {

    const timer = get("timer");
    if (!timer) return;

    tiempoRestante = 600;

    clearInterval(intervaloTimer);

    intervaloTimer = setInterval(() => {

        let m = Math.floor(tiempoRestante / 60);
        let s = tiempoRestante % 60;

        timer.innerText = `${m}:${s.toString().padStart(2, "0")}`;

        tiempoRestante--;

        if (tiempoRestante <= 0) {
            clearInterval(intervaloTimer);
            finalizar();
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
        finalizar();
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
function finalizar() {

    limpiar();

    const cont = get("step-content");

    cont.innerHTML = `
        <h2>${idiomaActual === "es" ? "Sesión finalizada" : "Session completed"}</h2>
        <button onclick="location.reload()">
            ${idiomaActual === "es" ? "Reiniciar" : "Restart"}
        </button>
    `;

    hablar(idiomaActual === "es"
        ? "Sesión finalizada"
        : "Session completed"
    );
}

// ----------------------------------------------------
// CLEAN
// ----------------------------------------------------
function limpiar() {
    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);
    window.speechSynthesis.cancel();
}
