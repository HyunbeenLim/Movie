import HomeView from '@/views/HomeView.vue'
import LogInView from '@/views/LogInView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieView from '@/views/MovieView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SignUpView from '@/views/SignUpView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useMovieStore } from '@/stores/counter'
import ProfileUpdateView from '@/views/ProfileUpdateView.vue'
import SearchView from '@/views/SearchView.vue'
import OtherProfileView from '@/views/OtherProfileView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'home',
      component:HomeView
    },
    {
      path:'/movie',
      name:'movie',
      component:MovieView
    },
    {
      path:'/:movieId',
      name:'moviedetail',
      component:MovieDetailView
    },
    {
      path: '/profile', 
      name: 'profile',
      component:ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/:userId?', 
      name: 'otherprofile',
      component:OtherProfileView,
    },
    {
      path:'/signup',
      name:'signup',
      component:SignUpView
    },
    {
      path:'/login',
      name:'login',
      component:LogInView
    },
    {
      // 회원정보수정
      path:'/update',
      name:'update',
      component:ProfileUpdateView
    },
    {
      // 검색결과
      path:'/search',
      name:'search',
      component:SearchView
    },
  ],
})

router.beforeEach((to,from) => {
  const store = useMovieStore()
  // 로그인 상태면 회원가입, 로그인 페이지 접근 제한
  if ((to.name === 'signup' || to.name === 'login') && (store.isLogin)) {
    return { name: 'home' }
  }
})

// 로그아웃 상태에서 프로필 버튼을 누르면 로그인 페이지로 안내
router.beforeEach((to, from, next) => {
  const store = useMovieStore()
  if (to.matched.some(record => record.meta.requiresAuth) && !store.isLogin) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
