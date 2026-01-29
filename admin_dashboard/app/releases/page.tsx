'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import {
  listReleases,
  createRelease,
  updateRelease,
  setLatestRelease,
  Release,
  CreateReleaseData,
  UpdateReleaseData,
} from '@/lib/api'
import ReleaseForm from '@/components/ReleaseForm'
import Toast from '@/components/Toast'
import ConfirmDialog from '@/components/ConfirmDialog'
import DashboardLayout from '@/components/DashboardLayout'

export default function ReleasesPage() {
  const router = useRouter()
  const { user, loading: authLoading, isAdmin, getToken } = useAuth()
  const [releases, setReleases] = useState<Release[]>([])
  const [loading, setLoading] = useState(true)
  const [platformFilter, setPlatformFilter] = useState<string>('windows')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [editingRelease, setEditingRelease] = useState<Release | null>(null)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)
  const [setLatestDialog, setSetLatestDialog] = useState<{ isOpen: boolean; releaseId: string | null }>({
    isOpen: false,
    releaseId: null,
  })

  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    if (!authLoading) {
      if (!user || !isAdmin()) {
        router.push('/login')
        return
      }
      setIsAuthenticated(true)
    }
  }, [user, authLoading, router])

  const loadReleases = async () => {
    if (!isAuthenticated) return
    try {
      setLoading(true)
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      const data = await listReleases(platformFilter || undefined, token)
      setReleases(data)
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to load releases', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!isAuthenticated) return
    loadReleases()
  }, [isAuthenticated, platformFilter])

  const handleCreate = async (data: CreateReleaseData) => {
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      await createRelease(data, token)
      setShowCreateForm(false)
      setToast({ message: 'Release created successfully', type: 'success' })
      loadReleases()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to create release', type: 'error' })
      throw error
    }
  }

  const handleUpdate = async (data: UpdateReleaseData | CreateReleaseData) => {
    if (!editingRelease) return
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      // Only send fields that are provided (for update)
      const updateData: UpdateReleaseData = {}
      if ('platform' in data && data.platform !== undefined) updateData.platform = data.platform
      if ('release_notes' in data && data.release_notes !== undefined) updateData.release_notes = data.release_notes
      if ('download_url' in data && data.download_url !== undefined) updateData.download_url = data.download_url
      if ('is_latest' in data && data.is_latest !== undefined) updateData.is_latest = data.is_latest
      
      await updateRelease(editingRelease.id, updateData, token)
      setEditingRelease(null)
      setToast({ message: 'Release updated successfully', type: 'success' })
      loadReleases()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to update release', type: 'error' })
      throw error
    }
  }

  const handleSetLatest = async () => {
    if (!setLatestDialog.releaseId) return
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      await setLatestRelease(setLatestDialog.releaseId, token)
      setSetLatestDialog({ isOpen: false, releaseId: null })
      setToast({ message: 'Release set as latest successfully', type: 'success' })
      loadReleases()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to set latest release', type: 'error' })
    }
  }

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    )
  }

  return (
    <DashboardLayout>
      <div className="max-w-full mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Releases</h2>
            <button
              onClick={() => setShowCreateForm(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
            >
              Create Release
            </button>
          </div>

          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Platform</label>
              <select
                value={platformFilter}
                onChange={(e) => setPlatformFilter(e.target.value)}
                className="w-full md:w-auto rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              >
                <option value="">All Platforms</option>
                <option value="windows">Windows</option>
              </select>
            </div>
          </div>

          {showCreateForm && (
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h3 className="text-lg font-medium mb-4">Create New Release</h3>
              <ReleaseForm
                onSubmit={handleCreate}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          )}

          {editingRelease && (
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h3 className="text-lg font-medium mb-4">Edit Release {editingRelease.version}</h3>
              <ReleaseForm
                onSubmit={handleUpdate}
                onCancel={() => setEditingRelease(null)}
                initialData={editingRelease}
                isEditMode={true}
              />
            </div>
          )}

          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Platform
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Version
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Release Notes
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Download URL
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Latest
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {releases.map((release) => (
                    <tr key={release.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {release.platform}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {release.version}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 max-w-md">
                        <div className="truncate" title={release.release_notes || ''}>
                          {release.release_notes || '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <a
                          href={release.download_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo-600 hover:text-indigo-900 truncate block max-w-xs"
                        >
                          {release.download_url}
                        </a>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {release.is_latest ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            Latest
                          </span>
                        ) : (
                          <span className="text-sm text-gray-500">-</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(release.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-3">
                          <button
                            onClick={() => setEditingRelease(release)}
                            className="text-indigo-600 hover:text-indigo-900"
                          >
                            Edit
                          </button>
                          {!release.is_latest && (
                            <button
                              onClick={() => setSetLatestDialog({ isOpen: true, releaseId: release.id })}
                              className="text-indigo-600 hover:text-indigo-900"
                            >
                              Set Latest
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {releases.length === 0 && (
                <div className="text-center py-12 text-gray-500">No releases found</div>
              )}
            </div>
          </div>
        </div>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <ConfirmDialog
        isOpen={setLatestDialog.isOpen}
        title="Set as Latest Release"
        message="This will unset the current latest release for this platform and set this one as the latest. Continue?"
        confirmText="Set Latest"
        cancelText="Cancel"
        onConfirm={handleSetLatest}
        onCancel={() => setSetLatestDialog({ isOpen: false, releaseId: null })}
      />
    </DashboardLayout>
  )
}
