/* ======================================================
   OPEN THAN GO PRO ENGINE v2 - STABLE FIXED VERSION
   (Performance + Sync + Voice Control + Mission Flow)
   May Roga LLC
====================================================== */

class OpenThanGoEngine {
    constructor() {

        this.state = {
            lang: "es",
            mode: null,
            pocket: "cero",

            started: false,

            timeLeft: 600,
            timer: null,
            breathingTimer: null,

            missions: null,
            activeMission: null,
            missionIndex: 0,

            voiceBusy: false
        };

        this.textBox = document.getElementById("step-content");

        this.init();
    }

    /* =========================
       INIT
    ========================= */
    init() {
        this.loadMissions();
    }

    /* =========================
       LOAD MISSIONS
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
       LANGUAGE SAFE TEXT
    ========================= */
    t(es, en) {
        return this.state.lang === "es" ? es : en;
    }

    /* =========================
       RENDER SAFE
    ========================= */
    renderText(html) {
        if (!this.textBox) return;
        this.textBox.innerHTML = html;
    }

    /* =========================
       SPEECH CONTROL (NO STACK)
    ========================= */
    speak(text) {
        if (!window.speechSynthesis) return;

        if (this.state.voiceBusy) return;

        this.state.voiceBusy = true;

        speechSynthesis.cancel();

        const u = new SpeechSynthesisUtterance(text);
        u.lang = this.state.lang === "es" ? "es-ES" : "en-US";
        u.rate = 0.95;
        u.pitch = 0.9;

        u.onend = () => {
            this.state.voiceBusy = false;
        };

        speechSynthesis.speak(u);
    }

    /* =========================
       START FLOW
    ========================= */
    startFlow(mode) {
        this.state.mode = mode;

        if (mode === "home") {
            this.startHomeMode();
        } else {
            this.startOutMode();
        }
    }

    /* =========================
       HOME MODE (10 MIN RESET)
    ========================= */
    startHomeMode() {

        this.state.timeLeft = 600;

        this.renderText(
            this.t(
                "Modo casa activado. Iniciando sesión guiada de 10 minutos.",
                "Home mode activated. Starting 10-minute guided session."
            )
        );

        this.startTimer();
        this.startBreathing();
    }

    /* =========================
       OUT MODE (MISSIONS)
    ========================= */
    startOutMode() {

        const data = this.state.missions;

        if (!data || !data.missions) {
            this.renderText("Loading missions...");
            return;
        }

        const pool = data.missions;

        this.state.activeMission =
            pool[Math.floor(Math.random() * pool.length)];

        this.state.missionIndex = 0;

        this.renderMissionStep(0);
    }

    /* =========================
       MISSION STEP ENGINE
    ========================= */
    renderMissionStep(index) {

        const m = this.state.activeMission;
        if (!m || !m.b[index]) {
            this.finishMission();
            return;
        }

        this.state.missionIndex = index;
        const step = m.b[index];

        if (step.v || step.t === "v") {
            this.renderText(step.tx?.[this.state.lang]);
            this.speak(step.tx?.[this.state.lang]);
        }

        if (step.h) {
            this.renderText(step.tx?.[this.state.lang]);
        }

        if (step.story) {
            this.renderText(step.story[this.state.lang]);
        }

        if (step.t === "breath_auto") {
            this.runBreathing(step.d || 24);
        }

        if (step.t === "d") {
            this.renderDecision(step);
            return;
        }

        if (step.t === "sil") {
            this.renderText(step.tx?.[this.state.lang]);

            setTimeout(() => {
                this.renderMissionStep(index + 1);
            }, (step.d || 10) * 1000);

            return;
        }

        if (step.t === "r") {
            this.renderText("+" + step.tx);
        }

        if (step.t === "c") {
            this.speak(step.tx?.[this.state.lang]);
        }

        setTimeout(() => {
            this.renderMissionStep(index + 1);
        }, 1500);
    }

    /* =========================
       DECISION SYSTEM
    ========================= */
    renderDecision(step) {

        let html = `<p>${step.q[this.state.lang]}</p>`;

        step.op.forEach((op, i) => {
            html += `
                <button onclick="OPEN_THAN_GO.chooseOption(${i})"
                style="width:100%;padding:10px;margin:5px;">
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
        }, 1500);
    }

    /* =========================
       BREATHING (STABLE)
    ========================= */
    startBreathing() {

        clearInterval(this.state.breathingTimer);

        let inhale = true;

        this.state.breathingTimer = setInterval(() => {

            if (inhale) {
                this.speak(this.t("Inhala", "Inhale"));
            } else {
                this.speak(this.t("Exhala", "Exhale"));
            }

            inhale = !inhale;

        }, 24000);
    }

    runBreathing(seconds) {

        clearInterval(this.state.breathingTimer);

        let cycles = Math.floor(seconds / 24);
        let count = 0;
        let inhale = true;

        this.state.breathingTimer = setInterval(() => {

            if (count >= cycles) {
                clearInterval(this.state.breathingTimer);
                this.renderMissionStep(this.state.missionIndex + 1);
                return;
            }

            if (inhale) {
                this.speak(this.t("Inhala", "Inhale"));
            } else {
                this.speak(this.t("Exhala", "Exhale"));
                count++;
            }

            inhale = !inhale;

        }, 24000);
    }

    /* =========================
       TIMER HOME MODE
    ========================= */
    startTimer() {

        clearInterval(this.state.timer);

        this.state.timer = setInterval(() => {

            this.state.timeLeft--;

            if (this.state.timeLeft <= 0) {
                this.endSession();
            }

        }, 1000);
    }

    /* =========================
       END SESSION
    ========================= */
    endSession() {

        clearInterval(this.state.timer);
        clearInterval(this.state.breathingTimer);

        speechSynthesis.cancel();

        this.renderText(
            this.t(
                "Por hoy terminamos. Puedes reiniciar cuando quieras.",
                "We are done for today. You can restart anytime."
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
                "Mission completed. Your internal state has shifted."
            )
        );
    }
}

/* ========================= */
window.addEventListener("DOMContentLoaded", () => {
    window.OPEN_THAN_GO = new OpenThanGoEngine();
});
