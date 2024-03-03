import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import Home from './views/Home/homeView.vue';
import Login from './views/User/LoginView.vue';
import ForgotPassword from './views/User/Password/ForgotPassword.vue'
import Step2 from './views/User/Password/Step2View.vue'
import SetPassword from './views/User/Password/SetPasswordView.vue'
import profileView from './views/Profile/profileView.vue'

const app = createApp(App)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name:"Login", component: Login},
    { path: '/home', name:"Home", component: Home},
    { path: '/reset_password/step1', name:"ResetPassword", component: ForgotPassword},
    { path: '/reset_password/step3', name:"ResetPasswordStep2", component: Step2},
    { path: '/reset_password/step2', name:"SetPassword", component: SetPassword},
    { path: '/dashboard', name:"Profile", component: profileView},

  ]
})

app.use(router)
app.mount('#app')