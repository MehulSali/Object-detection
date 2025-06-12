const video = document.getElementById("video");
const statusDiv = document.getElementById("status");
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

let lastSpoken = "";

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
  video.srcObject = stream;
});

function speak(text) {
  const synth = window.speechSynthesis;
  if (!synth.speaking) {
    const utter = new SpeechSynthesisUtterance(text);
    synth.speak(utter);
  }
}

setInterval(() => {
  if (video.readyState === 4) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/jpeg");

    fetch("/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: dataURL })
    })
    .then(res => res.json())
    .then(data => {
      const objectPart = data.labels.length > 0 ? `I see ${data.labels.join(", ")}` : "";
      const textPart = data.text ? ` and I read: ${data.text}` : "";
      const fullSentence = objectPart + textPart;

      if (fullSentence && fullSentence !== lastSpoken) {
        statusDiv.textContent = fullSentence;
        speak(fullSentence);
        lastSpoken = fullSentence;
      }
    });
  }
}, 3000);
