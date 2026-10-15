/**
 * Centralized API configuration.
 * 
 * In Docker / production, set the NEXT_PUBLIC_API_BASE environment variable
 * to point to your backend URL (e.g., "http://backend:8000/api/v1").
 * 
 * For local development, it defaults to http://localhost:8000/api/v1.
 */

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1';

/**
 * Returns an Authorization header object if an access token exists in localStorage.
 */
export function authHeader() {
  if (typeof window === 'undefined') return {};
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}
