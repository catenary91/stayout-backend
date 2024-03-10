from django.urls import path

from .views import signup, register

urlpatterns = [
    path('signup', signup),
    path('register', register)
]