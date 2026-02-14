<template>
  <div class="home">
    <div class="hero">
      <h1>SideEyes Dashboard</h1>
      <p>Real-time scraped data from across the web</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading data...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Unable to Load Data</h2>
      <p>{{ error }}</p>
      <button @click="loadData">Retry</button>
    </div>

    <div v-else>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon quotes">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 10h16v2H8zm0 6h16v2H8zm0 6h12v2H8z" fill="currentColor"/>
            </svg>
          </div>
          <div class="stat-info">
            <h3>{{ quoteCount }}</h3>
            <p>Quotes Scraped</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon books">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="6" y="4" width="6" height="18" rx="1" fill="currentColor"/>
              <rect x="14" y="6" width="6" height="16" rx="1" fill="currentColor"/>
              <rect x="22" y="8" width="6" height="14" rx="1" fill="currentColor"/>
            </svg>
          </div>
          <div class="stat-info">
            <h3>{{ bookCount }}</h3>
            <p>Books Scraped</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon hockey">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="12" stroke="currentColor" stroke-width="2"/>
              <path d="M16 10v12M10 16h12" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div class="stat-info">
            <h3>{{ hockeyCount }}</h3>
            <p>Hockey Teams</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon timestamp">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="12" stroke="currentColor" stroke-width="2"/>
              <path d="M16 8v8l6 3" stroke="currentColor" stroke-width="2" fill="none"/>
            </svg>
          </div>
          <div class="stat-info">
            <h3 class="time">{{ lastUpdated }}</h3>
            <p>Last Updated</p>
          </div>
        </div>
      </div>

      <div class="data-preview">
        <div class="preview-section">
          <h2>Latest Quotes</h2>
          <div v-if="latestQuotes.length === 0" class="empty">No quotes available</div>
          <div v-else class="preview-grid">
            <div v-for="(quote, index) in latestQuotes.slice(0, 3)" :key="index" class="preview-card quote">
              <p class="content">"{{ quote.text }}"</p>
              <p class="author">— {{ quote.author }}</p>
            </div>
          </div>
        </div>

        <div class="preview-section">
          <h2>Latest Books</h2>
          <div v-if="latestBooks.length === 0" class="empty">No books available</div>
          <div v-else class="preview-grid">
            <div v-for="(book, index) in latestBooks.slice(0, 3)" :key="index" class="preview-card book">
              <p class="title">{{ book.title }}</p>
              <p class="author">{{ book.author }}</p>
              <p v-if="book.price" class="price">{{ book.price }}</p>
            </div>
          </div>
        </div>

        <div class="preview-section">
          <h2>Hockey Teams</h2>
          <div v-if="latestHockey.length === 0" class="empty">No hockey data available</div>
          <div v-else class="preview-grid">
            <div v-for="(team, index) in latestHockey.slice(0, 3)" :key="index" class="preview-card hockey">
              <p class="title">{{ team.name || team.team }}</p>
              <p class="stats">{{ team.year || 'Data Available' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { fetchData } from '../services/api'

export default defineComponent({
  name: 'Home',
  data() {
    return {
      quoteCount: 0,
      bookCount: 0,
      hockeyCount: 0,
      lastUpdated: 'Never',
      latestQuotes: [],
      latestBooks: [],
      latestHockey: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        this.error = null
        const response = await fetch('http://localhost:5000/api/data')
        
        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`)
        }
        
        const data = await response.json()
        
        if (data.data) {
          this.latestQuotes = data.data.quotes || []
          this.quoteCount = this.latestQuotes.length
          
          this.latestBooks = data.data.books || []
          this.bookCount = this.latestBooks.length
          
          this.latestHockey = data.data.hockey_teams || []
          this.hockeyCount = this.latestHockey.length
          
          if (data.timestamp) {
            const date = new Date(data.timestamp)
            this.lastUpdated = date.toLocaleDateString() + '\n' + date.toLocaleTimeString()
          }
        }
      } catch (error) {
        console.error('Failed to load data:', error)
        this.error = `Unable to load scraped data: ${error.message}. Make sure the API server is running on http://localhost:5000`
        this.quoteCount = 0
        this.bookCount = 0
        this.hockeyCount = 0
      } finally {
        this.loading = false
      }
    }
  }
})
</script>

<style scoped>
.home {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.hero p {
  font-size: 1.25rem;
  opacity: 0.95;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  color: #1f2937;
}

.loading-state {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.error-state {
  background: white;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.error-state button:hover {
  background: #4f46e5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.quotes {
  background: #e0f2fe;
  color: #0284c7;
}

.stat-icon.books {
  background: #fce7f3;
  color: #ec4899;
}

.stat-icon.hockey {
  background: #fef3c7;
  color: #f59e0b;
}

.stat-icon.timestamp {
  background: #dcfce7;
  color: #16a34a;
}

.stat-info h3 {
  margin: 0;
  font-size: 2rem;
  color: #1f2937;
}

.stat-info p {
  margin: 0.25rem 0 0 0;
  color: #6b7280;
  font-size: 0.95rem;
}

.stat-info .time {
  font-size: 0.9rem;
  white-space: pre-line;
  line-height: 1.3;
}

.data-preview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.preview-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.preview-section h2 {
  color: #1f2937;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 1rem;
}

.preview-grid {
  display: grid;
  gap: 1rem;
}

.preview-card {
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #6366f1;
  background: #f9fafb;
  transition: all 0.3s ease;
}

.preview-card:hover {
  background: #f3f4f6;
  transform: translateX(4px);
}

.preview-card.quote .content {
  font-style: italic;
  color: #1f2937;
  font-size: 0.95rem;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
}

.preview-card.quote .author {
  color: #6366f1;
  font-weight: 600;
  font-size: 0.85rem;
  margin: 0;
}

.preview-card.book .title {
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.3rem 0;
  line-height: 1.4;
}

.preview-card.book .author {
  color: #6b7280;
  font-size: 0.85rem;
  margin: 0 0 0.5rem 0;
}

.preview-card.book .price {
  color: #6366f1;
  font-weight: 600;
  font-size: 0.95rem;
  margin: 0;
}

.preview-card.hockey .title {
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.3rem 0;
}

.preview-card.hockey .stats {
  color: #6b7280;
  font-size: 0.85rem;
  margin: 0;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #9ca3af;
  font-style: italic;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .data-preview {
    grid-template-columns: 1fr;
  }
}
</style>
