// OPEN THAN GO SYSTEM - Frontend Engine (FIXED VERSION)
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
        desahogo: "Desahogo Opcional (Filtro Emocional)",
        placeholder_text: "Escribe libremente cómo te sientes hoy...",
        btn_trigger: "GENERAR ESCAPE",
        loader: "Calculando tu vector de escape ideal...",
        btn_continue: "CONTINUAR",
        btn_gps: "ABRIR MAPA EN GPS",
        tipo_casa: "Protocolo Doméstico Activado",
        tipo_salida: "Protocolo de Exploración Abierto",
        txt_correcto: "<strong>¡Excelente elección!</strong><br>",
        txt_incorrecto: "<strong>Analiza esto con calma:</strong><br>",
        inspira: "Inhala",
        expira: "Exhala"
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State",
        region: "Region / County",
        zip: "ZIP Code",
        budget: "Available Budget",
        mode: "Go out or stay at home?",
        desahogo: "Optional Emotional Venting",
        placeholder_text: "Write freely about how you feel today...",
        btn_trigger: "GENERATE ESCAPE",
        loader: "Calculating your escape vector...",
        btn_continue: "CONTINUE",
        btn_gps: "OPEN MAP",
        tipo_casa: "Domestic Protocol Activated",
        tipo_salida: "Exploration Protocol Opened",
        txt_correcto: "<strong>Excellent choice!</strong><br>",
        txt_incorrecto: "<strong>Think about this:</strong><br>",
        inspira: "Inhale",
        expira: "Exhale"
    }
};

// ------------------------------
// SAFE GET (EVITA CRASHES)
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// INICIO SEGURO
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {

    const btn = get("btn-start");

    if (btn) {
        btn.addEventListener("click", solicitarEscape);
    } else {
        console.error("Botón btn-start no encontrado");
    }

});

// ------------------------------
// IDIOMA
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    const esBtn = get('lang-es');
    const enBtn = get('lang-en');

    if (esBtn && enBtn) {
        esBtn.classList.toggle('active', lang === 'es');
        enBtn.classList.toggle('active', lang === 'en');
    }

    const map = {
        'txt-subtitle': 'subtitle',
        'lbl-state': 'state',
        'lbl-region': 'region',
        'lbl-zip': 'zip',
        'lbl-budget': 'budget',
        'lbl-mode': 'mode',
        'lbl-desahogo': 'desahogo',
        'inp-text': 'placeholder_text'
    };

    Object.keys(map).forEach(id => {
        const el = get(id);
        if (!el) return;

        if (id === 'inp-text') {
            el.placeholder = traducciones[lang][map[id]];
        } else {
            el.innerText = traducciones[lang][map[id]];
        }
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

    const salir = get("m-salir");
    const casa = get("m-casa");

    if (salir && casa) {
        salir.classList.toggle("active", esSalir);
        casa.classList.toggle("active", !esSalir);
    }
}

// ------------------------------
// MAIN CALL
// ------------------------------
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

    // UI states
    if (get("wrapper-form")) get("wrapper-form").style.display = "none";
    if (get("wrapper-loader")) get("wrapper-loader").style.display = "flex";
    if (get("wrapper-interactive")) get("wrapper-interactive").style.display = "none";

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

        setTimeout(() => {

            if (get("wrapper-loader")) get("wrapper-loader").style.display = "none";
            if (get("wrapper-interactive")) get("wrapper-interactive").style.display = "block";

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            procesarPasoMision();

        }, 800);

    } catch (e) {
        console.error(e);

        if (get("wrapper-loader")) get("wrapper-loader").style.display = "none";
        if (get("wrapper-form")) get("wrapper-form").style.display = "block";

        alert("Error conectando con el sistema");
    }
}

// ------------------------------
// MOTOR DE PASOS
// ------------------------------
function procesarPasoMision() {

    clearInterval(intervaloRespiracion);
    window.speechSynthesis.cancel();

    const cont = get("step-content");

    const btnNext = ensureButtonNext();
    const btnMap = ensureMapButton();

    if (indicePasoActual >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
            btnMap.href = datosLugarGlobal.gps_link;
            btnMap.style.display = "block";
        } else {
            btnNext.innerText = "FINALIZAR";
            btnNext.style.display = "block";
            btnNext.onclick = () => location.reload();
        }

        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btnNext.onclick = () => {
        indicePasoActual++;
        procesarPasoMision();
    };

    if (!cont) return;

    // TEXTO SIMPLE
    if (paso.t === "v" || paso.t === "h") {
        cont.innerHTML = `<h3>${paso.tx?.[idiomaActual] || ""}</h3>`;
        btnNext.style.display = "block";
        return;
    }

    // HISTORIA
    if (paso.story) {
        cont.innerHTML = `<div>${paso.story?.[idiomaActual] || ""}</div>`;
        btnNext.style.display = "block";
        return;
    }

    // RESPIRACIÓN
    if (paso.t === "breath_auto") {

        let s = paso.d || 10;

        cont.innerHTML = `<h2>${traducciones[idiomaActual].inspira}</h2><div>${s}</div>`;

        intervaloRespiracion = setInterval(() => {
            s--;

            cont.innerHTML = `<h2>${
                s % 2 === 0
                    ? traducciones[idiomaActual].inspira
                    : traducciones[idiomaActual].expira
            }</h2><div>${s}</div>`;

            if (s <= 0) {
                clearInterval(intervaloRespiracion);
                indicePasoActual++;
                procesarPasoMision();
            }
        }, 1000);

        return;
    }

    // DEFAULT
    indicePasoActual++;
    procesarPasoMision();
}

// ------------------------------
// BOTONES PROTEGIDOS
// ------------------------------
function ensureButtonNext() {
    let b = get("btn-next");

    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        b.style.display = "none";
        b.innerText = "CONTINUAR";
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
        b.innerText = "MAPA";
        get("wrapper-interactive")?.appendChild(b);
    }

    return b;
}
