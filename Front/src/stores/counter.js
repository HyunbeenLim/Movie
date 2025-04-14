import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useMovieStore = defineStore('movie', () => {

const API_URL = 'http://127.0.0.1:8000/'
const Token = ref(null)
const userId = ref(null)
const userName = ref(null)
const userEmail = ref(null)
const userNickname = ref(null)


const isLogin = computed(() => {
  if (Token.value === null) {
    return false
  } else {
    return true
  }
})

const movies = ref([])
const getMovies = function () {
  const headers = Token.value
  ? { Authorization: `Token ${Token.value}` } // Token이 있는 경우 Authorization 헤더 추가
  : {}; // Token이 없는 경우 빈 객체
  axios({
    method:'get',
    url: `${API_URL}movies/`,
    headers: headers
  })
  .then(res => {
    console.log("영화 데이터 가져오기 성공:", res.data);
    // console.log(res.data)
    movies.value = res.data
  })
  .catch(err => {
    console.error("영화 데이터 가져오기 실패:", err);
  })
}

const getMovieDetail = function (movieId) {
  const movie = movies.value.find((element) => element.id == movieId)
  console.log('영화찾음 영화id:',movie.id)
  return movie
}

const genres = ref([])
const getGenres = function () {
  axios({
    method:'get',
    url: `${API_URL}movies/genre/`,
  }) .then((res) => {
    genres.value = res.data
    console.log("장르 데이터 가져오기 성공:", res.data);
  }) .catch((err) => {
    console.error("장르 데이터 가져오기 실패:", err);
  })
}

const selectedGenreMovies = ref([])
const getGenreMovies = function (selectedGenreId) {
  if (!movies.value || movies.value?.length === 0) {
    console.error("영화 데이터가 비어 있습니다.");
    return [];
  }
  if (!selectedGenreId) {
    return movies.value; // 선택된 장르가 없으면 전체 영화 반환
  }
  return movies.value.filter((movie) =>
    movie.genres.some((genre) => genre.id == selectedGenreId)
  );
};

// 회원가입 요청
const createSignUp = function (payload) {
  const { username, email, password1, password2, nickname } = payload
  console.log('시작!!!!!!')
  if (password1 !== password2) {
    alert('비밀번호가 일치하지 않습니다')
    return
  }

  const finalpayload = {
    username: username,
    email: email,
    password: password1,
    nickname: nickname,
  }

  axios({
    method:'post',
    url: `${API_URL}accounts/signup/`,
    data: finalpayload
  }) 
  .then(res => {
    console.log('회원가입 성공!')
    Token.value = res.data.key
    console.log(res.data)
    logIn({'username':username, 'password':password1})
    router.push({name: 'home'})
  })
  .catch(err => {
    console.log(err)
  })
}

// 로그인 요청
const logIn = function (payload) {
  const { username, password } = payload

  axios({
    method:'post',
    url: `${API_URL}dj-rest-auth/login/`,
    data: {
      username, password
    }
  }) 
  .then(res => {
    console.log('로그인 성공!')
    Token.value = res.data.key
    userId.value = res.data.user_id
    userName.value = res.data.user_name
    userEmail.value = res.data.user_email
    userNickname.value = res.data.nickname
    console.log(res.data)
    console.log('유저 정보 받아오기')
    fetchUserInfo()
    
    // fetchLikedMovies()
    movies.value = []; // 영화 목록 초기화
    getMovies()
    router.push({name: 'home'})
  })
  .catch(err => {
    console.log(err)
  })
}
// 유저 이름과 이메일 정보 갱신을 위한 요청
const fetchUserInfo = async function() {
  if (!Token.value || !userId.value) return
  try {
    const response = await axios.get(`${API_URL}accounts/user/`, {
      headers: { Authorization: `Token ${Token.value}` }
    })
    userName.value = response.data.username
    userEmail.value = response.data.email
    userNickname.value = response.data.nickname
    console.log('닉네임: ', response.data.nickname)
    console.log('유저 정보 받기 성공:', response.data)
  } catch (error) {
    console.error('유저 정보 받기 실패:', error)
  }
}

// 남의 프로필 방문시 필요한 다른 유저의 정보
const userData = ref(null)
const fetchOtherInfo = async function(user_id) {
  try {
    console.log('fetchOtherInfo 요청시작 유저id:',user_id)
    const response = await axios({
      method: 'get',
      url: `${API_URL}dj-rest-auth/${user_id}/`,
    });
    console.log('타 유저 정보 GET: ', response.data);
    userData.value = response.data; // 성공적으로 데이터를 받아오면 userData 업데이트
  } catch (error) {
    console.error('타 유저 정보 실패: ', error); // 에러 처리
  }
};

const updateUserInfo = async function(updatedInfo) {
  if (!Token.value) return
  try {
    const response = await axios.patch(`${API_URL}accounts/user/`, updatedInfo, {
      headers: { Authorization: `Token ${Token.value}` }
    })
    userName.value = response.data.username
    userEmail.value = response.data.email
    console.log('유저 정보 수정 성공', response.data)
  } catch (error) {
    console.error('유저 정보 수정 실패', error)
  }
}

// 로그아웃
const logout = function() {
  axios({
    method: 'post',
    url: `${API_URL}accounts/logout/`,
    headers: {
      'Authorization': `Token ${Token.value}`,
    },
  })
  .then(res => {
    Token.value = null
    userId.value = null
    userName.value = null
    userEmail.value = null
    userNickname.value = null
    likedMovies.value = []
    movies.value = []; // 영화 목록 초기화
    recommendationsIds.value = null; // 협업 필터링 영화 목록 초기화
    like_unlike_total.value = 0
    getMovies()
    console.log('로그아웃 성공')
    router.push({name: 'home'})
  })
  .catch(err => {
    console.log('로그아웃 실패:', err)
  })
}

// 유저가 좋아요 누른 영화 정보 저장
const likedMovies = ref(null)

// 좋아요 기능
const movieLike = function (movieId, preference) {
  if (!Token.value) {
    // 로그인이 안 된 경우
    alert("로그인이 필요합니다.");
    router.push({name: 'login'})
    return;
  }
  axios({
    method:'post',
    url:`${API_URL}movies/${movieId}/like/${preference}/`,
    headers: {
      'Authorization':`Token ${Token.value}`
    }
  })
    .then(res => {
      const movie = movies.value.find((element) => element.id == movieId)
      const {isLike, isDislike, userId} = res.data      
        if (movie) {
          movie.is_liked = isLike;
          movie.is_disliked = isDislike;
        }
    })
    .catch(err => {
      console.log(err)
    })
}

// 사용자의 좋아요 목록 찾기
const fetchLikedMovies = function(user_id) {
  // if (!Token.value) return

  axios({
    method: 'get',
    url: `${API_URL}movies/liked/${user_id}/`,
    // headers: { Authorization: `Token ${Token.value}` }
  })
  .then(res => {
    likedMovies.value = res.data
    console.log('좋아요 목록 가져오기 성공:', likedMovies.value)
  })
  .catch(err => {
    console.log('좋아요 목록 가져오기 실패:', err)
  })
}

// 리뷰 작성
const reviews = ref([])

// 해당 movieId에 해당하는 리뷰만 가져오기
const fetchReviews = async function(movieId) {
  try {
    const response = await axios.get(`${API_URL}movies/${movieId}/reviews/`)
    reviews.value = response.data
    console.log('Reviews fetched successfully:', reviews.value)
  } catch (error) {
    console.error('Error fetching reviews:', error)
  }
}

const submitReview = async function(movieId, review) {
  if (!Token.value) return

  try {
    const response = await axios.post(`${API_URL}movies/${movieId}/reviews/create/`, review, {
      headers: { Authorization: `Token ${Token.value}` }
    })
    console.log('Review submitted successfully:', response.data)
    await fetchReviews(movieId)
    return response.data
  } catch (error) {
    console.error('Error submitting review:', error)
    throw error
  }
}

// 로그인한 사용자 본인이 작성한 리뷰들만 저장 
const userReviews = ref([])

const fetchUserReviews = async function(user_id) {
  // if (!Token.value) return

  try {
    const response = await axios.get(`${API_URL}movies/user-reviews/${user_id}/`, {
      // headers: { Authorization: `Token ${Token.value}` }
    })
    userReviews.value = response.data
    console.log('User reviews fetched successfully:', userReviews.value)
  } catch (error) {
    console.error('Error fetching user reviews:', error)
  }
}

// 리뷰 삭제
const deleteReview = async function(movieId, reviewId) {
  if (!Token.value) return

  try {
    await axios.delete(`${API_URL}movies/${movieId}/reviews/${reviewId}/`, {
      headers: { Authorization: `Token ${Token.value}` }
    })
    console.log('리뷰 삭제 성공')
    await fetchReviews(movieId)
  } catch (error) {
    console.error('리뷰 삭제 실패 ㅠㅠ', error)
  }
}
const searchMovieIds = ref([])
const getSearchMovies = async (query) => {
  console.log('검색시작!!!')
  try {
    const response = await axios.get(`${API_URL}movies/search/`, {
     params: { search: query }
    });
    console.log('검색완료!!!')
    // console.log(response.data)
    searchMovieIds.value = response.data.search_movie_ids; // API 응답 구조에 따라 조정 필요
    console.log(searchMovieIds.value)
  } catch (error) {
    console.error('Error searching movies:', error);
    // return [];
  }
};

const updateReview = async function(movieId, reviewId, review) {
  if (!Token.value) return

  try {
    const response = await axios.put(`${API_URL}movies/${movieId}/reviews/${reviewId}/update/`, review, {
      headers: { Authorization: `Token ${Token.value}` }
    })
    console.log('Review updated successfully:', response.data)
    await fetchReviews(movieId)
    return response.data
  } catch (error) {
    console.error('Error updating review:', error)
    throw error
  }
}

// 유저가 좋아요 누른 장르 빈도수 
const genreCountList = ref([])

// 유저가 좋아요 누른 장르 빈도수 총합 
const getLikedGenreCount = function () {
  if (!isLogin.value) return
  axios({
    method:'get',
    url:`${API_URL}movies/genre/count/`,
    headers:{ Authorization:`Token ${Token.value}`}
  })
  .then(res => {
    console.log('장르별 유저의 좋아요 빈도수 가져오기 성공')
    console.log(res.data)
    genreCountList.value = res.data
  })
  .catch(err => {
    console.log('장르별 좋아요수 실패사유:',err)
    genreCountList.value = []
  })
}
// 장르별 빈도수 중 가장 높은 장르id 찾기
const topGenreId = computed(() => {
  if (genreCountList.value.length == 0) return null;
  // 좋아요 수가 가장 높은 장르 ID 반환
  const topGenre = genreCountList.value.reduce((prev, current) =>
    prev.count > current.count ? prev : current
  );
  console.log('최빈수 장르id : ',topGenre.genre_id)
  return topGenre.genre_id;
});

// 협업필터링 추천리스트
const recommendationsIds = ref(null)
const like_unlike_total = ref(0)
const getRecommendations = function () {
  if (!isLogin.value) return
  // 좋아요/싫어요 count 요청
  axios({
    method: 'get',
    url: `${API_URL}movies/liked/count/`,
    headers: { Authorization: `Token ${Token.value}` }
  })
    .then(res => {
      const newTotal = res.data['like_unlike_count'];
      console.log('좋아요/싫어요 count 가져오기 성공:', newTotal);
      
      // 이전 total과 비교하여 협업필터링 요청 여부 결정
      const flag = 
        // 처음으로 10개 이상이 된 경우
        (like_unlike_total.value < 10 && newTotal >= 10) ||
        // 이전 카운트값보다 10개 차이나는 경우
        (newTotal - like_unlike_total.value >= 10);
      
      like_unlike_total.value = newTotal;

      // 10개 미만이면 요청하지 않음
      if (newTotal < 10) return;

      // 협업필터링 요청 조건 확인
      if (flag) {
        // 협업필터링 추천 요청
        console.log('협업필터링 요청 시작!!');
        axios({
          method: 'get',
          url: `${API_URL}movies/recommendations/`,
          headers: { Authorization: `Token ${Token.value}` }
        })
          .then(res => {
            const newRecommendations = res.data['recommendations'];
            // 이전 추천 목록과 같은지 확인
            if (JSON.stringify(recommendationsIds.value) !== JSON.stringify(newRecommendations)) {
              console.log('협업필터링 가져오기 성공');
              console.log(newRecommendations);
              recommendationsIds.value = newRecommendations;
            } else {
              console.log('이전 추천 목록과 동일하여 업데이트하지 않음');
            }
          })
          .catch(err => {
            console.log('협업필터링 실패사유:', err);
          });
      }
    })
    .catch(err => {
      console.log('좋아요/싫어요 count 가져오기 실패:', err);
      like_unlike_total.value = 0;
    });
};

  return { 
    API_URL, movies, getMovies, getMovieDetail, genres, 
    getGenres, selectedGenreMovies, getGenreMovies, 
    createSignUp, logIn, isLogin, logout, Token, movieLike,
    likedMovies, reviews, fetchReviews, submitReview,
    userReviews, fetchUserReviews, userId, userName, deleteReview,
    fetchLikedMovies,searchMovieIds, getSearchMovies,updateReview,
    userEmail, fetchUserInfo, fetchOtherInfo, userData, updateUserInfo,
    getLikedGenreCount, topGenreId, getRecommendations,
    like_unlike_total, genreCountList, recommendationsIds, userNickname,
   }
},{persist: true,},)
