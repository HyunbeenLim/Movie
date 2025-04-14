<template>
  <div class="container">
    <UserInfo />
    <UserLikeMovie 
    v-if="likeMovies"
    :like-movies="likeMovies"
    />
    <UserReview v-if="store.userId"
    :user-id="store.userId"/>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { RouterLink } from 'vue-router';

import UserInfo from '@/components/Profile/UserInfo.vue';
import UserLikeMovie from '@/components/Profile/UserLikeMovie.vue';
import UserReview from '@/components/Profile/UserReview.vue';
const route = useRoute()
const userId = ref(route.params.userId)
const store = useMovieStore()
const likeMovies = computed(() => {
  const movies = store.movies?.filter(movie => movie.is_liked == true)
  console.log(movies)
  return movies
})

</script>

<style scoped>

</style>