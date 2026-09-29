'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, Search, Filter, Hand, Layers, Star, ArrowLeft, Shuffle, ChevronDown, Flame, Droplets, Wind, Mountain } from 'lucide-react';

const SUIT_CONFIG = {
  wands: { label: 'Wands', icon: Flame, color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/30', glow: 'shadow-orange-500/20' },
  cups: { label: 'Cups', icon: Droplets, color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/30', glow: 'shadow-blue-500/20' },
  swords: { label: 'Swords', icon: Wind, color: 'text-cyan-400', bg: 'bg-cyan-500/10', border: 'border-cyan-500/30', glow: 'shadow-cyan-500/20' },
  pentacles: { label: 'Pentacles', icon: Mountain, color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', glow: 'shadow-emerald-500/20' },
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function DatasetsPage() {
  const [activeTab, setActiveTab] = useState('tarot');
  const [cards, setCards] = useState([]);
  const [palmLines, setPalmLines] = useState([]);
  const [stats, setStats] = useState(null);
  const [drawnCards, setDrawnCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [arcanaFilter, setArcanaFilter] = useState('all');
  const [suitFilter, setSuitFilter] = useState('all');
  const [showDrawModal, setShowDrawModal] = useState(false);
  const [drawCount, setDrawCount] = useState(3);
  const [isDrawing, setIsDrawing] = useState(false);
  const [expandedLine, setExpandedLine] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [cardsRes, linesRes, statsRes] = await Promise.all([
        fetch(`${API_BASE}/datasets/tarot/cards`),
        fetch(`${API_BASE}/datasets/palmistry/lines`),
        fetch(`${API_BASE}/datasets/stats`),
      ]);
      const cardsData = await cardsRes.json();
      const linesData = await linesRes.json();
      const statsData = await statsRes.json();

      setCards(cardsData.data || []);
      setPalmLines(linesData.data || []);
      setStats(statsData.data || null);
    } catch (err) {
      console.error('Failed to load datasets:', err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDrawCards() {
    setIsDrawing(true);
    try {
      const res = await fetch(`${API_BASE}/datasets/tarot/cards/random?count=${drawCount}`);
      const data = await res.json();
      setDrawnCards(data.data || []);
      setShowDrawModal(true);
    } catch (err) {
      console.error('Failed to draw cards:', err);
    } finally {
      setIsDrawing(false);
    }
  }

  const filteredCards = cards.filter((card) => {
    if (arcanaFilter !== 'all' && card.arcana !== arcanaFilter) return false;
    if (suitFilter !== 'all' && card.suit !== suitFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        card.name.toLowerCase().includes(q) ||
        card.keywords?.some((k) => k.toLowerCase().includes(q))
      );
    }
    return true;
  });

  return (
    <div className="bg-cosmic-radial min-h-screen relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] bg-purple-900/15 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-indigo-900/15 rounded-full blur-[100px] pointer-events-none" />

      {/* Header */}
      <header className="sticky top-0 z-50 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 lg:px-12 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
            <span className="text-2xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-purple-300 to-indigo-200">
              MysticAI
            </span>
          </Link>
        </div>
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-300">
          <Link href="/" className="hover:text-amber-300 transition-colors flex items-center gap-1">
            <ArrowLeft className="w-4 h-4" /> Home
          </Link>
          <Link href="/dashboard" className="hover:text-amber-300 transition-colors">Dashboard</Link>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-6 lg:px-12 py-10">
        {/* Page Title */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-purple-500/30 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-4 backdrop-blur-sm">
            <Layers className="w-4 h-4 text-amber-400" />
            Integrated Datasets
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-purple-300 to-indigo-200 mb-3">
            Mystic Library
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto">
            Browse the complete tarot deck and palmistry reference guide powering MysticAI&apos;s spiritual intelligence engine.
          </p>
        </div>

        {/* Stats Bar */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatCard label="Total Tarot Cards" value={stats.tarot?.total_cards} icon={<Layers className="w-5 h-5 text-purple-400" />} />
            <StatCard label="Major Arcana" value={stats.tarot?.major_arcana} icon={<Star className="w-5 h-5 text-amber-400" />} />
            <StatCard label="Minor Arcana" value={stats.tarot?.minor_arcana} icon={<Sparkles className="w-5 h-5 text-indigo-400" />} />
            <StatCard label="Palm Lines" value={stats.palmistry?.total_lines} icon={<Hand className="w-5 h-5 text-emerald-400" />} />
          </div>
        )}

        {/* Tab Switcher */}
        <div className="flex items-center gap-2 mb-8">
          <button
            onClick={() => setActiveTab('tarot')}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'tarot'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-900/40'
                : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-white/10'
            }`}
          >
            <span className="flex items-center gap-2"><Layers className="w-4 h-4" /> Tarot Cards ({cards.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('palmistry')}
            className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'palmistry'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-900/40'
                : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-white/10'
            }`}
          >
            <span className="flex items-center gap-2"><Hand className="w-4 h-4" /> Palm Lines ({palmLines.length})</span>
          </button>

          {activeTab === 'tarot' && (
            <button
              onClick={handleDrawCards}
              disabled={isDrawing}
              className="ml-auto px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-900/40 hover:from-amber-400 hover:to-orange-400 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              <Shuffle className="w-4 h-4" /> {isDrawing ? 'Drawing...' : 'Draw Cards'}
            </button>
          )}
        </div>

        {/* ═══ TAROT TAB ═══ */}
        {activeTab === 'tarot' && (
          <>
            {/* Filters */}
            <div className="flex flex-wrap items-center gap-3 mb-6">
              <div className="relative flex-1 min-w-[200px]">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search cards by name or keyword..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-gray-200 text-sm placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/30 transition-all"
                />
              </div>
              <div className="relative">
                <select
                  value={arcanaFilter}
                  onChange={(e) => { setArcanaFilter(e.target.value); setSuitFilter('all'); }}
                  className="appearance-none pl-4 pr-9 py-2.5 rounded-xl bg-white/5 border border-white/10 text-gray-300 text-sm cursor-pointer focus:outline-none focus:border-purple-500/50"
                >
                  <option value="all">All Arcana</option>
                  <option value="major">Major Arcana</option>
                  <option value="minor">Minor Arcana</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
              </div>
              {arcanaFilter === 'minor' && (
                <div className="relative">
                  <select
                    value={suitFilter}
                    onChange={(e) => setSuitFilter(e.target.value)}
                    className="appearance-none pl-4 pr-9 py-2.5 rounded-xl bg-white/5 border border-white/10 text-gray-300 text-sm cursor-pointer focus:outline-none focus:border-purple-500/50"
                  >
                    <option value="all">All Suits</option>
                    <option value="wands">🔥 Wands</option>
                    <option value="cups">💧 Cups</option>
                    <option value="swords">💨 Swords</option>
                    <option value="pentacles">🌍 Pentacles</option>
                  </select>
                  <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
                </div>
              )}
              <span className="text-xs text-gray-500 ml-auto">{filteredCards.length} cards</span>
            </div>

            {/* Card Grid */}
            {loading ? (
              <div className="text-center py-20 text-gray-500">Loading tarot dataset...</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {filteredCards.map((card) => (
                  <TarotCard key={card.id} card={card} />
                ))}
              </div>
            )}
          </>
        )}

        {/* ═══ PALMISTRY TAB ═══ */}
        {activeTab === 'palmistry' && (
          <div className="space-y-4">
            {loading ? (
              <div className="text-center py-20 text-gray-500">Loading palmistry dataset...</div>
            ) : (
              palmLines.map((line) => (
                <PalmLineCard
                  key={line.id}
                  line={line}
                  isExpanded={expandedLine === line.id}
                  onToggle={() => setExpandedLine(expandedLine === line.id ? null : line.id)}
                />
              ))
            )}
          </div>
        )}
      </main>

      {/* ═══ DRAW MODAL ═══ */}
      {showDrawModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={() => setShowDrawModal(false)}>
          <div className="bg-cosmic-950 border border-white/10 rounded-2xl p-6 max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-amber-200 flex items-center gap-2">
                <Shuffle className="w-6 h-6" /> Your Reading
              </h2>
              <button onClick={() => setShowDrawModal(false)} className="text-gray-500 hover:text-white text-xl">✕</button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {drawnCards.map((card, idx) => (
                <div key={idx} className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                  <div className="text-xs text-purple-400 uppercase tracking-wider mb-1">Card {idx + 1}</div>
                  <div className="text-lg font-bold text-white mb-1">{card.name}</div>
                  <div className={`text-xs font-semibold px-3 py-1 rounded-full inline-block mb-3 ${
                    card.orientation === 'upright' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'
                  }`}>
                    {card.orientation === 'upright' ? '↑ Upright' : '↓ Reversed'}
                  </div>
                  <p className="text-sm text-gray-400 leading-relaxed">
                    {card.orientation === 'upright' ? card.upright_meaning : card.reversed_meaning}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-1 justify-center">
                    {card.keywords?.slice(0, 3).map((kw) => (
                      <span key={kw} className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/15 text-purple-300">{kw}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 flex justify-center gap-3">
              <button onClick={handleDrawCards} className="px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg hover:from-amber-400 hover:to-orange-400 transition-all flex items-center gap-2">
                <Shuffle className="w-4 h-4" /> Draw Again
              </button>
              <button onClick={() => setShowDrawModal(false)} className="px-5 py-2.5 rounded-xl text-sm font-semibold bg-white/5 text-gray-300 border border-white/10 hover:bg-white/10 transition-all">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


// ── Sub-Components ──────────────────────────────────────────────

function StatCard({ label, value, icon }) {
  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4 flex items-center gap-3">
      <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">{icon}</div>
      <div>
        <div className="text-2xl font-extrabold text-white">{value ?? '—'}</div>
        <div className="text-xs text-gray-500">{label}</div>
      </div>
    </div>
  );
}

function TarotCard({ card }) {
  const suitCfg = card.suit ? SUIT_CONFIG[card.suit] : null;
  const isMajor = card.arcana === 'major';

  return (
    <Link href={`/datasets/tarot/${card.id}`}>
      <div className={`group relative bg-white/5 backdrop-blur-sm border rounded-xl p-4 cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-xl ${
        isMajor ? 'border-amber-500/30 hover:border-amber-500/60 hover:shadow-amber-500/10' : `${suitCfg?.border || 'border-white/10'} hover:${suitCfg?.glow || ''}`
      }`}>
        {/* Card Number Badge */}
        <div className={`absolute top-3 right-3 w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
          isMajor ? 'bg-amber-500/20 text-amber-300' : `${suitCfg?.bg || 'bg-white/10'} ${suitCfg?.color || 'text-gray-300'}`
        }`}>
          {card.number}
        </div>

        {/* Arcana Badge */}
        <div className={`text-[10px] uppercase tracking-wider font-semibold mb-2 ${isMajor ? 'text-amber-400' : suitCfg?.color || 'text-gray-400'}`}>
          {isMajor ? '★ Major Arcana' : `${suitCfg?.label || card.suit}`}
        </div>

        {/* Card Name */}
        <h3 className="text-base font-bold text-white mb-2 group-hover:text-amber-200 transition-colors">{card.name}</h3>

        {/* Keywords */}
        <div className="flex flex-wrap gap-1 mb-3">
          {card.keywords?.slice(0, 3).map((kw) => (
            <span key={kw} className="text-[10px] px-2 py-0.5 rounded-full bg-white/5 text-gray-400 border border-white/5">{kw}</span>
          ))}
        </div>

        {/* Element & Zodiac */}
        <div className="flex items-center gap-2 text-[11px] text-gray-500">
          {card.element && <span>🌀 {card.element}</span>}
          {card.zodiac_sign && <span>✦ {card.zodiac_sign}</span>}
        </div>
      </div>
    </Link>
  );
}

function PalmLineCard({ line, isExpanded, onToggle }) {
  const elementColors = {
    Water: 'from-blue-600 to-cyan-600',
    Air: 'from-cyan-600 to-indigo-600',
    Earth: 'from-emerald-600 to-teal-600',
    Fire: 'from-orange-600 to-red-600',
  };
  const gradient = elementColors[line.element] || 'from-purple-600 to-indigo-600';

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl overflow-hidden transition-all duration-300">
      <button onClick={onToggle} className="w-full p-5 flex items-center gap-4 text-left hover:bg-white/5 transition-colors">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg flex-shrink-0`}>
          <Hand className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white">{line.name}</h3>
          <p className="text-xs text-gray-500">{line.alternative_names?.join(' • ')}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500 hidden sm:block">{line.element}</span>
          <span className="text-xs px-3 py-1 rounded-full bg-white/5 text-gray-400 border border-white/10">
            {Object.keys(line.interpretations || {}).length} interpretations
          </span>
          <ChevronDown className={`w-5 h-5 text-gray-500 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
        </div>
      </button>

      {isExpanded && (
        <div className="px-5 pb-5 border-t border-white/5">
          <div className="pt-4 mb-4">
            <p className="text-sm text-gray-300 leading-relaxed">{line.description}</p>
            <p className="text-xs text-gray-500 mt-2"><strong>Location:</strong> {line.location}</p>
          </div>

          <div className="mb-4">
            <h4 className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-2">Associated Traits</h4>
            <div className="flex flex-wrap gap-2">
              {line.associated_traits?.map((trait) => (
                <span key={trait} className="text-xs px-3 py-1 rounded-full bg-purple-500/15 text-purple-300 border border-purple-500/20">{trait}</span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3">Interpretations Guide</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {Object.entries(line.interpretations || {}).map(([key, meaning]) => (
                <div key={key} className="bg-white/5 rounded-lg p-3 border border-white/5">
                  <div className="text-xs font-semibold text-amber-300 mb-1 capitalize">{key.replace(/_/g, ' ')}</div>
                  <p className="text-xs text-gray-400 leading-relaxed">{meaning}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
