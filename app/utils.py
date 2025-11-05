import cv2
import numpy as np
from typing import List, Tuple

def to_rgb(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

def draw_annotations(image: np.ndarray, boxes: List[Tuple[int,int,int,int]], labels: List[str]):
    for (x, y, w, h), label in zip(boxes, labels):
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 220, 50), 2, cv2.LINE_AA)
    return image

def encode_image_bgr_to_jpeg_bytes(image_bgr: np.ndarray) -> bytes:
    ok, buf = cv2.imencode('.jpg', image_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ok:
        raise RuntimeError("Failed to encode image to JPEG")
    return buf.tobytes()
