# this will contain all the function related to scanning a json file of a hour or minute,

import json

"""
tweets_file: location of file to be scanned
keywords: keywords that used to be matched in comments
"""

def make_obj(json_obj):
    """
    return the object with key 'text', 'geo' and 'user', 'created_at', or count in the object
    """
    out = {}
    for key, value in json_obj.items():
        if isinstance(value, dict):
            tempout = make_obj(value)
            if tempout != {}:
                out[key] = tempout
        else:
            if ('count' in key) or key in ['text', 'geo', 'created_at']:
                out[key] = value
    return out
        

def filter_obj(json_obj, keywords):
    """
    return true if any of the object values with key 'text' contain any of the keywords, do pattern matching
    Checks recursively inside the object key value pairs
    """
    if isinstance(json_obj, dict):
        # do bfs instead of dfs in recur
        queue = []
        out = {}
        for key, value in json_obj.items():
            if isinstance(value, dict):
                queue.append(key)
            elif key == 'text':
                for keyword in keywords:
                    if keyword in value:
                        return make_obj(json_obj)
            elif key in ['geo', 'created_at']:
                out[key] = value
        for item in queue:
            out1 = filter_obj(json_obj[item], keywords)
            if out1 != {}:
                # ab isme created vagera vo sab bhi add hojayega
                out.update(out1)   
    if 'text' in out:
        return out
    else :
        return {}


# writing the below code as function
def filter_tweets_in_json(file_p, keywords):
    global it_i
    it_i = 0

    parsed_objects_with_match = []
    ParseCount = 0
    NotParsedCount = 0
    NotParsedFlag = False
    MatchedCount = 0
    
    try:
        for line in file_p:
            it_i = it_i + 1
            # Parse each JSON object
            json_object = json.loads(line)
            try:
                out = filter_obj(json_object, keywords)
                if  out != {}:
                    parsed_objects_with_match.append(out)
                    MatchedCount = MatchedCount + 1

            except Exception as e:
                NotParsedCount = NotParsedCount + 1
            ParseCount = ParseCount + 1
        # Now `parsed_objects` contains all JSON objects from the file
        return parsed_objects_with_match, ParseCount, NotParsedCount, NotParsedFlag, MatchedCount
    
    except Exception as e:
        print("Could not open file as json:", e)
        # print("Trying to parse the file manually")

        # try:
        #     current_object = ''
        #     brace_count = 0
        #     inside_object = False

        #     parsed_objects_with_match = []

        #     ParseCount = 0
        #     NotParsedCount = 0
        #     MatchedCount = 0
        #     # Iterate over each character to find balanced JSON objects
        #     for char in file_p.read():
        #         if char == '{':
        #             inside_object = True  # Start of a new JSON object
        #             brace_count += 1
        #             current_object += char
        #             # print("brace count: ", brace_count)
        #             # print(current_object)
        #         elif char == '}':
        #             current_object += char
        #             brace_count -= 1
        #             # print("brace count: ", brace_count)
        #             # print(current_object)

        #             # Check if we've closed an entire JSON object
        #             if inside_object and brace_count == 0:
        #                 try:
        #                     # print(current_object)
        #                     json_object = json.loads(current_object)

        #                     out = filter_obj(json_object, keywords)
        #                     if out != {}:
        #                         parsed_objects_with_match.append(out)
        #                         MatchedCount = MatchedCount + 1
        #                     # Check if the JSON object contains any of the keywords
        #                     # matching and appending part


        #                 except json.JSONDecodeError as e:
        #                     print("Could not parse JSON object:", e)
        #                     NotParsedCount = NotParsedCount + 1

        #                 ParseCount = ParseCount + 1
        #                 # Reset for the next object
        #                 current_object = ''
        #                 inside_object = False
        #         elif inside_object:
        #             # Accumulate characters inside the current JSON object
        #             current_object += char

        #     return parsed_objects_with_match, ParseCount, NotParsedCount, NotParsedFlag, MatchedCount
        
        # except Exception as e:
        # print("Could not parse the file manually too:", e)
        NotParsedFlag = True
        return parsed_objects_with_match, ParseCount, NotParsedCount, NotParsedFlag, MatchedCount


