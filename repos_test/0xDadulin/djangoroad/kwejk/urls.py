from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'kwejk'
urlpatterns = [
    path('upload/', views.image_upload_view)
    
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)