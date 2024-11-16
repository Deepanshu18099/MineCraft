import matplotlib.pyplot as plt
import os
import re
import json
import numpy as np
import pandas as pd


# Format:
#   {
    # "twitter_stream_2021_04_30_filtered.json": {
#     "Positive or Joyful Emotions": 505,
#     "Negative or Fearful Emotions": 554,
#     "Neutral or Objective Emotions": 3367,
#     "Love and Caring Emotions": 288,
#     "Surprise or Unexpected Responses": 232,
#     "Displeasure or Disapproval Emotions": 546,
#     "ParseCount": 5896795,
#     "MatchSize": 10986,
#     "LangSize": 5965
#   },
#   "twitter_stream_2021_05_01_filtered.json": {
#     "Positive or Joyful Emotions": 505,
#     "Negative or Fearful Emotions": 554,
#     "Neutral or Objective Emotions": 3367,
#     "Love and Caring Emotions": 288,
#     "Surprise or Unexpected Responses": 232,
#     "Displeasure or Disapproval Emotions": 546,
#     "ParseCount": 5896795,
#     "MatchSize": 10986,
#     "LangSize": 5965
#   }




# for key, value in sentiment_data.items():

# make graph of 6 sentiments with date on x axis and normalized langsize on y axis
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Load the JSON file
sentiment_file = 'sentiments.json'
with open(sentiment_file) as f:
    sentiment_data = json.load(f)

# Initialize lists for extracted dates and sentiment categories
dates = []
positive = []
negative = []
love = []
surprise = []
displeasure = []

# Extract data from the JSON file
for file_name, values in sentiment_data.items():
    # Extract date from the file name
    date_match = re.search(r'\d{4}_\d{2}_\d{2}', file_name)
    if date_match:
        date_str = date_match.group(0).replace('_', '-')
        dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
    
    # Absolute values
    neg = values.get("Negative or Fearful Emotions", 0)
    dis = values.get("Displeasure or Disapproval Emotions", 0)
    sur = values.get("Surprise or Unexpected Responses", 0)
    lov = values.get("Love and Caring Emotions", 0)
    pos = values.get("Positive or Joyful Emotions", 0)
    
    parse_count = values.get("ParseCount", 1)
    
    

    # Append to respective lists
    positive.append(pos/parse_count * 100 )
    negative.append(neg/parse_count * 100 )
    love.append(lov/parse_count * 100 )
    surprise.append(sur/parse_count * 100 )
    displeasure.append(dis/parse_count * 100 )

# Convert lists to numpy arrays for easier manipulation
positive = np.array(positive)
negative = np.array(negative)
love = np.array(love)
surprise = np.array(surprise)
displeasure = np.array(displeasure)

# Calculate total sentiment counts for each file
# total_counts = positive + negative + love + surprise + displeasure

# Normalize each sentiment count to a percentage of the total
positive_pct = (positive) 
negative_pct = (negative ) 
love_pct = (love )
surprise_pct = (surprise )
displeasure_pct = (displeasure )

# Create the stacked area chart
plt.figure(figsize=(14, 8))
plt.stackplot(
    dates,
    positive_pct,
    negative_pct,
    love_pct,
    surprise_pct,
    displeasure_pct,
    labels=[
        'Positive or Joyful Emotions',
        'Negative or Fearful Emotions',
        'Love and Caring Emotions',
        'Surprise or Unexpected Responses',
        'Displeasure or Disapproval Emotions'
    ],
    colors=['#1f77b4', '#d62728', '#ff7f0e', '#9467bd', '#8c564b']
)

# Adding labels and legend
plt.xlabel('Date (Months Granularity)')
plt.ylabel('Percentage (%)')
plt.title('Stacked Area Chart of Sentiment Proportions Over Time')
plt.xticks(rotation=45, ha='right')
plt.legend(loc='upper left')
plt.grid()
plt.tight_layout()

# Display the plot
plt.show()
