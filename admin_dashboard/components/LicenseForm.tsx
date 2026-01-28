'use client'

import { useState } from 'react'

interface LicenseFormData {
  customer_name: string
  max_activations: number
  status: 'active' | 'revoked' | 'suspended'
  expires_at: string
  notes: string
}

interface LicenseFormProps {
  onSubmit: (data: LicenseFormData) => Promise<void>
  onCancel: () => void
  initialData?: Partial<LicenseFormData>
}

export default function LicenseForm({ onSubmit, onCancel, initialData }: LicenseFormProps) {
  const [formData, setFormData] = useState<LicenseFormData>({
    customer_name: initialData?.customer_name || '',
    max_activations: initialData?.max_activations || 1,
    status: initialData?.status || 'active',
    expires_at: initialData?.expires_at || '',
    notes: initialData?.notes || '',
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
        <label htmlFor="customer_name" className="block text-sm font-medium text-gray-700">
          Customer Name
        </label>
        <input
          type="text"
          id="customer_name"
          value={formData.customer_name}
          onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="max_activations" className="block text-sm font-medium text-gray-700">
          Max Activations
        </label>
        <input
          type="number"
          id="max_activations"
          min="1"
          value={formData.max_activations}
          onChange={(e) => setFormData({ ...formData, max_activations: parseInt(e.target.value) || 1 })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="status" className="block text-sm font-medium text-gray-700">
          Status
        </label>
        <select
          id="status"
          value={formData.status}
          onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        >
          <option value="active">Active</option>
          <option value="revoked">Revoked</option>
          <option value="suspended">Suspended</option>
        </select>
      </div>

      <div>
        <label htmlFor="expires_at" className="block text-sm font-medium text-gray-700">
          Expires At (optional)
        </label>
        <input
          type="datetime-local"
          id="expires_at"
          value={formData.expires_at}
          onChange={(e) => setFormData({ ...formData, expires_at: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
          Notes
        </label>
        <textarea
          id="notes"
          rows={3}
          value={formData.notes}
          onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
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
