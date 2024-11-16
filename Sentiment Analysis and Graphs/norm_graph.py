
# make graph of 6 sentiments with date on x axis and normalized langsize on y axis
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from datetime import datetime
import re

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
    
    
    total_counts = pos + neg + lov + sur + dis
    # Append to respective lists
    positive.append(pos/total_counts)
    negative.append(neg/total_counts) 
    love.append(lov/total_counts )
    surprise.append(sur/total_counts) 
    displeasure.append(dis/total_counts) 

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
    surprise_pct,
    love_pct,
    displeasure_pct,
    negative_pct,
    labels=[
        'Positive or Joyful Emotions',
        'Surprise or Unexpected Responses',
        'Love and Caring Emotions',
        'Displeasure or Disapproval Emotions',
        'Negative or Fearful Emotions'
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
