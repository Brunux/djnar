from enum import Enum

from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _
# Create your models here.


class Server(models.Model):
    """[summary]
    Servers used for streaming
    [description]

    Extends:
        models.Model
    """

    class STATUS(Enum):
        """[summary]
        Manage Server status.
        [description]
        Possible server status are:
            Online: servers is usable for streaming.
            Offline: Server is unusable
        Extends:
            Enum
        """
        online = ("online", _("Online"))
        offline = ("offline", _("Offline"))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    ip = models.IPAddressField(
        _("Server IP Address"),
        blank=True,
        null=True
    )
    fqdn = models.CharField(
        _("Fully Qualified Domain Name"),
        max_length=512,
        blank=True,
        null=True,
    )
    is_public = models.BooleanField(
        _("Is Public?"),
        default=True,
        blank=True,
    )
    owners = models.ManyToManyField(
        _("Owners"),
        get_user_model(),
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("Status"),
        choices=[status.value for status in STATUS],
        max_length=50,
        default=STATUS.offline,
        blank=True
    )
    token = models.ForeignKey("tokens.Token")
