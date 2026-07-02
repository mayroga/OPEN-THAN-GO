// OPEN THAN GO SYSTEM - Frontend Engine v3 (STABLE + FIXED)
// Company: May Roga LLC

let idiomaActual = 'es';
let presupuestoActual = 'cero';
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let intervaloRespiracion = null;

// ------------------------------
// TRADUCCIONES
// ------------------------------
const traducciones = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        state: "Estado",
        region: "Región / Condado",
        zip: "ZIP Code",
        budget: "Presupuesto Disponible",
        mode: "¿Salir o quedarte en casa?",
        desahogo: "Desahogo Opcional",
        placeholder_text: "Escribe cómo te sientes...",
        btn_trigger: "GENERAR ESCAPE",
        loader: "Calculando...",
        btn_continue: "CONTINUAR",
        btn_gps: "ABRIR MAPA",
        inspira: "Inhala",
        expira: "Exhala"
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State",
        region: "Region",
        zip: "ZIP Code",
        budget: "Budget",
        mode: "Go out or stay home?",
        desahogo: "Optional emotional input",
        placeholder_text: "Write how you feel...",
        btn_trigger: "GENERATE ESCAPE",
        loader: "Calculating...",
        btn_continue: "CONTINUE",
        btn_gps: "OPEN MAP",
        inspira: "Inhale",
        expira: "Exhale"
    }
};

// ------------------------------
// SAFE GET
// ------------------------------
const get = (id) => document.getElementById(id);

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = get("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ------------------------------
// IDIOMA
// ------------------------------
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
        if (!el) return;
        el.innerText = traducciones[lang][map[id]];
    });

    const loader = get("txt-loader");
    if (loader) loader.innerText = traducciones[lang].loader;
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
// MODALIDAD
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;

    const s = get("m-salir");
    const c = get("m-casa");

    if (s && c) {
        s.classList.toggle("active", esSalir);
        c.classList.toggle("active", !esSalir);
    }
}

// ------------------------------
// MAIN CALL
// ------------------------------
async function solicitarEscape() {

    const zip = (get("inp-zip")?.value || "").trim();
    const estado = (get("inp-state")?.value || "FL").trim();
    const region = (get("inp-region")?.value || "").trim();

    // 🔥 FIX CRÍTICO: coherencia ubicación
    let ubicacionFinal = estado;

    if (zip.length === 5) {
        ubicacionFinal = zip;
    } else if (region && region !== estado) {
        ubicacionFinal = `${region}, ${estado}`;
    }

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        budget_level: presupuestoActual,
        zip_code: zip,
        estado,
        region,
        ubicacion_final: ubicacionFinal,
        desahogo: (get("inp-text")?.value || "").trim()
    };

    // UI
    toggleView("loading");

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok || data.status !== "success") {
            throw new Error(data.message || "Error backend");
        }

        pasosMisionGlobal = data.mision?.b || [];
        datosLugarGlobal = data.lugar || null;
        tipoEscapeGlobal = data.tipo || "";

        indicePasoActual = 0;

        setTimeout(() => {
            toggleView("app");
            procesarPaso();
        }, 600);

    } catch (e) {
        console.error(e);
        toggleView("form");
        alert("Error de conexión");
    }
}

// ------------------------------
// VIEW CONTROL (EVITA CONGELAMIENTOS)
// ------------------------------
function toggleView(state) {

    const form = get("wrapper-form");
    const load = get("wrapper-loader");
    const app = get("wrapper-interactive");

    if (!form || !load || !app) return;

    form.style.display = "none";
    load.style.display = "none";
    app.style.display = "none";

    if (state === "form") form.style.display = "block";
    if (state === "loading") load.style.display = "flex";
    if (state === "app") app.style.display = "block";
}

// ------------------------------
// MOTOR
// ------------------------------
function procesarPaso() {

    clearInterval(intervaloRespiracion);

    const cont = get("step-content");
    const btn = ensureNextButton();
    const map = ensureMapButton();

    if (!cont) return;

    if (indicePasoActual >= pasosMisionGlobal.length) {

        cont.innerHTML = "<h3>✔ Finalizado</h3>";

        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal?.gps_link) {
            map.href = datosLugarGlobal.gps_link;
            map.style.display = "block";
        } else {
            btn.innerText = "REINICIAR";
            btn.onclick = () => location.reload();
            btn.style.display = "block";
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btn.style.display = "block";
    btn.innerText = "CONTINUAR";

    btn.onclick = () => {
        indicePasoActual++;
        procesarPaso();
    };

    // STORY
    if (paso.story) {
        cont.innerHTML = `<div>${paso.story?.[idiomaActual] || ""}</div>`;
        return;
    }

    // TEXTO
    if (paso.t === "v" || paso.t === "h") {
        cont.innerHTML = `<h3>${paso.tx?.[idiomaActual] || ""}</h3>`;
        return;
    }

    // RESPIRACIÓN (FIX VISUAL)
    if (paso.t === "breath_auto") {

        let t = paso.d || 24;

        cont.innerHTML = `
            <div class="breath-circle"></div>
            <h2 id="breath-text">${traducciones[idiomaActual].inspira}</h2>
            <div>${t}s</div>
        `;

        const circle = cont.querySelector(".breath-circle");
        const text = cont.querySelector("#breath-text");

        intervaloRespiracion = setInterval(() => {

            t--;

            if (circle) {
                circle.style.transform = `scale(${1 + Math.sin(t) * 0.2})`;
            }

            if (text) {
                text.innerText = (t % 2 === 0)
                    ? traducciones[idiomaActual].inspira
                    : traducciones[idiomaActual].expira;
            }

            cont.querySelector("div:last-child").innerText = t + "s";

            if (t <= 0) {
                clearInterval(intervaloRespiracion);
                indicePasoActual++;
                procesarPaso();
            }

        }, 1000);

        return;
    }

    indicePasoActual++;
    procesarPaso();
}

// ------------------------------
// BOTONES
// ------------------------------
function ensureNextButton() {
    let b = get("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        get("wrapper-interactive")?.appendChild(b);
    }
    return b;
}

function ensureMapButton() {
    let b = get("btn-maps-action");
    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        b.className = "btn-maps-route";
        b.target = "_blank";
        get("wrapper-interactive")?.appendChild(b);
    }
    return b;
}
