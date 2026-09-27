---
fable_schema: "5.1.0"
urn: "urn:tgn:blueprint:monetization_engine:c8a942ff-2cea-4461-8586-4b6b36393033"
title: "CashFlow Architect: Monetization Engine & Bot Assessment Dashboard"
transport: "BotAPI"
concurrency:
  paradigm: "AsyncIO"
  max_throughput_est: "500 req/s"
fsm:
  defined: true
  states:
    - "LANDING"
    - "ASSESSMENT_PROFILE"
    - "ASSESSMENT_BUDGET"
    - "ASSESSMENT_TIME"
    - "CALCULATING_METRICS"
    - "DASHBOARD_VIEW"
    - "EXPORT_REPORT"
  storage_driver: "Memory"
dependencies:
  external:
    - "react>=18.2.0"
    - "react-dom>=18.2.0"
    - "lucide-react>=0.263.0"
    - "tailwindcss>=3.3.0"
  internal_urns:
    - "urn:tgn:blueprint:market_intelligence:64db5273-9cb7-44fe-bc94-27ba78234a00"
    - "urn:tgn:blueprint:financial_model:e38481dd-cdfa-4cf3-88b2-fc3ab82873f4"
breaking_changes_detected:
  - "React 18 concurrent rendering root API (createRoot) requirement"
verification_checksum: "1a1d2689d8171cb1bdd36b573daed2a17e29a6cda11d6b6133f7aa721892e0c5"
---
# CashFlow Architect - Complete Implementation

I'll create all the remaining files for a sophisticated, publish-ready monetization app. Here's the complete implementation:

## 1. index.tsx - Entry Point

React

```
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error('Failed to find the root element');

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## 2. App.tsx - Main Application

React

```
import React, { useState, useCallback, useEffect } from 'react';
import { UserAssessment, AppState, BotBlueprint } from './types';
import { BOT_BLUEPRINTS } from './constants';
import Landing from './components/Landing';
import Assessment from './components/Assessment';
import Dashboard from './components/Dashboard';
import { useAssessment } from './hooks/useAssessment';
import { useAnalytics } from './hooks/useAnalytics';
import { loadFromStorage, saveToStorage } from './utils/storage';
import { filterBlueprints, calculateMatchScore } from './utils/calculations';

type Screen = 'landing' | 'assessment' | 'dashboard';

const App: React.FC = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>('landing');
  const [filteredBlueprints, setFilteredBlueprints] = useState<BotBlueprint[]>([]);
  const { assessment, updateAssessment, resetAssessment, isComplete } = useAssessment();
  const { trackEvent, trackPageView } = useAnalytics();

  useEffect(() => {
    const savedState = loadFromStorage<AppState>('cashflow_state');
    if (savedState?.assessment && savedState?.completedAssessment) {
      updateAssessment(savedState.assessment);
      setCurrentScreen('dashboard');
    }
    trackPageView('app_loaded');
  }, []);

  useEffect(() => {
    if (currentScreen === 'dashboard' && isComplete) {
      const filtered = filterBlueprints(BOT_BLUEPRINTS, assessment);
      const scored = filtered.map(bp => ({
        ...bp,
        matchScore: calculateMatchScore(bp, assessment)
      })).sort((a, b) => b.matchScore - a.matchScore);
      setFilteredBlueprints(scored);
      
      saveToStorage('cashflow_state', {
        assessment,
        completedAssessment: true,
        lastUpdated: new Date().toISOString()
      });
    }
  }, [currentScreen, assessment, isComplete]);

  const handleStartAssessment = useCallback(() => {
    trackEvent('assessment_started');
    setCurrentScreen('assessment');
  }, [trackEvent]);

  const handleCompleteAssessment = useCallback((finalAssessment: UserAssessment) => {
    updateAssessment(finalAssessment);
    trackEvent('assessment_completed', finalAssessment);
    setCurrentScreen('dashboard');
  }, [updateAssessment, trackEvent]);

  const handleRestartAssessment = useCallback(() => {
    resetAssessment();
    trackEvent('assessment_restarted');
    setCurrentScreen('assessment');
  }, [resetAssessment, trackEvent]);

  const handleBackToLanding = useCallback(() => {
    setCurrentScreen('landing');
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="fixed inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiM5QzkyQUMiIGZpbGwtb3BhY2l0eT0iMC4wNCI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-40"></div>
      
      <div className="relative z-10">
        {currentScreen === 'landing' && (
          <Landing onStart={handleStartAssessment} />
        )}
        
        {currentScreen === 'assessment' && (
          <Assessment
            initialAssessment={assessment}
            onComplete={handleCompleteAssessment}
            onBack={handleBackToLanding}
          />
        )}
        
        {currentScreen === 'dashboard' && (
          <Dashboard
            assessment={assessment}
            blueprints={filteredBlueprints}
            onRestart={handleRestartAssessment}
          />
        )}
      </div>
    </div>
  );
};

export default App;
```

## 3. components/Landing.tsx

React

```
import React, { useState, useEffect } from 'react';

interface LandingProps {
  onStart: () => void;
}

