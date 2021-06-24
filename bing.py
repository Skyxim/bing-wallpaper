import os
import re
from threading import Thread

import requests

urlReg = re.compile(r"id=(.+?)_(.+?)_([\d]+x[\d]+)\.jpg")
host = "cn.bing.com"
folder = "./wallpapers"


class Image:
    def __init__(self, name, url, datetime, desc=""):
        self.name = name
        self.url = url
        self.datetime = datetime
        self.desc = desc

    def __str__(self):
        return f"\nname:{self.name}\nurl:{self.url}\ndatetime:{self.datetime}\ndesc:{self.desc}\n"

    def __repr__(self):
        return self.__str__()


def get_name_and_resolution(url):
    result = urlReg.findall(url)
    return result[0][0], result[0][2]


def wallpaper(num=1):
    api = f"https://{host}/HPImageArchive.aspx?format=js&idx=0&n={num}"
    # 设置copyright为中文
    headers = {
        "Cookie": "_EDGE_S=mkt=zh-cn;",
    }
    json = requests.get(api, headers=headers).json()
    images = json["images"]
    result_images = []
    for image in images:
        time = image["startdate"]
        name, resolution = get_name_and_resolution(image["url"])
        url = f"https://www.bing.com{str.replace(image['url'], resolution, 'UHD')}"
        desc = image["copyright"]
        result_images.append(Image(name, url, time, desc))
    return result_images


def download_wallpaper(images):
    if not os.path.exists(folder):
        os.makedirs(folder)
    threads = []
    for image in images:
        t = Thread(target=download, args=(f"{folder}/{image.datetime}-{image.name}.jpg", image.url))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def download(path, url):
    resp = requests.get(url)
    with open(path, "wb") as file:
        file.write(resp.content)


download_wallpaper(wallpaper(7))
