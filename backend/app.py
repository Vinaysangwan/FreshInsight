import base64
import re
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────
# CONFIG  –  paste your free keys here
# ──────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EDAMAM_APP_ID  = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")

# ──────────────────────────────────────────────
'''

def identify_fruit(image_bytes: bytes) -> dict:
    """
    Send the image to Gemini 1.5 Flash and ask it to return
    name + freshness in strict JSON.
    """
    b64 = base64.b64encode(image_bytes).decode()

    prompt = """You are a fruit and vegetable expert.
Look at this image and respond ONLY with a JSON object — no markdown, no extra text.

Format:
{
  "name": "<common name of the fruit or vegetable, lowercase>",
  "freshness": "<one of: Fresh / Slightly Overripe / Overripe / Rotten>",
  "confidence": "<High / Medium / Low>"
}

If the image does not contain a fruit or vegetable, set name to "unknown".
"""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
            ]
        }]
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    )
    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()

    raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Strip optional ```json fences
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()

    return json.loads(raw)

'''
def get_nutrition(food: str) -> dict:
    """Fetch calories & protein from Edamam Nutrition API."""
    url = (
        f"https://api.edamam.com/api/nutrition-data"
        f"?app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        f"&ingr=100g%20{requests.utils.quote(food)}"
    )
    try:
        res = requests.get(url, timeout=10).json()
        calories = round(res.get("calories", 0))
        protein  = round(res["totalNutrients"]["PROCNT"]["quantity"], 1)
        return {"calories": calories, "protein": protein}
    except Exception:
        return {"calories": "N/A", "protein": "N/A"}
'''

# TODO: For Debug
def get_nutrition(food: str) -> dict:
    """Fetch calories & protein from Edamam Nutrition API."""
    url = (
        f"https://api.edamam.com/api/nutrition-data"
        f"?app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        f"&ingr=100g%20{requests.utils.quote(food)}"
    )
    try:
        res = requests.get(url, timeout=10).json()
 
        # ✅ Nutrients are nested under ingredients[0].parsed[0].nutrients
        parsed    = res["ingredients"][0]["parsed"][0]
        nutrients = parsed["nutrients"]
 
        calories = round(nutrients["ENERC_KCAL"]["quantity"])
        protein  = round(nutrients["PROCNT"]["quantity"], 1)
 
        return {"calories": calories, "protein": protein}
    except Exception as e:
        print("EDAMAM PARSE ERROR:", e)
        return {"calories": "N/A", "protein": "N/A"}
 
 
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400
 
    image_bytes = request.files["image"].read()
    if not image_bytes:
        return jsonify({"error": "Empty image file."}), 400
 
    # 1️⃣  Identify via Gemini Vision
    try:
        result = identify_fruit(image_bytes)
    except Exception as e:
        return jsonify({"error": f"Vision API error: {str(e)}"}), 500
 
    name = result.get("name", "unknown").lower()
    freshness  = result.get("freshness", "Unknown")
    confidence = result.get("confidence", "Low")
 
    if name == "unknown":
        return jsonify({"error": "No fruit or vegetable detected in the image."}), 422
 
    # 2️⃣  Fetch nutrition
    nutrition = get_nutrition(name)
 
    return jsonify({
        "name":       name.title(),
        "calories":   nutrition["calories"],
        "protein":    nutrition["protein"],
        "freshness":  freshness,
        "confidence": confidence
    })
 
 
if __name__ == "__main__":
    app.run(debug=True)
'''
#####################################################################################################3 
def identify_fruit(image_bytes: bytes) -> dict:
    """Send image to Gemini and get name + freshness."""
    b64 = base64.b64encode(image_bytes).decode()
 
    prompt = """You are a fruit and vegetable expert.
Look at this image and respond ONLY with a JSON object — no markdown, no extra text.
 
Format:
{
  "name": "<common name of the fruit or vegetable, lowercase>",
  "freshness": "<one of: Fresh / Slightly Overripe / Overripe / Rotten>",
  "confidence": "<High / Medium / Low>"
}
 
If the image does not contain a fruit or vegetable, set name to "unknown".
"""
 
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
            ]
        }]
    }
 
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    )
    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
 
    raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)
 
 
