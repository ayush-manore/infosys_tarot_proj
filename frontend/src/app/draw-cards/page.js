'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import {
  Sparkles, ArrowLeft, RotateCcw, Shuffle, Star, Layers, Crown,
  Briefcase, Heart, Calendar, CreditCard, Flame, Droplets, Wind,
  Mountain, Moon, Sun, Zap, CheckCircle2, MessageCircle, Compass,
  Eye, Lock
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

/* ── Spread Definitions ─────────────────────────────────────── */
const spreads = [
  { id: 'single', name: 'Single Card', cards: 1, icon: Star, color: 'amber', desc: 'Quick insight — draw one card' },
  { id: 'three_card', name: 'Three Card', cards: 3, icon: Layers, color: 'purple', desc: 'Past · Present · Future' },
  { id: 'celtic_cross', name: 'Celtic Cross', cards: 10, icon: Crown, color: 'indigo', desc: 'Deep comprehensive reading' },
  { id: 'career', name: 'Career Spread', cards: 5, icon: Briefcase, color: 'emerald', desc: 'Professional guidance' },
  { id: 'relationship', name: 'Relationship', cards: 5, icon: Heart, color: 'rose', desc: 'Love & connection dynamics' },
  { id: 'daily', name: 'Daily Guidance', cards: 1, icon: Calendar, color: 'cyan', desc: 'Today\'s guiding energy' },
];

const elementIcons = { Fire: Flame, Water: Droplets, Air: Wind, Earth: Mountain };
const elementColors = { Fire: 'text-orange-400', Water: 'text-blue-400', Air: 'text-cyan-400', Earth: 'text-emerald-400' };

/* ── Full 78-Card Mini Deck (names only, for client-side visuals) ── */
const DECK_BACK_COUNT = 78;

