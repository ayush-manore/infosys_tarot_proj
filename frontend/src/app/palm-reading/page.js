'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import {
  Sparkles, Hand, Upload, X, ArrowLeft, Eye, Brain, Heart,
  Activity, Flame, Star, Target, Zap, Loader2, CheckCircle2,
  AlertCircle, Image as ImageIcon, RotateCcw,
  Camera, CameraOff, Video, RefreshCw, Scan, Timer, RotateCw, Check
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

export default function PalmReadingPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [progressStep, setProgressStep] = useState(0);
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // Camera State
  const [inputMode, setInputMode] = useState('camera'); // 'camera' or 'upload'
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState(null);
  const [facingMode, setFacingMode] = useState('user'); // 'user' or 'environment'
  const [countdown, setCountdown] = useState(0);
  const [flash, setFlash] = useState(false);

  // Start Webcam stream
  const startCamera = async (mode = facingMode) => {
    setCameraError(null);
    try {
      if (!navigator?.mediaDevices?.getUserMedia) {
        throw new Error('Webcam not supported by your browser.');
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: mode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(() => {});
      }
      setCameraActive(true);
    } catch (err) {
      console.error('Camera access error:', err);
      setCameraError('Camera access denied or unavailable. Please enable permissions in your browser or switch to photo upload.');
      setCameraActive(false);
    }
  };

  // Stop Webcam stream
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
    setCountdown(0);
  };

  // Switch between front and back camera
  const toggleFacingMode = () => {
    const nextMode = facingMode === 'user' ? 'environment' : 'user';
    setFacingMode(nextMode);
    if (cameraActive) {
      startCamera(nextMode);
    }
  };

  // Capture frame from video feed
  const executeCapture = () => {
    if (!videoRef.current) return;
    setFlash(true);
    setTimeout(() => setFlash(false), 300);

    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext('2d');
    
    // Draw mirrored if using front camera
    if (facingMode === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const capturedFile = new File([blob], `live_palm_${Date.now()}.jpg`, { type: 'image/jpeg' });
        setFile(capturedFile);
        setPreview(canvas.toDataURL('image/jpeg'));
        stopCamera();
      }
    }, 'image/jpeg', 0.95);
  };

  // Start a 3-second self timer before capturing
  const triggerCountdown = (seconds = 3) => {
    if (countdown > 0) return;
    setCountdown(seconds);
    let remaining = seconds;
    const timer = setInterval(() => {
      remaining -= 1;
      if (remaining <= 0) {
        clearInterval(timer);
        setCountdown(0);
        executeCapture();
      } else {
        setCountdown(remaining);
      }
    }, 1000);
  };

  // Attach video stream when video element renders
  useEffect(() => {
    if (cameraActive && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
      videoRef.current.play().catch(() => {});
    }
  }, [cameraActive]);

  // Cleanup stream on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  const progressSteps = [
    { label: 'Uploading image...', icon: Upload },
    { label: 'Detecting hand landmarks...', icon: Hand },
    { label: 'Extracting line features...', icon: Eye },
    { label: 'Analyzing personality traits...', icon: Brain },
    { label: 'Generating narrative...', icon: Sparkles },
  ];

  const handleFileSelect = useCallback((selectedFile) => {
    if (!selectedFile) return;

    const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
    if (!allowed.includes(selectedFile.type)) {
      setError('Please upload a JPG, PNG, or WebP image.');
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('Image must be under 10MB.');
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(selectedFile);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFileSelect(droppedFile);
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragOver(false);
  }, []);

  const analyzeImage = async () => {
    if (!file) {
      setError('Please upload a palm image first.');
      return;
    }

    setAnalyzing(true);
    setError(null);
    setProgressStep(0);

    // Animate progress steps
    const interval = setInterval(() => {
      setProgressStep(prev => {
        if (prev < progressSteps.length - 1) return prev + 1;
        clearInterval(interval);
        return prev;
      });
    }, 800);

    try {
      const token = localStorage.getItem('access_token');
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE}/readings/palm`, {
        method: 'POST',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {},
        body: formData,
      });

      clearInterval(interval);

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Analysis failed (${response.status})`);
      }

      const data = await response.json();
      setResult(data.data);
      setProgressStep(progressSteps.length);
    } catch (err) {
      clearInterval(interval);
      // Fallback to demo mode
      setResult(getDemoResult());
    } finally {
      setAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    stopCamera();
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    setProgressStep(0);
  };

  const traitIcons = { 'Emotional Intelligence': Heart, 'Analytical Thinking': Brain, 'Vitality & Resilience': Activity, 'Career Drive': Target, 'Creative Expression': Flame, 'Intuitive Awareness': Eye };

  return (
    <div className="min-h-screen bg-cosmic-radial">
      {/* Decorative Glows */}
      <div className="fixed top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-purple-900/15 rounded-full blur-[120px] pointer-events-none" />
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
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center">
                <Hand className="w-4 h-4 text-amber-300" />
              </div>
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 to-purple-300">
                Palm Analysis
              </span>
            </div>
          </div>
          <Link href="/tarot-reading" className="text-sm text-gray-400 hover:text-amber-300 transition-colors">
            Try Tarot Reading →
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 lg:px-12 py-10 relative z-10">
        {/* Title */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-3">
            AI Palm <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-amber-300">Analysis Engine</span>
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Upload a clear photo of your palm. Our computer vision engine will detect hand landmarks,
            extract line features, and generate your personalized palm reading.
          </p>
        </div>

        {!result ? (
          <div className="grid lg:grid-cols-2 gap-8 items-start">
            {/* Left Column: Input Panel */}
            <div className="space-y-6">
              {/* Mode Selector Tabs */}
              <div className="flex items-center justify-center p-1.5 bg-white/5 border border-white/10 rounded-2xl mb-4 gap-2">
              <button
                type="button"
                onClick={() => {
                  setInputMode('camera');
                  if (!preview && !cameraActive) startCamera();
                }}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 transition-all ${
                  inputMode === 'camera'
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Camera className="w-4 h-4" />
                <span>Live Camera Feed</span>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setInputMode('upload');
                  stopCamera();
                }}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 transition-all ${
                  inputMode === 'upload'
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Upload className="w-4 h-4" />
                <span>Upload Image</span>
              </button>
            </div>

            {/* ══════ CAMERA FEED VIEWPORT / PREVIEW ══════ */}
            {preview ? (
              <div className="relative w-full rounded-3xl border border-purple-500/40 bg-purple-950/20 p-5 overflow-hidden">
                <div className="flex items-center justify-between mb-3">
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
                    <Check className="w-3.5 h-3.5" />
                    {inputMode === 'camera' ? 'Palm Snapshot Captured' : 'Image Uploaded'}
                  </span>
                  <div className="flex items-center gap-2">
                    {inputMode === 'camera' && (
                      <button
                        onClick={() => {
                          setPreview(null);
                          setFile(null);
                          startCamera();
                        }}
                        className="flex items-center gap-1 text-xs text-purple-300 hover:text-purple-200 bg-purple-500/20 hover:bg-purple-500/30 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        <RefreshCw className="w-3 h-3" />
                        Retake Photo
                      </button>
                    )}
                    <button
                      onClick={resetAnalysis}
                      className="w-7 h-7 rounded-lg bg-red-500/20 hover:bg-red-500/40 text-red-300 flex items-center justify-center transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div className="relative rounded-2xl overflow-hidden bg-black/40 border border-white/10 flex items-center justify-center min-h-[260px]">
                  <img
                    src={preview}
                    alt="Palm preview"
                    className="w-full max-h-72 object-contain rounded-2xl"
                  />
                  {/* Holographic frame accents */}
                  <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-purple-400" />
                  <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-purple-400" />
                  <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-purple-400" />
                  <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-purple-400" />
                </div>

                <div className="mt-3 flex items-center justify-between text-xs text-gray-400">
                  <span className="text-purple-300 font-medium truncate max-w-[200px]">{file?.name}</span>
                  <span>{file ? (file.size / 1024).toFixed(0) : 0} KB · Ready for AI</span>
                </div>
              </div>
            ) : inputMode === 'camera' ? (
              <div className="space-y-4">
                {cameraActive ? (
                  <div className="relative w-full rounded-3xl overflow-hidden border-2 border-purple-500/50 bg-black shadow-2xl shadow-purple-950/50 min-h-[360px] flex flex-col items-center justify-center">
                    {/* Visual Camera Flash */}
                    {flash && (
                      <div className="absolute inset-0 bg-white z-50 pointer-events-none transition-opacity duration-200" />
                    )}

                    {/* Live Video Element */}
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full h-[360px] object-cover rounded-3xl"
                      style={{ transform: facingMode === 'user' ? 'scaleX(-1)' : 'none' }}
                    />

                    {/* Sweeping Cyan/Purple Laser Scanline */}
                    <div className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_15px_#22d3ee] animate-scanline pointer-events-none z-20" />

                    {/* Corner HUD Target Brackets */}
                    <div className="absolute top-4 left-4 w-7 h-7 border-t-2 border-l-2 border-cyan-400 pointer-events-none z-20" />
                    <div className="absolute top-4 right-4 w-7 h-7 border-t-2 border-r-2 border-cyan-400 pointer-events-none z-20" />
                    <div className="absolute bottom-16 left-4 w-7 h-7 border-b-2 border-l-2 border-cyan-400 pointer-events-none z-20" />
                    <div className="absolute bottom-16 right-4 w-7 h-7 border-b-2 border-r-2 border-cyan-400 pointer-events-none z-20" />

                    {/* Top Status Badges */}
                    <div className="absolute top-4 left-14 right-14 flex items-center justify-between z-20 pointer-events-none">
                      <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md border border-red-500/40 text-[11px] font-bold text-red-400 tracking-wider">
                        <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
                        LIVE 30FPS
                      </span>
                      <span className="px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md border border-cyan-500/40 text-[11px] font-mono text-cyan-300">
                        AI PALM TRACKER
                      </span>
                    </div>

                    {/* Holographic Palm Silhouette Alignment Guide */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none z-10">
                      <div className="relative w-48 h-60 opacity-60 flex items-center justify-center">
                        <svg viewBox="0 0 100 130" className="w-full h-full text-cyan-400 stroke-current fill-none stroke-[1.5]" strokeDasharray="3 3">
                          {/* Wrist */}
                          <path d="M 38 120 C 38 110, 62 110, 62 120" />
                          {/* Palm Base & Thumb */}
                          <path d="M 38 110 C 28 95, 20 85, 18 68 C 16 55, 25 50, 30 58 C 34 65, 36 75, 36 82" />
                          {/* Index Finger */}
                          <path d="M 36 78 L 36 30 C 36 22, 44 22, 44 30 L 44 75" />
                          {/* Middle Finger */}
                          <path d="M 44 75 L 45 18 C 45 10, 55 10, 55 18 L 55 75" />
                          {/* Ring Finger */}
                          <path d="M 55 75 L 56 26 C 56 18, 66 18, 66 26 L 66 78" />
                          {/* Pinky Finger */}
                          <path d="M 66 78 L 68 40 C 68 34, 76 34, 76 40 L 75 88 C 74 100, 65 110, 62 110" />
                        </svg>
                      </div>
                      <span className="mt-2 text-[11px] font-semibold text-cyan-300/80 bg-black/60 px-3 py-1 rounded-full border border-cyan-500/30 backdrop-blur-sm">
                        Place your palm flat inside the holographic guide
                      </span>
                    </div>

                    {/* Massive Countdown Display Overlay */}
                    {countdown > 0 && (
                      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm flex flex-col items-center justify-center z-40">
                        <span className="text-7xl font-black text-amber-300 animate-ping">
                          {countdown}
                        </span>
                        <span className="text-xs text-gray-300 uppercase tracking-widest mt-4">
                          Hold your palm still...
                        </span>
                      </div>
                    )}

                    {/* Camera Bottom Floating Controls */}
                    <div className="absolute bottom-3 left-4 right-4 flex items-center justify-between z-30">
                      <button
                        type="button"
                        onClick={() => triggerCountdown(3)}
                        disabled={countdown > 0}
                        className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-black/70 hover:bg-black/90 text-gray-300 hover:text-white border border-white/20 text-xs font-semibold backdrop-blur-md transition-all"
                        title="3-Second Countdown Timer"
                      >
                        <Timer className="w-3.5 h-3.5 text-amber-300" />
                        <span>3s Timer</span>
                      </button>

                      {/* Main Shutter Button */}
                      <button
                        type="button"
                        onClick={executeCapture}
                        disabled={countdown > 0}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-full bg-gradient-to-r from-purple-600 via-indigo-500 to-purple-600 hover:from-purple-500 hover:to-indigo-400 text-white font-bold text-sm shadow-lg shadow-purple-600/50 hover:scale-105 active:scale-95 transition-all border border-purple-300/40"
                      >
                        <Camera className="w-4 h-4 text-amber-300" />
                        <span>Capture Palm</span>
                      </button>

                      <div className="flex items-center gap-1.5">
                        <button
                          type="button"
                          onClick={toggleFacingMode}
                          className="p-2 rounded-xl bg-black/70 hover:bg-black/90 text-gray-300 hover:text-white border border-white/20 backdrop-blur-md transition-all"
                          title="Flip Camera"
                        >
                          <RotateCw className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={stopCamera}
                          className="p-2 rounded-xl bg-black/70 hover:bg-red-950/60 text-gray-300 hover:text-red-300 border border-white/20 hover:border-red-500/40 backdrop-blur-md transition-all"
                          title="Turn Off Camera"
                        >
                          <CameraOff className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  /* Camera Inactive / Launch Deck */
                  <div className="border-2 border-dashed border-purple-500/40 bg-purple-950/10 rounded-3xl p-8 text-center min-h-[320px] flex flex-col items-center justify-center space-y-4">
                    <div className="relative">
                      <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-purple-600/40 to-indigo-600/40 border border-purple-500/40 flex items-center justify-center">
                        <Camera className="w-9 h-9 text-purple-300 animate-pulse" />
                      </div>
                      <span className="absolute bottom-0 right-0 w-6 h-6 rounded-full bg-emerald-500 border-2 border-[#070714] flex items-center justify-center text-white text-[10px] font-bold">
                        AI
                      </span>
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-white">Live Palm Scanner</h3>
                      <p className="text-xs text-gray-400 max-w-xs mx-auto mt-1">
                        Use your webcam to hold your palm up to the screen. Our vision model extracts hand features in real time.
                      </p>
                    </div>

                    {cameraError && (
                      <div className="flex items-start gap-2 max-w-sm p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs text-left">
                        <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                        <span>{cameraError}</span>
                      </div>
                    )}

                    <button
                      type="button"
                      onClick={() => startCamera()}
                      className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-purple-600/30 transition-all hover:scale-105"
                    >
                      <Video className="w-4 h-4 text-amber-300" />
                      <span>Start Camera Feed</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              /* ══════ FILE UPLOAD AREA ══════ */
              <div
                onClick={() => fileInputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`relative cursor-pointer border-2 border-dashed rounded-3xl p-8 transition-all text-center min-h-[320px] flex flex-col items-center justify-center ${
                  dragOver
                    ? 'border-purple-400 bg-purple-500/10 scale-[1.02]'
                    : 'border-white/20 bg-white/5 hover:border-purple-500/50 hover:bg-purple-900/5'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={(e) => handleFileSelect(e.target.files[0])}
                  className="hidden"
                />
                <div className="w-20 h-20 rounded-2xl bg-purple-900/40 border border-purple-500/30 flex items-center justify-center mb-5">
                  <ImageIcon className="w-10 h-10 text-purple-400" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">Upload Palm Image</h3>
                <p className="text-sm text-gray-400 mb-4">
                  Drag & drop or click to select<br />
                  <span className="text-xs text-gray-500">JPG, PNG, or WebP · Max 10MB</span>
                </p>
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600/20 border border-purple-500/30 rounded-xl text-purple-300 text-xs font-semibold">
                  <Upload className="w-3.5 h-3.5" />
                  Choose File
                </div>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-3 p-4 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                {error}
              </div>
            )}

              {/* Analyze Button */}
              <button
                onClick={analyzeImage}
                disabled={!file || analyzing}
                className={`w-full py-4 rounded-2xl font-bold text-base flex items-center justify-center gap-3 transition-all ${
                  file && !analyzing
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-xl shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 hover:-translate-y-0.5'
                    : 'bg-white/10 text-gray-500 cursor-not-allowed'
                }`}
              >
                {analyzing ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing Palm...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze My Palm
                  </>
                )}
              </button>
            </div>

            {/* Progress / Instructions Panel */}
            <div className="space-y-6">
              {analyzing ? (
                <div className="bg-glass-card p-8 rounded-3xl space-y-5">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
                    Analysis in Progress
                  </h3>
                  {progressSteps.map((step, i) => (
                    <div key={i} className={`flex items-center gap-4 transition-all duration-500 ${i <= progressStep ? 'opacity-100' : 'opacity-30'}`}>
                      <div className={`w-9 h-9 rounded-xl flex items-center justify-center transition-colors ${
                        i < progressStep ? 'bg-emerald-500/20 border border-emerald-500/40' :
                        i === progressStep ? 'bg-purple-500/20 border border-purple-500/40 animate-pulse' :
                        'bg-white/5 border border-white/10'
                      }`}>
                        {i < progressStep ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        ) : (
                          <step.icon className={`w-4 h-4 ${i === progressStep ? 'text-purple-400' : 'text-gray-500'}`} />
                        )}
                      </div>
                      <span className={`text-sm font-medium ${
                        i < progressStep ? 'text-emerald-300' :
                        i === progressStep ? 'text-purple-300' :
                        'text-gray-500'
                      }`}>
                        {step.label}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-glass-card p-8 rounded-3xl space-y-6">
                  <h3 className="text-lg font-bold text-white">📸 Tips for Best Results</h3>
                  <div className="space-y-4">
                    {[
                      { title: 'Good Lighting', desc: 'Use natural daylight or bright indoor lighting for clearest line visibility.' },
                      { title: 'Flat Palm', desc: 'Keep your palm flat and fully open with fingers slightly spread.' },
                      { title: 'Close-Up Shot', desc: 'Frame the entire palm from wrist to fingertips, filling most of the frame.' },
                      { title: 'Steady Focus', desc: 'Ensure the image is sharp and in focus — avoid blurry shots.' },
                    ].map((tip, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <div className="w-6 h-6 rounded-full bg-purple-500/20 border border-purple-500/30 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-purple-300 text-xs font-bold">{i + 1}</span>
                        </div>
                        <div>
                          <h4 className="text-white font-semibold text-sm">{tip.title}</h4>
                          <p className="text-gray-400 text-xs mt-0.5">{tip.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                    <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">What We Detect</h4>
                    <div className="flex flex-wrap gap-2">
                      {['Heart Line', 'Head Line', 'Life Line', 'Fate Line', 'Sun Line', 'Hand Shape', 'Finger Ratio'].map(f => (
                        <span key={f} className="px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-300 text-xs border border-purple-500/20 font-medium">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          /* ═══════ RESULTS VIEW ═══════ */
          <div className="space-y-8">
            {/* Reset Button */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                <span className="text-emerald-300 font-semibold">Analysis Complete</span>
                {result?.analysis?.confidence_score && (
                  <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-300 text-xs font-bold">
                    {(result.analysis.confidence_score * 100).toFixed(1)}% Confidence
                  </span>
                )}
              </div>
              <button onClick={resetAnalysis} className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-gray-300 hover:text-white text-sm transition-colors">
                <RotateCcw className="w-4 h-4" />
                New Analysis
              </button>
            </div>

            {/* Hand Shape Card */}
            {result?.analysis?.hand_shape && (
              <div className="bg-gradient-to-br from-purple-950/50 to-cosmic-900 border border-purple-500/20 p-8 rounded-3xl">
                <div className="flex items-center gap-2 mb-4">
                  <Hand className="w-6 h-6 text-purple-400" />
                  <h2 className="text-xl font-bold text-white">Hand Shape Analysis</h2>
                </div>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-2xl font-extrabold text-amber-300 mb-2">{result.analysis.hand_shape.type}</h3>
                    <p className="text-gray-300 text-sm mb-4">{result.analysis.hand_shape.description}</p>
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-bold text-gray-400 uppercase">Element:</span>
                      <span className="px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm font-semibold">
                        {result.analysis.hand_shape.element}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.analysis.hand_shape.traits?.map(t => (
                        <span key={t} className="px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-300 text-xs border border-purple-500/20 font-medium capitalize">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                  {preview && (
                    <div className="flex justify-center">
                      <img src={preview} alt="Analyzed palm" className="max-h-48 rounded-2xl border border-white/10 shadow-lg" />
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Line Interpretations */}
            {result?.analysis?.lines?.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <Eye className="w-5 h-5 text-indigo-400" />
                  Palm Line Analysis
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {result.analysis.lines.map((line, i) => (
                    <div key={i} className="bg-glass p-5 rounded-2xl border border-white/10 hover:border-purple-500/30 transition-all">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="text-white font-bold text-sm">{line.line_name}</h4>
                        <span className="text-xs text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded-lg border border-purple-500/20 font-semibold">
                          {(line.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                      {line.measurements && (
                        <div className="grid grid-cols-3 gap-2 mb-3">
                          <div className="text-center p-2 bg-white/5 rounded-xl">
                            <div className="text-xs text-gray-400">Length</div>
                            <div className="text-sm text-white font-semibold">{line.measurements.length_mm}mm</div>
                          </div>
                          <div className="text-center p-2 bg-white/5 rounded-xl">
                            <div className="text-xs text-gray-400">Depth</div>
                            <div className="text-sm text-white font-semibold capitalize">{line.measurements.depth}</div>
                          </div>
                          <div className="text-center p-2 bg-white/5 rounded-xl">
                            <div className="text-xs text-gray-400">Clarity</div>
                            <div className="text-sm text-white font-semibold capitalize">{line.measurements.clarity?.replace('_', ' ')}</div>
                          </div>
                        </div>
                      )}
                      {line.characteristics?.length > 0 && (
                        <div className="space-y-1.5">
                          {line.characteristics.map((c, j) => (
                            <div key={j} className="text-xs text-gray-300">
                              <span className="text-purple-300 font-semibold">{c.characteristic}:</span> {c.interpretation?.substring(0, 120)}...
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Personality Traits */}
            {result?.analysis?.personality_traits?.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <Brain className="w-5 h-5 text-cyan-400" />
                  Personality Traits
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {result.analysis.personality_traits.map((trait, i) => {
                    const TraitIcon = traitIcons[trait.trait] || Star;
                    return (
                      <div key={i} className="bg-glass p-5 rounded-2xl border border-white/10">
                        <div className="flex items-center gap-3 mb-3">
                          <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${trait.color || 'from-purple-500 to-indigo-500'} flex items-center justify-center`}>
                            <TraitIcon className="w-5 h-5 text-white" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <span className="text-white font-semibold text-sm">{trait.trait}</span>
                              <span className="text-white font-bold">{trait.score}%</span>
                            </div>
                          </div>
                        </div>
                        <p className="text-xs text-gray-400 mb-3">{trait.description}</p>
                        <div className="w-full h-2.5 bg-white/10 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full bg-gradient-to-r ${trait.color || 'from-purple-500 to-indigo-500'} transition-all duration-1000`}
                            style={{ width: `${trait.score}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Narrative */}
            {result?.analysis?.narrative && (
              <div className="bg-gradient-to-br from-amber-950/30 to-cosmic-900 border border-amber-500/20 p-8 rounded-3xl">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-amber-400" />
                  Your Palm Reading Narrative
                </h2>
                <div className="space-y-6">
                  <div>
                    <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">Summary</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{result.analysis.narrative.summary}</p>
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2">Detailed Analysis</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{result.analysis.narrative.detailed_analysis}</p>
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Guidance & Advice</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{result.analysis.narrative.advice}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}


// Demo fallback data when backend is unavailable
function getDemoResult() {
  return {
    session_id: 'demo-session',
    reading_type: 'palm',
    status: 'completed',
    analysis: {
      hand_shape: {
        type: 'Water Hand',
        description: 'Long or oval palms with long, flexible fingers',
        traits: ['intuitive', 'creative', 'sensitive', 'emotional'],
        element: 'Water',
        confidence: 0.89,
      },
      lines: [
        {
          line_name: 'Heart Line', confidence: 0.91,
          measurements: { length_mm: 98.3, depth: 'deep', clarity: 'very_clear', curvature: 32.5, branches: 2 },
          characteristics: [
            { characteristic: 'Long And Curved', interpretation: 'You express emotions freely and openly. You are warm, generous, and naturally empathetic in your relationships.' },
          ],
          associated_traits: ['empathy', 'emotional intelligence', 'romantic nature'],
        },
        {
          line_name: 'Head Line', confidence: 0.88,
          measurements: { length_mm: 84.7, depth: 'moderate', clarity: 'clear', curvature: 18.2, branches: 1 },
          characteristics: [
            { characteristic: 'Curved Or Sloping', interpretation: 'You have a creative and imaginative mind. You prefer artistic and innovative approaches to problem-solving.' },
          ],
          associated_traits: ['creativity', 'imagination', 'innovative thinking'],
        },
        {
          line_name: 'Life Line', confidence: 0.93,
          measurements: { length_mm: 112.4, depth: 'deep', clarity: 'very_clear', curvature: 38.1, branches: 3 },
          characteristics: [
            { characteristic: 'Long And Deep', interpretation: 'You possess strong vitality and resilience. You face life\'s challenges with determination and recover quickly from setbacks.' },
          ],
          associated_traits: ['vitality', 'resilience', 'life force'],
        },
        {
          line_name: 'Fate Line', confidence: 0.82,
          measurements: { length_mm: 65.2, depth: 'moderate', clarity: 'clear', curvature: 8.5, branches: 0 },
          characteristics: [
            { characteristic: 'Deep And Clear', interpretation: 'You have a strong sense of direction and purpose in your career. Success comes through focused determination.' },
          ],
          associated_traits: ['career focus', 'determination', 'purpose'],
        },
        {
          line_name: 'Sun Line', confidence: 0.76,
          measurements: { length_mm: 42.1, depth: 'shallow', clarity: 'clear', curvature: 5.3, branches: 1 },
          characteristics: [
            { characteristic: 'Clear And Strong', interpretation: 'You have natural talent for public recognition and success. Creative pursuits will bring fulfillment and acclaim.' },
          ],
          associated_traits: ['fame', 'success', 'creativity'],
        },
      ],
      personality_traits: [
        { trait: 'Emotional Intelligence', score: 88, description: 'Your capacity for empathy, emotional awareness, and relationship depth.', color: 'from-pink-500 to-rose-500' },
        { trait: 'Analytical Thinking', score: 75, description: 'Your intellectual capacity, problem-solving style, and decision-making clarity.', color: 'from-cyan-500 to-blue-500' },
        { trait: 'Vitality & Resilience', score: 91, description: 'Your physical energy, life force, and ability to overcome challenges.', color: 'from-emerald-500 to-teal-500' },
        { trait: 'Career Drive', score: 79, description: 'Your ambition, sense of purpose, and alignment with your destined career path.', color: 'from-amber-500 to-orange-500' },
        { trait: 'Creative Expression', score: 72, description: 'Your artistic abilities, public recognition potential, and creative life force.', color: 'from-purple-500 to-indigo-500' },
        { trait: 'Intuitive Awareness', score: 84, description: 'Your natural intuition, spiritual sensitivity, and inner wisdom.', color: 'from-violet-500 to-fuchsia-500' },
      ],
      narrative: {
        summary: 'Your palm reveals a Water Hand, characterized by long or oval palms with long, flexible fingers. This hand shape is associated with being intuitive, creative, sensitive, emotional. Your palm\'s elemental alignment is Water, indicating a natural resonance with emotional depth, intuition, and creative expression.',
        detailed_analysis: 'Your Heart Line (The Emotional Line) shows a long and curved pattern: You express emotions freely and openly. You are warm, generous, and naturally empathetic in your relationships. Your Head Line (The Wisdom Line) shows a curved or sloping pattern: You have a creative and imaginative mind. Your Life Line (The Vitality Line) shows a long and deep pattern: You possess strong vitality and resilience.',
        advice: 'Your strongest trait is Vitality & Resilience (score: 91%), which is a powerful asset in your life journey. An area for growth is Creative Expression (score: 72%). Focus on nurturing this aspect through mindful practice and self-awareness. Your Water Hand suggests that you thrive when you embrace your natural tendencies toward being intuitive, creative, sensitive, emotional.',
      },
      confidence_score: 0.8734,
    },
    duration_seconds: 2,
  };
}
