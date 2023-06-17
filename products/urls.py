from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from products.views import *

router = DefaultRouter()
router.register(r'', ProductViewSet)
urlpatterns = router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
