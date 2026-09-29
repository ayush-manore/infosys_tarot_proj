'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, FileText, Download, Eye, ChevronDown, BarChart3, Brain, Hand, CreditCard, ArrowLeft, Loader2 } from 'lucide-react';

const API = 'http://localhost:8000/api/v1';

const REPORT_TYPES = [
  { id: 'palm', label: 'Palmistry Report', icon: Hand, color: 'from-purple-500 to-indigo-500', description: 'Comprehensive palm line analysis, hand shape classification, and personality traits.' },
  { id: 'tarot', label: 'Tarot Report', icon: CreditCard, color: 'from-indigo-500 to-blue-500', description: 'Full tarot spread analysis with card interpretations and narrative synthesis.' },
  { id: 'personality', label: 'Personality Report', icon: Brain, color: 'from-amber-500 to-orange-500', description: 'Big Five personality profiling, strengths, weaknesses, and development recommendations.' },
  { id: 'spiritual-guidance', label: 'Spiritual Guidance Report', icon: Sparkles, color: 'from-violet-500 to-fuchsia-500', description: 'Complete spiritual analysis combining all modules with insight scoring.' },
];

export default function ReportsPage() {
  const [token, setToken] = useState(null);
  const [selectedType, setSelectedType] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const t = localStorage.getItem('access_token');
    setToken(t);
  }, []);

  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const generateReport = async (type) => {
    setLoading(true);
    setError(null);
    setSelectedType(type);
    setReport(null);
    try {
      const url = type === 'spiritual-guidance'
        ? `${API}/reports/spiritual-guidance`
        : `${API}/reports/${type}`;
      const res = await fetch(url, { headers });
      const data = await res.json();
      if (data.status === 'success') {
        setReport(data.data);
      } else {
        setError(data.detail || 'Failed to generate report');
      }
    } catch (e) {
      setError('Could not connect to the backend. Generating sample report...');
      setReport(generateSampleReport(type));
    } finally {
      setLoading(false);
    }
  };

  const exportReport = async (format) => {
    if (!selectedType) return;
    const type = selectedType === 'spiritual-guidance' ? 'palm' : selectedType;
    try {
      const res = await fetch(`${API}/reports/export/${format}?report_type=${type}`, { headers });
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedType}_report.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert('Export requires backend connection.');
    }
  };

  return (
    <div className="min-h-screen bg-cosmic-radial flex flex-col">
      {/* Header */}
      <header className="bg-cosmic-950/80 border-b border-white/10 px-6 md:px-8 py-3.5 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <FileText className="w-5 h-5 text-amber-300" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
            Reports & Export
          </span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="text-xs text-gray-300 hover:text-white px-3 py-1.5 bg-white/5 border border-white/10 rounded-xl transition-colors">
            Dashboard
          </Link>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
        {/* Report Type Selection */}
        <div className="mb-10">
          <h1 className="text-3xl font-bold mb-2">Generate Reports</h1>
          <p className="text-gray-400 mb-8">Select a report type to generate a comprehensive analysis document.</p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {REPORT_TYPES.map((type) => {
              const Icon = type.icon;
              const isSelected = selectedType === type.id;
              return (
                <button
                  key={type.id}
                  onClick={() => generateReport(type.id)}
                  disabled={loading}
                  className={`text-left p-6 rounded-2xl border transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${
                    isSelected
                      ? 'border-purple-500/50 bg-purple-500/10 shadow-lg shadow-purple-500/10'
                      : 'border-white/10 bg-white/[0.03] hover:border-purple-500/30'
                  } ${loading ? 'opacity-60 cursor-wait' : ''}`}
                >
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${type.color} flex items-center justify-center mb-4 ${isSelected ? 'scale-110' : ''} transition-transform`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-sm font-bold text-white mb-1">{type.label}</h3>
                  <p className="text-xs text-gray-400 leading-relaxed">{type.description}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="flex items-center gap-3 text-purple-400">
              <Loader2 className="w-6 h-6 animate-spin" />
              <span className="font-medium">Generating {selectedType} report...</span>
            </div>
          </div>
        )}

        {/* Error */}
        {error && !report && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-300 text-sm">{error}</div>
        )}

        {/* Report Display */}
        {report && !loading && (
          <div className="space-y-6">
            {/* Report Header */}
            <div className="bg-glass-card p-8 rounded-2xl">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">{report.title}</h2>
                  <p className="text-sm text-purple-300">{report.subtitle}</p>
                  <div className="flex items-center gap-4 mt-3">
                    <span className="text-xs text-gray-400">Generated: {new Date(report.generated_at).toLocaleString()}</span>
                    {(report.confidence_score || report.insight_score) && (
                      <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-300 text-xs rounded-full border border-emerald-500/20">
                        Confidence: {((report.confidence_score || report.insight_score) * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => exportReport('csv')} className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 rounded-xl transition-colors">
                    <Download className="w-3.5 h-3.5" /> CSV
                  </button>
                  <button onClick={() => exportReport('json')} className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-colors">
                    <Download className="w-3.5 h-3.5" /> JSON
                  </button>
                </div>
              </div>
            </div>

            {/* Report Sections */}
            {report.sections?.map((section, idx) => (
              <div key={idx} className="bg-glass-card p-6 rounded-2xl">
                <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                  <span className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-300 text-xs font-bold flex items-center justify-center">{idx + 1}</span>
                  {section.title}
                </h3>
                <p className="text-gray-300 text-sm leading-relaxed mb-4">{section.narrative}</p>

                {/* Render content data */}
                {section.content && typeof section.content === 'object' && (
                  <div className="bg-white/[0.03] rounded-xl p-4 border border-white/5">
                    {/* Traits list */}
                    {section.content.traits && Array.isArray(section.content.traits) && (
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {section.content.traits.map((trait, i) => (
                          <div key={i} className="bg-white/[0.03] rounded-lg p-3 border border-white/5">
                            {typeof trait === 'string' ? (
                              <span className="text-xs text-purple-300">{trait}</span>
                            ) : (
                              <>
                                <div className="text-xs font-semibold text-white mb-1">{trait.trait || trait.name}</div>
                                <div className="flex items-center gap-2">
                                  <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full" style={{ width: `${trait.score || 0}%` }} />
                                  </div>
                                  <span className="text-xs text-gray-400">{trait.score || 0}%</span>
                                </div>
                              </>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Cards */}
                    {section.content.cards && Array.isArray(section.content.cards) && (
                      <div className="space-y-3">
                        {section.content.cards.map((card, i) => (
                          <div key={i} className="bg-white/[0.03] rounded-lg p-3 border border-white/5 flex items-start gap-3">
                            <span className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-300 text-xs font-bold flex items-center justify-center shrink-0">{i + 1}</span>
                            <div>
                              <div className="text-sm font-semibold text-white">{card.card_name} <span className="text-xs text-gray-400">({card.orientation})</span></div>
                              <div className="text-xs text-purple-300 mb-1">{card.position}</div>
                              <div className="text-xs text-gray-400">{card.core_meaning}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Lines */}
                    {section.content.lines && Array.isArray(section.content.lines) && (
                      <div className="space-y-2">
                        {section.content.lines.map((line, i) => (
                          <div key={i} className="flex items-center gap-3 bg-white/[0.03] p-2 rounded-lg border border-white/5">
                            <span className={`w-2 h-2 rounded-full ${line.detected ? 'bg-emerald-400' : 'bg-red-400'}`} />
                            <span className="text-xs font-medium text-white">{line.name}</span>
                            {line.measurements && (
                              <span className="text-xs text-gray-400">
                                {line.measurements.depth} · {line.measurements.clarity} · {line.measurements.length_mm}mm
                              </span>
                            )}
                            <span className="text-xs text-gray-500 ml-auto">{(line.confidence * 100).toFixed(1)}%</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Strengths */}
                    {section.content.strengths && Array.isArray(section.content.strengths) && (
                      <div className="space-y-3">
                        {section.content.strengths.map((s, i) => (
                          <div key={i} className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-3">
                            <div className="text-sm font-bold text-emerald-300 mb-1">💪 {s.strength || s.trait}</div>
                            <div className="text-xs text-gray-300">{s.description}</div>
                            {s.advice && <div className="text-xs text-emerald-400 mt-2 italic">→ {s.advice}</div>}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Growth Areas */}
                    {section.content.growth_areas && Array.isArray(section.content.growth_areas) && (
                      <div className="space-y-3">
                        {section.content.growth_areas.map((w, i) => (
                          <div key={i} className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-3">
                            <div className="text-sm font-bold text-amber-300 mb-1">🌱 {w.area || w.trait}</div>
                            <div className="text-xs text-gray-300">{w.description}</div>
                            {w.growth_path && <div className="text-xs text-amber-400 mt-2 italic">→ {w.growth_path}</div>}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Recommendations */}
                    {section.content.recommendations && Array.isArray(section.content.recommendations) && (
                      <div className="space-y-2">
                        {section.content.recommendations.slice(0, 5).map((r, i) => (
                          <div key={i} className="bg-white/[0.03] border border-white/5 rounded-lg p-3">
                            <div className="text-sm font-semibold text-white mb-1">{r.title}</div>
                            <div className="text-xs text-gray-400">{r.description}</div>
                            {r.priority && (
                              <span className={`inline-block mt-2 text-[10px] px-2 py-0.5 rounded-full ${
                                r.priority === 'high' ? 'bg-red-500/10 text-red-300 border border-red-500/20' :
                                r.priority === 'medium' ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20' :
                                'bg-gray-500/10 text-gray-300 border border-gray-500/20'
                              }`}>{r.priority} priority</span>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Simple key-value display for other content */}
                    {!section.content.traits && !section.content.cards && !section.content.lines && !section.content.strengths && !section.content.growth_areas && !section.content.recommendations && (
                      <div className="space-y-1">
                        {Object.entries(section.content).map(([key, value]) => {
                          if (typeof value === 'object') return null;
                          return (
                            <div key={key} className="flex justify-between text-xs">
                              <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
                              <span className="text-white font-medium">{String(value)}</span>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

function generateSampleReport(type) {
  return {
    report_type: type,
    title: `Sample ${type.charAt(0).toUpperCase() + type.slice(1)} Report`,
    subtitle: 'Demo Mode — Connect backend for live data',
    confidence_score: 0.847,
    generated_at: new Date().toISOString(),
    sections: [
      {
        title: 'Overview',
        narrative: 'This is a sample report generated in demo mode. Connect the FastAPI backend to generate real AI-powered analysis reports with full interpretation data.',
        content: { report_type: type, mode: 'demo', status: 'sample' },
      },
      {
        title: 'Key Findings',
        narrative: 'When connected to the backend, this section will display detailed findings from your palm analysis, tarot reading, or personality profiling engine.',
        content: { finding_1: 'Strong intuitive awareness', finding_2: 'Career momentum building', finding_3: 'Emotional intelligence peak' },
      },
    ],
  };
}
