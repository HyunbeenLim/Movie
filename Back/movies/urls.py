from . import views
from django.urls import path, include

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('genre/', views.genre, name='genre'),
    path('genre/count/', views.userGenre_count, name='userGenre_count'),
    path('genre/<int:genre_id>/', views.movie_genre, name='movie_genre'), # 특정 장르(<str:genre>)가 포함된 영화 출력
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/like/<int:preference>/', views.movie_like, name='movie_like'),
    path('<int:movie_pk>/reviews/', views.reviews, name='reviews'),
    path('<int:movie_pk>/reviews/create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.delete_review, name='delete_review'),
    path('<int:movie_pk>/reviews/<int:review_pk>/update/', views.update_review, name='update_review'),
    path('liked/<int:user_id>/', views.liked_movies, name='liked_movies'),
    path('liked/count/', views.like_unlike_count, name='like_unlike_count'),
    path('user-reviews/<int:user_id>/', views.user_reviews, name='user_reviews'),
    path('recommendations/', views.make_recommendations, name='recommendations'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/initial/', views.initial_chat_view, name='initial-chat'),
]
