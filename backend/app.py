import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Google Gemini API Key
genai.configure(api_key="__")  # Replace with your key

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(user_input, generation_config={
        "temperature": 0.7,  # Adjust creativity (lower = more factual, higher = more creative)
        "max_output_tokens": 300,  # Limits response length
    },
    safety_settings=[
        {"category": "HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
)


    return jsonify({"response": response.text})  # Gemini's response format

if __name__ == "__main__":
    app.run(debug=True)
