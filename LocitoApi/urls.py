from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "LocitoApi"
urlpatterns = [
    path("register",views.RegisterView.as_view(),name="registerApi"),
    path("login",views.customTokenObtainPairView.as_view(),name="loginApi"),
    path('accesstoken',views.AccessToken.as_view(),name='accesstokenApi'),
    path('updatePassword',views.UpdatePassword.as_view(),name='updatePasswordApi'),
    path('updateUsername',views.UpdateUsername.as_view(),name='updateUsernameApi'),
    path('createProfile',views.CreateProfile.as_view(),name='createProfileApi'),
    path("getProfile",views.getProfile.as_view(),name='getProfileApi'),
    path("getPosts",views.getPosts.as_view(),name="getPostsApi"),
    path('getProfileImage',views.getProfileImageUrl.as_view(),name="getprofileImageApi"),
    path('getProducts',views.getProducts.as_view(),name="getproductsApi"),
    path("searchProfile",views.SearchProfile.as_view()),
]
