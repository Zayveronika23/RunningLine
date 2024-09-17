import cv2
import numpy
import transliterate
from django.http import HttpResponse
from django.shortcuts import render

from creator_video.models import Video


def create_video(message):
    width, height = 1920, 1080
    title = transliterate.slugify('ъ'+message)
    out = cv2.VideoWriter(f'videos/{title}.mp4', cv2.VideoWriter_fourcc(
                            'm', 'p', '4', 'v'), 24, (width, height))
    frame = numpy.zeros((height, width, 3), dtype=numpy.uint8)
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 10
    font_thickness = 10
    font_color = (255, 255, 255)
    x, y = width, height // 2
    for i in range(72):
        frame.fill(0)
        x -= 6*len(message)
        cv2.putText(frame, message, (x, y), font,
                    font_scale, font_color, font_thickness)
        out.write(frame)
    out.release()


def index(request):
    if 'title' in request.GET:
        return download_video(request, request.GET['title'])
    return render(request, 'index.html')


def download_video(request, message):
    title = transliterate.slugify('ъ'+message)
    if not Video.objects.filter(title=title).exists():
        create_video(message)
        Video.objects.create(title=title, video=f'videos/{title}.mp4')
    video = Video.objects.get(title=title)
    response = HttpResponse(video.video, content_type='video/mp4')
    response['Content-Disposition'] = (
            f'attachment; filename={title}.mp4')
    return response
