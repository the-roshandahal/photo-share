from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("", views.home, name="home"),
    path('create_gallery/', views.create_gallery, name='create_gallery'),
    path('user_login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_photo_guest/<str:event_credentials>/', views.upload_photo_guest, name='upload_photo_guest'),
    path('create_event/', views.create_event, name='create_event'),
    path('event/<str:event_credentials>/<str:secret_token>/', views.event, name='event'),
    path('gallery_detail/<int:gallery_id>/', views.gallery_detail, name='gallery_detail'),
    path('download_qr_code/<str:event_credentials>/<str:secret_token>/', views.download_qr_code, name='download_qr_code'),


    
    
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)