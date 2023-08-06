from model_bakery import baker
from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission


def test_admin_can_update_contact(admin_client, contact):
    response = update_contact(admin_client, contact)

    assert_status_ok(response)
    assert response.json()['email'] != contact.email


def test_user_without_permissions_cannot_update_contact(client, contact):
    assert_status_forbidden(update_contact(client, contact))


def test_user_with_permissions_can_update_contact(client, contact, user):
    add_permission(user, 'change_contact')

    response = update_contact(client, contact)

    assert_status_ok(response)
    assert response.json()['email'] != contact.email


def test_anonymous_cannot_update_contact(client, contact):
    client.logout()
    assert_status_forbidden(update_contact(client, contact))


def update_contact(client, contact):
    address = baker.prepare('subjects.Address')

    data = dict(
        address=dict(
            city=address.city,
            country=address.country.name,
            street=address.street,
            zip_code=address.zip_code,
        ),
        first_name=contact.first_name,
        last_name=contact.last_name,
        display_name=contact.display_name,
        gender=contact.gender,
        date_of_birth=contact.date_of_birth,
        email='another@email.com',
    )
    return client.put(reverse('contact-detail', kwargs=dict(pk=contact.pk)),
                      data=data, format='json')
