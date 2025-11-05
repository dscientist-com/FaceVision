let ws = null;
let streaming = false;
let canvas, ctx, video;

function drawBoxes(boxes, labels){
  if(!canvas || !ctx) return;
  ctx.clearRect(0,0,canvas.width, canvas.height);
  ctx.lineWidth = 2;
  boxes.forEach((b, i) => {
    const [x, y, w, h] = b;
    ctx.strokeStyle = "#00ff88";
    ctx.strokeRect(x, y, w, h);
    ctx.font = "14px sans-serif";
    ctx.fillStyle = "#00ff88";
    ctx.fillText(labels[i] ?? "face", x, Math.max(0, y - 6));
  });
}

async function startCam(){
  video = document.getElementById("video");
  canvas = document.getElementById("overlay");
  ctx = canvas.getContext("2d");

  const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:false});
  video.srcObject = stream;
  await video.play();

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ws = new WebSocket(`ws://${location.host}/ws`);
  ws.onmessage = (ev)=>{
    const msg = JSON.parse(ev.data);
    if(msg.ok){
      drawBoxes(msg.boxes, msg.labels);
    }
  };
  ws.onopen = ()=>{
    streaming = true;
    sendFrames();
  };
  ws.onclose = ()=>{ streaming = false; };
}

function sendFrames(){
  if(!streaming || !ws) return;
  const off = document.createElement("canvas");
  off.width = video.videoWidth; off.height = video.videoHeight;
  const ictx = off.getContext("2d");
  ictx.drawImage(video, 0, 0);
  const dataUrl = off.toDataURL("image/jpeg", 0.7);
  ws.send(JSON.stringify({image_b64: dataUrl}));
  setTimeout(sendFrames, 120);
}

async function onImageUpload(ev){
  const file = ev.target.files[0];
  if(!file) return;
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/recognize_image",{method:"POST", body:form});
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const out = document.getElementById("imgOut");
  out.src = url;
}

async function onVideoUpload(ev){
  const file = ev.target.files[0];
  if(!file) return;
  const form = new FormData();
  form.append("file", file);
  const btn = document.getElementById("vidBtn");
  btn.disabled = true; btn.textContent = "Processing...";
  const res = await fetch("/api/recognize_video",{method:"POST", body:form});
  btn.disabled = false; btn.textContent = "Upload video";
  if(!res.ok){ alert("Video error"); return; }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.getElementById("vidLink");
  a.href = url;
  a.download = "processed.mp4";
  a.classList.remove("hidden");
}
window.addEventListener("DOMContentLoaded", ()=>{
  document.getElementById("imageInput").addEventListener("change", onImageUpload);
  document.getElementById("videoInput").addEventListener("change", onVideoUpload);
});
