<template>
  <div class="quotes">
    <div class="page-header">
      <h1>Quotes Collection</h1>
      <p>Discover inspiring and thought-provoking quotes from around the web</p>
    </div>

    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search quotes..."
          @input="filterQuotes"
        >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M14 14l4 4" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>

      <div class="filter-tags">
        <button 
          v-if="selectedTag" 
          class="tag active"
          @click="selectedTag = ''"
        >
          {{ selectedTag }} <span>×</span>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading quotes...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Unable to Load Quotes</h2>
      <p>{{ error }}</p>
      <button @click="loadQuotes">Retry</button>
    </div>

    <div v-else-if="filteredQuotes.length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <h2>No quotes found</h2>
      <p>Try adjusting your search or filters</p>
    </div>

    <div v-else class="quotes-grid">
      <div v-for="(quote, index) in filteredQuotes" :key="index" class="quote-card">
        <div class="quote-mark">"</div>
        <p class="quote-text">{{ quote.text }}</p>
        <p class="quote-author">— {{ formatAuthor(quote.author) }}</p>
        <div class="quote-tags">
          <span 
            v-for="tag in quote.tags" 
            :key="tag"
            class="tag"
            @click="filterByTag(tag)"
          >
            {{ tag }}
          </span>
        </div>
        <div class="quote-source">{{ quote.source }}</div>
      </div>
    </div>

    <div class="stats">
      <p>Showing {{ filteredQuotes.length }} of {{ allQuotes.length }} quotes</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Quotes',
  data() {
    return {
      allQuotes: [],
      filteredQuotes: [],
      searchQuery: '',
      selectedTag: '',
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadQuotes()
  },
  methods: {
    async loadQuotes() {
      try {
        this.loading = true
        this.error = null
        const response = await fetch('http://localhost:5000/api/quotes')
        
        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`)
        }
        
        const data = await response.json()
        this.allQuotes = data.quotes || []
        this.filteredQuotes = [...this.allQuotes]
      } catch (error) {
        console.error('Failed to load quotes:', error)
        this.error = `Unable to load quotes: ${error.message}`
        this.allQuotes = []
        this.filteredQuotes = []
      } finally {
        this.loading = false
      }
    },
    filterQuotes() {
      this.filteredQuotes = this.allQuotes.filter(quote => {
        const matchesSearch = quote.text.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            quote.author.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesTag = !this.selectedTag || (quote.tags && quote.tags.includes(this.selectedTag))
        return matchesSearch && matchesTag
      })
    },
    filterByTag(tag) {
      this.selectedTag = this.selectedTag === tag ? '' : tag
      this.filterQuotes()
    },
    formatAuthor(author) {
      return author.trim()
    }
  }
})
</script>

<style scoped>
.quotes {
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

.page-header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
}

.page-header p {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 250px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.search-box svg {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
}

.filter-tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.tag:hover {
  background: rgba(255, 255, 255, 0.3);
}

.tag.active {
  background: white;
  color: #667eea;
  border-color: white;
}

.tag span {
  margin-left: 0.5rem;
  font-weight: bold;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: white;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  color: #1f2937;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h2 {
  margin: 0.5rem 0;
  color: #dc2626;
}

.error-state p {
  color: #6b7280;
  margin: 1rem 0;
}

.error-state button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.error-state button:hover {
  background: #4f46e5;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: white;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h2,
.empty-state p {
  margin: 0.5rem 0;
}

.quotes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.quote-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.quote-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.quote-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.quote-mark {
  font-size: 4rem;
  color: #e0e7ff;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.quote-text {
  font-size: 1.1rem;
  font-style: italic;
  line-height: 1.6;
  color: #1f2937;
  margin: 1rem 0;
}

.quote-author {
  font-weight: 600;
  color: #6366f1;
  margin: 1rem 0 0.5rem 0;
  font-style: normal;
}

.quote-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}

.quote-tags .tag {
  background: #f0f4ff;
  color: #6366f1;
  border: 1px solid #e0e7ff;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  cursor: pointer;
}

.quote-tags .tag:hover {
  background: #e0e7ff;
}

.quote-source {
  font-size: 0.8rem;
  color: #9ca3af;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.stats {
  text-align: center;
  color: white;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 1.75rem;
  }

  .controls {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .quotes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
