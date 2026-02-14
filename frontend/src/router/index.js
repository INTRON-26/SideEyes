import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Quotes from '../views/Quotes.vue'
import Books from '../views/Books.vue'
import Sites from '../views/Sites.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/quotes',
    name: 'Quotes',
    component: Quotes
  },
  {
    path: '/books',
    name: 'Books',
    component: Books
  },
  {
    path: '/sites',
    name: 'Sites',
    component: Sites
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
