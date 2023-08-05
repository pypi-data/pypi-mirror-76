import pyshorteners
import requests
import webbrowser
import json
from icrawler.builtin import GoogleImageCrawler

s = pyshorteners.Shortener()

def shorten(url):
    if "https://" or "http://" or "file:///" or "ftp://" in url:
        mini_url = s.tinyurl.short(url)
        return mini_url
    else:
        raise Exception("The URL is invalid. It should start with https://, ftp://, http:// or file:///")

def downloader(keyword, imgnum):
    google_crawler = GoogleImageCrawler(storage={'root_dir': './images/'})
    google_crawler.crawl(keyword=keyword, max_num=imgnum)

def responsecode(url):
    resp = requests.get(url).status_code
    return resp

def webopen(url):
    webbrowser.open_new_tab(url)

def decodejson(jsonobj):
    obj = json.loads(jsonobj)
    return obj

def encodejson(dictobj):
    obj = json.dumps(dictobj)
    return obj