const Landing: React.FC<LandingProps> = ({ onStart }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveFeature(prev => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: '🎯',
      title: 'Personalized Blueprints',
      description: 'AI-powered recommendations based on your skills, budget, and time'
    },
    {
      icon: '💰',
      title: 'Revenue Projections',
      description: 'Realistic income forecasts with detailed breakdown models'
    },
    {
      icon: '🛠️',
      title: 'Complete Tech Stacks',
      description: 'Production-ready architecture and deployment guides'
    },
    {
      icon: '📊',
      title: 'Risk Analysis',
      description: 'Professional market and technical risk assessments'
    }
  ];

  const stats = [
    { value: '50+', label: 'Business Models' },
    { value: '$10K-100K', label: 'Revenue Potential' },
    { value: '2-8 Weeks', label: 'To MVP Launch' },
    { value: '1B+', label: 'Telegram Users' }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/30 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-conic from-purple-500/20 via-transparent to-blue-500/20 rounded-full blur-2xl animate-spin-slow"></div>
        </div>

        <nav className="relative z-10 container mx-auto px-6 py-6 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">💸</span>
            </div>
            <span className="text-white font-bold text-xl tracking-tight">CashFlow Architect</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-purple-300 text-sm hidden sm:block">Telegram Business Platform</span>
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </nav>

        <div className={`relative z-10 container mx-auto px-6 pt-16 pb-24 text-center transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-8 border border-white/20">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span className="text-purple-200 text-sm font-medium">Powered by Advanced AI Analysis</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-tight">
            Build Your
            <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 text-transparent bg-clip-text">
              Telegram Empire
            </span>
          </h1>

          <p className="text-xl text-purple-200 max-w-2xl mx-auto mb-12 leading-relaxed">
            Transform your skills into profitable Telegram bots. Get personalized blueprints,
            revenue projections, and complete technical roadmaps in minutes.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <button
              onClick={onStart}
              className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl text-white font-bold text-lg shadow-2xl shadow-purple-500/30 hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105 active:scale-95"
            >
              <span className="relative z-10 flex items-center gap-2">
                Start Free Assessment
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-blue-400 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity blur-xl"></div>
            </button>
            
            <span className="text-purple-300 text-sm">⏱️ Takes only 2 minutes</span>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <div
                key={index}
                className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-purple-500/50 transition-all duration-300 hover:scale-105"
              >
                <div className="text-3xl font-black text-white mb-1">{stat.value}</div>
                <div className="text-purple-300 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section className="relative py-24 bg-black/20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Everything You Need to Succeed
            </h2>
            <p className="text-purple-300 max-w-xl mx-auto">
              From idea validation to revenue generation, we provide the complete toolkit
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className={`relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm rounded-3xl p-8 border transition-all duration-500 cursor-pointer ${
                  activeFeature === index
                    ? 'border-purple-500 scale-105 shadow-2xl shadow-purple-500/20'
                    : 'border-white/10 hover:border-white/30'
                }`}
                onClick={() => setActiveFeature(index)}
              >
                <div className="text-5xl mb-6">{feature.icon}</div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-purple-300 leading-relaxed">{feature.description}</p>
                
                {activeFeature === index && (
                  <div className="absolute -inset-[1px] bg-gradient-to-r from-purple-500 to-blue-500 rounded-3xl -z-10 blur-sm"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-3xl mx-auto bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-xl rounded-3xl p-12 border border-purple-500/30">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Find Your Cashflow?
            </h2>
            <p className="text-purple-200 mb-8 text-lg">
              Join thousands of entrepreneurs building profitable Telegram businesses
            </p>
            <button
              onClick={onStart}
              className="px-10 py-5 bg-white text-purple-900 rounded-2xl font-bold text-lg hover:bg-purple-100 transition-all duration-300 hover:scale-105 shadow-2xl"
            >
              Start Your Journey →
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative py-8 border-t border-white/10">
        <div className="container mx-auto px-6 text-center">
          <p className="text-purple-400 text-sm">
            © 2024 CashFlow Architect. Built for ambitious entrepreneurs.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
```

## 4. components/Assessment.tsx

React

```
import React, { useState, useCallback } from 'react';
import { UserAssessment, TechnicalLevel, BudgetRange, TimeCommitment, NichePreference } from './types';

interface AssessmentProps {
  initialAssessment: UserAssessment;
  onComplete: (assessment: UserAssessment) => void;
  onBack: () => void;
}

const Assessment: React.FC<AssessmentProps> = ({ initialAssessment, onComplete, onBack }) => {
  const [step, setStep] = useState(1);
  const [assessment, setAssessment] = useState<UserAssessment>(initialAssessment);
  const [isAnimating, setIsAnimating] = useState(false);

  const totalSteps = 5;

  const handleNext = useCallback(() => {
    if (step < totalSteps) {
      setIsAnimating(true);
      setTimeout(() => {
        setStep(prev => prev + 1);
        setIsAnimating(false);
      }, 300);
    } else {
      onComplete(assessment);
    }
  }, [step, assessment, onComplete]);

  const handleBack = useCallback(() => {
    if (step > 1) {
      setIsAnimating(true);
      setTimeout(() => {
        setStep(prev => prev - 1);
        setIsAnimating(false);
      }, 300);
    } else {
      onBack();
    }
  }, [step, onBack]);

  const updateField = <K extends keyof UserAssessment>(field: K, value: UserAssessment[K]) => {
    setAssessment(prev => ({ ...prev, [field]: value }));
  };

  const technicalOptions: { value: TechnicalLevel; label: string; description: string; icon: string }[] = [
    { value: 'novice', label: 'Novice', description: 'New to programming, learning basics', icon: '🌱' },
    { value: 'beginner', label: 'Beginner', description: 'Know basics, built simple projects', icon: '🌿' },
    { value: 'intermediate', label: 'Intermediate', description: 'Comfortable with multiple languages', icon: '🌳' },
    { value: 'advanced', label: 'Advanced', description: 'Built production applications', icon: '🏗️' },
    { value: 'senior', label: 'Senior', description: 'Expert, can architect complex systems', icon: '🏛️' }
  ];

  const budgetOptions: { value: BudgetRange; label: string; range: string; icon: string }[] = [
    { value: 'bootstrapping', label: 'Bootstrapping', range: '$0 - $100/mo', icon: '💡' },
    { value: 'lean', label: 'Lean Startup', range: '$100 - $500/mo', icon: '🚀' },
    { value: 'moderate', label: 'Moderate', range: '$500 - $2,000/mo', icon: '📈' },
    { value: 'comfortable', label: 'Comfortable', range: '$2,000 - $10,000/mo', icon: '💼' },
    { value: 'scale', label: 'Scale Mode', range: '$10,000+/mo', icon: '🏢' }
  ];

  const timeOptions: { value: TimeCommitment; label: string; hours: string; icon: string }[] = [
    { value: 'minimal', label: 'Side Hustle', hours: '5-10 hrs/week', icon: '⏰' },
    { value: 'part-time', label: 'Part Time', hours: '10-20 hrs/week', icon: '🕐' },
    { value: 'significant', label: 'Significant', hours: '20-30 hrs/week', icon: '📅' },
    { value: 'full-time', label: 'Full Time', hours: '40+ hrs/week', icon: '💪' },
    { value: 'dedicated', label: 'All In', hours: '50+ hrs/week', icon: '🔥' }
  ];

  const nicheOptions: { value: NichePreference; label: string; icon: string }[] = [
    { value: 'fintech', label: 'Finance & Payments', icon: '💳' },
    { value: 'ecommerce', label: 'E-Commerce', icon: '🛒' },
    { value: 'content', label: 'Content & Media', icon: '📱' },
    { value: 'productivity', label: 'Productivity', icon: '⚡' },
    { value: 'gaming', label: 'Gaming & Entertainment', icon: '🎮' },
    { value: 'education', label: 'Education', icon: '📚' },
    { value: 'community', label: 'Community Management', icon: '👥' },
    { value: 'ai-tools', label: 'AI & Automation', icon: '🤖' },
    { value: 'any', label: 'Open to All', icon: '🌐' }
  ];

  const goalOptions = [
    { value: 'side-income', label: 'Side Income', target: '$500-2K/mo', icon: '💵' },
    { value: 'replace-salary', label: 'Replace Salary', target: '$5K-10K/mo', icon: '💰' },
    { value: 'build-business', label: 'Build Business', target: '$10K-50K/mo', icon: '🏢' },
    { value: 'scale-startup', label: 'Scale Startup', target: '$50K+/mo', icon: '🚀' }
  ];

  const isStepValid = (): boolean => {
    switch (step) {
      case 1: return !!assessment.technicalLevel;
      case 2: return !!assessment.budget;
      case 3: return !!assessment.timeCommitment;
      case 4: return assessment.nichePreferences.length > 0;
      case 5: return !!assessment.revenueGoal;
      default: return false;
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-4">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-3">Technical Proficiency</h2>
              <p className="text-purple-300">How would you rate your coding skills?</p>
            </div>
            <div className="grid gap-3">
              {technicalOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => updateField('technicalLevel', option.value)}
                  className={`w-full p-5 rounded-2xl border-2 transition-all duration-300 flex items-center gap-4 ${
                    assessment.technicalLevel === option.value
                      ? 'border-purple-500 bg-purple-500/20 scale-[1.02]'
                      : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
                  }`}
                >
                  <span className="text-3xl">{option.icon}</span>
                  <div className="text-left">
                    <div className="font-bold text-white text-lg">{option.label}</div>
                    <div className="text-purple-300 text-sm">{option.description}</div>
                  </div>
                  {assessment.technicalLevel === option.value && (
                    <div className="ml-auto w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-4">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-3">Monthly Budget</h2>
              <p className="text-purple-300">What can you invest monthly in infrastructure & tools?</p>
            </div>
            <div className="grid gap-3">
              {budgetOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => updateField('budget', option.value)}
                  className={`w-full p-5 rounded-2xl border-2 transition-all duration-300 flex items-center gap-4 ${
                    assessment.budget === option.value
                      ? 'border-purple-500 bg-purple-500/20 scale-[1.02]'
                      : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
                  }`}
                >
                  <span className="text-3xl">{option.icon}</span>
                  <div className="text-left flex-1">
                    <div className="font-bold text-white text-lg">{option.label}</div>
                    <div className="text-purple-300 text-sm">{option.range}</div>
                  </div>
                  {assessment.budget === option.value && (
                    <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-3">Time Commitment</h2>
              <p className="text-purple-300">How much time can you dedicate weekly?</p>
            </div>
            <div className="grid gap-3">
              {timeOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => updateField('timeCommitment', option.value)}
                  className={`w-full p-5 rounded-2xl border-2 transition-all duration-300 flex items-center gap-4 ${
                    assessment.timeCommitment === option.value
                      ? 'border-purple-500 bg-purple-500/20 scale-[1.02]'
                      : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
                  }`}
                >
                  <span className="text-3xl">{option.icon}</span>
                  <div className="text-left flex-1">
                    <div className="font-bold text-white text-lg">{option.label}</div>
                    <div className="text-purple-300 text-sm">{option.hours}</div>
                  </div>
                  {assessment.timeCommitment === option.value && (
                    <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-4">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-3">Niche Preferences</h2>
              <p className="text-purple-300">Select industries that interest you (multiple allowed)</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {nicheOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => {
                    const current = assessment.nichePreferences;
                    const updated = current.includes(option.value)
                      ? current.filter(n => n !== option.value)
                      : [...current, option.value];
                    updateField('nichePreferences', updated as NichePreference[]);
                  }}
                  className={`p-4 rounded-2xl border-2 transition-all duration-300 flex flex-col items-center gap-2 ${
                    assessment.nichePreferences.includes(option.value)
                      ? 'border-purple-500 bg-purple-500/20 scale-[1.02]'
                      : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
                  }`}
                >
                  <span className="text-3xl">{option.icon}</span>
                  <span className="text-white font-medium text-sm text-center">{option.label}</span>
                </button>
              ))}
            </div>
            <p className="text-center text-purple-400 text-sm mt-4">
              Selected: {assessment.nichePreferences.length} niche{assessment.nichePreferences.length !== 1 ? 's' : ''}
            </p>
          </div>
        );

      case 5:
        return (
          <div className="space-y-4">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-3">Revenue Goal</h2>
              <p className="text-purple-300">What's your target monthly income from this venture?</p>
            </div>
            <div className="grid gap-3">
              {goalOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => updateField('revenueGoal', option.value)}
                  className={`w-full p-5 rounded-2xl border-2 transition-all duration-300 flex items-center gap-4 ${
                    assessment.revenueGoal === option.value
                      ? 'border-purple-500 bg-purple-500/20 scale-[1.02]'
                      : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
                  }`}
                >
                  <span className="text-3xl">{option.icon}</span>
                  <div className="text-left flex-1">
                    <div className="font-bold text-white text-lg">{option.label}</div>
                    <div className="text-green-400 text-sm font-medium">{option.target}</div>
                  </div>
                  {assessment.revenueGoal === option.value && (
                    <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="p-6">
        <div className="container mx-auto flex justify-between items-center">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-purple-300 hover:text-white transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          
          {/* Progress */}
          <div className="flex items-center gap-3">
            <span className="text-purple-300 text-sm">Step {step} of {totalSteps}</span>
            <div className="w-32 h-2 bg-white/10 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-500"
                style={{ width: `${(step / totalSteps) * 100}%` }}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 flex items-center justify-center p-6">
        <div className={`w-full max-w-2xl transition-all duration-300 ${isAnimating ? 'opacity-0 translate-x-10' : 'opacity-100 translate-x-0'}`}>
          {renderStep()}
        </div>
      </main>

      {/* Footer */}
      <footer className="p-6">
        <div className="container mx-auto flex justify-end">
          <button
            onClick={handleNext}
            disabled={!isStepValid()}
            className={`px-8 py-4 rounded-2xl font-bold text-lg flex items-center gap-2 transition-all duration-300 ${
              isStepValid()
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:scale-105 shadow-lg shadow-purple-500/30'
                : 'bg-white/10 text-white/30 cursor-not-allowed'
            }`}
          >
            {step === totalSteps ? 'Get My Blueprints' : 'Continue'}
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </footer>
    </div>
  );
};

export default Assessment;
```

## 5. components/Dashboard.tsx

React

```
import React, { useState, useMemo } from 'react';
import { UserAssessment, BotBlueprint } from './types';
import BlueprintCard from './BlueprintCard';
import RevenueCalculator from './RevenueCalculator';
import RoadmapTimeline from './RoadmapTimeline';
import RiskMatrix from './RiskMatrix';
import ExportModal from './ExportModal';

interface DashboardProps {
  assessment: UserAssessment;
  blueprints: BotBlueprint[];
  onRestart: () => void;
}

type TabType = 'blueprints' | 'calculator' | 'roadmap' | 'risks';

const Dashboard: React.FC<DashboardProps> = ({ assessment, blueprints, onRestart }) => {
  const [activeTab, setActiveTab] = useState<TabType>('blueprints');
  const [selectedBlueprint, setSelectedBlueprint] = useState<BotBlueprint | null>(
    blueprints[0] || null
  );
  const [showExportModal, setShowExportModal] = useState(false);
  const [filterNiche, setFilterNiche] = useState<string>('all');

  const filteredBlueprints = useMemo(() => {
    if (filterNiche === 'all') return blueprints;
    return blueprints.filter(bp => bp.niche === filterNiche);
  }, [blueprints, filterNiche]);

  const uniqueNiches = useMemo(() => {
    const niches = new Set(blueprints.map(bp => bp.niche));
    return Array.from(niches);
  }, [blueprints]);

  const tabs = [
    { id: 'blueprints' as TabType, label: 'Blueprints', icon: '📋', count: filteredBlueprints.length },
    { id: 'calculator' as TabType, label: 'Revenue Calculator', icon: '💰' },
    { id: 'roadmap' as TabType, label: 'Roadmap', icon: '🗺️' },
    { id: 'risks' as TabType, label: 'Risk Analysis', icon: '⚠️' }
  ];

  const getProfileSummary = () => {
    const levelMap = { novice: 'Beginner', beginner: 'Developing', intermediate: 'Skilled', advanced: 'Expert', senior: 'Master' };
    const budgetMap = { bootstrapping: 'Minimal', lean: 'Lean', moderate: 'Moderate', comfortable: 'Solid', scale: 'Aggressive' };
    return {
      level: levelMap[assessment.technicalLevel] || 'Unknown',
      budget: budgetMap[assessment.budget] || 'Unknown',
      time: assessment.timeCommitment?.replace('-', ' ') || 'Unknown'
    };
  };

  const profile = getProfileSummary();

  return (
    <div className="min-h-screen pb-20">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <span className="text-3xl">💸</span>
                Your CashFlow Dashboard
              </h1>
              <p className="text-purple-300 text-sm mt-1">
                {filteredBlueprints.length} personalized blueprints based on your profile
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowExportModal(true)}
                className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl text-white text-sm font-medium transition-all flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Export
              </button>
              <button
                onClick={onRestart}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-xl text-white text-sm font-medium transition-all"
              >
                Retake Assessment
              </button>
            </div>
          </div>

          {/* Profile Summary */}
          <div className="flex flex-wrap gap-3 mt-4">
            <div className="bg-white/5 px-4 py-2 rounded-full flex items-center gap-2">
              <span className="text-purple-400 text-sm">Level:</span>
              <span className="text-white font-medium text-sm">{profile.level}</span>
            </div>
            <div className="bg-white/5 px-4 py-2 rounded-full flex items-center gap-2">
              <span className="text-purple-400 text-sm">Budget:</span>
              <span className="text-white font-medium text-sm">{profile.budget}</span>
            </div>
            <div className="bg-white/5 px-4 py-2 rounded-full flex items-center gap-2">
              <span className="text-purple-400 text-sm">Time:</span>
              <span className="text-white font-medium text-sm capitalize">{profile.time}</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="container mx-auto px-6">
          <div className="flex gap-1 overflow-x-auto pb-px">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 text-sm font-medium whitespace-nowrap transition-all relative flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'text-white'
                    : 'text-purple-300 hover:text-white'
                }`}
              >
                <span>{tab.icon}</span>
                {tab.label}
                {tab.count !== undefined && (
                  <span className="bg-purple-500 text-white text-xs px-2 py-0.5 rounded-full">
                    {tab.count}
                  </span>
                )}
                {activeTab === tab.id && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-purple-500 to-blue-500" />
                )}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-6 py-8">
        {activeTab === 'blueprints' && (
          <div className="space-y-6">
            {/* Filter */}
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setFilterNiche('all')}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  filterNiche === 'all'
                    ? 'bg-purple-500 text-white'
                    : 'bg-white/10 text-white hover:bg-white/20'
                }`}
              >
                All Niches
              </button>
              {uniqueNiches.map(niche => (
                <button
                  key={niche}
                  onClick={() => setFilterNiche(niche)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all capitalize ${
                    filterNiche === niche
                      ? 'bg-purple-500 text-white'
                      : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                >
                  {niche}
                </button>
              ))}
            </div>

            {/* Blueprint Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredBlueprints.map(blueprint => (
                <BlueprintCard
                  key={blueprint.id}
                  blueprint={blueprint}
                  isSelected={selectedBlueprint?.id === blueprint.id}
                  onSelect={() => setSelectedBlueprint(blueprint)}
                />
              ))}
            </div>

            {filteredBlueprints.length === 0 && (
              <div className="text-center py-16">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-bold text-white mb-2">No blueprints found</h3>
                <p className="text-purple-300">Try adjusting your filters or retaking the assessment</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'calculator' && selectedBlueprint && (
          <RevenueCalculator blueprint={selectedBlueprint} assessment={assessment} />
        )}

        {activeTab === 'roadmap' && selectedBlueprint && (
          <RoadmapTimeline blueprint={selectedBlueprint} assessment={assessment} />
        )}

        {activeTab === 'risks' && selectedBlueprint && (
          <RiskMatrix blueprint={selectedBlueprint} />
        )}

        {(activeTab !== 'blueprints' && !selectedBlueprint) && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">👆</div>
            <h3 className="text-xl font-bold text-white mb-2">Select a Blueprint First</h3>
            <p className="text-purple-300">Choose a blueprint from the Blueprints tab to see detailed analysis</p>
          </div>
        )}
      </main>

      {/* Export Modal */}
      {showExportModal && (
        <ExportModal
          assessment={assessment}
          blueprints={filteredBlueprints}
          selectedBlueprint={selectedBlueprint}
          onClose={() => setShowExportModal(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
```

