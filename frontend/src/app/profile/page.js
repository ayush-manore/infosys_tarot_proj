'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, User, Sparkles, Save, Check } from 'lucide-react';

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    first_name: '',
    last_name: '',
    display_name: '',
    age_group: '26-35',
    spiritual_interests: ['palmistry', 'tarot'],
    spiritual_goals: ['self_discovery'],
    preferred_spread: 'three_card',
    bio: ''
  });
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/auth/login';
      return;
    }

    fetch('http://localhost:8000/api/v1/profiles/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success' && data.data) {
          setProfile(prev => ({ ...prev, ...data.data }));
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    try {
      const res = await fetch('http://localhost:8000/api/v1/profiles/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profile)
      });
      if (res.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-cosmic-radial p-6 md:p-12">
      <div className="max-w-3xl mx-auto space-y-6">
        <Link href="/dashboard" className="inline-flex items-center gap-2 text-sm text-purple-400 hover:underline">
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </Link>

        <div className="bg-glass p-8 rounded-3xl border border-white/10 shadow-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-white/10 pb-6">
            <div>
              <h1 className="text-2xl font-bold text-white">Profile & Spiritual Preferences</h1>
              <p className="text-xs text-gray-400 mt-1">Manage your interests, goals, and reading preferences</p>
            </div>
            <div className="w-10 h-10 rounded-xl bg-purple-900/50 flex items-center justify-center">
              <User className="w-5 h-5 text-purple-400" />
            </div>
          </div>

          {saved && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
              <Check className="w-4 h-4" /> Profile settings saved successfully!
            </div>
          )}

          <form onSubmit={handleSave} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">First Name</label>
                <input
                  type="text"
                  value={profile.first_name || ''}
                  onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Last Name</label>
                <input
                  type="text"
                  value={profile.last_name || ''}
                  onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Age Group</label>
              <select
                value={profile.age_group || '26-35'}
                onChange={(e) => setProfile({ ...profile, age_group: e.target.value })}
                className="w-full px-4 py-2.5 bg-cosmic-900 border border-white/10 rounded-xl text-white text-sm"
              >
                <option value="18-25">18-25</option>
                <option value="26-35">26-35</option>
                <option value="36-45">36-45</option>
                <option value="46-55">46-55</option>
                <option value="55+">55+</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Preferred Tarot Spread</label>
              <select
                value={profile.preferred_spread || 'three_card'}
                onChange={(e) => setProfile({ ...profile, preferred_spread: e.target.value })}
                className="w-full px-4 py-2.5 bg-cosmic-900 border border-white/10 rounded-xl text-white text-sm"
              >
                <option value="single">Single Card Reading</option>
                <option value="three_card">Three Card Reading (Past/Present/Future)</option>
                <option value="relationship">Relationship Spread</option>
                <option value="career">Career Spread</option>
                <option value="celtic_cross">Celtic Cross Spread</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Spiritual Bio & Intentions</label>
              <textarea
                rows={3}
                value={profile.bio || ''}
                onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm placeholder-gray-500"
                placeholder="Share your spiritual journey, goals, or what brings you to MysticAI..."
              />
            </div>

            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg shadow-purple-600/30 text-sm flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              Save Preferences
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
