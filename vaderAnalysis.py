import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def process_headlines(alignment_dir, vader_dir):
    os.makedirs(vader_dir, exist_ok=True)
    sia = SentimentIntensityAnalyzer()

    for filename in os.listdir(alignment_dir):
        if filename.startswith(("LEFT_", "RIGHT_")):
            alignment, org, date = filename.split('_')[0], filename.split('_')[1], '_'.join(filename.split('_')[2:]).replace('.txt', '')
            filepath = os.path.join(alignment_dir, filename)
            with open(filepath, 'r') as file:
                headlines = file.readlines()
            file_score = sum(sia.polarity_scores(headline)['compound'] for headline in headlines)

            vader_filepath = os.path.join(vader_dir, f"{alignment}_{org}.txt")
            with open(vader_filepath, 'a') as vader_file:
                vader_file.write(f"{file_score} {date}\n")

if __name__ == "__main__":
    alignment_dir = './alignment'
    vader_dir = './vader'
    process_headlines(alignment_dir, vader_dir)
