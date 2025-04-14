<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-5 shadow-lg signup-card">
      <h3 class="text-center mb-4">회원가입</h3>
      <form @submit.prevent="signUp">
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
        <!-- Email -->
        <div class="mb-4">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            v-model.trim="email"
            :class="['form-control', 'form-control-lg', { 'is-invalid': !email }]"
            placeholder="이메일을 입력해주세요"
          />
          <div v-if="!email" class="invalid-feedback">이메일을 입력해주세요.</div>
        </div>
        <!-- Password -->
        <div class="mb-4">
          <label for="password1" class="form-label">비밀번호</label>
          <input
            type="password"
            id="password1"
            v-model.trim="password1"
            :class="['form-control', 'form-control-lg', { 'is-invalid': !password1 }]"
            placeholder="비밀번호를 입력해주세요"
          />
          <div v-if="!password1" class="invalid-feedback">비밀번호를 입력해주세요.</div>
        </div>
        <!-- Confirm Password -->
        <div class="mb-4">
          <label for="password2" class="form-label">비밀번호 재입력</label>
          <input
            type="password"
            id="password2"
            v-model.trim="password2"
            :class="
              ['form-control', 'form-control-lg', { 'is-invalid': password1 !== password2 || !password2 }]
            "
            placeholder="비밀번호를 다시 입력해주세요"
          />
          <div v-if="password1 !== password2 || !password2" class="invalid-feedback">
            비밀번호가 일치하지 않습니다.
          </div>
        </div>
        <!-- Nickname -->
        <div class="mb-4">
          <label for="nickname" class="form-label">닉네임</label>
          <input
            type="text"
            id="nickname"
            v-model.trim="nickname"
            :class="
              ['form-control', 'form-control-lg', { 'is-invalid': !nickname }]"
            placeholder="닉네임을 입력해주세요"
          />
          <div v-if="!nickname" class="invalid-feedback">닉네임을 입력해주세요.</div>
        </div>
        <!-- Submit Button -->
        <button type="submit" class="btn btn-dark btn-lg w-100">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMovieStore } from "@/stores/counter";

const store = useMovieStore();
const username = ref("");
const email = ref("");
const password1 = ref("");
const password2 = ref("");
const nickname = ref("");

const signUp = () => {
  if (!username.value || !email.value || !password1.value || password1.value !== password2.value || !nickname.value) {
    console.log("입력값 확인 필요");
    return;
  }

  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
  };
  console.log(payload);
  store.createSignUp(payload);
};
</script>

<style scoped>
/* 전체 컨테이너 */
.container {
  max-width: 80%; /* 화면 너비의 80% */
}

/* 회원가입 카드 */
.signup-card {
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