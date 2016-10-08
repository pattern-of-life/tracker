from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class TrackerProfile(models.Model):
    """A profile representing a tracker site patron."""

    user = models.OnetoOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=2083, blank=True)
    access_level = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=2083, blank=True)
    street_address = models.CharField(max_length=2083, blank=True)
    website = models.CharField(max_length=2083, blank=True)
    social_media = models.CharField(max_length=2083, blank=True)

    def __str__(self):
        return "TrackerProfile for {}".format(self.user)


@receiver(post_save, sender=User)
def update_tracker_profile(sender, **kwargs):
    if not TrackerProfile.objects.filter(user=kwargs['instance']):
        TrackerProfile(
            user=kwargs['instance']
        ).save()
