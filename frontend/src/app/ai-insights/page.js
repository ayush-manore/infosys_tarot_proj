'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { Sparkles, Brain, TrendingUp, Target, Heart, Briefcase, Leaf, Star, Zap, Eye, RefreshCw, ArrowRight, ChevronDown, ChevronUp, BookOpen, Moon, Compass, Award, Activity, Shield, Bot, Hand, CreditCard, BarChart3, Clock, CheckCircle, AlertCircle, Lightbulb, Flame, ChevronRight } from 'lucide-react';

const API = 'http://localhost:8000/api/v1';
function authHeader() {
  if (typeof window === 'undefined') return {};
  const t = localStorage.getItem('access_token');
  return t ? { Authorization: `Bearer ${t}` } : {};
}

const CATEGORY_META = {
  personal_growth: { label: 'Personal Growth', icon: Leaf, color: 'emerald', grad: 'from-emerald-500 to-teal-500' },
  relationship_guidance: { label: 'Relationships', icon: Heart, color: 'rose', grad: 'from-rose-500 to-pink-500' },
  career_suggestions: { label: 'Career', icon: Briefcase, color: 'amber', grad: 'from-amber-500 to-orange-500' },
  goal_alignment: { label: 'Goal Alignment', icon: Target, color: 'blue', grad: 'from-blue-500 to-indigo-500' },
  spiritual_development: { label: 'Spiritual', icon: Sparkles, color: 'purple', grad: 'from-purple-500 to-violet-500' },
};

const INSIGHT_META = {
  personality: { label: 'Personality', icon: Brain, color: 'violet' },
  relationships: { label: 'Relationships', icon: Heart, color: 'rose' },
  career: { label: 'Career', icon: Briefcase, color: 'amber' },
  health_wellness: { label: 'Health & Wellness', icon: Activity, color: 'emerald' },
  personal_growth: { label: 'Personal Growth', icon: Leaf, color: 'teal' },
  spiritual: { label: 'Spiritual', icon: Sparkles, color: 'purple' },
};

const TC = { violet:'text-violet-300', rose:'text-rose-300', amber:'text-amber-300', emerald:'text-emerald-300', teal:'text-teal-300', purple:'text-purple-300', blue:'text-blue-300' };
const BC = { violet:'border-violet-500/30 bg-violet-950/20', rose:'border-rose-500/30 bg-rose-950/20', amber:'border-amber-500/30 bg-amber-950/20', emerald:'border-emerald-500/30 bg-emerald-950/20', teal:'border-teal-500/30 bg-teal-950/20', purple:'border-purple-500/30 bg-purple-950/20' };
const BARS = ['from-violet-500 to-purple-500','from-blue-500 to-indigo-500','from-emerald-500 to-teal-500','from-amber-500 to-orange-500','from-rose-500 to-pink-500'];

function CircleScore({ value, label, color='purple', size=80 }) {
  const norm = value > 1 ? value : value * 100;
  const r = 28, circ = 2*Math.PI*r, dash = circ*(norm/100);
  const cs = { purple:'#a855f7', amber:'#f59e0b', emerald:'#10b981', rose:'#f43f5e', blue:'#3b82f6', teal:'#14b8a6' };
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox="0 0 64 64">
        <circle cx="32" cy="32" r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="5"/>
        <circle cx="32" cy="32" r={r} fill="none" stroke={cs[color]||cs.purple} strokeWidth="5"
          strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" transform="rotate(-90 32 32)"
          style={{{transition:'stroke-dasharray 1s ease'}}}/>
        <text x="32" y="36" textAnchor="middle" fontSize="13" fontWeight="800" fill="white">{Math.round(norm)}%</text>
      </svg>
      {label && <span className="text-xs text-gray-400 text-center leading-tight max-w-[72px]">{label}</span>}
    </div>
  );
}

function RecCard({ rec }) {
  const [exp, setExp] = useState(false);
  const cat = CATEGORY_META[rec.category] || CATEGORY_META.personal_growth;
  const Icon = cat.icon;
  const imp = rec.impact || rec.priority || 'medium';
  const ic = imp==='high'?'text-emerald-400 bg-emerald-500/10 border-emerald-500/20':imp==='medium'?'text-amber-400 bg-amber-500/10 border-amber-500/20':'text-blue-400 bg-blue-500/10 border-blue-500/20';
  return (
    <div className="bg-glass rounded-2xl border border-white/10 hover:border-white/20 transition-all overflow-hidden">
      <div className="p-5 cursor-pointer flex items-start gap-4" onClick={()=>setExp(!exp)}>
        <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${cat.grad} flex items-center justify-center flex-shrink-0 shadow-lg`}>
          <Icon className="w-5 h-5 text-white"/>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h4 className="text-white font-bold text-sm">{rec.title}</h4>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase ${ic}`}>{imp}</span>
              {exp?<ChevronUp className="w-4 h-4 text-gray-500"/>:<ChevronDown className="w-4 h-4 text-gray-500"/>}
            </div>
          </div>
          <p className="text-gray-400 text-xs mt-1 line-clamp-2">{rec.description}</p>
          {rec.duration&&<span className="text-xs text-gray-500 mt-1 inline-flex items-center gap-1"><Clock className="w-3 h-3"/> {rec.duration}</span>}
        </div>
      </div>
      {exp&&(
        <div className="px-5 pb-5 border-t border-white/5 pt-4">
          <p className="text-gray-300 text-sm leading-relaxed">{rec.description}</p>
          {rec.action&&<div className="mt-3 flex items-start gap-2 bg-white/5 rounded-xl p-3"><CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0"/><span className="text-sm text-emerald-300">{rec.action}</span></div>}
          {rec.source_trait&&<div className="mt-2 flex gap-2"><span className="text-[11px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">Trait: {rec.source_trait}</span></div>}
        </div>
      )}
    </div>
  );
}

