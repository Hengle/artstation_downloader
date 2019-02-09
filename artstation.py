import sys
import os
import re
import requests as rq
import glob

username = sys.argv[1]

page_no = 1
while True:
    url = f"https://www.artstation.com/users/{username}/projects.json?page="+str(page_no)
    resp = rq.get(url)
    if resp.status_code == 200 and resp.headers["content-type"] == "application/json; charset=utf-8":
        data = resp.json()
        if data["data"]:
            os.makedirs(username, exist_ok=True)
            for entry in data["data"]:
                thumblink = entry["cover"]["small_square_url"]
                link = re.sub(r"/20[0-9]{12}", "", thumblink)
                link = re.sub(r"small_square", "large", link)
                artid = entry["hash_id"]
                if not glob.glob(f"{username}/{artid}.*"):
                    extension = link.split(".")[-1].split("?")[0]
                    filepath = f"{username}/{artid}.{extension}"
                    img = rq.get(link)
                    if img.status_code == 200:
                        open( filepath, "wb").write(img.content)
                        print(f"Downloaded image {filepath}")
                    else:
                        print(f"Image link {link} request failed Status Code = {img.status_code}")
                else:
                    print(f"{artid} alreay exists .. Skipping")
        else:
            break;
    else:
        print("Request failed, Check username")
        break;
    page_no += 1


        
    
