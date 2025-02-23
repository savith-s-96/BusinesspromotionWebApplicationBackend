from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register-api",views.RegisterView.as_view(),name="register-api"),
    path("login",TokenObtainPairView.as_view(),name="login-api"),
    path('refreshtoken',TokenRefreshView.as_view(),name='refreshtoken-api'),
    path('updatePassword',views.UpdatePassword.as_view(),name='updatePassword-api'),
    path('updateUsername',views.UpdateUsername.as_view(),name='updateUsername-api')
]
