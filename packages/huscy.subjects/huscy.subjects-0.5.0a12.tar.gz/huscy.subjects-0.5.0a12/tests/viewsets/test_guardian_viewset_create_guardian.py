import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_guardians_url(subject, guardian):
    url = reverse('guardian-list', kwargs=dict(subject_pk=subject.pk))
    assert url == f'/api/subjects/{subject.pk}/guardians/'


def test_admin_user_can_create_guardian(admin_client, subject):
    response = create_guardian(admin_client, subject)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_create_guardian(client, user, subject):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = create_guardian(client, subject)

    assert response.status_code == HTTP_201_CREATED, response.json()


def test_user_without_permission_cannot_create_guardian(client, subject):
    response = create_guardian(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_guardian(anonymous_client, subject):
    response = create_guardian(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_guardian(client, subject):
    return client.post(
        reverse('guardian-list', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            address=dict(
                city='city',
                country='de',
                street='street',
                zip_code='12345',
            ),
            date_of_birth='2000-1-1',
            display_name='prof. dr. first_name last_name',
            first_name='first_name',
            gender=0,
            last_name='last_name',
        ),
        format='json',
    )
