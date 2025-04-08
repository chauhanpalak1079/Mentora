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

def generate_sleep_quality_plot(sleep_data, username):
    if not sleep_data:
        return None

    # Define order: map string to numeric score (used only for plotting)
    quality_order = {
        "didn't sleep": 0,
        "poor": 1,
        "okay": 2,
        "great": 3
    }

    # Sort by date
    sorted_data = dict(sorted(sleep_data.items(), key=lambda x: x[0]))

    dates = list(sorted_data.keys())
    sleep_scores = [quality_order.get(val.lower(), -1) for val in sorted_data.values()]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sleep_scores, marker='o', linestyle='-', color='purple', linewidth=2, markersize=8, label='Sleep Quality')

    # Set Y-axis ticks with labels
    plt.yticks(
        ticks=[0, 1, 2, 3],
        labels=["Didn't sleep", "Poor", "Okay", "Great"]
    )

    plt.xlabel("Date")
    plt.ylabel("Sleep Quality")
    plt.title("Sleep Quality Over Last 7 Days")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Ensure static folder exists
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    img_path = os.path.join(static_folder, f"sleep_quality_plot_{username}.png")
    plt.tight_layout()
    plt.savefig(img_path, bbox_inches="tight")
    plt.close()

    return img_path

from collections import Counter
def generate_mood_distribution_chart(mood_data, username):
    if not mood_data:
        return None

    # Extract only moods and count occurrences
    moods = [mood for _, mood in mood_data]
    mood_counts = Counter(moods)

    labels = list(mood_counts.keys())
    values = list(mood_counts.values())

    # Plotting
    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color='skyblue')

    # Add value labels on top
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(int(height)), ha='center', fontsize=10)

    plt.title("Mood Distribution (Last 7 Logs)")
    plt.xlabel("Mood")
    plt.ylabel("Frequency")
    plt.tight_layout()

    # Save to static folder
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    path = os.path.join(static_folder, f"mood_distribution_{username}.png")
    plt.savefig(path)
    plt.close()

    return path

import calendar
from datetime import datetime

def generate_missed_log_calendar(logged_dates, username):
    today = datetime.now()
    year = today.year
    month = today.month

    # Number of days in current month
    num_days = calendar.monthrange(year, month)[1]
    all_days = [f"{year}-{month:02d}-{day:02d}" for day in range(1, num_days + 1)]

    # Create empty heatmap grid (6 weeks x 7 days)
    heatmap = np.zeros((6, 7))
    first_weekday, _ = calendar.monthrange(year, month)

    row, col = 0, first_weekday
    for date_str in all_days:
        if date_str in logged_dates:
            value = 2  # Logged
        elif datetime.strptime(date_str, '%Y-%m-%d') < today:
            value = 1  # Missed
        else:
            value = 0  # Future/today

        heatmap[row][col] = value
        col += 1
        if col > 6:
            col = 0
            row += 1

    # Custom colormap
    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['#D5DBDB', '#F1948A', '#7FB3D5'])  # [0:gray, 1:red, 2:blue]

    fig, ax = plt.subplots(figsize=(10, 5))
    cax = ax.imshow(heatmap, cmap=custom_cmap, vmin=0, vmax=2)

    # Axis formatting
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.set_yticks(np.arange(6))
    ax.set_yticklabels([''] * 6)
    ax.set_title(f"Mood Log Heatmap - {calendar.month_name[month]} {year}")
    ax.axis('off')

    # Add day numbers to tiles
    day = 1
    row, col = 0, first_weekday
    for r in range(6):
        for c in range(7):
            if (r == row and c >= col) or r > row:
                if day <= num_days:
                    ax.text(c, r, str(day), ha='center', va='center', color='black', fontsize=10)
                    day += 1

    # Save image
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    path = os.path.join(static_folder, f"mood_log_heatmap_{username}.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    return path

def generate_coping_mech_donut_chart(mechanisms, username):

    if not mechanisms:
        return None

    counter = Counter(mechanisms)
    labels = list(counter.keys())
    values = list(counter.values())

    colors = plt.cm.Pastel1.colors[:len(labels)]

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.4)
    )

    plt.setp(autotexts, size=10, weight="bold", color="black")
    plt.title("Coping Mechanisms (Last 30 Days)")

    path = os.path.join("static", f"coping_mech_donut_{username}.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    return path
