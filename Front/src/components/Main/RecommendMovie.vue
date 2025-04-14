<template>
  <div class="container-fluid px-10 mb-4">
    <div class="movie-carousel">
      <h2 class="mb-0 fw-bold">{{ store.userNickname }}님과 비슷한 취향 영화</h2>
      <div class="movie-container" ref="scrollContainer">
        <div class="movie-card" v-for="movie in recommendationMovies" :key="movie.id">
          <div class="card h-100">
            <RouterLink :to="{name:'moviedetail', params:{movieId: movie.id}}">
              <div class="card-img-wrapper position-relative" style="padding-top: 133.33%;">
                <img 
                  :src="`https://image.tmdb.org/t/p/w200/${movie.poster}`" 
                  class="card-img-top position-absolute top-0 start-0 w-100 h-100" 
                  :alt="movie.title"
                >
                <div class="overlay">
                  <i 
                    @click.prevent="store.movieLike(movie.id, 1)"
                    :class="[movie.is_liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart']"
                    class="like-icon"
                  ></i>
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
      </div>
    </div>
  </div>
</template>
<script setup>
import { useMovieStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import { ref, onMounted, onUnmounted } from 'vue';

defineProps({
  recommendationMovies:Object
})

const store = useMovieStore()

const scrollContainer = ref(null);

const handleWheel = (event) => {
  event.preventDefault();

  const scrollSpeed = 3; // 스크롤 속도 조정
  if (scrollContainer.value) {
    scrollContainer.value.scrollLeft += event.deltaY * scrollSpeed;
  }
};

onMounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('wheel', handleWheel, { passive: false });
  }
});

onUnmounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('wheel', handleWheel);
  }
});

</script>

<style scoped>
.carousel-button {
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 10%;
  padding: 10px;
  cursor: pointer;
}

.movie-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 1rem 0;
  cursor: grab; /* 마우스 커서를 grab으로 변경 */
  -webkit-overflow-scrolling: touch; /* iOS 스크롤 지원 */
  scrollbar-width: none; /* Firefox에서 스크롤바 숨기기 */
}

/* Chrome, Safari, Opera에서 스크롤바 숨기기 */
.movie-container::-webkit-scrollbar {
  display: none;
}

/* 드래그 중일 때 커서 변경 */
.movie-container:active {
  cursor: grabbing;
}

.container-fluid {
  max-width: 1800px;
}

.card-img-wrapper {
  overflow: hidden;
}

.card {
  border-radius: 12px; 
  overflow: hidden;
  /* 카드 음영 효과 */
  box-shadow: 0 4px 8px rgba(0.5, 0.5, 0.5, 0.5);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Darker shadow on hover */
}

.movie-card {
  flex: 0 0 auto;
  width: calc(20% - 0.5rem); /* 5개 카드 표시 */
}

/* 반응형 처리 */
@media (max-width: 1200px) {
  .movie-card {
    width: calc(25% - 1rem); /* 4개 카드 */
  }
}

@media (max-width: 992px) {
  .movie-card {
    width: calc(33.333% - 1rem); /* 3개 카드 */
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: calc(50% - 1rem); /* 2개 카드 */
  }
}

/* 영화 이미지 */
.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: 12px 12px 0 0;
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
  border-radius: 12px;
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
</style>