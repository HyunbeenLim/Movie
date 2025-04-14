<template>
  <div class="container-fluid px-0 mb-5">
    <h3 class="mb-3">좋아요 누른 영화</h3>
    <div v-if="likeMovies.length > 0">
      <div class="row g-4">
        <div class="col-6 col-md-4 col-lg-3 col-xl" v-for="likemovie in likeMovies" :key="likemovie.id">
          <div class="card h-100">
            <div class="card-img-wrapper position-relative" style="padding-top: 133.33%;">
              <RouterLink :to="{name:'moviedetail', params:{movieId: likemovie.id}}">
                <img :src="`https://image.tmdb.org/t/p/w200/${likemovie.poster}`" 
                    class="card-img-top position-absolute top-0 start-0 w-100 h-100" 
                    :alt="likemovie.title">
                    <div class="overlay">
                      <i @click.prevent="store.movieLike(likemovie.id, 1)"
                      :class="[likemovie.is_liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart']"
                      class="like-icon">
                    </i>
                    <i @click.prevent="store.movieLike(likemovie.id, 0)"
                    :class="[likemovie.is_disliked ? 'fa-solid fa-thumbs-down' : 'fa-regular fa-thumbs-down']"
                    class="dislike-icon">
                  </i>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <h3>아직 좋아요를 누른 영화가 없어요</h3>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';

const store = useMovieStore()

defineProps({
  likeMovies:Object
})
</script>

<style scoped>
.container-fluid {
  max-width: 1800px;
}

.card-img-wrapper {
  overflow: hidden;
}

.card {
  border-radius: 12px; 
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0.5, 0.5, 0.5, 0.5);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: 12px 12px 0 0;
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

/* 반응형 처리 */
@media (min-width: 1200px) {
  .col-xl {
    flex: 0 0 20%;  /* 5개 카드를 위한 너비 설정 */
    max-width: 20%;
  }
}

@media (max-width: 1199px) {
  .col-lg-3 {
    flex: 0 0 25%;  /* 4개 카드 */
    max-width: 25%;
  }
}

@media (max-width: 991px) {
  .col-md-4 {
    flex: 0 0 33.333%;  /* 3개 카드 */
    max-width: 33.333%;
  }
}

@media (max-width: 767px) {
  .col-6 {
    flex: 0 0 50%;  /* 2개 카드 */
    max-width: 50%;
  }
}
</style>