"""
URL configuration for Triple_H project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomLoginView, CustomRegisterView, CustomUserView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('dj-rest-auth/<int:user_id>/', CustomUserView),
    # path('accounts/signup/', include('dj_rest_auth.registration.urls')),
        # 추가
    path('accounts/signup/', CustomRegisterView.as_view(), name='custom_signup'),
]
