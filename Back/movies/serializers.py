from rest_framework import serializers
from .models import Movie, Genre, Review, UserMovieLike, UserGenrePreference

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class UserMovieLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieLike
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태
    is_disliked = serializers.SerializerMethodField()  # 싫어요 상태
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

    def get_is_liked(self, obj):
        # 현재 요청한 유저가 이 영화를 좋아요했는지 확인
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked.filter(user=user, like=1).exists()
        return False

    def get_is_disliked(self, obj):
        # 현재 요청한 유저가 이 영화를 싫어요했는지 확인
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.liked.filter(user=user, like=0).exists()
        return False


class MovieSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
#         read_only_fields = ('user','movie','user_likes')

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'username', 'content', 'rating', 'created_at']
        read_only_fields = ['user', 'movie']

class ReviewWithMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = Review
        fields = ['id', 'content', 'rating', 'movie', 'created_at']

class UserGenrePreferenceSerializer(serializers.ModelSerializer):
    genre_id = serializers.IntegerField(source='genre.id')
    genre_name = serializers.CharField(source='genre.genre')

    class Meta:
        model = UserGenrePreference
        fields = ['genre_id', 'genre_name', 'count']