from rest_framework import serializers

from djinar.contacts.models import Contact
from .models import Event


class EventContactSerializer(serializers.ModelSerializer):
    """[summary]
    Manage Contacts items nested in Event serialization for retrieving.
    [description]
    """

    class Meta:
        model = Contact
        fields = ('name', 'email', 'pid', )


class EventSerializer(serializers.ModelSerializer):
    """[summary]
    Manage Event serialization for retrieving.
    [description]
    """
    attendants = EventContactSerializer(many=True)

    class Meta:
        model = Event
        exclude = ('owner', 'id', )
        depth = 1


class EventCreateSerializer(serializers.ModelSerializer):
    """[summary]
    Manage Event serialization for creation.
    [description]
    """

    class Meta:
        model = Event
        fields = "__all__"
