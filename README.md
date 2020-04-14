# FileScrape

FileScrape is a tool that downloads all the files on a website that has a specific extension (jpg, png etc.). 
Currently doesn't work on website that use JS to host pics or (mp3/4 extensions).

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
usage: filescrape.py [-h] [-c COOKIE] [-t THREADS] [-p PATH] url extension

This script downloads all images from a web page

positional arguments:
  url                   The URL of the web page you want to download images
  extension             The extension of the files to download (.jpg , .pdf
                        etc.)

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE, --cookie COOKIE
                        Cookie for your session ID. (If the web page requires
                        a log-in)
  -t THREADS, --threads THREADS
                        Number of threads to run. Default: 1. Higher value
                        yields faster results but might put pressure on your
                        hardware. Also when downloading multiple files using
                        higher thread count, individual downloads may slow
                        down.
  -p PATH, --path PATH  The Directory you want to store your images, default
                        is the domain of URL passed

```
### License
FileScrape is released under the Apache 2.0 license. See [LICENSE](https://github.com/adadonder/FileScrape/blob/master/LICENSE) for details.

### Contact
Feel free to contact me via e-mail: adadonderr@gmail.com
