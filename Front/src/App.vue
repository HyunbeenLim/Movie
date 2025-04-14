<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary px-4 fixed-top custom-nav">
    <div class="container-fluid">

      <RouterLink :to="{name:'home'}" class="d-flex align-items-center">
        <img src="@/assets/Logo.jpg" alt="Logo" class="img-fluid ms-0 me-2" style="width: 150px; height: auto;">
      </RouterLink>

      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" 
              aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"> </span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- 작은 화면에서만 보이는 검색폼 -->
        <form class="d-flex align-item-center search-form d-lg-none mb-3 mx-auto" role="search">
          <input v-model="searchQuery" class="form-control form-control-lg me-2 py-2" type="search" placeholder="영화를 검색해보세요" aria-label="Search">
          <button @click.prevent="getSearchMovie" class="btn btn-lg py-2" type="submit">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </form>

        <ul class="navbar-nav d-flex">
          <li class="nav-item me-4">
            <RouterLink :to="{name:'home'}" class="nav-link">
              <h3 class="mb-0 fw-bold">Main</h3>
            </RouterLink> 
          </li>
          <li class="nav-item me-4">
            <RouterLink :to="{name:'movie'}" class="nav-link">
              <h3 class="mb-0 fw-bold">Movie</h3>
            </RouterLink> 
          </li>
          <!-- 챗봇 -->
          <li class="nav-item me-4" v-if="store.isLogin" @click="toggleChatbot">
            <div class="nav-link">
              <h3 class="temp mb-0 fw-bold">ChatBot</h3>
            </div>
          </li>
        </ul>

        <!-- 큰 화면에서만 보이는 검색폼 -->
        <form class="d-none d-lg-flex search-form ms-auto me-3" role="search">
          <input v-model="searchQuery" class="form-control form-control-lg me-2 py-2" type="search" placeholder="영화를 검색해보세요" aria-label="Search">
          <button @click.prevent="getSearchMovie" class="btn btn-lg py-2" type="submit">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </form>

        <!-- 큰 화면에서만 보이는 프로필 아이콘 -->
        <ul class="navbar-nav d-none d-lg-flex">
          <li class="nav-item dropdown">
            <a class="nav-link" href="#" id="profileDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <RouterLink :to="{ name: 'profile'}">
                <img src="@/assets/Profile.png" alt="Profile" width="60" height="60">
              </RouterLink> 
            </a>
            <ul class="dropdown-menu custom-dropdown" aria-labelledby="profileDropdown">
              <div v-if="!store.isLogin">
                <li><RouterLink class="dropdown-item" :to="{name:'signup'}">회원가입</RouterLink></li>
                <li><RouterLink class="dropdown-item" :to="{name:'login'}">로그인</RouterLink></li>
              </div>
              <div v-else>
                <li><h5 class="ms-3 fw-bold">안녕하세요, <br> {{ store.userNickname }}님!</h5></li>
                <li><RouterLink class="dropdown-item" :to="{ name: 'profile'}">마이페이지</RouterLink></li>
                <li><a @click.prevent="logOut" href="#" class="dropdown-item">로그아웃</a></li>
              </div>
            </ul>
          </li>
        </ul>

        <!-- 작은 화면에서만 보이는 프로필 메뉴 -->
        <ul class="navbar-nav d-lg-none ">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <h3 class="mb-0">My Page</h3>
            </a>
            <ul class="dropdown-menu">
              <div v-if="!store.isLogin">
                <li><RouterLink class="dropdown-item" :to="{name:'signup'}"><h4 class="mb-0">회원가입</h4></RouterLink></li>
                <li><RouterLink class="dropdown-item" :to="{name:'login'}"><h4 class="mb-0">로그인</h4></RouterLink></li>
              </div>
              <div v-else>
                <li><RouterLink class="dropdown-item" :to="{ name: 'profile'}"><h4 class="mb-0">마이페이지</h4></RouterLink></li>
                <li><a @click.prevent="logOut" href="#" class="dropdown-item"><h4 class="mb-0">로그아웃</h4></a></li>
              </div>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="router-view-container">
    <RouterView/>
  </div>


  <!-- 챗봇 버튼 -->
  <button v-if="store.isLogin" class="chatbot-button" @click="toggleChatbot">
    <i class="fa-solid fa-comment"></i>
  </button>

  <!-- 챗봇 모달 -->
  <div v-if="isChatbotOpen" class="chatbot-modal">
    <div class="chatbot-header p-2">
      <h5 class="mb-0 fw-bold">Chatbot</h5>
      <button class="close-button" @click="toggleChatbot">
        <i class="fa-solid fa-x fa-2xs"></i>
      </button>
    </div>
    <div class="chatbot-content">
      <div class="chat-history">
        <!-- 메시지 렌더링 -->
        <div
          v-for="(msg, index) in chatHistory"
          :key="index"
          :class="['chat-message', msg.role === store.userName ? 'chat-user' : 'chat-bot']"
        >
          <!-- 챗봇 메시지에만 이모티콘 표시 -->
          <div v-if="msg.role !== store.userName" class="chat-icon">
            <i class="fa-solid fa-h fa-rotate-by mt-1" style="--fa-rotate-angle: -20deg; color:#74C0FC;"></i>
          </div>
          <!-- 텍스트 -->
          <div class="chat-text">
            <p class="mb-0">{{ msg.content }}</p>
          </div>
        </div>
      </div>
      <!-- 입력 영역 -->
      <div class="chat-input">
        <input
          type="text"
          v-model="userInput"
          placeholder="궁금한 것을 물어보세요!"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">보내기</button>
      </div>
    </div>
  </div>


