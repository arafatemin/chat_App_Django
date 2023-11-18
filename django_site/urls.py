from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path("login/", views.login_view, name="login"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
