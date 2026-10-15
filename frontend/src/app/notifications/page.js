'use client';
import { API_BASE as API, authHeader } from '@/utils/api';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Bell, Mail, Moon, Sun, Clock, Calendar, Sparkles, CheckCircle, AlertCircle, ChevronRight, RefreshCw, Send, Shield, Brain, Hand, CreditCard } from 'lucide-react';



function authHeader() {
  if (typeof window === 'undefined') return {};
  const t = localStorage.getItem('access_token');
  return t ? { Authorization: `Bearer ${t}` } : {};
}

function Toast({ msg, type, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 4000);
    return () => clearTimeout(t);
  }, []);
  const c = type === 'success'
    ? 'bg-emerald-900/80 border-emerald-500/40 text-emerald-200'
    : 'bg-rose-900/80 border-rose-500/40 text-rose-200';
  const Icon = type === 'success' ? CheckCircle : AlertCircle;
  return (
    <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl border backdrop-blur-md shadow-2xl animate-fadeIn ${c}`}>
      <Icon className="w-5 h-5 flex-shrink-0" />
      <p className="text-sm font-semibold">{msg}</p>
    </div>
  );
}

export default function NotificationsPage() {
  const [toast, setToast] = useState(null);
  const [loading, setLoading] = useState({});
  const [darkMode, setDarkMode] = useState(true);
  const [prefs, setPrefs] = useState({
    reminders: true,
    dailyGuidance: true,
    monthlyReport: true,
    readingType: 'tarot'
  });

  useEffect(() => {
    const saved = localStorage.getItem('theme');
    const isDark = saved ? saved === 'dark' : true;
    setDarkMode(isDark);
    document.documentElement.classList.toggle('light-mode', !isDark);
    const savedPrefs = localStorage.getItem('notif_prefs');
    if (savedPrefs) {
      try { setPrefs(JSON.parse(savedPrefs)); } catch (e) {}
    }
  }, []);

  const toggleTheme = () => {
    const next = !darkMode;
    setDarkMode(next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
    document.documentElement.classList.toggle('light-mode', !next);
  };

  const savePrefs = (next) => {
    setPrefs(next);
    localStorage.setItem('notif_prefs', JSON.stringify(next));
  };

  const showToast = (msg, type = 'success') => setToast({ msg, type });

  async function callAPI(key, path, body = {}) {
    setLoading(l => ({ ...l, [key]: true }));
    try {
      const res = await fetch(`${API}${path}`, {
        method: 'POST',
        headers: { ...authHeader(), 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const d = await res.json();
      if (d.status === 'success') showToast(d.message || 'Email queued! Check your inbox.');
      else showToast(d.detail || 'Something went wrong', 'error');
    } catch (e) {
      showToast('Backend not reachable. Ensure FastAPI is running on port 8000.', 'error');
    } finally {
      setLoading(l => ({ ...l, [key]: false }));
    }
  }

  const EMAIL_ACTIONS = [
    {
      key: 'reminder',
      icon: Bell,
      grad: 'from-purple-600 to-indigo-600',
      border: 'border-purple-500/20 bg-purple-950/30',
      title: 'Reading Reminder',
      desc: 'Send yourself a reminder email to do your daily tarot or palm reading.',
      action: () => callAPI('reminder', '/notifications/email/reminder', { reading_type: prefs.readingType }),
      btnLabel: 'Send Reminder Email'
    },
    {
      key: 'guidance',
      icon: Sparkles,
      grad: 'from-amber-500 to-orange-500',
      border: 'border-amber-500/20 bg-amber-950/30',
      title: 'Daily Spiritual Guidance',
      desc: "Receive today's AI-generated affirmation, crystal recommendation, and spiritual practice.",
      action: () => callAPI('guidance', '/notifications/email/daily-guidance', {}),
      btnLabel: 'Send Daily Guidance'
    },
    {
      key: 'report',
      icon: Calendar,
      grad: 'from-emerald-500 to-teal-500',
      border: 'border-emerald-500/20 bg-emerald-950/30',
      title: 'Monthly Spiritual Report',
      desc: 'Get your complete monthly spiritual journey summary with stats, insights, and growth analysis.',
      action: () => callAPI('report', '/notifications/email/monthly-report', { total_readings: 5, streak_days: 12, growth_score: 82 }),
      btnLabel: 'Send Monthly Report'
    },
    {
      key: 'test',
      icon: Mail,
      grad: 'from-blue-500 to-indigo-500',
      border: 'border-blue-500/20 bg-blue-950/30',
      title: 'Test Email Connection',
      desc: 'Send a test welcome email to verify your Gmail SMTP config in backend/.env is working.',
      action: () => callAPI('test', '/notifications/email/test', {}),
      btnLabel: 'Send Test Email'
    },
  ];

  const PREF_ITEMS = [
    { key: 'reminders', label: 'Reading Reminders', desc: 'Get reminded to do your daily reading' },
    { key: 'dailyGuidance', label: 'Daily Spiritual Guidance', desc: 'Morning affirmations, crystals & practices' },
    { key: 'monthlyReport', label: 'Monthly Journey Reports', desc: 'Full spiritual progress report each month' },
  ];

  const QUICK_LINKS = [
    { href: '/palm-reading', label: 'Palm Reading', icon: Hand },
    { href: '/tarot-reading', label: 'Tarot Reading', icon: CreditCard },
    { href: '/ai-insights', label: 'AI Insights', icon: Brain },
    { href: '/reports', label: 'Reports', icon: Calendar },
  ];

  const SETUP_STEPS = [
    'Go to your Google Account → Security → 2-Step Verification (enable if not already)',
    'Then go to Security → App Passwords → Select "Mail" → Generate a new app password',
    'Copy the 16-character App Password (no spaces needed)',
    'Open backend/.env and set: GMAIL_USER=your_email@gmail.com',
    'Also set: GMAIL_APP_PASSWORD=your16charpassword',
    'Restart the backend server — all email features will now be live!',
  ];

  return (
    <div className="min-h-screen bg-cosmic-radial">
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-purple-900/10 rounded-full blur-[100px] pointer-events-none" />

      {/* Header */}
      <header className="sticky top-0 z-40 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-1.5 text-gray-400 hover:text-white text-sm transition-colors">
            <ChevronRight className="w-4 h-4 rotate-180" /> Dashboard
          </Link>
          <span className="text-gray-600">/</span>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center">
              <Bell className="w-4 h-4 text-amber-300" />
            </div>
            <span className="text-white font-bold text-sm">Notifications &amp; Emails</span>
          </div>
        </div>
        <button
          onClick={toggleTheme}
          title={darkMode ? 'Light Mode' : 'Dark Mode'}
          className="w-8 h-8 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors"
        >
          {darkMode ? <Sun className="w-4 h-4 text-amber-300" /> : <Moon className="w-4 h-4 text-indigo-400" />}
        </button>
      </header>

      <div className="max-w-4xl mx-auto px-4 md:px-6 py-8 space-y-8">

        {/* Hero Banner */}
        <div className="relative bg-gradient-to-br from-purple-950/60 via-indigo-950/40 to-cosmic-900 border border-purple-500/20 rounded-3xl p-6 md:p-8 overflow-hidden">
          <div className="absolute top-0 right-0 w-48 h-48 bg-purple-600/10 rounded-full blur-[60px] pointer-events-none" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/30">
                <Bell className="w-5 h-5 text-amber-300" />
              </div>
              <span className="text-[11px] font-bold text-purple-400 uppercase tracking-widest">Gmail Email Notifications</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white mb-2">Notifications &amp; Reminders</h1>
            <p className="text-gray-400 text-sm max-w-xl leading-relaxed">
              Manage your spiritual reminders, receive daily guidance, and get monthly journey reports — all delivered beautifully to your Gmail inbox.
            </p>
            <div className="mt-4 inline-flex items-center gap-2 text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20 rounded-xl px-3 py-2">
              <Shield className="w-3.5 h-3.5" /> Configure GMAIL_USER + GMAIL_APP_PASSWORD in backend/.env to activate
            </div>
          </div>
        </div>

        {/* Notification Preferences */}
        <div className="bg-glass rounded-2xl border border-white/10 p-6">
          <h2 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5 text-purple-400" /> Notification Preferences
          </h2>
          <div className="space-y-3">
            {PREF_ITEMS.map(p => (
              <div key={p.key} className="flex items-center justify-between py-3 border-b border-white/5 last:border-0">
                <div>
                  <div className="text-white font-semibold text-sm">{p.label}</div>
                  <div className="text-gray-500 text-xs mt-0.5">{p.desc}</div>
                </div>
                <button
                  id={`toggle-${p.key}`}
                  onClick={() => savePrefs({ ...prefs, [p.key]: !prefs[p.key] })}
                  className={`relative w-11 h-6 rounded-full transition-all ${prefs[p.key] ? 'bg-purple-600' : 'bg-white/10'}`}
                >
                  <span
                    className="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-all"
                    style={{ left: prefs[p.key] ? '22px' : '2px' }}
                  />
                </button>
              </div>
            ))}
            <div className="pt-2">
              <label className="text-white font-semibold text-sm block mb-2">Preferred Reading Type for Reminders</label>
              <div className="flex gap-2">
                {['tarot', 'palm', 'combined'].map(t => (
                  <button
                    key={t}
                    id={`reading-type-${t}`}
                    onClick={() => savePrefs({ ...prefs, readingType: t })}
                    className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all capitalize ${prefs.readingType === t ? 'bg-purple-600 border-purple-500 text-white' : 'bg-white/5 border-white/10 text-gray-400 hover:text-white'}`}
                  >
                    {t === 'tarot' ? '🔮' : t === 'palm' ? '🤚' : '✨'} {t}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Email Actions Grid */}
        <div>
          <h2 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
            <Send className="w-5 h-5 text-indigo-400" /> Send Email Now
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {EMAIL_ACTIONS.map(a => {
              const Icon = a.icon;
              return (
                <div key={a.key} className={`rounded-2xl border p-5 ${a.border}`}>
                  <div className="flex items-start gap-4 mb-4">
                    <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${a.grad} flex items-center justify-center flex-shrink-0 shadow-lg`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-white font-bold text-sm">{a.title}</h3>
                      <p className="text-gray-400 text-xs mt-1 leading-relaxed">{a.desc}</p>
                    </div>
                  </div>
                  <button
                    id={`btn-email-${a.key}`}
                    onClick={a.action}
                    disabled={loading[a.key]}
                    className={`w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-bold text-white bg-gradient-to-r ${a.grad} hover:opacity-90 transition-all disabled:opacity-50 shadow-lg`}
                  >
                    {loading[a.key] ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Mail className="w-4 h-4" />}
                    {loading[a.key] ? 'Queuing...' : a.btnLabel}
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Gmail Setup Guide */}
        <div className="bg-gradient-to-br from-amber-950/30 to-cosmic-900 border border-amber-500/20 rounded-2xl p-6">
          <h2 className="text-white font-bold mb-4 flex items-center gap-2">
            <Mail className="w-5 h-5 text-amber-400" /> Gmail Setup Guide
          </h2>
          <div className="space-y-3">
            {SETUP_STEPS.map((s, i) => (
              <div key={i} className="flex items-start gap-3">
                <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold flex items-center justify-center flex-shrink-0 border border-amber-500/30">
                  {i + 1}
                </span>
                <p className="text-gray-300 text-sm">{s}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {QUICK_LINKS.map(a => (
            <Link
              key={a.href}
              href={a.href}
              className="flex items-center gap-2 p-3 border border-white/10 bg-white/5 hover:bg-white/10 rounded-2xl transition-all group"
            >
              <a.icon className="w-4 h-4 text-gray-400 group-hover:text-purple-400 transition-colors" />
              <span className="text-white font-semibold text-sm">{a.label}</span>
            </Link>
          ))}
        </div>
      </div>

      {toast && <Toast msg={toast.msg} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
}
