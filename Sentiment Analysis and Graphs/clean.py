import re
import string
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK Data
nltk.data.path.append("./model/Lib/nltk_data")
nltk.download("stopwords")
nltk.download("punkt")

# Initialize English Stop Words
STOP_WORDS = set(stopwords.words("english"))

# 1. Function to Remove URLs
def remove_urls(text):
    return re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

# 2. Function to Remove Special Characters and Numbers
def remove_special_chars(text):
    return re.sub(r"[^a-zA-Z\s]", "", text)

# 3. Function to Remove Emojis
def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")

# 4. Function to Remove Stop Words
def remove_stop_words(text):
    tokens = word_tokenize(text)  # Tokenize text
    filtered_words = [word for word in tokens if word.lower() not in STOP_WORDS]
    return " ".join(filtered_words)

# 5. Combined Preprocessing Function
def preprocess_tweet(text):
    text = text.lower()  # Convert text to lowercase
    text = remove_urls(text)  # Remove URLs
    text = remove_emojis(text)  # Remove emojis
    text = remove_special_chars(text)  # Remove special characters and numbers
    text = remove_stop_words(text)  # Remove stop words
    return text.strip()  # Remove leading/trailing whitespace

# Example Usage
if __name__ == "__main__":
    # Sample Tweets
    sample_tweets = [
        "I'm so happy! 😊 COVID-19 cases are dropping! Visit: https://example.com",
        "Lockdowns are frustrating!! 😡 But we must follow the rules. #StayHome",
        "The vaccine rollout is amazing. Kudos to all involved!! 🥳💉 #Vaccinated",
    ]
    
    # Preprocess Each Tweet
    processed_tweets = [preprocess_tweet(tweet) for tweet in sample_tweets]
    
    # Display Results
    for i, (original, processed) in enumerate(zip(sample_tweets, processed_tweets), start=1):
        print(f"Tweet {i} (Original): {original}")
        print(f"Tweet {i} (Processed): {processed}")
        print("-" * 50)
