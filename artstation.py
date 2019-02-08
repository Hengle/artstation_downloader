import sys
import os
import re
import requests as rq
from lxml import etree
import glob


def perror(msg):
    print(msg)
    sys.exit(0)


username = sys.argv[1]
url = f"https://www.artstation.com/users/{username}/projects.json?page=1"
resp = rq.get(url)

if resp.status_code == 200 and resp.headers["content-type"] == "application/json; charset=utf-8":
    data = resp.json()
    os.makedirs(username, exist_ok=True)
    for entry in data["data"]:
        permalink = entry["permalink"]
        artid = permalink.split("/")[-1]
        if not glob.glob(f"{username}/{artid}.*"):
            entry_resp = rq.get(permalink)
            if entry_resp.status_code == 200:
                doc = etree.HTML(entry_resp.text)
                imglink = doc.cssselect('head meta[property="og:image"]')[0].attrib["content"]
                extension = imglink.split(".")[-1].split("?")[0]
                filepath = f"{username}/{artid}.{extension}"
                img = rq.get(imglink)
                if img.status_code == 200:
                    open( filepath, "wb").write(img.content)
                    print(f"Downloaded image {filepath}")
                else:
                    print(f"{imglink} request failed")
            else:
                print(f"{permalink} request failed")
        else:
            print(f"{artid} alreay exists .. Skipping")
else:
    print("Request failed, Check username")


        
    