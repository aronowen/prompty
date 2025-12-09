from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #Home Views
    path('', include('home.urls')),
    path("i18n/", include("django.conf.urls.i18n"))
]
