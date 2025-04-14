<template>
  <div class="container">
    <div class="mb-3">
      <LatestMovie :sorted-movies="sortedMovies"/>
      <LikeGenreMovie 
      v-if="store.isLogin && store.topGenreId && likedGenreMovies.length > 0"
      :liked-genre-movies="likedGenreMovies"
      />
      <RecommendMovie 
        v-if="store.isLogin && store.like_unlike_total >= 10 && recommendationMovies.length > 0"
        :recommendation-movies="recommendationMovies"
      />
      <RandomMovie 
        v-if="randomMovies"
        :random-movies="randomMovies" 
        :genre-name="genreName"
        @genreReset="selectNewGenre" 
      />
    </div>
  </div>
</template>

<script setup>
import LatestMovie from '@/components/Main/LatestMovie.vue';
import LikeGenreMovie from '@/components/Main/LikeGenreMovie.vue';
import RecommendMovie from '@/components/Main/RecommendMovie.vue';
import RandomMovie from '@/components/Main/RandomMovie.vue';

import { useMovieStore } from '@/stores/counter';
import { onMounted, computed, ref, watch } from 'vue';

const store = useMovieStore();

// 최신순으로 정렬한 영화 데이터
const sortedMovies = computed(() => {
  return [...store.movies].sort((a, b) => {
    return new Date(b.released_date) - new Date(a.released_date);
  });
});
// 좋아요한 장르 영화 데이터
const likedGenreMovies = computed(() => {
  if (!store.topGenreId || store.movies?.length == 0) return [];
  // 선택된 장르에 속한 영화 필터링
  const filteredMovies = store.movies.filter((movie) =>
    movie.genres.some((genre) => genre.id === store.topGenreId)
  );
  console.log('좋아요한 장르 영화 필터링 성공')
  // 랜덤으로 최대 10개의 영화 선택
  return filteredMovies.sort(() => Math.random() - Math.random()).slice(0, 10);
});

// 기본값을 "로맨스"로 설정
const selectedGenreId = ref(10749) 
const genreName = ref("로맨스");

// 랜덤 장르 선택 및 영화 업데이트 함수
function selectNewGenre() {
  const genres = store.genres;
  if (genres.length > 0) {
    const randomIndex = Math.floor(Math.random() * genres.length);
    genreName.value = genres[randomIndex].genre;
    selectedGenreId.value = genres[randomIndex].id;
    console.log(selectedGenreId.value)
    };
  }
// 랜덤 추출한 영화 데이터 저장
const randomMovies = computed(() => {
  if(selectedGenreId.value == 10749){
    console.log('로맨스 장르 찿기시작')
    return store.movies?.filter(movie => {
      const genres = movie.genres
      return genres.some(genre => genre.id == 10749)
  }) 
  } else {
    return store.movies?.filter(movie => {
      const genres = movie.genres
      return genres.some(genre => genre.id == selectedGenreId.value)
  })
  }
  }
)

// 협업 필터링 영화 데이터 저장
const recommendationMovies = computed(() => {
  if(store.recommendationsIds){
    return store.recommendationsIds.map(id => store.movies?.find(movie => movie.id === id));
  } else {return []}
  })
  

// onMounted에서 기본 장르와 영화를 설정
onMounted(async () => {
  try {
    // 영화 데이터와 장르 데이터를 비동기로 가져옴
    await store.getMovies();
    await store.getGenres();
    await store.getLikedGenreCount();
    await store.getRecommendations();
    
  } catch (error) {
    console.error("데이터를 가져오는 중 오류 발생:", error);
  }
});

// 로그인/로그아웃 이벤트 감지 및 처리
watch(
  () => store.isLogin,
  async (isLogin) => {
    if (isLogin) {
      console.log('유저 로그인 상태 변경됨: 로그인');
      await store.getMovies(); // 로그인 후 영화 목록 갱신
    } else {
      console.log('유저 로그인 상태 변경됨: 로그아웃');
      await store.getMovies(); // 로그아웃 후 영화 목록 초기화
    }
  }
);
</script>

<style>
</style>