def parse_tweets_from_file(file_p, keywords):
    # reading the file which is json format without ',' seperation
    parsed_objects_with_match, ParseCount, NotParsedCount, NotParsedFlag, MatchedCount = filter_tweets_in_json(file_p, keywords)

    if not (NotParsedFlag or ParseCount - NotParsedCount == 0):
        # write in file name + _filtered + .json
        return {
                "ParseCount": ParseCount,
                "NotParsedCount" : NotParsedCount,
                "MatchSize": MatchedCount,
                "Objects": parsed_objects_with_match
                }
    else:
        return {
                "ParseCount": ParseCount,
                "NotParsedCount" : NotParsedCount,
                "MatchSize": MatchedCount,
                "Objects": []
                }
            
import os
import zipfile
import tarfile
import shutil
import gzip
import bz2
import lzma
import time

def dodfs(directory, results):
    # print("Directory: ", directory)
    # if its a zip, tar, gz, or bz2, then extract it first
    if directory.split('.')[-1] in ['zip', 'tar', 'gz', 'bz2']:
        work_dir = directory.rsplit('.', 1)[0]  # Directory to extract to
        # extract the file
        # print("Extracting file: ", directory)
        try:
            if directory.endswith('.zip'):
                with zipfile.ZipFile(directory, 'r') as zip_ref:
                    zip_ref.extractall(work_dir)
            elif directory.endswith(('.tar', '.gz', '.bz2')):
                with tarfile.open(directory, 'r:*') as tar_ref:
                    tar_ref.getmembers
                    tar_ref.extractall(work_dir)
        except Exception as e:
            # print("Could not extract the file:", e)
            # try as standalone file
            sttime = time.time()
            try:
                # buffer_size = 8 * 1024 * 1024
                if directory.endswith('.gz'):
                    with gzip.open(directory, 'rb') as f_in:
                        out = parse_tweets_from_file(f_in, keywords)
                elif directory.endswith('.bz2'):
                    with bz2.open(directory, 'rb') as f_in:
                        out = parse_tweets_from_file(f_in, keywords)
                elif directory.endswith('.xz'):
                    with lzma.open(directory, 'rb') as f_in:
                        out = parse_tweets_from_file(f_in, keywords)
                print("Time taken to extract as standalone: ", time.time() - sttime)
                # if out['Objects'] != []:
                results.append({
                    "file": directory,
                    "output": out
                })
                return results
            except Exception as e:
                print("Could not extract the file as standalone:", e)
                return results
        
        results =  dodfs(work_dir, results)
        # now delete the extra extracted files/folders
        try:
            shutil.rmtree(work_dir)
        except Exception as e:
            print("Could not delete the extracted file/folder:", e)
        return results
    

    work_dir = directory
    # if work_dir is now a json file, then parse it
    if work_dir.endswith('.json'):
        # print("Parsing file: ", work_dir)
        with open(work_dir, 'r') as file:
            out = parse_tweets_from_file(file, keywords)
            results.append({
                "file": work_dir,
                "output": out
            })

    # now if not a dir, then exit and print error
    if not os.path.isdir(work_dir):
        print("Not a directory or file: ", work_dir)
        return results

# Get all files and directories in work_dir
    files = os.listdir(work_dir)
    for file in files:
        file_path = os.path.join(work_dir, file)
        results = dodfs(file_path, results)
    return results

            
# now code that processes all the files in a directory
def get_all_files_from_directory(directory):
    # given that directory is a valid directory, not a zip
    results = []
    # now doing the dfs way
    results = dodfs(directory, results)
    

    # write each item in new file in dir + _filtered.json
    for item in results:
        with open(directory + "_filtered.json", 'a') as f:
            f.write(json.dumps(item) + '\n')

# write these to new file, tweets_file + '_filtered'

# temp_location
temp_loc = "/home/maverick/Downloads/courses/cs685/twitter_stream_2020_04_04"

# keywords
keywords = [
    "corona",
    'covid',
    "virus",
    "SARS",
    "MERS",
    "Ebola",
    "Zika",
    "H1N1",
    "H5N1",
    "H3N2",
    "Influenza",
    "Cholera",
    "Smallpox",
    "HIV/AIDS",
    "Dengue",
    "Yellow Fever",
    "Malaria",
    "Plague",
    "Marburg",
    "Lassa fever",
    "Immunity",
    "Pandemic",
    "Quarantine",
    "Lockdown",
    "Isolation",
    "Infection",
    "Social distancing",
]


# parse_tweets_from_file(temp_loc, keywords)
# get_all_files_from_directory(temp_loc)