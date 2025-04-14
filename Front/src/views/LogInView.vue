<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-5 shadow-lg login-card">
      <h1 class="text-center mb-4">로그인</h1>
      <form @submit.prevent="logIn">
        <!-- Username -->
        <div class="mb-4">
          <label for="username" class="form-label">ID</label>
          <input
            type="text"
            id="username"
            v-model.trim="username"
            :class="['form-control', 'form-control-lg', { 'is-invalid': !username }]"
            placeholder="아이디를 입력해주세요"
          />
          <div v-if="!username" class="invalid-feedback">아이디를 입력해주세요.</div>
        </div>
        <!-- Password -->
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            id="password"
            v-model.trim="password"
            :class="['form-control', 'form-control-lg', { 'is-invalid': !password }]"
            placeholder="비밀번호를 입력해주세요"
          />
          <div v-if="!password" class="invalid-feedback">비밀번호를 입력해주세요.</div>
        </div>
        <!-- Submit Button -->
        <button type="submit" class="btn btn-dark btn-lg w-100">Log In</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/counter";

const store = useMovieStore();
const username = ref("");
const password = ref("");

const logIn = () => {
  if (!username.value || !password.value) {
    console.log("입력값 확인 필요");
    return;
  }

  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style scoped>
/* 전체 컨테이너 */
.container {
  max-width: 80%; /* 화면 너비의 80% */
}

/* 로그인 카드 */
.login-card {
  width: 100%;
  max-width: 1000px; /* 최대 너비 설정 */
  height: auto;
  border-radius: 12px;
  background-color: #fff; /* 흰색 배경 */
}

/* 입력 필드 */
.form-control-lg {
  font-size: 18px; /* 폰트 크기 증가 */
  height: calc(2.5rem + 2px); /* 높이 증가 */
  padding: 10px; /* 내부 여백 증가 */
}

.is-invalid {
  border-color: #f46c79; /* 빨간 테두리 */
}

.invalid-feedback {
  color: #f46c79;
}

/* 버튼 */
.btn-dark {
  background-color: #000; /* 검은색 배경 */
  color: #fff; /* 흰색 텍스트 */
}

.btn-dark:hover {
  background-color: #333; /* hover 시 더 밝은 검은색 */
}

.btn-lg {
  font-size: 18px; /* 버튼 텍스트 크기 증가 */
}
</style>