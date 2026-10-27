import React, { useState } from 'react';
import { 
  Home, 
  HeartHandshake, 
  Stethoscope, 
  History, 
  BarChart3, 
  Menu, 
  X,
  Sparkles
} from 'lucide-react';
import ribbonSvg from '../assets/ribbon.svg';

export default function Navbar({ activeTab, setActiveTab, isBackendOnline }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Accueil', icon: Home },
    { id: 'story', label: 'Notre Histoire', icon: HeartHandshake, badge: 'Humain' },
    { id: 'predict', label: 'Diagnostic IA', icon: Stethoscope },
    { id: 'history', label: 'Historique', icon: History },
    { id: 'analytics', label: 'Analyse & EDA', icon: BarChart3 },
  ];

  const handleNavClick = (id) => {
    setActiveTab(id);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-pink-100 shadow-sm transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo & Octobre Rose Branding */}
          <div 
            onClick={() => handleNavClick('home')}
            className="flex items-center gap-3.5 cursor-pointer group select-none"
          >
            <div className="relative w-10 h-12 flex-shrink-0 transition-transform group-hover:scale-105 duration-300">
              <img 
                src={ribbonSvg} 
                alt="Ruban Rose Octobre Rose" 
                className="w-full h-full object-contain filter drop-shadow-sm" 
              />
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-xl sm:text-2xl font-extrabold tracking-tight bg-gradient-to-r from-octobre-800 via-octobre-600 to-pink-600 bg-clip-text text-transparent">
                  BreastDiag<span className="text-pink-500 font-black">AI</span>
                </span>
                <span className="hidden sm:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-pink-100/80 text-pink-800 border border-pink-200">
                  <span className="w-1.5 h-1.5 rounded-full bg-pink-500 animate-pulse"></span>
                  Octobre Rose 🎗️
                </span>
              </div>
              <span className="text-[11px] font-medium text-slate-500 tracking-wide">
                Aide au diagnostic précoce • Centré sur l'humain
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1.5 lg:gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`relative flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-pink-600 to-octobre-600 text-white shadow-md shadow-pink-200'
                      : 'text-slate-600 hover:text-pink-600 hover:bg-pink-50/80'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-pink-500'}`} />
                  <span>{item.label}</span>
                  {item.badge && !isActive && (
                    <span className="px-1.5 py-0.2 text-[10px] uppercase font-bold tracking-wider rounded bg-pink-100 text-pink-700">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Status & CTA */}
          <div className="hidden lg:flex items-center gap-3">
            <div 
              title={isBackendOnline ? 'Serveur FastAPI connecté' : 'Vérification du serveur en cours...'}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${
                isBackendOnline 
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
                  : 'bg-amber-50 text-amber-700 border-amber-200'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${isBackendOnline ? 'bg-emerald-500' : 'bg-amber-400 animate-ping'}`} />
              <span>{isBackendOnline ? 'API Active' : 'API En attente'}</span>
            </div>

            <button
              onClick={() => handleNavClick('predict')}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-bold bg-octobre-soft text-pink-700 hover:bg-pink-100 border border-pink-200 transition-colors shadow-sm"
            >
              <Sparkles className="w-4 h-4 text-pink-500" />
              <span>Tester l'IA</span>
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-slate-600 hover:text-pink-600 hover:bg-pink-50 focus:outline-none"
              aria-label="Menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white/95 backdrop-blur-md border-b border-pink-100 px-4 pt-2 pb-4 space-y-1 shadow-lg animate-in slide-in-from-top-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-4 py-3 rounded-xl text-sm font-semibold transition-colors ${
                  isActive
                    ? 'bg-gradient-to-r from-pink-600 to-octobre-600 text-white'
                    : 'text-slate-700 hover:bg-pink-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                    isActive ? 'bg-white/20 text-white' : 'bg-pink-100 text-pink-700'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
          
          <div className="pt-2 border-t border-pink-100 flex items-center justify-between px-2 text-xs text-slate-500">
            <span>État de l'API :</span>
            <span className={isBackendOnline ? 'text-emerald-600 font-semibold' : 'text-amber-600 font-semibold'}>
              {isBackendOnline ? 'Connectée (FastAPI)' : 'Hors-ligne / Démarrage'}
            </span>
          </div>
        </div>
      )}
    </header>
  );
}
