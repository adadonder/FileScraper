import requests
import argparse
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

parser = argparse.ArgumentParser(description="This script downloads all images from a web page")
parser.add_argument("url", help="The URL of the web page you want to download images")
parser.add_argument("-c", "--cookie", help="Cookie for your session ID.")
parser.add_argument("-p", "--path",
                    help="The Directory you want to store your images, default is the domain of URL passed")

args = parser.parse_args()
url = args.url
path = args.path
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


def get_all_images(url_in):
    """
    Returns all images on a URL.
    :param url_in: URL to get images from
    :return: List of URLs of images on a website
    """

    soup = bs(session.get(url=url_in, cookies=cookie).content, "html.parser")
    urls = []
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

    return urls


def download(url_in, pathname):
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
    progress_bar = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_name, "wb") as f:
        for progress in progress_bar:
            f.write(progress)
            # Update the progress bar manually
            progress_bar.update(len(progress))


def main(url_in, path_in):
    # get all images
    imgs = get_all_images(url_in)
    for img in imgs:
        # download each image
        download(img, path_in)


if __name__ == '__main__':
    main(url, path)
