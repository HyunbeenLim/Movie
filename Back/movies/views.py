from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .serializers import MovieListSerializer, MovieSerializer, GenreListSerializer, ReviewSerializer, ReviewWithMovieSerializer, UserGenrePreferenceSerializer
from .models import Movie, Genre, UserMovieLike, UserGenrePreference, Review
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
# 추천 함수
import numpy as np
import pandas as pd
from scipy.special import digamma, polygamma
from .recommender_system import safe_log, logsumexp, safe_tri, psi_vec, vector_int_sum, vector_int_prod, vector_sum, vector_diff, vector_prod, make_id, df2triplet, get_top_indices, find_user, recommend, lda 
import json
## 사용자 데이터 가져오기
from django.contrib.auth import get_user_model
## sentiment 파일 가져올 때
import os
from django.conf import settings
# 챗봇
from .models import ChatMessage
from .utils.openai_api import chat_with_gpt
# 검색용도
from django.db.models import Q                  # 조건문 Q객체로 만들기
# from django.core.paginator import Paginator     # 페이지 나누기

# Create your views here.
@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True, context={'request': request})

        return Response(serializer.data)
    
    return render(request, 'movies/index.html')

# 검색기능
@api_view(['GET'])
def search(request):
    if request.method == 'GET':
        # 검색 쿼리 설정
        search_query = request.GET.get('search', '')
        movies = Movie.objects.all()
        if search_query:
            movies = movies.filter(Q(title__icontains=search_query) | Q(overview__icontains=search_query))
            print('검색 동작!!')
            search_movie_ids = [
            movie.id for movie in movies
            ]
        return JsonResponse({'search_movie_ids':search_movie_ids})

