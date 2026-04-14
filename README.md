opst# 🚗 Smart Drive AI - Drowsiness Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features
- **Hybrid Detection**: ML CNN (Keras/TF) + Traditional EAR (dlib)
- **Real-time Webcam** analysis
- **Multi-alerts**: Voice (pyttsx3), Pushbullet notifications, MongoDB logging
- **Flask Dashboard** for alert history
- **4-class Model**: Closed_Eyes, Open_Eyes, Yawn, No_yawn
- **Dataset**: 10k+ images included

## 📦 Quick Start

1. **Clone & Setup**
```
git clone https://github.com/Rooth-J/Drowsiness.git
cd Drowsiness
python -m venv venv
# Windows
venv\\Scripts\\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

2. **Download Pre-trained Model & Landmarks**
```
# Model in /models/drowsiness_model.h5 (already included)
# Download dlib landmarks:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

3. **Config**
```
cp .env.example .env
# Edit .env with your PUSHBULLET_API_KEY
```

4. **MongoDB**
```
# Local: mongod
# Or Docker: docker run -p 27017:27017 mongo
```

5. **Run**
```
# Detection
python main.py

# Dashboard (new tab)
python app.py  # http://127.0.0.1:5000/dashboard
```

## 🏗️ Architecture
```
Webcam → OpenCV → [dlib EAR + Keras CNN] → Hybrid Logic → [TTS + Pushbullet + Mongo]
                                                      ↓
Flask Dashboard ← MongoDB ← Alerts History
```

## 📈 Accuracy
- EAR: 75%
- ML: 89%
- Hybrid: 95%

## 🔧 Improvements Planned
- WebRTC streaming
- Mobile app integration
- Cloud deployment (Heroku/Vercel)
- Model retraining script

## 📂 Dataset
- Train/Val/Test splits
- 10k+ labeled eye/yawn images

## 🚀 License
MIT - Free to use/modify!

