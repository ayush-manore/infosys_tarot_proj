'use client';

import { useEffect } from 'react';
import { X, Sparkles, Star, Flame, Droplets, Wind, Mountain, Eye, RotateCw } from 'lucide-react';
import { getTarotCardImage } from '../utils/tarotImages';

const elementIcons = { Fire: Flame, Water: Droplets, Air: Wind, Earth: Mountain };
const elementColors = {
  Fire: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
  Water: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  Air: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20',
  Earth: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
};

export default function AstrotalkCardModal({ card, onClose }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!card) return null;

  const isReversed = card.orientation === 'reversed';
  const imageUrl = getTarotCardImage(card);
  const ElIcon = card.element ? (elementIcons[card.element] || Star) : Star;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      {/* Click outside backdrop */}
      <div className="absolute inset-0" onClick={onClose} />

      {/* Modal Container */}
      <div className="relative z-10 w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-gradient-to-b from-cosmic-900 via-indigo-950 to-cosmic-950 border-2 border-amber-500/40 rounded-3xl shadow-2xl shadow-purple-950/80 p-6 md:p-8">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 border border-white/20 text-gray-300 hover:text-white flex items-center justify-center transition-all z-20 cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Content Layout */}
        <div className="grid md:grid-cols-2 gap-8 items-center">
          
          {/* Card Image Display */}
          <div className="flex flex-col items-center justify-center">
            <div className="relative group">
              {/* Gold Ornate Glowing Aura */}
              <div className="absolute -inset-2 bg-gradient-to-r from-amber-500/30 via-purple-600/30 to-amber-500/30 rounded-3xl blur-xl opacity-75 group-hover:opacity-100 transition-opacity" />
              
              <div className="relative rounded-2xl overflow-hidden border-2 border-amber-400/60 shadow-2xl bg-black">
                <img
                  src={imageUrl}
                  alt={card.card_name || 'Tarot Card'}
                  className={`w-[240px] md:w-[270px] h-auto object-cover transition-transform duration-500 ${
                    isReversed ? 'rotate-180' : ''
                  }`}
                  onError={(e) => {
                    e.currentTarget.src = '/tarot/card_back.jpg';
                  }}
                />

                {/* Gold Header Tag */}
                <div className="absolute top-2 left-2 right-2 flex justify-between items-center pointer-events-none">
                  {card.position && (
                    <span className="px-2.5 py-1 rounded-full bg-black/70 backdrop-blur-md border border-amber-400/50 text-[10px] font-bold text-amber-300 uppercase tracking-widest">
                      {card.position}
                    </span>
                  )}
                  <span className={`px-2.5 py-1 rounded-full backdrop-blur-md border text-[10px] font-bold uppercase tracking-wider ${
                    isReversed
                      ? 'bg-red-950/80 border-red-500/50 text-red-300'
                      : 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300'
                  }`}>
                    {isReversed ? '↩ Reversed' : '★ Upright'}
                  </span>
                </div>
              </div>
            </div>

            <span className="text-[11px] text-amber-300/70 font-medium mt-3 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Authentic Rider-Waite-Smith Artwork
            </span>
          </div>

          {/* Card Lore & Meanings */}
          <div className="space-y-4">
            <div>
              <div className="text-xs font-bold text-amber-400 uppercase tracking-widest mb-1 flex items-center gap-1.5">
                <Star className="w-3.5 h-3.5" />
                {card.position || 'Card Oracle'}
              </div>
              <h2 className="text-2xl md:text-3xl font-black text-white">
                {card.card_name}
              </h2>
            </div>

            {/* Badges */}
            <div className="flex flex-wrap gap-2 text-xs">
              {card.arcana && (
                <span className="px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300 font-semibold capitalize">
                  {card.arcana} Arcana
                </span>
              )}
              {card.suit && (
                <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 font-semibold capitalize">
                  Suit of {card.suit}
                </span>
              )}
              {card.element && (
                <span className={`px-2.5 py-1 rounded-lg border font-semibold flex items-center gap-1 ${elementColors[card.element] || 'text-gray-300'}`}>
                  <ElIcon className="w-3.5 h-3.5" />
                  {card.element}
                </span>
              )}
              {card.zodiac_sign && (
                <span className="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 font-semibold">
                  ♊ {card.zodiac_sign}
                </span>
              )}
            </div>

            {/* Position Interpretation */}
            {card.position_interpretation && (
              <div className="bg-purple-950/40 border border-purple-500/30 rounded-2xl p-4">
                <h4 className="text-xs font-bold text-purple-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <Eye className="w-3.5 h-3.5 text-amber-400" />
                  Position in Spread
                </h4>
                <p className="text-xs md:text-sm text-gray-200 leading-relaxed">
                  {card.position_interpretation}
                </p>
              </div>
            )}

            {/* Core Meaning */}
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
              <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">
                Core Meaning ({isReversed ? 'Reversed' : 'Upright'})
              </h4>
              <p className="text-xs md:text-sm text-gray-300 leading-relaxed">
                {card.core_meaning || card.upright_meaning || card.description}
              </p>
            </div>

            {/* Keywords */}
            {card.keywords?.length > 0 && (
              <div>
                <h4 className="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">
                  Keywords
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {card.keywords.map((kw) => (
                    <span
                      key={kw}
                      className="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-medium"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Question Insight */}
            {card.question_insight && (
              <div className="bg-indigo-900/30 border border-indigo-500/30 rounded-2xl p-4 text-xs text-indigo-200 leading-relaxed">
                <span className="font-bold text-indigo-300 block mb-1">Direct Answer to Your Question:</span>
                {card.question_insight}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
