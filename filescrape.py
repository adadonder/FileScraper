import sys

import requests
import argparse
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="This script downloads all images from a web page")
parser.add_argument("url", help="The URL of the web page you want to download images")
parser.add_argument("extension", help="The extension of the files to download (.jpg , .pdf etc.)")
parser.add_argument("-c", "--cookie", help="Cookie for your session ID. (If the web page requires a log-in)")
parser.add_argument("-t", "--threads", type=int,
                    help="Number of threads to run. Default: 1. Higher value yields faster results "
                         "but might put pressure on your hardware. Also when downloading multiple "
                         "files using higher thread count, individual downloads may slow down.")
parser.add_argument("-p", "--path",
                    help="The Directory you want to store your images, default is the domain of URL passed")

args = parser.parse_args()
url = args.url
extension = args.extension
path = args.path
thread_count = args.threads

if not thread_count:
    thread_count = 1

cookie = args.cookie
if cookie:
    cookie_key = cookie.split("=")[0]
    cookie_value = cookie.split("=")[1]
    cookie = dict(cookie_key=cookie_value)

# Create a session to use the cookie provided by the user
session = requests.Session()

if not path:
    # if path isn't specified, use the domain name of that url as the folder name
    path = urlparse(url).netloc


def is_valid_url(url_in):
    """
    Checks whether URL is a valid URL.
    :param url_in: url to test
    :return: Is Url valid
    """
    parsed = urlparse(url_in)
    return bool(parsed.netloc) and bool(
        parsed.scheme)  # netloc checks if domain is there, scheme checks if protocol is there


def get_all_files(url_in, extension_in):
    """
    Returns all files with the given extension on a URL.
    :param url_in: URL to get files from
    :param extension_in: Extension of the files to look for
    :return: List of URLs of files on a website
    """

    soup = bs(session.get(url=url_in, cookies=cookie).content, "html.parser")
    urls = []
    # Check if the extension is from an image
    if extension_in == ".jpg" or extension_in == ".png" or extension_in == ".jpeg":
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain a src attribute, skip
                continue
            # Make the new url by combining the url_in and the img_url
            img_url = urljoin(url_in, img_url)
            # remove URLs like /hsts-pixel.gif?c=3.2.5.
            try:  # remove everything after "?". If there is nothing it raises ValueError, handle error
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            if is_valid_url(url_in):
                urls.append(img_url)

    else:
        for file in tqdm(soup.find_all("a"), "Extracting files"):
            file_url = file.attrs.get("href")  # Check for the href tag
            if not file_url:  # If not a file_url, skip
                continue

            if not (file_url[-3:] == extension_in or file_url[-4:] == extension_in):  # Skip if the extensions don't match.
                continue

            # Make the new url by combining the original url and the file url.
            file_url = urljoin(url_in, file_url)

            # remove URLs like /hsts-pixel.gif?c=3.2.5.
            try:  # remove everything after "?". If there is nothing it raises ValueError, handle error
                pos = file_url.index("?")
                file_url = file_url[:pos]
            except ValueError:
                pass

            if is_valid_url(url_in):
                urls.append(file_url)
    if len(urls) == 0:
        num_files_found = len(soup.find_all("a"))
        sys.exit(
            f"Of the {num_files_found} files, none of them had {extension_in} as their extension. No files were downloaded.")
    return urls


def download(url_in, pathname=path):
    """
    Download images from url_in into the pathname
    :param url_in: URL of the image
    :param pathname: Where to save the image
    :return: None
    """
    # If path doesn't exist, create it
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    # Download the body of response by chunk, not immediately.
    response = session.get(url_in, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    file_name = os.path.join(pathname, url_in.split("/")[-1])

    # Visual progress bar
    progress_bar = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B",
                        unit_scale=True, unit_divisor=1024)
    with open(file_name, "wb") as f:
        for progress in progress_bar:
            f.write(progress)
            # Update the progress bar manually
            progress_bar.update(len(progress))


def main(url_in, extension_in):
    # get all files
    files = get_all_files(url_in, extension_in)
    # Use threads to speed up the download process
    with ThreadPoolExecutor(max_workers=thread_count) as tpool:
        tpool.map(download, files)
    print("Above files downloaded.")


if __name__ == '__main__':
    main(url, extension)
