'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function AuthCallback() {
  const router = useRouter()

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const console_token = params.get('console_token') || ''
    const refresh_token = params.get('refresh_token') || ''

    if (console_token) {
      localStorage.setItem('console_token', console_token)
      localStorage.setItem('refresh_token', refresh_token)

      // Remove sensitive tokens from the URL to reduce leakage risk
      window.history.replaceState({}, document.title, window.location.pathname)

      router.replace('/')
    } else {
      router.replace('/signin?error=missing-jwt')
    }
  }, [router])

  return <div>Logging you in...</div>
}