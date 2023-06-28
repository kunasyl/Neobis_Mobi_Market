from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from products.views import *

router = DefaultRouter()
router.register(r'', ProductViewSet)
urlpatterns = [
    path('my_products/', UserProductView.as_view(), name='user_products'),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
