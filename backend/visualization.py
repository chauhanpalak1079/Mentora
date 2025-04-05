import matplotlib.pyplot as plt
import os
import numpy as np
from database import get_latest_emotion_record


def generate_sentiment_plot(sentiment_data, username):
    if not sentiment_data:
        return None  # No data to visualize

    
    sorted_data = dict(sorted(sentiment_data.items(), key=lambda x: x[0]))
    last_7_days_data = dict(list(sorted_data.items())[-7:])  # Get last 7 days, preserving order

    # Extracting Scores
    scores = list(last_7_days_data.values())

    #  Creating X-axis Placeholder (Just for Plotting)
    x_values = range(len(scores))  # Only last 7 entries

    #  Plotting
    plt.figure(figsize=(8, 4))
    plt.plot(x_values, scores, marker='o', linestyle='-', color='b', label="Sentiment Score")

    plt.xlabel("Time")  
    plt.xticks([])  
    plt.ylabel("Sentiment Score")
    plt.title("Mood Trends Over Last 7 Days")
    plt.ylim(0, 5)  
    plt.grid(True)
    plt.legend()

    #  Ensure `static/` folder exists before saving
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    #  Save to Static Folder
    img_path = os.path.join(static_folder, f"sentiment_plot_{username}.png")
    plt.savefig(img_path, bbox_inches="tight")
    plt.close()

    return img_path  # Return path to the saved image



def generate_sentiment_pie_chart(sentiments, username):
    if not sentiments:
        return None  # No data to visualize

    sentiment_counts = {
        "Very Negative": sentiments.count("Very Negative"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral"),
        "Positive": sentiments.count("Positive"),
        "Very Positive": sentiments.count("Very Positive"),
    }

    labels = [label for label, count in sentiment_counts.items() if count > 0]
    sizes = [count for count in sentiment_counts.values() if count > 0]
    colors = ["#d73027", "#fc8d59", "#ffffbf", "#91cf60", "#1a9850"]  # Red to Green Gradient

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title("Sentiment Distribution (Last 7 Days)")

    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    img_path = os.path.join(static_folder, f"sentiment_pie_{username}.png")
    plt.savefig(img_path, bbox_inches="tight")
    plt.close()

    return img_path

def generate_emotion_radar_chart(username):
    emotion_data = get_latest_emotion_record(username)
    emotion_data_dict = dict(emotion_data)

    print("Happiness:", emotion_data_dict.get('happiness'))
    print("Neutral:", emotion_data_dict.get('neutral'))
    print("Sadness:", emotion_data_dict.get('sadness'))
    print("Anger:", emotion_data_dict.get('anger'))
    print("Surprise:", emotion_data_dict.get('surprise'))
    print("Fear:", emotion_data_dict.get('fear'))
    print("Disgust:", emotion_data_dict.get('disgust'))
    
    if not emotion_data:
        print("no data to visualize")
        return None  # No data to visualize

    # Labels for the emotions
    labels = ['Happiness', 'Neutral', 'Sadness', 'Anger', 'Surprise', 'Fear', 'Disgust']
    
    # Ensure the data has the correct length (7 emotions)
    if len(emotion_data) != len(labels):
        print("len doesnt matches")
        return None

    # Normalize the data for visualization
    max_value = max(emotion_data)
    if max_value == 0:
        max_value = 1  # Avoid division by zero
    normalized_data = [x / max_value for x in emotion_data]

    # Number of variables (emotions)
    num_vars = len(labels)

    # Compute the angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The radar chart should start from the same point, so we repeat the first data point
    normalized_data += normalized_data[:1]
    angles += angles[:1]

    # Create the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    ax.fill(angles, normalized_data, color='blue', alpha=0.25)
    ax.plot(angles, normalized_data, color='blue', linewidth=2)

    # Labels for each emotion
    ax.set_yticklabels([])  # Hide y-axis ticks
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, ha='center')

    # Add a title
    ax.set_title(f"Emotion Analysis for {username}", size=14, color='blue', weight='bold')

    # Static folder to save the chart image
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Save the radar chart as an image
    img_path = os.path.join(static_folder, f"emotion_radar_{username}.png")
    plt.savefig(img_path, bbox_inches="tight")
    plt.close()

    return img_path