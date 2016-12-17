#!/usr/bin/env python

"""
    Purpose of the script is to upload an image file to the following services:
        * postimage.org DONE
        * imgur.com DONE
        * imgsafe.org DONE
        * imgup.net DONE
        * funkyimg.com 
        * swiftpic.org 
        * imageupload.co.uk 
"""

import argh
from imgurpython import ImgurClient
import requests
from bs4 import BeautifulSoup

IMGUR_CLIENT_ID = "ac89bea92cad345"

def imgur_uploader(filename):
    client = ImgurClient(IMGUR_CLIENT_ID, None)
    try:
        result = client.upload_from_path(filename)
        return result['link']
    except Exception as e:
        print("imgur upload failed: " + str(e))


def postimage_uploader(filename):
    from datetime import datetime

    POSTIMAGE_URL = 'http://old.postimage.org'

    data = {
        'session_upload': str(int(datetime.now().timestamp()*1000))
    }

    files = {
        'upload': (filename, open(filename, 'rb'), 'image/*')
    }

    with requests.session() as session:
        r0 = session.get(POSTIMAGE_URL)
        r1 = session.post(POSTIMAGE_URL, files = files, data = data)
        gallery_id = r1.text
        r2 = session.get(POSTIMAGE_URL + "/gallery/" + gallery_id)
        soup = BeautifulSoup(r2.text, "html.parser")
        return soup.select('img')[0].get('src')

def imgsafe_uploader(filename):
    IMGSAFE_URL = 'http://imgsafe.org/upload'

    files = {
        'files[]': (filename, open(filename, 'rb'), 'image/*')
    }

    resp = requests.post(IMGSAFE_URL, files=files)
    return 'http:' + resp.json()['files'][0]['url']

def imgup_uploader(filename):
    IMGUP_URL = 'http://imgup.net/upload'

    data = {
        '_method': 'put'
    }

    files = {
        'image[image][]': (filename, open(filename, 'rb'), 'image/*')
    }

    resp = requests.post(IMGUP_URL, files = files, data = data)
    url = resp.json()['img_link'].replace('i.imgup', '.imgup')
    return url

def upload(filename):
    """"
    print("Uploading to imgur...")
    imgur_link = imgur_uploader(filename)
    if imgur_link:
        print(imgur_link)
    
    
    print("Uploading to postimage...")
    postimage_link = postimage_uploader(filename)
    
    if postimage_link:
        print(postimage_link)
    
    print("Uploading to imgsafe...")
    imgsafe_link = imgsafe_uploader(filename)
    if imgsafe_link:
        print(imgsafe_link)
    """

    print("Uploading to imgup...")
    imgup_link = imgup_uploader(filename)
    if imgup_link:
        print(imgup_link)
    


if __name__ == "__main__":
    argh.dispatch_command(upload)

