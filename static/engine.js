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
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        
        const payload = {
            zip: document.getElementById('inp-zip').value,
            mente: document.getElementById('inp-mente').value,
            modo: document.getElementById('modo-selector').value
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
        
        const content = document.getElementById('step-content');
        
        if (res.modo === "CASA") {
            this.iniciarMisiones(res.misiones, content);
        } else {
            this.iniciarSalida(res, content);
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
        container.innerHTML = `
            <div class="mision-card">
                <h3>${mision.titulo}</h3>
                <p>${mision.descripcion}</p>
                <button id="btn-next">CONTINUAR</button>
            </div>
        `;
        document.getElementById('btn-next').onclick = onContinue;
    },

    iniciarTemporizador(container) {
        container.innerHTML = `<div id="breath-circle"></div><div id="timer">10:00</div>`;
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            document.getElementById('timer').innerText = `${m}:${s.toString().padStart(2, '0')}`;
            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                location.reload();
            }
        }, 1000);
    },

    iniciarSalida(res, container) {
        container.innerHTML = `
            <div class="mision-card">
                <h2>${res.titulo}</h2>
                <p><strong>Por qué:</strong> ${res.porque}</p>
                <p><strong>Qué hacer:</strong> ${res.que_hacer}</p>
                <p><strong>Dónde:</strong> ${res.donde}</p>
                <button onclick="window.open('${res.gps}')">EJECUTAR RUTA</button>
            </div>
        `;
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
