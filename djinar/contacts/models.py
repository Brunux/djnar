from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Contact(TimeStampedModel):
    """[summary]
    Model for managing `contact` information.

    [description]

    """
    name = models.CharField(_("Full name"), max_length=254)
    job_title = models.CharField(_("Job title"), max_length=62)
    company = models.CharField(_("Company Name"), max_length=254)
    email = models.EmailField()
    contact_number = models.CharField(_("Contact Number"), max_length=14)
    notes = models.CharField(_("Notes"), max_length=508)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return str(self.email)
