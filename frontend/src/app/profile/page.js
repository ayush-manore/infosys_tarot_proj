'use client';
import { API_BASE, authHeader } from '@/utils/api';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ArrowLeft, User, Sparkles, Save, Check, RefreshCw,
  Compass, Flame, Heart, Brain, Moon, Sun, Star, Zap,
  CheckCircle2, Copy, Layers, Hand, CreditCard, ChevronRight,
  TrendingUp, Award, ExternalLink, Loader2, BookOpen
} from 'lucide-react';



export default function ProfilePage() {
  const [activeView, setActiveView] = useState('profile'); // 'profile' or 'recommendations'
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

  // AI Recommendation State
  const [recommendations, setRecommendations] = useState(null);
  const [recLoading, setRecLoading] = useState(false);
  const [recError, setRecError] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');
  const [copiedAffirmation, setCopiedAffirmation] = useState(false);
  const [completedPractices, setCompletedPractices] = useState({});

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    // Check URL params for tab=recommendations
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (params.get('tab') === 'recommendations') {
        setActiveView('recommendations');
      }
    }

    if (!token) {
      setLoading(false);
      // Load fallback recommendations
      setRecommendations(getSampleRecommendations());
      return;
    }

    // Fetch user profile
    fetch(`${API_BASE}/profiles/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.status === 'success' && data.data) {
          setProfile(prev => ({ ...prev, ...data.data }));
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));

    // Fetch AI Recommendations based on readings
    fetchAiRecommendations(token);
  }, []);

  const fetchAiRecommendations = async (authToken) => {
    setRecLoading(true);
    setRecError(null);
    const token = authToken || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

    try {
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const res = await fetch(`${API_BASE}/ai/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
        body: JSON.stringify({ include_reading_history: true }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.status === 'success' && data.data?.ai_recommendations) {
          setRecommendations(data.data.ai_recommendations);
          return;
        }
      }
      // If server returns error, use enriched fallback
      setRecommendations(getSampleRecommendations(profile));
    } catch (err) {
      setRecommendations(getSampleRecommendations(profile));
    } finally {
      setRecLoading(false);
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    try {
      const res = await fetch(`${API_BASE}/profiles/me`, {
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
        // Refresh recommendations with updated profile goals
        fetchAiRecommendations(token);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCopyAffirmation = (text) => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(text);
      setCopiedAffirmation(true);
      setTimeout(() => setCopiedAffirmation(false), 2500);
    }
  };

  const togglePractice = (id) => {
    setCompletedPractices(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const filteredRecs = (recommendations?.growth_recommendations || []).filter(item => {
    if (activeCategory === 'all') return true;
    return item.category?.toLowerCase().includes(activeCategory);
  });

  return (
    <div className="min-h-screen bg-cosmic-radial text-white p-4 sm:p-6 md:p-10 flex flex-col">
      <div className="max-w-4xl w-full mx-auto space-y-6 flex-1">
        {/* Navigation & Breadcrumbs */}
        <div className="flex items-center justify-between">
          <Link href="/dashboard" className="inline-flex items-center gap-2 text-sm text-purple-300 hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Dashboard
          </Link>
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <Link href="/reports" className="hover:text-purple-300 transition-colors">Reports</Link>
            <span>•</span>
            <Link href="/tarot-reading" className="hover:text-purple-300 transition-colors">Tarot</Link>
            <span>•</span>
            <Link href="/palm-reading" className="hover:text-purple-300 transition-colors">Palmistry</Link>
          </div>
        </div>

        {/* 🌟 PROMINENT TOP HERO BUTTON FOR AI RECOMMENDATIONS 🌟 */}
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 via-pink-600 to-amber-500 rounded-3xl blur-md opacity-40 group-hover:opacity-75 transition duration-500 animate-pulse" />
          <div className="relative bg-gradient-to-r from-cosmic-950 via-purple-950/80 to-cosmic-950 border border-purple-500/40 rounded-3xl p-5 md:p-6 shadow-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4 text-left">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-purple-600 via-fuchsia-600 to-amber-400 flex items-center justify-center shadow-lg shadow-purple-500/30 shrink-0">
                <Sparkles className="w-7 h-7 text-white animate-bounce" />
              </div>
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <h2 className="text-lg md:text-xl font-bold text-white">AI Reading Recommendations</h2>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-400/20 text-amber-300 border border-amber-400/30 uppercase tracking-wider">
                    Based on Your Readings
                  </span>
                </div>
                <p className="text-xs text-purple-200/80 mt-1 max-w-xl">
                  Deeply personalized rituals, growth practices, daily affirmations, and crystals synthesized from your palm & tarot history.
                </p>
              </div>
            </div>
            
            <button
              id="ai-recommendations-top-btn"
              onClick={() => setActiveView(activeView === 'recommendations' ? 'profile' : 'recommendations')}
              className={`px-5 py-3 rounded-2xl font-bold text-xs uppercase tracking-wider transition-all duration-300 flex items-center gap-2 shrink-0 shadow-lg ${
                activeView === 'recommendations'
                  ? 'bg-white/10 hover:bg-white/20 text-white border border-white/20'
                  : 'bg-gradient-to-r from-purple-500 via-indigo-500 to-fuchsia-500 hover:from-purple-400 hover:to-fuchsia-400 text-white shadow-purple-500/30 hover:scale-105 active:scale-95'
              }`}
            >
              <Sparkles className="w-4 h-4 text-amber-300" />
              <span>{activeView === 'recommendations' ? 'View Profile Settings' : 'Explore AI Guidance'}</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex bg-white/[0.03] p-1.5 rounded-2xl border border-white/10 max-w-md mx-auto">
          <button
            onClick={() => setActiveView('profile')}
            className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
              activeView === 'profile'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <User className="w-4 h-4" />
            <span>Profile & Preferences</span>
          </button>
          <button
            onClick={() => setActiveView('recommendations')}
            className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
              activeView === 'recommendations'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-600/30'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>AI Recommendations</span>
          </button>
        </div>

        {/* ========================================================= */}
        {/* VIEW 1: AI RECOMMENDATIONS BASED ON READINGS              */}
        {/* ========================================================= */}
        {activeView === 'recommendations' && (
          <div className="space-y-6">
            {/* Header & Metrics Card */}
            <div className="bg-glass-card p-6 md:p-8 rounded-3xl border border-white/10 shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />
              
              <div className="flex flex-wrap items-center justify-between gap-4 relative z-10">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
                    <span className="text-xs text-purple-300 font-semibold uppercase tracking-wider">
                      Live Reading Synthesis Engine
                    </span>
                  </div>
                  <h2 className="text-2xl font-bold text-white mt-1">Your Personalized AI Guidance</h2>
                  <p className="text-xs text-gray-300 mt-1">
                    Continuous spiritual guidance generated from your reading history, palm lines, and soul archetypes.
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => fetchAiRecommendations()}
                    disabled={recLoading}
                    className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-xs font-semibold text-purple-200 transition-colors shadow-sm disabled:opacity-50"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${recLoading ? 'animate-spin' : ''}`} />
                    <span>{recLoading ? 'Analyzing...' : 'Refresh Guidance'}</span>
                  </button>
                </div>
              </div>

              {/* Reading Insights Summary Bar */}
              {recommendations?.reading_insights_summary && (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-white/10">
                  <div className="bg-white/[0.03] p-3 rounded-xl border border-white/5">
                    <div className="text-[11px] text-gray-400 uppercase font-semibold">Readings Analyzed</div>
                    <div className="text-base font-bold text-white mt-0.5">
                      {recommendations.reading_insights_summary.total_readings || 5} Readings
                    </div>
                  </div>
                  <div className="bg-white/[0.03] p-3 rounded-xl border border-white/5">
                    <div className="text-[11px] text-gray-400 uppercase font-semibold">Elemental Balance</div>
                    <div className="text-base font-bold text-cyan-300 mt-0.5">
                      {recommendations.reading_insights_summary.elemental_balance || 'Water / Intuitive'}
                    </div>
                  </div>
                  <div className="bg-white/[0.03] p-3 rounded-xl border border-white/5">
                    <div className="text-[11px] text-gray-400 uppercase font-semibold">Dominant Resonance</div>
                    <div className="text-base font-bold text-purple-300 mt-0.5 truncate">
                      {recommendations.reading_insights_summary.dominant_trait || 'Intuitive Awareness'}
                    </div>
                  </div>
                  <div className="bg-white/[0.03] p-3 rounded-xl border border-white/5">
                    <div className="text-[11px] text-gray-400 uppercase font-semibold">Seeker Stage</div>
                    <div className="text-base font-bold text-amber-300 mt-0.5">
                      {recommendations.reading_insights_summary.readings_status || 'Active Seeker'}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Daily Practice & Weekly Focus Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Daily Spiritual Practice */}
              {recommendations?.daily_practice && (
                <div className="bg-glass-card p-6 rounded-3xl border border-white/10 shadow-xl flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-300 flex items-center justify-center">
                          <Sun className="w-4 h-4" />
                        </div>
                        <span className="text-xs font-bold uppercase tracking-wider text-amber-300">
                          Recommended Daily Practice
                        </span>
                      </div>
                      <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                        {recommendations.daily_practice.duration || '10 mins'}
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-white mt-3">
                      {recommendations.daily_practice.title}
                    </h3>
                    <p className="text-xs text-gray-300 mt-2 leading-relaxed">
                      {recommendations.daily_practice.description}
                    </p>
                  </div>

                  <button
                    onClick={() => togglePractice('daily')}
                    className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 border ${
                      completedPractices['daily']
                        ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300'
                        : 'bg-white/5 hover:bg-white/10 border-white/10 text-white'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{completedPractices['daily'] ? 'Completed Today! ✨' : 'Mark Completed Today'}</span>
                  </button>
                </div>
              )}

              {/* Weekly Sacred Focus & Rituals */}
              {recommendations?.weekly_focus && (
                <div className="bg-glass-card p-6 rounded-3xl border border-white/10 shadow-xl space-y-4">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-purple-500/20 text-purple-300 flex items-center justify-center">
                      <Moon className="w-4 h-4" />
                    </div>
                    <span className="text-xs font-bold uppercase tracking-wider text-purple-300">
                      Weekly Sacred Theme
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-white">
                      {recommendations.weekly_focus.theme}
                    </h3>
                    <p className="text-xs text-gray-300 mt-1 leading-relaxed">
                      {recommendations.weekly_focus.description}
                    </p>
                  </div>

                  {/* Checklist of suggested activities */}
                  {recommendations.weekly_focus.activities && (
                    <div className="space-y-2 pt-1">
                      {recommendations.weekly_focus.activities.map((act, i) => (
                        <div
                          key={i}
                          onClick={() => togglePractice(`act-${i}`)}
                          className="flex items-start gap-2.5 p-2 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] border border-white/5 cursor-pointer transition-colors"
                        >
                          <div className={`w-4 h-4 rounded-md border mt-0.5 flex items-center justify-center shrink-0 ${
                            completedPractices[`act-${i}`] ? 'bg-purple-600 border-purple-500 text-white' : 'border-white/20'
                          }`}>
                            {completedPractices[`act-${i}`] && <Check className="w-3 h-3" />}
                          </div>
                          <span className={`text-xs ${completedPractices[`act-${i}`] ? 'line-through text-gray-500' : 'text-gray-300'}`}>
                            {act}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Mystical Prescriptions (Affirmation, Crystal, Meditation) */}
            <div className="grid sm:grid-cols-3 gap-4">
              {/* Affirmation */}
              {recommendations?.affirmation && (
                <div className="bg-gradient-to-br from-purple-900/30 to-indigo-900/30 p-5 rounded-2xl border border-purple-500/30 shadow-lg flex flex-col justify-between space-y-3">
                  <div>
                    <div className="flex items-center justify-between text-amber-300 text-xs font-bold uppercase tracking-wider mb-2">
                      <span className="flex items-center gap-1.5"><Sparkles className="w-3.5 h-3.5" /> Affirmation</span>
                      <button
                        onClick={() => handleCopyAffirmation(recommendations.affirmation)}
                        className="text-[10px] text-gray-400 hover:text-white flex items-center gap-1 bg-white/5 px-2 py-0.5 rounded"
                      >
                        <Copy className="w-3 h-3" /> {copiedAffirmation ? 'Copied!' : 'Copy'}
                      </button>
                    </div>
                    <p className="text-xs text-white font-medium italic leading-relaxed">
                      "{recommendations.affirmation}"
                    </p>
                  </div>
                  <div className="text-[10px] text-purple-300/80">Repeat 3x daily during moments of transition</div>
                </div>
              )}

              {/* Crystal Guidance */}
              {recommendations?.crystal_recommendation && (
                <div className="bg-gradient-to-br from-cyan-900/30 to-blue-900/30 p-5 rounded-2xl border border-cyan-500/30 shadow-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-cyan-300 text-xs font-bold uppercase tracking-wider">
                    <Star className="w-3.5 h-3.5" /> Crystal Prescription
                  </div>
                  <p className="text-xs text-white font-medium leading-relaxed">
                    {recommendations.crystal_recommendation}
                  </p>
                  <div className="text-[10px] text-cyan-200/70 pt-1">Balances your palm line frequencies</div>
                </div>
              )}

              {/* Meditation Focus */}
              {recommendations?.meditation_focus && (
                <div className="bg-gradient-to-br from-fuchsia-900/30 to-pink-900/30 p-5 rounded-2xl border border-fuchsia-500/30 shadow-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-fuchsia-300 text-xs font-bold uppercase tracking-wider">
                    <Brain className="w-3.5 h-3.5" /> Meditation Anchor
                  </div>
                  <p className="text-xs text-white font-medium leading-relaxed">
                    {recommendations.meditation_focus}
                  </p>
                  <div className="text-[10px] text-fuchsia-200/70 pt-1">Calibrates mental clarity & psychic receptors</div>
                </div>
              )}
            </div>

            {/* Categorized Growth Recommendations */}
            <div className="bg-glass-card p-6 md:p-8 rounded-3xl border border-white/10 shadow-2xl space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="text-xl font-bold text-white">Actionable Growth Pathways</h3>
                  <p className="text-xs text-gray-400 mt-0.5">Targeted steps mapped to your traits and reading revelations</p>
                </div>

                {/* Category filters */}
                <div className="flex flex-wrap gap-1.5 bg-white/5 p-1 rounded-xl border border-white/5 text-xs">
                  {['all', 'spiritual', 'wellness', 'career', 'relationships'].map((cat) => (
                    <button
                      key={cat}
                      onClick={() => setActiveCategory(cat)}
                      className={`px-3 py-1 rounded-lg capitalize font-medium transition-all ${
                        activeCategory === cat
                          ? 'bg-purple-600 text-white shadow-sm'
                          : 'text-gray-400 hover:text-white'
                      }`}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* Recommendation Cards */}
              <div className="grid md:grid-cols-2 gap-4">
                {filteredRecs.map((rec, i) => (
                  <div key={i} className="bg-white/[0.03] hover:bg-white/[0.06] p-5 rounded-2xl border border-white/10 hover:border-purple-500/40 transition-all space-y-3 shadow-md flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between gap-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                          rec.category === 'spiritual' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                          rec.category === 'career' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                          rec.category === 'relationships' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                          'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        }`}>
                          {rec.category || 'growth'}
                        </span>
                        {rec.impact && (
                          <span className="text-[10px] text-gray-400 font-medium">
                            {rec.impact.toUpperCase()} IMPACT · {rec.duration || '15 mins'}
                          </span>
                        )}
                      </div>

                      <h4 className="text-sm font-bold text-white mt-2.5">{rec.title}</h4>
                      <p className="text-xs text-gray-300 mt-1 leading-relaxed">{rec.description}</p>
                    </div>

                    <div className="pt-2 flex items-center justify-between text-[11px] text-purple-300/80 border-t border-white/5">
                      <span>Priority: #{rec.priority || i + 1}</span>
                      <span className="text-amber-300 font-semibold">Ready to practice</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions to deepen recommendations */}
            <div className="p-6 rounded-3xl bg-gradient-to-r from-purple-950/40 via-indigo-950/40 to-cosmic-950 border border-white/10 flex flex-wrap items-center justify-between gap-4">
              <div>
                <h4 className="text-sm font-bold text-white">Want even deeper AI recommendations?</h4>
                <p className="text-xs text-gray-400 mt-0.5">Take new readings to refine your life trend trajectory and spiritual accuracy.</p>
              </div>
              <div className="flex items-center gap-3">
                <Link
                  href="/tarot-reading"
                  className="px-4 py-2 rounded-xl bg-purple-600/80 hover:bg-purple-600 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-md"
                >
                  <CreditCard className="w-3.5 h-3.5" /> Draw Cards
                </Link>
                <Link
                  href="/palm-reading"
                  className="px-4 py-2 rounded-xl bg-indigo-600/80 hover:bg-indigo-600 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-md"
                >
                  <Hand className="w-3.5 h-3.5" /> Palm Scan
                </Link>
                <Link
                  href="/reports"
                  className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
                >
                  <BookOpen className="w-3.5 h-3.5" /> Full Reports
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* VIEW 2: PROFILE & PREFERENCES SETTINGS                     */}
        {/* ========================================================= */}
        {activeView === 'profile' && (
          <div className="bg-glass-card p-6 md:p-8 rounded-3xl border border-white/10 shadow-2xl space-y-6">
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
                <Check className="w-4 h-4" /> Profile settings saved successfully! Recommendations updated.
              </div>
            )}

            <form onSubmit={handleSaveProfile} className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">First Name</label>
                  <input
                    type="text"
                    value={profile.first_name || ''}
                    onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500/60"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Last Name</label>
                  <input
                    type="text"
                    value={profile.last_name || ''}
                    onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500/60"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Age Group</label>
                <select
                  value={profile.age_group || '26-35'}
                  onChange={(e) => setProfile({ ...profile, age_group: e.target.value })}
                  className="w-full px-4 py-2.5 bg-cosmic-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500/60"
                >
                  <option value="18-25">18-25</option>
                  <option value="26-35">26-35</option>
                  <option value="36-45">36-45</option>
                  <option value="46-55">46-55</option>
                  <option value="55+">55+</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Primary Spiritual Goal</label>
                <select
                  value={profile.spiritual_goals?.[0] || 'self_discovery'}
                  onChange={(e) => setProfile({ ...profile, spiritual_goals: [e.target.value] })}
                  className="w-full px-4 py-2.5 bg-cosmic-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500/60"
                >
                  <option value="self_discovery">Self Discovery & Archetype Understanding</option>
                  <option value="career_guidance">Career Guidance & Purpose Alignment</option>
                  <option value="relationship_healing">Relationship Harmony & Heart Opening</option>
                  <option value="spiritual_growth">Spiritual Growth & Intuitive Expansion</option>
                  <option value="stress_management">Stress Alchemy & Energetic Balance</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Preferred Tarot Spread</label>
                <select
                  value={profile.preferred_spread || 'three_card'}
                  onChange={(e) => setProfile({ ...profile, preferred_spread: e.target.value })}
                  className="w-full px-4 py-2.5 bg-cosmic-900 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500/60"
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
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm placeholder-gray-500 focus:outline-none focus:border-purple-500/60"
                  placeholder="Share your spiritual journey, intentions, or what brings you to MysticAI..."
                />
              </div>

              <div className="flex items-center justify-between pt-2">
                <button
                  type="submit"
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg shadow-purple-600/30 text-sm flex items-center gap-2 transition-all hover:scale-105 active:scale-95"
                >
                  <Save className="w-4 h-4" />
                  Save Preferences
                </button>

                <button
                  type="button"
                  onClick={() => setActiveView('recommendations')}
                  className="text-xs text-purple-300 hover:text-white flex items-center gap-1 underline underline-offset-4"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-300" /> View AI Recommendations →
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

function getSampleRecommendations(profile) {
  return {
    daily_practice: {
      title: "Third Eye Intuition Calibration",
      description: "Dedicate 10 minutes at sunrise to stillness and third-eye visualization. Reflect on your recent tarot archetypes and notice syncronicities throughout your day.",
      duration: "10-15 mins daily",
      category: "spiritual"
    },
    growth_recommendations: [
      {
        title: "Tarot Mirror Journaling",
        description: "Draw one card at dawn and write 3 stream-of-consciousness associations. Notice how its energy mirrors your interactions by dusk.",
        category: "spiritual",
        impact: "high",
        duration: "15 mins",
        priority: 1
      },
      {
        title: "Elemental Hand Energy Balancing",
        description: "Based on your Water palm alignment, ground yourself with 20 minutes of barefoot earth connection or salt water cleansing.",
        category: "wellness",
        impact: "high",
        duration: "20 mins",
        priority: 2
      },
      {
        title: "Strategic Intuition in Career",
        description: "Combine your analytical structure with intuitive gut-checks when making professional decisions this week.",
        category: "career",
        impact: "medium",
        duration: "Weekly review",
        priority: 3
      },
      {
        title: "Vulnerability & Connection Ritual",
        description: "Share one authentic spiritual or personal insight with someone in your inner circle to deepen mutual trust and heart alignment.",
        category: "relationships",
        impact: "high",
        duration: "Ongoing",
        priority: 4
      }
    ],
    weekly_focus: {
      theme: "Sacred Alignment & Intuitive Momentum",
      description: "Synthesized from your readings and energetic profile. Focus on trusting your inner compass and anchoring insights into tangible daily habits.",
      activities: [
        "Pull a 3-Card Tarot Spread on Wednesday to assess mid-week trajectory",
        "Perform a 5-minute palm breathing meditation focusing on your Life and Heart lines",
        "Clear your sacred space with sage or incense before sleep",
        "Write down 3 synchronicities you noticed during the week"
      ]
    },
    affirmation: "I trust the wisdom of my readings and allow the universe to guide my steps with clarity and grace.",
    crystal_recommendation: "Amethyst & Moonstone — Enhances intuition, psychic protection, and heart chakra alignment",
    meditation_focus: "Breath-Synchronized Third Eye Focus with Radiant Violet Light Visualization",
    reading_insights_summary: {
      total_readings: 5,
      elemental_balance: "Water / Intuitive",
      dominant_trait: "Intuitive Awareness (92%)",
      readings_status: "Active Seeker"
    }
  };
}
