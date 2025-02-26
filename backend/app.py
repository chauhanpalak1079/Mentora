import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Google Gemini API Key
genai.configure(api_key="AIzaSyBcfVY6OI_pQdROE-CCgMb1hLgKXukWya0")  # Replace with your key

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(user_input)

    return jsonify({"response": response.text})  # Gemini's response format

if __name__ == "__main__":
    app.run(debug=True)
