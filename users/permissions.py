from rest_framework.permissions import BasePermission
from rest_framework import exceptions

from . import repos


class IsVerifiedUserPermission(BasePermission):
    repos = repos.AuthRepos()
    message = "Ваш аккаунт неактивен. Пройдите по ссылке, которую мы отправили вам на почту."

    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        user = self.repos.get_user(user_id=user_id)

        if not user.is_verified:
            raise exceptions.PermissionDenied(detail=self.message)

        return True


class IsAuthorizedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
