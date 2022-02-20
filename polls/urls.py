"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . import views
from .views import ChangePasswordView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('hello/', views.index.as_view(), name='index'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='auth_logout'),
   # path('login/', views.login_api),
    path('user/', views.get_user_data),
    path('register/', views.register_api),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),

   # path('reset-password/verify-token/', acc_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    # NEW: The django-rest-passwordreset urls to request a token and confirm pw-reset
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    #path(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('<int:question_id>/', views.detail),
    path('<int:question_id>/results/',views.results),
    path('<int:question_id>/vote/',views.vote),
    path('age/<str:my_age>',views.age)
]
