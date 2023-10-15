from django.urls import path
from . import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'posts', views.Post, basename='posts')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='token_register'),
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='token_logout'),
    path('user/', views.User.as_view(), name="user")
]+router.urls