import cv2
import numpy
import transliterate
from django.http import HttpResponse
from django.shortcuts import render

from creator_video.models import Video


def create_video(message):
    width, height = 100, 100
    if message.isdigit():
        title = message
    else:
        title = transliterate.slugify('ъ'+str(message))
    out = cv2.VideoWriter(f'videos/{title}.mp4', cv2.VideoWriter_fourcc(
                            'm', 'p', '4', 'v'), 24, (width, height))
    frame = numpy.zeros((height, width, 3), dtype=numpy.uint8)
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 0
    font_color = (255, 255, 255)
    x, y = width, height // 2
    message_size = cv2.getTextSize(message, font, font_scale, font_thickness)
    for i in range(72):
        frame.fill(0)
        x -= round((100+message_size[0][0])/72)
        cv2.putText(frame, message, (x, y), font,
                    font_scale, font_color, font_thickness)
        out.write(frame)
    out.release()


def index(request):
    if 'title' in request.GET:
        return download_video(request, request.GET['title'])
    return render(request, 'index.html')


def download_video(request, message):
    if message.isdigit():
        title = message
    else:
        title = transliterate.slugify('ъ'+str(message))
    if not Video.objects.filter(title=title).exists():
        create_video(message)
        Video.objects.create(title=title, video=f'videos/{title}.mp4')
    video = Video.objects.get(title=title)
    response = HttpResponse(video.video, content_type='video/mp4')
    response['Content-Disposition'] = (
            f'attachment; filename={title}.mp4')
    return response
