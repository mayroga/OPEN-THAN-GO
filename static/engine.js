// OPEN THAN GO - ENGINE v5.0 (FASTAPI READY)
// Motor de mando de MAY ROGA

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

function get(id) { return document.getElementById(id); }

function hablar(texto) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(texto);
    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
}

function t(p) { return p[idiomaActual] || p.es || p.en || p; }

function cambiarIdioma(lang) {
    idiomaActual = lang;
    get("lang-es").classList.toggle("active", lang === "es");
    get("lang-en").classList.toggle("active", lang === "en");
}

function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;
    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        get(`b-${v}`).classList.toggle("active", v === opcion);
    });
}

function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;
    get("m-salir").classList.toggle("active", esSalir);
    get("m-casa").classList.toggle("active", !esSalir);
    get("wrapper-form").style.borderColor = esSalir ? "#f12711" : "#2a5298";
}

async function solicitarEscape() {
    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: get("inp-zip")?.value || "33101",
        estado: get("inp-state")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";

    try {
        const response = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        get("wrapper-loader").style.display = "none";
        get("wrapper-interactive").style.display = "block";
        
        if (data.tipo === "Casa") {
            ejecutarProtocoloCasa(data.mision);
        } else {
            ejecutarProtocoloSalida(data.opciones);
        }
    } catch (e) {
        console.error("Error en mando:", e);
        get("wrapper-form").style.display = "block";
        get("wrapper-loader").style.display = "none";
    }
}

function ejecutarProtocoloCasa(mision) {
    const cont = get("step-content");
    cont.innerHTML = `
        <div class="breath-circle"></div>
        <div class="mision-card">
            <h2>${t(mision.titulo)}</h2>
            <p>${t(mision.descripcion)}</p>
        </div>
        <div id="timer">10:00</div>
    `;
    
    hablar(t(mision.descripcion));
    
    let t_restante = 600;
    const timerDisplay = get("timer");
    const interval = setInterval(() => {
        t_restante--;
        let m = Math.floor(t_restante / 60);
        let s = t_restante % 60;
        timerDisplay.innerText = `${m}:${s.toString().padStart(2, '0')}`;
        if (t_restante <= 0) {
            clearInterval(interval);
            window.location.reload();
        }
    }, 1000);
}

function ejecutarProtocoloSalida(opciones) {
    const cont = get("step-content");
    cont.innerHTML = `<h2 class="salida-title">TU MANDO EXTERIOR</h2>`;
    
    opciones.forEach(opt => {
        let btn = document.createElement("button");
        btn.className = "btn-vibrante";
        btn.innerText = opt.nombre;
        btn.onclick = () => window.open(opt.gps, "_blank");
        cont.appendChild(btn);
    });
    
    hablar("El mundo está listo. Selecciona tu ruta.");
}

document.addEventListener("DOMContentLoaded", () => {
    get("btn-start").onclick = solicitarEscape;
});
