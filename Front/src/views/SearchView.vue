<template>
  <div>
    <h1>검색결과</h1>
    <div class="container">
      <div class="row row-cols-1 row-cols-md-5 g-4">
        <div 
        class="col"
        v-if="store.searchMovieIds"
        v-for="movieId in store.searchMovieIds"
        :key="movieId">
          <SearchMovie :movieId="movieId"/>
        </div>          
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchMovie from '@/components/main/SearchMovie.vue'
import { useMovieStore } from '@/stores/counter';

const store = useMovieStore()
// console.log(store.searchMovieIds)

</script>

<style scoped>

</style>