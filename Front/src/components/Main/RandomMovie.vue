<template>
  <div class="d-flex gap-2 mb-3">
    <div class="slot-machine-container">
      <!-- 슬롯 머신 -->
      <div v-if="!isHidden && !isInitial" class="slot-machine">
        <div class="reel" v-for="(reel, index) in reels" :key="index" 
             :style="{ transform: `translateY(${reel.position}px)` }">
          <div class="slot-item" v-for="(symbol, i) in symbols" :key="i">
            <h2>{{ symbol }}</h2>
          </div>
        </div>
      </div>
      <!-- 초기 장르(로맨스) 또는 선택된 장르 -->
       <div class="genre-box">
        <!-- <h2> " </h2> -->
        <h2 class="mb-0 selected-genre fw-bold" v-if="showGenre">" {{ isInitial ? "로맨스" : genreName }} "</h2>
        <!-- <h2> " </h2> -->
       </div>
    </div>
    <h2 class="genre-text fw-bold">장르는 어때요?</h2>
    <button @click="spinReels" type="button" class="btn btn-outline-secondary btn-lg">
      <i class="fa-solid fa-shuffle fa-lg"></i>
    </button>
  </div>

  <div class="container-fluid px-10">
    <!-- 영화 정보 -->
    <div class="movie-carousel">
      <div class="movie-container" ref="scrollContainer">
        <div class="movie-card" v-for="randommovie in randomTenMovies" :key="randommovie.id">
          <div class="card h-100">
            <RouterLink :to="{name:'moviedetail', params:{movieId: randommovie.id}}">
              <div class="card-img-wrapper position-relative" style="padding-top: 133.33%;">
                <img 
                  :src="`https://image.tmdb.org/t/p/w200/${randommovie.poster}`" 
                  class="card-img-top position-absolute top-0 start-0 w-100 h-100" 
                  :alt="randommovie.title"
                >
                <div class="overlay">
                  <i 
                    @click.prevent="store.movieLike(randommovie.id, 1)"
                    :class="[randommovie.is_liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart']"
                    class="like-icon"
                  ></i>
                  <i 
                    @click.prevent="store.movieLike(randommovie.id, 0)"
                    :class="[randommovie.is_disliked ? 'fa-solid fa-thumbs-down' : 'fa-regular fa-thumbs-down']"
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
import { RouterLink } from 'vue-router';
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useMovieStore } from '@/stores/counter';
const props = defineProps({
  randomMovies: Array,
  genreName: String
});
const store = useMovieStore();
// 랜덤으로 10개 영화 뽑기 
const randomTenMovies = computed(() => {
  const shuffled = [...props.randomMovies].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, 10);
});

const showGenre = ref(true);

const emit = defineEmits(["genreReset"]);

const symbols = ["모험", "판타지", "애니메이션", "드라마", "공포", "액션", "코미디", "역사", "서부", 
                 "스릴러", "범죄", "SF", "미스터리", "음악", "로맨스", "가족", "전쟁", "TV 영화", "다큐멘터리"]; // 슬롯 심볼

const reels = ref([
  { position: 0 }, // 첫 번째 릴
  { position: 0 }, // 두 번째 릴
  { position: 0 }, // 세 번째 릴
]);
const isHidden = ref(false); // 슬롯 머신 숨김 상태
const isInitial = ref(true); // 초기 상태 여부

function spinReels() {
  showGenre.value = false;
  isInitial.value = false;
  isHidden.value = false;  // 이 세 줄을 함수 맨 앞으로 이동

  // 즉시 슬롯 머신 위치 초기화
  reels.value.forEach((reel, index) => {
    reel.position = 0;  // 초기 위치로 즉시 설정
  });

  // 약간의 지연 후 애니메이션 시작
  setTimeout(() => {
    const randomStops = [
      Math.floor(Math.random() * symbols.length),
      Math.floor(Math.random() * symbols.length),
      Math.floor(Math.random() * symbols.length),
    ];

    reels.value.forEach((reel, index) => {
      const slotHeight = 100;
      const totalItems = symbols.length;
      const totalHeight = totalItems * slotHeight;
      const targetPosition = -(randomStops[index] * slotHeight);
      const extraSpins = totalHeight * 3;

      reel.position = targetPosition - extraSpins;

      setTimeout(() => {
        reel.position = targetPosition;
      }, 1000);
    });
  }, 50);  // 아주 짧은 지연 추가

  setTimeout(() => {
    isHidden.value = true;
    emit("genreReset");
    setTimeout(() => {
      showGenre.value = true;
    }, 0);
  }, 1500);
}

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
  box-shadow: 0 4px 8px rgba(0.5, 0.5, 0.5, 0.5);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.movie-card {
  flex: 0 0 auto;
  width: calc(20% - 0.5rem);
}

@media (max-width: 1200px) {
  .movie-card {
    width: calc(25% - 1rem);
  }
}

@media (max-width: 992px) {
  .movie-card {
    width: calc(33.333% - 1rem);
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: calc(50% - 1rem);
  }
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
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

/* 슬롯 머신 관련 스타일 */
.d-flex {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 15px;
}

.slot-machine-container {
  position: relative;
  height: 40px;
  width: px;
}

.genre-text {
  margin: 0;
}

.spin-button {
  margin: 0;
  cursor: pointer;
}

.slot-machine {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.reel {
  display: flex;
  flex-direction: column;
  transform: translateY(0);
  transition: transform 3s cubic-bezier(0.23, 1, 0.32, 1);
}

.slot-item {
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 슬롯 실행 버튼 테두리 제거 */
.btn-outline-secondary {
  border: none;
}

.genre-box {
  width: 300px;  /* 고정된 너비 */
  margin: 0;
  height: 30px;  /* 고정된 높이 */
  display: flex;
  justify-content: center;  /* 가로 중앙 정렬 */
  align-items: center;     /* 세로 중앙 정렬 */
}

.selected-genre {
  width: 300px;
  margin-top: 10px;
  text-align: center;
  white-space: nowrap;    /* 텍스트 줄바꿈 방지 */
  overflow: hidden;       /* 넘치는 텍스트 숨김 */
  text-overflow: ellipsis;
  opacity: 0;
  animation: fadeIn 0.5s ease-in forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>