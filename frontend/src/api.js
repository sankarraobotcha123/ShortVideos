const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      message = body.detail || message
    } catch (_) {
      // Keep default message.
    }
    throw new Error(message)
  }

  if (response.status === 204) return null
  return response.json()
}

export function fetchPackages() {
  return request('/api/packages')
}

export function fetchPackage(id) {
  return request(`/api/content/${id}`)
}

export function generateContent(payload) {
  return request('/api/content/generate', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateReview(id, payload) {
  return request(`/api/content/${id}/review`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function addAnalytics(id, payload) {
  return request(`/api/content/${id}/analytics`, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function fetchAiSettings() {
  return request('/api/settings/ai')
}

export function exportUrl(id) {
  return `${API_BASE_URL}/content/${id}/export`
}
