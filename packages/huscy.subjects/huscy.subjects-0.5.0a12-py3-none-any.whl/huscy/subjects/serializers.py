import logging
from datetime import date

from dateutil import relativedelta
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import exceptions, serializers

from huscy.subjects import helpers, models, services

logger = logging.getLogger('huscy.subjects')


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(initial='DE')

    class Meta:
        model = models.Address
        fields = (
            'city',
            'country',
            'street',
            'zip_code',
        )


class PhoneSerializer(serializers.ModelSerializer):
    label_display = serializers.CharField(source='get_label_display', read_only=True)
    number = PhoneNumberField()

    class Meta:
        model = models.Phone
        fields = (
            'contact',
            'label',
            'label_display',
            'number',
        )


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = models.Contact
        fields = (
            'address',
            'date_of_birth',
            'display_name',
            'email',
            'first_name',
            'gender',
            'gender_display',
            'last_name',
        )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = services.create_address(**address_data)
        return services.create_contact(address=address, **validated_data)

    def update(self, contact, validated_data):
        address_data = validated_data.pop('address')
        services.update_address(contact, **address_data)
        return services.update_contact(contact, **validated_data)


class GuardianSerializer(ContactSerializer):

    def create(self, validated_data):
        subject = self.context['subject']
        contact = super().create(validated_data)
        return services.add_guardian(subject, contact)


class SubjectSerializer(serializers.ModelSerializer):
    age_in_months = serializers.SerializerMethodField()
    contact = ContactSerializer()
    guardians = GuardianSerializer(many=True, read_only=True)
    is_child = serializers.BooleanField()
    is_patient = serializers.BooleanField()

    class Meta:
        model = models.Subject
        fields = (
            'age_in_months',
            'contact',
            'guardians',
            'id',
            'is_active',
            'is_child',
            'is_patient',
        )

    def get_age_in_months(self, subject):
        delta = relativedelta.relativedelta(date.today(), subject.contact.date_of_birth)
        return delta.years * 12 + delta.months

    def create(self, validated_data):
        request = self.context.get('request')
        logger.info('User %s tried to create new subject from ip %s',
                    request.user.username, helpers.get_client_ip(request))

        contact_data = validated_data.pop('contact')
        address_data = contact_data.pop('address')

        address = services.create_address(**address_data)
        contact = services.create_contact(address=address, **contact_data)
        return services.create_subject(contact, **validated_data)

    def update(self, subject, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = contact_data.pop('address')

        services.update_address(subject.contact, **address_data)
        services.update_contact(subject.contact, **contact_data)
        return services.update_subject(subject, **validated_data)


class InactivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inactivity
        fields = (
            'subject',
            'until',
        )

    def create(self, validated_data):
        try:
            return services.set_inactivity(**validated_data)
        except ValueError:
            raise exceptions.ValidationError


class NoteSerializer(serializers.ModelSerializer):
    option_display = serializers.CharField(source='get_option_display', read_only=True,)
    creator_username = serializers.SerializerMethodField(source='get_creator_username')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def get_creator_username(self, obj):
        return obj.creator.username

    class Meta:
        model = models.Note
        fields = (
            'id',
            'option',
            'option_display',
            'creator',
            'creator_username',
            'created_at',
            'text',
        )
        extra_kwargs = {
            'creator': {'write_only': True},
            'option': {'write_only': True},
        }

    def create(self, validated_data):
        subject = self.context['subject']
        return services.create_note(subject=subject, **validated_data)
