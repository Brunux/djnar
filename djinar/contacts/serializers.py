from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """[summary]
    Manage contact serialization
    [description]
    """

    class Meta:
        model = Contact
        exclude = ('owner',)
