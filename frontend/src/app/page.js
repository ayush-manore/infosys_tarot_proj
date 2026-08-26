'use client';

import Link from 'next/link';
import { Sparkles, Hand, CreditCard, Brain, Compass, ArrowRight, ShieldCheck, Star } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="bg-cosmic-radial min-h-screen flex flex-col justify-between relative overflow-hidden">
      {/* Background Decorative Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-3/4 left-1/4 w-[400px] h-[400px] bg-indigo-900/20 rounded-full blur-[100px] pointer-events-none" />

      {/* Navigation Header */}
      <header className="sticky top-0 z-50 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 lg:px-12 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <Sparkles className="w-5 h-5 text-amber-300" />
          </div>
          <span className="text-2xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-purple-300 to-indigo-200">
            MysticAI
          </span>
        </div>

        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-300">
          <Link href="#features" className="hover:text-amber-300 transition-colors">Features</Link>
          <Link href="#workflows" className="hover:text-amber-300 transition-colors">How It Works</Link>
          <Link href="#about" className="hover:text-amber-300 transition-colors">About Platform</Link>
        </nav>

        <div className="flex items-center gap-4">
          <Link
            href="/auth/login"
            className="px-4 py-2 text-sm font-medium text-gray-200 hover:text-white transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/auth/register"
            className="px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 rounded-xl shadow-lg shadow-purple-900/40 transition-all transform hover:-translate-y-0.5"
          >
            Get Started
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="px-6 lg:px-12 pt-16 pb-20 max-w-7xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-purple-500/30 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-8 backdrop-blur-sm">
            <Sparkles className="w-4 h-4 text-amber-400" />
            AI-Powered Spiritual Intelligence Platform
          </div>

          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-tight mb-8">
            Unveil Your Destined Path with <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-purple-400 to-indigo-300 text-glow">
              Palmistry & Tarot Intelligence
            </span>
          </h1>

          <p className="max-w-3xl mx-auto text-lg md:text-xl text-gray-300 mb-10 leading-relaxed font-light">
            Combining state-of-the-art Computer Vision, MediaPipe hand landmark detection,
            and specialized AI interpretations to generate deep, personalized guidance on career,
            relationships, and life trends.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link
              href="/auth/register"
              className="w-full sm:w-auto px-8 py-4 text-base font-bold text-white bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-700 hover:from-purple-500 hover:to-indigo-500 rounded-2xl shadow-xl shadow-purple-600/30 transition-all flex items-center justify-center gap-3 transform hover:-translate-y-1"
            >
              Start Free Reading
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/auth/login"
              className="w-full sm:w-auto px-8 py-4 text-base font-semibold text-gray-200 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl backdrop-blur-md transition-all flex items-center justify-center"
            >
              View Sample Insights
            </Link>
          </div>

          {/* Key Metrics / Highlights */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto pt-8 border-t border-white/10">
            <div className="p-4">
              <div className="text-3xl font-extrabold text-amber-300">5 Lines</div>
              <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">Palm Detection</div>
            </div>
            <div className="p-4">
              <div className="text-3xl font-extrabold text-purple-400">6 Spreads</div>
              <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">Tarot Engine</div>
            </div>
            <div className="p-4">
              <div className="text-3xl font-extrabold text-indigo-400">95%</div>
              <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">Confidence Metric</div>
            </div>
            <div className="p-4">
              <div className="text-3xl font-extrabold text-emerald-400">RBAC</div>
              <div className="text-xs text-gray-400 mt-1 uppercase tracking-wider">4 System Roles</div>
            </div>
          </div>
        </section>

        {/* Feature Modules */}
        <section id="features" className="px-6 lg:px-12 py-20 max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">Core Platform Modules</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Integrated multi-modal spiritual analysis combining computer vision and natural language understanding.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Palm Analysis Engine */}
            <div className="bg-glass-card p-8 rounded-3xl hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/10 group">
              <div className="w-14 h-14 rounded-2xl bg-purple-950/80 border border-purple-500/30 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Hand className="w-7 h-7 text-purple-400" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Palm Analysis Engine</h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-6">
                Computer vision feature extraction analyzing Life Line, Head Line, Heart Line, Fate Line, and Sun Line using OpenCV & MediaPipe.
              </p>
              <ul className="space-y-2 text-xs text-purple-300 font-medium">
                <li className="flex items-center gap-2">✓ Hand landmark segmentation</li>
                <li className="flex items-center gap-2">✓ Palm shape & finger structure</li>
                <li className="flex items-center gap-2">✓ Automated pattern recognition</li>
              </ul>
            </div>

            {/* Tarot Reading Engine */}
            <div className="bg-glass-card p-8 rounded-3xl hover:border-indigo-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-indigo-500/10 group">
              <div className="w-14 h-14 rounded-2xl bg-indigo-950/80 border border-indigo-500/30 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <CreditCard className="w-7 h-7 text-indigo-400" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Tarot Reading Engine</h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-6">
                Interactive card shuffling simulation supporting Single Card, Three Card, Celtic Cross, Career, and Relationship spreads.
              </p>
              <ul className="space-y-2 text-xs text-indigo-300 font-medium">
                <li className="flex items-center gap-2">✓ 78 Major & Minor Arcana deck</li>
                <li className="flex items-center gap-2">✓ Position-specific interpretations</li>
                <li className="flex items-center gap-2">✓ Contextual question mapping</li>
              </ul>
            </div>

            {/* AI Interpretation & Insights */}
            <div className="bg-glass-card p-8 rounded-3xl hover:border-amber-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-500/10 group">
              <div className="w-14 h-14 rounded-2xl bg-amber-950/80 border border-amber-500/30 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Brain className="w-7 h-7 text-amber-400" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">AI Interpretation Engine</h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-6">
                Synthesis engine generating personality profiles, relationship guidance, career trends, and weighted confidence scoring.
              </p>
              <ul className="space-y-2 text-xs text-amber-300 font-medium">
                <li className="flex items-center gap-2">✓ 5-factor weighted scoring model</li>
                <li className="flex items-center gap-2">✓ Life trend analysis & monitoring</li>
                <li className="flex items-center gap-2">✓ Exportable PDF/Excel reports</li>
              </ul>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 px-6 lg:px-12 bg-cosmic-950/90 text-center text-xs text-gray-400">
        <p>© 2026 MysticAI — Palmistry & Tarot Intelligence Platform. Internship Project — Week 1 Milestone Completed.</p>
      </footer>
    </div>
  );
}
