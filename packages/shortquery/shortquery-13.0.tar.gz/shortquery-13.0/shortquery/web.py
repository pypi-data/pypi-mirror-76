import pyshorteners
import requests
import webbrowser
import json
from google_images_download import google_images_download 

s = pyshorteners.Shortener()

def shorten(url):
    if "https://" or "http://" or "file:///" or "ftp://" in url:
        mini_url = s.tinyurl.short(url)
        return mini_url
    else:
        raise Exception("The URL is invalid. It should start with https://, ftp://, http:// or file:///")

def downloader(keyword, imgnum):
    response = google_images_download.googleimagesdownload() 
    arguments = {"keywords":str(keyword),"limit":imgnum,"print_urls":True}
    paths = response.download(arguments) 

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
