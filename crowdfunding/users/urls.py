from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('users/profiles/<int:user_id>/', views.ProfileDetail.as_view()),
    path('users/check-username/<str:username>/', views.CheckUsernameAvailable.as_view()),
]