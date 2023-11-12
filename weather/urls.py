from django.urls import path

from .views import located

urlpatterns = [
    path("", located, name="home"),
]
