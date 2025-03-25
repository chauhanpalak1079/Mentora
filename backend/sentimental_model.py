import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

# Load pre-trained model
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

# Sentiment Labels
SENTIMENT_LABELS = {
    1: "Very Negative",
    2: "Negative",
    3: "Neutral",
    4: "Positive",
    5: "Very Positive"
}

# Keywords indicating strong negative sentiment
NEGATIVE_KEYWORDS = ["hate", "dislike", "don't like", "not good", "never", "awful", "worst", "terrible"]
# Define the threshold-based label assignment
def get_sentiment_label(average_score):
    if average_score >= 4.5:
        return "Very Positive"
    elif 3.5 <= average_score < 4.5:
        return "Positive"
    elif 2.5 <= average_score < 3.5:
        return "Neutral"
    elif 1.5 <= average_score < 2.5:
        return "Negative"
    else:
        return "Very Negative"

def bert_sentiment_analysis(texts):
    try:
        # Tokenize input text
        inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # Predict sentiment
        with torch.no_grad():
            outputs = model(**inputs)

        # Convert logits to probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)

        # Get sentiment scores
        sentiment_scores = torch.argmax(probabilities, dim=1).tolist()

        # Convert to 1-5 scale
        sentiment_scores = [score + 1 for score in sentiment_scores]

        # Average sentiment score
        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        rounded_score = round(avg_score)  # Ensure consistency in label assignment

        

        sentiment_label = get_sentiment_label(rounded_score)

        # Debugging Statements
       

        return {
            "average_sentiment_score": round(avg_score, 2),
            "sentiment_label": sentiment_label
        }

    except Exception as e:
        return {"error": str(e)}

# Testing the function
if __name__ == "__main__":
    sample_text = [
        "I love this! It's amazing.",  # Should be Positive or Very Positive
        "I hate this, it's the worst.",  # Should be Very Negative
        "It's okay, nothing special.",  # Should be Neutral
        "Not bad, could be better.",  # Should be Neutral or Positive
        "I really dislike this."  # Should be Negative
    ]

    result = bert_sentiment_analysis(sample_text)
    print(result)