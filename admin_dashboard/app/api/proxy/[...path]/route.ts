import { NextRequest, NextResponse } from 'next/server'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params, 'GET')
}

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params, 'POST')
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params, 'PUT')
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleRequest(request, params, 'DELETE')
}

async function handleRequest(
  request: NextRequest,
  params: { path: string[] },
  method: string
) {
  try {
    const path = params.path.join('/')
    const url = new URL(request.url)
    const searchParams = url.searchParams.toString()
    const queryString = searchParams ? `?${searchParams}` : ''

    const targetUrl = `${LICENSE_SERVER_URL}/${path}${queryString}`

    // Get headers from request
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    // Forward Authorization header if present
    const authHeader = request.headers.get('Authorization')
    if (authHeader) {
      headers['Authorization'] = authHeader
    }

    // Get body for POST/PUT requests
    let body: string | undefined
    if (method === 'POST' || method === 'PUT') {
      try {
        body = await request.text()
      } catch (e) {
        // No body
      }
    }

    // Make request to License Server
    const response = await fetch(targetUrl, {
      method,
      headers,
      body,
    })

    // Get response data
    const data = await response.text()
    let jsonData: any
    try {
      jsonData = JSON.parse(data)
    } catch {
      jsonData = data
    }

    // Return response with CORS headers
    return NextResponse.json(jsonData, {
      status: response.status,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    })
  } catch (error: any) {
    console.error('Proxy error:', error)
    return NextResponse.json(
      { detail: error.message || 'Proxy error' },
      { status: 500 }
    )
  }
}
