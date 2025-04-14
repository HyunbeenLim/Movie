from django.db import models
from accounts.models import User

class Genre(models.Model):
    genre = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.TextField()
    overview = models.TextField()
    released_date = models.DateField()
    running_time = models.IntegerField(blank=True, null=True)
    avg_rating = models.FloatField()
    nation = models.CharField(max_length=100, blank=True, null=True)
    language = models.TextField()
    adult = models.BooleanField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    # liked = models.ManyToManyField(User, related_name='liked_movies', through='UserMovieLike')
    youtube_key = models.CharField(max_length=100)

class UserMovieLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_movie')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='liked')
    like = models.IntegerField(default=0)

class UserGenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='user_preferences')
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'genre')

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    rating = models.FloatField()
    user_likes = models.ManyToManyField(User, related_name='liked_reviews')

# 챗봇 채팅 기록
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 대화의 주체 system은 프롬프트 설정, assistant는 챗봇
    role = models.CharField(max_length=20, choices=[('system', 'System'), ('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)