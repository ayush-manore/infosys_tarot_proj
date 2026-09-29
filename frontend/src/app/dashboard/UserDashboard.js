'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Sparkles, Hand, CreditCard, User, Heart, Brain, Star, Clock,
  BookOpen, Compass, TrendingUp, Award, Calendar, Activity,
  Eye, Flame, Moon, Sun, Zap, Target, Gift, MessageCircle,
  FileText, Bell, BarChart3
} from 'lucide-react';

// Sample demo data for the seeker dashboard
const readingHistory = [
  { id: 1, type: 'tarot', spread: '3-Card Spread', date: '2026-08-30', cards: ['The Fool', 'The Magician', 'The High Priestess'], rating: 5, status: 'completed' },
  { id: 2, type: 'palm', spread: 'Full Palm Scan', date: '2026-08-28', lines: ['Heart Line', 'Head Line', 'Life Line'], rating: 4, status: 'completed' },
  { id: 3, type: 'tarot', spread: 'Celtic Cross', date: '2026-08-25', cards: ['The Emperor', 'Ace of Cups', 'Ten of Pentacles'], rating: 5, status: 'completed' },
  { id: 4, type: 'tarot', spread: 'Single Card', date: '2026-08-22', cards: ['The Star'], rating: 4, status: 'completed' },
  { id: 5, type: 'palm', spread: 'Quick Read', date: '2026-08-20', lines: ['Fate Line', 'Sun Line'], rating: 3, status: 'completed' },
];

const personalityTraits = [
  { trait: 'Intuition', score: 92, color: 'from-purple-500 to-indigo-500', icon: Eye },
  { trait: 'Emotional Depth', score: 85, color: 'from-pink-500 to-rose-500', icon: Heart },
  { trait: 'Analytical Mind', score: 78, color: 'from-cyan-500 to-blue-500', icon: Brain },
  { trait: 'Creative Energy', score: 88, color: 'from-amber-500 to-orange-500', icon: Flame },
  { trait: 'Spiritual Growth', score: 71, color: 'from-emerald-500 to-teal-500', icon: Star },
];

const guidanceMessages = [
  { icon: Moon, title: 'Evening Reflection', message: 'Your Heart Line suggests deep emotional connections are forming. Trust the process and stay open to vulnerability.', time: '2 hours ago', accent: 'purple' },
  { icon: Sun, title: 'Morning Insight', message: 'The Magician appeared in your last reading — a powerful sign that you have all the tools needed to manifest your goals today.', time: '8 hours ago', accent: 'amber' },
  { icon: Zap, title: 'Weekly Focus', message: 'Your Life Line\'s strong arc indicates high vitality this week. Channel this energy into creative pursuits and physical activity.', time: '2 days ago', accent: 'emerald' },
];

const defaultDailyCard = {
  name: 'The Star',
  number: 17,
  keywords: ['hope', 'faith', 'renewal', 'serenity', 'inspiration'],
  meaning: 'The Star brings renewed hope and faith after a period of challenge. Trust that the universe is guiding you toward your highest purpose. This is a time of healing, inspiration, and spiritual connection.',
  element: 'Air',
  zodiac: 'Aquarius',
};

