'use client'

import { useState } from 'react'
import { License } from '@/lib/api'
import Link from 'next/link'

interface LicenseListProps {
  licenses: License[]
  onRevoke: (id: string) => void
  onCopy?: (licenseKey: string) => void
}

export default function LicenseList({ licenses, onRevoke, onCopy }: LicenseListProps) {
  const [copiedId, setCopiedId] = useState<string | null>(null)

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

  const handleCopy = async (licenseKey: string, licenseId: string) => {
    try {
      await navigator.clipboard.writeText(licenseKey)
      setCopiedId(licenseId)
      if (onCopy) {
        onCopy(licenseKey)
      }
      setTimeout(() => setCopiedId(null), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
          <tr>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              License Key
            </th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              Customer
            </th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              Max Activations
            </th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              Expires
            </th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {licenses.map((license) => (
            <tr key={license.id} className="hover:bg-gray-50 transition-colors duration-150">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center gap-2">
                  <Link
                    href={`/licenses/${license.id}`}
                    className="text-sm font-mono text-indigo-600 hover:text-indigo-700 font-medium transition-colors"
                  >
                    {license.license_key.substring(0, 20)}...
                  </Link>
                  <button
                    onClick={() => handleCopy(license.license_key, license.id)}
                    className="flex-shrink-0 inline-flex items-center justify-center w-7 h-7 rounded-md text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1"
                    title="Copy license key"
                  >
                    {copiedId === license.id ? (
                      <svg className="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    )}
                  </button>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                {license.customer_name || <span className="text-gray-400 italic">-</span>}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {license.max_activations}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                    license.status
                  )}`}
                >
                  {license.status.toUpperCase()}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                {license.expires_at
                  ? new Date(license.expires_at).toLocaleDateString()
                  : <span className="text-gray-400">Never</span>}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div className="flex items-center gap-3">
                  <Link
                    href={`/licenses/${license.id}`}
                    className="text-indigo-600 hover:text-indigo-700 font-medium transition-colors"
                  >
                    View
                  </Link>
                  {license.status !== 'revoked' && (
                    <button
                      onClick={() => onRevoke(license.id)}
                      className="text-red-600 hover:text-red-700 font-medium transition-colors"
                    >
                      Revoke
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {licenses.length === 0 && (
        <div className="text-center py-16">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="mt-4 text-sm text-gray-500">No licenses found</p>
        </div>
      )}
    </div>
  )
}
