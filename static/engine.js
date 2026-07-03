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
    remaining: 0,
    locked: false
};

// ---------------- DOM SAFE ----------------
const $ = (id) => document.getElementById(id);

// ---------------- UI ----------------
function show(el) { if (el) el.style.display = "block"; }
function hide(el) { if (el) el.style.display = "none"; }

// ---------------- VOICE (CONTROL SIMPLE) ----------------
function speak(text) {
    if (!text || !("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();

    let v =
        state.lang === "es"
            ? voices.find(x => x.lang?.startsWith("es"))
            : voices.find(x => x.lang?.startsWith("en"));

    u.voice = v || voices[0];
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = 0.92;

    setTimeout(() => speechSynthesis.speak(u), 150);
}

// ---------------- INIT ----------------
window.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = start;
});

// ---------------- START ----------------
async function start() {

    const payload = {
        decision: state.mode === "casa" ? "casa" : "salir",
        lang: state.lang,
        budget_level: state.budget,
        zip_code: $("inp-zip").value || "",
        estado: $("inp-state").value || "",
        region: $("inp-region")?.value || "",
        desahogo: $("inp-text").value || ""
    };

    hide($("wrapper-form"));
    show($("wrapper-loader"));
    hide($("wrapper-interactive"));

    try {

        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!data || data.status !== "success") throw new Error("backend");

        state.steps = data.mision?.b || [];
        state.place = data.lugar || null;
        state.type = data.tipo || "Salida";

        state.stepIndex = 0;
        state.remaining = state.type === "Casa" ? 600 : 60;

        hide($("wrapper-loader"));
        show($("wrapper-interactive"));

        run();

    } catch (e) {
        console.error(e);
        alert("Error backend");
        show($("wrapper-form"));
    }
}

// ---------------- MAIN FLOW ----------------
function run() {

    clearAll();

    if (state.stepIndex >= state.steps.length || state.remaining <= 0) {
        finish();
        return;
    }

    const step = state.steps[state.stepIndex];

    $("btn-next").style.display = "none";
    $("btn-next").onclick = () => {
        state.stepIndex++;
        run();
    };

    // BREATH ONLY ONE SYSTEM
    if (step?.t === "breath_auto") {
        breath(step.d || 10);
        return;
    }

    // TIMER ONLY HOME
    if (state.type === "Casa") {
        timer();
    }

    const text = normalize(step.tx || step.story || step);

    $("step-content").innerHTML = `<div>${text}</div>`;
    speak(text);

    $("btn-next").style.display = "block";
}

// ---------------- BREATH (ONE ONLY CANVAS SYSTEM) ----------------
function breath(seconds) {

    const container = $("step-content");

    container.innerHTML = `
        <canvas id="breathe" width="200" height="200"></canvas>
        <div id="breathText">Inhala</div>
        <div id="breathTime"></div>
    `;

    const c = $("breathe");
    const ctx = c.getContext("2d");

    let t = seconds;
    let r = 50;
    let grow = true;

    state.breath = setInterval(() => {

        ctx.clearRect(0, 0, 200, 200);

        ctx.beginPath();
        ctx.arc(100, 100, r, 0, Math.PI * 2);

        ctx.fillStyle = "rgba(120,200,255,0.25)";
        ctx.strokeStyle = "rgba(180,220,255,0.9)";
        ctx.lineWidth = 2;

        ctx.fill();
        ctx.stroke();

        r += grow ? 1.2 : -1.2;

        if (r > 80) grow = false;
        if (r < 50) grow = true;

        $("breathText").innerText = grow ? "Inhala" : "Exhala";
        $("breathTime").innerText = t + "s";

        if (t % 4 === 0) speak(grow ? "inhala" : "exhala");

        t--;
        state.remaining--;

        if (t <= 0) {
            clearInterval(state.breath);
            state.stepIndex++;
            run();
        }

    }, 1000);
}

// ---------------- TIMER HOME ----------------
function timer() {

    if (state.timer) return;

    state.timer = setInterval(() => {

        const m = Math.floor(state.remaining / 60);
        const s = state.remaining % 60;

        $("timer").innerText = `${m}:${s.toString().padStart(2, "0")}`;

        state.remaining--;

        if (state.remaining <= 0) {
            clearInterval(state.timer);
            state.timer = null;
        }

    }, 1000);
}

// ---------------- FINISH ----------------
function finish() {

    clearAll();

    $("step-content").innerHTML = `
        <h2>Sesión completada</h2>
        <p>${state.type === "Casa"
            ? "Regulación interna completada"
            : "Micro-escape completado"}
        </p>
    `;

    const btn = $("btn-next");
    btn.style.display = "block";
    btn.innerText = "REINICIAR";
    btn.onclick = () => location.reload();
}

// ---------------- CLEAR SAFE ----------------
function clearAll() {
    clearInterval(state.breath);
    clearInterval(state.timer);
    state.breath = null;
    state.timer = null;
    window.speechSynthesis.cancel();
}

// ---------------- NORMALIZE ----------------
function normalize(t) {
    if (!t) return "";
    if (typeof t === "string") return t;
    return t[state.lang] || t.es || t.en || "";
}
