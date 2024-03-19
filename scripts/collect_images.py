from duckduckgo_search import DDGS
from fastdownload import download_url
from pathlib import Path
from urllib.error import URLError

import os
import time


def retrieve_image_urls(search_term: str, max_images: int = 20):
    """
    Retrieve a collection of image urls for a specified `search_term` using DuckDuckGo search.
    Returns as a python list.
    """
    return [i.get('image') for i in DDGS().images(keywords=search_term, max_results=max_images)]


def return_next_image_file_name(dir: str):
    """
    Return highest found image file in the listed directory + 1 to indicate the next file
    name to use
    """
    values = set()
    if os.path.exists(dir):
        for i in os.listdir(dir):
            try:
                values.add(int(i.replace(".jpg", "")))
            except ValueError:
                pass
    if len(values) > 0:
        return max(values) + 1
    else:
        return 0
    

def generate_directory_from_search_term(search_term: str):
    """
    Generate directory from search term along with url.txt file
    """
    # Create a text file to save downloaded URLs to
    url_dir = os.path.join("images", search_term)
    url_file = os.path.join(url_dir, "urls.txt")

    Path(url_dir).mkdir(parents=True, exist_ok=True)
    Path(url_file).touch(exist_ok=True)

    return url_dir, url_file


def download_image_files(url_dir: str, url_file: str, image_urls: list) -> int:
    """
    Download files in image_urls list and save to url_dir directory
    """
    max_image = return_next_image_file_name(url_dir)

    with open(url_file, "r") as f:
        urls_from_file = f.readlines()

    # Download each image and save to the destination path
    successes = 0
    for i, image in enumerate(image_urls):
        if image+"\n" in urls_from_file:
             pass
        else:
            try:
                download_url(image, dest=os.path.join(url_dir, str(i+max_image)+".jpg"), show_progress=False, timeout=1)
                with open(url_file, "a") as f:
                    f.writelines(image+"\n")
                urls_from_file.append(image)
                successes += 1
            except (URLError, TimeoutError):
                pass
            time.sleep(0.5)
    f.close()
    return successes, len(urls_from_file)
    

def retrieve_image_library(search_term: str, max_images: int = 20):
    """
    Download a collection of images based on a search term and save to a directory named after
    the search term.
    """
    # Get list of URLs for images
    image_urls = retrieve_image_urls(search_term=search_term, max_images=max_images)

    # Prepare directory
    url_dir, url_file = generate_directory_from_search_term(search_term=search_term)
    
    # Download files to directory
    successes, total = download_image_files(url_dir=url_dir, url_file=url_file, image_urls=image_urls)
    print(f"Complete! {successes} additional files added. {total} total images in {url_dir} directory.")


if __name__ == "__main__":
    retrieve_image_library("basalt", 50)
    retrieve_image_library("schist", 50)
