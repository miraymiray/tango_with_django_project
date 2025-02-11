from django.contrib import admin
from django.urls import path, include  # Added include
from rango import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rango'

urlpatterns = [
   path('', views.index, name='index'),
   path('rango/', include('rango.urls')),
   path('admin/', admin.site.urls),

   # NEW: Django's built-in authentication URLs
   path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
