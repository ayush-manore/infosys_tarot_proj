'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
  Sparkles, CreditCard, Users, BarChart3, Clock, Star,
  TrendingUp, Activity, Eye, FileText, Filter, ArrowUpRight,
  Layers, Shuffle, PieChart, CalendarDays, MessageSquare, ThumbsUp
} from 'lucide-react';

const recentSessions = [
  { id: 'S-1042', seeker: 'Priya M.', spread: '3-Card Spread', cards: ['The Fool', 'Queen of Cups', 'Ten of Pentacles'], orientation: ['upright', 'reversed', 'upright'], rating: 5, date: '2026-08-31', duration: '12 min', status: 'completed' },
  { id: 'S-1041', seeker: 'Amit K.', spread: 'Celtic Cross', cards: ['The Tower', 'The Star', 'Ace of Wands'], orientation: ['upright', 'upright', 'reversed'], rating: 4, date: '2026-08-30', duration: '28 min', status: 'completed' },
  { id: 'S-1040', seeker: 'Nisha R.', spread: 'Single Card', cards: ['The High Priestess'], orientation: ['upright'], rating: 5, date: '2026-08-30', duration: '5 min', status: 'completed' },
  { id: 'S-1039', seeker: 'Rahul S.', spread: 'Career Spread', cards: ['The Emperor', 'Eight of Pentacles', 'Ace of Swords'], orientation: ['upright', 'upright', 'upright'], rating: 4, date: '2026-08-29', duration: '18 min', status: 'completed' },
  { id: 'S-1038', seeker: 'Deepa L.', spread: '3-Card Spread', cards: ['The Moon', 'The Sun', 'Judgment'], orientation: ['reversed', 'upright', 'upright'], rating: 5, date: '2026-08-28', duration: '14 min', status: 'completed' },
];

const spreadStats = [
  { name: '3-Card Spread', count: 45, pct: 38 },
  { name: 'Celtic Cross', count: 28, pct: 23 },
  { name: 'Single Card', count: 22, pct: 18 },
  { name: 'Career Spread', count: 15, pct: 13 },
  { name: 'Relationship', count: 10, pct: 8 },
];

const topCards = [
  { name: 'The Star', draws: 18, pctUpright: 72 },
  { name: 'The Fool', draws: 15, pctUpright: 80 },
  { name: 'Queen of Cups', draws: 14, pctUpright: 64 },
  { name: 'The High Priestess', draws: 12, pctUpright: 58 },
  { name: 'Ace of Pentacles', draws: 11, pctUpright: 91 },
];

