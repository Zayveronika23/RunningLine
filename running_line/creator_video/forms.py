from django import forms

from creator_video.models import Video


class VideoForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Video
        fields = '__all__'
