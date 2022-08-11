from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('activate/<str:activation_code>/', views.ActivationView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('users/', views.UserListAPIView.as_view()),
    path('profile/<int:pk>/', views.ProfileRetrieveAPIView.as_view()),
    path('profile/update/<int:pk>/', views.ProfileUpdateAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]