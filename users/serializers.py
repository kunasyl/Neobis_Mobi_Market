from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models, services, repos

repos = repos.AuthRepos()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'username')

    def create(self, validated_data):
        request = self.context.get('request')

        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = repos.get_user_by_email(email=instance.email)
        data['user_id'] = user.id  # Add user ID to the response data
        return data


class RetrieveProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_username(self, obj):
        user = repos.get_user(user_id=obj.user_id)
        return user.username

    def get_email(self, obj):
        user = repos.get_user(user_id=obj.user_id)
        return user.email

    class Meta:
        model = models.Profile
        fields = '__all__'


class CreateProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)

    class Meta:
        model = models.Profile
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'birth_date': {'format': '%d.%m.%Y', 'required': True}
        }

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        user = repos.get_user(user_id=user_id)

        if validated_data.get('email'):
            form_email = validated_data.get('email')
            if form_email != user.email:
                raise ValidationError("Invalid email.")

        profile = models.Profile.objects.create(
            user_id=user,
            **validated_data
        )

        return profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
