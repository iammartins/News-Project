from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('analysis/', include('analysis.urls')),
    path('accounts/', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)