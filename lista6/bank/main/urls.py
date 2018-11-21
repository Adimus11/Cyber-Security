from django.urls import path
from main.views import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
]