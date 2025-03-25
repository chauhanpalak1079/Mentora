import matplotlib.pyplot as plt
import os

def generate_sentiment_plot(sentiment_data, username):
    """
    Generates a sentiment trend plot for the last 7 days and saves it as an image.

    :param sentiment_data: Dictionary {date: score}
    :param username: Username for saving file
    :return: Path to saved image
    """
    if not sentiment_data:
        return None  # No data to visualize

    # ✅ Sort by date (ascending order)
    sorted_data = dict(sorted(sentiment_data.items(), key=lambda x: x[0]))

    # ✅ Keep only the last 7 days (in correct order)
    last_7_days_data = dict(list(sorted_data.items())[-7:])  # Get last 7 days, preserving order

    # ✅ Extracting Scores
    scores = list(last_7_days_data.values())

    # ✅ Creating X-axis Placeholder (Just for Plotting)
    x_values = range(len(scores))  # Only last 7 entries

    # ✅ Plotting
    plt.figure(figsize=(8, 4))
    plt.plot(x_values, scores, marker='o', linestyle='-', color='b', label="Sentiment Score")

    plt.xlabel("Time")  # ✅ Instead of dates, just label "Time"
    plt.xticks([])  # ✅ Removes all x-axis labels (no dates)

    plt.ylabel("Sentiment Score")
    plt.title("Mood Trends Over Last 7 Days")
    plt.ylim(0, 5)  # Assuming sentiment scores are between 0 and 5
    plt.grid(True)
    plt.legend()

    # ✅ Ensure `static/` folder exists before saving
    static_folder = "static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # ✅ Save to Static Folder
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
