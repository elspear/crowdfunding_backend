from django.contrib import admin
from django.urls import path, include
from users.views import CustomAuthToken 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fundraisers.urls')),
    path('', include('users.urls')),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token_auth')
]