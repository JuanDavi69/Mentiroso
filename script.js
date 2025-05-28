const video = document.getElementById("video");
const detectBtn = document.getElementById("detectBtn");
const resultText = document.getElementById("resultText");
const popupContainer = document.getElementById("popupContainer");

const challenges = [
  "Canta una canción ridícula",
  "Imita a un animal",
  "Cuenta un secreto embarazoso",
  "Baila frente a la cámara",
  "Imita el sonido de una vaca durante 3 segundos",
"Habla como robot durante 5 segundos",
"Baila sin música por 7 segundos",
"Cuenta un chiste corto y ríe fuerte",
"Haz el saludo de un superhéroe invisible",
"Camina en puntillas alrededor de la cámara durante 5 segundos",
"Sopla aire por la nariz exageradamente 4 veces",
"Hazte un selfie haciendo cara de detective por 6 segundos",
"Mueve solo las cejas como si tuvieras antenas durante 5 segundos",
"Imita a un pajarito cantando una nota alta por 4 segundos",
"Finge que eres un espía susurrando un mensaje secreto",
"Realiza un mini monólogo dramático de 10 segundos",
"Pretende que tu dedo es un micrófono y canta una estrofa",
"Salta en un solo pie durante 6 segundos",
"Actúa como si estuvieras tropezando sin caer",
"Haz el sonido de un tambor con las palmas de las manos",
"Finge que estás atornillando algo invisible durante 5 segundos",
"Imita el bramido de un león por 4 segundos",
"Cuenta hasta cinco en voz de villano de película",
"Haz una reverencia elegante como si fueras realeza",
"Ladra como un perro pequeño por 4 segundos",
"Baila el paso del robot durante 6 segundos",
"Haz una pose de yoga graciosa sin caerte",
"Imita el sonido de una sirena de policía por 3 segundos",
"Finge que escribes en una máquina de escribir antigua",
"Susurra un cumplido al borde de la cámara",
"Parpadea rápidamente como si fueras disco de rave",
"Gira en círculo tres veces y saluda al terminar",
"Finge que sostienes una pelota caliente y pásala de mano",
"Simula estar pintando un retrato por 5 segundos",
"Haz el sonido de un cohete despegando durante 3 segundos",
"Imita el sonido de teclas de piano rápidamente",
"Finge que lees un poema con mucho dramatismo",
"Finge que estás atrapado en una caja transparente",
"Imita a un robot intentando cargarse con electricidad",
"Pretende que montas una bicicleta invisible por 5 segundos",
"Aplaude lentamente como jurado de talento",
"Imita un tombo leyendo texto sin parar",
"Haz como que afilas un lápiz imaginario",
"Susurra un secreto y luego ríe en voz baja",
"Haz una caminata de modelo por 5 segundos",
"Finge que miras por un telescopio gigante",
"Inventa un breve eslogan publicitario para tu nariz",
"Imita el sonido de una alarma de despertador fuerte",
"Finge que giras una llave enorme en una cerradura",
"Haz como que sostienes una taza caliente y la bebes",
"Imita un pingüino caminando durante 6 segundos",
"Pretende que estás lanzando confeti al aire",
"Finge que izas una bandera invisible durante 5 segundos",
"Cuenta un trabalenguas rápido y claro"
];

// Inicia la cámara
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => alert("No se pudo acceder a la cámara: " + err));

// Botón de detección
detectBtn.addEventListener("click", () => {
  showProgressPopup(() => {
    const isLie = Math.random() < 0.5;
    const confidence = (Math.random() * 0.5 + 0.5).toFixed(2);
    if (isLie) {
      showPopup(`😡 ¡ERES UN MENTIROSO! (${confidence * 100}%)`, () => {
        showChallenge(confidence);
      });
    } else {
      showPopup(`😇 DICE LA VERDAD (${confidence * 100}%)`);
      resultText.textContent = `Resultado: Verdad (${confidence * 100}%)`;
    }
  });
});

function showProgressPopup(callback) {
  const popup = document.createElement("div");
  popup.className = "popup";
  popup.innerHTML = `
    <p>🔍 Detectando...</p>
    <div class="progress-bar"><div class="progress-fill" id="fill"></div></div>
  `;
  popupContainer.innerHTML = "";
  popupContainer.style.display = "flex";
  popupContainer.appendChild(popup);
  let progress = 0;
  const fill = popup.querySelector(".progress-fill");

  const interval = setInterval(() => {
    progress += 33;
    fill.style.width = `${progress}%`;
    if (progress >= 100) {
      clearInterval(interval);
      popupContainer.style.display = "none";
      callback();
    }
  }, 1000);
}

function showPopup(message, onClose) {
  const popup = document.createElement("div");
  popup.className = "popup";
  popup.innerHTML = `<p>${message}</p>`;
  popupContainer.innerHTML = "";
  popupContainer.style.display = "flex";
  popupContainer.appendChild(popup);

  setTimeout(() => {
    popupContainer.style.display = "none";
    if (onClose) onClose();
  }, 2500);
}

function showChallenge(confidence) {
  const challenge = challenges[Math.floor(Math.random() * challenges.length)];
  const popup = document.createElement("div");
  popup.className = "popup";
  popup.innerHTML = `
    <p>🕵️ Reto: ${challenge}</p>
    <div class="progress-bar"><div class="progress-fill" id="fillChallenge"></div></div>
  `;
  popupContainer.innerHTML = "";
  popupContainer.style.display = "flex";
  popupContainer.appendChild(popup);

  let progress = 0;
  const fill = popup.querySelector(".progress-fill");
  const interval = setInterval(() => {
    progress += 20;
    fill.style.width = `${progress}%`;
    if (progress >= 100) {
      clearInterval(interval);
      popupContainer.style.display = "none";
      resultText.textContent = `Resultado: Mentira (${confidence * 100}%)`;
    }
  }, 1000);
}
