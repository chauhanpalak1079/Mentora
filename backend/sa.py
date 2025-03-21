from flask import Blueprint, request, jsonify, send_file
import google.generativeai as genai
import os
import jwt
from functools import wraps
from database import get_last_7_days_chat, get_username_by_id
from config import Config
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sentimental_model import bert_sentiment_analysis  # Corrected function name

# Define Flask Blueprint
sentiment_bp = Blueprint("sentiment", __name__)

# Load Gemini API key
SECRET_KEY = os.getenv("SECRET_KEY", "fucking_do_it_pr0prely") 
genai.configure(api_key=Config.GEMINI_API_KEY)

# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated

# API Route: Analyze Sentiment for a User
@sentiment_bp.route("/analyze_sentiment", methods=["POST"])
@token_required
def analyze_sentiment(user_id):  # Function name is back to normal
    # Fetch chat history
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    chat_history = get_last_7_days_chat(username)
    if not chat_history:
        return jsonify({"message": "No chat history found for past 7 days"}), 404

    # Format chat history
    formatted_chat = "\n".join([f"User: {msg} | Bot: {resp}" for msg, resp, _ in chat_history])

    # **1. BERT Sentiment Analysis**
    bert_sentiment = bert_sentiment_analysis([msg for msg, _, _ in chat_history])  # Function name corrected
    print (bert_sentiment)
    # **2. Gemini API Report Generation**
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

## **2. Summary of Mood Patterns**  
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
        text = text.replace("##", "").replace("**", "")
        text = text.replace(" - ", "• ")
        return text.strip()

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    cleaned_report = clean_report(response.text)
    print(cleaned_report)


    response_data = {
    "user_id": user_id,
    "bert_sentiment": bert_sentiment,
    "gemini_report": cleaned_report
}

    print("Final Response Sent:", response_data)  # Debugging

    return jsonify(response_data), 200


# API Route: Generate PDF Report
@sentiment_bp.route("/download_report", methods=["GET"])
@token_required
def download_report(user_id):
    username = get_username_by_id(user_id)
    if not username:
        return jsonify({"error": "User not found"}), 404

    chat_history = get_last_7_days_chat(username)
    if not chat_history:
        return jsonify({"message": "No chat history found for past 7 days"}), 404

    formatted_chat = "\n".join([f"User: {msg} | Bot: {resp}" for msg, resp, _ in chat_history])
    
    # BERT Sentiment Analysis
    bert_sentiment = bert_sentiment_analysis([msg for msg, _, _ in chat_history])  # Function name corrected

    # Gemini AI Report Generation
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"""
    Analyze the following 7-day chat history:
    {formatted_chat}

    The report should have three **clearly separated sections** with headings, bullet points, and proper paragraph spacing.

    ## **1. Emotional Trends**  
- Identify key emotional patterns (happiness, sadness, anxiety, neutrality, etc.).  
- Explain any mood shifts and potential triggers.  
- Provide insights into how the user emotional state evolved over the week.  

---

## **2. Summary of Mood Patterns**  
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
    """)
    gemini_report = response.text.replace("##", "").replace("**", "").replace(" - ", "• ").strip()

    # Create PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    y_position = 750

    def add_text(text, y_offset):
        nonlocal y_position
        lines = text.split("\n")
        for line in lines:
            pdf.drawString(50, y_position, line)
            y_position -= y_offset

    pdf.drawString(50, 780, f"Sentiment Analysis Report for {username}")
    pdf.line(50, 775, 550, 775)

    add_text("BERT Sentiment Analysis:", 15)
    add_text(f"Detected Moods: {', '.join(bert_sentiment)}", 15)
    add_text("", 15)

    add_text("Gemini AI Report:", 15)
    add_text(gemini_report, 15)

    pdf.showPage()
    pdf.save()
    
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name="Sentiment_Report.pdf", mimetype="application/pdf")
