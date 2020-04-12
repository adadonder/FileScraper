# PhotoScraper

PhotoScraper is a tool that downloads all the images on a website. Currently doesn't work on website that use JS to host pics.

### Installation
````
$ python3 setup.py install
````
or
````
$ pip install .
````

### Usage
Be sure to run with ``python3``.
```
usage: pscraper.py [-h] [-c COOKIE] [-p PATH] url

This script downloads all images from a web page

positional arguments:
  url                   The URL of the web page you want to download images

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE, --cookie COOKIE
                        Cookie for your session ID.
  -p PATH, --path PATH  The Directory you want to store your images, default
                        is the domain of URL passed

```
### License
PhotoScraper is released under the Apache 2.0 license. See [LICENSE](https://github.com/adadonder/PhotoScraper/blob/master/LICENSE) for details.

###Contact
Feel free to contact me via e-mail: adadonderr@gmail.com
