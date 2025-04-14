<template>
  <div v-if="movie">
    <div class="card h-100">
      <RouterLink :to="{name:'moviedetail', params:{movieId: movie.id}}">
        <!-- 이미지 컨테이너 -->
        <div class="card-img-wrapper position-relative">
          <!-- 영화 이미지 -->
          <img :src="`https://image.tmdb.org/t/p/w200/${movie.poster}`" class="card-img-top" :alt="movie.title">

          <!-- 오버레이 -->
          <div class="overlay">
            <!-- 좋아요 아이콘 -->
            <i 
              @click.prevent="store.movieLike(movie.id, 1)"
              :class="[movie.is_liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart']"
              class="like-icon"
            ></i>

            <!-- 싫어요 아이콘 -->
            <i 
              @click.prevent="store.movieLike(movie.id, 0)"
              :class="[movie.is_disliked ? 'fa-solid fa-thumbs-down' : 'fa-regular fa-thumbs-down']"
              class="dislike-icon"
            ></i>
          </div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useMovieStore } from '@/stores/counter';

const store = useMovieStore()
const props = defineProps({
              movieId:Number,
              })
const movie = store.getMovieDetail(props.movieId) || {}

</script>

<style scoped>
.card-img-wrapper {
  position: relative;
  height: 300px;
  overflow: hidden;
}

/* 영화 이미지 */
.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* 오버레이 (초기 상태: 숨김) */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 검정 음영 */
  opacity: 0; /* 기본적으로 투명 */
  transition: opacity 0.3s ease; /* 부드러운 전환 효과 */
}

/* 마우스 오버 시 오버레이 표시 */
.card-img-wrapper:hover .overlay {
  opacity: 1; /* 오버레이가 나타남 */
}

/* 좋아요 아이콘 (왼쪽 상단) */
.like-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  color: white; /* 흰색 아이콘 */
  font-size: 1.5rem;
  cursor: pointer;
}

/* 싫어요 아이콘 (오른쪽 상단) */
.dislike-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  color: white; /* 흰색 아이콘 */
  font-size: 1.5rem;
  cursor: pointer;
}

/* 카드 제목 스타일 */
.card-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>