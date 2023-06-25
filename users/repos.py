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


class ProfileRepos:
    user_model = models.User
    profile_model = models.Profile

    def get_profile(self, user_id):
        return self.profile_model.objects.get(user_id=user_id)

    def get_phone_number(self, user_id):
        profile = self.get_profile(user_id=user_id)
        return profile.phone_number