def get_extra_info(name: str) -> dict:
    """Use Gemini to get shelf life, health benefits and best season."""
    prompt = f"""You are a nutrition and produce expert.
For the fruit/vegetable "{name}", respond ONLY with a JSON object — no markdown, no extra text.
 
Format:
{{
  "shelf_life": "<e.g. 3-5 days at room temperature, up to 2 weeks refrigerated>",
  "storage_tip": "<one practical storage tip>",
  "health_benefits": ["<benefit 1>", "<benefit 2>", "<benefit 3>"],
  "best_season": "<e.g. Summer (June-August) in the Northern Hemisphere>"
}}
"""
 
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    )
    try:
        resp = requests.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()
        return json.loads(raw)
    except Exception as e:
        print("GEMINI EXTRA INFO ERROR:", e)
        return {"shelf_life": "N/A", "storage_tip": "N/A", "health_benefits": [], "best_season": "N/A"}
 
 
def get_nutrition(food: str) -> dict:
    """Fetch full nutrition info from Edamam Nutrition API."""
    url = (
        f"https://api.edamam.com/api/nutrition-data"
        f"?app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        f"&ingr=100g%20{requests.utils.quote(food)}"
    )
    try:
        res = requests.get(url, timeout=10).json()
        n = res["ingredients"][0]["parsed"][0]["nutrients"]
 
        def val(key, decimals=1):
            try:
                return round(n[key]["quantity"], decimals)
            except Exception:
                return "N/A"
 
        return {
            "calories": val("ENERC_KCAL", 0),
            "protein":  val("PROCNT"),
            "carbs":    val("CHOCDF"),
            "fat":      val("FAT"),
            "fiber":    val("FIBTG"),
            "sugar":    val("SUGAR"),
            "vitA":     val("VITA_RAE"),
            "vitC":     val("VITC"),
            "vitK":     val("VITK1"),
        }
    except Exception as e:
        print("EDAMAM PARSE ERROR:", e)
        return {k: "N/A" for k in ["calories","protein","carbs","fat","fiber","sugar","vitA","vitC","vitK"]}
 
 
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400
 
    image_bytes = request.files["image"].read()
    if not image_bytes:
        return jsonify({"error": "Empty image file."}), 400
 
    try:
        result = identify_fruit(image_bytes)
    except Exception as e:
        return jsonify({"error": f"Vision API error: {str(e)}"}), 500
 
    name       = result.get("name", "unknown").lower()
    freshness  = result.get("freshness", "Unknown")
    confidence = result.get("confidence", "Low")
 
    if name == "unknown":
        return jsonify({"error": "No fruit or vegetable detected in the image."}), 422
 
    nutrition = get_nutrition(name)
    extra     = get_extra_info(name)
 
    return jsonify({
        "name":            name.title(),
        "freshness":       freshness,
        "confidence":      confidence,
        "calories":        nutrition["calories"],
        "protein":         nutrition["protein"],
        "carbs":           nutrition["carbs"],
        "fat":             nutrition["fat"],
        "fiber":           nutrition["fiber"],
        "sugar":           nutrition["sugar"],
        "vitA":            nutrition["vitA"],
        "vitC":            nutrition["vitC"],
        "vitK":            nutrition["vitK"],
        "shelf_life":      extra.get("shelf_life", "N/A"),
        "storage_tip":     extra.get("storage_tip", "N/A"),
        "health_benefits": extra.get("health_benefits", []),
        "best_season":     extra.get("best_season", "N/A"),
    })
 
 
if __name__ == "__main__":
    app.run(debug=True)
 