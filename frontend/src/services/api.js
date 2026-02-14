const API_BASE_URL = 'http://localhost:5000/api'

export async function fetchData() {
  try {
    const response = await fetch(`${API_BASE_URL}/data`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Failed to fetch data:', error)
    throw error
  }
}

export async function fetchQuotes() {
  try {
    const response = await fetch(`${API_BASE_URL}/quotes`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Failed to fetch quotes:', error)
    throw error
  }
}

export async function fetchBooks() {
  try {
    const response = await fetch(`${API_BASE_URL}/books`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Failed to fetch books:', error)
    throw error
  }
}

export async function fetchSites() {
  try {
    const response = await fetch(`${API_BASE_URL}/sites`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Failed to fetch sites:', error)
    throw error
  }
}
