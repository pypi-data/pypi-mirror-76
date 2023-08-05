from functools import lru_cache
from typing import Set, Iterable

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils.functional import cached_property
from .utils import get_all_dynamic_perm_names, get_dynamic_perms

User = get_user_model()

ALL_DYNA_PERMS = get_all_dynamic_perm_names()


class DynamicBackend(ModelBackend):

    @cached_property
    def _get_all_dynamic_perms(self) -> Iterable[str]:
        """
        Property exists so that if people need to override
        the behavior of fetching all the permissions
        """
        return ALL_DYNA_PERMS

    @lru_cache()
    def _get_user_dynamic_perms(self, user: User) -> Set[str]:
        """
        Based on a user obj, check a bunch of functions and return them if they're valid
        """
        perms = set()

        for name, funcs in get_dynamic_perms().items():
            authorized = any([func(user) for func in funcs])

            if authorized:
                perms.add(name)

        return perms

    def get_all_permissions(self, user: User, obj=None):
        if not user.is_active or user.is_anonymous or obj is not None:
            return set()

        if user.is_superuser:
            return self._get_all_dynamic_perms
        else:
            return self._get_user_dynamic_perms(user)
