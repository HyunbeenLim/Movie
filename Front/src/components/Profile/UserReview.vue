<template>
  <div>
    <h2 class="fw-bold">작성한 리뷰</h2>

    <!-- 로딩 중 표시 -->
    <div v-if="isLoading">
      <p>로딩 중...</p>
    </div>

    <!-- 리뷰 출력 -->
    <div v-else>
      <div v-for="(reviews, title) in groupedReviews" :key="title" class="movie-reviews">
        <RouterLink :to="{ name: 'moviedetail', params: { movieId: reviews[0].movie.id } }" class="title">
          <h3 class="me-3 mt-3">{{ title }}</h3>
        </RouterLink>

        <div v-for="review in reviews" :key="review.id" class="review-item d-flex">
          <div class="d-flex me-2">
            <p style="color:goldenrod;">{{ '★'.repeat(review.rating) }}</p>
            <p style="color: grey;">{{ '☆'.repeat(5 - review.rating) }}</p>
          </div>
          <div class="d-flex">
            <p class="me-3">{{ formatDate(review.created_at) }}</p>
            <p>{{ review.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { onMounted, computed, ref, watch } from 'vue';

// Props 정의
const props = defineProps({
  userId: {
    type: Number,
    required: true,
  },
});

// Store와 상태 변수
const store = useMovieStore();
const userReviews = ref([]); // 리뷰 데이터를 로컬 상태로 관리
const isLoading = ref(true); // 로딩 상태

// 영화 제목별로 리뷰를 그룹화
const groupedReviews = computed(() => {
  if (isLoading.value) return {}; // 로딩 중에는 빈 객체 반환

  const grouped = {};
  userReviews.value.forEach((review) => {
    const movieTitle = review.movie.title;
    if (!grouped[movieTitle]) {
      grouped[movieTitle] = [];
    }
    grouped[movieTitle].push(review);
  });

  // 각 영화의 리뷰를 평점 순으로 정렬 (내림차순)
  Object.keys(grouped).forEach((title) => {
    grouped[title].sort((a, b) => b.rating - a.rating);
  });

  return grouped;
});

// 날짜 포맷팅 함수
function formatDate(isoString) {
  if (!isoString) return '날짜 없음';
  const date = new Date(isoString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 데이터 로드 함수
async function fetchReviews() {
  isLoading.value = true; // 로딩 시작
  userReviews.value = []; // 기존 데이터 초기화
  try {
    await store.fetchUserReviews(props.userId); // 비동기 호출
    userReviews.value = store.userReviews; // 스토어에서 데이터 가져오기
  } catch (error) {
    console.error('리뷰 데이터를 가져오는 중 오류 발생:', error);
  } finally {
    isLoading.value = false; // 로딩 종료
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(fetchReviews);

// userId 변경 시 데이터 다시 로드
watch(() => props.userId, fetchReviews);
</script>

<style scoped>
.title {
  width: 350px;          /* 고정된 너비 설정 */
  overflow: hidden;      /* 넘치는 텍스트 숨김 */
  white-space: nowrap;   /* 텍스트 줄바꿈 방지 */
  text-overflow: ellipsis;  /* 넘치는 텍스트를 ...으로 표시 */
  text-decoration: none;    /* 링크 밑줄 제거 */
  color: black;           /* 부모 요소의 색상 상속 */
  transition: all 0.3s ease;  /* 투명도 변화에 애니메이션 효과 */
  cursor: pointer;          /* 마우스 오버시 포인터 커서 표시 */
  font-weight: bold;
}

.title:hover {
  color: #666;          /* 색상이 밝아지는 효과 */
  transform: translateX(5px);  /* 살짝 오른쪽으로 이동 */
  opacity: 0.8;        /* 투명도 변화 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);  /* 텍스트에 그림자 효과 */
}
</style>
