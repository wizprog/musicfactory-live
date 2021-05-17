from django.db import models

import os
# Create your models here.
class Track(models.Model):
    file = models.FileField(null=True, blank=True)
    artist = models.CharField(max_length=255, blank=True, null=True, default='unknown', verbose_name='artist name')
    title = models.CharField(max_length=255, blank=True, null=True, default='unknown', verbose_name='track title')

    class Meta:
        verbose_name_plural = "Tracks"

    def __str__(self) -> str:
        return f'{self.title}, {self.artist}'

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(Track, self).delete(*args, **kwargs)