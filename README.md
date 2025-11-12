# 👁️ Facial Recognition Web App  
*FastAPI + OpenCV | Real-Time Face Detection & Recognition*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-success.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-critical.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

### 🔍 Overview

This project is a **full-stack facial recognition web application** built with **Python (FastAPI + OpenCV)**.  
It demonstrates both **backend development** and **machine learning integration**, using a live camera stream, image uploads, and video uploads for facial recognition — all in one seamless interface.

The goal is to showcase real-world **Python full-stack development** and **computer vision** skills.

---

## 🧠 Features

- **🎥 Live Camera Recognition** – Detects faces in real-time using your webcam (via WebSocket).
- **🖼️ Image Upload Recognition** – Upload an image and receive the annotated result.
- **🎞️ Video Upload Recognition** – Upload a video, process it on the server, and download the annotated file.
- **⚙️ Auto Model Training** – Automatically trains on face images stored in `data/known/<person_name>/`.
- **💡 No Signup Required** – Works instantly in the browser.
- **🧰 Lightweight & Local** – Runs fully offline using CPU; no GPU needed.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | FastAPI (Python 3.10+) |
| **Frontend** | HTML, CSS, JavaScript |
| **Machine Learning** | OpenCV (Haar Cascade + LBPHFaceRecognizer) |
| **Data Handling** | NumPy, Pillow |
| **Runtime** | Uvicorn |

---

## 🚀 Getting Started

### 1️⃣ Clone this Repository

```bash
git clone https://github.com/<yourusername>/facial_recognition_fullstack.git
cd facial_recognition_fullstack
```

### 2️⃣ Create & Activate a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Install the Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
uvicorn app.main:app --reload
```

Then open your browser at 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧩 How Recognition Works

1. **Haar Cascade Classifier** detects faces in real-time (CPU-only).  
2. **LBPHFaceRecognizer** (OpenCV Contrib) classifies faces based on trained data.  
3. The app automatically trains on any images found in `data/known/<person_name>/`.  
4. Recognized faces are labeled and displayed in real-time or on uploaded media.

---

## 🧪 Health Check

To verify installation, visit:  
👉 **[http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)**

Example response:
```json
{
  "ok": true,
  "opencv_version": "4.10.0",
  "opencv_face_module": true,
  "recognizer_trained": true,
  "label_map": {"0": "John"}
}
```

---

## 🧩 Training Your Model

To recognize specific people:

1. Create folders in `data/known/` for each person  
   Example: `data/known/Alice/`, `data/known/Bob/`
2. Add **3–10 clear JPG images** of each person.
3. Restart the app – it will train automatically.

If no faces are added, the app will still detect faces but label them as `"face"`.

---

## 🧰 Troubleshooting

| Issue | Possible Solution |
|-------|--------------------|
| **`cv2.face` not found** | Make sure `opencv-contrib-python` is installed (`pip install opencv-contrib-python`). |
| **No faces recognized** | Add more clear, frontal images for each person. |
| **Webcam access denied** | Allow camera access in your browser. |
| **Video processing too slow** | Try shorter video clips or resize before upload. |

---

## 📁 Project Structure

```
facial_recognition_fullstack/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── recognition.py         # Face detection and recognition logic
│   ├── models.py              # Pydantic models for data exchange
│   ├── utils.py               # Helper utilities for encoding/annotation
│   ├── static/                # Frontend assets (JS, CSS)
│   └── templates/             # HTML templates (Jinja2)
│
├── data/
│   └── known/                 # Training data folders
│
├── requirements.txt
├── run.bat / run.sh
└── README.md
```

---

## 🧍‍♂️ About Me

**John Doe**  
📧 atif@dscientist.com  
_Data Scientist | Machine Learning Enthusiast | Transforming Data into Insights_  

**Core Skills:**  
Python • FastAPI • OpenCV • Scikit-learn • SQL • Django • React • Tableau • Machine Learning

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute it with attribution.

---

⭐ **If you found this project helpful, consider giving it a star!**  
It helps others discover the repository and supports future improvements. 🌟
