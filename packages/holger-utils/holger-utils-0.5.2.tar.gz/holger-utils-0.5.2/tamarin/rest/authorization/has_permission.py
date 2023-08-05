from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.db.models import Q


class HasPermission(BasePermission):

    def has_permission(self, request, view):
        User = get_user_model()
        permissions = getattr(self, 'filter')
        if permissions:
            if type(permissions) == list:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(permissions__codename_in=permissions) | Q(groups__permissions__codename_in=permissions),
                )
                return queryset.exists()
            elif type(permissions) == str:
                queryset = User.objects.filter(
                    Q(pk=request.user.pk),
                    Q(permissions__codename=permissions) | Q(groups__permissions__codename=permissions),
                )
                return queryset.exists()
            else:
                raise AttributeError('permissions type is not list or string')
        else:
            raise AttributeError('permissions does not set')
