from rest_framework.permissions import DjangoObjectPermissions
from . import models


class IsProductOwner(DjangoObjectPermissions):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj: models.Product):
        return obj.user_id == request.user
