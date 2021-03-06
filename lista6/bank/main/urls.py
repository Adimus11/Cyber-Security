from django.contrib.auth import views as auth_views
from django.urls import path
from main.views import (
    index,
    signup,
    account,
    signin,
    signout,
    transfer,
    transfer_detail,
    transfer_overview,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', index, name='index'),
    path('account/', account, name='account'),
    path('signin/', signin, name='login'),
    path('signout/', signout, name='logout'),
    path('transfer/', transfer, name='transfer'),
    path('transfer_detail/<int:transfer_id>/', transfer_detail, name='show_transfer'),
    path('transfer/<int:transfer_id>/', transfer_overview, name='look_transfer'),
]