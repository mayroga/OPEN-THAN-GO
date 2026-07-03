/**
 * OPEN THAN GO | KERNEL V.2.0.0
 * Arquitectura: Sistema Integral de Misiones y Estabilización
 */

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,

    init() {
        document.getElementById('btn-mando').addEventListener('click', () => this.ejecutar());
        window.speechSynthesis.getVoices(); // Cargar voces al iniciar
    },

    hablar(texto) {
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(texto);
        msg.lang = 'es-ES';
        msg.rate = 1.0;
        msg.pitch = 0.9;
        const voces = window.speechSynthesis.getVoices();
        const nombresMasculinos = ['Google español', 'Jorge', 'Daniel', 'Carlos', 'Microsoft Pablo', 'Microsoft Raul', 'Alejandro'];
        const vozElegida = voces.find(v => nombresMasculinos.some(n => v.name.includes(n)) || v.name.toLowerCase().includes('male'));
        if (vozElegida) msg.voice = vozElegida;
        window.speechSynthesis.speak(msg);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        const payload = {
            zip: document.getElementById('inp-zip').value,
            mente: document.getElementById('inp-mente').value,
            modo: document.getElementById('modo-selector').value,
            budget: document.getElementById('inp-budget').value,
            perfil: document.getElementById('inp-perfil').value
        };
        const res = await (await fetch("/api/mando-integral", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })).json();
        this.procesarRespuesta(res);
    },

    procesarRespuesta(res) {
        document.getElementById('wrapper-form').classList.add('hidden');
        const container = document.getElementById('wrapper-interactive');
        container.classList.remove('hidden');
        if (res.modo === "CASA") {
            this.iniciarMisiones(res.misiones, container);
        } else {
            this.iniciarSalida(res, container);
        }
    },

    iniciarMisiones(misiones, container) {
        let index = 0;
        this.renderMision(misiones[index], container, () => {
            index++;
            if (index < misiones.length) {
                this.renderMision(misiones[index], container, () => {
                    this.iniciarTemporizador(container);
                });
            }
        });
    },

    renderMision(mision, container, onContinue) {
        this.hablar(mision.titulo + ". " + mision.descripcion);
        container.innerHTML = `
            <div class="mision-card">
                <h3>${mision.titulo}</h3>
                <p>${mision.descripcion}</p>
                <button id="btn-next">CONTINUAR</button>
            </div>
        `;
        document.getElementById('btn-next').onclick = onContinue;
    },

    iniciarSalida(res, container) {
        this.hablar(res.titulo + ". " + res.porque + ". " + res.que_hacer);
        container.innerHTML = `
            <div class="mision-card">
                <h2>${res.titulo}</h2>
                <p><strong>Por qué:</strong> ${res.porque}</p>
                <p><strong>Qué hacer:</strong> ${res.que_hacer}</p>
                <p><strong>Dónde:</strong> ${res.donde}</p>
                <button onclick="window.open('${res.gps}')">EJECUTAR RUTA</button>
            </div>
        `;
    },

    iniciarTemporizador(container) {
        container.innerHTML = `<div id="breath-circle"></div><div id="timer">10:00</div>`;
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            document.getElementById('timer').innerText = `${m}:${s.toString().padStart(2, '0')}`;
            if (this.timeLeft <= 0) { clearInterval(this.timer); location.reload(); }
        }, 1000);
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
