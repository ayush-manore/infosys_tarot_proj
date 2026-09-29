'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, ArrowLeft, Star, Flame, Droplets, Wind, Mountain, RotateCcw } from 'lucide-react';

const SUIT_ICONS = {
  wands: { Icon: Flame, color: 'text-orange-400', gradient: 'from-orange-600 to-red-600' },
  cups: { Icon: Droplets, color: 'text-blue-400', gradient: 'from-blue-600 to-cyan-600' },
  swords: { Icon: Wind, color: 'text-cyan-400', gradient: 'from-cyan-600 to-indigo-600' },
  pentacles: { Icon: Mountain, color: 'text-emerald-400', gradient: 'from-emerald-600 to-teal-600' },
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function TarotCardDetailPage({ params }) {
  const { id } = params;
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showReversed, setShowReversed] = useState(false);

  useEffect(() => {
    async function loadCard() {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/datasets/tarot/cards/${id}`);
        const data = await res.json();
        setCard(data.data || null);
      } catch (err) {
        console.error('Failed to load card:', err);
      } finally {
        setLoading(false);
      }
    }
    loadCard();
  }, [id]);

  if (loading) {
    return (
      <div className="bg-cosmic-radial min-h-screen flex items-center justify-center">
        <div className="text-gray-500 text-lg">Loading card...</div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="bg-cosmic-radial min-h-screen flex flex-col items-center justify-center gap-4">
        <div className="text-gray-400 text-lg">Card not found</div>
        <Link href="/datasets" className="text-purple-400 hover:text-purple-300 underline">← Back to Library</Link>
      </div>
    );
  }

  const isMajor = card.arcana === 'major';
  const suitCfg = card.suit ? SUIT_ICONS[card.suit] : null;
  const gradient = isMajor ? 'from-amber-500 to-purple-600' : (suitCfg?.gradient || 'from-purple-600 to-indigo-600');

  return (
    <div className="bg-cosmic-radial min-h-screen relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-purple-900/20 rounded-full blur-[150px] pointer-events-none" />

      {/* Header */}
      <header className="sticky top-0 z-50 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 lg:px-12 py-4 flex items-center justify-between">
        <Link href="/datasets" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm font-medium">
          <ArrowLeft className="w-4 h-4" /> Back to Mystic Library
        </Link>
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-amber-300" />
          </div>
          <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-indigo-200">MysticAI</span>
        </Link>
      </header>

      <main className="max-w-4xl mx-auto px-6 lg:px-12 py-12">
        {/* Card Hero */}
        <div className="flex flex-col md:flex-row gap-8 mb-10">
          {/* Visual Card */}
          <div className={`flex-shrink-0 w-full md:w-64 h-80 rounded-2xl bg-gradient-to-br ${gradient} p-[2px] shadow-2xl shadow-purple-900/30`}>
            <div className="w-full h-full rounded-2xl bg-cosmic-950/90 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center">
              <div className="text-5xl font-black text-white/90 mb-2">{card.number}</div>
              <div className="text-xl font-bold text-white mb-2">{card.name}</div>
              <div className={`text-xs uppercase tracking-widest font-semibold ${isMajor ? 'text-amber-400' : suitCfg?.color || 'text-gray-400'}`}>
                {isMajor ? '★ Major Arcana' : `${card.suit} • Minor Arcana`}
              </div>
              {card.element && (
                <div className="mt-3 text-xs text-gray-500">🌀 {card.element}</div>
              )}
              {card.zodiac_sign && (
                <div className="text-xs text-gray-500">✦ {card.zodiac_sign}</div>
              )}
            </div>
          </div>

          {/* Card Info */}
          <div className="flex-1">
            <div className={`text-xs uppercase tracking-widest font-semibold mb-2 ${isMajor ? 'text-amber-400' : suitCfg?.color || 'text-gray-400'}`}>
              {isMajor ? '★ Major Arcana' : `Suit of ${card.suit}`} • Card {card.number}
            </div>
            <h1 className="text-4xl font-extrabold text-white mb-4">{card.name}</h1>
            <p className="text-gray-400 leading-relaxed mb-6">{card.description}</p>

            {/* Keywords */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-2">Keywords</h3>
              <div className="flex flex-wrap gap-2">
                {card.keywords?.map((kw) => (
                  <span key={kw} className="text-xs px-3 py-1.5 rounded-full bg-purple-500/15 text-purple-300 border border-purple-500/20 font-medium">{kw}</span>
                ))}
              </div>
            </div>

            {/* Meta Info */}
            <div className="flex flex-wrap gap-4 text-sm text-gray-500">
              {card.element && (
                <div className="flex items-center gap-1.5">
                  <span className="text-amber-400">🌀</span> Element: <span className="text-gray-300">{card.element}</span>
                </div>
              )}
              {card.zodiac_sign && (
                <div className="flex items-center gap-1.5">
                  <span className="text-amber-400">✦</span> Zodiac: <span className="text-gray-300">{card.zodiac_sign}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Meaning Toggle */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-xl font-bold text-white">Card Meaning</h2>
            <button
              onClick={() => setShowReversed(!showReversed)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                showReversed
                  ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                  : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
              }`}
            >
              <RotateCcw className="w-4 h-4" />
              {showReversed ? '↓ Reversed' : '↑ Upright'}
            </button>
          </div>

          <div className={`rounded-xl p-6 border transition-all duration-500 ${
            showReversed
              ? 'bg-red-500/5 border-red-500/20'
              : 'bg-emerald-500/5 border-emerald-500/20'
          }`}>
            <p className="text-gray-300 leading-relaxed text-lg">
              {showReversed ? card.reversed_meaning : card.upright_meaning}
            </p>
          </div>
        </div>

        {/* Both Meanings Side by Side */}
        <div className="grid md:grid-cols-2 gap-4 mb-10">
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-5">
            <h3 className="text-sm font-bold text-emerald-400 mb-2 flex items-center gap-2">
              <span>↑</span> Upright Meaning
            </h3>
            <p className="text-sm text-gray-400 leading-relaxed">{card.upright_meaning}</p>
          </div>
          <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-5">
            <h3 className="text-sm font-bold text-red-400 mb-2 flex items-center gap-2">
              <span>↓</span> Reversed Meaning
            </h3>
            <p className="text-sm text-gray-400 leading-relaxed">{card.reversed_meaning}</p>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-center">
          <Link
            href="/datasets"
            className="px-6 py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-900/40 hover:from-purple-500 hover:to-indigo-500 transition-all flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" /> Browse All Cards
          </Link>
        </div>
      </main>
    </div>
  );
}