## 6. components/BlueprintCard.tsx

React

```
import React, { useState } from 'react';
import { BotBlueprint } from './types';

interface BlueprintCardProps {
  blueprint: BotBlueprint;
  isSelected: boolean;
  onSelect: () => void;
}

const BlueprintCard: React.FC<BlueprintCardProps> = ({ blueprint, isSelected, onSelect }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-400 bg-green-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'hard': return 'text-orange-400 bg-orange-400/20';
      case 'expert': return 'text-red-400 bg-red-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const matchScore = (blueprint as any).matchScore || 0;

  return (
    <div
      className={`relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm rounded-3xl border-2 transition-all duration-300 overflow-hidden ${
        isSelected
          ? 'border-purple-500 shadow-2xl shadow-purple-500/20 scale-[1.02]'
          : 'border-white/10 hover:border-white/30'
      }`}
    >
      {/* Match Score Badge */}
      {matchScore > 0 && (
        <div className="absolute top-4 right-4 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-xs font-bold px-3 py-1 rounded-full">
          {matchScore}% Match
        </div>
      )}

      <div className="p-6">
        {/* Header */}
        <div className="flex items-start gap-4 mb-4">
          <div className="text-4xl">{blueprint.icon}</div>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-1">{blueprint.name}</h3>
            <div className="flex items-center gap-2">
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${getDifficultyColor(blueprint.difficulty)}`}>
                {blueprint.difficulty.toUpperCase()}
              </span>
              <span className="text-purple-300 text-xs capitalize">{blueprint.niche}</span>
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="text-purple-200 text-sm mb-4 line-clamp-2">{blueprint.description}</p>

        {/* Revenue & Timeline */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-white/5 rounded-xl p-3">
            <div className="text-purple-400 text-xs mb-1">Monthly Revenue</div>
            <div className="text-green-400 font-bold">
              {formatCurrency(blueprint.revenueModel.minMonthly)} - {formatCurrency(blueprint.revenueModel.maxMonthly)}
            </div>
          </div>
          <div className="bg-white/5 rounded-xl p-3">
            <div className="text-purple-400 text-xs mb-1">Time to MVP</div>
            <div className="text-white font-bold">{blueprint.timeline.mvp}</div>
          </div>
        </div>

        {/* Monetization */}
        <div className="flex flex-wrap gap-2 mb-4">
          {blueprint.revenueModel.monetization.slice(0, 3).map((method, index) => (
            <span
              key={index}
              className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded-full"
            >
              {method}
            </span>
          ))}
          {blueprint.revenueModel.monetization.length > 3 && (
            <span className="text-purple-400 text-xs">
              +{blueprint.revenueModel.monetization.length - 3} more
            </span>
          )}
        </div>

        {/* Expandable Details */}
        {isExpanded && (
          <div className="space-y-4 pt-4 border-t border-white/10">
            {/* Tech Stack */}
            <div>
              <h4 className="text-white font-medium mb-2">Tech Stack</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="text-purple-300">
                  <span className="text-purple-400">Backend:</span> {blueprint.techStack.backend}
                </div>
                <div className="text-purple-300">
                  <span className="text-purple-400">Database:</span> {blueprint.techStack.database}
                </div>
                <div className="text-purple-300">
                  <span className="text-purple-400">Hosting:</span> {blueprint.techStack.hosting}
                </div>
                <div className="text-purple-300">
                  <span className="text-purple-400">APIs:</span> {blueprint.techStack.apis?.join(', ')}
                </div>
              </div>
            </div>

            {/* MVP Features */}
            <div>
              <h4 className="text-white font-medium mb-2">MVP Features</h4>
              <ul className="space-y-1">
                {blueprint.mvpFeatures.map((feature, index) => (
                  <li key={index} className="text-purple-300 text-sm flex items-start gap-2">
                    <svg className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            {/* Startup Costs */}
            <div>
              <h4 className="text-white font-medium mb-2">Initial Investment</h4>
              <div className="text-2xl font-bold text-white">
                {formatCurrency(blueprint.costs.initial.min)} - {formatCurrency(blueprint.costs.initial.max)}
              </div>
              <div className="text-purple-400 text-sm">
                Monthly: {formatCurrency(blueprint.costs.monthly.min)} - {formatCurrency(blueprint.costs.monthly.max)}
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 mt-4">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex-1 py-3 bg-white/10 hover:bg-white/20 rounded-xl text-white font-medium transition-all text-sm"
          >
            {isExpanded ? 'Show Less' : 'View Details'}
          </button>
          <button
            onClick={onSelect}
            className={`flex-1 py-3 rounded-xl font-medium transition-all text-sm ${
              isSelected
                ? 'bg-purple-500 text-white'
                : 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:shadow-lg hover:shadow-purple-500/30'
            }`}
          >
            {isSelected ? '✓ Selected' : 'Select Blueprint'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BlueprintCard;
```

## 7. components/RevenueCalculator.tsx

React

```
import React, { useState, useMemo } from 'react';
import { BotBlueprint, UserAssessment } from './types';
import { calculateProjectedRevenue, calculateROI, calculateBreakeven } from './utils/calculations';

interface RevenueCalculatorProps {
  blueprint: BotBlueprint;
  assessment: UserAssessment;
}

const RevenueCalculator: React.FC<RevenueCalculatorProps> = ({ blueprint, assessment }) => {
  const [customUsers, setCustomUsers] = useState(1000);
  const [conversionRate, setConversionRate] = useState(5);
  const [avgPrice, setAvgPrice] = useState(blueprint.revenueModel.avgTicket || 10);
  const [growthRate, setGrowthRate] = useState(15);

  const projections = useMemo(() => {
    return calculateProjectedRevenue({
      users: customUsers,
      conversionRate: conversionRate / 100,
      averagePrice: avgPrice,
      monthlyGrowth: growthRate / 100,
      costs: blueprint.costs
    });
  }, [customUsers, conversionRate, avgPrice, growthRate, blueprint.costs]);

  const roi = useMemo(() => {
    return calculateROI(
      projections.yearOneRevenue,
      blueprint.costs.initial.max + (blueprint.costs.monthly.max * 12)
    );
  }, [projections, blueprint.costs]);

  const breakeven = useMemo(() => {
    return calculateBreakeven(
      blueprint.costs.initial.max,
      projections.monthlyRevenue[0],
      blueprint.costs.monthly.max
    );
  }, [blueprint.costs, projections]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-white mb-2">Revenue Calculator</h2>
        <p className="text-purple-300">
          Customize projections for <span className="text-white font-medium">{blueprint.name}</span>
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Input Controls */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <h3 className="text-white font-bold mb-6">Adjust Variables</h3>
            
            {/* Users Slider */}
            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <label className="text-purple-300 text-sm">Monthly Active Users</label>
                <span className="text-white font-bold">{customUsers.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min="100"
                max="100000"
                step="100"
                value={customUsers}
                onChange={(e) => setCustomUsers(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <div className="flex justify-between text-xs text-purple-400">
                <span>100</span>
                <span>100,000</span>
              </div>
            </div>

            {/* Conversion Rate */}
            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <label className="text-purple-300 text-sm">Conversion Rate</label>
                <span className="text-white font-bold">{conversionRate}%</span>
              </div>
              <input
                type="range"
                min="1"
                max="30"
                step="0.5"
                value={conversionRate}
                onChange={(e) => setConversionRate(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <div className="flex justify-between text-xs text-purple-400">
                <span>1%</span>
                <span>30%</span>
              </div>
            </div>

            {/* Average Price */}
            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <label className="text-purple-300 text-sm">Avg Transaction Value</label>
                <span className="text-white font-bold">${avgPrice}</span>
              </div>
              <input
                type="range"
                min="1"
                max="500"
                step="1"
                value={avgPrice}
                onChange={(e) => setAvgPrice(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <div className="flex justify-between text-xs text-purple-400">
                <span>$1</span>
                <span>$500</span>
              </div>
            </div>

            {/* Growth Rate */}
            <div className="space-y-3">
              <div className="flex justify-between">
                <label className="text-purple-300 text-sm">Monthly Growth Rate</label>
                <span className="text-white font-bold">{growthRate}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                step="1"
                value={growthRate}
                onChange={(e) => setGrowthRate(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <div className="flex justify-between text-xs text-purple-400">
                <span>0%</span>
                <span>50%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Projections */}
        <div className="lg:col-span-2 space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-2xl p-5 border border-green-500/20">
              <div className="text-green-400 text-sm mb-1">Month 1 Revenue</div>
              <div className="text-2xl font-bold text-white">{formatCurrency(projections.monthlyRevenue[0])}</div>
            </div>
            <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-2xl p-5 border border-blue-500/20">
              <div className="text-blue-400 text-sm mb-1">Year 1 Total</div>
              <div className="text-2xl font-bold text-white">{formatCurrency(projections.yearOneRevenue)}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-2xl p-5 border border-purple-500/20">
              <div className="text-purple-400 text-sm mb-1">ROI</div>
              <div className={`text-2xl font-bold ${roi > 0 ? 'text-green-400' : 'text-red-400'}`}>
                {roi > 0 ? '+' : ''}{roi.toFixed(0)}%
              </div>
            </div>
            <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 rounded-2xl p-5 border border-yellow-500/20">
              <div className="text-yellow-400 text-sm mb-1">Break-even</div>
              <div className="text-2xl font-bold text-white">
                {breakeven === Infinity ? 'N/A' : `${breakeven.toFixed(1)} mo`}
              </div>
            </div>
          </div>

          {/* Monthly Chart */}
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <h3 className="text-white font-bold mb-6">12-Month Revenue Projection</h3>
            <div className="h-64 flex items-end gap-2">
              {projections.monthlyRevenue.map((revenue, index) => {
                const maxRevenue = Math.max(...projections.monthlyRevenue);
                const height = (revenue / maxRevenue) * 100;
                return (
                  <div key={index} className="flex-1 flex flex-col items-center gap-2">
                    <div className="w-full relative group">
                      <div
                        className="w-full bg-gradient-to-t from-purple-600 to-blue-500 rounded-t-lg transition-all duration-300 group-hover:from-purple-500 group-hover:to-blue-400"
                        style={{ height: `${height}%`, minHeight: '4px' }}
                      />
                      <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-black/80 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        {formatCurrency(revenue)}
                      </div>
                    </div>
                    <span className="text-purple-400 text-xs">M{index + 1}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Profit Breakdown */}
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <h3 className="text-white font-bold mb-4">Year 1 Profit Breakdown</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-purple-300">Gross Revenue</span>
                <span className="text-green-400 font-bold">{formatCurrency(projections.yearOneRevenue)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-purple-300">Initial Investment</span>
                <span className="text-red-400 font-bold">-{formatCurrency(blueprint.costs.initial.max)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-purple-300">Annual Operating Costs</span>
                <span className="text-red-400 font-bold">-{formatCurrency(blueprint.costs.monthly.max * 12)}</span>
              </div>
              <div className="border-t border-white/10 pt-4 flex justify-between items-center">
                <span className="text-white font-bold">Net Profit (Year 1)</span>
                <span className={`text-xl font-bold ${projections.yearOneProfit > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {formatCurrency(projections.yearOneProfit)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RevenueCalculator;
```

## 8. components/RoadmapTimeline.tsx

React

```
import React, { useState } from 'react';
import { BotBlueprint, UserAssessment } from './types';

interface RoadmapTimelineProps {
  blueprint: BotBlueprint;
  assessment: UserAssessment;
}

interface Phase {
  id: number;
  name: string;
  duration: string;
  tasks: string[];
  deliverables: string[];
  resources: string[];
}

const RoadmapTimeline: React.FC<RoadmapTimelineProps> = ({ blueprint, assessment }) => {
  const [activePhase, setActivePhase] = useState(0);

  const getTimeMultiplier = () => {
    switch (assessment.technicalLevel) {
      case 'novice': return 2;
      case 'beginner': return 1.5;
      case 'intermediate': return 1;
      case 'advanced': return 0.8;
      case 'senior': return 0.6;
      default: return 1;
    }
  };

  const adjustDuration = (baseDuration: string): string => {
    const multiplier = getTimeMultiplier();
    const match = baseDuration.match(/(\d+)/);
    if (match) {
      const adjustedWeeks = Math.ceil(parseInt(match[1]) * multiplier);
      return baseDuration.replace(/\d+/, adjustedWeeks.toString());
    }
    return baseDuration;
  };

  const phases: Phase[] = [
    {
      id: 1,
      name: 'Research & Planning',
      duration: adjustDuration('1 week'),
      tasks: [
        'Market research and competitor analysis',
        'Define target audience personas',
        'Document technical requirements',
        'Create wireframes and user flow',
        'Set up project management tools'
      ],
      deliverables: ['Market Analysis Report', 'Technical Spec Document', 'Wireframes'],
      resources: ['Notion/Trello', 'Figma/Excalidraw', 'ChatGPT for research']
    },
    {
      id: 2,
      name: 'Environment Setup',
      duration: adjustDuration('1 week'),
      tasks: [
        `Set up ${blueprint.techStack.backend} development environment`,
        `Configure ${blueprint.techStack.database} database`,
        'Create Telegram Bot via BotFather',
        'Set up version control (Git)',
        'Configure hosting environment'
      ],
      deliverables: ['Development Environment', 'Bot Token', 'Git Repository'],
      resources: blueprint.techStack.apis || ['Telegram Bot API', 'Deployment Platform']
    },
    {
      id: 3,
      name: 'MVP Development',
      duration: adjustDuration(blueprint.timeline.mvp),
      tasks: [
        'Implement core bot commands',
        ...blueprint.mvpFeatures.slice(0, 4).map(f => `Build: ${f}`),
        'Integrate payment processing',
        'Implement user authentication'
      ],
      deliverables: ['Working Bot MVP', 'Payment Integration', 'User System'],
      resources: ['IDE', 'API Documentation', 'Testing Tools']
    },
    {
      id: 4,
      name: 'Testing & QA',
      duration: adjustDuration('1-2 weeks'),
      tasks: [
        'Unit testing all core functions',
        'Integration testing with Telegram API',
        'Security audit and vulnerability testing',
        'Performance optimization',
        'Beta testing with selected users'
      ],
      deliverables: ['Test Reports', 'Bug Fixes', 'Performance Metrics'],
      resources: ['Testing Frameworks', 'Beta Testers', 'Monitoring Tools']
    },
    {
      id: 5,
      name: 'Launch & Marketing',
      duration: adjustDuration('2 weeks'),
      tasks: [
        'Prepare launch materials',
        'Set up analytics tracking',
        'Create Telegram channel for updates',
        'Submit to bot directories',
        'Execute initial marketing campaign'
      ],
      deliverables: ['Live Bot', 'Marketing Materials', 'Analytics Dashboard'],
      resources: ['Social Media', 'Bot Directories', 'Analytics Platforms']
    },
    {
      id: 6,
      name: 'Growth & Iteration',
      duration: 'Ongoing',
      tasks: [
        'Monitor user feedback and metrics',
        'Implement feature requests',
        'A/B test pricing strategies',
        'Scale infrastructure as needed',
        'Build community and partnerships'
      ],
      deliverables: ['Feature Updates', 'Growth Reports', 'Community'],
      resources: ['User Feedback Tools', 'Analytics', 'Community Platforms']
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-white mb-2">Development Roadmap</h2>
        <p className="text-purple-300">
          Personalized timeline for <span className="text-white font-medium">{blueprint.name}</span>
        </p>
        <p className="text-purple-400 text-sm mt-2">
          ⏱️ Adjusted for your skill level: <span className="text-white capitalize">{assessment.technicalLevel}</span>
        </p>
      </div>

      {/* Timeline */}
      <div className="relative">
        {/* Progress Line */}
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-blue-500 to-purple-500" />

        {/* Phases */}
        <div className="space-y-6">
          {phases.map((phase, index) => (
            <div
              key={phase.id}
              className={`relative pl-20 transition-all duration-300 ${
                activePhase === index ? 'scale-[1.02]' : ''
              }`}
            >
              {/* Phase Indicator */}
              <div
                onClick={() => setActivePhase(index)}
                className={`absolute left-4 w-8 h-8 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 ${
                  activePhase === index
                    ? 'bg-gradient-to-r from-purple-500 to-blue-500 scale-125 shadow-lg shadow-purple-500/50'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                <span className="text-white font-bold text-sm">{phase.id}</span>
              </div>

              {/* Phase Card */}
              <div
                className={`bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm rounded-2xl border-2 overflow-hidden transition-all duration-300 ${
                  activePhase === index
                    ? 'border-purple-500 shadow-2xl shadow-purple-500/10'
                    : 'border-white/10 hover:border-white/20'
                }`}
              >
                {/* Phase Header */}
                <div
                  onClick={() => setActivePhase(index)}
                  className="p-6 cursor-pointer"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-1">{phase.name}</h3>
                      <div className="flex items-center gap-3">
                        <span className="text-purple-400 text-sm">⏱️ {phase.duration}</span>
                        <span className="text-purple-400 text-sm">📋 {phase.tasks.length} tasks</span>
                      </div>
                    </div>
                    <svg
                      className={`w-6 h-6 text-purple-400 transition-transform duration-300 ${
                        activePhase === index ? 'rotate-180' : ''
                      }`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>

                {/* Phase Details */}
                {activePhase === index && (
                  <div className="px-6 pb-6 space-y-6 border-t border-white/10 pt-6">
                    {/* Tasks */}
                    <div>
                      <h4 className="text-white font-medium mb-3 flex items-center gap-2">
                        <span>📝</span> Tasks
                      </h4>
                      <ul className="space-y-2">
                        {phase.tasks.map((task, idx) => (
                          <li key={idx} className="flex items-start gap-3 text-purple-200">
                            <div className="w-5 h-5 rounded-full border-2 border-purple-500/50 flex-shrink-0 mt-0.5" />
                            <span>{task}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Deliverables */}
                    <div>
                      <h4 className="text-white font-medium mb-3 flex items-center gap-2">
                        <span>📦</span> Deliverables
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {phase.deliverables.map((deliverable, idx) => (
                          <span
                            key={idx}
                            className="bg-green-500/20 text-green-300 text-sm px-3 py-1 rounded-full"
                          >
                            {deliverable}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Resources */}
                    <div>
                      <h4 className="text-white font-medium mb-3 flex items-center gap-2">
                        <span>🔧</span> Resources Needed
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {phase.resources.map((resource, idx) => (
                          <span
                            key={idx}
                            className="bg-blue-500/20 text-blue-300 text-sm px-3 py-1 rounded-full"
                          >
                            {resource}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30">
        <h3 className="text-xl font-bold text-white mb-4">📊 Timeline Summary</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">{adjustDuration(blueprint.timeline.mvp)}</div>
            <div className="text-purple-300">To MVP Launch</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">{adjustDuration(blueprint.timeline.fullProduct)}</div>
            <div className="text-purple-300">To Full Product</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">{adjustDuration(blueprint.timeline.profitability)}</div>
            <div className="text-purple-300">To Profitability</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoadmapTimeline;
```

## 9. components/RiskMatrix.tsx

React

```
import React, { useState } from 'react';
import { BotBlueprint } from './types';

interface RiskMatrixProps {
  blueprint: BotBlueprint;
}

interface Risk {
  id: string;
  category: 'technical' | 'market' | 'financial' | 'operational';
  name: string;
  description: string;
  likelihood: number; // 1-5
  impact: number; // 1-5
  mitigation: string[];
}

const RiskMatrix: React.FC<RiskMatrixProps> = ({ blueprint }) => {
  const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null);
  const [viewMode, setViewMode] = useState<'matrix' | 'list'>('matrix');

  const generateRisks = (): Risk[] => {
    const baseRisks: Risk[] = [
      {
        id: 'tech-1',
        category: 'technical',
        name: 'API Rate Limiting',
        description: 'Telegram API has rate limits that could affect high-volume operations',
        likelihood: 3,
        impact: 4,
        mitigation: [
          'Implement request queuing and throttling',
          'Use webhook instead of polling for efficiency',
          'Cache frequently accessed data',
          'Monitor API usage metrics'
        ]
      },
      {
        id: 'tech-2',
        category: 'technical',
        name: 'Scalability Issues',
        description: 'System may not handle rapid user growth efficiently',
        likelihood: blueprint.difficulty === 'expert' ? 2 : 4,
        impact: 4,
        mitigation: [
          'Design with horizontal scaling in mind',
          'Use cloud auto-scaling features',
          'Implement efficient database indexing',
          'Use caching layers (Redis)'
        ]
      },
      {
        id: 'market-1',
        category: 'market',
        name: 'Competition',
        description: 'Similar bots may capture market share',
        likelihood: 4,
        impact: 3,
        mitigation: [
          'Focus on unique value proposition',
          'Build strong community and brand',
          'Iterate quickly based on feedback',
          'Consider niche specialization'
        ]
      },
      {
        id: 'market-2',
        category: 'market',
        name: 'Platform Dependency',
        description: 'Complete reliance on Telegram platform policies',
        likelihood: 2,
        impact: 5,
        mitigation: [
          'Stay updated on Telegram ToS changes',
          'Build email list as backup communication',
          'Consider multi-platform presence',
          'Maintain compliant operations'
        ]
      },
      {
        id: 'fin-1',
        category: 'financial',
        name: 'Payment Processing Issues',
        description: 'Payment gateway problems or fraud could affect revenue',
        likelihood: 3,
        impact: 4,
        mitigation: [
          'Use established payment processors',
          'Implement fraud detection',
          'Have backup payment methods',
          'Maintain reserve funds'
        ]
      },
      {
        id: 'fin-2',
        category: 'financial',
        name: 'Low Conversion Rate',
        description: 'Users may not convert to paid customers as expected',
        likelihood: 3,
        impact: 4,
        mitigation: [
          'A/B test pricing strategies',
          'Offer freemium tier',
          'Improve onboarding experience',
          'Gather user feedback regularly'
        ]
      },
      {
        id: 'ops-1',
        category: 'operational',
        name: 'Downtime & Reliability',
        description: 'Service outages could damage reputation and revenue',
        likelihood: 3,
        impact: 4,
        mitigation: [
          'Implement monitoring and alerting',
          'Use reliable hosting providers',
          'Set up auto-recovery mechanisms',
          'Maintain incident response procedures'
        ]
      },
      {
        id: 'ops-2',
        category: 'operational',
        name: 'Data Security Breach',
        description: 'User data could be compromised',
        likelihood: 2,
        impact: 5,
        mitigation: [
          'Encrypt sensitive data at rest and in transit',
          'Regular security audits',
          'Minimal data collection policy',
          'Implement proper access controls'
        ]
      }
    ];

    return baseRisks;
  };

  const risks = generateRisks();

  const getRiskLevel = (risk: Risk): 'low' | 'medium' | 'high' | 'critical' => {
    const score = risk.likelihood * risk.impact;
    if (score <= 6) return 'low';
    if (score <= 12) return 'medium';
    if (score <= 18) return 'high';
    return 'critical';
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'medium': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'high': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      case 'critical': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'technical': return '⚙️';
      case 'market': return '📊';
      case 'financial': return '💰';
      case 'operational': return '🔧';
      default: return '📌';
    }
  };

  const risksByCategory = risks.reduce((acc, risk) => {
    if (!acc[risk.category]) acc[risk.category] = [];
    acc[risk.category].push(risk);
    return acc;
  }, {} as Record<string, Risk[]>);

  const overallRiskScore = Math.round(
    risks.reduce((sum, risk) => sum + (risk.likelihood * risk.impact), 0) / risks.length
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-white mb-2">Risk Analysis</h2>
        <p className="text-purple-300">
          Professional risk assessment for <span className="text-white font-medium">{blueprint.name}</span>
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-2xl p-5 border border-green-500/20">
          <div className="text-green-400 text-sm mb-1">Low Risk</div>
          <div className="text-2xl font-bold text-white">
            {risks.filter(r => getRiskLevel(r) === 'low').length}
          </div>
        </div>
        <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 rounded-2xl p-5 border border-yellow-500/20">
          <div className="text-yellow-400 text-sm mb-1">Medium Risk</div>
          <div className="text-2xl font-bold text-white">
            {risks.filter(r => getRiskLevel(r) === 'medium').length}
          </div>
        </div>
        <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/10 rounded-2xl p-5 border border-orange-500/20">
          <div className="text-orange-400 text-sm mb-1">High Risk</div>
          <div className="text-2xl font-bold text-white">
            {risks.filter(r => getRiskLevel(r) === 'high').length}
          </div>
        </div>
        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-2xl p-5 border border-purple-500/20">
          <div className="text-purple-400 text-sm mb-1">Overall Score</div>
          <div className="text-2xl font-bold text-white">{overallRiskScore}/25</div>
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex justify-center gap-2">
        <button
          onClick={() => setViewMode('matrix')}
          className={`px-4 py-2 rounded-lg font-medium transition-all ${
            viewMode === 'matrix'
              ? 'bg-purple-500 text-white'
              : 'bg-white/10 text-white hover:bg-white/20'
          }`}
        >
          Matrix View
        </button>
        <button
          onClick={() => setViewMode('list')}
          className={`px-4 py-2 rounded-lg font-medium transition-all ${
            viewMode === 'list'
              ? 'bg-purple-500 text-white'
              : 'bg-white/10 text-white hover:bg-white/20'
          }`}
        >
          List View
        </button>
      </div>

      {viewMode === 'matrix' ? (
        /* Risk Matrix Grid */
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
          <div className="flex">
            {/* Y-Axis Label */}
            <div className="w-20 flex flex-col justify-center items-center">
              <span className="text-purple-400 text-sm transform -rotate-90 whitespace-nowrap">
                ← Impact →
              </span>
            </div>
            
            {/* Matrix */}
            <div className="flex-1">
              <div className="grid grid-cols-5 gap-2">
                {[5, 4, 3, 2, 1].map(impact => (
                  <React.Fragment key={`impact-${impact}`}>
                    {[1, 2, 3, 4, 5].map(likelihood => {
                      const cellRisks = risks.filter(
                        r => r.likelihood === likelihood && r.impact === impact
                      );
                      const score = likelihood * impact;
                      let bgColor = 'bg-green-500/20';
                      if (score > 6) bgColor = 'bg-yellow-500/20';
                      if (score > 12) bgColor = 'bg-orange-500/20';
                      if (score > 18) bgColor = 'bg-red-500/20';

                      return (
                        <div
                          key={`${likelihood}-${impact}`}
                          className={`aspect-square ${bgColor} rounded-lg flex flex-col items-center justify-center p-2 relative cursor-pointer hover:scale-105 transition-transform`}
                          onClick={() => cellRisks.length > 0 && setSelectedRisk(cellRisks[0])}
                        >
                          {cellRisks.length > 0 && (
                            <>
                              <span className="text-2xl">{getCategoryIcon(cellRisks[0].category)}</span>
                              {cellRisks.length > 1 && (
                                <span className="absolute -top-1 -right-1 bg-purple-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                                  {cellRisks.length}
                                </span>
                              )}
                            </>
                          )}
                        </div>
                      );
                    })}
                  </React.Fragment>
                ))}
              </div>
              
              {/* X-Axis Label */}
              <div className="text-center mt-4">
                <span className="text-purple-400 text-sm">← Likelihood →</span>
              </div>
            </div>
          </div>
          
          {/* Legend */}
          <div className="flex justify-center gap-4 mt-6 pt-4 border-t border-white/10">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-500/40 rounded" />
              <span className="text-purple-300 text-sm">Low</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-yellow-500/40 rounded" />
              <span className="text-purple-300 text-sm">Medium</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-orange-500/40 rounded" />
              <span className="text-purple-300 text-sm">High</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-red-500/40 rounded" />
              <span className="text-purple-300 text-sm">Critical</span>
            </div>
          </div>
        </div>
      ) : (
        /* List View */
        <div className="space-y-6">
          {Object.entries(risksByCategory).map(([category, categoryRisks]) => (
            <div key={category} className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 capitalize">
                <span>{getCategoryIcon(category)}</span>
                {category} Risks
              </h3>
              <div className="space-y-4">
                {categoryRisks.map(risk => (
                  <div
                    key={risk.id}
                    onClick={() => setSelectedRisk(risk)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all hover:scale-[1.01] ${getRiskColor(getRiskLevel(risk))}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-bold text-white">{risk.name}</h4>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${getRiskColor(getRiskLevel(risk))}`}>
                        {getRiskLevel(risk).toUpperCase()}
                      </span>
                    </div>
                    <p className="text-purple-300 text-sm">{risk.description}</p>
                    <div className="flex gap-4 mt-2 text-sm">
                      <span className="text-purple-400">Likelihood: {risk.likelihood}/5</span>
                      <span className="text-purple-400">Impact: {risk.impact}/5</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Risk Detail Modal */}
      {selectedRisk && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setSelectedRisk(null)}>
          <div
            className="bg-gradient-to-br from-slate-900 to-purple-900 rounded-3xl p-8 max-w-lg w-full border border-purple-500/30"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-6">
              <div>
                <span className="text-3xl mb-2 block">{getCategoryIcon(selectedRisk.category)}</span>
                <h3 className="text-2xl font-bold text-white">{selectedRisk.name}</h3>
                <span className={`inline-block mt-2 text-xs font-medium px-3 py-1 rounded-full ${getRiskColor(getRiskLevel(selectedRisk))}`}>
                  {getRiskLevel(selectedRisk).toUpperCase()} RISK
                </span>
              </div>
              <button
                onClick={() => setSelectedRisk(null)}
                className="text-purple-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <p className="text-purple-200 mb-6">{selectedRisk.description}</p>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-white/5 rounded-xl p-4 text-center">
                <div className="text-purple-400 text-sm mb-1">Likelihood</div>
                <div className="text-2xl font-bold text-white">{selectedRisk.likelihood}/5</div>
              </div>
              <div className="bg-white/5 rounded-xl p-4 text-center">
                <div className="text-purple-400 text-sm mb-1">Impact</div>
                <div className="text-2xl font-bold text-white">{selectedRisk.impact}/5</div>
              </div>
            </div>

            <div>
              <h4 className="text-white font-bold mb-3">🛡️ Mitigation Strategies</h4>
              <ul className="space-y-2">
                {selectedRisk.mitigation.map((strategy, idx) => (
                  <li key={idx} className="flex items-start gap-3 text-purple-200">
                    <svg className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {strategy}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskMatrix;
```

## 10. components/ExportModal.tsx

React

```
import React, { useState } from 'react';
import { UserAssessment, BotBlueprint } from './types';

interface ExportModalProps {
  assessment: UserAssessment;
  blueprints: BotBlueprint[];
  selectedBlueprint: BotBlueprint | null;
  onClose: () => void;
}

type ExportFormat = 'pdf' | 'markdown' | 'json' | 'notion';

const ExportModal: React.FC<ExportModalProps> = ({ assessment, blueprints, selectedBlueprint, onClose }) => {
  const [exportFormat, setExportFormat] = useState<ExportFormat>('markdown');
  const [includeOptions, setIncludeOptions] = useState({
    assessment: true,
    blueprints: true,
    techStack: true,
    roadmap: true,
    risks: true,
    financials: true
  });
  const [isExporting, setIsExporting] = useState(false);
  const [exportComplete, setExportComplete] = useState(false);

  const formatOptions: { id: ExportFormat; label: string; icon: string; description: string }[] = [
    { id: 'markdown', label: 'Markdown', icon: '📝', description: 'Clean, readable format for docs' },
    { id: 'json', label: 'JSON', icon: '🔧', description: 'Machine-readable data format' },
    { id: 'pdf', label: 'PDF Report', icon: '📄', description: 'Professional document (coming soon)' },
    { id: 'notion', label: 'Notion', icon: '📓', description: 'Copy to Notion (coming soon)' }
  ];

  const generateMarkdown = (): string => {
    const lines: string[] = [];
    
    lines.push('# CashFlow Architect - Business Blueprint Report');
    lines.push(`\n*Generated on ${new Date().toLocaleDateString()}*\n`);

    if (includeOptions.assessment) {
      lines.push('## 📊 Your Profile Assessment\n');
      lines.push(`- **Technical Level:** ${assessment.technicalLevel}`);
      lines.push(`- **Budget:** ${assessment.budget}`);
      lines.push(`- **Time Commitment:** ${assessment.timeCommitment}`);
      lines.push(`- **Revenue Goal:** ${assessment.revenueGoal}`);
      lines.push(`- **Preferred Niches:** ${assessment.nichePreferences.join(', ')}\n`);
    }

    if (includeOptions.blueprints && selectedBlueprint) {
      const bp = selectedBlueprint;
      lines.push('## 🎯 Selected Blueprint\n');
      lines.push(`### ${bp.icon} ${bp.name}\n`);
      lines.push(`${bp.description}\n`);
      lines.push(`- **Difficulty:** ${bp.difficulty}`);
      lines.push(`- **Niche:** ${bp.niche}`);
      lines.push(`- **Time to MVP:** ${bp.timeline.mvp}`);
      lines.push(`- **Revenue Potential:** $${bp.revenueModel.minMonthly} - $${bp.revenueModel.maxMonthly}/month\n`);

      if (includeOptions.techStack) {
        lines.push('### 🛠️ Tech Stack\n');
        lines.push(`- **Backend:** ${bp.techStack.backend}`);
        lines.push(`- **Database:** ${bp.techStack.database}`);
        lines.push(`- **Hosting:** ${bp.techStack.hosting}`);
        if (bp.techStack.frontend) lines.push(`- **Frontend:** ${bp.techStack.frontend}`);
        if (bp.techStack.apis) lines.push(`- **APIs:** ${bp.techStack.apis.join(', ')}`);
        lines.push('');
      }

      lines.push('### 📋 MVP Features\n');
      bp.mvpFeatures.forEach(feature => {
        lines.push(`- [ ] ${feature}`);
      });
      lines.push('');

      if (includeOptions.financials) {
        lines.push('### 💰 Financial Overview\n');
        lines.push(`- **Initial Investment:** $${bp.costs.initial.min} - $${bp.costs.initial.max}`);
        lines.push(`- **Monthly Costs:** $${bp.costs.monthly.min} - $${bp.costs.monthly.max}`);
        lines.push(`- **Time to Profitability:** ${bp.timeline.profitability}\n`);
        lines.push('**Monetization Strategies:**');
        bp.revenueModel.monetization.forEach(method => {
          lines.push(`- ${method}`);
        });
        lines.push('');
      }

      if (includeOptions.roadmap) {
        lines.push('### 🗺️ Development Timeline\n');
        lines.push(`1. **MVP Launch:** ${bp.timeline.mvp}`);
        lines.push(`2. **Full Product:** ${bp.timeline.fullProduct}`);
        lines.push(`3. **Profitability:** ${bp.timeline.profitability}`);
        lines.push('');
      }

      if (includeOptions.risks) {
        lines.push('### ⚠️ 
```

Something went wrong with this response, please try again.

├── index.html  
├── index.tsx  
├── App.tsx  
├── types.ts  
├── constants.ts  
├── components/  
│ ├── Landing.tsx  
│ ├── Assessment.tsx  
│ ├── Dashboard.tsx  
│ ├── BlueprintCard.tsx  
│ ├── RevenueCalculator.tsx  
│ ├── RoadmapTimeline.tsx  
│ ├── RiskMatrix.tsx  
│ └── ExportModal.tsx  
├── hooks/  
│ ├── useAssessment.ts  
│ └── useAnalytics.ts  
├── utils/  
│ ├── calculations.ts  
│ └── storage.ts  
└── metadata.json

THATS THE ROOT OF THE APP IM BUILDING. I HAVE already "index.html" , "types.ts" and "constants.ts". create the rest of the codes for this app a sophisticated monetizing and publish ready .

This application, titled "CashFlow Architect," serves as an interactive business strategy and technical planning tool for entrepreneurs and developers looking to build profitable businesses on the Telegram platform.  
Its specific purposes are:  
Resource Assessment: It evaluates the user's specific constraints through a 3-step intake form, asking about Technical Proficiency (Novice to Senior), Budget (Bootstrapping to Scale), and Time Commitment.  
Tailored Recommendations: Based on the assessment, it filters and recommends specific "Bot Blueprints" (business models) that match the user's profile (e.g., suggesting a simple "Lead Gen Bot" for a novice with a low budget, or a "SaaS Service" for an advanced dev with capital).  
Technical & Business Strategy: For each recommended model, it provides a comprehensive Blueprint containing:  
Tech Stack: Specific frontend, backend, database, and infrastructure choices.  
Revenue Modeling: How to monetize (subscriptions, fees, etc.) and estimated potential income.  
MVP Features: The core features needed for a Minimum Viable Product.  
Risk Analysis: A professional assessment of technical and market risks.  
Essentially, it acts as an automated consultant that bridges the gap between technical implementation and business strategy for the Telegram ecosystem.  
User  
whats the project root structure  
Gemini 3 Pro Preview  
Ran for 28s  
lightbulb  
Thought for 28 seconds  
Based on the code provided, the project has a flat directory structure. All files reside in the root directory (conceptually acting as the src folder).  
Here is the file structure:  
index.html - The entry HTML file that loads the React app.  
index.tsx - The entry point for the React code (mounts App to the DOM).  
App.tsx - The main application component containing the routing logic (Landing vs. Assessment vs. Dashboard).  
types.ts - TypeScript definitions for user assessments and bot blueprints.  
constants.ts - Static data containing the list of Bot Blueprints and their details.  
metadata.json - Configuration file for app permissions and description.

IMPROVE THISAPP TO A REAL CASHFLOW FINDER. A SOPHISTICATED MONETIZING READY APP. IM BULDING IT INSIDE BUILD WITH GEMINI.