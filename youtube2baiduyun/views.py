from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

import youtube_dl
import sys
import subprocess


# syn to baiduyun module
def syn_baiduyun(request):
    # local test
    if sys.platform == 'darwin':
        subprocess.call(
            "bypy -v syncup /Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download/ /",
            shell=True)
        # messages.success(request, 'syn down start to delete download file')

        subprocess.call(
            "rm -rf /Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download/*",
            shell=True)
        # messages.success(request, 'action down!plz check baiduyun')

    # for server
    elif sys.platform == 'linux':
        subprocess.call(
            "bypy -v syncup /home/video_crawler/download/ /", shell=True)
        # messages.success(request, 'syn down start to delete download file')

        subprocess.call("rm -rf /home/video_crawler/download/*", shell=True)
        # messages.success(request, 'action down!plz check baiduyun')


# online video downloader module
def url_dl(url, request):
    ydl_opts = {
        # Download best format available but not better that 720p
        'format': 'best[height<=720][ext=mp4]/bestvideo[height<=720][ext=mp4]+worstaudio[ext=m4a]/best',
        'merge_output_format': 'mp4',
        'outtmpl': './download/%(id)s.%(ext)s',
        'ignoreerrors': True,
        'nooverwrites': True,
        # 'simulate': 'true',
        #     # 'postprocessors': [{
        #     #    'key': 'FFmpegExtractAudio',
        #     #    'preferredcodec': 'mp3',
        #     #    'preferredquality': '192',
        #     # }],
        #     # 'logger': MyLogger(),
        #     #'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        messages.success(request, 'youtube download finished.')


@csrf_protect
def index(req):
    if req.method == 'POST':  # req == POST
        # read url list in upload file
        try:
            uploadfile = (req.FILES['urls_file'])

        except KeyError:
            messages.error(req, 'error no file upload')
            return render(req, 'index.html')

        for line in uploadfile:
            # print(url)
            url = line.decode(encoding='UTF-8')

            url_dl(url, req)

            syn_baiduyun(req)

        messages.success(req, 'finished check baidu yun.')

    return render(req, 'index.html')
