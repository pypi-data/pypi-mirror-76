from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission

from huscy.subjects.serializers import ContactSerializer


def test_admin_can_create_subject(admin_client, contact):
    assert_status_created(create_subject(admin_client, contact))


def test_anonymous_cannot_create_subject(client, contact):
    client.logout()
    assert_status_forbidden(create_subject(client, contact))


def test_user_with_permissions_can_create_subject(client, user, contact):
    add_permission(user, 'add_subject')
    assert_status_created(create_subject(client, contact))


def test_user_without_permissions_cannot_create_subject(client, contact):
    assert_status_forbidden(create_subject(client, contact))


def create_subject(client, contact):
    data = {
        'contact': ContactSerializer(contact).data,
        'is_child': False,
        'is_patient': False,
    }
    return client.post(reverse('subject-list'), data=data, format='json')
