import os

# Define the path to your data directory
DATA_DIR = "/685_Data"

# List all files and directories in the specified path
for filename in os.listdir(data_dir):
    print(filename)

import os
import glob
import json
import bz2
import pandas as pd
import nltk
# Download necessary NLTK data files (only need to run once)
nltk.download('wordnet')  # Lemmatizer
nltk.download('omw-1.4')  # WordNet data
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import re

# Download necessary NLTK data files (only need to run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# List of seed terms to build the association network around
SEED_TERMS = ['COVID', 'vaccine', 'mask', 'lockdown']

# Number of top associated words to display for each seed term
TOP_N = 10

# Minimum co-occurrence threshold to include an edge in the network
MIN_COOC = 5

def load_tweet_texts(data_dir):
    all_texts = []
    # Include both .json and .json.bz2 files
    json_patterns = ['*.json', '*.json.bz2']
    json_files = []
    for pattern in json_patterns:
        json_files.extend(glob.glob(os.path.join(data_dir, pattern)))

    print(f"Found {len(json_files)} JSON files in '{data_dir}'.")

    for file in tqdm(json_files, desc="Processing JSON files"):
        try:
            # Check if file is compressed
            if file.endswith('.bz2'):
                open_func = bz2.open
                mode = 'rt'
            else:
                open_func = open
                mode = 'r'

            with open_func(file, mode, encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    try:
                        data = json.loads(line)
                        # Navigate to "output" -> "Objects"
                        output = data.get('output', {})
                        objects = output.get('Objects', [])
                        for obj in objects:
                            text = obj.get('text', '')
                            if text:
                                all_texts.append(text)
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError in file {file}, line {line_number}: {e}")
        except Exception as e:
            print(f"Unexpected error processing file {file}: {e}")

    return all_texts


# Execution
tweets = load_tweet_texts(DATA_DIR)
print(f"Total tweets loaded: {len(tweets)}")

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng') # Download the 'averaged_perceptron_tagger_eng' resource

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()


# Extend the stopwords list with additional undesired tokens
additional_stopwords = {'rt', 'amp', 'https', 'http', 'like', 'would', 'u'}
stop_words = set(stopwords.words('english')).union(additional_stopwords)

def preprocess_text(text):
    """
    Preprocesses the input text by removing URLs, converting to lowercase,
    tokenizing, removing stopwords and non-alphabetic tokens, removing verbs,
    and lemmatizing the tokens.

    Parameters:
    text (str): The tweet text to preprocess.

    Returns:
    List[str]: A list of processed tokens.
    """
    # 1. Remove URLs using regex
    text = re.sub(r'http\S+', '', text)    # Removes http:// and https:// URLs
    text = re.sub(r'www\.\S+', '', text)   # Removes www. URLs

    # 2. Convert text to lowercase
    text = text.lower()

    # 3. Tokenize the text
    tokens = word_tokenize(text)

    # 4. Remove stopwords and non-alphabetic tokens
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    # 5. Perform POS tagging
    tagged_tokens = nltk.pos_tag(tokens)

    # 6. Remove verbs (POS tags starting with 'VB')
    tokens_no_verbs = [word for word, tag in tagged_tokens if not tag.startswith('VB')]

    # 7. Lemmatize tokens
    tokens_lemmatized = [lemmatizer.lemmatize(word) for word in tokens_no_verbs]

    return tokens_lemmatized



# Apply preprocessing with progress tracking
processed_tweets = []
print("Preprocessing tweets...")
for tweet in tqdm(tweets, desc="Preprocessing"):
    tokens = preprocess_text(tweet)
    if tokens:
        processed_tweets.append(tokens)

print(f"Total processed tweets: {len(processed_tweets)}")

def build_cooccurrence_matrix(tweets, seed_terms, min_cooc=1):
    cooc_dict = defaultdict(lambda: defaultdict(int))
    seed_set = set([term.lower() for term in seed_terms])

    for tokens in tqdm(tweets, desc="Building co-occurrence matrix"):
        token_set = set(tokens)
        intersect = token_set & seed_set
        if intersect:
            for seed in intersect:
                for token in token_set:
                    if token != seed:
                        cooc_dict[seed][token] += 1
    return cooc_dict

# Execution
cooc_matrix = build_cooccurrence_matrix(processed_tweets, SEED_TERMS, MIN_COOC)

def get_top_associations(cooc_matrix, top_n):
    top_assoc = {}
    for seed, assoc_dict in cooc_matrix.items():
        sorted_assoc = sorted(assoc_dict.items(), key=lambda item: item[1], reverse=True)
        top_assoc[seed] = sorted_assoc[:top_n]
    return top_assoc

top_associations = get_top_associations(cooc_matrix, TOP_N)

# Display top associations
for seed, assoc in top_associations.items():
    print(f"\nTop associations for '{seed}':")
    for word, count in assoc:
        print(f"  {word}: {count}")

def build_network(top_assoc, min_cooc):
    G = nx.Graph()
    # Add seed nodes
    for seed in top_assoc:
        G.add_node(seed, color='red')  # Seed terms in red

    # Add associated nodes and edges
    for seed, associations in top_assoc.items():
        for word, count in associations:
            if count >= min_cooc:
                G.add_node(word, color='blue')  # Associated terms in blue
                G.add_edge(seed, word, weight=count)
    return G

# Adjust min_cooc as needed for visualization clarity
network = build_network(top_associations, MIN_COOC)

def visualize_network(G):
    plt.figure(figsize=(12, 8))

    # Get node colors
    node_colors = [data['color'] for _, data in G.nodes(data=True)]

    # Get edge weights for linewidth
    edge_weights = [data['weight'] for _, _, data in G.edges(data=True)]
    # Normalize edge widths for better visibility
    max_weight = max(edge_weights) if edge_weights else 1
    edge_widths = [ (weight / max_weight) * 5 for weight in edge_weights]

    # Layout for nodes
    pos = nx.spring_layout(G, k=0.5, seed=42)  # Positions for all nodes

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700)

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.title("Word Association Network")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Visualization
visualize_network(network)

