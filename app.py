from flask import Flask, render_template, request, jsonify
from google import genai
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        prompt = request.json.get("prompt", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = client.models.generate_content(
            model="models/gemini-2.5-flash-image",  # image generation capable
            contents=prompt
        )

        # Save or return the image as base64 (depends on response type)
        if hasattr(response, "image") and response.image:
            image_bytes = response.image  # binary data
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            return jsonify({"image": base64_image})
        else:
            return jsonify({"error": "No image generated"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
