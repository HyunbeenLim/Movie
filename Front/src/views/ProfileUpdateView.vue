<template>
  <div class="container">
    <h2>프로필 정보 수정하기</h2>
    <form @submit.prevent="updateProfile">
      <div class="form-group">
        <label for="username">이름:</label>
        <input v-model="updateUsername" :placeholder="store.userName" id="username" class="form-control">
      </div>
      <div class="form-group">
        <label for="email">이메일:</label>
        <input v-model="updateEmail" :placeholder="store.userEmail" id="email" type="email" class="form-control">
      </div>
      <button type="submit" class="btn btn-info">회원 정보 수정</button>
    </form>

    <h2 class="mt-4">비밀번호 변경</h2>
    <form @submit.prevent="changePassword">
      <div class="form-group">
        <label for="currentPassword">현재 비밀번호:</label>
        <input v-model="currentPassword" type="password" id="currentPassword" class="form-control">
      </div>
      <div class="form-group">
        <label for="newPassword">새 비밀번호:</label>
        <input v-model="newPassword" type="password" id="newPassword" class="form-control">
      </div>
      <div class="form-group">
        <label for="confirmPassword">새 비밀번호 확인:</label>
        <input v-model="confirmPassword" type="password" id="confirmPassword" class="form-control">
      </div>
      <button type="submit" class="btn btn-warning">비밀번호 변경</button>
    </form>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const store = useMovieStore();
const updateUsername = ref('');
const updateEmail = ref('');
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');

onMounted(async () => {
  try {
    const userInfo = await store.fetchUserInfo();
    updateUsername.value = store.userName; // Use store value to ensure reactivity
    updateEmail.value = store.userEmail;   // Use store value to ensure reactivity
  } catch (error) {
    console.error('사용자 정보 로드 실패:', error);
    errorMessage.value = '사용자 정보를 불러오는데 실패했습니다.';
  }
});

const updateProfile = async () => {
  try {
    await store.updateUserInfo({
      username: updateUsername.value,
      email: updateEmail.value
    });
    successMessage.value = '프로필이 성공적으로 업데이트되었습니다.';
  } catch (error) {
    console.error('프로필 업데이트 실패:', error);
    errorMessage.value = '프로필 업데이트에 실패했습니다.';
  }
};

const changePassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = '새 비밀번호가 일치하지 않습니다.';
    return;
  }

  try {
    await store.changePassword({
      old_password: currentPassword.value,
      new_password1: newPassword.value,
      new_password2: confirmPassword.value
    });
    successMessage.value = '비밀번호가 성공적으로 변경되었습니다.';
    currentPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
  } catch (error) {
    console.error('비밀번호 변경 실패:', error);
    errorMessage.value = '비밀번호 변경에 실패했습니다.';
  }
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
.btn {
  margin-top: 1rem;
}
</style>