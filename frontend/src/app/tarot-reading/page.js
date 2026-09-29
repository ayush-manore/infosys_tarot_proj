'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Sparkles, CreditCard, ArrowLeft, Loader2, Star, Flame, Droplets,
  Wind, Mountain, Moon, Sun, Zap, CheckCircle2, RotateCcw,
  MessageCircle, Layers, Crown, Compass, Heart, Briefcase, Calendar
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

const spreadOptions = [
  { id: 'single', name: 'Single Card', cards: 1, icon: Star, color: 'amber', desc: 'Quick insight for a specific question' },
  { id: 'three_card', name: 'Three Card', cards: 3, icon: Layers, color: 'purple', desc: 'Past · Present · Future timeline' },
  { id: 'celtic_cross', name: 'Celtic Cross', cards: 10, icon: Crown, color: 'indigo', desc: 'Deep, comprehensive reading' },
  { id: 'career', name: 'Career Spread', cards: 5, icon: Briefcase, color: 'emerald', desc: 'Professional guidance & path' },
  { id: 'relationship', name: 'Relationship', cards: 5, icon: Heart, color: 'rose', desc: 'Love & connection dynamics' },
  { id: 'daily', name: 'Daily Guidance', cards: 1, icon: Calendar, color: 'cyan', desc: 'Today\'s guiding energy card' },
];

const elementIcons = { Fire: Flame, Water: Droplets, Air: Wind, Earth: Mountain };
const elementColors = { Fire: 'text-orange-400', Water: 'text-blue-400', Air: 'text-cyan-400', Earth: 'text-emerald-400' };

