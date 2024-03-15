import matplotlib.pyplot as plt
import datetime
import os
import random

def read_scores(filename):
    dates = []
    scores = []
    with open(filename, 'r') as f:
        for line in f:
            score, date_str = line.strip().split()
            date = datetime.datetime.strptime(date_str, "%d:%m:%Y_%H:%M:%S")
            dates.append(date)
            scores.append(float(score))
    # Sort the data by dates to ensure line plot connects points from left to right
    sorted_dates_scores = sorted(zip(dates, scores))
    return zip(*sorted_dates_scores)  # Unzip into two lists

def plot_data(vader_dir='./vader', plots_dir='./vader_plots'):
    os.makedirs(plots_dir, exist_ok=True)
    plt.figure()
    files_to_plot = ['RIGHT_fox.txt', 'LEFT_fox.txt', 'RIGHT_cnn.txt', 'LEFT_cnn.txt']
    colors = ['r', 'g', 'b', 'y']
    labels = ['Right Fox', 'Left Fox', 'Right CNN', 'Left CNN']

    for file, color, label in zip(files_to_plot, colors, labels):
        filepath = os.path.join(vader_dir, file)
        if os.path.exists(filepath):
            dates, scores = read_scores(filepath)
            plt.plot(dates, scores, color=color, label=label, marker='o', linestyle='-')  # Connect points with line

    plt.xlabel('Time')
    plt.ylabel('VADER Score')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Generate a random 5-digit number for the filename
    plot_filename = f"{random.randint(10000, 99999)}.png"
    plt.savefig(os.path.join(plots_dir, plot_filename))
    plt.close()

if __name__ == '__main__':
    plot_data()
