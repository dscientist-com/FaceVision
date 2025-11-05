import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple

FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class FaceRecognizer:
    def __init__(self, known_dir: Path):
        self.known_dir = known_dir
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            self.face_module_available = True
        except Exception:
            self.recognizer = None
            self.face_module_available = False
        self.label_map = {}
        self.trained = False

    def detect_faces(self, img_gray: np.ndarray) -> List[Tuple[int,int,int,int]]:
        faces = FACE_CASCADE.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        return faces

    def _load_training_data(self):
        images, labels = [], []
        label_id = 0
        self.label_map = {}
        if not self.known_dir.exists():
            return images, labels
        for person_dir in sorted([p for p in self.known_dir.iterdir() if p.is_dir()]):
            name = person_dir.name
            jpgs = list(person_dir.glob("*.jpg"))
            for img_path in jpgs:
                img = cv2.imread(str(img_path))
                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.detect_faces(gray)
                if len(faces) > 0:
                    x, y, w, h = sorted(faces, key=lambda b: b[2]*b[3], reverse=True)[0]
                    face_roi = gray[y:y+h, x:x+w]
                else:
                    face_roi = gray
                images.append(cv2.resize(face_roi, (200, 200)))
                labels.append(label_id)
            if jpgs:
                self.label_map[label_id] = name
                label_id += 1
        return images, labels

    def train(self):
        images, labels = self._load_training_data()
        if self.recognizer is not None and len(images) >= 2 and len(set(labels)) >= 1:
            self.recognizer.train(images, np.array(labels))
            self.trained = True
        else:
            self.trained = False

    def recognize(self, img_bgr: np.ndarray):
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        boxes = self.detect_faces(gray)
        labels = []
        for (x, y, w, h) in boxes:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            if self.recognizer is not None and self.trained:
                label_id, confidence = self.recognizer.predict(face_roi)
                if confidence < 85:
                    name = self.label_map.get(label_id, "unknown")
                    label = f"{name} ({confidence:.0f})"
                else:
                    label = "unknown"
            else:
                label = "face"
            labels.append(label)
        return boxes, labels
