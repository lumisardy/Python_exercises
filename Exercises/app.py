import base64
from flask import Flask, request, jsonify, render_template
from google.genai import Client

app = Flask(__name__)
client = Client(api_key="AIzaSyC9siTix33xKA9qLC8Km0wVx4U9z8Px8Jk")  # Asegúrate de configurar tu API Key correctamente


def encode_image(image_file):
    """Convierte una imagen en base64"""
    return base64.b64encode(image_file.read()).decode("utf-8")


@app.route("/")
def index():
    return render_template("index.html")  # Página web principal


@app.route("/analyze", methods=["POST"])
def analyze_image():
    """Recibe una imagen desde el frontend, la convierte y envía la solicitud a Gemini"""
    if "image" not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    image_file = request.files["image"]
    image_base64 = encode_image(image_file)

    # Construcción de la solicitud a Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}},
                    {"text": "¿Qué color es el coche?"},
                    {"text": "¿Qué marca es el coche?"},
                    {"text": "¿Qué modelo es el coche?"}
                ]
            }
        ]
    )

    return jsonify({"response": response.text})


if __name__ == "__main__":
    app.run(debug=True)
