# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from datetime import datetime
import json

import csv


filename = "sample_data.csv"

# Create your models here.
class CsvRow(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=5)
    os = models.CharField(max_length=5)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    installs = models.IntegerField(default=0)
    spend = models.FloatField(default=0)
    revenue = models.FloatField(default=0)

    def info(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "channel": self.channel,
            "country": self.country,
            "os": self.os,
            "impressions": self.impressions,
            "installs": self.installs,
            "clicks": self.clicks,
            "spend": self.spend,
            "revenue": self.revenue
        }

    def __str__(self):
        # there wasn't any suitable string representation that i could think
        # of, hence stringy-fying JSON Info of the object
        return json.dumps(self.info())


def read_data():
    """
    This is the method to read the data from the CSV file using
    csv module, and fetch all details from its each row and convert
    them into a db record by calling CsvRow Model object
    """

    counter = 0
    with open(filename, "r") as infile:
        reader = csv.reader(infile)
        reader.next()
        for row in reader:
            date = row[0].replace(".", "-")
            date = datetime.strptime(date, "%d-%m-%Y").date()
            channel = row[1]
            country = row[2]
            os = row[3]
            impressions = int(row[4])
            clicks = int(row[5])
            installs = int(row[6])
            spend = float(row[7])
            revenue = float(row[8])

            try:
                obj, created = CsvRow.objects.get_or_create(date=date, channel=channel,
                        country=country, os=os, impressions=impressions,
                        clicks=clicks, installs=installs,
                        spend=spend, revenue=revenue)
                if created:
                    obj.save()
            except Exception as e:
                print e
