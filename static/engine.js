// OPEN THAN GO SYSTEM - ENGINE v6 STABLE CORE
// May Roga LLC

let state = {
    lang: "es",
    budget: "cero",
    mode: "out",
    stepIndex: 0,
    steps: [],
    place: null,
    type: "",
    timer: null,
    breath: null,
    remaining: 0
};

// ---------------- DOM HELPERS ----------------
const $ = (id) => document.getElementById(id);
const hide = (el) => { if (el) el.style.display = "none"; };
const show = (el) => { if (el) el.style.display = "block"; };

// ---------------- VOICE ENGINE ----------------
function speak(text) {
    if (!text || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();
    u.voice = voices.find(v => v.lang.startsWith(state.lang)) || voices[0];
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;

    setTimeout(() => speechSynthesis.speak(u), 100);
}

// ---------------- CORE FLOW ----------------
window.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = start;
});

async function start() {
    const payload = {
        decision: state.mode,
        lang: state.lang,
        budget_level: state.budget,
        zip_code: $("inp-zip")?.value || "",
        estado: $("inp-state")?.value || "",
        desahogo: $("inp-text")?.value || ""
    };

    hide($("wrapper-form"));
    show($("wrapper-loader"));

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.status !== "success") throw new Error("API Error");

        state.steps = data.mision?.b || [];
        state.place = data.lugar || null;
        state.type = data.tipo || "Salida";
        state.remaining = data.duration || 60;
        state.stepIndex = 0;

        hide($("wrapper-loader"));
        show($("wrapper-interactive"));
        run();

    } catch (e) {
        alert("Error de conexión. Intente de nuevo.");
        show($("wrapper-form"));
        hide($("wrapper-loader"));
    }
}

function run() {
    clearAll();
    if (state.stepIndex >= state.steps.length) return finish();

    const step = state.steps[state.stepIndex];
    const content = $("step-content");
    
    // Si es respiración
    if (step.t === "breath_auto") {
        breath(step.d);
    } else {
        content.innerHTML = `<div>${step.tx}</div>`;
        speak(step.tx);
        show($("btn-next"));
    }

    if (state.type === "Casa") timer();
}

// ---------------- TOOLS ----------------
function breath(seconds) {
    let t = seconds;
    let grow = true;
    let r = 50;
    const container = $("step-content");
    
    container.innerHTML = `<canvas id="breathe" width="200" height="200"></canvas><div id="bt">Inhala</div>`;
    const ctx = $("breathe").getContext("2d");

    state.breath = setInterval(() => {
        ctx.clearRect(0, 0, 200, 200);
        ctx.beginPath();
        ctx.arc(100, 100, r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(100, 200, 255, 0.3)";
        ctx.fill();
        
        r += grow ? 1 : -1;
        if (r > 90 || r < 40) grow = !grow;
        $("bt").innerText = grow ? "Inhala" : "Exhala";
        
        if (--t <= 0) {
            clearInterval(state.breath);
            state.stepIndex++;
            run();
        }
    }, 1000);
}

function timer() {
    state.timer = setInterval(() => {
        if (--state.remaining <= 0) clearInterval(state.timer);
        $("timer").innerText = Math.floor(state.remaining / 60) + ":" + (state.remaining % 60).toString().padStart(2, '0');
    }, 1000);
}

function clearAll() {
    clearInterval(state.breath);
    clearInterval(state.timer);
    hide($("btn-next"));
    window.speechSynthesis.cancel();
}

function finish() {
    $("step-content").innerHTML = `<h2>Sesión completada</h2>`;
    const btn = $("btn-next");
    show(btn);
    btn.innerText = "REINICIAR";
    btn.onclick = () => location.reload();
}