export default function UserDashboard({ user }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [historyList, setHistoryList] = useState(readingHistory);
  const [activeDailyCard, setActiveDailyCard] = useState(defaultDailyCard);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    // Fetch user's real reading history from FastAPI backend
    fetch('http://localhost:8000/api/v1/readings/history', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.data?.readings && data.data.readings.length > 0) {
          const formatted = data.data.readings.map((r, i) => ({
            id: r.id || i + 1,
            type: r.reading_type || 'tarot',
            spread: r.spread_type ? r.spread_type.replace(/_/g, ' ') : 'Card Spread',
            date: r.created_at ? new Date(r.created_at).toISOString().split('T')[0] : 'Today',
            cards: r.result_summary?.cards || ['Live Reading Session'],
            rating: r.feedback_rating || 5,
            status: r.status || 'completed'
          }));
          setHistoryList(formatted);
        }
      })
      .catch(() => {});

    // Fetch daily guidance card
    fetch('http://localhost:8000/api/v1/readings/tarot/daily', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.data?.cards && data.data.cards.length > 0) {
          const c = data.data.cards[0];
          setActiveDailyCard({
            name: c.card_name,
            number: c.number || 1,
            keywords: c.keywords || ['insight', 'guidance'],
            meaning: c.position_interpretation || c.core_meaning,
            element: c.element || 'Universal',
            zodiac: c.zodiac_sign || 'Cosmic'
          });
        }
      })
      .catch(() => {});
  }, []);
  const displayName = user?.email?.split('@')[0] || 'Seeker';

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-glass-card p-8 rounded-3xl border border-white/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-[80px] pointer-events-none" />
        <div className="relative z-10">
          <span className="text-xs font-semibold text-purple-400 uppercase tracking-widest">Seeker Dashboard</span>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-2">
            Welcome back, <span className="text-amber-300">{displayName}</span> ✨
          </h1>
          <p className="text-gray-400 text-sm mt-2 max-w-2xl">
            Role: <span className="capitalize text-purple-300 font-semibold">{user?.role?.name || 'User'}</span> · Your spiritual journey continues. Explore your readings, insights, and personalized guidance below.
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'overview', label: 'Overview', icon: Compass },
          { id: 'history', label: 'Reading History', icon: Clock },
          { id: 'personality', label: 'Personality Insights', icon: Brain },
          { id: 'guidance', label: 'Guidance', icon: MessageCircle },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* ═══════ OVERVIEW TAB ═══════ */}
      {activeTab === 'overview' && (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Total Readings
                <Activity className="w-4 h-4 text-purple-400" />
              </div>
              <div className="text-2xl font-extrabold text-white mt-2">12</div>
              <div className="text-xs text-purple-300 mt-1">8 Tarot · 4 Palm</div>
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

          {/* Daily Card + Quick Actions */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Daily Tarot Card */}
            <div className="bg-gradient-to-br from-amber-950/40 to-cosmic-900 border border-amber-500/20 p-6 rounded-3xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-48 h-48 bg-amber-500/5 rounded-full blur-[60px] pointer-events-none" />
              <div className="relative z-10">
                <div className="flex items-center gap-2 mb-4">
                  <Star className="w-5 h-5 text-amber-400" />
                  <span className="text-xs font-bold text-amber-400 uppercase tracking-widest">Daily Card</span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-1">{activeDailyCard.name}</h3>
                <div className="flex items-center gap-3 text-xs text-gray-400 mb-4">
                  <span>#{activeDailyCard.number}</span>
                  <span>·</span>
                  <span>{activeDailyCard.element}</span>
                  <span>·</span>
                  <span>{activeDailyCard.zodiac}</span>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed mb-4">{activeDailyCard.meaning}</p>
                <div className="flex flex-wrap gap-2">
                  {activeDailyCard.keywords.map(kw => (
                    <span key={kw} className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-300 text-xs font-medium border border-amber-500/20">{kw}</span>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Action Cards */}
            <div className="space-y-4">
              <Link href="/palm-reading" className="block bg-gradient-to-br from-purple-950/60 to-cosmic-900 border border-purple-500/30 p-5 rounded-2xl hover:border-purple-500/60 transition-all group">
                <div className="flex items-center gap-4">
                  <div className="w-11 h-11 rounded-xl bg-purple-900/50 border border-purple-500/40 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <Hand className="w-5 h-5 text-purple-300" />
                  </div>
                  <div>
                    <h4 className="text-white font-bold text-sm">Start Palm Reading</h4>
                    <p className="text-gray-400 text-xs mt-0.5">Upload palm image for AI feature extraction</p>
                  </div>
                </div>
              </Link>
              <Link href="/tarot-reading" className="block bg-gradient-to-br from-indigo-950/60 to-cosmic-900 border border-indigo-500/30 p-5 rounded-2xl hover:border-indigo-500/60 transition-all group">
                <div className="flex items-center gap-4">
                  <div className="w-11 h-11 rounded-xl bg-indigo-900/50 border border-indigo-500/40 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <CreditCard className="w-5 h-5 text-indigo-300" />
                  </div>
                  <div>
                    <h4 className="text-white font-bold text-sm">Draw Tarot Cards</h4>
                    <p className="text-gray-400 text-xs mt-0.5">Select spread and reveal your guidance</p>
                  </div>
                </div>
              </Link>
              <Link href="/datasets" className="block bg-gradient-to-br from-emerald-950/60 to-cosmic-900 border border-emerald-500/30 p-5 rounded-2xl hover:border-emerald-500/60 transition-all group">
                <div className="flex items-center gap-4">
                  <div className="w-11 h-11 rounded-xl bg-emerald-900/50 border border-emerald-500/40 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <BookOpen className="w-5 h-5 text-emerald-300" />
                  </div>
                  <div>
                    <h4 className="text-white font-bold text-sm">Explore Knowledge Base</h4>
                    <p className="text-gray-400 text-xs mt-0.5">Browse 78 tarot cards & 7 palm lines</p>
                  </div>
                </div>
              </Link>
              <div className="grid grid-cols-3 gap-3">
                <Link href="/reports" className="bg-gradient-to-br from-cyan-950/60 to-cosmic-900 border border-cyan-500/30 p-4 rounded-2xl hover:border-cyan-500/60 transition-all group text-center">
                  <FileText className="w-5 h-5 text-cyan-300 mx-auto mb-1" />
                  <span className="text-xs text-white font-semibold">Reports</span>
                </Link>
                <Link href="/notifications" className="bg-gradient-to-br from-amber-950/60 to-cosmic-900 border border-amber-500/30 p-4 rounded-2xl hover:border-amber-500/60 transition-all group text-center">
                  <Bell className="w-5 h-5 text-amber-300 mx-auto mb-1" />
                  <span className="text-xs text-white font-semibold">Notifications</span>
                </Link>
                <Link href="/profile" className="bg-gradient-to-br from-rose-950/60 to-cosmic-900 border border-rose-500/30 p-4 rounded-2xl hover:border-rose-500/60 transition-all group text-center">
                  <BarChart3 className="w-5 h-5 text-rose-300 mx-auto mb-1" />
                  <span className="text-xs text-white font-semibold">Analytics</span>
                </Link>
              </div>
            </div>
          </div>
        </>
      )}

      {/* ═══════ READING HISTORY TAB ═══════ */}
      {activeTab === 'history' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">Reading History</h2>
            <span className="text-xs text-gray-400 bg-white/5 px-3 py-1.5 rounded-lg">{historyList.length} readings total</span>
          </div>
          {historyList.map(reading => (
            <div key={reading.id} className="bg-glass p-5 rounded-2xl border border-white/10 hover:border-white/20 transition-all">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${reading.type === 'tarot' ? 'bg-indigo-900/50 border border-indigo-500/40' : 'bg-purple-900/50 border border-purple-500/40'}`}>
                    {reading.type === 'tarot' ? <CreditCard className="w-5 h-5 text-indigo-300" /> : <Hand className="w-5 h-5 text-purple-300" />}
                  </div>
                  <div>
                    <h4 className="text-white font-semibold text-sm">{reading.spread}</h4>
                    <p className="text-gray-400 text-xs mt-0.5">{reading.date}</p>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className={`w-3.5 h-3.5 ${i < reading.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-600'}`} />
                  ))}
                </div>
              </div>
              <div className="flex flex-wrap gap-2 mt-3">
                {(reading.cards || reading.lines || []).map(item => (
                  <span key={item} className="px-2 py-1 rounded-lg bg-white/5 text-gray-300 text-xs border border-white/10">{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ═══════ PERSONALITY INSIGHTS TAB ═══════ */}
      {activeTab === 'personality' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Personality Insights</h2>
          <p className="text-sm text-gray-400">Aggregated from your tarot spreads, palm morphology, and reading patterns.</p>
          <div className="grid md:grid-cols-2 gap-4">
            {personalityTraits.map(t => (
              <div key={t.trait} className="bg-glass p-5 rounded-2xl border border-white/10">
                <div className="flex items-center gap-3 mb-3">
                  <div className={`w-9 h-9 rounded-lg bg-gradient-to-br ${t.color} flex items-center justify-center`}>
                    <t.icon className="w-4 h-4 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="text-white font-semibold text-sm">{t.trait}</span>
                      <span className="text-white font-bold text-sm">{t.score}%</span>
                    </div>
                  </div>
                </div>
                <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full bg-gradient-to-r ${t.color} transition-all duration-1000`} style={{ width: `${t.score}%` }} />
                </div>
              </div>
            ))}
          </div>

          {/* Tarot & Palm Report Summaries */}
          <div className="grid md:grid-cols-2 gap-6 mt-4">
            <div className="bg-gradient-to-br from-indigo-950/50 to-cosmic-900 border border-indigo-500/20 p-6 rounded-2xl">
              <div className="flex items-center gap-2 mb-3">
                <CreditCard className="w-5 h-5 text-indigo-400" />
                <h3 className="text-white font-bold">Tarot Report Summary</h3>
              </div>
              <ul className="space-y-2 text-sm text-gray-300">
                <li className="flex justify-between"><span>Most drawn suit</span><span className="text-indigo-300 font-semibold">Cups (Emotions)</span></li>
                <li className="flex justify-between"><span>Dominant arcana</span><span className="text-indigo-300 font-semibold">Major Arcana (67%)</span></li>
                <li className="flex justify-between"><span>Recurring card</span><span className="text-indigo-300 font-semibold">The Star</span></li>
                <li className="flex justify-between"><span>Reversed ratio</span><span className="text-indigo-300 font-semibold">28%</span></li>
                <li className="flex justify-between"><span>Preferred spread</span><span className="text-indigo-300 font-semibold">3-Card Spread</span></li>
              </ul>
            </div>
            <div className="bg-gradient-to-br from-purple-950/50 to-cosmic-900 border border-purple-500/20 p-6 rounded-2xl">
              <div className="flex items-center gap-2 mb-3">
                <Hand className="w-5 h-5 text-purple-400" />
                <h3 className="text-white font-bold">Palm Report Summary</h3>
              </div>
              <ul className="space-y-2 text-sm text-gray-300">
                <li className="flex justify-between"><span>Heart Line</span><span className="text-purple-300 font-semibold">Long & curved</span></li>
                <li className="flex justify-between"><span>Head Line</span><span className="text-purple-300 font-semibold">Curved (creative)</span></li>
                <li className="flex justify-between"><span>Life Line</span><span className="text-purple-300 font-semibold">Strong & deep</span></li>
                <li className="flex justify-between"><span>Fate Line</span><span className="text-purple-300 font-semibold">Clear & vertical</span></li>
                <li className="flex justify-between"><span>Dominant element</span><span className="text-purple-300 font-semibold">Water</span></li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* ═══════ GUIDANCE TAB ═══════ */}
      {activeTab === 'guidance' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Personalized Guidance</h2>
          <p className="text-sm text-gray-400">AI-synthesized recommendations based on your readings, palm analysis, and spiritual profile.</p>
          <div className="space-y-4">
            {guidanceMessages.map((msg, i) => (
              <div key={i} className={`bg-glass p-6 rounded-2xl border border-white/10 hover:border-${msg.accent}-500/30 transition-all`}>
                <div className="flex items-start gap-4">
                  <div className={`w-11 h-11 rounded-xl bg-${msg.accent}-900/50 border border-${msg.accent}-500/30 flex items-center justify-center flex-shrink-0`}>
                    <msg.icon className={`w-5 h-5 text-${msg.accent}-400`} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-white font-semibold text-sm">{msg.title}</h4>
                      <span className="text-xs text-gray-500">{msg.time}</span>
                    </div>
                    <p className="text-gray-300 text-sm leading-relaxed">{msg.message}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Goals Section */}
          <div className="bg-glass p-6 rounded-2xl border border-white/10 mt-4">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-emerald-400" />
              <h3 className="text-white font-bold">Active Spiritual Goals</h3>
            </div>
            <div className="space-y-3">
              {[
                { goal: 'Self-Discovery & Inner Awareness', progress: 72 },
                { goal: 'Emotional Balance & Healing', progress: 58 },
                { goal: 'Career Direction Clarity', progress: 45 },
              ].map(g => (
                <div key={g.goal}>
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-300">{g.goal}</span>
                    <span className="text-emerald-400 font-semibold">{g.progress}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400" style={{ width: `${g.progress}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
