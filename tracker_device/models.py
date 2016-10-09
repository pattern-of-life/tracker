from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import uuid


@python_2_unicode_compatible
class TrackerDevice(models.Model):
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