export default function TarotReaderDashboard({ user }) {
  const [activeTab, setActiveTab] = useState('analytics');
  const [sessionsList, setSessionsList] = useState(recentSessions);
  const [clientName, setClientName] = useState('');
  const [clientQuestion, setClientQuestion] = useState('');
  const [selectedSpread, setSelectedSpread] = useState('three_card');
  const [readerLoading, setReaderLoading] = useState(false);
  const [readerResult, setReaderResult] = useState(null);
  const [readerError, setReaderError] = useState(null);

  const displayName = user?.email?.split('@')[0] || 'Reader';

  const handleCastClientReading = async (e) => {
    e.preventDefault();
    setReaderLoading(true);
    setReaderError(null);
    setReaderResult(null);

    const token = localStorage.getItem('access_token');
    try {
      const promptQuestion = clientName 
        ? `[Client: ${clientName}] ${clientQuestion || 'General spiritual guidance'}` 
        : (clientQuestion || 'General spiritual guidance');

      const res = await fetch('http://localhost:8000/api/v1/readings/tarot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          spread_type: selectedSpread,
          question: promptQuestion
        })
      });

      const data = await res.json();
      if (res.ok && data.data?.reading) {
        const r = data.data.reading;
        setReaderResult(r);
        
        // Add to live session queue
        const newSession = {
          id: `S-${Math.floor(1000 + Math.random() * 9000)}`,
          seeker: clientName || 'Anonymous Seeker',
          spread: r.spread_name,
          cards: r.cards.map(c => c.card_name),
          orientation: r.cards.map(c => c.orientation),
          rating: 5,
          date: new Date().toISOString().split('T')[0],
          duration: 'Live Client Draw',
          status: 'completed'
        };
        setSessionsList(prev => [newSession, ...prev]);
      } else {
        setReaderError(data.detail || 'Failed to generate reading');
      }
    } catch (err) {
      setReaderError('Failed to connect to Tarot reading service');
    } finally {
      setReaderLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-glass-card p-8 rounded-3xl border border-white/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-cyan-600/8 rounded-full blur-[80px] pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest">Tarot Reader Dashboard</span>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-2">
              Welcome, <span className="text-cyan-300">{displayName}</span> 🔮
            </h1>
            <p className="text-gray-400 text-sm mt-2 max-w-2xl">
              Role: <span className="capitalize text-indigo-300 font-semibold">Tarot Reader</span> · Manage your reading sessions, track engagement, and analyze card patterns.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveTab('client_console')}
              className="flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 transition-all transform hover:scale-105"
            >
              <Sparkles className="w-4 h-4 text-amber-300" />
              Client Reading Console
            </button>
            <Link
              href="/datasets"
              className="flex items-center gap-2 px-4 py-3 rounded-xl bg-white/10 hover:bg-white/15 text-white font-medium text-sm transition-all border border-white/10"
            >
              <Layers className="w-4 h-4 text-cyan-300" />
              Card Archives
            </Link>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'client_console', label: 'Client Reading Console (Live)', icon: Sparkles },
          { id: 'analytics', label: 'Reading Analytics', icon: BarChart3 },
          { id: 'sessions', label: 'Session Tracking', icon: Clock },
          { id: 'engagement', label: 'User Engagement', icon: Users },
          { id: 'reports', label: 'Report Management', icon: FileText },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* ═══════ CLIENT READING CONSOLE (LIVE POWER) ═══════ */}
      {activeTab === 'client_console' && (
        <div className="space-y-6">
          <div className="bg-glass-card p-6 rounded-2xl border border-indigo-500/20">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-widest border border-indigo-500/30">
                Tarot Reader Authority Power
              </span>
              <span className="text-xs text-indigo-400 font-semibold">Live Client Reading Session</span>
            </div>
            <h2 className="text-2xl font-bold text-white">Cast Live Reading for a Seeker</h2>
            <p className="text-xs text-gray-400 mt-1">
              As a certified Tarot Reader, you can draw cards on behalf of seekers, tailor the positional spread, and document guidance notes into the live session queue.
            </p>

            <form onSubmit={handleCastClientReading} className="mt-5 grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Client / Seeker Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Rohan Verma"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Spread Architecture
                </label>
                <select
                  value={selectedSpread}
                  onChange={(e) => setSelectedSpread(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-gray-900 border border-white/10 rounded-xl text-white text-xs focus:outline-none focus:border-indigo-500"
                >
                  <option value="single">Single Card (Immediate Insight - 1 Card)</option>
                  <option value="three_card">Three Card Spread (Past, Present, Future - 3 Cards)</option>
                  <option value="celtic_cross">Celtic Cross (Comprehensive Matrix - 10 Cards)</option>
                  <option value="career">Career Trajectory (3 Cards)</option>
                  <option value="relationship">Relationship Harmony (3 Cards)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Guiding Question / Topic
                </label>
                <input
                  type="text"
                  placeholder="e.g. Career change into AI consulting"
                  value={clientQuestion}
                  onChange={(e) => setClientQuestion(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="md:col-span-3 flex items-center justify-between pt-2">
                <span className="text-xs text-gray-400">
                  ⚡ Uses FastAPI <code className="text-indigo-300">POST /api/v1/readings/tarot</code> with Reader authorization.
                </span>
                <button
                  type="submit"
                  disabled={readerLoading}
                  className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-xs font-bold transition-all shadow-lg shadow-indigo-600/30 flex items-center gap-2"
                >
                  {readerLoading ? 'Shuffling & Dealing Cards...' : 'Cast Client Reading Now'}
                  <Sparkles className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>

            {readerError && (
              <div className="mt-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs">
                {readerError}
              </div>
            )}
          </div>

          {/* Live Reading Result Box */}
          {readerResult && (
            <div className="bg-glass-card p-6 rounded-2xl border border-indigo-500/30 space-y-6 animate-fadeIn">
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-2 border-b border-white/10 pb-4">
                <div>
                  <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
                    ✓ Reading Successfully Executed & Added to Session Queue
                  </span>
                  <h3 className="text-xl font-bold text-white mt-1">
                    {readerResult.spread_name} for <span className="text-amber-300">{clientName || 'Seeker'}</span>
                  </h3>
                  <p className="text-xs text-gray-400 mt-0.5">
                    Confidence: <span className="text-indigo-300 font-semibold">{Math.round(readerResult.confidence_score * 100)}%</span> · Drawn Cards: {readerResult.card_count}
                  </p>
                </div>
              </div>

              {/* Cards Grid */}
              <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
                {readerResult.cards.map((card, idx) => (
                  <div key={idx} className="bg-white/5 border border-white/10 p-4 rounded-xl space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] uppercase font-bold text-indigo-400">{card.position}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        card.orientation === 'reversed' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      }`}>
                        {card.orientation}
                      </span>
                    </div>
                    <h4 className="text-white font-bold text-base">{card.card_name}</h4>
                    <p className="text-gray-400 text-xs leading-relaxed">{card.position_interpretation || card.core_meaning}</p>
                    <div className="flex flex-wrap gap-1 pt-1">
                      {(card.keywords || []).slice(0, 3).map(kw => (
                        <span key={kw} className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-gray-300 border border-white/5">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Synthesized Narrative */}
              {readerResult.narrative && (
                <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/20">
                  <h4 className="text-xs font-bold text-indigo-300 uppercase tracking-wider mb-1">
                    Synthesized Reader Guidance Brief
                  </h4>
                  <p className="text-xs text-gray-300 leading-relaxed">
                    {readerResult.narrative.summary || readerResult.narrative.general || JSON.stringify(readerResult.narrative)}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ═══════ ANALYTICS TAB ═══════ */}
      {activeTab === 'analytics' && (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Total Readings
                <Layers className="w-4 h-4 text-indigo-400" />
              </div>
              <div className="text-2xl font-extrabold text-white mt-2">120</div>
              <div className="text-xs text-indigo-300 mt-1 flex items-center gap-1"><ArrowUpRight className="w-3 h-3" /> +12 this week</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Avg Rating
                <Star className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-2xl font-extrabold text-amber-300 mt-2">4.7</div>
              <div className="text-xs text-gray-400 mt-1">Out of 5.0 stars</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Active Seekers
                <Users className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-extrabold text-emerald-400 mt-2">34</div>
              <div className="text-xs text-gray-400 mt-1">Unique users served</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Avg Duration
                <Clock className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="text-2xl font-extrabold text-cyan-300 mt-2">15m</div>
              <div className="text-xs text-gray-400 mt-1">Per reading session</div>
            </div>
          </div>

          {/* Spread Distribution & Top Cards */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-glass p-6 rounded-2xl border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <PieChart className="w-5 h-5 text-indigo-400" />
                <h3 className="text-white font-bold">Spread Distribution</h3>
              </div>
              <div className="space-y-3">
                {spreadStats.map(s => (
                  <div key={s.name}>
                    <div className="flex items-center justify-between text-sm mb-1">
                      <span className="text-gray-300">{s.name}</span>
                      <span className="text-indigo-300 font-semibold">{s.count} ({s.pct}%)</span>
                    </div>
                    <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400" style={{ width: `${s.pct}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-glass p-6 rounded-2xl border border-white/10">
              <div className="flex items-center gap-2 mb-4">
                <Shuffle className="w-5 h-5 text-amber-400" />
                <h3 className="text-white font-bold">Most Drawn Cards</h3>
              </div>
              <div className="space-y-3">
                {topCards.map((c, i) => (
                  <div key={c.name} className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/5">
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-bold text-gray-500 w-5">#{i + 1}</span>
                      <span className="text-white font-semibold text-sm">{c.name}</span>
                    </div>
                    <div className="flex items-center gap-4 text-xs">
                      <span className="text-gray-400">{c.draws} draws</span>
                      <span className="text-emerald-400 font-semibold">{c.pctUpright}% ↑</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {/* ═══════ SESSIONS TAB ═══════ */}
      {activeTab === 'sessions' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">Session Tracking</h2>
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <span className="text-xs text-gray-400">Showing latest 5 sessions</span>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">ID</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Seeker</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Spread</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Cards</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Duration</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Rating</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Date</th>
                </tr>
              </thead>
              <tbody>
                {recentSessions.map(s => (
                  <tr key={s.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-3 px-4 text-indigo-300 font-mono text-xs">{s.id}</td>
                    <td className="py-3 px-4 text-white font-medium">{s.seeker}</td>
                    <td className="py-3 px-4 text-gray-300">{s.spread}</td>
                    <td className="py-3 px-4">
                      <div className="flex flex-wrap gap-1">
                        {s.cards.map((c, i) => (
                          <span key={c} className={`px-2 py-0.5 rounded text-xs ${s.orientation[i] === 'reversed' ? 'bg-red-500/10 text-red-300 border border-red-500/20' : 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'}`}>
                            {c} {s.orientation[i] === 'reversed' ? '↓' : '↑'}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-gray-400">{s.duration}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-0.5">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-3 h-3 ${i < s.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-600'}`} />
                        ))}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-gray-400 text-xs">{s.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ═══════ ENGAGEMENT TAB ═══════ */}
      {activeTab === 'engagement' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">User Engagement Insights</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="text-gray-400 text-xs font-semibold uppercase mb-2">Return Rate</div>
              <div className="text-2xl font-extrabold text-emerald-400">78%</div>
              <div className="text-xs text-gray-400 mt-1">Users requesting 2+ readings</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="text-gray-400 text-xs font-semibold uppercase mb-2">Avg Feedback Score</div>
              <div className="text-2xl font-extrabold text-amber-300">4.6 / 5.0</div>
              <div className="text-xs text-gray-400 mt-1">Based on 96 reviews</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="text-gray-400 text-xs font-semibold uppercase mb-2">Peak Hours</div>
              <div className="text-2xl font-extrabold text-cyan-300">7–9 PM</div>
              <div className="text-xs text-gray-400 mt-1">Most active reading window</div>
            </div>
          </div>

          <div className="bg-glass p-6 rounded-2xl border border-white/10">
            <div className="flex items-center gap-2 mb-4">
              <CalendarDays className="w-5 h-5 text-indigo-400" />
              <h3 className="text-white font-bold">Weekly Reading Volume</h3>
            </div>
            <div className="flex items-end gap-3 h-40">
              {[8, 12, 6, 15, 22, 18, 14].map((val, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div className="w-full bg-gradient-to-t from-indigo-600 to-cyan-400 rounded-t-lg transition-all" style={{ height: `${(val / 22) * 100}%` }} />
                  <span className="text-xs text-gray-500">{['M', 'T', 'W', 'T', 'F', 'S', 'S'][i]}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-glass p-6 rounded-2xl border border-white/10">
            <div className="flex items-center gap-2 mb-4">
              <MessageSquare className="w-5 h-5 text-amber-400" />
              <h3 className="text-white font-bold">Recent Seeker Feedback</h3>
            </div>
            <div className="space-y-3">
              {[
                { seeker: 'Priya M.', text: 'Incredibly accurate reading! The 3-card spread perfectly captured my current situation.', rating: 5 },
                { seeker: 'Amit K.', text: 'Very detailed Celtic Cross interpretation. Helped me gain clarity on my career path.', rating: 4 },
                { seeker: 'Nisha R.', text: 'Quick but powerful single card reading. Will definitely come back for more!', rating: 5 },
              ].map((f, i) => (
                <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/5">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white font-semibold text-sm">{f.seeker}</span>
                    <div className="flex items-center gap-0.5">
                      {[...Array(f.rating)].map((_, j) => <Star key={j} className="w-3 h-3 text-amber-400 fill-amber-400" />)}
                    </div>
                  </div>
                  <p className="text-gray-300 text-sm">{f.text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ═══════ REPORTS TAB ═══════ */}
      {activeTab === 'reports' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Report Management</h2>
          <p className="text-sm text-gray-400">View, export, and manage reading interpretation reports generated for seekers.</p>
          <div className="space-y-3">
            {recentSessions.map(s => (
              <div key={s.id} className="bg-glass p-5 rounded-2xl border border-white/10 flex items-center justify-between hover:border-indigo-500/30 transition-all">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-indigo-900/50 border border-indigo-500/40 flex items-center justify-center">
                    <FileText className="w-5 h-5 text-indigo-300" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold text-sm">{s.spread} — {s.seeker}</h4>
                    <p className="text-gray-400 text-xs mt-0.5">{s.id} · {s.date} · {s.duration}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 text-xs font-semibold border border-emerald-500/20">Completed</span>
                  <button className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition-all">
                    View Report
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
