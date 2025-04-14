<template>
  <div class="container d-flex ps-0">
    <h2 class="fw-bold">{{ store.userNickname }}</h2>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router';

const store = useMovieStore()
const userName = computed(() => {
  console.log('userName:', store.userName)
  console.log('useremail:', store.userEmail)
  return store.userName
})

// onMounted(() => {
//   store.fetchLikedMovies()
// })
</script>

<style scoped>
.icon {
  text-decoration: none;    /* 링크 밑줄 제거 */
  color: rgb(160, 160, 160);           /* 부모 요소의 색상 상속 */
  transition: opacity 0.3s ease;  /* 투명도 변화에 애니메이션 효과 */
  cursor: pointer;          /* 마우스 오버시 포인터 커서 표시 */
}
</style>