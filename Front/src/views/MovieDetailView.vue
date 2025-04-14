<template>
  <div class="movie-detail">
    <!-- YouTube 배경 비디오 -->
    <div class="video-background" v-if="movie">
      <iframe 
      :src="`https://www.youtube.com/embed/${movie?.youtube_key}?autoplay=1&controls=0&showinfo=0&mute=1&loop=1&playlist=${movie?.youtube_key}`"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen>
    </iframe>
    <div class="gradient-overlay"></div> <!--  불투명하고 어두운 부분을 담당 -->>
  </div>
  
    <!-- 뒤로가기 버튼 -->
    <div class="back-button">
      <i @click="goBack" class="fa-solid fa-arrow-left fa-2xl glow-effect"></i>
    </div>
    
    <!-- 영화 정보 -->
    <div class="content-container w-full md:w-4/5 lg:w-3/5">
      <div class="content m-0custom-margin" v-if="movie">
        <div class="d-flex">
          <h2 class="fw-bold">{{ movie.title }}</h2>
        </div>
        <div class="d-flex" style="gap: 1rem; color: lightgrey;">
          <p>영화 개봉일 : {{ movie.released_date }}</p>
          <p>평균 평점 : {{ movie.avg_rating }}</p>
          <p>언어 : {{ movie.language }}</p>
        </div>
        <div class="genres">
          <h5 v-for="genre in movie.genres" :key="genre.id" class="btn btn-outline-light"># {{ genre.genre }}</h5>
        </div>
        <div>
          <p class="fw-light">{{ movie.overview }}</p>
        </div>
  
        <hr>

        <h3 class="fw-semibold">한줄평</h3>

        <!-- 리뷰 작성 폼 -->
        <form v-if="store.isLogin" @submit.prevent="isEditing ? updateReview() : submitReview()" 
              class="mt-4" style="background-color: transparent;">
          <div class="form-group mb-3 d-flex">
            <select v-model="newReview.rating" 
                    :class="{'glow-effect': errors.rating}"
                    class="form-control me-3 text-light custom-select" 
                    style="background-color: transparent; color: white;">
              <option value="" disabled selected>별점을 선택해주세요</option>
              <option value="1">★</option>
              <option value="2">★★</option>
              <option value="3">★★★</option>
              <option value="4">★★★★</option>
              <option value="5">★★★★★</option>
            </select>
            <div class="d-flex">
              <button type="submit" class="btn btn-outline-light btn-custom">{{ isEditing ? '수정' : '제출' }}</button>
              <button v-if="isEditing" @click="cancelEdit" class="btn btn-outline-light btn-custom ms-2">취소</button>
            </div>
          </div>
          <div class="form-group mb-3">
            <textarea v-model="newReview.content" 
                      :class="{'glow-effect': errors.content}"
                      placeholder="리뷰를 작성해주세요" 
                      class="form-control" 
                      rows="2" 
                      style="background-color: transparent; color: white;">
            </textarea>
          </div>
        </form>
          
        <!-- 이전에 작성된 리뷰 출력 -->
        <div>
          <div v-for="review in store.reviews" :key="review.id">
            <div class="d-flex" style="gap: 1rem;">
              <div class="d-flex me-3">
                <RouterLink 
                  v-if="review.user === store.userId" 
                  :to="{ name: 'profile'}"
                >
                  <h5 class="me-3 username">{{ review.username }}</h5>
                </RouterLink>
                <RouterLink 
                  v-else 
                  :to="{ name: 'otherprofile', params: { userId: review.user }}"
                >
                  <h5 class="me-3 username">{{ review.username }}</h5>
                </RouterLink>
                <p style="color:goldenrod;">{{ '★'.repeat(review.rating) }}</p><p style="color: grey;">{{ '☆'.repeat(5-review.rating) }}</p>
              </div>
              <div>
                <p>{{ review.content }}</p>
              </div>
              <div class="ms-auto">
                <button class="btn btn-outline-secondary btn-sm me-2" v-if="store.isLogin && review.user === store.userId" @click="editReview(review)">Edit</button>
                <button class="btn btn-outline-secondary btn-sm" v-if="store.isLogin && review.user === store.userId" @click="deleteReview(review.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>


<script setup>
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { RouterLink } from 'vue-router';
const router = useRouter();

const userId = ref(null)
const movie = ref(null)
const route = useRoute()
const store = useMovieStore()
const movieId = route.params.movieId
const newReview = ref({ content: '', rating: '' })
const isEditing = ref(false)
const editingReviewId = ref(null)

const errors = ref({ rating: false, content: false });

const submitReview = async () => {

  errors.value = { rating: false, content: false };
  if (!newReview.value.rating) errors.value.rating = true;
  if (!newReview.value.content.trim()) errors.value.content = true;
  
  if (errors.value.rating || errors.value.content) {
    return; // 유효성 검사 실패 시 제출하지 않음
  }

  try {
    await store.submitReview(movieId, newReview.value)
    newReview.value = { content: '', rating: '' }
    await store.fetchReviews(movieId)
  } catch (error) {
    console.error('Error submitting review:', error)
  }
}

