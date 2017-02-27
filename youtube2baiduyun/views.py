from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

import youtube_dl
import os, sys
import bypy


# Create your views here.

@csrf_protect
def index(req):
    if req.method == 'POST':  # 当提交表单时
        # read comment in textarea

        try:
            uploadfile = (req.FILES['urls_file'])

        except KeyError:
            messages.error(req, 'error no file upload')
            return render(req, 'index.html')

        for line in uploadfile:
            url = line.decode(encoding='UTF-8')
            # line = line.strip('\n')

            # print(line)

            # with open(urls_file, 'rt') as file:
            #
            #     print(file)
            ydl_opts = {
                ##Download best format available but not better that 480p
                'format': 'bestvideo[height<=720]+worstaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
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

        messages.success(req, 'start to syn to baiduyun.')

        by = bypy.ByPy()

        # local test
        if sys.platform == 'darwin' == 'darwin':
            a = by.syncup('/Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download', '/')
            messages.success(req, 'syn down start to delete download file')

            os.system('rm -rf /Users/chaochen/Dropbox/project/env_Django_Demo/video_crawler/download/*')
            messages.success(req, 'action down!plz check baiduyun')

            return render(req, 'index.html')

        # for server
        elif sys.platform == 'linux':

            a = by.syncup('/home/youtube_crawler/download', '/')
            messages.success(req, 'syn down start to delete download file')

            os.system('rm -rf /home/youtube_crawler/download/*')
            messages.success(req, 'action down!plz check baiduyun')

        return render(req, 'index.html')

    return render(req, 'index.html')
