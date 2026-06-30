let configuracion = { 
    idioma: 'es', 
    puedes_salir: true, 
    bolsillo: 'cero' 
}; 

const textos = { 
    es: { 
        subtitle: "Tu botón de escape inmediato para romper la monotonía urbana.", 
        lblState: "Estado / State:", 
        lblZip: "ZIP Code (5 dígitos):", 
        lblPocket: "¿Cuál es tu presupuesto real para hoy?", 
        pocketCero: "GASTO $0 HOY", 
        pocketMod: "MODERADO", 
        pocketLibre: "LIBRE", 
        lblMode: "¿Puedes o quieres salir de casa hoy?", 
        btnOut: "🟢 SÍ, SALIR", 
        btnIn: "🏠 EN CASA", 
        lblText: "Desahógate aquí (Escribe libremente lo que traigas en la mente):", 
        placeholder: "Escribe si estás cansado de la rutina, preocupado por biles o el trabajo, solo, o con niños aburridos...", 
        btnSubmit: "SÁCAME DE LA MONOTONÍA", 
        alertZip: "Por favor, ingresa un código postal (ZIP Code) válido de 5 dígitos.", 
        alertError: "Ocurrió un inconveniente al conectar con el servidor de OPEN THAN GO. Inténtalo de nuevo.", 
        btnMaps: "🗺️ ABRIR RUTA EN MI MAPA GRATIS" 
    }, 
    en: { 
        subtitle: "Your instant escape button to break free from urban monotony.", 
        lblState: "State / Estado:", 
        lblZip: "ZIP Code (5 digits):", 
        lblPocket: "What is your real budget for today?", 
        pocketCero: "$0 SPENDING", 
        pocketMod: "MODERATE", 
        pocketLibre: "FREE BUDGET", 
        lblMode: "Can you or do you want to leave the house today?", 
        btnOut: "🟢 YES, GO OUT", 
        btnIn: "🏠 STAY HOME", 
        lblText: "Vent here (Write freely whatever is on your mind):", 
        placeholder: "Write if you are tired of the routine, worried about bills or work, alone, or with bored kids...", 
        btnSubmit: "BREAK THE MONOTONY", 
        alertZip: "Please enter a valid 5-digit ZIP Code.", 
        alertError: "An issue occurred while connecting to the OPEN THAN GO server. Please try again.", 
        btnMaps: "🗺️ OPEN ROUTE IN MY MAP FOR FREE" 
    } 
}; 

function cambiarIdioma(nuevoIdioma) { 
    configuracion.idioma = nuevoIdioma; 
    document.getElementById('lang-es').classList.toggle('active', nuevoIdioma === 'es'); 
    document.getElementById('lang-en').classList.toggle('active', nuevoIdioma === 'en'); 
    
    const t = textos[nuevoIdioma]; 
    document.getElementById('txt-subtitle').innerText = t.subtitle; 
    document.getElementById('lbl-state').innerText = t.lblState; 
    document.getElementById('lbl-zip').innerText = t.lblZip; 
    document.getElementById('lbl-pocket').innerText = t.lblPocket; 
    document.getElementById('pocket-cero').innerText = t.pocketCero; 
    document.getElementById('pocket-mod').innerText = t.pocketMod; 
    document.getElementById('pocket-libre').innerText = t.pocketLibre; 
    document.getElementById('lbl-mode').innerText = t.lblMode; 
    document.getElementById('mode-out').innerText = t.btnOut; 
    document.getElementById('mode-in').innerText = t.btnIn; 
    document.getElementById('lbl-text').innerText = t.lblText; 
    document.getElementById('inp-text').placeholder = t.placeholder; 
    document.getElementById('btn-submit').innerText = t.btnSubmit; 
    document.getElementById('res-maps').innerText = t.btnMaps; 
    document.getElementById('result-box').style.display = 'none'; 
} 

function setBolsillo(tipoBolsillo) { 
    configuracion.bolsillo = tipoBolsillo; 
    document.getElementById('pocket-cero').classList.toggle('active', tipoBolsillo === 'cero'); 
    document.getElementById('pocket-mod').classList.toggle('active', tipoBolsillo === 'moderado'); 
    document.getElementById('pocket-libre').classList.toggle('active', tipoBolsillo === 'libre'); 
} 

function setModalidad(salir) { 
    configuracion.puedes_salir = salir; 
    document.getElementById('mode-out').classList.toggle('active', salir); 
    document.getElementById('mode-in').classList.toggle('active', !salir); 
    
    const campoZip = document.getElementById('inp-zip'); 
    if (!salir) { 
        campoZip.style.opacity = '0.4'; 
        campoZip.disabled = true; 
    } else { 
        campoZip.style.opacity = '1'; 
        campoZip.disabled = false; 
    } 
} 

function ejecutarEscape() { 
    const estado = document.getElementById('inp-state').value; 
    const zip = document.getElementById('inp-zip').value.trim(); 
    const textoLibre = document.getElementById('inp-text').value.trim(); 
    const t = textos[configuracion.idioma]; 

    if (configuracion.puedes_salir && (zip.length !== 5 || isNaN(zip))) { 
        alert(t.alertZip); 
        return; 
    } 

    const payload = { 
        puedes_salir: configuracion.puedes_salir, 
        idioma: configuracion.idioma, 
        zip_code: zip, 
        estado: estado, 
        bolsillo: configuracion.bolsillo, 
        texto_libre: textoLibre 
    }; 

    // CONEXIÓN DIRECTA Y LIQUIDACIÓN DE ERRORES DE RED
    fetch('/diagnostico-kamizen', { 
        method: 'POST', 
        headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json' 
        }, 
        body: JSON.stringify(payload) 
    }) 
    .then(response => response.json()) 
    .then(data => { 
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('res-title').innerText = data.titulo; 
        document.getElementById('res-location').innerText = data.lugar; 
        
        // CONEXIÓN PERFECTA CON TUS JSON: Muestra de forma secuencial las respiraciones, silencios y preguntas
        if (data.bloques_interactivos) { 
            let textoMisiones = ""; 
            data.bloques_interactivos.forEach(b => { 
                if (b.tx) { 
                    textoMisiones += `${b.tx}\n\n`; 
                } 
                if (b.story) { 
                    textoMisiones += `📖 STORY:\n${b.story}\n\n`; 
                } 
                if (b.inf) { 
                    textoMisiones += `💡 INFO:\n${b.inf}\n\n`; 
                } 
                if (b.c) { 
                    textoMisiones += `🌟 CONCLUSIÓN:\n${b.c}\n\n`; 
                } 
                if (b.q) { 
                    textoMisiones += `❓ CHALLENGE:\n${b.q}\n`; 
                    if (b.op && b.op.length > 0) { 
                        b.op.forEach((opcion, i) => { 
                            textoMisiones += `   [${i + 1}] ${opcion}\n`; 
                        }); 
                    } 
                    textoMisiones += `\n`; 
                } 
            }); 
            document.getElementById('res-steps').innerText = textoMisiones; 
        } 

        const btnMaps = document.getElementById('res-maps'); 
        if (data.modalidad === 'outdoor' && data.url_maps) { 
            btnMaps.href = data.url_maps; 
            btnMaps.style.display = 'block'; 
        } else { 
            btnMaps.style.display = 'none'; 
        } 

        const resultBox = document.getElementById('result-box'); 
        resultBox.style.display = 'block'; 
        resultBox.scrollIntoView({ behavior: 'smooth' }); 
    }) 
    .catch(error => { 
        console.error('Error detectado:', error); 
        alert(t.alertError); 
    }); 
}  
