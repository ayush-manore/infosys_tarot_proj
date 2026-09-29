'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Bell, Check, CheckCheck, Trash2, Sparkles, ArrowLeft, Sun, BookOpen, TrendingUp, Megaphone, Loader2 } from 'lucide-react';

const API = 'http://localhost:8000/api/v1';

const TYPE_CONFIG = {
  daily_guidance: { icon: Sun, color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/20', label: 'Daily Guidance' },
  reading_reminder: { icon: BookOpen, color: 'text-indigo-400', bg: 'bg-indigo-500/10 border-indigo-500/20', label: 'Reading Reminder' },
  growth_alert: { icon: TrendingUp, color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/20', label: 'Growth Alert' },
  announcement: { icon: Megaphone, color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/20', label: 'Announcement' },
  insight_update: { icon: Sparkles, color: 'text-purple-400', bg: 'bg-purple-500/10 border-purple-500/20', label: 'Insight Update' },
};

export default function NotificationsPage() {
  const [token, setToken] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'unread'
  const [generating, setGenerating] = useState(null);

  useEffect(() => {
    const t = localStorage.getItem('access_token');
    setToken(t);
  }, []);

  useEffect(() => {
    if (token !== null) fetchNotifications();
  }, [token, filter]);

  const headers = token ? { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } : {};

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const unreadParam = filter === 'unread' ? '?unread_only=true' : '';
      const res = await fetch(`${API}/notifications${unreadParam}`, { headers });
      const data = await res.json();
      if (data.status === 'success') {
        setNotifications(data.data || []);
        setUnreadCount(data.unread_count || 0);
      }
    } catch (e) {
      // Demo fallback
      setNotifications(getDemoNotifications());
      setUnreadCount(3);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (id) => {
    try {
      await fetch(`${API}/notifications/${id}/read`, { method: 'PUT', headers });
      setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (e) {
      setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
    }
  };

  const markAllRead = async () => {
    try {
      await fetch(`${API}/notifications/mark-all-read`, { method: 'PUT', headers });
    } catch (e) {}
    setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
    setUnreadCount(0);
  };

  const dismissNotification = async (id) => {
    try {
      await fetch(`${API}/notifications/${id}`, { method: 'DELETE', headers });
    } catch (e) {}
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const generateNotification = async (type) => {
    setGenerating(type);
    try {
      const res = await fetch(`${API}/notifications/${type}`, { method: 'POST', headers });
      const data = await res.json();
      if (data.status === 'success' && data.data) {
        setNotifications(prev => [data.data, ...prev]);
        setUnreadCount(prev => prev + 1);
      }
    } catch (e) {
      const demo = {
        id: Date.now().toString(),
        type: type.replace('-', '_'),
        title: type === 'daily-guidance' ? 'Daily Spiritual Guidance' : type === 'reading-reminder' ? 'Reading Reminder' : 'Growth Alert',
        message: type === 'daily-guidance' ? '🌟 Trust your intuition today — it\'s sharper than usual.' : type === 'reading-reminder' ? 'It\'s been a while since your last reading. The cards may have new wisdom.' : '📈 Your reading consistency is improving!',
        priority: 'normal',
        is_read: false,
        created_at: new Date().toISOString(),
      };
      setNotifications(prev => [demo, ...prev]);
      setUnreadCount(prev => prev + 1);
    } finally {
      setGenerating(null);
    }
  };

  return (
    <div className="min-h-screen bg-cosmic-radial flex flex-col">
      {/* Header */}
      <header className="bg-cosmic-950/80 border-b border-white/10 px-6 md:px-8 py-3.5 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <Bell className="w-5 h-5 text-amber-300" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
            Notifications
          </span>
          {unreadCount > 0 && (
            <span className="px-2.5 py-0.5 bg-red-500 text-white text-xs font-bold rounded-full">{unreadCount}</span>
          )}
        </div>
        <Link href="/dashboard" className="text-xs text-gray-300 hover:text-white px-3 py-1.5 bg-white/5 border border-white/10 rounded-xl transition-colors">Dashboard</Link>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto p-6 md:p-8">
        {/* Generate Buttons */}
        <div className="mb-8">
          <h2 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-3">Generate Notifications</h2>
          <div className="flex flex-wrap gap-2">
            {[
              { id: 'daily-guidance', label: '🌟 Daily Guidance', color: 'bg-amber-600 hover:bg-amber-500' },
              { id: 'reading-reminder', label: '📖 Reading Reminder', color: 'bg-indigo-600 hover:bg-indigo-500' },
              { id: 'growth-alert', label: '📈 Growth Alert', color: 'bg-emerald-600 hover:bg-emerald-500' },
            ].map((btn) => (
              <button
                key={btn.id}
                onClick={() => generateNotification(btn.id)}
                disabled={generating === btn.id}
                className={`px-4 py-2 text-xs font-semibold text-white rounded-xl transition-all ${btn.color} ${generating === btn.id ? 'opacity-60' : ''}`}
              >
                {generating === btn.id ? <Loader2 className="w-3.5 h-3.5 animate-spin inline mr-1" /> : null}
                {btn.label}
              </button>
            ))}
          </div>
        </div>

        {/* Filter & Actions */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex gap-1 bg-white/5 border border-white/10 rounded-xl p-1">
            {['all', 'unread'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all capitalize ${
                  filter === f ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                {f} {f === 'unread' && unreadCount > 0 ? `(${unreadCount})` : ''}
              </button>
            ))}
          </div>
          {unreadCount > 0 && (
            <button onClick={markAllRead} className="flex items-center gap-1.5 text-xs text-purple-300 hover:text-purple-200 transition-colors">
              <CheckCheck className="w-3.5 h-3.5" /> Mark all read
            </button>
          )}
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-6 h-6 animate-spin text-purple-400" />
          </div>
        )}

        {/* Notification List */}
        {!loading && (
          <div className="space-y-2">
            {notifications.length === 0 ? (
              <div className="text-center py-16">
                <Bell className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400">No notifications yet. Generate one above!</p>
              </div>
            ) : (
              notifications.map((n) => {
                const config = TYPE_CONFIG[n.type] || TYPE_CONFIG.insight_update;
                const Icon = config.icon;
                return (
                  <div
                    key={n.id}
                    className={`flex items-start gap-4 p-4 rounded-xl border transition-all ${
                      n.is_read
                        ? 'bg-white/[0.02] border-white/5'
                        : 'bg-white/[0.05] border-purple-500/20 shadow-sm shadow-purple-500/5'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl ${config.bg} border flex items-center justify-center shrink-0`}>
                      <Icon className={`w-5 h-5 ${config.color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-bold text-white">{n.title}</span>
                        {!n.is_read && <span className="w-2 h-2 rounded-full bg-purple-400" />}
                        <span className="text-[10px] text-gray-500 ml-auto">{n.created_at ? new Date(n.created_at).toLocaleString() : ''}</span>
                      </div>
                      <p className="text-xs text-gray-300 leading-relaxed">{n.message}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full ${config.bg} border ${config.color}`}>{config.label}</span>
                        {n.priority === 'high' && <span className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/10 border border-red-500/20 text-red-300">High Priority</span>}
                      </div>
                    </div>
                    <div className="flex flex-col gap-1 shrink-0">
                      {!n.is_read && (
                        <button onClick={() => markAsRead(n.id)} className="p-1.5 hover:bg-white/10 rounded-lg transition-colors" title="Mark as read">
                          <Check className="w-3.5 h-3.5 text-gray-400 hover:text-emerald-400" />
                        </button>
                      )}
                      <button onClick={() => dismissNotification(n.id)} className="p-1.5 hover:bg-white/10 rounded-lg transition-colors" title="Dismiss">
                        <Trash2 className="w-3.5 h-3.5 text-gray-400 hover:text-red-400" />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}
      </main>
    </div>
  );
}

function getDemoNotifications() {
  return [
    { id: '1', type: 'daily_guidance', title: 'Daily Spiritual Guidance', message: '🌟 Your daily energy aligns with introspection. Take a moment to reflect on your path today.', priority: 'normal', is_read: false, created_at: new Date().toISOString() },
    { id: '2', type: 'growth_alert', title: 'Spiritual Growth Update', message: '📈 Your personality profile shows growth in emotional intelligence. Keep nurturing this strength.', priority: 'normal', is_read: false, created_at: new Date(Date.now() - 3600000).toISOString() },
    { id: '3', type: 'reading_reminder', title: 'Reading Reminder', message: 'It\'s been a while since your last reading. The cards may have new wisdom to share.', priority: 'low', is_read: false, created_at: new Date(Date.now() - 86400000).toISOString() },
    { id: '4', type: 'announcement', title: 'Platform Update', message: '🎉 New Celtic Cross spread interpretations and career guidance module now available!', priority: 'high', is_read: true, created_at: new Date(Date.now() - 172800000).toISOString() },
    { id: '5', type: 'daily_guidance', title: 'Daily Spiritual Guidance', message: '🌙 A period of emotional clarity opens. This is an excellent time for a palm analysis session.', priority: 'normal', is_read: true, created_at: new Date(Date.now() - 259200000).toISOString() },
  ];
}