</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import axios from 'axios';
import { useMovieStore } from './stores/counter';
import { useRouter, useRoute } from 'vue-router';
import { ref, watch } from 'vue';
const router = useRouter()
const store = useMovieStore()
const searchQuery = ref('') // 검색창에 입력한 영화
// const searchMovies = ref([]) // 검색창에 입력한 영화
const goSearch = function () {
  router.push({name: 'search'})
}
const logOut = function () {
  store.logout()
  if (isChatbotOpen) {
    isChatbotOpen.value = false
    chatHistory.value = []
  }
}


const getSearchMovie = async () => {
  if (searchQuery.value.trim()) {
    try {
      await store.getSearchMovies(searchQuery.value);
      // console.log(searchMovies.value)
      searchQuery.value = ''
      router.push({name: 'search'})
      
    } catch (error) {
      console.error('Error searching movies:', error);
    }
  }
};

// 챗봇
const userInput = ref(''); // 사용자 입력
const isChatbotOpen = ref(false); // 챗봇 모달 상태
const chatHistory = ref([]); // 챗봇 대화 기록

// 챗봇 모달 열고 닫기
const toggleChatbot = () => {
  isChatbotOpen.value = !isChatbotOpen.value;
};

const loadInitialMessage = function () {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/movies/chatbot/initial/',
    headers: { Authorization: `Token ${store.Token}` }
  })
  .then(res => {
    chatHistory.value.push(res.data)
  })
  .catch(error => {
    console.error('Error loading initial message:', error)
    chatHistory.value.push({ role:'도우미', content:'초기메시지를 불러오지 못 했습니다.' })
  })
}

const clearChatHistory = () => {
  chatHistory.value = [];
};

watch(isChatbotOpen, (newValue) => {
  if (newValue) {
    loadInitialMessage();
  }
  else {
    clearChatHistory()
  }
})

// 사용자 입력 처리 및 챗봇 API 호출
const sendMessage = function () {
  if (!userInput.value.trim()) return;

  const userMessage = userInput.value.trim();
  chatHistory.value.push({ role: `${store.userName}`, content: userMessage });

  
  // const response = await axios.post('http://127.0.0.1:8000/movies/chatbot/', { message: userMessage });
  console.log('요청시작!!!!!')
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/movies/chatbot/',
    headers: { Authorization: `Token ${store.Token}` },
    data: { message: userMessage }
  })
  .then(res => {
    console.log('요청성공!!!!!')
    chatHistory.value.push({ role: '도우미', content: res.data.response });
  })
  .catch(error => {
    console.log('요청실패!!!!!')
    chatHistory.value.push({ role: '도우미', content: 'Error: Unable to connect.' });
  })

  userInput.value = ''; // 입력 초기화
};
</script>

