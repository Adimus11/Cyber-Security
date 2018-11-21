from django.urls import path
from main.views import (
    index,
    signup,
    account,
    signin,
    signout,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('account/', account, name='account'),
    path('signin/', signin, name='login'),
    path('signout', signout, name='logout')
]