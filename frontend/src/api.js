const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')
const AUTH_TOKEN_KEY = 'edu_content_auth_token'
const AUTH_USER_KEY = 'edu_content_auth_user'

export function getAuthToken() {
  return window.localStorage.getItem(AUTH_TOKEN_KEY) || ''
}

export function getStoredAuthUser() {
  try {
    const raw = window.localStorage.getItem(AUTH_USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (_) {
    return null
  }
}

export function clearAuthToken() {
  window.localStorage.removeItem(AUTH_TOKEN_KEY)
  window.localStorage.removeItem(AUTH_USER_KEY)
}

function authHeaders() {
  const token = getAuthToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers || {})
    },
    ...options
  })

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken()
      window.dispatchEvent(new CustomEvent('auth:expired'))
    }
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

export async function loginUser(payload) {
  const data = await request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
  if (data.access_token) {
    window.localStorage.setItem(AUTH_TOKEN_KEY, data.access_token)
    window.localStorage.setItem(AUTH_USER_KEY, JSON.stringify(data.user))
  }
  return data
}

export async function logoutUser() {
  try {
    return await request('/api/auth/logout', { method: 'POST' })
  } finally {
    clearAuthToken()
  }
}

export async function fetchCurrentUser() {
  const data = await request('/api/auth/me')
  if (data.user) {
    window.localStorage.setItem(AUTH_USER_KEY, JSON.stringify(data.user))
  } else {
    window.localStorage.removeItem(AUTH_USER_KEY)
  }
  return data
}

export function fetchAuthStatus() {
  return request('/api/auth/status')
}

export function fetchAuthPermissions() {
  return request('/api/auth/permissions')
}

export function fetchAuthHardening() {
  return request('/api/auth/hardening')
}

export function cleanupAuthSessions() {
  return request('/api/auth/sessions/cleanup', { method: 'POST' })
}

export function changeAuthPassword(payload) {
  return request('/api/auth/change-password', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function fetchAuthUsers() {
  return request('/api/auth/users')
}

export function createAuthUser(payload) {
  return request('/api/auth/users', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateAuthUser(id, payload) {
  return request(`/api/auth/users/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
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
    credentials: 'same-origin',
    headers: authHeaders(),
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

export function generatePublishingApproval(id) {
  return request(`/api/content/${id}/publishing-approval`, {
    method: 'POST'
  })
}

export function updatePublishingApproval(packageId, approvalId, payload) {
  return request(`/api/content/${packageId}/publishing-approval/${approvalId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function publishingApprovalDownloadUrl(packageId, approvalId) {
  return `${API_BASE_URL}/content/${packageId}/publishing-approval/${approvalId}/download`
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

export function fetchProductionBoard() {
  return request('/api/production-board')
}

export function updateProductionCard(packageId, payload) {
  return request(`/api/production-board/cards/${packageId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function productionBoardDownloadUrl() {
  return `${API_BASE_URL}/production-board/download`
}
