'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, User, LogOut, Shield, Compass, BookOpen, Layers, Shuffle, Bot } from 'lucide-react';

import UserDashboard from './UserDashboard';
import TarotReaderDashboard from './TarotReaderDashboard';
import ConsultantDashboard from './ConsultantDashboard';
import AdminDashboard from './AdminDashboard';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [selectedRole, setSelectedRole] = useState('user');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      // Demo fallback user if not logged in
      const defaultUser = { email: 'ayush@example.com', role: { name: 'user' } };
      setUser(defaultUser);
      setSelectedRole('user');
      setLoading(false);
      return;
    }

    fetch('http://localhost:8000/api/v1/users/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setUser(data.data);
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

  const personaAccounts = {
    user: { email: 'seeker@mystic.ai', label: 'Seeker', color: 'bg-purple-600', badge: 'bg-purple-500/20 text-purple-300 border-purple-500/30' },
    tarot_reader: { email: 'reader@mystic.ai', label: 'Tarot Reader', color: 'bg-indigo-600', badge: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30' },
    spiritual_consultant: { email: 'consultant@mystic.ai', label: 'Consultant', color: 'bg-emerald-600', badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' },
    admin: { email: 'admin@mystic.ai', label: 'Super Admin', color: 'bg-red-600', badge: 'bg-red-500/20 text-red-300 border-red-500/30' },
  };

  const handleSwitchPersona = async (roleId) => {
    const target = personaAccounts[roleId];
    if (!target) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: target.email, password: 'password123' })
      });
      const data = await res.json();
      if (res.ok) {
        const token = data.data.tokens.access_token;
        localStorage.setItem('access_token', token);
        const meRes = await fetch('http://localhost:8000/api/v1/users/me', {
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

        {/* Real Persona Switcher Bar */}
        <div className="hidden lg:flex items-center bg-white/5 border border-white/10 rounded-2xl p-1 gap-1">
          <span className="text-[11px] font-bold text-gray-400 uppercase px-2.5 flex items-center gap-1">
            <Shield className="w-3 h-3 text-purple-400" /> Switch Active Persona:
          </span>
          {Object.entries(personaAccounts).map(([id, info]) => (
            <button
              key={id}
              onClick={() => handleSwitchPersona(id)}
              className={`px-3 py-1 rounded-xl text-xs font-semibold transition-all ${
                selectedRole === id
                  ? `${info.color} text-white shadow-md`
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              {info.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-5">
          <Link href="/draw-cards" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Shuffle className="w-3.5 h-3.5 text-purple-300" />
            Draw Cards
          </Link>
          <Link href="/chat" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Bot className="w-3.5 h-3.5 text-emerald-300" />
            AI Chat
          </Link>
          <Link href="/datasets" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <BookOpen className="w-3.5 h-3.5 text-amber-300" />
            Knowledge Base
          </Link>
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

      {/* RBAC Active Identity & Powers Banner */}
      <div className="bg-white/[0.02] border-b border-white/5 px-6 md:px-8 py-2.5 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-gray-400">Authenticated Session:</span>
          <span className="font-semibold text-white">{user?.email}</span>
          <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase border ${personaAccounts[selectedRole]?.badge || 'bg-purple-500/20 text-purple-300 border-purple-500/30'}`}>
            {user?.role?.name ? user.role.name.replace('_', ' ') : selectedRole}
          </span>
          <span className="hidden md:inline text-gray-500">|</span>
          <span className="hidden md:flex items-center gap-1 text-gray-400">
            <Shield className="w-3 h-3 text-emerald-400" />
            Active Backend Powers:
          </span>
          <div className="hidden md:flex flex-wrap gap-1">
            {activePermissionList.slice(0, 4).map((p) => (
              <span key={p} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 text-[10px] border border-emerald-500/20 capitalize">
                ✓ {p}
              </span>
            ))}
            {activePermissionList.length > 4 && (
              <span className="px-2 py-0.5 rounded bg-white/5 text-gray-400 text-[10px]">
                +{activePermissionList.length - 4} more
              </span>
            )}
          </div>
        </div>

        {/* Mobile Switcher */}
        <div className="flex lg:hidden items-center gap-1 overflow-x-auto">
          {Object.entries(personaAccounts).map(([id, info]) => (
            <button
              key={id}
              onClick={() => handleSwitchPersona(id)}
              className={`px-2 py-1 rounded text-[11px] font-semibold ${
                selectedRole === id ? `${info.color} text-white` : 'bg-white/5 text-gray-400'
              }`}
            >
              {info.label}
            </button>
          ))}
        </div>
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
