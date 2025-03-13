from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import jwt  # For JWT authentication
from functools import wraps
from database import get_last_7_days_chat, get_username_by_id  # Removed get_user_password
from config import Config  # Store JWT secret in config.py
from flask import send_file
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

 

# Define Flask Blueprint
sentiment_bp = Blueprint("sentiment", __name__)

# Load Gemini API key
SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely") 
genai.configure(api_key=Config.GEMINI_API_KEY)

# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")  # Get token from headers

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])  # Fix Bearer token format
            user_id = decoded_token["user_id"]  # Changed from username to user_id
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)  # Pass user_id instead of username

    return decorated

# API Route: Analyze Sentiment for a User
@sentiment_bp.route("/analyze_sentiment", methods=["POST"])
@token_required
def analyze_sentiment(user_id):  # Now using user_id
    # Fetch chat history
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    chat_history = get_last_7_days_chat(username)
    if not chat_history:
        return jsonify({"message": "No chat history found for past 7 days"}), 404

    # Format chat history
    formatted_chat = "\n".join([f"User: {msg} | Bot: {resp}" for msg, resp, _ in chat_history])

    # Define prompt for Gemini API
    prompt = f"""
    Analyze the following 7-day chat history:
    {formatted_chat}

    The report should have three **clearly separated sections** with headings, bullet points, and proper paragraph spacing:

---

## **1. Emotional Trends**  
- Identify key emotional patterns (happiness, sadness, anxiety, neutrality, etc.).  
- Explain any mood shifts and potential triggers.  
- Provide insights into how the user emotional state evolved over the week.  

---

## **1. Summary of Mood Patterns**  
- Summarize the overall emotional trends in 3-4 sentences.  
- Mention recurring themes in conversations.  
- Highlight any noticeable emotional fluctuations.  

---

## **3. Helpful Resources & Recommendations**  
- Provide 2-3 **actionable well-being tips** based on the user's emotional trends.  
- Suggest **relevant books, podcasts, or mindfulness exercises** to help with their emotional state.  
- Keep recommendations **clear and practical.**  

---

 **Important Formatting Rules:**  
- Do **NOT** use `*`, `#`, or unnecessary symbols.  
- Keep the headings **bold and clear** (e.g., "## **Emotional Trends**").  
- Use **bullet points** for key information.  
- Ensure **proper spacing** between paragraphs.  

Return only the **formatted report**, nothing extra.
    """
    def clean_report(text):
        text = text.replace("##", "").replace("**", "")  # Remove Markdown bold & headings
        text = text.replace(" - ", "• ")  # Convert dashes to bullet points
        return text.strip()

    # Generate report using Gemini API
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    # Clean up response before sending it
    cleaned_report = clean_report(response.text)

    return jsonify({"user_id": user_id, "sentiment_report": cleaned_report})


# Function to Generate PDF with Mentora Logo
def generate_pdf(username, report_text):
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle(f"{username}'s Sentiment Report")

    # Add Logo
    logo_path = "logo.jpg"  
    pdf.drawImage(logo_path, 40, 700, width=100, height=50)

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, f"{username}'s Sentiment Analysis Report")

    # Report Content
    pdf.setFont("Helvetica", 12)
    y_position = 720
    for line in report_text.split("\n"):
        if line.strip():
            pdf.drawString(50, y_position, line.strip())
            y_position -= 20

    pdf.save()
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()

# API Route to Download Sentiment Report as PDF
@sentiment_bp.route("/download_report", methods=["GET"])
@token_required
def download_report(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    # Get Report from `sa.py`
    sentiment_response = analyze_sentiment(user_id)
    report_data = sentiment_response.get_json()

    if "sentiment_report" not in report_data:
        return jsonify({"error": "Sentiment report not available"}), 500

    report_text = report_data["sentiment_report"]

    # Generate PDF
    pdf_bytes = generate_pdf(username, report_text)

    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf", as_attachment=True, download_name=f"{username}_sentiment_report.pdf")
