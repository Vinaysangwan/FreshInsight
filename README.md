# 🍎 Fresh Insight – AI-Based Fruit & Vegetable Analyzer

Fresh Insight is a web-based AI application that analyzes images of fruits and vegetables to provide real-time insights such as nutritional values and freshness level.

The system uses a cloud-based computer vision model to identify food items from images and integrates a nutrition API to deliver accurate dietary information.

---

## 🔍 Features

* 📸 Image-based fruit & vegetable detection
* 🧠 AI-powered classification using vision models
* 🥗 Nutritional information (calories, protein)
* ⏳ Freshness estimation (Fresh / Overripe / Rotten)
* ⚡ Real-time processing with responsive UI

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **AI Model:** Google Gemini Vision API
* **Nutrition API:** Edamam API

---

## ⚙️ How It Works

1. User uploads an image of a fruit or vegetable
2. The backend sends the image to a vision AI model
3. The model returns the food name, freshness, and confidence
4. The system fetches nutritional data from an API
5. Results are displayed on the frontend

---

## 🚀 Future Improvements

* Custom-trained fruit classification model
* Real-time camera detection
* Multi-object detection (YOLO)
* Mobile app integration

---

## 🔐 Security

API keys are stored securely using environment variables and are not exposed in the source code.

---

## 🎯 Use Case

This project demonstrates practical applications of AI in food analysis, nutrition tracking, and smart kitchen systems.
