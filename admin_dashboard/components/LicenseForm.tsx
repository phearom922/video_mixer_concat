'use client'

import { useState, useEffect } from 'react'

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

type ExpirationPreset = '30' | '90' | '180' | '365' | '730' | 'custom'

export default function LicenseForm({ onSubmit, onCancel, initialData }: LicenseFormProps) {
  const [formData, setFormData] = useState<LicenseFormData>({
    customer_name: initialData?.customer_name || '',
    max_activations: initialData?.max_activations || 1,
    status: initialData?.status || 'active',
    expires_at: initialData?.expires_at || '',
    notes: initialData?.notes || '',
  })
  const [loading, setLoading] = useState(false)
  const [expirationMode, setExpirationMode] = useState<ExpirationPreset>('365')
  const [customDate, setCustomDate] = useState<string>('')
  const [errors, setErrors] = useState<Record<string, string>>({})

  // Calculate expiration date based on preset
  const calculateExpirationDate = (days: number): string => {
    const date = new Date()
    date.setDate(date.getDate() + days)
    // Format as YYYY-MM-DDTHH:mm for datetime-local input
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day}T${hours}:${minutes}`
  }

  // Update expires_at when expiration mode changes
  useEffect(() => {
    if (expirationMode === 'custom') {
      if (customDate) {
        setFormData((prev) => ({ ...prev, expires_at: customDate }))
      }
    } else {
      const days = parseInt(expirationMode)
      const expirationDate = calculateExpirationDate(days)
      setFormData((prev) => ({ ...prev, expires_at: expirationDate }))
    }
  }, [expirationMode, customDate])

  // Initialize expiration mode from initialData
  useEffect(() => {
    if (initialData?.expires_at) {
      // Try to detect if it matches a preset
      const initialDate = new Date(initialData.expires_at)
      const now = new Date()
      const diffDays = Math.floor((initialDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
      
      if (diffDays === 30) setExpirationMode('30')
      else if (diffDays === 90) setExpirationMode('90')
      else if (diffDays === 180) setExpirationMode('180')
      else if (diffDays === 365) setExpirationMode('365')
      else if (diffDays === 730) setExpirationMode('730')
      else {
        setExpirationMode('custom')
        // Format for datetime-local input
        const formatted = initialDate.toISOString().slice(0, 16)
        setCustomDate(formatted)
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}
    
    if (!formData.customer_name.trim()) {
      newErrors.customer_name = 'Customer name is required'
    }
    
    if (formData.max_activations < 1) {
      newErrors.max_activations = 'Max activations must be at least 1'
    }
    
    if (expirationMode === 'custom' && !customDate) {
      newErrors.expires_at = 'Please select a custom expiration date'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }
    
    setLoading(true)
    try {
      await onSubmit(formData)
    } finally {
      setLoading(false)
    }
  }

  const handleExpirationModeChange = (mode: ExpirationPreset) => {
    setExpirationMode(mode)
    setErrors({ ...errors, expires_at: '' })
  }

  const handleCustomDateChange = (date: string) => {
    setCustomDate(date)
    setFormData({ ...formData, expires_at: date })
    setErrors({ ...errors, expires_at: '' })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Customer Name */}
      <div>
        <label htmlFor="customer_name" className="block text-sm font-medium text-gray-700 mb-1">
          Customer Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="customer_name"
          value={formData.customer_name}
          onChange={(e) => {
            setFormData({ ...formData, customer_name: e.target.value })
            setErrors({ ...errors, customer_name: '' })
          }}
          placeholder="Enter customer name"
          required
          className={`mt-1 block w-full rounded-md border ${
            errors.customer_name ? 'border-red-300' : 'border-gray-300'
          } shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2`}
        />
        {errors.customer_name && (
          <p className="mt-1 text-sm text-red-600">{errors.customer_name}</p>
        )}
      </div>

      {/* Max Activations */}
      <div>
        <label htmlFor="max_activations" className="block text-sm font-medium text-gray-700 mb-1">
          Max Activations <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          id="max_activations"
          min="1"
          max="1000"
          value={formData.max_activations}
          onChange={(e) => {
            const value = parseInt(e.target.value) || 1
            setFormData({ ...formData, max_activations: value })
            setErrors({ ...errors, max_activations: '' })
          }}
          placeholder="1"
          required
          className={`mt-1 block w-full rounded-md border ${
            errors.max_activations ? 'border-red-300' : 'border-gray-300'
          } shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2`}
        />
        {errors.max_activations && (
          <p className="mt-1 text-sm text-red-600">{errors.max_activations}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">Number of devices that can activate this license</p>
      </div>

      {/* Status */}
      <div>
        <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
          Status <span className="text-red-500">*</span>
        </label>
        <select
          id="status"
          value={formData.status}
          onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
          className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 bg-white"
        >
          <option value="active">Active</option>
          <option value="revoked">Revoked</option>
          <option value="suspended">Suspended</option>
        </select>
        <p className="mt-1 text-xs text-gray-500">License activation status</p>
      </div>

      {/* Expiration Date */}
      <div>
        <label htmlFor="expiration_mode" className="block text-sm font-medium text-gray-700 mb-1">
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Expiration Date
          </span>
        </label>
        <select
          id="expiration_mode"
          value={expirationMode}
          onChange={(e) => handleExpirationModeChange(e.target.value as ExpirationPreset)}
          className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 bg-white"
        >
          <option value="30">30 days</option>
          <option value="90">90 days (3 months)</option>
          <option value="180">180 days (6 months)</option>
          <option value="365">365 days (1 year)</option>
          <option value="730">730 days (2 years)</option>
          <option value="custom">Custom</option>
        </select>
        
        {expirationMode === 'custom' && (
          <div className="mt-3">
            <input
              type="datetime-local"
              id="expires_at"
              value={customDate}
              onChange={(e) => handleCustomDateChange(e.target.value)}
              min={new Date().toISOString().slice(0, 16)}
              className={`block w-full rounded-md border ${
                errors.expires_at ? 'border-red-300' : 'border-gray-300'
              } shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2`}
            />
            {errors.expires_at && (
              <p className="mt-1 text-sm text-red-600">{errors.expires_at}</p>
            )}
          </div>
        )}
        
        {expirationMode !== 'custom' && formData.expires_at && (
          <p className="mt-2 text-xs text-gray-500">
            Expires on: {new Date(formData.expires_at).toLocaleString()}
          </p>
        )}
      </div>

      {/* Notes */}
      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
          Notes
        </label>
        <textarea
          id="notes"
          rows={3}
          value={formData.notes}
          onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          placeholder="Optional notes about this license..."
          className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 resize-none"
        />
        <p className="mt-1 text-xs text-gray-500">Optional notes for internal reference</p>
      </div>

      <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            </span>
          ) : (
            'Create License'
          )}
        </button>
      </div>
    </form>
  )
}
