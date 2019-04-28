import models
import django_filters

class CsvRowFilter(django_filters.FilterSet):
    class Meta:
        model = models.CsvRow
        fields = ["date", "channel", "country", "os",]
