<template>
  <div class="container">
    <form class="my-0" action="">
      <label for=""></label>
      <select class="form-select form-select-lg mb-3" v-model="selectedGenre" @change="changeGenre">
        <option value="장르선택"> 장르를 선택해주세요 </option>  
        <option v-for="genre in store.genres" :value="genre.id" :key="genre.id">
          {{ genre.genre }}
        </option>
      </select>
    </form>

    <!-- 영화 리스트 -->
    <div v-if="paginatedMovies.length" class="movie-container mb-5">
      <div class="movie-card" v-for="movie in paginatedMovies" :key="movie.id">
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
    </div>

    <!-- 페이징 버튼 -->
    <div v-if="totalPages > 1" class="pagination-controls">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1"
        class="btn btn-outline-secondary me-4"
      >
      <i class="fa-solid fa-backward"></i>
      </button>
      <p>{{ currentPage }} / {{ totalPages }}</p>
      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages"
        class="btn btn-outline-secondary ms-4"
      >
      <i class="fa-solid fa-forward"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

const store = useMovieStore();
const selectedMovies = ref(store.movies);

// 페이징 상태
const currentPage = ref(1); // 현재 페이지
const moviesPerPage = ref(30); // 한 페이지에 표시할 영화 수

// 선택된 장르 관리
const selectedGenre = ref('장르선택');

// 선택된 장르에 따라 영화 필터링
const changeGenre = async function() {
  console.log(selectedGenre.value);
  selectedMovies.value = store.getGenreMovies(Number(selectedGenre.value));
};

// 페이징된 영화 데이터 계산
const paginatedMovies = computed(() => {
  const startIndex = (currentPage.value - 1) * moviesPerPage.value;
  const endIndex = startIndex + moviesPerPage.value;
  return selectedMovies.value.slice(startIndex, endIndex);
});

// 총 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(selectedMovies.value.length / moviesPerPage.value);
});

// 이전/다음 페이지 이동 함수
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

onMounted(async () => {
  await store.getMovies();
  await store.getGenres();
});
</script>

<style scoped>
.movie-container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap; /* 카드가 화면 크기에 따라 줄바꿈 */
}

.movie-card {
  flex: 0 0 calc(20% - 1rem); /* 기본 카드 크기 (5개 표시) */
}

.card-img-wrapper {
  position: relative;
  width: 100%;
  height: 300px; /* 모든 카드의 높이를 동일하게 설정 */
  overflow: hidden;
  border-radius: 12px; /* 카드 전체 둥글게 */
}

.card-img-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지 크기를 맞추기 위해 추가 */
  border-radius: inherit; /* 부모의 border-radius 상속 */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.card-img-wrapper:hover .overlay {
  opacity: 1;
}

.like-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.dislike-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  color: white; /* 흰색 아이콘 */
  font-size: 1.5rem;
  cursor: pointer;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: stretch; 
}

.btn.btn-outline-secondary {
  border: none; /* 테두리 제거 */
}

.movie-card {
  flex: 0 0 calc(20% - 1rem); /* 기본 카드 크기 (한 줄에 5개) */
}

/* 반응형 처리 */
@media (max-width: 1200px) {
  .movie-card {
    flex: 0 0 calc(25% - 1rem); /* 한 줄에 4개 */
  }
}

@media (max-width: 992px) {
  .movie-card {
    flex: 0 0 calc(33.333% - 1rem); /* 한 줄에 3개 */
  }
}

@media (max-width: 768px) {
  .movie-card {
    flex: 0 0 calc(50% - 1rem); /* 한 줄에 두 개 */
  }
}

</style>