@api_view(['GET'])
def genre(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreListSerializer(genres, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def movie_genre(request, genre_id):
    if request.method == 'GET':
        genre = Genre.objects.get(id=genre_id)
        movies = Movie.objects.filter(genres=genre)
        serializer = MovieListSerializer(movies, many=True, context={'request': request})  # context 추가
        return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request,movie_pk):
    if request.method == 'GET':
        movie = Movie.objects.get(id=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def reviews(request, movie_pk):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=movie_pk)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie = Movie.objects.get(pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def movie_like(request, movie_pk, preference):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        # UserMovieLike 인스턴스를 조회하거나 생성
        user_like, created = UserMovieLike.objects.get_or_create(user=request.user, movie=movie)

        if created:
            if preference:  # 좋아요를 눌렀는데 새로 만들어진 경우
                user_like.like = 1
                user_like.save()
                # 영화 장르 기반으로 UserGenrePreference 업데이트
                for genre in movie.genres.all():
                    user_genre_pref, _ = UserGenrePreference.objects.get_or_create(
                        user=request.user, genre=genre
                    )
                    user_genre_pref.count += 1
                    user_genre_pref.save()
                isLike = True
                isDislike = False
            else:
                isLike = False
                isDislike = True
        else:
            if preference and user_like.like == 0:  # 싫어요에서 좋아요로 변경
                isLike = True
                isDislike = False
                user_like.like = 1
                user_like.save()
                # 장르 선호도 증가
                for genre in movie.genres.all():
                    user_genre_pref, _ = UserGenrePreference.objects.get_or_create(
                        user=request.user, genre=genre
                    )
                    user_genre_pref.count += 1
                    user_genre_pref.save()
            elif preference and user_like.like == 1:  # 좋아요 취소
                isLike = False
                isDislike = False
                user_like.delete()
                # 장르 선호도 감소
                for genre in movie.genres.all():
                    user_genre_pref = UserGenrePreference.objects.filter(
                        user=request.user, genre=genre
                    ).first()
                    if user_genre_pref:
                        user_genre_pref.count -= 1
                        if user_genre_pref.count == 0:  # count가 0이면 삭제
                            user_genre_pref.delete()
                        else:
                            user_genre_pref.save()
            elif not preference and user_like.like == 1:  # 좋아요에서 싫어요로 변경
                isLike = False
                isDislike = True
                user_like.like = 0
                user_like.save()
                # 장르 선호도 감소
                for genre in movie.genres.all():
                    user_genre_pref = UserGenrePreference.objects.filter(
                        user=request.user, genre=genre
                    ).first()
                    if user_genre_pref:
                        user_genre_pref.count -= 1
                        if user_genre_pref.count == 0:  # count가 0이면 삭제
                            user_genre_pref.delete()
                        else:
                            user_genre_pref.save()
            elif not preference and user_like.like == 0:  # 싫어요 취소
                user_like.delete()
                isLike = False
                isDislike = False

        return JsonResponse({'isLike': isLike, 'isDislike': isDislike, 'userId': request.user.id})

# 좋아요한 영화 출력
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_movies(request,user_id):
    # user = request.user
    temp_lst = UserMovieLike.objects.filter(user_id=user_id, like=1)
    print(temp_lst)
    liked_movie_ids = [
        liked_id.movie_id for liked_id in temp_lst
    ]
    # print(liked_movie_ids)
    print('liked_movie_ids 출력됨')
    liked_movies_info = [
        Movie.objects.get(pk=movie_id) for movie_id in liked_movie_ids
    ]
    # print(liked_movies_info)
    print('liked_movies_info_출력됨')

    serializer = MovieSerializer(liked_movies_info, many=True)
    return Response(serializer.data)

# 좋아요/싫어요 개수 출력
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_unlike_count(request):
    user = request.user
    like_unlike_count = UserMovieLike.objects.filter(user_id=user.pk).count()
    return JsonResponse({'like_unlike_count':like_unlike_count})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_create(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_reviews(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    reviews = Review.objects.filter(user=user).select_related('movie')
    serializer = ReviewWithMovieSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def make_recommendations(request):
    
    file_path = os.path.join(settings.BASE_DIR, 'movies', 'fixtures', 'sentiment.json')
    # Json 파일 불러오기
    with open(file_path, 'rb') as f:
        dummy_data = json.load(f)
    
    # User 데이터베이스 불러오기
    User = get_user_model()
    
    # 현재 로그인한 유저
    user = request.user
    
    # 좋아요, 싫어요 데이터 가져오기
    user_movie_likes = UserMovieLike.objects.all()
    db_data = [
        {
            'movie_id': like_entry.movie_id,
            'user_name': User.objects.get(id=like_entry.user_id).username,  # user_id를 user_name으로 변환
            'like': like_entry.like
        }
        for like_entry in user_movie_likes
    ]
    
    # 더미데이터랑 합치기
    combined = dummy_data + db_data
    
    # 추천
    df = pd.DataFrame(combined)
    id_dict = make_id(df)
    triplet = df2triplet(id_dict)
    result = lda(triplet, 5)
    
    recommendations = recommend(result, triplet, 10, user.username)
    
    return JsonResponse({'recommendations': recommendations})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, movie__pk=movie_pk)
    
    # 리뷰 작성자와 현재 사용자가 같은지 확인
    if review.user != request.user:
        return Response({'error': 'You do not have permission to delete this review.'}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    review.delete()
    return Response({'message': 'Review successfully deleted.'}, 
                    status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, movie__pk=movie_pk)
    
    # 리뷰 작성자와 현재 사용자가 같은지 확인
    if review.user != request.user:
        return Response({'error': 'You do not have permission to update this review.'}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userGenre_count(request):
    user = request.user
    genre_preferences = UserGenrePreference.objects.filter(user=user).order_by('-count')
    serializer = UserGenrePreferenceSerializer(genre_preferences, many=True)
    return Response(serializer.data)
    
    pass

# 챗봇
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'error': 'Message is required.'}, status=400)

            # GPT와 대화
            user = request.user
            gpt_response = chat_with_gpt(user, user_message)

            return JsonResponse({'response': gpt_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def initial_chat_view(request):
    user = request.user
    chat_history = ChatMessage.objects.filter(user=user).exists()  # 기록 확인

    if chat_history:
        # 이전 대화 기록이 있는 경우
        first_message = {
            "role": "도우미",
            "content": "다시 오셨네요! 무엇을 도와드릴까요?"
        }
    else:
        # 첫 대화인 경우
        first_message = {
            "role": "도우미",
            "content": "안녕하세요! 처음 만나 뵙게 되어 반가워요. \n저는 이 사이트의 챗봇이에요. 사이트 이용 방법이나 궁금한 점을 알려드릴게요. \n이곳에서는 좋아요를 누른 영화들을 바탕으로 취향에 맞는 영화를 추천받을 수 있어요. \n또한, 다른 사용자들이 좋아하는 영화와 리뷰를 확인해 볼 수도 있답니다. \n궁금한 점이 있다면 언제든 물어보세요! "
        }

    return JsonResponse(first_message)