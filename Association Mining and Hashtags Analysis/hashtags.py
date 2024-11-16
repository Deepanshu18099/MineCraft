from google.colab import drive
drive.mount('/content/drive')

!pip install -U -q PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# List the first 10 files in your Drive
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list[:10]:
    print(f"title: {file['title']}, id: {file['id']}")

# Commented out IPython magic to ensure Python compatibility.
# Change directory to a specific folder in Drive
# %cd "/content/drive/My Drive/CS685 Data"

import os
import json
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

# List files in the current directory
!ls

# Path to your data directory
data_dir = "/content/drive/My Drive/CS685 Data"

# Initialize an empty list to store hashtags and timestamps
all_hashtags = []

# Function to extract hashtags from text
def extract_hashtags(text):
    return re.findall(r"#\w+", text)

# Process each file in the directory
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):  # Adjust this condition if your files have a different extension
        file_path = os.path.join(data_dir, filename)

        # Extract the full date (YYYY-MM-DD) from the file name
        try:
            # Example filename: "twitter_stream_2020_06_06_filtered.json"
            match = re.search(r'(\d{4})[-_](\d{2})[-_](\d{2})', filename)
            if match:
                date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"  # YYYY-MM-DD format
            else:
                print(f"Could not parse date from filename: {filename}")
                continue
        except AttributeError:
            print(f"Could not parse date from filename: {filename}")
            continue

        # Open and read the JSON file
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    # Load JSON data
                    data = json.loads(line)
                    # Access "Objects" array in the "output" key
                    for obj in data.get('output', {}).get('Objects', []):
                        # Extract text
                        text = obj.get('text', "")
                        # Extract hashtags if text exists
                        if text:
                            hashtags = extract_hashtags(text)
                            if hashtags:
                                all_hashtags.extend([(tag.lower(), date_str) for tag in hashtags])
                except Exception as e:
                    print(f"Error processing line in file {filename}: {e}")
                    continue

# Convert to DataFrame
hashtags_df = pd.DataFrame(all_hashtags, columns=["hashtag", "date"])

# Group by date and hashtag to count frequencies
hashtag_counts = (
    hashtags_df.groupby(['date', 'hashtag'])
    .size()
    .reset_index(name='count')
)

# Filter for specific hashtags (e.g., top 5 hashtags)
top_hashtags = (
    hashtag_counts.groupby('hashtag')['count']
    .sum()
    .nlargest(5)
    .index
)

# Filter the data for these top hashtags
top_hashtag_trends = hashtag_counts[hashtag_counts['hashtag'].isin(top_hashtags)]

# Pivot the data for plotting
trend_pivot = top_hashtag_trends.pivot(index='date', columns='hashtag', values='count').fillna(0)

# Apply rolling average for smoothing
trend_pivot_smoothed_filtered = trend_pivot.rolling(window=7, min_periods=1).mean()

# Plot trends with smoothed curves (excluding #endsars)
plt.figure(figsize=(12, 6))
trend_pivot_smoothed_filtered.plot(ax=plt.gca())
plt.title('Top Hashtag Trends by Date')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.legend(title='Hashtags')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()