<style scoped>
.router-view-container {
  min-height: calc(100vh - 100px);
  margin-top: 120px; /* Nav 높이(100px)보다 더 큰 값으로 설정 */
  padding: 20px 0; /* 추가 여백 */
}

/* nav 관련 */
.custom-nav {
  z-index: 1030; /* Bootstrap의 기본 fixed-top z-index */
  background-color: rgba(255, 255, 255, 0.95); /* 배경 추가 (선택사항) */
}

.nav-item a {
  text-decoration: none;
  color: inherit;
}

.navbar-toggler {
  height: 80%;          /* Nav 높이의 80% */
  padding: 0.8rem;      /* 내부 여백 조정 */
  margin: auto 0;       /* 세로 중앙 정렬 */
}

.navbar-toggler-icon {
  width: 3em;           /* 아이콘 너비 증가 */
  height: 2em;          /* 아이콘 높이 증가 */
  font-size: 1.5rem;    /* 기본 폰트 크기 증가 */
}
.nav-item a:hover {
  color: #555;
}

/* 프로필 드롭다운 관련*/
.custom-dropdown {
  right: 1rem;
  left: auto;
  min-width: 200px;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
}

.custom-dropdown .dropdown-item {
  padding: 0.5rem 1rem;
}

/* 검색폼 관련 */
.search-form {
  width: 100%;
}

/* 작은 화면에서의 검색폼 스타일 */
@media (max-width: 992px) {
  .search-form {
    width: 100%;
    margin: 0.5rem 0;
  }
  
  .search-form .form-control {
    width: 100%;
  }
}

/* 챗봇 */
/* 챗봇 버튼 */
.chatbot-button {
  position: fixed;
  bottom: 40px;
  right: 40px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: grab;
  z-index: 1000;
}

/* 챗봇 모달 */
.chatbot-modal {
  position: fixed;
  bottom: 100px;
  right: 40px;
  width: 30%;
  background-color: white;
  border: 1px solid black;
  border-radius: 10px;
  box-shadow: 0 4px 6px black;
  z-index: 1000;
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: black;
  color: white;
  border-radius: 10px 10px 0 0;
}

.close-button {
  display: flex;
  background: none;
  border: none;
  color: white;
  font-size: 35px;
  cursor: grab;
}

.chatbot-content {
  max-height: 30%;
  display: flex;
  flex-direction: column;
}

.chat-history {
  /* height: 300px; */
  margin-top: 5px;
  min-height: 200px;
  max-height: 50vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 5px;
  border: 1px solid white;
  border-radius: 5px;
}

.chat-input {
  display: flex;
  gap: 5px;
  padding: 10px;
  border-radius: 10px;
}

.chat-input input {
  flex-grow: 1;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.chat-input button {
  padding: 5px 10px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
/* 추가한 것 */
.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}

.chat-user {
  justify-content: flex-end;
}

.chat-bot {
  justify-content: flex-start;
}

.chat-icon {
  margin: 0 10px;
  font-size: 24px;
}

.chat-text {
  position: relative;
  max-width: 60%;
  padding: 8px;
  border-radius: 10px;
  word-wrap: break-word;
  white-space: pre-wrap;
  font-size: 15px;
}

.chat-user .chat-text {
  background-color: #f1f1f1;
  color: black;
}

.chat-user .chat-text::after {
  content: ''; /* 가상 요소로 뾰족한 부분 추가 */
  position: absolute;
  top: 0;
  right: -10px; /* 오른쪽에 뾰족한 부분 */
  border-width: 10px;
  border-style: solid;
  border-color: transparent transparent #f1f1f1 transparent;
}

.chat-bot .chat-text {
  background-color: rgb(189, 188, 181);
  color: black;
  margin-left: 10px;
}

.chat-bot .chat-text::after {
  content: '';
  position: absolute;
  top: 0;
  left: -10px; /* 왼쪽에 뾰족한 부분 */
  border-width: 10px;
  border-style: solid;
  border-color: transparent transparent rgb(189, 188, 181) transparent;
}

.temp {
  cursor: pointer;
}
</style>