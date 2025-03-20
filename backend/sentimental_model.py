import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load pre-trained model and tokenizer
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

# Ensure model is in evaluation mode
model.eval()

# Sentiment Labels
SENTIMENT_LABELS = {
    0: "Very Negative 😞",
    1: "Negative 🙁",
    2: "Neutral 😐",
    3: "Positive 🙂",
    4: "Very Positive 😃"
}

def bert_sentiment_analysis(text):
    
    try:
        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # Predict sentiment
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get sentiment score (highest probability class)
        sentiment_score = torch.argmax(outputs.logits).item()
        sentiment_label = SENTIMENT_LABELS.get(sentiment_score, "Unknown Sentiment")

        return {
            "text": text,
            "sentiment_score": sentiment_score + 1,  # Convert to 1-5 scale
            "sentiment_label": sentiment_label
        }
    except Exception as e:
        return {"error": str(e)}

# Testing the function
if __name__ == "__main__":
    sample_text = "I love using Mentora! It's really helpful."
    result = bert_sentiment_analysis(sample_text)
    print(result)
