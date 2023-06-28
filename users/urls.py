from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('form/', ProfileForm.as_view(), name='form'),
    path('update_phone_number/', UpdatePhoneNumberView.as_view(), name='update_password'),
    path('verify_code/<str:phone_number>', PhoneNumberVerificationView.as_view(), name='verify_code'),

    path('<int:user_id>/set_password/', UpdatePasswordView.as_view(), name='set_password'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