const deleteReview = async (reviewId) => {
  try {
    await store.deleteReview(movieId, reviewId)
    await store.fetchReviews(movieId)
  } catch (error) {
    console.error('Error deleting review:', error)
  }
}

const editReview = (review) => {
  isEditing.value = true
  editingReviewId.value = review.id
  newReview.value = { content: review.content, rating: review.rating.toString() }
}

const updateReview = async () => {
  try {
    await store.updateReview(movieId, editingReviewId.value, newReview.value)
    isEditing.value = false
    editingReviewId.value = null
    newReview.value = { content: '', rating: '' }
    await store.fetchReviews(movieId)
  } catch (error) {
    console.error('Error updating review:', error)
  }
}

const cancelEdit = () => {
  isEditing.value = false
  editingReviewId.value = null
  newReview.value = { content: '', rating: null }
}

const goBack = () => {
  router.go(-1)
}

const goProfile = () => {

}

onMounted(async () => {
  //window.scrollTo(0, 0) // 페이지 로드시 최상단에서 시작
  movie.value = store.getMovieDetail(movieId)
  await store.fetchReviews(movieId)
})

</script>

<style scoped>
.movie-detail {
  position: relative;
  min-height: calc(100vh - 130px);
  color: white;
  overflow: hidden;
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.video-background iframe {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100vw;
  height: 100vh;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.5) 50%,
    rgba(0, 0, 0, 0.8) 80%
  );
}

.content-container {
  width: 80%; /* Adjusted to use 60% of the available width */
  margin: auto;
}

.content {
  position: relative;
  padding: 2rem 2rem;
  max-width: 800px;
  margin-left: auto;
  /* margin-top: 5%; */
  height: calc(100vh - 130px); /* 추가: 상단 여백을 고려한 높이 */
  overflow-y: auto; /* 추가: 세로 스크롤 허용 */
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.overview {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.genres {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.genre-tag {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.movie-info {
  font-size: 1.1rem;
}

.label {
  color: #ccc;
  margin-right: 0.5rem;
}

/* 뒤로가기 버튼 관련 스타일 */
.back-button i {
  transition: box-shadow 0.3s ease, color 0.3s ease;
  cursor: grab; 
}

.back-button i:hover {
  color: #525252; /* 선택한 표시를 위해 색상 변경 */
  box-shadow: 0 0 50px rgba(255, 255, 255, 0.8); /* 빛나는 효과 */
}

.back-button {
  position: fixed;
  top: 150px;
  left: 50px;
  z-index: 10;
}

.custom-margin {
  margin-top: 130px; /* Adjust this value as needed */
}

html, body {
  overflow: hidden;
}

/* 별점 선택 드롭다운 관련*/
.custom-select {
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
  color: #fff; /* White text */
}

.custom-select option {
  background-color: #000; /* Black background for options */
  color: #fff; /* White text for options */
}

/* 리뷰 작성부분 글씨 */
textarea::placeholder {
  color: rgba(255, 255, 255, 0.7); /* 흰색에 약간의 투명도 */
}

/* 완전하지 않은 상태로 리뷰 제출하려는 경우 빛나는 효과 */
.glow-effect {
  box-shadow: 0 0 5px #f46c79, 0 0 10px #f46c79, 0 0 15px #f46c79; 
  animation: glow 1.2s ease-in-out infinite alternate; /* 움직이는 효과 */
}

@keyframes glow {
  from {
    box-shadow: 0 0 5px #f46c79, 0 0 10px #f46c79, 0 0 15px #f46c79; /* Initial state */
  }
  to {
    box-shadow: 0 0 7px #f46c79, 0 0 12px #f46c79, 0 0 17px #f46c79; /* Final state with larger glow */
    transform: scale(1.02); /* Slightly scale up for a pulsing effect */
  }
}

/* username 너비 고정 */
.username {
  width: 150px; /* Fixed width */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis; /* Adds ellipsis (...) for overflow text */
  text-decoration: none;    /* 링크 밑줄 제거 */
  color: white;           /* 부모 요소의 색상 상속 */
  transition: all 0.3s ease;  /* 투명도 변화에 애니메이션 효과 */
  cursor: pointer;          /* 마우스 오버시 포인터 커서 표시 */
}

.username:hover {
  color: #666;          /* 색상이 밝아지는 효과 */
  transform: translateX(5px);  /* 살짝 오른쪽으로 이동 */
  opacity: 0.8;        /* 투명도 변화 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);  /* 텍스트에 그림자 효과 */
}

/* 제출 버튼 관련 */
.btn-custom {
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center;    /* 세로 중앙 정렬 */
  width: 110px;           /* 원하는 너비 설정 */
  height: 40px;           /* 원하는 높이 설정 */
  line-height: normal;    /* line-height를 normal로 설정 */
}

</style>