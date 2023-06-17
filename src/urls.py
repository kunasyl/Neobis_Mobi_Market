from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      # description="Description",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kunasyl45@gmail.com"),
      # license=openapi.License(name="BSD License"),
      date_format="%d.%m.%Y",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('', include('users.urls')),
    path('products/', include('products.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
