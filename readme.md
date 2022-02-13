# YT-Archiver

[NOT COMPLETE]

A small CLI-based program for downloading and archiving YouTube videos.

## Features
* Supports single video downloads
* Supports bulk video downloads (from file)

## How To Use
### Single Video Download
**Single video downloads** only need a single URL, and a PATH to download the video to. The program will then create a folder named after the video title in the supplied path.

**Bulk video downloads** needs the path to a '.txt' file containing 1 or more YouTube video URLs. These URLs need to be on separate lines such as this:

> youtube.com/URLForVideo1

> youtube.com/URLForVideo2

> youtube.com/URLForVideo3

The program will then read the file, and for each of the lines in the '.txt' file it will attempt to download each video. 

The program also needs to be supplied a PATH to download to, the program will then create a folder named after the video title in the supplied path.

## Acknowledgements
Thanks to u/caveyh96 on Reddit for helping me get PyTube working with his forked repo. 
https://github.com/caevh/pytube.git

## To-Do
1. Allow for more options
    - Choose resolution
2. Create a GUI
    - Could allow for more options, what language to download CC in, FPS, download Thumbnail, create statistics file, et cetera.
3. Code-Cleanup (Of course...)
4. Support for playlist downloads
5. Download CC, in various languages
6. Create an option for updating stats file