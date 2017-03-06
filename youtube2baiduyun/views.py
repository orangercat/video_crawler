from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

import youtube_dl
import os, sys
import bypy
import subprocess


# online video downloader module
def string_ydl(file):
    for line in file:
        # print(url)
        url = line.decode(encoding='UTF-8')
        ydl_opts = {
            # Download best format available but not better that 720p
            'format': 'best[height<=720][ext=mp4]/bestvideo[height<=720][ext=mp4]+worstaudio[ext=m4a]/best',
            'merge_output_format': 'mp4',
            'outtmpl': './download/%(title)s.%(ext)s',
            # 'simulate': 'True',
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


# syn to baiduyun module
def syn_baiduyun(request):
    # local test
    if sys.platform == 'darwin':
        subprocess.call("bypy -v syncup /Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download/ /",
                        shell=True)
        messages.success(request, 'syn down start to delete download file')

        subprocess.call("rm -rf /Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download/*", shell=True)
        messages.success(request, 'action down!plz check baiduyun')

    # for server
    elif sys.platform == 'linux':
        subprocess.call("bypy -v syncup /home/video_crawler/download/ /", shell=True)
        messages.success(request, 'syn down start to delete download file')

        subprocess.call("rm -rf /home/video_crawler/download/*", shell=True)
        messages.success(request, 'action down!plz check baiduyun')


@csrf_protect
def index(req):
    if req.method == 'POST':  # 当提交表单时
        # read url list in upload file
        try:
            uploadfile = (req.FILES['urls_file'])

        except KeyError:
            messages.error(req, 'error no file upload')
            return render(req, 'index.html')

        string_ydl(uploadfile)

        messages.success(req, 'youtube download finished.')

        messages.success(req, 'start to syn to baiduyun.')

        syn_baiduyun(req)

    return render(req, 'index.html')
