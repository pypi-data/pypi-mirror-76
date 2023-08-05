from typing import Iterable
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_all_dynamic_perm_names() -> Iterable[str]:
    """
    Get a list of all dynamic permissions
    """
    return settings.DYNAMIC_PERMISSIONS.keys()


def get_funcs_for_dynamic_perm_name(key: str) -> Iterable[str]:
    """
    Get a list of strings at a particular dictionary key
    """
    return settings.DYNAMIC_PERMISSIONS[key]


def get_dynamic_perms():
    """
    Return a dictionary where each key has a list of functions
    """
    perms = {}

    try:
        for perm in get_all_dynamic_perm_names():
            perms[perm] = [import_string(func_path) for func_path in get_funcs_for_dynamic_perm_name(perm)]
    except ImportError as e:
        raise ImproperlyConfigured(e)

    return perms