function TrendBar({ trend }) {
  const dc = { ascending:'text-emerald-400 bg-emerald-500/10', stable:'text-blue-400 bg-blue-500/10', transitioning:'text-amber-400 bg-amber-500/10', resting:'text-rose-400 bg-rose-500/10' };
  const dl = { ascending:'Ascending â†‘', stable:'Stable â†’', transitioning:'Shifting â†—', resting:'Resting â†“' };
  return (
    <div className="bg-glass rounded-2xl border border-white/10 p-5">
      <div className="flex items-center justify-between mb-3">
        <div><h4 className="text-white font-bold text-sm">{trend.name}</h4><p className="text-gray-500 text-xs mt-0.5 line-clamp-1">{trend.description}</p></div>
        <span className={`text-xs font-bold px-2.5 py-1 rounded-full ml-2 flex-shrink-0 ${dc[trend.direction]||dc.stable}`}>{dl[trend.direction]||'Stable â†’'}</span>
      </div>
      <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden mb-2">
        <div className="h-full rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-1000" style={{{width:`${trend.score}}%`}}/>
      </div>
      <div className="flex justify-between text-xs text-gray-500"><span>{trend.momentum} momentum</span><span>{trend.score}%</span></div>
    </div>
  );
}

function LoadBox({ icon: Ic, color, text }) {
  return (
    <div className="bg-glass rounded-2xl border border-white/10 p-12 text-center">
      <Ic className={`w-10 h-10 text-${color}-400 animate-spin mx-auto mb-4`}/>
      <p className="text-gray-300 font-semibold">{text}</p>
    </div>
  );
}

function ErrBox({ msg, retry }) {
  return (
    <div className="bg-rose-950/30 border border-rose-500/30 rounded-2xl p-6 text-center">
      <AlertCircle className="w-8 h-8 text-rose-400 mx-auto mb-3"/>
      <p className="text-rose-300 font-semibold">{msg}</p>
      <p className="text-gray-400 text-sm mt-1">Ensure FastAPI backend is running on port 8000 and you are logged in.</p>
      <button onClick={retry} className="mt-4 px-4 py-2 bg-rose-600/20 border border-rose-500/30 text-rose-300 rounded-xl text-sm font-semibold hover:bg-rose-600/30 transition-all">Retry</button>
    </div>
  );
}

export default function AIInsightsPage() {
  const [tab, setTab] = useState('recommendations');
  const [recs, setRecs] = useState(null);
  const [interp, setInterp] = useState(null);
  const [trends, setTrends] = useState(null);
  const [persona, setPersona] = useState(null);
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});
  const [recCat, setRecCat] = useState('all');

  async function fetchData(key, url, method='GET', body=null) {
    setLoading(l=>({...l,[key]:true}));
    setErrors(e=>({...e,[key]:null}));
    try {
      const opts = { method, headers:{...authHeader(),'Content-Type':'application/json'} };
      if (body) opts.body = JSON.stringify(body);
      const res = await fetch(url, opts);
      const d = await res.json();
      if (d.status === 'success') return d.data;
      throw new Error(d.message || 'Failed');
    } catch(err) {
      setErrors(e=>({...e,[key]:err.message||'Backend not reachable. Ensure FastAPI is running on port 8000.'}));
      return null;
    } finally {
      setLoading(l=>({...l,[key]:false}));
    }
  }

  const loadRecs = useCallback(async()=>{ const d=await fetchData('recs',`${API}/ai/recommendations`); if(d) setRecs(d); },[]);
  const loadInterp = useCallback(async()=>{ const d=await fetchData('interp',`${API}/ai/interpret`,'POST',{reading_type:'combined'}); if(d) setInterp(d); },[]);
  const loadTrends = useCallback(async()=>{ const d=await fetchData('trends',`${API}/ai/trends`,'POST',{}); if(d) setTrends(d); },[]);
  const loadPersona = useCallback(async()=>{ const d=await fetchData('persona',`${API}/ai/personality`,'POST',{include_tarot:true}); if(d) setPersona(d); },[]);

  useEffect(()=>{
    if(tab==='recommendations'&&!recs) loadRecs();
    if(tab==='interpretation'&&!interp) loadInterp();
    if(tab==='trends'&&!trends) loadTrends();
    if(tab==='personality'&&!persona) loadPersona();
  },[tab]);

  const TABS = [
    {id:'recommendations',label:'AI Recommendations',icon:Target},
    {id:'interpretation',label:'AI Interpretation',icon:Sparkles},
    {id:'trends',label:'Life Trends',icon:TrendingUp},
    {id:'personality',label:'Personality Intel',icon:Brain},
  ];

  const allRecs = recs?.ai_recommendations||recs;
  const recMap = allRecs ? {
    all:[...(allRecs.personal_growth||[]),...(allRecs.relationship_guidance||[]),...(allRecs.career_suggestions||[]),...(allRecs.goal_alignment||[]),...(allRecs.spiritual_development||[])],
    personal_growth:allRecs.personal_growth||[], relationship_guidance:allRecs.relationship_guidance||[],
    career_suggestions:allRecs.career_suggestions||[], goal_alignment:allRecs.goal_alignment||[], spiritual_development:allRecs.spiritual_development||[],
  } : null;
  const shownRecs = recMap?(recMap[recCat]||recMap.all):[];
  const topRecs = allRecs?.top_recommendations||[];

  return (
    <div className="min-h-screen bg-cosmic-radial">
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-purple-900/15 rounded-full blur-[120px] pointer-events-none"/>
      <div className="fixed bottom-0 right-0 w-[400px] h-[400px] bg-indigo-900/10 rounded-full blur-[100px] pointer-events-none"/>
      <header className="sticky top-0 z-40 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-1.5 text-gray-400 hover:text-white text-sm transition-colors">
            <ChevronRight className="w-4 h-4 rotate-180"/> Dashboard
          </Link>
          <span className="text-gray-600">/</span>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-amber-300"/>
            </div>
            <span className="text-white font-bold text-sm">AI Insights Engine</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/chat" className="flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Bot className="w-3.5 h-3.5 text-emerald-300"/> Ask AI
          </Link>
          <Link href="/palm-reading" className="hidden sm:flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-white/5 border border-white/10 px-3 py-1.5 rounded-xl transition-colors">
            <Hand className="w-3.5 h-3.5 text-purple-300"/> Palm Reading
          </Link>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 md:px-6 py-8 space-y-8">
        <div className="relative bg-gradient-to-br from-purple-950/60 via-indigo-950/40 to-cosmic-900 border border-purple-500/20 rounded-3xl p-6 md:p-8 overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-purple-600/10 rounded-full blur-[80px] pointer-events-none"/>
          <div className="relative z-10 flex flex-col md:flex-row md:items-center gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/30"><Sparkles className="w-5 h-5 text-amber-300"/></div>
                <span className="text-[11px] font-bold text-purple-400 uppercase tracking-widest">Gemini-Powered</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-extrabold text-white leading-tight mb-2">AI Interpretation & Recommendations</h1>
              <p className="text-gray-400 text-sm leading-relaxed max-w-2xl">Your personalized spiritual intelligence report combining palm feature analysis, tarot card interpretations, personality profiling, and life trend forecasting into actionable guidance.</p>
              <div className="flex flex-wrap gap-2 mt-4">
                {['Palm Analysis','Tarot Synthesis','Personality Mapping','Life Trends','Growth Recommendations'].map(tag=>(
                  <span key={tag} className="px-2.5 py-1 rounded-lg bg-white/5 text-purple-300 text-xs border border-purple-500/20 font-medium">âœ¦ {tag}</span>
                ))}
              </div>
            </div>
            <div className="hidden md:flex gap-4 flex-shrink-0">
              {[{label:'Insight Score',value:82,color:'purple'},{label:'Palm Confidence',value:78,color:'blue'},{label:'Tarot Relevance',value:75,color:'amber'},{label:'Growth Potential',value:88,color:'emerald'}].map(s=>(
                <CircleScore key={s.label} value={s.value} label={s.label} color={s.color}/>
              ))}
            </div>
          </div>
        </div>

        <div className="flex gap-2 overflow-x-auto pb-1">
          {TABS.map(t=>(
            <button key={t.id} onClick={()=>setTab(t.id)} id={`tab-${t.id}`}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold whitespace-nowrap transition-all ${tab===t.id?'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30':'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white border border-white/10'}`}>
              <t.icon className="w-4 h-4"/>{t.label}
            </button>
          ))}
        </div>

        {tab==='recommendations'&&(
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div><h2 className="text-xl font-bold text-white">Personalized Recommendations</h2><p className="text-sm text-gray-400 mt-0.5">AI-generated guidance based on your palm traits, tarot readings & spiritual profile</p></div>
              <button id="btn-refresh-recs" onClick={loadRecs} disabled={loading.recs} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600/20 border border-purple-500/30 text-purple-300 text-sm font-semibold hover:bg-purple-600/30 transition-all disabled:opacity-50">
                <RefreshCw className={`w-4 h-4 ${loading.recs?'animate-spin':''}`}/>{loading.recs?'Generating...':'Refresh'}
              </button>
            </div>
            {loading.recs&&<LoadBox icon={Sparkles} color="purple" text="Gemini AI is generating your personalized recommendations..."/>}
            {!loading.recs&&errors.recs&&<ErrBox msg={errors.recs} retry={loadRecs}/>}
            {!loading.recs&&!errors.recs&&recMap&&(
              <>
                {topRecs.length>0&&(
                  <div className="bg-gradient-to-br from-amber-950/40 to-cosmic-900 border border-amber-500/20 rounded-2xl p-6">
                    <div className="flex items-center gap-2 mb-4"><Award className="w-5 h-5 text-amber-400"/><h3 className="text-white font-bold">Top Priority Recommendations</h3></div>
                    <div className="space-y-3">
                      {topRecs.slice(0,3).map((rec,i)=>(
                        <div key={i} className="flex items-start gap-3 bg-white/5 rounded-xl p-4">
                          <span className="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold flex items-center justify-center flex-shrink-0 border border-amber-500/30">{rec.rank||i+1}</span>
                          <div className="flex-1"><h4 className="text-white font-semibold text-sm">{rec.title}</h4><p className="text-gray-400 text-xs mt-1">{(rec.description||'').slice(0,120)}{(rec.description||'').length>120?'...':''}</p></div>
                          {rec.priority_score&&<span className="flex-shrink-0 text-xs font-bold text-amber-300 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">Score: {rec.priority_score}</span>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                <div className="flex gap-2 flex-wrap">
                  {['all',...Object.keys(CATEGORY_META)].map(cat=>{
                    const m=CATEGORY_META[cat];
                    const cnt=cat==='all'?recMap.all.length:(recMap[cat]?.length||0);
                    return(
                      <button key={cat} onClick={()=>setRecCat(cat)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border ${recCat===cat?'bg-purple-600 border-purple-500 text-white':'bg-white/5 border-white/10 text-gray-400 hover:text-white hover:bg-white/10'}`}>
                        {m&&<m.icon className="w-3.5 h-3.5"/>}{m?m.label:'All'} <span className="opacity-60 text-[10px]">({cnt})</span>
                      </button>
                    );
                  })}
                </div>
                {shownRecs.length===0?(
                  <div className="bg-glass rounded-2xl border border-white/10 p-8 text-center"><Star className="w-8 h-8 text-amber-400 mx-auto mb-3"/><p className="text-gray-300 font-semibold">No recommendations in this category yet</p></div>
                ):(
                  <div className="grid md:grid-cols-2 gap-4">{shownRecs.map((rec,i)=><RecCard key={i} rec={rec}/>)}</div>
                )}
                {allRecs?.generated_at&&<p className="text-xs text-gray-600 text-center">Generated: {new Date(allRecs.generated_at).toLocaleString()} Â· {allRecs.total_recommendations||shownRecs.length} total Â· Gemini 2.0 Flash</p>}
              </>
            )}
            {!loading.recs&&!errors.recs&&!recMap&&(
              <div className="bg-glass rounded-2xl border border-white/10 p-12 text-center">
                <Target className="w-12 h-12 text-purple-400 mx-auto mb-4 opacity-50"/>
                <h3 className="text-white font-bold text-lg mb-2">No Recommendations Yet</h3>
                <p className="text-gray-400 text-sm mb-6">Generate AI-powered personalized recommendations based on your spiritual profile</p>
                <button id="btn-gen-recs" onClick={loadRecs} className="px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl transition-all">Generate Recommendations</button>
              </div>
            )}
          </div>
        )}

        {tab==='interpretation'&&(
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div><h2 className="text-xl font-bold text-white">AI Reading Interpretation</h2><p className="text-sm text-gray-400 mt-0.5">Deep narrative synthesis of your palm & tarot readings</p></div>
              <button id="btn-refresh-interp" onClick={loadInterp} disabled={loading.interp} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-300 text-sm font-semibold hover:bg-indigo-600/30 transition-all disabled:opacity-50">
                <RefreshCw className={`w-4 h-4 ${loading.interp?'animate-spin':''}`}/>{loading.interp?'Interpreting...':'New Reading'}
              </button>
            </div>
            {loading.interp&&<LoadBox icon={Sparkles} color="indigo" text="Gemini AI is interpreting your combined reading..."/>}
            {!loading.interp&&errors.interp&&<ErrBox msg={errors.interp} retry={loadInterp}/>}
            {!loading.interp&&!errors.interp&&interp&&(()=>{
              const data=interp.ai_interpretation||interp;
              const insights=data?.insights||{};
              return(
                <div className="space-y-6">
                  {data?.energy_summary&&(
                    <div className="bg-gradient-to-br from-indigo-950/50 to-cosmic-900 border border-indigo-500/20 rounded-2xl p-6">
                      <div className="flex items-center gap-2 mb-3"><Sparkles className="w-5 h-5 text-indigo-400"/><h3 className="text-white font-bold">Energy Summary</h3></div>
                      <p className="text-indigo-200 text-lg font-medium italic">"{data.energy_summary}"</p>
                    </div>
                  )}
                  {data?.overall_narrative&&(
                    <div className="bg-glass border border-white/10 rounded-2xl p-6">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2"><BookOpen className="w-5 h-5 text-purple-400"/> Overall Reading Narrative</h3>
                      <p className="text-gray-300 leading-relaxed text-sm">{data.overall_narrative}</p>
                    </div>
                  )}
                  {Object.keys(insights).length>0&&(
                    <div>
                      <h3 className="text-white font-bold mb-4">Life Domain Insights</h3>
                      <div className="grid md:grid-cols-2 gap-4">
                        {Object.entries(insights).map(([cat,d])=>{
                          const m=INSIGHT_META[cat]||INSIGHT_META.personal_growth;
                          const Icon=m.icon;
                          return(
                            <div key={cat} className={`rounded-2xl border p-5 ${BC[m.color]||BC.purple}`}>
                              <div className="flex items-center gap-3 mb-3">
                                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center"><Icon className={`w-4 h-4 ${TC[m.color]}`}/></div>
                                <span className="font-bold text-white text-sm">{m.label}</span>
                                {d.score!==undefined&&<span className={`ml-auto font-bold text-sm ${TC[m.color]}`}>{Math.round(d.score)}%</span>}
                              </div>
                              {d.narrative&&<p className="text-gray-300 text-sm leading-relaxed mb-2">{d.narrative}</p>}
                              {d.advice&&<div className="flex items-start gap-2 mt-2 bg-white/5 rounded-xl p-3"><Lightbulb className={`w-4 h-4 ${TC[m.color]} mt-0.5 flex-shrink-0`}/><p className="text-sm text-gray-200">{d.advice}</p></div>}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                  <div className="grid md:grid-cols-2 gap-4">
                    {data?.affirmation&&<div className="bg-gradient-to-br from-purple-950/40 to-cosmic-900 border border-purple-500/20 rounded-2xl p-5"><div className="flex items-center gap-2 mb-3"><Star className="w-4 h-4 text-amber-400"/><h4 className="text-white font-bold text-sm">Daily Affirmation</h4></div><p className="text-purple-200 italic text-sm">"{data.affirmation}"</p></div>}
                    {data?.crystal_recommendation&&<div className="bg-gradient-to-br from-emerald-950/40 to-cosmic-900 border border-emerald-500/20 rounded-2xl p-5"><div className="flex items-center gap-2 mb-3"><Zap className="w-4 h-4 text-emerald-400"/><h4 className="text-white font-bold text-sm">Crystal Recommendation</h4></div><p className="text-emerald-200 text-sm">{data.crystal_recommendation}</p></div>}
                  </div>
                </div>
              );
            })()}
            {!loading.interp&&!errors.interp&&!interp&&(
              <div className="bg-glass rounded-2xl border border-white/10 p-12 text-center">
                <Sparkles className="w-12 h-12 text-indigo-400 mx-auto mb-4 opacity-50"/>
                <h3 className="text-white font-bold text-lg mb-2">Start AI Interpretation</h3>
                <p className="text-gray-400 text-sm mb-6">Generate a deep AI-powered interpretation of your combined palm and tarot reading</p>
                <button id="btn-start-interp" onClick={loadInterp} className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all">Interpret My Reading</button>
              </div>
            )}
          </div>
        )}

        {tab==='trends'&&(
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div><h2 className="text-xl font-bold text-white">Life Trend Analysis</h2><p className="text-sm text-gray-400 mt-0.5">Trajectory analysis across emotional, career, spiritual & creative domains</p></div>
              <button id="btn-refresh-trends" onClick={loadTrends} disabled={loading.trends} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600/20 border border-emerald-500/30 text-emerald-300 text-sm font-semibold hover:bg-emerald-600/30 transition-all disabled:opacity-50">
                <RefreshCw className={`w-4 h-4 ${loading.trends?'animate-spin':''}`}/>{loading.trends?'Analyzing...':'Refresh'}
              </button>
            </div>
            {loading.trends&&<LoadBox icon={TrendingUp} color="emerald" text="Analyzing your life trends across all domains..."/>}
            {!loading.trends&&errors.trends&&<ErrBox msg={errors.trends} retry={loadTrends}/>}
            {!loading.trends&&!errors.trends&&trends&&(()=>{
              const t=trends.ai_trends||trends;
              const td=t?.trend_scores||t?.trends||{};
              const opps=t?.opportunities||[];
              const chal=t?.challenges||[];
              const grw=t?.growth_potential||{};
              const lp=t?.life_path_analysis||{};
              const tr=t?.overall_trajectory||{};
              return(
                <div className="space-y-6">
                  {tr.message&&(
                    <div className={`border rounded-2xl p-6 ${tr.direction?.includes('ascending')?'bg-emerald-950/30 border-emerald-500/20':'bg-amber-950/30 border-amber-500/20'}`}>
                      <div className="flex items-center gap-3 mb-3"><Compass className="w-5 h-5 text-emerald-400"/><h3 className="text-white font-bold">Overall Life Trajectory</h3>
                        <span className="ml-auto text-xs font-bold px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">{(tr.direction||'stable').replace('_',' ').toUpperCase()} Â· {tr.score}%</span>
                      </div>
                      <p className="text-gray-200 text-sm leading-relaxed">{tr.message}</p>
                    </div>
                  )}
                  {(lp.summary||t?.life_path_narrative)&&(
                    <div className="bg-glass border border-white/10 rounded-2xl p-6">
                      <h3 className="text-white font-bold mb-3 flex items-center gap-2"><Moon className="w-5 h-5 text-purple-400"/> Life Path Analysis</h3>
                      <p className="text-gray-300 text-sm leading-relaxed">{lp.summary||t?.life_path_narrative}</p>
                      {lp.guidance&&<div className="mt-3 bg-purple-950/30 rounded-xl p-3 border border-purple-500/20"><p className="text-purple-200 text-sm">{lp.guidance}</p></div>}
                    </div>
                  )}
                  {Object.keys(td).length>0&&(
                    <div><h3 className="text-white font-bold mb-4">Domain Trend Scores</h3>
                      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">{Object.entries(td).map(([id,trend])=><TrendBar key={id} trend={trend}/>)}</div>
                    </div>
                  )}
                  <div className="grid md:grid-cols-2 gap-6">
                    {opps.length>0&&<div><h3 className="text-white font-bold mb-3 flex items-center gap-2"><Star className="w-4 h-4 text-amber-400"/> Active Opportunities ({opps.length})</h3><div className="space-y-3">{opps.map((opp,i)=>(<div key={i} className="bg-glass border border-amber-500/20 rounded-xl p-4"><div className="flex items-center justify-between mb-1"><h4 className="text-white font-semibold text-sm">{opp.title}</h4><span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">{opp.strength}</span></div><p className="text-gray-400 text-xs">{opp.description}</p></div>))}</div></div>}
                    {chal.length>0&&<div><h3 className="text-white font-bold mb-3 flex items-center gap-2"><Shield className="w-4 h-4 text-rose-400"/> Areas of Attention ({chal.length})</h3><div className="space-y-3">{chal.map((ch,i)=>(<div key={i} className="bg-glass border border-rose-500/20 rounded-xl p-4"><div className="flex items-center justify-between mb-1"><h4 className="text-white font-semibold text-sm">{ch.title}</h4><span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">{ch.severity}</span></div><p className="text-gray-400 text-xs mb-2">{ch.description}</p>{ch.mitigation&&<p className="text-emerald-300 text-xs italic">ðŸ’¡ {ch.mitigation}</p>}</div>))}</div></div>}
                  </div>
                  {grw.phase&&(
                    <div className="bg-gradient-to-br from-teal-950/40 to-cosmic-900 border border-teal-500/20 rounded-2xl p-6">
                      <div className="flex items-center gap-3 mb-3"><TrendingUp className="w-5 h-5 text-teal-400"/><h3 className="text-white font-bold">Growth Phase: <span className="text-teal-300">{grw.phase}</span></h3><span className="ml-auto text-teal-300 font-bold">{grw.overall_score}%</span></div>
                      <p className="text-gray-300 text-sm mb-4">{grw.message}</p>
                      {grw.potential_areas?.length>0&&<div className="space-y-2">{grw.potential_areas.slice(0,5).map((a,i)=>(<div key={i} className="flex items-center justify-between bg-white/5 rounded-lg px-3 py-2"><span className="text-gray-300 text-xs">{a.area}</span><div className="flex items-center gap-2"><span className="text-teal-300 text-xs">+{a.growth_room}% potential</span><span className={`text-[10px] px-1.5 py-0.5 rounded ${a.priority==='high'?'bg-rose-500/20 text-rose-300':'bg-amber-500/20 text-amber-300'}`}>{a.priority}</span></div></div>))}</div>}
                    </div>
                  )}
                </div>
              );
            })()}
            {!loading.trends&&!errors.trends&&!trends&&(
              <div className="bg-glass rounded-2xl border border-white/10 p-12 text-center">
                <TrendingUp className="w-12 h-12 text-emerald-400 mx-auto mb-4 opacity-50"/>
                <h3 className="text-white font-bold text-lg mb-2">Analyze Your Life Trends</h3>
                <p className="text-gray-400 text-sm mb-6">Discover trajectory patterns across your emotional, career, spiritual and creative dimensions</p>
                <button id="btn-start-trends" onClick={loadTrends} className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-all">Start Trend Analysis</button>
              </div>
            )}
          </div>
        )}

        {tab==='personality'&&(
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div><h2 className="text-xl font-bold text-white">Personality Intelligence Report</h2><p className="text-sm text-gray-400 mt-0.5">Big Five mapping, spiritual archetype & behavioral insights powered by Gemini AI</p></div>
              <button id="btn-refresh-persona" onClick={loadPersona} disabled={loading.persona} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-violet-600/20 border border-violet-500/30 text-violet-300 text-sm font-semibold hover:bg-violet-600/30 transition-all disabled:opacity-50">
                <RefreshCw className={`w-4 h-4 ${loading.persona?'animate-spin':''}`}/>{loading.persona?'Analyzing...':'Refresh'}
              </button>
            </div>
            {loading.persona&&<LoadBox icon={Brain} color="violet" text="Building your personality intelligence profile..."/>}
            {!loading.persona&&errors.persona&&<ErrBox msg={errors.persona} retry={loadPersona}/>}
            {!loading.persona&&!errors.persona&&persona&&(()=>{
              const p=persona.ai_personality||persona;
              const bf=p?.big_five_traits||p?.big_five||{};
              const str=p?.strengths||[];
              const wk=p?.growth_areas||p?.weaknesses||[];
              const arch=p?.spiritual_archetype||{};
              const beh=p?.behavioral_insights||[];
              const dev=p?.development_pathway||p?.development_path||{};
              return(
                <div className="space-y-6">
                  {arch.name&&(
                    <div className="bg-gradient-to-br from-violet-950/50 via-purple-950/30 to-cosmic-900 border border-violet-500/20 rounded-2xl p-6">
                      <div className="flex items-center gap-2 mb-1"><Eye className="w-5 h-5 text-violet-400"/><span className="text-xs font-bold text-violet-400 uppercase tracking-widest">Spiritual Archetype</span></div>
                      <h2 className="text-2xl font-extrabold text-white mb-2">{arch.name}</h2>
                      <p className="text-gray-300 text-sm leading-relaxed mb-3">{arch.description}</p>
                      {arch.strengths&&<div className="flex flex-wrap gap-2">{arch.strengths.map((s,i)=><span key={i} className="px-2.5 py-1 rounded-lg bg-violet-500/10 text-violet-300 text-xs border border-violet-500/20">âœ¦ {s}</span>)}</div>}
                    </div>
                  )}
                  {Object.keys(bf).length>0&&(
                    <div className="bg-glass border border-white/10 rounded-2xl p-6">
                      <h3 className="text-white font-bold mb-4 flex items-center gap-2"><BarChart3 className="w-5 h-5 text-violet-400"/> Big Five Personality Traits</h3>
                      <div className="space-y-4">
                        {Object.entries(bf).map(([trait,data],idx)=>{
                          const sc=typeof data==='object'?(data.score||data.value||65):data;
                          const desc=typeof data==='object'?(data.description||data.insight||''):'';
                          return(
                            <div key={trait}>
                              <div className="flex items-center justify-between mb-1.5"><span className="text-gray-200 font-semibold text-sm capitalize">{trait.replace(/_/g,' ')}</span><span className="text-white font-bold text-sm">{Math.round(sc)}%</span></div>
                              <div className="w-full h-2.5 bg-white/10 rounded-full overflow-hidden"><div className={`h-full rounded-full bg-gradient-to-r ${BARS[idx%BARS.length]} transition-all duration-1000`} style={{{width:`${sc}}%`}}/></div>
                              {desc&&<p className="text-gray-500 text-xs mt-1">{desc}</p>}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                  <div className="grid md:grid-cols-2 gap-6">
                    {str.length>0&&(
                      <div className="bg-gradient-to-br from-emerald-950/40 to-cosmic-900 border border-emerald-500/20 rounded-2xl p-5">
                        <h3 className="text-white font-bold mb-3 flex items-center gap-2"><Zap className="w-4 h-4 text-emerald-400"/> Core Strengths</h3>
                        <div className="space-y-2">{str.slice(0,6).map((s,i)=>(<div key={i} className="flex items-start gap-2"><CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0"/><span className="text-gray-200 text-sm">{typeof s==='object'?(s.trait||s.area||s.name||''):s}</span></div>))}</div>
                      </div>
                    )}
                    {wk.length>0&&(
                      <div className="bg-gradient-to-br from-amber-950/40 to-cosmic-900 border border-amber-500/20 rounded-2xl p-5">
                        <h3 className="text-white font-bold mb-3 flex items-center gap-2"><Flame className="w-4 h-4 text-amber-400"/> Growth Opportunities</h3>
                        <div className="space-y-2">{wk.slice(0,6).map((w,i)=>(<div key={i} className="flex items-start gap-2"><ArrowRight className="w-3.5 h-3.5 text-amber-400 mt-0.5 flex-shrink-0"/><span className="text-gray-200 text-sm">{typeof w==='object'?(w.trait||w.area||w.name||''):w}</span></div>))}</div>
                      </div>
                    )}
                  </div>
                  {beh.length>0&&(
                    <div className="bg-glass border border-white/10 rounded-2xl p-6">
                      <h3 className="text-white font-bold mb-4 flex items-center gap-2"><Compass className="w-5 h-5 text-blue-400"/> Behavioral Insights</h3>
                      <div className="grid md:grid-cols-2 gap-3">{beh.slice(0,6).map((b,i)=>(<div key={i} className="flex items-start gap-3 bg-white/5 rounded-xl p-3"><Lightbulb className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0"/><p className="text-gray-300 text-xs leading-relaxed">{typeof b==='object'?(b.insight||b.description||''):b}</p></div>))}</div>
                    </div>
                  )}
                  {(dev.immediate_focus||dev.next_steps)&&(
                    <div className="bg-gradient-to-br from-indigo-950/40 to-cosmic-900 border border-indigo-500/20 rounded-2xl p-6">
                      <h3 className="text-white font-bold mb-4 flex items-center gap-2"><Target className="w-5 h-5 text-indigo-400"/> Development Pathway</h3>
                      <div className="space-y-3">
                        {[{label:'Immediate Focus',data:dev.immediate_focus||(Array.isArray(dev.next_steps)?dev.next_steps[0]:null)},{label:'3-Month Goal',data:dev.three_month_goal||(Array.isArray(dev.next_steps)?dev.next_steps[1]:null)},{label:'Long-term Vision',data:dev.long_term_vision||(Array.isArray(dev.next_steps)?dev.next_steps[2]:null)}].filter(s=>s.data).map((step,i)=>(
                          <div key={i} className="flex items-start gap-3 bg-white/5 rounded-xl p-4">
                            <span className="w-6 h-6 rounded-full bg-indigo-500/30 text-indigo-300 text-xs font-bold flex items-center justify-center flex-shrink-0">{i+1}</span>
                            <div><span className="text-indigo-300 text-xs font-bold uppercase tracking-wide">{step.label}</span><p className="text-gray-300 text-sm mt-0.5">{step.data}</p></div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })()}
            {!loading.persona&&!errors.persona&&!persona&&(
              <div className="bg-glass rounded-2xl border border-white/10 p-12 text-center">
                <Brain className="w-12 h-12 text-violet-400 mx-auto mb-4 opacity-50"/>
                <h3 className="text-white font-bold text-lg mb-2">Generate Personality Intelligence</h3>
                <p className="text-gray-400 text-sm mb-6">Build a comprehensive Big Five profile with spiritual archetypes and development pathways</p>
                <button id="btn-start-persona" onClick={loadPersona} className="px-6 py-3 bg-violet-600 hover:bg-violet-500 text-white font-bold rounded-xl transition-all">Analyze My Personality</button>
              </div>
            )}
          </div>
        )}

        <div className="border-t border-white/5 pt-6">
          <h3 className="text-gray-400 text-xs uppercase font-bold tracking-widest mb-4">Continue Your Journey</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              {href:'/palm-reading',label:'Palm Reading',icon:Hand,cls:'border-purple-500/20 bg-purple-950/30 hover:bg-purple-950/50 hover:border-purple-500/40',ic:'text-purple-300 bg-purple-900/50'},
              {href:'/tarot-reading',label:'Tarot Reading',icon:CreditCard,cls:'border-indigo-500/20 bg-indigo-950/30 hover:bg-indigo-950/50 hover:border-indigo-500/40',ic:'text-indigo-300 bg-indigo-900/50'},
              {href:'/chat',label:'AI Chat',icon:Bot,cls:'border-emerald-500/20 bg-emerald-950/30 hover:bg-emerald-950/50 hover:border-emerald-500/40',ic:'text-emerald-300 bg-emerald-900/50'},
              {href:'/reports',label:'Full Reports',icon:BarChart3,cls:'border-amber-500/20 bg-amber-950/30 hover:bg-amber-950/50 hover:border-amber-500/40',ic:'text-amber-300 bg-amber-900/50'},
            ].map(a=>(
              <Link key={a.href} href={a.href} className={`flex items-center gap-3 p-4 border ${a.cls} rounded-2xl transition-all group`}>
                <div className={`w-9 h-9 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform ${a.ic}`}><a.icon className="w-4 h-4"/></div>
                <span className="text-white font-semibold text-sm">{a.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}


