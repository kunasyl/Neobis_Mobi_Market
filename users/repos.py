from rest_framework.generics import get_object_or_404

from . import models


class AuthRepos:
    model = models.User
    profile = models.Profile

    def get_user(self, user_id) -> models.User:
        return self.model.objects.get(id=user_id)

    def get_user_by_email(self, email) -> models.User:
        return self.model.objects.get(email=email)

    def get_user_by_data(self, data):
        user = get_object_or_404(self.model, username=data['username'])

        if not user.check_password(data['password']):
            raise self.model.DoesNotExist

        return user

    def get_profile(self, user_id):
        return self.profile.objects.get(user_id=user_id)
