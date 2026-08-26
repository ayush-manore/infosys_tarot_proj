'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, Hand, CreditCard, User, LogOut, Compass, TrendingUp, Award, Calendar, Activity } from 'lucide-react';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/auth/login';
      return;
    }

    fetch('http://localhost:8000/api/v1/users/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setUser(data.data);
        } else {
          localStorage.removeItem('access_token');
          window.location.href = '/auth/login';
        }
      })
      .catch(() => {
        setUser({ email: 'demo@mystic.ai', role: { name: 'user' } });
      })
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/auth/login';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-cosmic-radial flex items-center justify-center">
        <div className="flex items-center gap-3 text-purple-400 font-medium">
          <Sparkles className="w-6 h-6 animate-spin text-amber-400" />
          Loading your spiritual portal...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cosmic-radial flex flex-col">
      {/* Top Header */}
      <header className="bg-cosmic-950/80 border-b border-white/10 px-8 py-4 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <Sparkles className="w-5 h-5 text-amber-300" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
            MysticAI Portal
          </span>
        </div>

        <div className="flex items-center gap-6">
          <Link href="/profile" className="flex items-center gap-2 text-sm text-gray-300 hover:text-white transition-colors">
            <User className="w-4 h-4 text-purple-400" />
            Profile
          </Link>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-sm text-red-400 hover:text-red-300 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8 space-y-8">
        {/* Welcome Greeting Banner */}
        <div className="bg-glass-card p-8 rounded-3xl border border-white/10 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px] pointer-events-none" />
          <div className="relative z-10">
            <span className="text-xs font-semibold text-purple-400 uppercase tracking-widest">Spiritual Dashboard</span>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-2">
              Welcome back, <span className="text-amber-300">{user?.email?.split('@')[0] || 'Seeker'}</span> ✨
            </h1>
            <p className="text-gray-400 text-sm mt-2 max-w-2xl">
              Role: <span className="capitalize text-purple-300 font-semibold">{user?.role?.name || 'User'}</span> | All spiritual intelligence modules operational.
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-glass p-5 rounded-2xl border border-white/10">
            <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
              Total Readings
              <Activity className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-2xl font-extrabold text-white mt-2">12</div>
            <div className="text-xs text-purple-300 mt-1">8 Palm / 4 Tarot</div>
          </div>

          <div className="bg-glass p-5 rounded-2xl border border-white/10">
            <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
              Insight Score
              <Award className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-extrabold text-amber-300 mt-2">88%</div>
            <div className="text-xs text-gray-400 mt-1">Weighted confidence</div>
          </div>

          <div className="bg-glass p-5 rounded-2xl border border-white/10">
            <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
              Growth Trend
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-extrabold text-emerald-400 mt-2">+15%</div>
            <div className="text-xs text-gray-400 mt-1">Self-alignment score</div>
          </div>

          <div className="bg-glass p-5 rounded-2xl border border-white/10">
            <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
              Active Streak
              <Calendar className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-2xl font-extrabold text-indigo-300 mt-2">4 Days</div>
            <div className="text-xs text-gray-400 mt-1">Daily guidance check</div>
          </div>
        </div>

        {/* Action Modules */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Start Palm Scan Card */}
          <div className="bg-gradient-to-br from-purple-950/60 to-cosmic-900 border border-purple-500/30 p-6 rounded-3xl hover:border-purple-500/60 transition-all group">
            <div className="w-12 h-12 rounded-2xl bg-purple-900/50 border border-purple-500/40 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
              <Hand className="w-6 h-6 text-purple-300" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Palm Analysis Workflow</h3>
            <p className="text-sm text-gray-400 mb-6">
              Upload or capture palm image for line extraction (Life, Head, Heart, Fate, Sun lines) and pattern recognition.
            </p>
            <button className="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm rounded-xl transition-all shadow-lg shadow-purple-600/30">
              Launch Palm Engine (Week 3)
            </button>
          </div>

          {/* Start Tarot Reading Card */}
          <div className="bg-gradient-to-br from-indigo-950/60 to-cosmic-900 border border-indigo-500/30 p-6 rounded-3xl hover:border-indigo-500/60 transition-all group">
            <div className="w-12 h-12 rounded-2xl bg-indigo-900/50 border border-indigo-500/40 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
              <CreditCard className="w-6 h-6 text-indigo-300" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Tarot Reading Workflow</h3>
            <p className="text-sm text-gray-400 mb-6">
              Select spread (Single, Three Card, Celtic Cross, Career, Relationship) and shuffle 78 cards.
            </p>
            <button className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl transition-all shadow-lg shadow-indigo-600/30">
              Launch Tarot Deck (Week 3)
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
