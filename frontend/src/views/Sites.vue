<template>
  <div class="sites">
    <div class="page-header">
      <h1>Scraped Sites</h1>
      <p>Overview of all the websites we've scraped data from</p>
    </div>

    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search sites..."
          @input="filterSites"
        >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M14 14l4 4" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading sites...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h2>Unable to Load Sites</h2>
      <p>{{ error }}</p>
      <button @click="loadSites">Retry</button>
    </div>

    <div v-else-if="filteredSites.length === 0" class="empty-state">
      <div class="empty-icon">🌐</div>
      <h2>No sites found</h2>
      <p>Try adjusting your search</p>
    </div>

    <div v-else class="sites-grid">
      <div v-for="(site, index) in filteredSites" :key="index" class="site-card">
        <div class="site-header">
          <div class="site-icon">{{ getSiteEmoji(site.name) }}</div>
          <h3>{{ site.name }}</h3>
        </div>

        <div class="site-url">
          <a :href="site.url" target="_blank" rel="noopener noreferrer">
            {{ site.url }}
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 13H13V3H8.5M13 3L3 13" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </a>
        </div>

        <div class="site-info">
          <div class="info-item">
            <label>Data Type</label>
            <span>{{ site.dataType }}</span>
          </div>
          <div class="info-item">
            <label>Records</label>
            <span class="badge">{{ site.recordCount || '—' }}</span>
          </div>
          <div class="info-item">
            <label>Status</label>
            <span class="status-badge" :class="{active: site.active !== false}">
              {{ site.active !== false ? '✓ Active' : '✗ Inactive' }}
            </span>
          </div>
        </div>

        <p class="site-description" v-if="site.description">
          {{ site.description }}
        </p>

        <div class="site-tags" v-if="site.tags && site.tags.length">
          <span v-for="tag in site.tags" :key="tag" class="tag">
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <div class="stats">
      <p>Showing {{ filteredSites.length }} of {{ allSites.length }} sites</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Sites',
  data() {
    return {
      allSites: [],
      filteredSites: [],
      searchQuery: '',
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadSites()
  },
  methods: {
    async loadSites() {
      try {
        this.loading = true
        this.error = null
        const response = await fetch('http://localhost:5000/api/data')
        
        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`)
        }
        
        const data = await response.json()
        
        // Extract unique sites from the data
        const sites = [
          {
            name: 'Quote Scraper',
            url: 'http://quotes.toscrape.com',
            dataType: 'Quotes',
            recordCount: (data.data?.quotes || []).length,
            active: true,
            description: 'A website to scrape quotes from famous people',
            tags: ['quotes', 'sayings', 'famous-people']
          },
          {
            name: 'Book Scraper',
            url: 'http://books.toscrape.com',
            dataType: 'Books',
            recordCount: (data.data?.books || []).length,
            active: true,
            description: 'Browse and scrape book information and prices',
            tags: ['books', 'fiction', 'ecommerce']
          },
          {
            name: 'Scrape This Site',
            url: 'http://scrapethissite.com',
            dataType: 'Mixed',
            recordCount: (data.data?.hockey_teams || []).length,
            active: true,
            description: 'A sandbox website for learning web scraping',
            tags: ['sandbox', 'tutorial', 'practice', 'hockey']
          }
        ]

        this.allSites = sites
        this.filteredSites = [...sites]
      } catch (error) {
        console.error('Failed to load sites:', error)
        this.error = `Unable to load sites: ${error.message}`
        this.allSites = []
        this.filteredSites = []
      } finally {
        this.loading = false
      }
    },
    filterSites() {
      const query = this.searchQuery.toLowerCase()
      this.filteredSites = this.allSites.filter(site => {
        return site.name.toLowerCase().includes(query) ||
               site.url.toLowerCase().includes(query) ||
               site.description.toLowerCase().includes(query) ||
               (site.tags && site.tags.some(tag => tag.includes(query)))
      })
    },
    getSiteEmoji(name) {
      const emojiMap = {
        'Quote Scraper': '💬',
        'Book Scraper': '📚',
        'Scrape This Site': '🕸️'
      }
      return emojiMap[name] || '🌐'
    }
  }
})
</script>

<style scoped>
.sites {
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
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 500px;
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

.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.site-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.site-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.site-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.site-icon {
  font-size: 2.5rem;
}

.site-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.3rem;
}

.site-url {
  margin-bottom: 1rem;
}

.site-url a {
  color: #6366f1;
  text-decoration: none;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  word-break: break-all;
  transition: color 0.3s ease;
}

.site-url a:hover {
  color: #4f46e5;
}

.site-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.info-item {
  text-align: center;
}

.info-item label {
  display: block;
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}

.info-item span {
  display: block;
  color: #1f2937;
  font-weight: 600;
}

.badge {
  display: inline-block;
  background: #e0e7ff;
  color: #6366f1;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
  background: #fee2e2;
  color: #dc2626;
}

.status-badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.site-description {
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 1rem 0;
}

.site-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.tag {
  display: inline-block;
  background: #f3f4f6;
  color: #4b5563;
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
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

  .sites-grid {
    grid-template-columns: 1fr;
  }

  .site-info {
    grid-template-columns: 1fr;
  }
}
</style>