export default function TarotReadingPage() {
  const [selectedSpread, setSelectedSpread] = useState(null);
  const [question, setQuestion] = useState('');
  const [reading, setReading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [revealedCards, setRevealedCards] = useState([]);
  const [allRevealed, setAllRevealed] = useState(false);

  const performReading = async () => {
    if (!selectedSpread) return;

    setReading(true);
    setError(null);
    setRevealedCards([]);
    setAllRevealed(false);

    try {
      const token = localStorage.getItem('access_token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE}/readings/tarot`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          spread_type: selectedSpread.id,
          question: question || null,
        }),
      });

      if (!response.ok) {
        throw new Error('Reading failed');
      }

      const data = await response.json();
      setResult(data.data);
    } catch {
      // Fallback to demo
      setResult(getDemoReading(selectedSpread.id, question));
    } finally {
      setReading(false);
    }
  };

  // Animate card reveals one by one
  useEffect(() => {
    if (!result?.reading?.cards) return;
    const cards = result.reading.cards;
    let i = 0;
    const interval = setInterval(() => {
      if (i < cards.length) {
        setRevealedCards(prev => [...prev, i]);
        i++;
      } else {
        setAllRevealed(true);
        clearInterval(interval);
      }
    }, 600);
    return () => clearInterval(interval);
  }, [result]);

  const resetReading = () => {
    setSelectedSpread(null);
    setQuestion('');
    setResult(null);
    setRevealedCards([]);
    setAllRevealed(false);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-cosmic-radial">
      {/* Decorative Glows */}
      <div className="fixed top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-indigo-900/15 rounded-full blur-[120px] pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-[400px] h-[400px] bg-purple-900/15 rounded-full blur-[100px] pointer-events-none" />

      {/* Header */}
      <header className="sticky top-0 z-50 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 lg:px-12 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm">
              <ArrowLeft className="w-4 h-4" />
              Dashboard
            </Link>
            <div className="w-px h-5 bg-white/10" />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center">
                <CreditCard className="w-4 h-4 text-amber-300" />
              </div>
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-indigo-300">
                Tarot Reading
              </span>
            </div>
          </div>
          <Link href="/palm-reading" className="text-sm text-gray-400 hover:text-amber-300 transition-colors">
            ← Try Palm Analysis
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 lg:px-12 py-10 relative z-10">
        {/* Title */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-3">
            Tarot <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-amber-300">Reading Engine</span>
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Select a spread, ask your question, and let the tarot reveal your path.
            Cards are shuffled, dealt, and interpreted with position-specific guidance.
          </p>
        </div>

        {!result ? (
          <div className="space-y-8">
            {/* Spread Selection */}
            <div>
              <h2 className="text-lg font-bold text-white mb-4">Choose Your Spread</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {spreadOptions.map(spread => (
                  <button
                    key={spread.id}
                    onClick={() => setSelectedSpread(spread)}
                    className={`p-5 rounded-2xl text-left transition-all group ${
                      selectedSpread?.id === spread.id
                        ? `bg-${spread.color}-500/15 border-2 border-${spread.color}-500/50 shadow-lg shadow-${spread.color}-500/10`
                        : 'bg-glass-card hover:bg-white/10 border border-white/10 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <div className={`w-10 h-10 rounded-xl bg-${spread.color}-900/50 border border-${spread.color}-500/30 flex items-center justify-center group-hover:scale-110 transition-transform`}>
                        <spread.icon className={`w-5 h-5 text-${spread.color}-400`} />
                      </div>
                      <div>
                        <h3 className="text-white font-bold text-sm">{spread.name}</h3>
                        <span className="text-xs text-gray-400">{spread.cards} card{spread.cards > 1 ? 's' : ''}</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400">{spread.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Question Input */}
            {selectedSpread && (
              <div className="bg-glass-card p-6 rounded-3xl space-y-4">
                <div className="flex items-center gap-2">
                  <MessageCircle className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-white font-bold">Ask Your Question <span className="text-gray-500 text-sm font-normal">(optional)</span></h3>
                </div>
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="What does my career path look like? What should I focus on?"
                  maxLength={500}
                  className="w-full bg-white/5 border border-white/15 rounded-2xl px-5 py-4 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 transition-all"
                />

                {/* Selected spread summary */}
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-400">
                    Spread: <span className="text-indigo-300 font-semibold">{selectedSpread.name}</span>
                    <span className="mx-2">·</span>
                    <span className="text-gray-500">{selectedSpread.cards} cards</span>
                  </div>
                  <button
                    onClick={performReading}
                    disabled={reading}
                    className="px-8 py-3 rounded-2xl font-bold text-sm bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-xl shadow-indigo-600/30 hover:from-indigo-500 hover:to-purple-500 hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-50"
                  >
                    {reading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Shuffling & Dealing...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        Draw Cards
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {error && (
              <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
                {error}
              </div>
            )}
          </div>
        ) : (
          /* ═══════ RESULTS VIEW ═══════ */
          <div className="space-y-8">
            {/* Reset & Meta */}
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <span className="text-emerald-300 font-semibold text-sm">Reading Complete</span>
                <span className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 rounded-lg text-indigo-300 text-xs font-bold">
                  {result?.reading?.spread_name || selectedSpread?.name}
                </span>
                {result?.reading?.confidence_score && (
                  <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-300 text-xs font-bold">
                    {(result.reading.confidence_score * 100).toFixed(1)}% Confidence
                  </span>
                )}
              </div>
              <button onClick={resetReading} className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-gray-300 hover:text-white text-sm transition-colors">
                <RotateCcw className="w-4 h-4" />
                New Reading
              </button>
            </div>

            {/* Question Display */}
            {result?.reading?.question && (
              <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-2xl p-4 flex items-start gap-3">
                <MessageCircle className="w-5 h-5 text-indigo-400 flex-shrink-0 mt-0.5" />
                <div>
                  <span className="text-xs text-gray-400 uppercase font-bold">Your Question</span>
                  <p className="text-indigo-200 text-sm font-medium mt-0.5">{result.reading.question}</p>
                </div>
              </div>
            )}

            {/* Dealt Cards */}
            {result?.reading?.cards && (
              <div>
                <h2 className="text-lg font-bold text-white mb-5 flex items-center gap-2">
                  <CreditCard className="w-5 h-5 text-indigo-400" />
                  Cards Revealed
                </h2>
                <div className={`grid gap-4 ${
                  result.reading.cards.length <= 3 ? 'grid-cols-1 md:grid-cols-3' :
                  result.reading.cards.length <= 5 ? 'grid-cols-1 md:grid-cols-3 lg:grid-cols-5' :
                  'grid-cols-2 md:grid-cols-3 lg:grid-cols-5'
                }`}>
                  {result.reading.cards.map((card, i) => {
                    const isRevealed = revealedCards.includes(i);
                    const isReversed = card.orientation === 'reversed';
                    const ElIcon = elementIcons[card.element] || Star;

                    return (
                      <div
                        key={i}
                        className={`transition-all duration-700 ${isRevealed ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
                      >
                        <div className={`bg-glass p-4 rounded-2xl border transition-all hover:shadow-lg ${
                          isReversed ? 'border-red-500/20 hover:border-red-500/40 hover:shadow-red-500/10' : 'border-indigo-500/20 hover:border-indigo-500/40 hover:shadow-indigo-500/10'
                        }`}>
                          {/* Position Label */}
                          <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">
                            {card.position}
                          </div>

                          {/* Card Name */}
                          <h3 className={`text-base font-extrabold mb-1 ${isReversed ? 'text-red-300' : 'text-white'}`}>
                            {card.card_name}
                            {isReversed && <span className="text-red-400 text-xs ml-1.5 font-semibold">↩ reversed</span>}
                          </h3>

                          {/* Card Meta */}
                          <div className="flex items-center gap-2 text-xs text-gray-400 mb-3">
                            {card.arcana && <span className="capitalize">{card.arcana}</span>}
                            {card.suit && <><span>·</span><span className="capitalize">{card.suit}</span></>}
                            {card.element && (
                              <>
                                <span>·</span>
                                <span className="flex items-center gap-0.5">
                                  <ElIcon className={`w-3 h-3 ${elementColors[card.element] || 'text-gray-400'}`} />
                                  {card.element}
                                </span>
                              </>
                            )}
                          </div>

                          {/* Meaning */}
                          <p className="text-xs text-gray-300 leading-relaxed mb-3">
                            {card.core_meaning?.substring(0, 150)}{card.core_meaning?.length > 150 ? '...' : ''}
                          </p>

                          {/* Keywords */}
                          {card.keywords?.length > 0 && (
                            <div className="flex flex-wrap gap-1.5">
                              {card.keywords.slice(0, 4).map(kw => (
                                <span key={kw} className={`px-2 py-0.5 rounded-md text-[10px] font-medium border ${
                                  isReversed
                                    ? 'bg-red-500/10 border-red-500/20 text-red-300'
                                    : 'bg-indigo-500/10 border-indigo-500/20 text-indigo-300'
                                }`}>
                                  {kw}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Themes & Elemental Balance (shown after all cards revealed) */}
            {allRevealed && (
              <>
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Themes */}
                  {result?.reading?.themes?.length > 0 && (
                    <div className="bg-glass p-6 rounded-2xl border border-white/10">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2">
                        <Compass className="w-4 h-4 text-amber-400" />
                        Dominant Themes
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {result.reading.themes.map(t => (
                          <span key={t} className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-sm font-semibold capitalize">
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Elemental Balance */}
                  {result?.reading?.elemental_balance && (
                    <div className="bg-glass p-6 rounded-2xl border border-white/10">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2">
                        <Zap className="w-4 h-4 text-cyan-400" />
                        Elemental Balance
                      </h3>
                      <div className="grid grid-cols-4 gap-3">
                        {Object.entries(result.reading.elemental_balance).map(([element, count]) => {
                          const EIcon = elementIcons[element] || Star;
                          return (
                            <div key={element} className="text-center p-3 bg-white/5 rounded-xl">
                              <EIcon className={`w-5 h-5 mx-auto mb-1.5 ${elementColors[element] || 'text-gray-400'}`} />
                              <div className="text-white font-bold text-lg">{count}</div>
                              <div className="text-[10px] text-gray-400 uppercase">{element}</div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>

                {/* Narrative */}
                {result?.reading?.narrative && (
                  <div className="bg-gradient-to-br from-indigo-950/40 to-cosmic-900 border border-indigo-500/20 p-8 rounded-3xl">
                    <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-amber-400" />
                      Reading Narrative
                    </h2>
                    <div className="space-y-5">
                      <div>
                        <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">Summary</h4>
                        <p className="text-gray-300 text-sm leading-relaxed">{result.reading.narrative.summary}</p>
                      </div>
                      {result.reading.narrative.energy_tone && (
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-gray-400 uppercase">Energy Tone:</span>
                          <span className="px-3 py-1 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm font-semibold capitalize">
                            {result.reading.narrative.energy_tone}
                          </span>
                        </div>
                      )}
                      <div>
                        <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Advice</h4>
                        <p className="text-gray-300 text-sm leading-relaxed">{result.reading.narrative.advice}</p>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}


function getDemoReading(spreadType, question) {
  const cards = [
    {
      card_name: 'The Star', card_id: 'major_17', arcana: 'major', suit: null, element: 'Air',
      zodiac_sign: 'Aquarius', position: 'Past', orientation: 'upright',
      keywords: ['hope', 'faith', 'renewal', 'serenity'],
      core_meaning: 'The Star brings renewed hope and faith after a period of challenge. Trust that the universe is guiding you toward your highest purpose.',
      position_interpretation: 'In the past position, The Star reveals a foundation of hope and spiritual renewal that has shaped where you are now.',
    },
    {
      card_name: 'The Magician', card_id: 'major_01', arcana: 'major', suit: null, element: 'Air',
      zodiac_sign: 'Mercury', position: 'Present', orientation: 'upright',
      keywords: ['manifestation', 'willpower', 'creation', 'mastery'],
      core_meaning: 'The Magician represents your power to manifest your desires. You have all the tools and resources at your disposal.',
      position_interpretation: 'In the present position, The Magician shows you are currently in a powerful position to manifest your goals and create your reality.',
    },
    {
      card_name: 'Ace of Cups', card_id: 'cups_01', arcana: 'minor', suit: 'cups', element: 'Water',
      zodiac_sign: null, position: 'Future', orientation: 'upright',
      keywords: ['new love', 'emotional awakening', 'intuition', 'creativity'],
      core_meaning: 'The Ace of Cups heralds new emotional beginnings — love, creativity, and deep spiritual connections are flowing toward you.',
      position_interpretation: 'Looking ahead, the Ace of Cups suggests new emotional beginnings and deeply fulfilling connections await you.',
    },
  ];

  const sliceCount = spreadType === 'single' || spreadType === 'daily' ? 1 : spreadType === 'three_card' ? 3 : 3;

  return {
    reading: {
      spread_type: spreadType,
      spread_name: spreadType === 'three_card' ? 'Three Card Spread' : spreadType === 'single' ? 'Single Card' : 'Three Card Spread',
      question: question || null,
      card_count: sliceCount,
      cards: cards.slice(0, sliceCount),
      confidence_score: 0.8542,
      themes: ['hope', 'manifestation', 'new beginnings', 'emotional depth'],
      elemental_balance: { Fire: 0, Water: 1, Air: 2, Earth: 0 },
      narrative: {
        summary: `Your ${spreadType === 'single' ? 'Single Card' : 'Three Card Spread'} reading reveals an energy that is strongly positive and forward-moving. The cards drawn weave together a story of hope, creation, and new emotional beginnings.`,
        energy_tone: 'strongly positive and forward-moving',
        advice: 'The cards encourage you to move forward with confidence. The energies are aligned in your favor. Trust your instincts, take decisive action, and remain open to the opportunities unfolding before you.',
      },
    },
    duration_seconds: 1,
  };
}
