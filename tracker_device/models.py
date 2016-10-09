from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import uuid


@python_2_unicode_compatible
class TrackerDevice(models.Model):
    """Model for tracker hardware."""
    user = models.ForeignKey(
        User,
        related_name="devices",
        on_delete=models.deletion.CASCADE
    )
    device_type = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    mode = models.CharField(
        max_length=200,
        choices=(
            ('quiet', 'quiet'),
            ('transmit', 'transmit'),
            ('debug', 'debug'),
            ),
        default='transmit'
        )
    id_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class DataPoint(models.Model):
    """Model for data points."""
    device = models.ForeignKey(
        TrackerDevice,
        related_name='data',
        on_delete=models.deletion.CASCADE
    )
    time = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()
    elevation = models.FloatField()
    time_received = models.DateTimeField(auto_now_add=True)


class Route(models.Model):
    """Model for route."""
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    device = models.ForeignKey(
        TrackerDevice,
        related_name='routes',
        on_delete=models.deletion.CASCADE
    )
