# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=50)
    songs_count = models.IntegerField(default=0)
    genre = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=50)
    size = models.IntegerField(default=0)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

