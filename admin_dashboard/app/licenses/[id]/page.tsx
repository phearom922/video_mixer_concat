'use client'

import { useEffect, useState, useRef, useCallback, useMemo } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import {
  getLicense,
  getLicenseActivations,
  revokeActivation,
  License,
  Activation,
} from '@/lib/api'
import ActivationTable from '@/components/ActivationTable'
import Toast from '@/components/Toast'
import ConfirmDialog from '@/components/ConfirmDialog'
import Link from 'next/link'
import DashboardLayout from '@/components/DashboardLayout'

export default function LicenseDetailPage() {
  const router = useRouter()
  const params = useParams()
  const { user, loading: authLoading, isAdmin, getToken } = useAuth()
  const [license, setLicense] = useState<License | null>(null)
  const [activations, setActivations] = useState<Activation[]>([])
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null)
  const [revokeDialog, setRevokeDialog] = useState<{ isOpen: boolean; activationId: string | null }>({
    isOpen: false,
    activationId: null,
  })
  const hasLoadedRef = useRef(false)
  
  // Memoize isAdmin result to prevent infinite loops
  const isUserAdmin = useMemo(() => {
    return user && isAdmin()
  }, [user, isAdmin])

  const loadData = useCallback(async () => {
    try {
      setLoading(true)
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      const licenseId = params.id as string
      const [licenseData, activationsData] = await Promise.all([
        getLicense(licenseId, token),
        getLicenseActivations(licenseId, token),
      ])
      setLicense(licenseData)
      setActivations(activationsData)
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to load license', type: 'error' })
    } finally {
      setLoading(false)
    }
  }, [params.id, getToken, router])

  // Check authentication and redirect if needed
  useEffect(() => {
    if (!authLoading) {
      if (!isUserAdmin) {
        router.push('/login')
        return
      }
    }
  }, [authLoading, isUserAdmin, router])

  // Load data only once when authenticated and params.id is available
  useEffect(() => {
    if (!authLoading && isUserAdmin && params.id && !hasLoadedRef.current) {
      hasLoadedRef.current = true
      loadData()
    }
  }, [authLoading, isUserAdmin, params.id, loadData])

  const handleRevokeActivation = async () => {
    if (!revokeDialog.activationId) return
    try {
      const token = await getToken()
      if (!token) {
        router.push('/login')
        return
      }
      await revokeActivation(revokeDialog.activationId, token)
      setRevokeDialog({ isOpen: false, activationId: null })
      setToast({ message: 'Activation revoked successfully', type: 'success' })
      await loadData()
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to revoke activation', type: 'error' })
    }
  }

  const handleCopyLicenseKey = async () => {
    if (!license) return
    try {
      await navigator.clipboard.writeText(license.license_key)
      setToast({ message: 'License key copied to clipboard!', type: 'success' })
    } catch (error) {
      setToast({ message: 'Failed to copy license key', type: 'error' })
    }
  }

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    )
  }

  if (!license) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500">License not found</p>
          <Link href="/licenses" className="text-indigo-600 hover:text-indigo-900 mt-4 inline-block">
            Back to Licenses
          </Link>
        </div>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-emerald-100 text-emerald-800 border border-emerald-200'
      case 'revoked':
        return 'bg-red-100 text-red-800 border border-red-200'
      case 'suspended':
        return 'bg-amber-100 text-amber-800 border border-amber-200'
      default:
        return 'bg-gray-100 text-gray-800 border border-gray-200'
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
          <Link
            href="/licenses"
            className="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-700 mb-6 font-medium transition-colors duration-200"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Licenses
          </Link>

          <div className="bg-white shadow-lg rounded-xl p-8 mb-6 border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold text-gray-900">License Details</h2>
            </div>
            <dl className="grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <dt className="text-sm font-semibold text-gray-700 mb-2">License Key</dt>
                <dd className="mt-1 flex items-center gap-3">
                  <code className="flex-1 text-sm text-gray-900 font-mono break-all bg-gray-50 px-4 py-3 rounded-lg border border-gray-200">
                    {license.license_key}
                  </code>
                  <button
                    onClick={handleCopyLicenseKey}
                    className="flex-shrink-0 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 hover:bg-indigo-100 hover:text-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    title="Copy license key"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-gray-700 mb-2">Customer Name</dt>
                <dd className="mt-1 text-base text-gray-900 font-medium">
                  {license.customer_name || <span className="text-gray-400 italic">Not specified</span>}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-gray-700 mb-2">Max Activations</dt>
                <dd className="mt-1 text-base text-gray-900 font-medium">{license.max_activations}</dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-gray-700 mb-2">Status</dt>
                <dd className="mt-1">
                  <span
                    className={`px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${getStatusColor(
                      license.status
                    )}`}
                  >
                    {license.status.toUpperCase()}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-gray-700 mb-2">Expires At</dt>
                <dd className="mt-1 text-base text-gray-900 font-medium">
                  {license.expires_at
                    ? new Date(license.expires_at).toLocaleString()
                    : <span className="text-gray-500">Never</span>}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-gray-700 mb-2">Created At</dt>
                <dd className="mt-1 text-base text-gray-900 font-medium">
                  {new Date(license.created_at).toLocaleString()}
                </dd>
              </div>
              {license.notes && (
                <div className="sm:col-span-2">
                  <dt className="text-sm font-semibold text-gray-700 mb-2">Notes</dt>
                  <dd className="mt-1 text-sm text-gray-900 bg-gray-50 px-4 py-3 rounded-lg border border-gray-200">{license.notes}</dd>
                </div>
              )}
            </dl>
          </div>

          <div className="bg-white shadow-lg rounded-xl p-8 border border-gray-100">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Activations</h3>
            <ActivationTable
              activations={activations}
              onRevoke={(id) => setRevokeDialog({ isOpen: true, activationId: id })}
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
        title="Revoke Activation"
        message="Are you sure you want to revoke this activation? The device will no longer be able to use the license."
        confirmText="Revoke"
        cancelText="Cancel"
        danger
        onConfirm={handleRevokeActivation}
        onCancel={() => setRevokeDialog({ isOpen: false, activationId: null })}
      />
    </DashboardLayout>
  )
}
