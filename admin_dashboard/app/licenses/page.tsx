'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { listLicenses, createLicense, revokeLicense, License, CreateLicenseData } from '@/lib/api'
import LicenseList from '@/components/LicenseList'
import LicenseForm from '@/components/LicenseForm'
import Toast from '@/components/Toast'
import ConfirmDialog from '@/components/ConfirmDialog'
import DashboardLayout from '@/components/DashboardLayout'

export default function LicensesPage() {
  const router = useRouter()
  const { user, loading: authLoading, isAdmin, getToken } = useAuth()
  const [licenses, setLicenses] = useState<License[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)
  const [revokeDialog, setRevokeDialog] = useState<{ isOpen: boolean; licenseId: string | null }>({
    isOpen: false,
    licenseId: null,
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

  const loadLicenses = async () => {
    if (!isAuthenticated) return
    try {
      setLoading(true)
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      const data = await listLicenses(search || undefined, statusFilter || undefined, token)
      setLicenses(data)
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to load licenses', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!isAuthenticated) return
    const debounce = setTimeout(() => {
      loadLicenses()
    }, 300)
    return () => clearTimeout(debounce)
  }, [search, statusFilter, isAuthenticated])

  const handleCreate = async (data: CreateLicenseData) => {
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      await createLicense(data, token)
      setShowCreateForm(false)
      setToast({ message: 'License created successfully', type: 'success' })
      loadLicenses()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to create license', type: 'error' })
      throw error
    }
  }

  const handleRevoke = async () => {
    if (!revokeDialog.licenseId) return
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      await revokeLicense(revokeDialog.licenseId, token)
      setRevokeDialog({ isOpen: false, licenseId: null })
      setToast({ message: 'License revoked successfully', type: 'success' })
      loadLicenses()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to revoke license', type: 'error' })
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
      <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Licenses</h2>
            <button
              onClick={() => setShowCreateForm(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
            >
              Create License
            </button>
          </div>

          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search by license key or customer name..."
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="">All</option>
                  <option value="active">Active</option>
                  <option value="revoked">Revoked</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>
            </div>
          </div>

          {showCreateForm && (
            <div className="bg-white shadow-lg rounded-xl p-8 mb-6 border border-gray-100">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Create New License</h3>
              <LicenseForm
                onSubmit={handleCreate}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          )}

          <div className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">
            <LicenseList
              licenses={licenses}
              onRevoke={(id) => setRevokeDialog({ isOpen: true, licenseId: id })}
              onCopy={(licenseKey) => setToast({ message: 'License key copied to clipboard!', type: 'success' })}
            />
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
        isOpen={revokeDialog.isOpen}
        title="Revoke License"
        message="Are you sure you want to revoke this license? This action cannot be undone."
        confirmText="Revoke"
        cancelText="Cancel"
        danger
        onConfirm={handleRevoke}
        onCancel={() => setRevokeDialog({ isOpen: false, licenseId: null })}
      />
    </DashboardLayout>
  )
}
