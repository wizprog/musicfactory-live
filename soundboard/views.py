from django import http
from django.conf import settings
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from soundboard.models import Track
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.utils.encoding import smart_str

from django.http import HttpResponse

from .forms import CreateTrackForm

import os
import socket
from pydub import AudioSegment, silence
from rest_framework import status

from pathlib import Path
import os

# Create your views here.


@cache_page(60 * 1)
def calculate_start_time(request, track_id):
    response_data = 0.0
    if request.method == 'GET' or request.method == 'POST':
        track_data = Track.objects.get(pk=track_id)
        track_location, track_extension= os.path.splitext(track_data.file.path)
        track_name = track_location + track_extension
        try:
            track_audio = AudioSegment.from_file(track_name, format=track_extension[1:])
            response_data = silence.detect_leading_silence(track_audio) / 1000
        except:
            return HttpResponse(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
        return HttpResponse(response_data)
    return HttpResponse(response_data)


def download_song(request, track_name):
    media_name = os.path.join(settings.MEDIA_ROOT, track_name)
    try:
        track = open(media_name, 'r')
    except:
        return HttpResponse(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(track_name)
    response['X-Sendfile'] = smart_str(media_root)
    return response


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request: http.HttpRequest, *args: any, **kwargs: any) -> http.HttpResponse:       
        return render(request, 'index.html')


class TrackListView(ListView):
    model = Track
    template_name = 'soundboard/track-list.html'

    def get_queryset(self) -> QuerySet:
        return Track.objects.all() 

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class TrackDetailView(DetailView):
    model = Track
    template_name = 'soundboard/track-detail.html'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        return super().get_context_data(**kwargs)


class TrackCreateView(CreateView):
    model = Track
    template_name = 'soundboard/track-custom-form.html'
    fields = '__all__'
    success_url  = reverse_lazy('track-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('track-list')

    def form_valid(self, form):
        response = super().form_valid(form)  
        host = socket.gethostbyname(socket.gethostname())
        print(host)
        data = {
            'id': self.object.pk,
            'artist': self.object.artist,
            'title': self.object.title,
            'file': self.object.file.url
        }
        return JsonResponse(data)


class TrackUpdateView(UpdateView):
    model = Track
    template_name = 'soundboard/track-custom-form.html'
    fields = '__all__'
    success_url = reverse_lazy('track-list')

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('track-list')


class TrackDeleteView(DeleteView):
    model = Track
    template_name = 'soundboard/track-confirm-delete.html'
    success_url = reverse_lazy('track-list')

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        return super().get_context_data(**kwargs)