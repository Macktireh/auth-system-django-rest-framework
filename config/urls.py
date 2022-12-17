
from django.contrib import admin
from django.urls import include, path, re_path

from docs.swagger import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/user/', include('apps.authentication.urls')),
    
    # swagger
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='docs-api'),
]
