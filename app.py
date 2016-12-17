#!/usr/bin/env python

"""
    Purpose of the script is to upload an image file to the following services:
        * postimage.org DONE
        * imgur.com DONE
        * imgsafe.org DONE
        * imgup.net DONE
        * funkyimg.com DONE
        * swiftpic.org DONE
        * imageupload.co.uk DONE
"""

import argh
from imgurpython import ImgurClient
import requests
from bs4 import BeautifulSoup
import sys
import csv

csv_stdout = csv.writer(sys.stdout)

def random_alphanumeric_string(length=10):
    import random
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length)) + '.png'

def imgur_uploader(filename):
    IMGUR_URL = 'http://imgur.net'

    headers = {
        'Origin': IMGUR_URL.replace('.net', '.com'),
        'Referer': IMGUR_URL.replace('.net', '.com'),
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    files = {
         'Filedata': (random_alphanumeric_string(), open(filename, 'rb'), 'image/png')
    }

    with requests.session() as session:
        r0 = session.get(IMGUR_URL, headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
        r1 = session.post(IMGUR_URL.replace('.net', '.com') + '/upload/checkcaptcha', data = {'create_album': 'true', 'total_uploads': 1}, headers=headers)
        album_id = r1.json()['data']['new_album_id']

        data = {
            'new_album_id' : album_id
        }

        r2 = session.post(IMGUR_URL.replace('.net', '.com') + '/upload', files = files, data = data, headers = headers)
        return 'http://i.imgur.com/' + r2.json()['data']['hash'] + '.png'



def postimage_uploader(filename):
    from datetime import datetime

    POSTIMAGE_URL = 'http://old.postimage.org'

    data = {
        'session_upload': str(int(datetime.now().timestamp()*1000))
    }

    files = {
        'upload': (random_alphanumeric_string(), open(filename, 'rb'), 'image/*')
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
        'files[]': (random_alphanumeric_string(), open(filename, 'rb'), 'image/*')
    }

    resp = requests.post(IMGSAFE_URL, files=files)
    return 'http:' + resp.json()['files'][0]['url']

def imgup_uploader(filename):
    IMGUP_URL = 'http://imgup.net/upload'

    data = {
        '_method': 'put'
    }

    files = {
        'image[image][]': (random_alphanumeric_string(), open(filename, 'rb'), 'image/*')
    }

    resp = requests.post(IMGUP_URL, files = files, data = data)
    url = resp.json()['img_link'].replace('i.imgup', '.imgup')
    return url

def funkyimg_uploader(filename):
    import time
    FUNKYIMG_URL = 'http://funkyimg.com/upload/'

    files = {
         'images': (random_alphanumeric_string(), open(filename, 'rb'), 'image/*')
    }

    r0 = requests.post(FUNKYIMG_URL, files=files)
    jid = r0.json()['jid']
    time.sleep(3) # give the service time to process the image
    r1 = requests.get(FUNKYIMG_URL + '/check/' + jid)
    soup = BeautifulSoup(r1.json()['bit'], 'html.parser')
    inputs = soup.select('input')
    for input in inputs:
        if input.get('value').startswith('http://funkyimg.com/i/'):
            return input.get('value')


def swiftpic_uploader(filename):
    SWIFTPIC_URL = 'http://www.swiftpic.org/ajax-upload'
    
    # SwiftPic doesn't really care about MIME-type being correct; it doesn't accept empty one or wildcard
    files = {
         'up_file[]': (random_alphanumeric_string(), open(filename, 'rb'), 'image/png')
    }

    data = {
        'terms': 'yes'
    }

    resp = requests.post(SWIFTPIC_URL, files = files, data = data)
    url = resp.json()['redirect_to']
    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup.select('input')[1].get('value')


def imageuploadcouk_uploader(filename):
    from datetime import datetime
    IMAGEUPLOADCOUK_URL = 'http://imageupload.co.uk'
    
    files = {
         'source': (random_alphanumeric_string(), open(filename, 'rb'), 'image/png')
    }

    data = {
        'action': 'upload',
        'category_id': 'null',
        'privacy': 'public',
        'nsfw': '0',
        'timestamp': str(int(datetime.now().timestamp()*1000)),
        'type': 'file',
    }

    with requests.session() as session:
        resp = session.get(IMAGEUPLOADCOUK_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        data['auth_token'] = soup.find(attrs={'name': 'auth_token'}).get('value')

        resp = session.post(IMAGEUPLOADCOUK_URL + '/json', files = files, data = data)
        return resp.json()['image']['image']['url']


uploaders = {
    'imgur.com' : imgur_uploader,
    'postimage.org' : postimage_uploader,
    'imgsafe.org' : imgsafe_uploader,
    'imgup.net' : imgup_uploader,
    'funkyimg.com' : funkyimg_uploader,
    'swiftpic.org' : swiftpic_uploader,
    'imageupload.co.uk' : imageuploadcouk_uploader
}


def upload(filename):
    csv_stdout.writerow(['Filename', 'Service', 'Link'])
    for service in uploaders:
        uploader = uploaders[service]
        link = uploader(filename)
        csv_stdout.writerow([filename, service, link])


if __name__ == "__main__":
    argh.dispatch_command(upload)

