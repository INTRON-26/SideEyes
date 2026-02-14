<template>
  <div class="books">
    <div class="page-header">
      <h1>Books Collection</h1>
      <p>Explore a curated collection of books from around the web</p>
    </div>

    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search books by title or author..."
          @input="filterBooks"
        >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M14 14l4 4" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>

      <div class="sort-selector">
        <select v-model="sortBy" @change="filterBooks">
          <option value="title">Sort by Title</option>
          <option value="rating">Sort by Rating</option>
          <option value="price">Sort by Price</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading books...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Unable to Load Books</h2>
      <p>{{ error }}</p>
      <button @click="loadBooks">Retry</button>
    </div>

    <div v-else-if="filteredBooks.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h2>No books found</h2>
      <p>Try adjusting your search</p>
    </div>

    <div v-else class="books-grid">
      <div v-for="(book, index) in filteredBooks" :key="index" class="book-card">
        <div class="book-cover">
          <div class="cover-placeholder">
            <svg width="80" height="120" viewBox="0 0 80 120" fill="none">
              <rect width="80" height="120" fill="#e0e7ff" rx="4"/>
              <text x="40" y="60" text-anchor="middle" dominant-baseline="middle" fill="#6366f1" font-size="24" font-weight="bold">📖</text>
            </svg>
          </div>
        </div>
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author || 'Unknown Author' }}</p>
          
          <div class="book-meta">
            <div class="rating" v-if="book.rating">
              <div class="stars">
                <span v-for="i in 5" :key="i" :class="i <= Math.round(book.rating) ? 'star filled' : 'star'">★</span>
              </div>
              <span class="rating-text">{{ book.rating }}</span>
            </div>
          </div>

          <p class="book-description" v-if="book.description">
            {{ truncate(book.description, 100) }}
          </p>

          <div class="book-footer">
            <span class="price" v-if="book.price">{{ book.price }}</span>
            <span class="availability" :class="{available: book.available !== false}">
              {{ book.available !== false ? 'In Stock' : 'Out of Stock' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="stats">
      <p>Showing {{ filteredBooks.length }} of {{ allBooks.length }} books</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Books',
  data() {
    return {
      allBooks: [],
      filteredBooks: [],
      searchQuery: '',
      sortBy: 'title',
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadBooks()
  },
  methods: {
    async loadBooks() {
      try {
        this.loading = true
        this.error = null
        const response = await fetch('http://localhost:5000/api/books')
        
        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`)
        }
        
        const data = await response.json()
        this.allBooks = data.books || []
        this.filteredBooks = [...this.allBooks]
        this.filterBooks()
      } catch (error) {
        console.error('Failed to load books:', error)
        this.error = `Unable to load books: ${error.message}`
        this.allBooks = []
        this.filteredBooks = []
      } finally {
        this.loading = false
      }
    },
    filterBooks() {
      let filtered = this.allBooks.filter(book => {
        const query = this.searchQuery.toLowerCase()
        return (book.title && book.title.toLowerCase().includes(query)) ||
               (book.author && book.author.toLowerCase().includes(query))
      })

      // Sort
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'rating':
            return (b.rating || 0) - (a.rating || 0)
          case 'price':
            const priceA = parseFloat(a.price?.replace(/[^\d.-]/g, '') || 0)
            const priceB = parseFloat(b.price?.replace(/[^\d.-]/g, '') || 0)
            return priceA - priceB
          case 'title':
          default:
            return (a.title || '').localeCompare(b.title || '')
        }
      })

      this.filteredBooks = filtered
    },
    truncate(text, length) {
      return text && text.length > length ? text.slice(0, length) + '...' : text
    }
  }
})
</script>

<style scoped>
.books {
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

.sort-selector {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.sort-selector select {
  padding: 0.75rem 1rem;
  border: none;
  background: white;
  font-size: 1rem;
  cursor: pointer;
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

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.book-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.book-cover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.book-info {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.book-author {
  color: #6366f1;
  font-size: 0.95rem;
  margin: 0 0 1rem 0;
}

.book-meta {
  margin-bottom: 1rem;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  display: flex;
  gap: 0.2rem;
}

.star {
  color: #d1d5db;
  font-size: 1rem;
}

.star.filled {
  color: #fbbf24;
}

.rating-text {
  color: #6b7280;
  font-size: 0.9rem;
}

.book-description {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
  flex: 1;
}

.book-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #667eea;
}

.availability {
  font-size: 0.85rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  background: #fee2e2;
  color: #dc2626;
}

.availability.available {
  background: #dcfce7;
  color: #16a34a;
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

  .books-grid {
    grid-template-columns: 1fr;
  }
}
</style>
