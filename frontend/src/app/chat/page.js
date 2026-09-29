'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import {
  Sparkles, ArrowLeft, Send, Bot, User, Trash2, Moon, Sun,
  CreditCard, Hand, Brain, Star, RotateCcw, MessageSquare,
  Loader2, Wand2, ChevronDown
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

/* ── Quick Prompts ──────────────────────────────────────── */
const quickPrompts = [
  { icon: CreditCard, label: 'Tarot guidance', prompt: 'What tarot spread would you recommend for me right now?' },
  { icon: Hand, label: 'Palm reading', prompt: 'Tell me about the Heart Line in palm reading. What does it reveal?' },
  { icon: Brain, label: 'Personality insight', prompt: 'Based on tarot archetypes, what personality traits might I have?' },
  { icon: Star, label: 'Daily guidance', prompt: 'Can you give me a daily spiritual guidance message for today?' },
  { icon: Moon, label: 'Meditation', prompt: 'Suggest a meditation practice for spiritual growth and inner peace.' },
  { icon: Sun, label: 'Affirmation', prompt: 'Give me a powerful affirmation to start my day with positive energy.' },
];

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [showQuickPrompts, setShowQuickPrompts] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  /* ── Auto-scroll to latest message ──────────────────────── */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /* ── Welcome message on mount ───────────────────────────── */
  useEffect(() => {
    setMessages([{
      role: 'assistant',
      content: '✨ Welcome, dear seeker! I am **MysticAI**, your spiritual guide and mystic counselor.\n\nI can help you with:\n- 🔮 **Tarot card meanings** and spread recommendations\n- 🤚 **Palm reading** insights and line interpretations\n- 🧠 **Personality analysis** from your readings\n- 🌙 **Meditation & rituals** for spiritual growth\n- ✨ **Daily guidance** and affirmations\n\nAsk me anything, or try one of the quick prompts below!',
      timestamp: new Date().toISOString(),
    }]);
  }, []);

  /* ── Send Message ───────────────────────────────────────── */
  const sendMessage = async (text) => {
    const messageText = text || input.trim();
    if (!messageText || loading) return;

    setInput('');
    setShowQuickPrompts(false);

    // Add user message
    const userMsg = { role: 'user', content: messageText, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const body = {
        message: messageText,
      };
      if (conversationId) body.conversation_id = conversationId;

      const response = await fetch(`${API_BASE}/ai/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      });

      if (!response.ok) throw new Error('Chat request failed');

      const data = await response.json();
      const aiResponse = data.data?.response || data.data?.message || 'The cosmic energies are realigning... please try again.';

      if (data.data?.conversation_id) {
        setConversationId(data.data.conversation_id);
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: aiResponse,
        timestamp: data.data?.timestamp || new Date().toISOString(),
        model: data.data?.model,
        aiStatus: data.data?.ai_status,
      }]);
    } catch {
      // Fallback response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: getFallbackResponse(messageText),
        timestamp: new Date().toISOString(),
        model: 'fallback',
        aiStatus: 'fallback',
      }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{
      role: 'assistant',
      content: '✨ Chat cleared! How can I guide you on your spiritual journey today? 🌙',
      timestamp: new Date().toISOString(),
    }]);
    setConversationId(null);
    setShowQuickPrompts(true);
  };

  /* ── Simple markdown renderer ───────────────────────────── */
  const renderMarkdown = (text) => {
    return text
      .split('\n')
      .map((line, i) => {
        // Bold
        line = line.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>');
        // Bullet points
        if (line.startsWith('- ')) {
          return `<div class="flex items-start gap-2 ml-2"><span class="text-purple-400 mt-0.5">•</span><span>${line.substring(2)}</span></div>`;
        }
        if (line === '') return '<br/>';
        return `<p>${line}</p>`;
      })
      .join('');
  };

  return (
    <div className="min-h-screen bg-cosmic-radial flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-cosmic-950/80 backdrop-blur-md border-b border-white/10 px-6 lg:px-12 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm">
              <ArrowLeft className="w-4 h-4" />
              Dashboard
            </Link>
            <div className="w-px h-5 bg-white/10" />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-emerald-600 to-purple-600 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-200 to-purple-300">
                MysticAI Chat
              </span>
            </div>
            {conversationId && (
              <span className="hidden md:inline-flex px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/30 rounded text-emerald-300 text-[10px] font-bold">
                LIVE SESSION
              </span>
            )}
          </div>
          <button
            onClick={clearChat}
            className="flex items-center gap-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-xl text-gray-400 hover:text-white text-xs transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear Chat
          </button>
        </div>
      </header>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 lg:px-0">
        <div className="max-w-4xl mx-auto py-6 space-y-6">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 animate-fadeIn ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'assistant' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-gradient-to-br from-purple-600 to-emerald-600 flex items-center justify-center mt-1">
                  <Wand2 className="w-4 h-4 text-white" />
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-2xl px-5 py-4 text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-br-md'
                    : 'bg-glass text-gray-200 rounded-bl-md'
                }`}
              >
                {msg.role === 'assistant' ? (
                  <div
                    className="space-y-1 [&_strong]:text-purple-200"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
                  />
                ) : (
                  <p>{msg.content}</p>
                )}

                {/* Metadata */}
                <div className={`flex items-center gap-2 mt-2 text-[10px] ${
                  msg.role === 'user' ? 'text-purple-200/60' : 'text-gray-500'
                }`}>
                  <span>{new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  {msg.model && msg.model !== 'fallback' && (
                    <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                      Gemini AI
                    </span>
                  )}
                  {msg.aiStatus === 'fallback' && (
                    <span className="px-1.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-400">
                      Offline Mode
                    </span>
                  )}
                </div>
              </div>

              {msg.role === 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mt-1">
                  <User className="w-4 h-4 text-white" />
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {loading && (
            <div className="flex gap-3 justify-start animate-fadeIn">
              <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-gradient-to-br from-purple-600 to-emerald-600 flex items-center justify-center mt-1">
                <Wand2 className="w-4 h-4 text-white" />
              </div>
              <div className="bg-glass rounded-2xl rounded-bl-md px-5 py-4 flex items-center gap-3">
                <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
                <span className="text-gray-400 text-sm">Channeling cosmic wisdom...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Quick Prompts */}
      {showQuickPrompts && (
        <div className="px-4 lg:px-0 pb-2">
          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {quickPrompts.map((qp, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(qp.prompt)}
                  className="flex items-center gap-2.5 px-4 py-3 bg-glass-card rounded-xl hover:bg-white/10 border border-white/10 hover:border-purple-500/30 transition-all text-left group"
                >
                  <qp.icon className="w-4 h-4 text-purple-400 flex-shrink-0 group-hover:text-amber-300 transition-colors" />
                  <span className="text-xs text-gray-300 group-hover:text-white transition-colors">{qp.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="sticky bottom-0 bg-cosmic-950/90 backdrop-blur-md border-t border-white/10 px-4 lg:px-0 py-4">
        <div className="max-w-4xl mx-auto flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask MysticAI anything about tarot, palmistry, spirituality..."
              rows={1}
              className="w-full bg-white/5 border border-white/15 rounded-2xl px-5 py-4 pr-14 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/30 transition-all resize-none"
              style={{ minHeight: '56px', maxHeight: '150px' }}
            />
          </div>
          <button
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            className="flex-shrink-0 w-14 h-14 rounded-2xl bg-gradient-to-r from-purple-600 to-emerald-600 text-white flex items-center justify-center shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-emerald-500 transition-all disabled:opacity-40 disabled:cursor-not-allowed hover:-translate-y-0.5"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="max-w-4xl mx-auto text-[10px] text-gray-500 mt-2 text-center">
          MysticAI is powered by Google Gemini. Responses are for spiritual guidance and entertainment — not medical, legal, or financial advice.
        </p>
      </div>
    </div>
  );
}


/* ── Fallback Responses ────────────────────────────────────── */
function getFallbackResponse(message) {
  const lower = message.toLowerCase();

  if (['hello', 'hi', 'hey', 'greetings'].some(w => lower.includes(w))) {
    return '✨ Greetings, dear seeker! I am MysticAI, your spiritual guide. While my cosmic connection is being established, I\'m here to help you explore the mysteries of tarot and palmistry. What draws your curiosity today? 🌙';
  }

  if (['tarot', 'card', 'reading', 'spread'].some(w => lower.includes(w))) {
    return '🔮 The tarot speaks in symbols and archetypes that mirror our inner landscape. Each card holds layers of meaning waiting to be revealed.\n\nYou can perform a reading from your dashboard:\n- **Three Card Spread** for past-present-future insights\n- **Celtic Cross** for deeper exploration\n- **Single Card** for quick guidance\n\nWould you like guidance on choosing a spread? ✨';
  }

  if (['palm', 'hand', 'line'].some(w => lower.includes(w))) {
    return '🤚 Your palm is a living map of your potential!\n\n- **Heart Line** reveals your emotional nature\n- **Head Line** shows your intellectual approach\n- **Life Line** maps your vitality and life path\n- **Fate Line** indicates destiny\'s influence\n- **Sun Line** reflects success and creativity\n\nUpload a palm image from your dashboard for a detailed analysis. What aspect interests you most? ✨';
  }

  if (['meditation', 'meditate', 'calm', 'peace'].some(w => lower.includes(w))) {
    return '🧘 Here\'s a grounding meditation for you:\n\n**1.** Find a quiet space and close your eyes\n**2.** Take 3 deep breaths, inhaling through your nose\n**3.** Visualize a warm golden light at your crown chakra\n**4.** Let the light slowly flow down through your body\n**5.** Feel it grounding you to the earth\n**6.** Hold this visualization for 5-10 minutes\n\nThis practice strengthens your intuitive connection and prepares you for more insightful readings. 🌙';
  }

  return '✨ Thank you for reaching out, dear seeker. The cosmic energies are aligning for your journey.\n\nI can help you explore:\n- 🔮 **Tarot card meanings** and spread guidance\n- 🤚 **Palm reading** interpretations\n- 🧠 **Personality insights** from your readings\n- 🌙 **Meditation** and spiritual practices\n\nStart a reading from your dashboard, or ask me about any spiritual topic! 🌙';
}
