from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models, services, repos

auth_repos = repos.AuthRepos()
profile_repos = repos.ProfileRepos()

sms_services = services.SMSServices()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'username')

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        user.save()

        profile = models.Profile.objects.create(user_id=user)
        profile.save()

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = auth_repos.get_user_by_email(email=instance.email)
        data['user_id'] = user.id  # Add user ID to the response data
        return data


class RetrieveProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_username(self, obj):
        user = auth_repos.get_user(user_id=obj.user_id.id)
        return user.username

    def get_email(self, obj):
        user = auth_repos.get_user(user_id=obj.user_id.id)
        return user.email

    class Meta:
        model = models.Profile
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()

        return instance


class UpdatePhoneNumberSerializer(serializers.ModelSerializer):
    """
    Send SMS to phone number for verification
    """

    class Meta:
        model = models.PhoneVerification
        fields = '__all__'
        extra_kwargs = {
            'phone_number': {'required': True}
        }

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        msg_code = sms_services.send_message(phone=phone_number, message='Код для верификации')
        if msg_code:
            phone_ver = models.PhoneVerification.objects.create(phone_number=phone_number, code=msg_code)
            return phone_ver
        raise ValidationError("Ошибка при отправке SMS на номер телефона")


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)

    def create(self, validated_data):
        phone_number = self.context.get('phone_number')
        user_id = self.context.get('user_id')
        actual_code = models.PhoneVerification.objects.get(phone_number=phone_number).code
        if validated_data.get('code') == actual_code:
            # verify user
            user = models.User.objects.get(id=user_id)
            user.is_verified = True
            user.save()

            # save phone_number
            profile = models.Profile.objects.get(user_id=user_id)
            profile.phone_number = phone_number
            profile.save()

        return {'code': actual_code}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
