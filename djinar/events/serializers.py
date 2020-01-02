from rest_framework import serializers

from djinar.contacts.models import Contact
from .models import Event


class EventContactLinkSerializer(serializers.ModelSerializer):
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
    attendants = EventContactLinkSerializer(many=True)

    class Meta:
        model = Event
        exclude = ('owner', 'id', )
        depth = 1


class EventContactLinkCreateSerializer(serializers.Serializer):
    """[summary]
    Manage Contacts items nested in Event serialization for retrieving.
    [description]
    """
    pid = serializers.UUIDField(format='hex_verbose')

    def validate_pid(self, data):
        """[summary]
        Returns the Contact instance model instance instead of uuid.
        [description]

        Arguments:
            value {[uuid4]} -- [uuid to validate]
        """
        pid_validated = super().validate(data)
        qs = Contact.objects.filter(
            pid=pid_validated,
        )
        if not qs.exists():
            return Contact.objects.none()
        return qs.first()


class EventCreateSerializer(serializers.ModelSerializer):
    """[summary]
    Manage Event serialization for creation.
    [description]
    """

    attendants = EventContactLinkCreateSerializer(many=True, allow_null=True)

    class Meta:
        model = Event
        fields = "__all__"

    @staticmethod
    def _set_attendants(attendants, event):
        """[summary]
        Sets attendants to an event.

        [description]

        Arguments:
            attendants {[List of OrderDicts]} -- [The contacts to
            link to event]
            event {[`Event` model instance]} -- [Event.attendants to link]
        """
        if attendants:
            event.attendants.set(
                (contact['pid'] for contact in attendants
                    if contact.get('pid', False))
            )

    def _perform_create_or_update(self, validate_data, instance=None):
        """[summary]
        Performs creation or updated for an event.

        [description]
        It identifies the `update` bases on the `instance` parameter,
        if it exists updates otherwise creates.
        """
        attendants = validate_data['attendants']
        del validate_data['attendants']

        if instance is None:
            event = super().create(validate_data)
        else:
            event = super().update(instance, validate_data)

        self._set_attendants(attendants, event)
        return event

    def create(self, validate_data):
        """[summary]
        Delegates creation to _perform_create_or_update.
        [description]

        Arguments:
            validate_data {[Dictionary]} -- [Creational data]
        """
        return self._perform_create_or_update(validate_data)

    def update(self, instance, validate_data):
        """[summary]
        Delegates update to _perform_create_or_update
        [description]

        Arguments:
            instance {[`Event` model instance]} -- [the event to be updated]
            validate_data {[Dictionary]} -- [Data to be updated]
        """
        return self._perform_create_or_update(validate_data, instance=instance)
