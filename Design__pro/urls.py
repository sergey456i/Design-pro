from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from requests import views as req_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superadmin/', include('requests.urls_admin')),
    path('', req_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('profile/', include('requests.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)