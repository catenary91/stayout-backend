from django.urls import path

from .views import signup_view
from .kakao_views import register_view, get_history_view, apply_view

urlpatterns = [
    path('signup', signup_view),
    path('register', register_view),
    path('get_history', get_history_view),
    path('apply', apply_view),
]