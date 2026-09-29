'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
  Sparkles, Users, TrendingUp, Activity, Target, Heart, Brain,
  BarChart3, LineChart, Award, Clock, Compass, Eye, Shield,
  MessageCircle, ThumbsUp, Zap, CheckCircle2, AlertTriangle,
  Hand, CreditCard
} from 'lucide-react';

const clientOverview = [
  { name: 'Priya M.', sessions: 8, lastVisit: '2026-08-31', trend: 'improving', satisfaction: 92, focus: 'Emotional Healing' },
  { name: 'Amit K.', sessions: 5, lastVisit: '2026-08-30', trend: 'stable', satisfaction: 88, focus: 'Career Direction' },
  { name: 'Nisha R.', sessions: 12, lastVisit: '2026-08-30', trend: 'improving', satisfaction: 95, focus: 'Self-Discovery' },
  { name: 'Rahul S.', sessions: 3, lastVisit: '2026-08-29', trend: 'new', satisfaction: 82, focus: 'Relationship Guidance' },
  { name: 'Deepa L.', sessions: 6, lastVisit: '2026-08-28', trend: 'stable', satisfaction: 90, focus: 'Spiritual Growth' },
];

const guidanceEffectiveness = [
  { category: 'Self-Discovery', seekers: 18, avgImprovement: 24, icon: Eye },
  { category: 'Career Guidance', seekers: 12, avgImprovement: 19, icon: Target },
  { category: 'Emotional Healing', seekers: 15, avgImprovement: 31, icon: Heart },
  { category: 'Relationship Insight', seekers: 9, avgImprovement: 22, icon: MessageCircle },
  { category: 'Spiritual Growth', seekers: 14, avgImprovement: 27, icon: Compass },
];

const consultationLog = [
  { date: '2026-08-31', client: 'Priya M.', type: 'Combined (Palm + Tarot)', duration: '45 min', outcome: 'Breakthrough', notes: 'Major emotional clarity achieved. Heart Line analysis correlated with Queen of Cups draw.' },
  { date: '2026-08-30', client: 'Amit K.', type: 'Tarot Deep Dive', duration: '35 min', outcome: 'Progress', notes: 'Career spread showed strong alignment. The Emperor appeared upright — authority and structure themes.' },
  { date: '2026-08-29', client: 'Nisha R.', type: 'Palm Analysis', duration: '25 min', outcome: 'Insight', notes: 'Life Line shows strong vitality. Fate Line clarity indicates focused life direction.' },
  { date: '2026-08-27', client: 'Deepa L.', type: 'Combined (Palm + Tarot)', duration: '50 min', outcome: 'Breakthrough', notes: 'Spiritual growth trajectory confirmed by both palm features and Major Arcana dominance.' },
];

