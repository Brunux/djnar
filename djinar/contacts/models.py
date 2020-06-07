import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Contact(TimeStampedModel):
    """Model for managing `contact` information."""

    name = models.CharField(_("Full name"), max_length=255)
    job_title = models.CharField(_("Job title"), max_length=255)
    company = models.CharField(_("Company Name"), max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(_("Contact Number"), max_length=62)
    notes = models.TextField(_("Notes"))
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    pid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ('-modified', )

    def __str__(self):
        return str(self.email)
