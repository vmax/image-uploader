#!/usr/bin/env python

"""
    Purpose of the script is to upload an image file to the following services:
        * postimage.org
        * imgur.com 
        * imgsafe.org 
        * imgup.net 
        * funkyimg.com 
        * swiftpic.org 
        * imageupload.co.uk 
"""

import argh
from imgurpython import ImgurClient

IMGUR_CLIENT_ID = "ac89bea92cad345"

def imgur_uploader(filename):
    client = ImgurClient(IMGUR_CLIENT_ID, None)
    try:
        result = client.upload_from_path(filename)
        return result['link']
    except Exception as e:
        print("imgur upload failed: " + str(e))
    

def upload(filename):
    print("Uploading to imgur...")
    imgur_link = imgur_uploader(filename)
    if imgur_link:
        print(imgur_link)

if __name__ == "__main__":
    argh.dispatch_command(upload)