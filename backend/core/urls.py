from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', views.PeopleView, basename='users')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='token_register'),
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='token_logout'),
    path('user/', views.UserView.as_view(), name="user"),
    path('posts/', views.PostView.as_view(), name='posts')
]+router.urls