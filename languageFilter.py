from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

# Function to detect language
def detect_language(text):
    try:
        language = detect(text)
        return f"Detected language: {language}"
    except LangDetectException:
        return "Language could not be detected. Please provide a longer or clearer text."

# Function to process a single file
def process_file(file):
    output_dir = '../New/'
    output_path = os.path.join(output_dir, os.path.basename(file))

    # Skip if file already exists
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        return

    data = []
    with open(file) as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {file}: {e}")

    for i in range(len(data)):
        if i % 50 == 0:
            print(f"Processing line {i} in {file}")

        # Ensure the `Objects` field is not removed; filter it instead
        data[i]['output']['Objects'] = [
            obj for obj in data[i]['output']['Objects']
            if detect_language(obj['text']) == "Detected language: en"
        ]
        # Add LangSize to reflect the count of valid objects
        data[i]['output']['LangSize'] = len(data[i]['output']['Objects'])

    # Write cleaned data to output directory
    with open(output_path, 'w') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n')
    print(f"File written: {output_path}")

# Main function to handle parallel processing
def main():
    files_dir = "../Data_Json/"

    # List all files in the directory
    files = [os.path.join(files_dir, f) for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        executor.map(process_file, files)

if __name__ == "__main__":
    main()

