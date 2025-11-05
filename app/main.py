from fastapi import FastAPI, WebSocket, UploadFile, File, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import base64, io, os, uuid, cv2, numpy as np

from .models import FrameMessage
from .recognition import FaceRecognizer
from .utils import draw_annotations, encode_image_bgr_to_jpeg_bytes

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "known"

app = FastAPI(title="Facial Recognition Demo", version="1.0.1")
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

recognizer = FaceRecognizer(DATA_DIR)
recognizer.train()
try:
    _cv_version = cv2.__version__
    _has_face = hasattr(cv2, "face")
except Exception:
    _cv_version = "unknown"
    _has_face = False

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "opencv_version": _cv_version,
        "opencv_face_module": _has_face,
        "recognizer_trained": recognizer.trained,
        "label_map": recognizer.label_map,
    }

@app.post("/api/recognize_image")
async def recognize_image(file: UploadFile = File(...)):
    contents = await file.read()
    file_bytes = np.frombuffer(contents, np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)
    boxes, labels = recognizer.recognize(img_bgr)
    annotated = draw_annotations(img_bgr.copy(), boxes, labels)
    jpeg = encode_image_bgr_to_jpeg_bytes(annotated)
    return StreamingResponse(io.BytesIO(jpeg), media_type="image/jpeg")

@app.post("/api/recognize_video")
async def recognize_video(file: UploadFile = File(...)):
    tmp_in = BASE_DIR / f"upload_{uuid.uuid4().hex}.mp4"
    tmp_out = BASE_DIR / f"processed_{uuid.uuid4().hex}.mp4"
    with open(tmp_in, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(str(tmp_in))
    if not cap.isOpened():
        tmp_in.unlink(missing_ok=True)
        return JSONResponse({"error": "Could not open video"}, status_code=400)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(str(tmp_out), fourcc, fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        boxes, labels = recognizer.recognize(frame)
        annotated = draw_annotations(frame, boxes, labels)
        writer.write(annotated)
    cap.release()
    writer.release()
    tmp_in.unlink(missing_ok=True)
    return FileResponse(str(tmp_out), media_type="video/mp4", filename=tmp_out.name)

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            msg = FrameMessage.model_validate_json(data)
            b64 = msg.image_b64.split(",")[-1]
            img_bytes = base64.b64decode(b64)
            arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                await ws.send_json({"ok": False, "error": "bad-frame"})
                continue
            boxes, labels = recognizer.recognize(frame)
            await ws.send_json({"ok": True, "boxes": boxes, "labels": labels})
    except Exception:
        await ws.close()
