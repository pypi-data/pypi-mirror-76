from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from django.contrib.auth import get_user_model

import pytest

pytestmark = pytest.mark.django_db(transaction=True)

User = get_user_model()

PERM_NAME = 'has_test'


def always_true(user):
    return True


def always_false(user):
    return False


@pytest.fixture(autouse=True)
def user():
    user = User(username='test', password='Safepass1.', is_active=True)
    user.save()
    return user


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.always_true'
    ]
})
def test_parm_is_present():
    from dynaperms.utils import get_dynamic_perms

    assert get_dynamic_perms()[PERM_NAME]


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.always_false'
    ]
})
def test_user_has_perm_false(user):
    assert user.has_perm(PERM_NAME) is False


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.always_true'
    ]
})
def test_user_has_perm_true(user):
    from dynaperms.utils import get_dynamic_perms

    assert get_dynamic_perms()[PERM_NAME]

    user.is_active = False
    user.save()
    assert user.has_perm(PERM_NAME) is False
    user.is_active = True
    user.save()
    assert user.has_perm(PERM_NAME) is True


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.always_false',
        'tests.tests.always_false'
    ]
})
def test_multiple_dynamic_checks_none_return_true(user):
    assert user.has_perm(PERM_NAME) is False


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.always_true',
        'tests.tests.always_false'
    ]
})
def test_multiple_dynamic_checks_at_least_one_returns_true(user):
    assert user.has_perm(PERM_NAME) is True


@override_settings(DYNAMIC_PERMISSIONS={
    PERM_NAME: [
        'tests.tests.not_here'
    ]
})
def test_multiple_dynamic_checks_at_least_one_returns_true(user):
    with pytest.raises(ImproperlyConfigured):
        user.has_perm(PERM_NAME)
