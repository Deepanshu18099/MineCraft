"""
This file is to downloads twitter tweet streams from internet archive, and continuously deleting and parsing the data.
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import threading
import ScanFile
import time


# Semaphore to limit concurrent downloads
semaphore = threading.Semaphore(8)

# Directory to save downloaded files
download_dir = "/home/maverick/Downloads/courses/cs685/ProjectWorkspace/twitter_data"
os.makedirs(download_dir, exist_ok=True)
freq = 6







# open helper files

# other logs
# download log file
download_log_file = 'download_log.txt'
download_log = open(download_log_file, 'w')


# download percent log file
progress_logs_file = 'download_logs.txt'
progress_logs = open(progress_logs_file, 'a')

# Downloaded files log file
downloaded_files_file = 'downloaded_files.txt'
downloaded_files = open(downloaded_files_file, 'a')

# Processed files log file
processed_files_file = 'processed_files.txt'
processed_files = open(processed_files_file, 'a')


# getting the downloads
# download base url https://archive.org/download/archiveteam-twitter-stream-20yy-mm/
def get_download_links():
    
    base_url = "https://archive.org/download/archiveteam-twitter-stream-"
    links = []

    styr = 2020
    endyr = 2022
    stmnth = 3
    endmth = 13

    for year in range(styr, endyr):
        for month in range(year == styr and stmnth or 1, year == endyr - 1 and endmth or 13):
            comp_url = base_url + str(year) + "-" + str(month).zfill(2) + "/"
            response = requests.get(comp_url)
            soup = BeautifulSoup(response.text, "html.parser")
            # get tr td a href, its href should be zip or tar
            for link in soup.find_all('a', href = re.compile(r'\.zip$|\.tar$')):
                links.append(comp_url + link.get('href'))

    # write all links to a file
    with open("links.txt", "w") as f:
        for link in links:
            f.write(link + "\n")



def download_file(link):
    """Function to download a single file, with semaphore control."""
    with semaphore:
        file_name = link.strip().split("/")[-1]
        file_path = os.path.join(download_dir, file_name)

        # now print this in the download log file
        download_log.write(f"Downloading {file_name}...\n")
        download_log.flush()


        # if download_dir + "/" + file_name.split(".")[0] + _filtered.json exists, then skip the download and return
        if os.path.exists(download_dir + "/" + file_name.split(".")[0] + "_filtered.json"):
            download_log.write(f"{file_name} already exists, skipping download\n")
            download_log.flush()
            return

        try:
            # Track time and download speed

            # if folder is not present, means download of tar is incomplete
            if not os.path.exists(download_dir + "/" + file_name.split(".")[0]):
                start_time = time.time()
                downloaded_size = 0
                with requests.get(link.strip(), stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))

                    # continue from last state if the file is already downloaded partially
                    if os.path.exists(file_path):
                        downloaded_size = os.path.getsize(file_path)
                        response = requests.get(link.strip(), stream=True, headers={"Range": f"bytes={downloaded_size}-"})
                        response.raise_for_status()

                    chunk_size = 1024 * 1024  #  MB
                    with open(file_path, "ab") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)

                                # Calculate progress
                                percent_done = int(1000 * 100 * downloaded_size / total_size)
                                elapsed_time = time.time() - start_time
                                speed = downloaded_size / (elapsed_time + 1e-6)  # in bytes/sec

                                # Print progress every 10%
                                if percent_done % 10 == 0:
                                    progress_logs.write(f"{file_name} - {percent_done/1000}% downloaded at {speed / 1_048_576:.2f} MB/s\n")
                                    progress_logs.flush()

                downloaded_files.write(f"{file_name}\n")
                downloaded_files.flush()

                # unzip the downloaded file, delete the compress file after unzipping to save memory
                # and start processing the data by ScanFile.py functions
            
            
                # making directory with the name of the file
                os.makedirs(download_dir + '/' + file_name.split('.')[0], exist_ok=True)

            # check if file exists, if yes, then unzip it
            if os.path.exists(file_path):
                if file_name.endswith(".zip"):
                    os.system(f"unzip {file_path} -d {download_dir + '/' + file_name.split('.')[0]}")
                elif file_name.endswith(".tar"):
                    os.system(f"tar -xvf {file_path} -C {download_dir + '/' + file_name.split('.')[0]}")
                # delete the compressed file
                os.remove(file_path)

            # start processing the data
            ScanFile.get_all_files_from_directory(download_dir + "/" + file_name.split(".")[0])

            # write the processed file to the processed files log
            processed_files.write(f"{file_name}\n")
            # making the changes in the processed files visible
            processed_files.flush()

            # remove extracted folder
            os.system(f"rm -rf {download_dir}/{file_name.split('.')[0]}")

        except requests.RequestException as e:
            print(f"Error downloading {file_name}: {e}")

def download_files(text_links):
    # Read links from the file and start download threads
    with open(text_links, "r") as f:
        links = f.readlines()
    
    threads = []

    for i, link in enumerate(links):
        if i % freq != 0:
            continue
        # Start a new thread for each download
        thread = threading.Thread(target=download_file, args=(link,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    

        
# get_download_links()
download_files("links.txt")
