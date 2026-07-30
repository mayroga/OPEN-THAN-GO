// ==========================================================================================
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Frontend Logic & UI)
// Company: May Roga LLC - Version: 1.0.1 - Producción Ultra-Segura
// ==========================================================================================

(function(){
const PERFILES_ESPECIALES={

activo:false,
perfilSeleccionado:"veterano",
keywordsSeleccionadas:[],
textoPdfExtraido:"",
grabando:false,
timerGrabacion:null,
recorridoMisiones:[],
recognitionInstance:null,

TEXTOS:{
es:{
switchEspecial:"Módulo Especial",
switchNormal:"Open Than Go",
seleccionaPerfil:"Selecciona tu perfil de autocuidado:",
veterano:"Veteranos",
adulto_mayor:"Adultos Mayores",
gubernamental:"Trabajadores Públicos",
lblKeywords:"Palabras clave flotantes (Toca para seleccionar):",
lblTexto:"Comparte tus observaciones o pega contenido aquí:",
placeholderTexto:"Escribe libremente sobre tu entorno actual...",
lblPdf:"Cargar documento de orientación (PDF):",
lblMic:"Micro de autocuidado (Máx 1 min):",
btnMicGrabar:"🎙️ Grabar Voz",
btnMicDetener:"🛑 Detener (Transcripción...)",
btnProcesar:"Activar Mando Especial",
btnReporte:"📋 Solicitar Reporte de Bienestar",
errorMic:"El reconocimiento de voz o micrófono no está disponible.",
alertPdf:"Contenido del documento cargado con éxito.",
errorProcesar:"Por favor, introduce texto o selecciona palabras clave."
},
en:{
switchEspecial:"Special Module",
switchNormal:"Open Than Go",
seleccionaPerfil:"Select your self-care profile:",
veterano:"Veterans",
adulto_mayor:"Senior Citizens",
gubernamental:"Public Servants",
lblKeywords:"Floating keywords (Tap to select):",
lblTexto:"Share your observations or paste content here:",
placeholderTexto:"Write freely about your current environment...",
lblPdf:"Load orientation document (PDF):",
lblMic:"Self-care microphone (Max 1 min):",
btnMicGrabar:"🎙️ Record Voice",
btnMicDetener:"🛑 Stop (Transcribing...)",
btnProcesar:"Activate Special Control",
btnReporte:"📋 Request Wellbeing Report",
errorMic:"Voice recognition or microphone is not available.",
alertPdf:"Document content loaded successfully.",
errorProcesar:"Please enter text or select keywords."
}
},

init(){
this.inyectarEstilosAdicionales();
this.crearBotonAlternancia();
this.crearContenedorInterfazEspecial();
console.log("Módulo Especial inicializado correctamente.");
},

inyectarEstilosAdicionales(){
if(document.getElementById("styles-perfiles-especiales"))return;
let css=document.createElement("style");
css.id="styles-perfiles-especiales";
css.textContent=`

.switch-perfiles-container{display:flex;justify-content:center;margin:10px 0}
.btn-switch-perfil{background:#111;color:#888;border:1px solid #333;padding:8px 16px;border-radius:20px;font-weight:bold;cursor:pointer;transition:.3s;font-size:.85rem}
.btn-switch-perfil.active{background:var(--accent,#d84315);color:#fff;border-color:var(--accent,#d84315)}
.perfil-selector-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:15px}
.btn-perfil-opcion{background:#0a0a0a;border:1px solid #222;color:#aaa;padding:12px 6px;border-radius:6px;cursor:pointer;font-weight:bold;font-size:.8rem}
.btn-perfil-opcion.active{border-color:#00bcd4;color:#00bcd4;background:rgba(0,188,212,.05)}
.keywords-floating-box{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;min-height:40px;padding:8px;background:#070707;border:1px dashed #222;border-radius:6px}
.badge-keyword{background:#151515;border:1px solid #333;color:#bbb;padding:6px 12px;border-radius:15px;font-size:.75rem;cursor:pointer}
.badge-keyword.selected{background:#4caf50;color:#fff;border-color:#4caf50}
.media-controls-wrapper{display:flex;gap:10px;margin:12px 0}
.btn-audio-action{flex:1;padding:12px;font-weight:bold;border-radius:4px;border:none;cursor:pointer}
.file-pdf-input{background:#0a0a0a;border:1px solid #222;color:#888;padding:8px;width:100%}
.reporte-output-box{background:#050505;border:1px solid #222;border-radius:8px;padding:20px;margin-top:20px}

`;
document.head.appendChild(css);
},

crearBotonAlternancia(){
if(document.getElementById("btn-master-toggle-modulo"))return;
const langBar=document.querySelector(".lang-bar");
if(!langBar)return;

const container=document.createElement("div");
container.className="switch-perfiles-container";

const btn=document.createElement("button");
btn.className="btn-switch-perfil";
btn.id="btn-master-toggle-modulo";
btn.innerText=this.TEXTOS[window.KERNEL?.idiomaActual||"es"].switchEspecial;

btn.onclick=()=>{
this.activo=!this.activo;
btn.classList.toggle("active",this.activo);
btn.innerText=this.activo?
this.TEXTOS[window.KERNEL.idiomaActual].switchNormal:
this.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
this.alternarVisibilidadPaneles();
};

container.appendChild(btn);
langBar.parentNode.insertBefore(container,langBar.nextSibling);
},

crearContenedorInterfazEspecial(){
if(document.getElementById("panel-perfiles-especiales"))return;
const wrapperForm=document.getElementById("wrapper-form");
if(!wrapperForm)return;

const div=document.createElement("div");
div.id="panel-perfiles-especiales";
div.className="hidden";
div.style.marginTop="15px";
wrapperForm.parentNode.insertBefore(div,wrapperForm.nextSibling);
},
alternarVisibilidadPaneles(){

const wrapperForm=document.getElementById("wrapper-form");
const panelEspecial=document.getElementById("panel-perfiles-especiales");
const wrapperInteractive=document.getElementById("wrapper-interactive");
const pantallaCierre=document.getElementById("pantalla-cierre");

if(this.activo){

if(wrapperForm)wrapperForm.classList.add("hidden");
if(wrapperInteractive)wrapperInteractive.classList.add("hidden");
if(pantallaCierre)pantallaCierre.classList.add("hidden");

if(panelEspecial){
panelEspecial.classList.remove("hidden");
this.renderizarInterfazEspecial();
}

if(window.KERNEL?.hablar)
window.KERNEL.hablar(
window.KERNEL.idiomaActual==="es"?
"Entrando al entorno de personalización adaptada.":
"Entering tailored personalization environment."
);

}else{

if(panelEspecial)panelEspecial.classList.add("hidden");

if(wrapperForm){
wrapperForm.classList.remove("hidden");
if(window.KERNEL?.inyectarBloquePreguntas)
window.KERNEL.inyectarBloquePreguntas();
}

}

},


renderizarInterfazEspecial(){

const container=document.getElementById("panel-perfiles-especiales");
if(!container)return;

const lang=window.KERNEL?.idiomaActual||"es";
const t=this.TEXTOS[lang];

container.innerHTML=`

<div class="especial-header">
<h2>OPEN THAN GO - TAILORED EXPERIENCE</h2>
<p>${t.seleccionaPerfil}</p>
</div>

<div class="perfil-selector-grid">

<button class="btn-perfil-opcion active" data-perf="veterano">
${t.veterano}
</button>

<button class="btn-perfil-opcion" data-perf="adulto_mayor">
${t.adulto_mayor}
</button>

<button class="btn-perfil-opcion" data-perf="gubernamental">
${t.gubernamental}
</button>

</div>


<h4>${t.lblKeywords}</h4>

<div id="box-keywords-flotantes" class="keywords-floating-box"></div>


<h4>${t.lblTexto}</h4>

<textarea id="txt-input-especial"
placeholder="${t.placeholderTexto}"
style="width:100%;min-height:100px;">
</textarea>


<h4>${t.lblPdf}</h4>

<input id="file-pdf-especial"
class="file-pdf-input"
type="file"
accept=".pdf">


<h4>${t.lblMic}</h4>

<div class="media-controls-wrapper">

<button id="btn-mic-especial"
class="btn-audio-action">
${t.btnMicGrabar}
</button>

</div>


<button id="btn-procesar-especial"
class="btn-audio-action">
${t.btnProcesar}
</button>


<button id="btn-reporte-especial"
class="btn-audio-action">
${t.btnReporte}
</button>


<div id="wrapper-reporte-output"
class="reporte-output-box hidden">
</div>

`;

this.enlazarEventosInterfaz();
this.cargarKeywordsPerfil();

},


enlazarEventosInterfaz(){

const container=document.getElementById("panel-perfiles-especiales");
if(!container)return;


container.querySelectorAll(".btn-perfil-opcion").forEach(btn=>{

btn.onclick=()=>{

container.querySelectorAll(".btn-perfil-opcion")
.forEach(b=>b.classList.remove("active"));

btn.classList.add("active");

this.perfilSeleccionado=
btn.getAttribute("data-perf");

this.keywordsSeleccionadas=[];

this.cargarKeywordsPerfil();

};

});


const fileInput=document.getElementById("file-pdf-especial");

if(fileInput){

fileInput.onchange=e=>{

const file=e.target.files[0];

if(file){

this.textoPdfExtraido=
`Contenido del documento voluntario: ${file.name}. Orientación de autocuidado activo.`;

alert(this.TEXTOS[
window.KERNEL?.idiomaActual||"es"
].alertPdf);

}

};

}


const btnMic=document.getElementById("btn-mic-especial");

if(btnMic)
btnMic.onclick=()=>this.gestionarFlujoMicrofono(btnMic);


const btnProcesar=document.getElementById("btn-procesar-especial");

if(btnProcesar)
btnProcesar.onclick=()=>this.ejecutarMandoEspecial();


const btnReporte=document.getElementById("btn-reporte-especial");

if(btnReporte)
btnReporte.onclick=()=>this.generarReporteBienestar();


},
cargarKeywordsPerfil(){

const box=document.getElementById("box-keywords-flotantes");
if(!box)return;

box.innerHTML="";

const lang=window.KERNEL?.idiomaActual||"es";

fetch(`/api/perfiles-especiales/config?perfil=${this.perfilSeleccionado}&lang=${lang}`)
.then(r=>r.json())
.then(data=>{

if(data.keywords){

data.keywords.forEach(kw=>{

const b=document.createElement("div");

b.className="badge-keyword";

b.innerText=kw;

b.onclick=()=>{

b.classList.toggle("selected");

if(b.classList.contains("selected")){

this.keywordsSeleccionadas.push(kw);

}else{

this.keywordsSeleccionadas=
this.keywordsSeleccionadas.filter(k=>k!==kw);

}

};

box.appendChild(b);

});

}

})

.catch(e=>console.error("Error cargando keywords:",e));

},


gestionarFlujoMicrofono(btn){

const lang=window.KERNEL?.idiomaActual||"es";

const t=this.TEXTOS[lang];

const SpeechRecognition=
window.SpeechRecognition||
window.webkitSpeechRecognition;


if(!SpeechRecognition){

alert(t.errorMic);

return;

}


if(!this.grabando){

this.grabando=true;

btn.style.background="#dc2626";

btn.innerText=t.btnMicDetener;


this.recognitionInstance=
new SpeechRecognition();


this.recognitionInstance.lang=
lang==="es"?"es-US":"en-US";


this.recognitionInstance.interimResults=false;

this.recognitionInstance.continuous=true;


this.recognitionInstance.onresult=(event)=>{

const index=event.resultIndex;

const textoVoz=
event.results[index][0].transcript;


const txtArea=
document.getElementById("txt-input-especial");


if(txtArea&&textoVoz){

txtArea.value=
(txtArea.value+" "+textoVoz).trim();

}

};


this.recognitionInstance.onerror=(e)=>{

console.error("Speech error:",e.error);

this.detenerGraboHardware(btn,t);

};


this.recognitionInstance.start();


this.timerGrabacion=setTimeout(()=>{

this.detenerGraboHardware(btn,t);

},60000);


}else{

this.detenerGraboHardware(btn,t);

}

},


detenerGraboHardware(btn,t){

this.grabando=false;

clearTimeout(this.timerGrabacion);


btn.style.background="#222";

btn.innerText=t.btnMicGrabar;


if(this.recognitionInstance){

this.recognitionInstance.stop();

}

},


async ejecutarMandoEspecial(){

const txtArea=
document.getElementById("txt-input-especial");


const txtInput=
txtArea?
txtArea.value.trim():"";


const lang=
window.KERNEL?.idiomaActual||"es";


if(
txtInput.length===0 &&
this.keywordsSeleccionadas.length===0
){

alert(this.TEXTOS[lang].errorProcesar);

return;

}


const containerInteractive=
document.getElementById("wrapper-interactive");


const panelPerfiles=
document.getElementById("panel-perfiles-especiales");


if(panelPerfiles)
panelPerfiles.classList.add("hidden");


if(containerInteractive){

containerInteractive.innerHTML=`

<div style="text-align:center;padding:40px 0;">

<h2 style="color:#fff;font-size:1.1rem;">

${lang==="es"?
"ESTABLECIENDO ENTORNO ESPECIAL...":
"ESTABLISHING SPECIAL ENVIRONMENT..."}

</h2>

</div>

`;

containerInteractive.classList.remove("hidden");

}


const payload={

perfil:this.perfilSeleccionado,

lang:lang,

texto:txtInput,

keywords_seleccionadas:
this.keywordsSeleccionadas,

contexto_pdf:
this.textoPdfExtraido

};


try{


const res=await fetch(
"/api/perfiles-especiales/procesar",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(payload)

});


const data=await res.json();


if(
data.status==="success" &&
window.KERNEL
){


window.KERNEL.tipoEscapeGlobal=
"ACCION_CAMPO";


window.KERNEL.indiceMision=0;


window.KERNEL.pasosMisiones=
data.misiones||[];


window.KERNEL.mensajeCalidezHumanaActual=
data.calidez_humana;


if(
data.misiones &&
data.misiones.length>0
){

this.recorridoMisiones.push(
data.misiones[0].destino_titulo
);

}


if(window.KERNEL.hablar)
window.KERNEL.hablar(data.calidez_humana);


if(window.KERNEL.mostrarOpcionesSalir)
window.KERNEL.mostrarOpcionesSalir(containerInteractive);


const btnVolver=
document.getElementById("btn-volver-app");


if(btnVolver)
btnVolver.classList.remove("hidden");


}


}catch(e){

console.error(
"Error al procesar mando especial:",
e
);

this.activo=false;

this.alternarVisibilidadPaneles();

}

},
generarReporteBienestar(){

const txtArea=document.getElementById("txt-input-especial");

const txtInput=txtArea?
txtArea.value.trim():"";

const wrapperReporte=
document.getElementById("wrapper-reporte-output");

if(!wrapperReporte)return;


const lang=
window.KERNEL?.idiomaActual||"es";


const infoCompartida=[
...this.keywordsSeleccionadas
];


if(txtInput)
infoCompartida.push(txtInput);


if(this.textoPdfExtraido)
infoCompartida.push("Documento de orientación.");


const payload={

perfil:this.perfilSeleccionado,

lang:lang,

recorrido:this.recorridoMisiones,

informacion_compartida:infoCompartida

};


fetch("/api/perfiles-especiales/reporte",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(payload)

})

.then(r=>r.json())

.then(data=>{


wrapperReporte.innerHTML=`

<h2>${data.titulo||""}</h2>

<h3>
${lang==="es"?
"Resumen descriptivo:":
"Descriptive Summary:"}
</h3>

<p>
${data.resumen_descriptivo||""}
</p>


<h3>
${lang==="es"?
"Recorrido de Orientación:":
"Orientation Journey:"}
</h3>

<ul>

${
(data.recorrido_realizado||[])
.map(r=>`<li>${r}</li>`)
.join("")
}

</ul>


<h3>
${lang==="es"?
"Dinámicas Sugeridas:":
"Suggested Dynamics:"}
</h3>

<ul>

${
(data.actividades_sugeridas||[])
.map(a=>`<li>${a}</li>`)
.join("")
}

</ul>


<h3>
${lang==="es"?
"Observaciones de Autocuidado:":
"Self-Care Observations:"}
</h3>

<p>
${data.observaciones_finales||""}
</p>


<span class="nota-legal-reporte">

${data.nota_legal||""}

</span>

`;


wrapperReporte.classList.remove("hidden");


if(window.KERNEL?.hablar){

window.KERNEL.hablar(
lang==="es"?
"Reporte descriptivo de bienestar listo.":
"Descriptive wellbeing report is ready."
);

}


})

.catch(e=>{

console.error(
"Error compilando reporte:",
e
);

});


},


}; // FIN OBJETO PERFILES_ESPECIALES


function intentarMontarModulo(){

const langBar=document.querySelector(".lang-bar");

const wrapperForm=document.getElementById("wrapper-form");


if(
langBar &&
wrapperForm &&
window.KERNEL
){

PERFILES_ESPECIALES.init();

}else{

setTimeout(
intentarMontarModulo,
150
);

}

}


intentarMontarModulo();


window.PERFILES_ESPECIALES=
PERFILES_ESPECIALES;


})();
