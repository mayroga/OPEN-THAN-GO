/* ======================================================
   OPEN THAN GO PRO ENGINE v3
   FULL ORCHESTRATION SYSTEM (ONBOARDING + MISSIONS + HOME RESET)
   May Roga LLC
====================================================== */

class OpenThanGoEngine {
    constructor() {

        this.state = {
            lang: "es",
            mode: null, // home | out
            pocket: "cero",

            started: false,
            onboarding: true,
            step: 0,

            timeLeft: 600,
            timer: null,
            breathing: null,

            missions: null,
            activeMission: null,
            missionIndex: 0,

            userProfile: {
                feeling: "",
                goal: "",
                need: ""
            }
        };

        this.circle = document.getElementById("breathingCircle"); // opcional
        this.textBox = document.getElementById("step-content");

        this.init();
    }

    /* =========================
       INIT
    ========================= */
    init() {
        this.loadMissions();
        this.startOnboarding();
    }

    /* =========================
       MISSIONS LOAD
    ========================= */
    async loadMissions() {
        try {
            const res = await fetch("/static/missions_15_21.json");
            this.state.missions = await res.json();
        } catch (e) {
            console.error("Mission load error:", e);
        }
    }

    /* =========================
       LANGUAGE
    ========================= */
    setLang(lang) {
        this.state.lang = lang;

        const esBtn = document.getElementById("lang-es");
        const enBtn = document.getElementById("lang-en");

        if (esBtn && enBtn) {
            esBtn.classList.toggle("active", lang === "es");
            enBtn.classList.toggle("active", lang === "en");
        }
    }

    t(es, en) {
        return this.state.lang === "es" ? es : en;
    }

    /* =========================
       ONBOARDING (CLAVE NUEVA)
    ========================= */
    startOnboarding() {
        this.state.onboarding = true;
        this.state.step = 1;
        this.askFeeling();
    }

    askFeeling() {
        this.renderText(
            this.t(
                "¿Cómo te sientes realmente hoy?",
                "How do you really feel today?"
            )
        );
    }

    askGoal() {
        this.renderText(
            this.t(
                "¿Qué quieres lograr hoy?",
                "What do you want to achieve today?"
            )
        );
    }

    askNeed() {
        this.renderText(
            this.t(
                "¿Qué necesitas ahora mismo?",
                "What do you need right now?"
            )
        );
    }

    saveAnswer(value) {
        if (this.state.step === 1) this.state.userProfile.feeling = value;
        if (this.state.step === 2) this.state.userProfile.goal = value;
        if (this.state.step === 3) this.state.userProfile.need = value;

        this.state.step++;

        if (this.state.step === 2) this.askGoal();
        else if (this.state.step === 3) this.askNeed();
        else this.askMode();
    }

    /* =========================
       MODE SELECTION
    ========================= */
    askMode() {
        this.state.onboarding = false;

        this.renderText(
            this.t(
                "¿Qué deseas ahora? SALIR o QUEDARTE EN CASA",
                "What do you want now? GO OUT or STAY HOME"
            )
        );
    }

    setMode(mode) {
        this.state.mode = mode;

        if (mode === "home") this.startHomeMode();
        if (mode === "out") this.startOutMode();
    }

    /* =========================
       HOME MODE (10 MIN RESET)
    ========================= */
    startHomeMode() {

        this.state.timeLeft = 600;

        this.renderText(
            this.t(
                "Modo CASA activado. Iniciamos un reinicio guiado de 10 minutos.",
                "HOME mode activated. Starting 10-minute guided reset."
            )
        );

        this.startBreathing();
        this.startTimer();
        this.startSilentPhase();
    }

    startSilentPhase() {
        this.renderText(
            this.t(
                "Primeros 5 minutos: solo respira. No tienes que hacer nada más.",
                "First 5 minutes: just breathe. You don’t need to do anything else."
            )
        );
    }

    /* =========================
       OUT MODE → MISSIONS
    ========================= */
    startOutMode() {

        const data = this.state.missions;

        if (!data) {
            this.renderText("Loading missions...");
            return;
        }

        const pool = data.missions;
        this.state.activeMission = pool[Math.floor(Math.random() * pool.length)];
        this.state.missionIndex = 0;

        this.renderMissionIntro();
    }

    /* =========================
       MISSION ENGINE
    ========================= */
    renderMissionIntro() {
        const m = this.state.activeMission;

        const txt = m.b[0].tx[this.state.lang];
        this.renderText(txt);
        this.speak(txt);

        setTimeout(() => {
            this.renderMissionStep(1);
        }, 1800);
    }