export default function ConsultantDashboard({ user }) {
  const [activeTab, setActiveTab] = useState('trends');
  const [logsList, setLogsList] = useState(consultationLog);
  const [seekerName, setSeekerName] = useState('');
  const [consultType, setConsultType] = useState('Combined (Palm + Tarot)');
  const [consultFocus, setConsultFocus] = useState('Emotional Healing');
  const [consultNotes, setConsultNotes] = useState('');
  const [consultLoading, setConsultLoading] = useState(false);
  const [consultResult, setConsultResult] = useState(null);
  const [consultError, setConsultError] = useState(null);

  const displayName = user?.email?.split('@')[0] || 'Consultant';

  const handleRunConsultation = async (e) => {
    e.preventDefault();
    setConsultLoading(true);
    setConsultError(null);
    setConsultResult(null);

    const token = localStorage.getItem('access_token');
    try {
      // Call combined reading endpoint or tarot reading
      const res = await fetch('http://localhost:8000/api/v1/readings/combined', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          tarot_spread: 'three_card',
          question: `[Consultation for ${seekerName}] Focus: ${consultFocus}. Notes: ${consultNotes}`
        })
      });

      const data = await res.json();
      if (res.ok && data.data?.reading) {
        const r = data.data.reading;
        setConsultResult(r);

        // Prepend to consultation logs
        const newLog = {
          date: new Date().toISOString().split('T')[0],
          client: seekerName || 'Client Seeker',
          type: consultType,
          duration: '45 min',
          outcome: 'Breakthrough',
          notes: `${consultFocus}: ${consultNotes || 'Comprehensive multi-line and archetype synergy achieved.'}`
        };
        setLogsList(prev => [newLog, ...prev]);
      } else {
        setConsultError(data.detail || 'Failed to execute consultation synthesis');
      }
    } catch (err) {
      setConsultError('Failed to connect to consultation orchestration service');
    } finally {
      setConsultLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-glass-card p-8 rounded-3xl border border-white/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-teal-600/8 rounded-full blur-[80px] pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-widest">Spiritual Consultant Dashboard</span>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-2">
              Welcome, <span className="text-emerald-300">{displayName}</span> 🙏
            </h1>
            <p className="text-gray-400 text-sm mt-2 max-w-2xl">
              Role: <span className="capitalize text-emerald-300 font-semibold">Spiritual Consultant</span> · Track client progress, measure guidance effectiveness, and review consultation insights.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveTab('new_consultation')}
              className="flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-sm shadow-lg shadow-emerald-600/30 transition-all transform hover:scale-105"
            >
              <Sparkles className="w-4 h-4 text-amber-300" />
              New Consultation Session
            </button>
            <Link
              href="/palm-reading"
              className="flex items-center gap-2 px-4 py-3 rounded-xl bg-white/10 hover:bg-white/15 text-white font-medium text-sm transition-all border border-white/10"
            >
              <Hand className="w-4 h-4 text-emerald-300" />
              Palm Scanner
            </Link>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'new_consultation', label: 'Consultation Launcher (Live)', icon: Sparkles },
          { id: 'trends', label: 'User Trend Analysis', icon: TrendingUp },
          { id: 'effectiveness', label: 'Guidance Effectiveness', icon: Target },
          { id: 'consultations', label: 'Consultation Insights', icon: MessageCircle },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* ═══════ LIVE CONSULTATION LAUNCHER (LIVE POWER) ═══════ */}
      {activeTab === 'new_consultation' && (
        <div className="space-y-6">
          <div className="bg-glass-card p-6 rounded-2xl border border-emerald-500/20">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold uppercase tracking-widest border border-emerald-500/30">
                Spiritual Consultant Authority Power
              </span>
              <span className="text-xs text-emerald-400 font-semibold">Multimodal Synthesis Engine</span>
            </div>
            <h2 className="text-2xl font-bold text-white">Initiate Client Spiritual Consultation</h2>
            <p className="text-xs text-gray-400 mt-1">
              Combine palm morphology with tarot archetypes to generate comprehensive breakthrough reports.
            </p>

            <form onSubmit={handleRunConsultation} className="mt-5 grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Client / Seeker Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Meera Kapoor"
                  value={seekerName}
                  onChange={(e) => setSeekerName(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 text-xs focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Consultation Mode
                </label>
                <select
                  value={consultType}
                  onChange={(e) => setConsultType(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-gray-900 border border-white/10 rounded-xl text-white text-xs focus:outline-none focus:border-emerald-500"
                >
                  <option value="Combined (Palm + Tarot)">Combined (Palm Morphology + Tarot Alignment)</option>
                  <option value="Palm Analysis">Deep Palmistry Crease Scan</option>
                  <option value="Tarot Deep Dive">Tarot Deep Archetype Dive</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Primary Focus Domain
                </label>
                <select
                  value={consultFocus}
                  onChange={(e) => setConsultFocus(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-gray-900 border border-white/10 rounded-xl text-white text-xs focus:outline-none focus:border-emerald-500"
                >
                  <option value="Emotional Healing">Emotional Healing & Heart Line Alignment</option>
                  <option value="Career Direction">Career Trajectory & Fate Line Clarity</option>
                  <option value="Self-Discovery">Cognitive Style & Head Line Analysis</option>
                  <option value="Spiritual Growth">Vitality & Major Arcana Synergy</option>
                  <option value="Relationship Guidance">Interpersonal Harmony</option>
                </select>
              </div>

              <div className="md:col-span-3">
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                  Consultant Observation Notes
                </label>
                <textarea
                  rows={3}
                  placeholder="Record confidential client observations, astrological correlations, or specific areas of resistance..."
                  value={consultNotes}
                  onChange={(e) => setConsultNotes(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 text-xs focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="md:col-span-3 flex items-center justify-between pt-2">
                <span className="text-xs text-gray-400">
                  ⚡ Calls FastAPI <code className="text-emerald-300">POST /api/v1/readings/combined</code> with Consultant authentication.
                </span>
                <button
                  type="submit"
                  disabled={consultLoading}
                  className="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold transition-all shadow-lg shadow-emerald-600/30 flex items-center gap-2"
                >
                  {consultLoading ? 'Synthesizing Multimodal Insights...' : 'Run Consultation Synthesis'}
                  <Sparkles className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>

            {consultError && (
              <div className="mt-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs">
                {consultError}
              </div>
            )}
          </div>

          {/* Result Card */}
          {consultResult && (
            <div className="bg-glass-card p-6 rounded-2xl border border-emerald-500/30 space-y-4 animate-fadeIn">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <div>
                  <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
                    ✓ Consultation Successfully Logged & Synced
                  </span>
                  <h3 className="text-xl font-bold text-white mt-1">
                    Multimodal Synthesis for <span className="text-amber-300">{seekerName || 'Seeker'}</span>
                  </h3>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold uppercase">
                  Breakthrough Achieved
                </span>
              </div>

              {consultResult.palm_analysis && (
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                    <h4 className="text-xs font-bold text-emerald-400 uppercase mb-2">Detected Hand Morphology</h4>
                    <p className="text-xs text-white font-semibold">{consultResult.palm_analysis.hand_shape?.type || 'Earth Hand'}</p>
                    <p className="text-xs text-gray-400 mt-1">{consultResult.palm_analysis.hand_shape?.element} element · {consultResult.palm_analysis.hand_shape?.temperament}</p>
                  </div>
                  <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                    <h4 className="text-xs font-bold text-emerald-400 uppercase mb-2">Major Crease Measurements</h4>
                    <p className="text-xs text-gray-300">
                      Heart Line: <span className="text-emerald-300 font-semibold">{consultResult.palm_analysis.detected_lines?.heart_line?.curvature || 'Curved'}</span> · 
                      Head Line: <span className="text-emerald-300 font-semibold">{consultResult.palm_analysis.detected_lines?.head_line?.length || 'Long'}</span>
                    </p>
                  </div>
                </div>
              )}

              {consultResult.combined_narrative && (
                <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/20">
                  <h4 className="text-xs font-bold text-emerald-300 uppercase tracking-wider mb-1">
                    Integrated Spiritual Diagnosis
                  </h4>
                  <p className="text-xs text-gray-300 leading-relaxed">
                    {consultResult.combined_narrative.synthesis || JSON.stringify(consultResult.combined_narrative)}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ═══════ USER TREND ANALYSIS ═══════ */}
      {activeTab === 'trends' && (
        <div className="space-y-6">
          {/* Overview Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Active Clients
                <Users className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-2xl font-extrabold text-white mt-2">28</div>
              <div className="text-xs text-emerald-300 mt-1">+4 new this month</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Avg Satisfaction
                <Award className="w-4 h-4 text-amber-400" />
              </div>
              <div className="text-2xl font-extrabold text-amber-300 mt-2">91%</div>
              <div className="text-xs text-gray-400 mt-1">Across all consultations</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Breakthroughs
                <Zap className="w-4 h-4 text-purple-400" />
              </div>
              <div className="text-2xl font-extrabold text-purple-300 mt-2">14</div>
              <div className="text-xs text-gray-400 mt-1">Life-changing sessions</div>
            </div>
            <div className="bg-glass p-5 rounded-2xl border border-white/10">
              <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase">
                Consultation Hours
                <Clock className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="text-2xl font-extrabold text-cyan-300 mt-2">86h</div>
              <div className="text-xs text-gray-400 mt-1">Total this month</div>
            </div>
          </div>

          {/* Client Overview Table */}
          <div className="bg-glass p-6 rounded-2xl border border-white/10">
            <h3 className="text-white font-bold mb-4 flex items-center gap-2">
              <Users className="w-5 h-5 text-emerald-400" />
              Client Overview & Trends
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Client</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Sessions</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Focus Area</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Trend</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Satisfaction</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-semibold text-xs uppercase">Last Visit</th>
                  </tr>
                </thead>
                <tbody>
                  {clientOverview.map(c => (
                    <tr key={c.name} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 text-white font-medium">{c.name}</td>
                      <td className="py-3 px-4 text-gray-300">{c.sessions}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded-lg bg-emerald-500/10 text-emerald-300 text-xs border border-emerald-500/20">{c.focus}</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded-lg text-xs font-semibold border ${
                          c.trend === 'improving' ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20' :
                          c.trend === 'stable' ? 'bg-cyan-500/10 text-cyan-300 border-cyan-500/20' :
                          'bg-amber-500/10 text-amber-300 border-amber-500/20'
                        }`}>{c.trend}</span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                            <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400" style={{ width: `${c.satisfaction}%` }} />
                          </div>
                          <span className="text-emerald-300 text-xs font-semibold">{c.satisfaction}%</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-400 text-xs">{c.lastVisit}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ═══════ GUIDANCE EFFECTIVENESS ═══════ */}
      {activeTab === 'effectiveness' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Guidance Effectiveness Metrics</h2>
          <p className="text-sm text-gray-400">Measuring the impact of your consultations across different guidance categories.</p>

          <div className="grid md:grid-cols-2 gap-4">
            {guidanceEffectiveness.map(g => (
              <div key={g.category} className="bg-glass p-5 rounded-2xl border border-white/10 hover:border-emerald-500/30 transition-all">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-emerald-900/50 border border-emerald-500/30 flex items-center justify-center">
                    <g.icon className="w-5 h-5 text-emerald-400" />
                  </div>
                  <div>
                    <h4 className="text-white font-semibold text-sm">{g.category}</h4>
                    <p className="text-gray-400 text-xs">{g.seekers} seekers guided</p>
                  </div>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">Avg. Improvement</span>
                  <span className="text-emerald-400 font-bold text-sm">+{g.avgImprovement}%</span>
                </div>
                <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400" style={{ width: `${g.avgImprovement * 3}%` }} />
                </div>
              </div>
            ))}
          </div>

          {/* Holistic Assessment Summary */}
          <div className="bg-gradient-to-br from-emerald-950/40 to-cosmic-900 border border-emerald-500/20 p-6 rounded-2xl">
            <h3 className="text-white font-bold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-emerald-400" />
              Holistic Assessment Summary
            </h3>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="text-center p-4 rounded-xl bg-white/5 border border-white/5">
                <div className="text-3xl font-extrabold text-emerald-400">87%</div>
                <div className="text-xs text-gray-400 mt-1">Seekers report positive change</div>
              </div>
              <div className="text-center p-4 rounded-xl bg-white/5 border border-white/5">
                <div className="text-3xl font-extrabold text-amber-300">4.8</div>
                <div className="text-xs text-gray-400 mt-1">Average consultation rating</div>
              </div>
              <div className="text-center p-4 rounded-xl bg-white/5 border border-white/5">
                <div className="text-3xl font-extrabold text-cyan-300">73%</div>
                <div className="text-xs text-gray-400 mt-1">Goal completion rate</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ═══════ CONSULTATION INSIGHTS ═══════ */}
      {activeTab === 'consultations' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Consultation Insights</h2>
          <p className="text-sm text-gray-400">Detailed log of your recent consultations, outcomes, and key observations.</p>
          <div className="space-y-4">
            {consultationLog.map((c, i) => (
              <div key={i} className="bg-glass p-6 rounded-2xl border border-white/10 hover:border-emerald-500/20 transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-white font-semibold">{c.client}</h4>
                    <p className="text-gray-400 text-xs mt-0.5">{c.type} · {c.duration} · {c.date}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-lg text-xs font-bold border ${
                    c.outcome === 'Breakthrough' ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' :
                    c.outcome === 'Progress' ? 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30' :
                    'bg-amber-500/15 text-amber-300 border-amber-500/30'
                  }`}>
                    {c.outcome === 'Breakthrough' && <CheckCircle2 className="w-3 h-3 inline mr-1" />}
                    {c.outcome}
                  </span>
                </div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                  <p className="text-gray-300 text-sm leading-relaxed">{c.notes}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
