/**
 * OPEN THAN GO | MANDO INTEGRAL NACIONAL
 * Motor de decisión profesional para el mercado USA.
 */

const App = {
    state: {
        perfil: {},
        isProcessing: false
    },

    init() {
        document.getElementById('btn-mando').addEventListener('click', () => this.handleAction());
    },

    async handleAction() {
        if (this.state.isProcessing) return;
        
        // Captura y validación de datos
        this.state.perfil = {
            zip: document.getElementById('inp-zip').value.trim(),
            mente: document.getElementById('inp-mente').value,
            acompanantes: document.getElementById('inp-acompanantes').value,
            presupuesto: document.getElementById('inp-presupuesto').value
        };

        if (!this.state.perfil.zip) return alert("ZIP Code es obligatorio para el cálculo nacional.");

        this.setUIProcessing(true);

        try {
            const response = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.state.perfil)
            });

            if (!response.ok) throw new Error("Mando no disponible");

            const res = await response.json();
            this.renderResult(res);
        } catch (e) {
            console.error("Fallo en el Mando:", e);
            this.setUIProcessing(false);
            alert("El sistema de mando está recalibrando. Intente de nuevo.");
        }
    },

    renderResult(res) {
        const wrapper = document.getElementById('wrapper-interactive');
        const content = document.getElementById('step-content');
        
        document.getElementById('wrapper-form').classList.add('hidden');
        wrapper.classList.remove('hidden');

        // Activación del protocolo de calma si es necesario
        if (res.requiere_calma) {
            document.getElementById('breath-circle').style.display = 'block';
            new Audio('/static/assets/calm.mp3').play().catch(() => {}); // Opcional
        }

        content.innerHTML = `
            <div class="mando-card">
                <h2>${res.titulo_destino}</h2>
                <p><strong>Propósito:</strong> ${res.proposito_terapeutico}</p>
                <div class="mision-box">
                    <p>${res.mision_activa}</p>
                </div>
                <button class="btn-gps" onclick="window.open('${res.gps_url}', '_blank')">
                    EJECUTAR RUTA
                </button>
            </div>
        `;
    },

    setUIProcessing(status) {
        this.state.isProcessing = status;
        document.getElementById('btn-mando').innerText = status ? "PROCESANDO..." : "RECIBIR MANDO";
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
