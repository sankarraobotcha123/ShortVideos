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

export function assignPackageBatch(id, payload) {
  return request(`/api/content/${id}/batch`, {
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

export function fetchBatches() {
  return request('/api/batches')
}

export function createBatch(payload) {
  return request('/api/batches', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function fetchBatch(id) {
  return request(`/api/batches/${id}`)
}

export function updateBatch(id, payload) {
  return request(`/api/batches/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function fetchCalendar() {
  return request('/api/calendar')
}

export function createCalendarEntry(payload) {
  return request('/api/calendar', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateCalendarEntry(id, payload) {
  return request(`/api/calendar/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function deleteCalendarEntry(id) {
  return request(`/api/calendar/${id}`, {
    method: 'DELETE'
  })
}

export function generateAudio(id) {
  return request(`/api/content/${id}/audio`, {
    method: 'POST'
  })
}

export function generateAssembly(id) {
  return request(`/api/content/${id}/assembly`, {
    method: 'POST'
  })
}

export function generateVideoDraft(id) {
  return request(`/api/content/${id}/video-draft`, {
    method: 'POST'
  })
}

export function videoDraftDownloadUrl(packageId, draftId) {
  return `${API_BASE_URL}/content/${packageId}/video-draft/${draftId}/download`
}

export function assemblyDownloadUrl(packageId, planId) {
  return `${API_BASE_URL}/content/${packageId}/assembly/${planId}/download`
}

export function fetchAudioSettings() {
  return request('/api/settings/audio')
}

export function audioDownloadUrl(packageId, assetId) {
  return `${API_BASE_URL}/content/${packageId}/audio/${assetId}/download`
}

export function fetchAiSettings() {
  return request('/api/settings/ai')
}

export function exportUrl(id) {
  return `${API_BASE_URL}/content/${id}/export`
}
