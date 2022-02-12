from pytube import YouTube
import os
import datetime
import requests
import json
from threading import Thread

def start():

    global yt

    F_FILE = input('Download from file or single video? \n1. Download from file\n2. Single video')
    if F_FILE == '1':
        multiple_video()
    elif F_FILE == '2':
        single_video()

    else:
        print('Invalid input! Try again!')


def single_video():
    URL = input('Link to video: ')
    P_DIR = input('Full path to directory to save to: ')

    t5 = Thread(target=start_download, args=(URL, P_DIR,))
    t5.join()

    N_VIDEO = input('New video? y/n')
    while N_VIDEO != 'n':
        start()

def start_download(URL, P_DIR):
    global yt
    yt = YouTube(URL)

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
        (create_folder, (PATH,)),
        (create_text, (YT_TITLE, PATH,)),
        (download_thumb, (YT_TH_URL, YT_TITLE, PATH,)),
        (download_video, (URL, PATH, YT_TITLE,))
    ]

    threads = [Thread(target=func, args=args) for func, args in pairs]

    for t in threads:
        t.start()

    for t in threads:
        t.join()   

 
def multiple_video():
    V_FILE = input('Full path to file containing URLS:')
    PATH = input('Enter directory to download to: ')

    if os.path.isfile(V_FILE):
        with open(V_FILE, 'r') as f:
            LINES = f.readlines()
            for x in LINES:
                start_download(x, PATH)
                print(x.strip())

    else:
        print('Invalid file! Try again.')
        start()


def create_folder(PATH):
    # Needs to include full path to directory for now

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
            
            print(f'Video successfully downloaded to {PATH}')
    except:
        print(f'Something went wrong while downloading')


if __name__ == '__main__':
    start()
