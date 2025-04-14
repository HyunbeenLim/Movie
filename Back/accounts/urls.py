from . import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.account_delete, name='account_delete'),
    path('update/', views.account_update, name='account_update'),
    path('<int:user_pk>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/password/', views.change_password, name='change_password'),
]
