#!/usr/binenv python3
from pytube import YouTube
import os
import datetime
import requests
import time
import json

def create_folder(YT_TITLE, YT_TH_URL):
    P_DIR = '/Users/johannesfalnes/PycharmProjects/YT-Archiver/Downloads'
    STR_TITLE = YT_TITLE
    PATH = os.path.join(P_DIR, STR_TITLE)
    os.mkdir(PATH)
    print(PATH)
    create_text(YT_TITLE=YT_TITLE, PATH=PATH)
    time.sleep(0.5)
    download_thumb(YT_TH_URL=YT_TH_URL, YT_TITLE=YT_TITLE, PATH=PATH)
    download_video(YT_TITLE, PATH)



def create_text(YT_TITLE, PATH):
    time_downloaded = datetime.datetime.now()
    file_entries = [YT_TITLE, time_downloaded]
    N_TITLE = YT_TITLE + '.txt'
    my_file = (PATH + '/' + N_TITLE)
    write_to_file = {'Title': YT_TITLE,
                     'Channel URL': yt.channel_url,
                     'Video Views': yt.views,
                     'Video Desc': yt.description,
                     'Length': yt.length,
                     'Publication Date': yt.publish_date,
                     'Rating': yt.rating,
                     'Time Downloaded': str(time_downloaded)
                     }
    with open(os.path.join(PATH, my_file), 'w') as f:
        f.write(json.dumps(write_to_file, indent=4, sort_keys=False, default=str))


def download_thumb(YT_TH_URL, YT_TITLE, PATH):
    response = requests.get(YT_TH_URL)
    print(PATH)
    with open(os.path.join(PATH, (YT_TITLE + '.jpg')), 'wb') as f:
        f.write(response.content)
        f.close()


def download_video(YT_LINK, PATH):
    yt = YouTube(YT_LINK)
    yt = yt.get('mp4', '720p')
    yt.download(PATH)
    

dl_path = 'Downloads'
YT_LINK = 'https://www.youtube.com/watch?v=OvKNTaySrsE/'
yt = YouTube(YT_LINK)

YT_TITLE = yt.title

# Get the YouTube Thumbnail URL
YT_TH_URL = yt.thumbnail_url
create_folder(YT_TITLE=YT_TITLE, YT_TH_URL=YT_TH_URL)
