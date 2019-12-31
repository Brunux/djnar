from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """[summary]
    Manage contact serialization for retrieving
    [description]
    """

    class Meta:
        model = Contact
        exclude = ('owner',)


class ContactCreateSerializer(serializers.ModelSerializer):
    """[summary]
    Manage contact serialization for creation
    [description]
    """

    class Meta:
        model = Contact
        fields = "__all__"
