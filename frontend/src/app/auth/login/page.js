'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Sparkles, Mail, Lock, LogIn } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('access_token', data.data.tokens.access_token);
        window.location.href = '/dashboard';
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Cannot connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cosmic-radial flex items-center justify-center p-6 relative overflow-hidden">
      <div className="w-full max-w-md bg-glass p-8 rounded-3xl shadow-2xl border border-white/10 relative z-10 backdrop-blur-xl">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-purple-500/30">
            <Sparkles className="w-6 h-6 text-amber-300" />
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
          <p className="text-sm text-gray-400 mt-1">Sign in to your spiritual intelligence portal</p>
        </div>

        {error && (
          <div className="mb-6 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs text-center font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Email Address</label>
            <div className="relative">
              <Mail className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 text-sm transition-all"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Password</label>
            <div className="relative">
              <Lock className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 text-sm transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg shadow-purple-600/30 transition-all flex items-center justify-center gap-2"
          >
            {loading ? 'Signing In...' : 'Sign In'}
            <LogIn className="w-4 h-4" />
          </button>
        </form>

        {/* Quick Demo Persona Sign-In */}
        <div className="mt-6 pt-6 border-t border-white/10">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Quick Persona Login (Real RBAC)
            </span>
            <span className="text-[10px] text-purple-400 font-semibold">1-Click Sign In</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            {[
              { email: 'seeker@mystic.ai', role: 'Seeker', color: 'border-purple-500/30 bg-purple-900/20 hover:bg-purple-900/40 text-purple-300' },
              { email: 'reader@mystic.ai', role: 'Tarot Reader', color: 'border-indigo-500/30 bg-indigo-900/20 hover:bg-indigo-900/40 text-indigo-300' },
              { email: 'consultant@mystic.ai', role: 'Consultant', color: 'border-emerald-500/30 bg-emerald-900/20 hover:bg-emerald-900/40 text-emerald-300' },
              { email: 'admin@mystic.ai', role: 'Super Admin', color: 'border-red-500/30 bg-red-900/20 hover:bg-red-900/40 text-red-300' },
            ].map((p) => (
              <button
                key={p.email}
                type="button"
                onClick={async () => {
                  setEmail(p.email);
                  setPassword('password123');
                  setLoading(true);
                  try {
                    const res = await fetch('http://localhost:8000/api/v1/auth/login', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ email: p.email, password: 'password123' })
                    });
                    const data = await res.json();
                    if (res.ok) {
                      localStorage.setItem('access_token', data.data.tokens.access_token);
                      window.location.href = '/dashboard';
                    } else {
                      setError(data.detail || 'Login failed');
                    }
                  } catch (e) {
                    setError('Cannot connect to server');
                  } finally {
                    setLoading(false);
                  }
                }}
                className={`p-2.5 rounded-xl border text-left text-xs font-semibold transition-all ${p.color}`}
              >
                <div className="font-bold">{p.role}</div>
                <div className="text-[10px] text-gray-400 truncate">{p.email}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="mt-8 text-center text-xs text-gray-400">
          Don&apos;t have an account?{' '}
          <Link href="/auth/register" className="text-purple-400 font-semibold hover:underline">
            Register now
          </Link>
        </div>
      </div>
    </div>
  );
}
