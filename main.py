from ast import arg
from pytube import YouTube
import os
import datetime
import requests
import time
import json
from threading import Thread
import concurrent.futures

def start():

    global yt

    YT_LINK = input('Link to video: ')
    P_DIR = input('Full path to directory to save to: ')
    yt = YouTube(YT_LINK)

    YT_TITLE = yt.title
    # Going to make a solution for 'illegal' characters here
    ILLEGAL_CHAR = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for x in ILLEGAL_CHAR:
        if x in YT_TITLE:
            YT_TITLE = YT_TITLE.replace(x, '')
            
    # Get the YouTube Thumbnail URL
    YT_TH_URL = yt.thumbnail_url
    PATH = os.path.join(P_DIR, YT_TITLE)


    pairs = [
        (create_folder, (YT_TITLE, PATH,)),
        (create_text, (YT_TITLE, PATH,)),
        (download_thumb, (YT_TH_URL, YT_TITLE, PATH,)),
        (download_video, (YT_LINK, PATH, YT_TITLE,))
    ]

    threads = [Thread(target=func, args=args) for func, args in pairs]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    N_VIDEO = input('New video? y/n')
    while N_VIDEO != 'n':
        start()

def create_folder(YT_TITLE, PATH):
    # Needs to include full path to directory for now

    #P_DIR = '/Users/johannesfalnes/PycharmProjects/YT-Archiver/Downloads'

    if os.path.isdir(PATH):
        print(f'Folder already exists in path {PATH}. Bypassing.')
    else:
        print(f'Creating folder in {PATH}')
        os.mkdir(PATH)



def create_text(YT_TITLE, PATH):
    N_TITLE = YT_TITLE + '.txt'

    my_file = (PATH + '/' + N_TITLE)
    FILE_PATH = os.path.join(PATH, my_file)

    if os.path.isfile(FILE_PATH):
        print(f'File already exists in path {FILE_PATH}, bypassing...')
    else:
        print(f'Creating stats file in {FILE_PATH}')
        time_downloaded = datetime.datetime.now()
        write_to_file = {'Title': YT_TITLE,
                        'Channel URL': yt.channel_url,
                        'Video Views': yt.views,
                        'Video Desc': yt.description,
                        'Video ID': yt.video_id,
                        'Length': yt.length,
                        'Publication Date': yt.publish_date,
                        'Rating': yt.rating,
                        'Time Downloaded': time_downloaded,
                        'Age restricted': yt.age_restricted
                        }

        with open(FILE_PATH, 'w') as f:
            f.write(json.dumps(write_to_file, indent=4, sort_keys=False, default=str))



def download_thumb(YT_TH_URL, YT_TITLE, PATH):
    response = requests.get(YT_TH_URL)

    THUMB_PATH = os.path.join(PATH, (YT_TITLE + '.jpg'))
    if os.path.isfile(THUMB_PATH):
        print(f'Thumbnail already exists in path: {THUMB_PATH}. Bypassing')
    else:
        print(f'Downloading thumbnail to {THUMB_PATH}')
        with open(THUMB_PATH, 'wb') as f:
            f.write(response.content)
            f.close()



def download_video(YT_LINK, PATH, YT_TITLE):

    try:
        VIDEO_PATH = os.path.join(PATH, (YT_TITLE + '.mp4'))
        print(VIDEO_PATH)
        if os.path.isfile(VIDEO_PATH):
            print(f'Video already exists in path: {VIDEO_PATH}. Bypassing')
        else:
            print('Downloading video ', YT_LINK)

            yt = YouTube(YT_LINK)
            video = yt.streams.get_highest_resolution()
            video.download(PATH)
    except:
        print(f'Something went wrong while downloading')


if __name__ == '__main__':
    start()
