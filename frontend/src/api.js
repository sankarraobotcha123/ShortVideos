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

export function generateThumbnailGuide(id) {
  return request(`/api/content/${id}/thumbnail`, {
    method: 'POST'
  })
}

export function thumbnailGuideDownloadUrl(packageId, guideId) {
  return `${API_BASE_URL}/content/${packageId}/thumbnail/${guideId}/download`
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

export function fetchVisualAssets() {
  return request('/api/assets')
}

export async function uploadVisualAsset(formData) {
  const response = await fetch(`${API_BASE_URL}/api/assets`, {
    method: 'POST',
    body: formData
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
  return response.json()
}

export function deleteVisualAsset(id) {
  return request(`/api/assets/${id}`, {
    method: 'DELETE'
  })
}

export function visualAssetUrl(id) {
  return `${API_BASE_URL}/assets/${id}/download`
}

export function generateSourceSafetyReview(id) {
  return request(`/api/content/${id}/source-safety`, {
    method: 'POST'
  })
}

export function sourceSafetyDownloadUrl(packageId, reviewId) {
  return `${API_BASE_URL}/content/${packageId}/source-safety/${reviewId}/download`
}

export function generateTrustReview(id) {
  return request(`/api/content/${id}/trust-review`, {
    method: 'POST'
  })
}

export function updateTrustReview(packageId, reviewId, payload) {
  return request(`/api/content/${packageId}/trust-review/${reviewId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function trustReviewDownloadUrl(packageId, reviewId) {
  return `${API_BASE_URL}/content/${packageId}/trust-review/${reviewId}/download`
}

export function fetchAiSettings() {
  return request('/api/settings/ai')
}

export function exportUrl(id) {
  return `${API_BASE_URL}/content/${id}/export`
}

export function generateLearningOutput(id) {
  return request(`/api/content/${id}/learning-output`, {
    method: 'POST'
  })
}

export function learningOutputDownloadUrl(packageId, outputId) {
  return `${API_BASE_URL}/content/${packageId}/learning-output/${outputId}/download`
}

export function fetchPromptTemplates(taskType = '') {
  const suffix = taskType ? `?task_type=${encodeURIComponent(taskType)}` : ''
  return request(`/api/prompt-templates${suffix}`)
}

export function seedPromptTemplates() {
  return request('/api/prompt-templates/seed', {
    method: 'POST'
  })
}

export function createPromptTemplate(payload) {
  return request('/api/prompt-templates', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updatePromptTemplate(id, payload) {
  return request(`/api/prompt-templates/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function deletePromptTemplate(id) {
  return request(`/api/prompt-templates/${id}`, {
    method: 'DELETE'
  })
}

export function previewPromptTemplate(id, payload) {
  return request(`/api/prompt-templates/${id}/preview`, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function fetchAnalyticsInsights() {
  return request('/api/analytics/insights')
}

export function fetchProviderLogs() {
  return request('/api/provider-logs')
}


export function fetchSystemReadiness() {
  return request('/api/system/readiness')
}

export function seedDemoData(resetDemo = false) {
  return request('/api/demo/seed', {
    method: 'POST',
    body: JSON.stringify({ reset_demo: resetDemo })
  })
}

export function fetchReleaseChecklist() {
  return request('/api/release/checklist')
}

export function releaseChecklistDownloadUrl() {
  return `${API_BASE_URL}/release/checklist/download`
}

export function fetchSetupGuide() {
  return request('/api/setup/guide')
}

export function setupGuideDownloadUrl() {
  return `${API_BASE_URL}/setup/guide/download`
}
