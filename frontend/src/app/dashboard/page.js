'use client';
import { API_BASE, authHeader } from '@/utils/api';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, User, LogOut, Shield, BookOpen, Shuffle, Bot, Brain, Sun, Moon, Bell } from 'lucide-react';

import UserDashboard from './UserDashboard';
import TarotReaderDashboard from './TarotReaderDashboard';
import ConsultantDashboard from './ConsultantDashboard';
import AdminDashboard from './AdminDashboard';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [selectedRole, setSelectedRole] = useState('user');
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem('theme');
    const isDark = saved ? saved === 'dark' : true;
    setDarkMode(isDark);
    document.documentElement.classList.toggle('light-mode', !isDark);
  }, []);

  const toggleTheme = () => {
    const next = !darkMode;
    setDarkMode(next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
    document.documentElement.classList.toggle('light-mode', !next);
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      const defaultUser = { email: 'seeker@mystic.ai', role: { name: 'user' } };
      setUser(defaultUser);
      setSelectedRole('user');
      setLoading(false);
      return;
    }

    fetch(`${API_BASE}/users/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setUser(data.data);
          // Role comes from the JWT / backend — cannot be overridden from UI
          const roleName = data.data.role?.name || 'user';
          setSelectedRole(roleName);
        } else {
          setUser({ email: 'seeker@mystic.ai', role: { name: 'user' } });
          setSelectedRole('user');
        }
      })
      .catch(() => {
        setUser({ email: 'seeker@mystic.ai', role: { name: 'user' } });
        setSelectedRole('user');
      })
      .finally(() => setLoading(false));
  }, []);

  const roleLabels = {
    user: { label: 'Seeker', badge: 'bg-purple-500/20 text-purple-300 border-purple-500/30' },
    tarot_reader: { label: 'Tarot Reader', badge: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30' },
    spiritual_consultant: { label: 'Consultant', badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' },
    admin: { label: 'Super Admin', badge: 'bg-red-500/20 text-red-300 border-red-500/30' },
  };

  const handleSwitchPersona = async (roleId) => {
    // SECURITY: Role switching disabled — role is determined by backend JWT only
    return;
    const target = roleLabels[roleId];
    if (!target) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: target.email, password: 'password123' })
      });
      const data = await res.json();
      if (res.ok) {
        const token = data.data.tokens.access_token;
        localStorage.setItem('access_token', token);
        const meRes = await fetch(`${API_BASE}/users/me`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const meData = await meRes.json();
        if (meData.status === 'success') {
          setUser(meData.data);
          setSelectedRole(meData.data.role?.name || roleId);
        }
      }
    } catch (e) {
      console.error(e);
      setSelectedRole(roleId);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/auth/login';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-cosmic-radial flex items-center justify-center">
        <div className="flex items-center gap-3 text-purple-400 font-medium">
          <Sparkles className="w-6 h-6 animate-spin text-amber-400" />
          Authenticating role session with FastAPI backend...
        </div>
      </div>
    );
  }

  const activePermissions = user?.role?.permissions || {};
  const activePermissionList = Object.entries(activePermissions)
    .filter(([k, v]) => v === true && k.startsWith('can_'))
    .map(([k]) => k.replace('can_', '').replace(/_/g, ' '));

  return (
    <div className="min-h-screen bg-cosmic-radial flex flex-col">
      {/* Top Header */}
      <header className="bg-cosmic-950/80 border-b border-white/10 px-6 md:px-8 py-3.5 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <Sparkles className="w-5 h-5 text-amber-300" />
          </div>
          <Link href="/" className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
            MysticAI Portal
          </Link>
        </div>

        {/* Branding center spacer */}
        <div className="hidden lg:flex items-center gap-2 text-[11px] font-bold text-purple-400 uppercase tracking-widest">
          <Shield className="w-3 h-3" /> Secure Role-Based Access
        </div>

        <div className="flex items-center gap-3">
          <Link href="/ai-insights" className="hidden sm:flex items-center gap-1.5 text-xs text-white bg-gradient-to-r from-purple-600/80 to-indigo-600/80 border border-purple-500/40 px-3 py-1.5 rounded-xl transition-colors hover:from-purple-600 hover:to-indigo-600 font-semibold shadow-md shadow-purple-900/30">
            <Brain className="w-3.5 h-3.5 text-amber-300" />
            AI Insights
          </Link>
          <Link href="/draw-cards" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Shuffle className="w-3.5 h-3.5 text-purple-300" />
            Draw Cards
          </Link>
          <Link href="/chat" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Bot className="w-3.5 h-3.5 text-emerald-300" />
            AI Chat
          </Link>
          <Link href="/notifications" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Bell className="w-3.5 h-3.5 text-amber-300" />
            Notifications
          </Link>
          {/* Theme Toggle */}
          <button onClick={toggleTheme} title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            className="flex items-center justify-center w-8 h-8 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
            {darkMode ? <Sun className="w-4 h-4 text-amber-300" /> : <Moon className="w-4 h-4 text-indigo-400" />}
          </button>
          <Link href="/profile" className="flex items-center gap-1.5 text-xs text-gray-300 hover:text-white transition-colors">
            <User className="w-4 h-4 text-purple-400" />
            Profile
          </Link>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-300 transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign Out
          </button>
        </div>
      </header>

      {/* Identity Banner — read-only, role locked to JWT */}
      <div className="bg-white/[0.02] border-b border-white/5 px-6 md:px-8 py-2 flex flex-wrap items-center gap-3 text-xs">
        <Shield className="w-3 h-3 text-emerald-400" />
        <span className="text-gray-400">Session:</span>
        <span className="font-semibold text-white">{user?.email}</span>
        <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase border ${roleLabels[selectedRole]?.badge || 'bg-purple-500/20 text-purple-300 border-purple-500/30'}`}>
          {roleLabels[selectedRole]?.label || selectedRole}
        </span>
        {activePermissionList.length > 0 && (
          <>
            <span className="text-gray-600">|</span>
            <div className="hidden md:flex flex-wrap gap-1">
              {activePermissionList.slice(0, 4).map((p) => (
                <span key={p} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 text-[10px] border border-emerald-500/20 capitalize">✓ {p}</span>
              ))}
              {activePermissionList.length > 4 && (
                <span className="px-2 py-0.5 rounded bg-white/5 text-gray-400 text-[10px]">+{activePermissionList.length - 4} more</span>
              )}
            </div>
          </>
        )}
      </div>

      {/* Main Role-Specific View */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
        {selectedRole === 'user' && <UserDashboard user={user} />}
        {selectedRole === 'tarot_reader' && <TarotReaderDashboard user={user} />}
        {selectedRole === 'spiritual_consultant' && <ConsultantDashboard user={user} />}
        {selectedRole === 'admin' && <AdminDashboard user={user} />}
      </main>
    </div>
  );
}
