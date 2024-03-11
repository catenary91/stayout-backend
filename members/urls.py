from django.urls import path

from .views import apply_view, signup_view, register_view

urlpatterns = [
    path('signup', signup_view),
    path('register', register_view),
    path('apply', apply_view),
]