export default function DrawCardsPage() {
  const [phase, setPhase] = useState('choose-spread'); // choose-spread | shuffling | draw | reading-complete
  const [selectedSpread, setSelectedSpread] = useState(null);
  const [question, setQuestion] = useState('');
  const [deckCards, setDeckCards] = useState([]); // the face-down deck for drawing
  const [drawnCards, setDrawnCards] = useState([]); // cards the user has drawn
  const [flippedIndexes, setFlippedIndexes] = useState(new Set());
  const [readingResult, setReadingResult] = useState(null);
  const [isShuffling, setIsShuffling] = useState(false);
  const [error, setError] = useState(null);
  const shuffleTimerRef = useRef(null);

  /* ── Build a visual deck ──────────────────────────────────── */
  const buildDeck = useCallback(() => {
    const cards = [];
    for (let i = 0; i < DECK_BACK_COUNT; i++) {
      cards.push({
        index: i,
        x: 0,
        y: 0,
        rotation: 0,
        selected: false,
      });
    }
    return cards;
  }, []);

  /* ── Shuffle animation ────────────────────────────────────── */
  const startShuffle = useCallback(() => {
    setIsShuffling(true);
    setPhase('shuffling');

    // Create a scattered deck animation
    const scattered = [];
    for (let i = 0; i < DECK_BACK_COUNT; i++) {
      scattered.push({
        index: i,
        x: (Math.random() - 0.5) * 400,
        y: (Math.random() - 0.5) * 200,
        rotation: (Math.random() - 0.5) * 60,
        selected: false,
      });
    }
    setDeckCards(scattered);

    // After 1.5s, collect them into a neat spread
    shuffleTimerRef.current = setTimeout(() => {
      const fanned = [];
      const totalCards = Math.min(24, DECK_BACK_COUNT); // Show 24 cards fanned out for picking
      for (let i = 0; i < totalCards; i++) {
        const angle = ((i - totalCards / 2) / totalCards) * 60;
        fanned.push({
          index: i,
          x: Math.sin((angle * Math.PI) / 180) * 320,
          y: -Math.abs(Math.cos((angle * Math.PI) / 180) * 80) + 80,
          rotation: angle * 0.6,
          selected: false,
        });
      }
      setDeckCards(fanned);
      setIsShuffling(false);
      setPhase('draw');
    }, 2000);
  }, []);

  useEffect(() => {
    return () => {
      if (shuffleTimerRef.current) clearTimeout(shuffleTimerRef.current);
    };
  }, []);

  /* ── Handle card selection from the fan ────────────────────── */
  const handleCardPick = (cardIndex) => {
    if (!selectedSpread) return;
    if (drawnCards.length >= selectedSpread.cards) return;
    if (deckCards[cardIndex]?.selected) return;

    // Mark as selected
    setDeckCards(prev =>
      prev.map((c, i) => i === cardIndex ? { ...c, selected: true } : c)
    );

    // Add to drawn cards (will be populated with real data later)
    setDrawnCards(prev => [...prev, { deckIndex: cardIndex, data: null }]);

    // If we've drawn all needed cards, fetch the reading
    if (drawnCards.length + 1 >= selectedSpread.cards) {
      setTimeout(() => fetchReading(), 600);
    }
  };

  /* ── Fetch reading from API ───────────────────────────────── */
  const fetchReading = async () => {
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

      if (!response.ok) throw new Error('Reading failed');
      const data = await response.json();
      applyReadingData(data.data);
    } catch {
      // Fallback to demo data
      applyReadingData(getDemoReading(selectedSpread.id, question));
    }
  };

  const applyReadingData = (data) => {
    setReadingResult(data);
    const cards = data?.reading?.cards || [];
    setDrawnCards(prev =>
      prev.map((d, i) => ({ ...d, data: cards[i] || null }))
    );
    setPhase('reading-complete');
  };

  /* ── Flip a drawn card ────────────────────────────────────── */
  const flipCard = (idx) => {
    setFlippedIndexes(prev => {
      const next = new Set(prev);
      next.add(idx);
      return next;
    });
  };

  /* ── Reset ────────────────────────────────────────────────── */
  const resetAll = () => {
    setPhase('choose-spread');
    setSelectedSpread(null);
    setQuestion('');
    setDeckCards([]);
    setDrawnCards([]);
    setFlippedIndexes(new Set());
    setReadingResult(null);
    setError(null);
  };

  const allFlipped = drawnCards.length > 0 && flippedIndexes.size >= drawnCards.length;

  return (
    <div className="min-h-screen bg-cosmic-radial">
      {/* Decorative Glows */}
      <div className="fixed top-1/4 left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-purple-900/15 rounded-full blur-[150px] pointer-events-none" />
      <div className="fixed bottom-0 right-0 w-[400px] h-[400px] bg-indigo-900/15 rounded-full blur-[100px] pointer-events-none" />

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
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-amber-600 flex items-center justify-center">
                <Shuffle className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
                Draw From Deck
              </span>
            </div>
          </div>
          <Link href="/tarot-reading" className="text-sm text-gray-400 hover:text-amber-300 transition-colors">
            Standard Reading →
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 lg:px-12 py-10 relative z-10">
        {/* Title */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-3">
            Draw Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-300 via-purple-400 to-indigo-300">Cards</span>
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Select a spread, shuffle the deck, and pick your cards one by one — just like a real tarot reading.
            Tap each drawn card to reveal its face.
          </p>
        </div>

        {/* ═══════ PHASE 1: Choose Spread ═══════ */}
        {phase === 'choose-spread' && (
          <div className="space-y-8 animate-fadeIn">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Compass className="w-5 h-5 text-amber-400" />
              Choose Your Spread
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {spreads.map(spread => (
                <button
                  key={spread.id}
                  onClick={() => setSelectedSpread(spread)}
                  className={`p-5 rounded-2xl text-left transition-all group ${
                    selectedSpread?.id === spread.id
                      ? 'bg-purple-500/15 border-2 border-purple-500/50 shadow-lg shadow-purple-500/10'
                      : 'bg-glass-card hover:bg-white/10 border border-white/10 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                      <spread.icon className="w-5 h-5 text-purple-400" />
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
                  placeholder="What should I focus on? What lies ahead for me?"
                  maxLength={500}
                  className="w-full bg-white/5 border border-white/15 rounded-2xl px-5 py-4 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/30 transition-all"
                />
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-400">
                    Spread: <span className="text-purple-300 font-semibold">{selectedSpread.name}</span>
                    <span className="mx-2">·</span>
                    <span className="text-gray-500">{selectedSpread.cards} cards to draw</span>
                  </div>
                  <button
                    onClick={startShuffle}
                    className="px-8 py-3 rounded-2xl font-bold text-sm bg-gradient-to-r from-purple-600 to-amber-600 text-white shadow-xl shadow-purple-600/30 hover:from-purple-500 hover:to-amber-500 hover:-translate-y-0.5 transition-all flex items-center gap-2"
                  >
                    <Shuffle className="w-4 h-4" />
                    Shuffle & Spread Deck
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ═══════ PHASE 2: Shuffling Animation ═══════ */}
        {phase === 'shuffling' && (
          <div className="flex flex-col items-center justify-center min-h-[400px] space-y-8">
            <div className="relative w-[500px] h-[300px]">
              {deckCards.map((card, i) => (
                <div
                  key={i}
                  className="absolute left-1/2 top-1/2 w-[60px] h-[90px] transition-all duration-[1500ms] ease-out"
                  style={{
                    transform: `translate(calc(-50% + ${card.x}px), calc(-50% + ${card.y}px)) rotate(${card.rotation}deg)`,
                    zIndex: i,
                  }}
                >
                  <div className="w-full h-full rounded-lg bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-900 border border-amber-500/30 shadow-lg shadow-purple-500/20 flex items-center justify-center">
                    <Star className="w-4 h-4 text-amber-400/60" />
                  </div>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-3 text-purple-300 font-semibold animate-pulse">
              <Sparkles className="w-5 h-5 text-amber-400 animate-spin" />
              Shuffling the cosmic deck...
            </div>
          </div>
        )}

        {/* ═══════ PHASE 3: Draw Cards from Fanned Deck ═══════ */}
        {phase === 'draw' && (
          <div className="space-y-10">
            {/* Draw instructions */}
            <div className="text-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm font-semibold mb-4">
                <Eye className="w-4 h-4" />
                {drawnCards.length} / {selectedSpread.cards} cards drawn
              </div>
              <p className="text-gray-400 text-sm">
                Focus on your question and click the cards that call to you
              </p>
            </div>

            {/* The fanned deck */}
            <div className="relative flex items-center justify-center" style={{ height: '280px' }}>
              {deckCards.map((card, i) => (
                <button
                  key={i}
                  disabled={card.selected || drawnCards.length >= selectedSpread.cards}
                  onClick={() => handleCardPick(i)}
                  className={`absolute transition-all duration-500 ease-out group ${
                    card.selected ? 'opacity-30 scale-90 pointer-events-none' : 'hover:scale-110 hover:-translate-y-4 cursor-pointer'
                  } ${drawnCards.length >= selectedSpread.cards ? 'pointer-events-none' : ''}`}
                  style={{
                    transform: `translateX(${card.x}px) translateY(${card.y}px) rotate(${card.rotation}deg)`,
                    zIndex: card.selected ? 0 : 10 + i,
                    transformOrigin: 'bottom center',
                  }}
                >
                  <div className="w-[65px] h-[100px] rounded-xl bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-900 border-2 border-amber-500/30 shadow-lg shadow-purple-500/20 flex items-center justify-center group-hover:border-amber-400/60 group-hover:shadow-amber-500/30 transition-all">
                    <div className="w-[50px] h-[78px] rounded-lg border border-amber-500/20 flex items-center justify-center bg-gradient-to-b from-purple-900/50 to-indigo-950/50">
                      <Star className="w-5 h-5 text-amber-400/50 group-hover:text-amber-300 transition-colors" />
                    </div>
                  </div>
                </button>
              ))}
            </div>

            {/* Drawn cards area */}
            {drawnCards.length > 0 && (
              <div className="text-center">
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Your Selected Cards</h3>
                <div className="flex items-center justify-center gap-4 flex-wrap">
                  {drawnCards.map((d, i) => (
                    <div
                      key={i}
                      className="w-[70px] h-[105px] rounded-xl bg-gradient-to-br from-purple-700 to-indigo-800 border-2 border-amber-400/40 shadow-xl shadow-amber-500/20 flex items-center justify-center animate-bounceIn"
                    >
                      <Lock className="w-5 h-5 text-amber-300/70" />
                    </div>
                  ))}
                </div>
                {drawnCards.length >= selectedSpread.cards && (
                  <p className="text-emerald-300 text-sm mt-4 animate-pulse font-semibold">
                    ✨ All cards drawn! Generating your reading...
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* ═══════ PHASE 4: Reading Complete — Flip to Reveal ═══════ */}
        {phase === 'reading-complete' && (
          <div className="space-y-8">
            {/* Controls */}
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <span className="text-emerald-300 font-semibold text-sm">Cards Drawn</span>
                <span className="px-3 py-1 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-300 text-xs font-bold">
                  {selectedSpread?.name}
                </span>
                <span className="text-gray-500 text-xs">
                  Tap each card to reveal
                </span>
              </div>
              <button onClick={resetAll} className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-gray-300 hover:text-white text-sm transition-colors">
                <RotateCcw className="w-4 h-4" />
                New Reading
              </button>
            </div>

            {/* Question */}
            {readingResult?.reading?.question && (
              <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-2xl p-4 flex items-start gap-3">
                <MessageCircle className="w-5 h-5 text-indigo-400 flex-shrink-0 mt-0.5" />
                <div>
                  <span className="text-xs text-gray-400 uppercase font-bold">Your Question</span>
                  <p className="text-indigo-200 text-sm font-medium mt-0.5">{readingResult.reading.question}</p>
                </div>
              </div>
            )}

            {/* Flip Cards Grid */}
            <div className="flex flex-wrap items-center justify-center gap-6">
              {drawnCards.map((drawn, i) => {
                const isFlipped = flippedIndexes.has(i);
                const card = drawn.data;
                const isReversed = card?.orientation === 'reversed';
                const ElIcon = card ? (elementIcons[card.element] || Star) : Star;

                return (
                  <div key={i} className="perspective-1000" style={{ perspective: '1000px' }}>
                    <button
                      onClick={() => flipCard(i)}
                      disabled={isFlipped}
                      className={`relative w-[180px] h-[280px] transition-transform duration-700 cursor-pointer`}
                      style={{
                        transformStyle: 'preserve-3d',
                        transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
                      }}
                    >
                      {/* Card Back */}
                      <div
                        className="absolute inset-0 rounded-2xl bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-900 border-2 border-amber-500/40 shadow-2xl shadow-purple-500/30 flex flex-col items-center justify-center gap-3 hover:border-amber-400/70 hover:shadow-amber-500/30 transition-all"
                        style={{ backfaceVisibility: 'hidden' }}
                      >
                        <div className="w-[140px] h-[220px] rounded-xl border border-amber-500/25 bg-gradient-to-b from-purple-900/60 to-indigo-950/60 flex flex-col items-center justify-center gap-2">
                          <Star className="w-8 h-8 text-amber-400/60" />
                          <span className="text-[10px] text-amber-300/50 font-bold uppercase tracking-widest">MysticAI</span>
                          <span className="text-[9px] text-purple-300/50 mt-1">Tap to Reveal</span>
                        </div>
                        {card?.position && (
                          <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">{card.position}</span>
                        )}
                      </div>

                      {/* Card Front */}
                      <div
                        className={`absolute inset-0 rounded-2xl border-2 shadow-2xl p-4 flex flex-col ${
                          isReversed
                            ? 'bg-gradient-to-br from-red-950 via-rose-900/80 to-red-950 border-red-500/40 shadow-red-500/20'
                            : 'bg-gradient-to-br from-cosmic-800 via-indigo-900/80 to-cosmic-800 border-indigo-500/40 shadow-indigo-500/20'
                        }`}
                        style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
                      >
                        {card && (
                          <>
                            {/* Position */}
                            <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest mb-1">{card.position}</div>

                            {/* Card Name */}
                            <h3 className={`text-sm font-extrabold mb-1 leading-tight ${isReversed ? 'text-red-300' : 'text-white'}`}>
                              {card.card_name}
                              {isReversed && <span className="text-red-400 text-[10px] ml-1">↩</span>}
                            </h3>

                            {/* Meta */}
                            <div className="flex items-center gap-1.5 text-[10px] text-gray-400 mb-2 flex-wrap">
                              {card.arcana && <span className="capitalize">{card.arcana}</span>}
                              {card.suit && <><span>·</span><span className="capitalize">{card.suit}</span></>}
                              {card.element && (
                                <span className="flex items-center gap-0.5">
                                  · <ElIcon className={`w-3 h-3 ${elementColors[card.element] || ''}`} />
                                </span>
                              )}
                            </div>

                            {/* Meaning */}
                            <p className="text-[10px] text-gray-300 leading-relaxed flex-1 overflow-hidden">
                              {card.core_meaning?.substring(0, 120)}{card.core_meaning?.length > 120 ? '...' : ''}
                            </p>

                            {/* Keywords */}
                            {card.keywords?.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-2">
                                {card.keywords.slice(0, 3).map(kw => (
                                  <span key={kw} className={`px-1.5 py-0.5 rounded text-[8px] font-medium border ${
                                    isReversed
                                      ? 'bg-red-500/10 border-red-500/20 text-red-300'
                                      : 'bg-indigo-500/10 border-indigo-500/20 text-indigo-300'
                                  }`}>
                                    {kw}
                                  </span>
                                ))}
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    </button>
                  </div>
                );
              })}
            </div>

            {/* Narrative (shown after all cards flipped) */}
            {allFlipped && readingResult?.reading && (
              <div className="space-y-6 animate-fadeIn">
                {/* Themes & Elemental Balance */}
                <div className="grid md:grid-cols-2 gap-6">
                  {readingResult.reading.themes?.length > 0 && (
                    <div className="bg-glass p-6 rounded-2xl border border-white/10">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2">
                        <Compass className="w-4 h-4 text-amber-400" />
                        Dominant Themes
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {readingResult.reading.themes.map(t => (
                          <span key={t} className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-sm font-semibold capitalize">
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {readingResult.reading.elemental_balance && (
                    <div className="bg-glass p-6 rounded-2xl border border-white/10">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2">
                        <Zap className="w-4 h-4 text-cyan-400" />
                        Elemental Balance
                      </h3>
                      <div className="grid grid-cols-4 gap-3">
                        {Object.entries(readingResult.reading.elemental_balance).map(([element, count]) => {
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
                {readingResult.reading.narrative && (
                  <div className="bg-gradient-to-br from-indigo-950/40 to-cosmic-900 border border-indigo-500/20 p-8 rounded-3xl">
                    <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-amber-400" />
                      Reading Narrative
                    </h2>
                    <div className="space-y-5">
                      <div>
                        <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">Summary</h4>
                        <p className="text-gray-300 text-sm leading-relaxed">{readingResult.reading.narrative.summary}</p>
                      </div>
                      {readingResult.reading.narrative.energy_tone && (
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-gray-400 uppercase">Energy Tone:</span>
                          <span className="px-3 py-1 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm font-semibold capitalize">
                            {readingResult.reading.narrative.energy_tone}
                          </span>
                        </div>
                      )}
                      <div>
                        <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Advice</h4>
                        <p className="text-gray-300 text-sm leading-relaxed">{readingResult.reading.narrative.advice}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Confidence */}
                {readingResult.reading.confidence_score && (
                  <div className="text-center">
                    <span className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl text-emerald-300 text-sm font-bold">
                      ✨ Reading Confidence: {(readingResult.reading.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}


/* ── Demo Reading Fallback ────────────────────────────────── */
function getDemoReading(spreadType, question) {
  const cards = [
    {
      card_name: 'The Tower', card_id: 'major_16', arcana: 'major', suit: null, element: 'Fire',
      zodiac_sign: 'Mars', position: 'Present Situation', orientation: 'upright',
      keywords: ['upheaval', 'revelation', 'breakthrough', 'awakening'],
      core_meaning: 'The Tower signals sudden change and awakening. Structures that no longer serve you are crumbling to make way for authentic rebuilding.',
    },
    {
      card_name: 'Ten of Cups', card_id: 'cups_10', arcana: 'minor', suit: 'cups', element: 'Water',
      zodiac_sign: null, position: 'Immediate Challenge', orientation: 'upright',
      keywords: ['fulfillment', 'harmony', 'family', 'emotional bliss'],
      core_meaning: 'The Ten of Cups heralds emotional fulfillment, deep connections, and the joy of shared love. True happiness awaits.',
    },
    {
      card_name: 'Knight of Swords', card_id: 'swords_12', arcana: 'minor', suit: 'swords', element: 'Air',
      zodiac_sign: null, position: 'Distant Past / Root Cause', orientation: 'reversed',
      keywords: ['impulsive', 'hasty', 'unfocused', 'reckless'],
      core_meaning: 'Reversed Knight of Swords warns against rushing into situations without proper thought. Slow down and strategize.',
    },
    {
      card_name: 'The Empress', card_id: 'major_03', arcana: 'major', suit: null, element: 'Earth',
      zodiac_sign: 'Venus', position: 'Recent Past', orientation: 'upright',
      keywords: ['nurturing', 'abundance', 'creativity', 'beauty'],
      core_meaning: 'The Empress brings growth, abundance, and creative energy. Connect with your nurturing side and embrace beauty.',
    },
    {
      card_name: 'Ace of Wands', card_id: 'wands_01', arcana: 'minor', suit: 'wands', element: 'Fire',
      zodiac_sign: null, position: 'Best Possible Outcome', orientation: 'upright',
      keywords: ['inspiration', 'new venture', 'passion', 'spark'],
      core_meaning: 'The Ace of Wands ignites a new beginning filled with passion, creativity, and bold inspiration. Seize this moment.',
    },
    {
      card_name: 'The Moon', card_id: 'major_18', arcana: 'major', suit: null, element: 'Water',
      zodiac_sign: 'Pisces', position: 'Near Future', orientation: 'upright',
      keywords: ['illusion', 'intuition', 'subconscious', 'mystery'],
      core_meaning: 'The Moon invites you to explore your subconscious. Trust your intuition even when the path seems unclear.',
    },
    {
      card_name: 'Four of Pentacles', card_id: 'pentacles_04', arcana: 'minor', suit: 'pentacles', element: 'Earth',
      zodiac_sign: null, position: 'Your Attitude', orientation: 'reversed',
      keywords: ['release', 'generosity', 'letting go', 'openness'],
      core_meaning: 'Reversed Four of Pentacles encourages letting go of material attachment. Generosity and openness will bring greater rewards.',
    },
    {
      card_name: 'Queen of Cups', card_id: 'cups_13', arcana: 'minor', suit: 'cups', element: 'Water',
      zodiac_sign: null, position: 'External Influences', orientation: 'upright',
      keywords: ['compassion', 'emotional depth', 'intuitive', 'caring'],
      core_meaning: 'The Queen of Cups represents deep emotional intelligence and compassion. A caring influence guides your path.',
    },
    {
      card_name: 'The Star', card_id: 'major_17', arcana: 'major', suit: null, element: 'Air',
      zodiac_sign: 'Aquarius', position: 'Hopes & Fears', orientation: 'upright',
      keywords: ['hope', 'faith', 'renewal', 'serenity'],
      core_meaning: 'The Star brings renewed hope and faith. Trust that the universe is guiding you toward your highest purpose.',
    },
    {
      card_name: 'The World', card_id: 'major_21', arcana: 'major', suit: null, element: 'Earth',
      zodiac_sign: 'Saturn', position: 'Final Outcome', orientation: 'upright',
      keywords: ['completion', 'achievement', 'fulfillment', 'wholeness'],
      core_meaning: 'The World signals completion and achievement of a major life cycle. Wholeness and integration are within reach.',
    },
  ];

  const count = spreads.find(s => s.id === spreadType)?.cards || 3;
  const sliced = cards.slice(0, count);

  // Reassign positions based on spread
  const positionSets = {
    single: ['Present Insight'],
    daily: ["Today's Guiding Energy"],
    three_card: ['Past', 'Present', 'Future'],
    career: ['Current Career Energy', 'Obstacles to Overcome', 'Hidden Talents', 'Recommended Action', 'Career Outcome'],
    relationship: ['Your Energy', "Partner's Energy", 'Foundation', 'Current Challenge', 'Potential'],
    celtic_cross: ['Present Situation', 'Immediate Challenge', 'Distant Past', 'Recent Past', 'Best Outcome', 'Near Future', 'Your Attitude', 'External Influences', 'Hopes & Fears', 'Final Outcome'],
  };

  const positions = positionSets[spreadType] || positionSets.three_card;
  sliced.forEach((c, i) => { c.position = positions[i] || `Position ${i + 1}`; });

  return {
    reading: {
      spread_type: spreadType,
      spread_name: spreads.find(s => s.id === spreadType)?.name || 'Reading',
      question: question || null,
      card_count: sliced.length,
      cards: sliced,
      confidence_score: 0.87,
      themes: ['transformation', 'emotional depth', 'new beginnings', 'intuition'],
      elemental_balance: { Fire: 2, Water: 3, Air: 1, Earth: 3 },
      narrative: {
        summary: `Your ${spreads.find(s => s.id === spreadType)?.name || 'Tarot'} reading reveals a powerful journey of transformation and emotional depth. The cards suggest a period of significant change leading to fulfillment and wholeness.`,
        energy_tone: 'transformative with deep emotional currents',
        advice: 'Embrace the changes unfolding in your life. Trust your intuition during uncertain moments, and remember that endings are doorways to new beginnings. Stay open-hearted and generous — the universe is conspiring in your favor.',
      },
    },
  };
}
