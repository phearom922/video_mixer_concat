'use client'

import { useState } from 'react'

interface ReleaseFormData {
  platform: string
  version: string
  release_notes: string
  download_url: string
  is_latest: boolean
}

interface ReleaseFormProps {
  onSubmit: (data: ReleaseFormData) => Promise<void>
  onCancel: () => void
  initialData?: Partial<ReleaseFormData>
}

export default function ReleaseForm({ onSubmit, onCancel, initialData }: ReleaseFormProps) {
  const [formData, setFormData] = useState<ReleaseFormData>({
    platform: initialData?.platform || 'windows',
    version: initialData?.version || '',
    release_notes: initialData?.release_notes || '',
    download_url: initialData?.download_url || '',
    is_latest: initialData?.is_latest ?? false,
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onSubmit(formData)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="platform" className="block text-sm font-medium text-gray-700">
          Platform
        </label>
        <select
          id="platform"
          value={formData.platform}
          onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        >
          <option value="windows">Windows</option>
        </select>
      </div>

      <div>
        <label htmlFor="version" className="block text-sm font-medium text-gray-700">
          Version (semver, e.g., 1.2.3)
        </label>
        <input
          type="text"
          id="version"
          required
          value={formData.version}
          onChange={(e) => setFormData({ ...formData, version: e.target.value })}
          placeholder="1.0.0"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="download_url" className="block text-sm font-medium text-gray-700">
          Download URL
        </label>
        <input
          type="url"
          id="download_url"
          required
          value={formData.download_url}
          onChange={(e) => setFormData({ ...formData, download_url: e.target.value })}
          placeholder="https://example.com/download/v1.0.0.exe"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="release_notes" className="block text-sm font-medium text-gray-700">
          Release Notes
        </label>
        <textarea
          id="release_notes"
          rows={6}
          value={formData.release_notes}
          onChange={(e) => setFormData({ ...formData, release_notes: e.target.value })}
          placeholder="What's new in this version..."
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div className="flex items-center">
        <input
          id="is_latest"
          type="checkbox"
          checked={formData.is_latest}
          onChange={(e) => setFormData({ ...formData, is_latest: e.target.checked })}
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <label htmlFor="is_latest" className="ml-2 block text-sm text-gray-900">
          Set as latest release for this platform
        </label>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? 'Saving...' : 'Save'}
        </button>
      </div>
    </form>
  )
}
