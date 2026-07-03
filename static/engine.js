// OPEN THAN GO BY MAY ROGA LLC - CORE ENGINE DEFINITIVO
// Protocolo: Intervención Biopsicosocial Encubierta

const state = {
    lang: "es",
    mission: null,      // Objeto misión recibido del servidor
    currentStep: 0,     // Índice del paso actual
    timerInterval: null
};

// Helpers de UI
const $ = (id) => document.getElementById(id);
const show = (id) => $(id).style.display = "block";
const hide = (id) => $(id).style.display = "none";

async function startSession() {
    const payload = {
        desahogo: $("inp-text").value,
        budget: $("inp-budget").value,
        state: $("inp-state").value
    };

    hide("wrapper-form");
    show("wrapper-loader");

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        state.mission = data.mision;
        state.currentStep = 0;
        
        hide("wrapper-loader");
        show("wrapper-interactive");
        renderStep();
    } catch (e) {
        alert("El sistema requiere conexión para sincronizar la guía.");
        show("wrapper-form");
    }
}

function renderStep() {
    const steps = state.mission.b;
    const step = steps[state.currentStep];
    const content = $("step-content");
    
    // Limpiar UI anterior
    hide("btn-next");
    hide("btn-maps-action");
    content.innerHTML = "";

    // Lógica de Renderizado según tipo
    if (step.tx) {
        content.innerHTML = `<p>${step.tx}</p>`;
        speak(step.tx);
    }

    // Si es Dilema (d)
    if (step.t === "d") {
        step.op.forEach((op, idx) => {
            const b = document.createElement("button");
            b.className = "btn btn-secondary";
            b.innerText = op;
            b.onclick = () => {
                content.innerHTML += `<div class="card-box" style="margin-top:10px">${step.ex[idx]}</div>`;
                show("btn-next");
            };
            content.appendChild(b);
        });
    } else {
        show("btn-next");
    }

    // Si hay mapa o acción final
    if (step.mapa) {
        const btnMap = $("btn-maps-action");
        btnMap.href = step.mapa;
        show("btn-maps-action");
    }
}

// Control de flujo
$("btn-next").onclick = () => {
    state.currentStep++;
    if (state.currentStep < state.mission.b.length) {
        renderStep();
    } else {
        finishSession();
    }
};

// Función de exportación definitiva
function finishSession() {
    const content = $("step-content");
    content.innerHTML = `
        <h3>Sesión Completada</h3>
        <p>Tu plan de acción está listo. Mantén este equilibrio.</p>
        <button class="btn btn-primary" onclick="window.print()">GUARDAR / IMPRIMIR PDF</button>
    `;
    hide("btn-next");
}

// Speaker Engine
function speak(text) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    window.speechSynthesis.speak(u);
}

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = startSession;
});
