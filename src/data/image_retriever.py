from duckduckgo_search import DDGS
from fastdownload import download_url
from pathlib import Path
from urllib.error import URLError

import os
import time


class ImageRetriever(object):
    def __init__(self, search_term: str, max_images: int = 20):
        self.search_term = search_term
        self.max_images = max_images

        self.url_dir = os.path.join("images", self.search_term)
        self.url_file = os.path.join(self.url_dir, "urls.txt")

    def retrieve_image_urls(self):
        """
        Retrieve a collection of image urls for a specified `search_term` using DuckDuckGo search.
        Returns as a python list.
        """
        return [i.get('image') for i in DDGS().images(keywords=self.search_term, max_results=self.max_images)]

    def return_next_image_file_name(self):
        """
        Return highest found image file in the listed directory + 1 to indicate the next file
        name to use
        """
        img_values = set()
        for i in os.listdir(self.url_dir):
            try:
                img_values.add(int(i.replace(".jpg", "")))
            except ValueError:
                pass
        if len(img_values) > 0:
            return max(img_values) + 1
        else:
            return 0
    
    def generate_directory_from_search_term(self):
        """
        Generate directory from search term along with url.txt file
        """
        # Create a text file to save downloaded URLs to
        Path(self.url_dir).mkdir(parents=True, exist_ok=True)
        Path(self.url_file).touch(exist_ok=True)
        return

    def download_image_files(self, image_urls: list) -> int:
        """
        Download files in image_urls list and save to url_dir directory
        """
        max_image = self.return_next_image_file_name()

        with open(self.url_file, "r") as f:
            urls_from_file = f.readlines()

        # Download each image and save to the destination path
        successes = 0
        for i, image in enumerate(image_urls):
            if image+"\n" in urls_from_file:
                pass
            else:
                try:
                    # Download to directory, write to url.txt file, append to urls_from_file list, note success
                    download_url(image, dest=os.path.join(self.url_dir, str(i+max_image)+".jpg"), show_progress=False, timeout=1)
                    with open(self.url_file, "a") as f:
                        f.writelines(image+"\n")
                    urls_from_file.append(image)
                    successes += 1
                # If the image is problematic, just skip it
                except (URLError, TimeoutError):
                    pass
                time.sleep(0.5)
        f.close()
        return successes, len(urls_from_file)
    
    def retrieve_image_library(self):
        """
        Download a collection of images based on a search term and save to a directory named after
        the search term.
        """
        # Get list of URLs for images
        image_urls = self.retrieve_image_urls()

        # Prepare directory
        self.generate_directory_from_search_term()
        
        # Download files to directory
        successes, total = self.download_image_files(image_urls=image_urls)
        print(f"Complete! {successes} additional files added. {total} total images in {self.url_dir} directory.")


if __name__ == "__main__":
    ImageRetriever("basalt", 50).retrieve_image_library()
    ImageRetriever("schist", 50).retrieve_image_library()
    ImageRetriever("limestone", 50).retrieve_image_library()
