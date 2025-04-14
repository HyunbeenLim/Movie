<template>
  <div class="container" v-if="store.userData">
    <div class="container d-flex ps-0">
    <h2 class="fw-bold">{{ store.userData.nickname }}님의 프로필</h2>
  </div>
    <!-- <h3>유저 ID: {{ userId }}</h3> -->
    <!-- <h3>이메일: {{ store.userData.email }}</h3> -->



    <!-- 사용자가 좋아하는 영화 목록 -->
    <UserLikeMovie v-if="store.likedMovies"
    :like-movies="store.likedMovies" />

    <!-- 사용자가 작성한 리뷰 -->
    <UserReview v-if="userId"
    :user-id="Number(userId)" />
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

// 하위 컴포넌트 가져오기
import UserInfo from '@/components/Profile/UserInfo.vue';
import UserLikeMovie from '@/components/Profile/UserLikeMovie.vue';
import UserReview from '@/components/Profile/UserReview.vue';

// Vue Router로부터 현재 경로 정보 가져오기
const route = useRoute();
const userId = ref(route.params.userId);
const store = useMovieStore();

// userId가 변경될 때마다 사용자 정보를 갱신
watch(() => route.params.userId, async (newId) => {
  if (newId) {
    await store.fetchOtherInfo(newId); // API 호출로 사용자 정보 가져오기
  }
});

// 컴포넌트가 마운트될 때 초기 사용자 정보 로드
onMounted(async () => {
  if (route.params.userId) {
    await store.fetchOtherInfo(route.params.userId);
    await store.fetchLikedMovies(route.params.userId)
  }
});
</script>

<style scoped>
.container {
  padding: 20px;
}
h1 {
  font-size: 24px;
  margin-bottom: 10px;
}
h3 {
  margin: 5px 0;
}
</style>