    renderMissionStep(index) {

        const m = this.state.activeMission;
        const step = m.b[index];

        if (!step) return this.finishMission();

        this.state.missionIndex = index;

        if (step.t === "v" || step.t === "h" || step.story) {
            this.renderText(step.tx?.[this.state.lang] || step.story?.[this.state.lang]);
        }

        if (step.t === "breath_auto") {
            this.runBreathing(step.d);
        }

        if (step.t === "d") {
            this.renderDecision(step);
        }

        if (step.t === "sil") {
            this.renderText(step.tx[this.state.lang]);

            setTimeout(() => {
                this.renderMissionStep(index + 1);
            }, step.d * 1000);
        }

        if (step.t === "r") {
            this.renderText("+" + step.tx);
        }

        if (step.t === "c") {
            this.speak(step.tx[this.state.lang]);
        }
    }

    /* =========================
       DECISION ENGINE
    ========================= */
    renderDecision(step) {

        let html = `<p>${step.q[this.state.lang]}</p>`;

        step.op.forEach((op, i) => {
            html += `
                <button onclick="OPEN_THAN_GO.chooseOption(${i})"
                    style="width:100%;margin:5px;padding:12px;border-radius:8px;">
                    ${op[this.state.lang]}
                </button>
            `;
        });

        this.renderText(html);
    }

    chooseOption(i) {

        const step = this.state.activeMission.b[this.state.missionIndex];

        const feedback = step.ex[i];

        this.renderText(feedback[this.state.lang]);

        setTimeout(() => {
            this.renderMissionStep(this.state.missionIndex + 1);
        }, 1800);
    }

    /* =========================
       BREATHING SYSTEM
    ========================= */
    startBreathing() {

        let inhale = true;

        this.state.breathing = setInterval(() => {

            if (!this.circle) return;

            this.circle.style.transition = "all 24s ease";

            if (inhale) {
                this.circle.style.transform = "scale(1.4)";
                this.speak(this.t("Inhala", "Inhale"));
            } else {
                this.circle.style.transform = "scale(0.8)";
                this.speak(this.t("Exhala", "Exhale"));
            }

            inhale = !inhale;

        }, 24000);
    }

    runBreathing(seconds) {

        let cycles = Math.floor(seconds / 24);
        let count = 0;
        let inhale = true;

        const interval = setInterval(() => {

            if (count >= cycles) {
                clearInterval(interval);
                this.renderMissionStep(this.state.missionIndex + 1);
                return;
            }

            if (this.circle) {
                this.circle.style.transform = inhale ? "scale(1.4)" : "scale(0.8)";
            }

            inhale = !inhale;
            count++;

        }, 24000);
    }

    /* =========================
       TIMER HOME MODE
    ========================= */
    startTimer() {

        clearInterval(this.state.timer);

        this.state.timer = setInterval(() => {

            this.state.timeLeft--;

            if (this.state.timeLeft === 300) {
                this.renderText(
                    this.t(
                        "Te quedan 5 minutos. Respira. Estás haciendo algo bueno por ti.",
                        "5 minutes left. Keep breathing. You are doing something good for yourself."
                    )
                );
            }

            if (this.state.timeLeft <= 0) {
                this.endSession();
            }

        }, 1000);
    }

    /* =========================
       END HOME SESSION (IMPORTANTE)
    ========================= */
    endSession() {

        clearInterval(this.state.timer);
        clearInterval(this.state.breathing);

        if (this.circle) this.circle.style.transform = "scale(1)";

        this.renderText(
            this.t(
                "Por hoy terminamos. Tu sistema ha sido estabilizado. Puedes volver cuando quieras.",
                "We are done for today. Your system has stabilized. You can return anytime."
            )
        );

        this.state.started = false;
    }

    /* =========================
       FINISH MISSION
    ========================= */
    finishMission() {

        this.renderText(
            this.t(
                "Misión completada. Has cambiado tu estado interno.",
                "Mission completed. You have changed your internal state."
            )
        );
    }

    /* =========================
       UI
    ========================= */
    renderText(text) {
        if (this.textBox) this.textBox.innerHTML = text;
    }

    speak(text) {

        if (!window.speechSynthesis) return;

        const u = new SpeechSynthesisUtterance(text);

        u.lang = this.state.lang === "es" ? "es-ES" : "en-US";
        u.rate = 0.95;
        u.pitch = 0.85; // más masculino

        speechSynthesis.cancel();
        speechSynthesis.speak(u);
    }
}

/* =========================
   GLOBAL
========================= */
window.addEventListener("DOMContentLoaded", () => {
    window.OPEN_THAN_GO = new OpenThanGoEngine();
});
