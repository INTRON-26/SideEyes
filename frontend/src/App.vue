<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="nav-content">
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" stroke="#6366f1" stroke-width="2"/>
            <circle cx="10" cy="12" r="2" fill="#6366f1"/>
            <circle cx="22" cy="12" r="2" fill="#6366f1"/>
            <path d="M 10 20 Q 16 24 22 20" stroke="#6366f1" stroke-width="2" fill="none"/>
          </svg>
          <span>SideEyes</span>
        </div>
        <ul class="nav-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/quotes">Quotes</router-link></li>
          <li><router-link to="/books">Books</router-link></li>
          <li><router-link to="/sites">Sites</router-link></li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2024 SideEyes - Web Scraper Dashboard. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #6366f1;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
  position: relative;
}

.nav-links a:hover {
  color: #6366f1;
}

.nav-links a.router-link-active {
  color: #6366f1;
}

.nav-links a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  right: 0;
  height: 2px;
  background: #6366f1;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 2rem auto;
  width: 100%;
  padding: 0 2rem;
}

.footer {
  background: rgba(0, 0, 0, 0.1);
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: 4rem;
}
</style>
