import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
from djinar.contacts.models import Contact


class Event(TimeStampedModel):
    """[summary]
    Events for webinar like sessions.

    [description]
    """
    title = models.CharField(_("Title"), max_length=128)
    date = models.DateTimeField(_("Date and time"))
    duration = models.PositiveSmallIntegerField(_("Duration in minutes"))
    notes = models.TextField(_("Notes"))
    attendants = models.ManyToManyField(Contact, blank=True)
    pid = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ('-modified', )

    def __str__(self):
        return str(self.title)
