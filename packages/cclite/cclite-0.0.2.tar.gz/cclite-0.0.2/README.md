# cclite - a lightweight Common Crawl API for Python3

`cclite` is a lightweight API for extracting data from Common Crawl using Python.

It supports reading Common Crawl WARC files sequentially and also querying the Common Crawl index by URL. In the latter case, the relevant parts of WARCs can be read without overhead, since `cclite` only reads the relevant parts of the WARC files.

# Installation

`pip3 install cclite`

# Usage

````
from cclite import CCParser

parser = CCParser(version='CC-MAIN-2020-16')

# get all WARCData objects
warcs = parser.get_warcs()

# get data from a single warc (lazily evaluated generator)
# calling next(data) will take a while (a few minutes) since it loads a whole WARC
data = warcs[0].data()

# only gets English pages with HTTP 200 containing UTF-8 HTML
filtered_data = warcs[0].filtered_data()

# query index for data associated with URL
# returns array of WARCData objects which can be used as above
url_data = parser.url_search('http://example.com/')
````


