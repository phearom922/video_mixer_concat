const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export interface License {
  id: string
  license_key: string
  customer_name?: string
  max_activations: number
  status: 'active' | 'revoked' | 'suspended'
  expires_at?: string
  notes?: string
  created_at: string
  updated_at: string
}

export interface Activation {
  id: string
  license_id: string
  device_id_hash: string
  device_label?: string
  first_activated_at: string
  last_seen_at: string
  status: 'active' | 'revoked'
  activated_app_version: string
  created_at: string
  updated_at: string
}

export interface Release {
  id: string
  platform: string
  version: string
  release_notes?: string
  download_url: string
  is_latest: boolean
  created_at: string
}

export interface CreateLicenseData {
  customer_name?: string
  max_activations: number
  status?: 'active' | 'revoked' | 'suspended'
  expires_at?: string
  notes?: string
}

export interface CreateReleaseData {
  platform: string
  version: string
  release_notes?: string
  download_url: string
  is_latest: boolean
}

export interface UpdateReleaseData {
  platform?: string
  release_notes?: string
  download_url?: string
  is_latest?: boolean
}

async function apiRequest(
  endpoint: string,
  options: RequestInit = {},
  token?: string
): Promise<Response> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  return response
}

// License APIs
export async function createLicense(
  data: CreateLicenseData,
  token: string
): Promise<License> {
  const response = await apiRequest('/admin/licenses', {
    method: 'POST',
    body: JSON.stringify(data),
  }, token)
  return response.json()
}

export async function listLicenses(
  search?: string,
  statusFilter?: string,
  token?: string
): Promise<License[]> {
  const params = new URLSearchParams()
  if (search) params.append('search', search)
  if (statusFilter) params.append('status_filter', statusFilter)
  
  const response = await apiRequest(
    `/admin/licenses?${params.toString()}`,
    {},
    token
  )
  return response.json()
}

export async function getLicense(id: string, token: string): Promise<License> {
  const response = await apiRequest(`/admin/licenses/${id}`, {}, token)
  return response.json()
}

export async function revokeLicense(id: string, token: string): Promise<void> {
  await apiRequest(`/admin/licenses/${id}/revoke`, { method: 'POST' }, token)
}

// Activation APIs
export async function getLicenseActivations(
  licenseId: string,
  token: string
): Promise<Activation[]> {
  const response = await apiRequest(
    `/admin/licenses/${licenseId}/activations`,
    {},
    token
  )
  return response.json()
}

export async function revokeActivation(
  activationId: string,
  token: string
): Promise<void> {
  await apiRequest(
    `/admin/activations/${activationId}/revoke`,
    { method: 'POST' },
    token
  )
}

// Release APIs
export async function createRelease(
  data: CreateReleaseData,
  token: string
): Promise<Release> {
  const response = await apiRequest('/admin/releases', {
    method: 'POST',
    body: JSON.stringify(data),
  }, token)
  return response.json()
}

export async function listReleases(
  platform?: string,
  token?: string
): Promise<Release[]> {
  const params = new URLSearchParams()
  if (platform) params.append('platform', platform)
  
  const response = await apiRequest(
    `/admin/releases?${params.toString()}`,
    {},
    token
  )
  return response.json()
}

export async function updateRelease(
  releaseId: string,
  data: UpdateReleaseData,
  token: string
): Promise<Release> {
  const response = await apiRequest(`/admin/releases/${releaseId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }, token)
  return response.json()
}

export async function setLatestRelease(
  releaseId: string,
  token: string
): Promise<void> {
  await apiRequest(
    `/admin/releases/${releaseId}/set-latest`,
    { method: 'POST' },
    token
  )
}
