from pytube import YouTube
import os
import datetime
import requests
import json
from threading import Thread

def start():

    global yt

    F_FILE = input('Download from file or single video? \n1. Download from file \n2. Single video \n')
    if F_FILE == '1':
        multiple_video()
    elif F_FILE == '2':
        single_video()

    else:
        print('Invalid input! Try again!')


def single_video():
    URL = input('Link to video: ')
    P_DIR = input('Full path to directory to save to: ')

    start_download(URL, P_DIR)
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


    PAIRS = [
        (create_folder, (PATH,)),
        (create_text, (YT_TITLE, PATH,)),
        (download_thumb, (YT_TH_URL, YT_TITLE, PATH,)),
        (download_video, (URL, PATH, YT_TITLE,))
    ]

    THREADS = [Thread(target=func, args=args) for func, args in PAIRS]

    for T in THREADS:
        T.start()

    for T in THREADS:
        T.join()   

 
def multiple_video():
    """Function for downloading multiple files
    Scans the supplied file for YT URLs."""
    V_FILE = input('Full path to file containing URLS:')
    PATH = input('Enter directory to download to: ')

    if os.path.isfile(V_FILE):
        with open(V_FILE, 'r') as f:
            LINES = f.readlines()
            for URL in LINES:
                start_download(URL, PATH)
                print(URL.strip())

    else:
        print('Invalid file! Try again.')
        start()


def create_folder(PATH):
    """Creates a folder using the PATH variable.
    If folder exists it will skip creation, and tell user that PATH already exists."""
    if os.path.isdir(PATH):
        print(f'Folder already exists in path {PATH}. Bypassing.')
    else:
        print(f'Creating folder in {PATH}')
        os.mkdir(PATH)



def create_text(YT_TITLE, PATH):
    """Creates the statistics text. 
    Uses the yt object, YT_TITLE and PATH variables to create the file."""
    
    N_TITLE = YT_TITLE + '.txt'

    STAT_FILE = (PATH + '/' + N_TITLE)
    FILE_PATH = os.path.join(PATH, STAT_FILE)

    if os.path.isfile(FILE_PATH):
        print(f'File already exists in path {FILE_PATH}, bypassing...')
    else:
        print(f'Creating stats file in {FILE_PATH}')

        TIME_DOWNLOADED = datetime.datetime.now()

        WRITE_TO_FILE = {
                        'Title': yt.title,
                        'Channel URL': yt.channel_url,
                        'Video Views': yt.views,
                        'Video Desc': yt.description,
                        'Video ID': yt.video_id,
                        'Length': yt.length,
                        'Publication Date': yt.publish_date,
                        'Rating': yt.rating,
                        'Time Downloaded': TIME_DOWNLOADED,
                        'Age restricted': yt.age_restricted,
                        'Author': yt.author
                        }

        with open(FILE_PATH, 'w') as f:
            f.write(json.dumps(WRITE_TO_FILE, indent=4, sort_keys=False, default=str))
            f.close()



def download_thumb(YT_TH_URL, YT_TITLE, PATH):
    """Download the Thumbnail for the selected video, 
    and saves it to PATH using the YT_TITLE var as name"""

    R_THUMB = requests.get(YT_TH_URL)

    THUMB_PATH = os.path.join(PATH, (YT_TITLE + '.jpg'))
    if os.path.isfile(THUMB_PATH):
        print(f'Thumbnail already exists in path: {THUMB_PATH}. Bypassing')
    else:
        print(f'Downloading thumbnail to {THUMB_PATH}')
        with open(THUMB_PATH, 'wb') as f:
            f.write(R_THUMB.content)
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
            VIDEO = yt.streams.get_highest_resolution()
            VIDEO.download(PATH)

            print(f'Video successfully downloaded to {PATH}')
    except:
        print(f'Something went wrong while downloading')


if __name__ == '__main__':
    start()
