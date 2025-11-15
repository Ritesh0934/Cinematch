from django.urls import path
from . import views
from django.contrib.auth import views as Auth_views

urlpatterns = [
    path('register/',views.Register,name='register'),
    path('login/',views.login_view,name = 'login'),
    path('logout/', views.logout_view, name='logout'),
]
