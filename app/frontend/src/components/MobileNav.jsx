import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import ribbonSvg from '../assets/ribbon.svg';

const NAV = [
  { id: 'home',      label: 'Accueil' },
  { id: 'predict',   label: 'Diagnostic' },
  { id: 'story',     label: 'Notre Histoire' },
  { id: 'history',   label: 'Historique' },
  { id: 'analytics', label: 'Stats & EDA' },
];

export default function MobileNav({ activeTab, setActiveTab }) {
  const [open, setOpen] = useState(false);

  const go = (id) => {
    setActiveTab(id);
    setOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <>
      {/* Barre supérieure mobile */}
      <header className="md:hidden sticky top-0 z-40 h-14 flex items-center justify-between px-4
                         bg-[var(--sidebar-bg)] backdrop-blur-md border-b border-white/10 shadow-sm">
        <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => go('home')}>
          <img src={ribbonSvg} alt="ribbon" className="w-6 h-6" />
          <span className="text-sm font-semibold text-white">
            BreastDiag<span className="text-pink-400">AI</span>
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Bouton unique Soleil/Lune dans le header */}
          <ThemeToggle compact={true} />

          {/* Bouton Menu Burger */}
          <button
            onClick={() => setOpen(o => !o)}
            className="p-2 rounded-xl text-white/70 hover:text-white hover:bg-white/10 transition-colors border border-white/10"
            aria-label="Menu de navigation"
          >
            {open ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {/* Tiroir de navigation mobile (Drawer) */}
      {open && (
        <div
          className="md:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs animate-fade-in"
          onClick={() => setOpen(false)}
        >
          <div
            className="absolute top-14 left-0 right-0 bg-[var(--sidebar-bg)] border-b border-white/10 p-4 space-y-4 shadow-2xl"
            onClick={e => e.stopPropagation()}
          >
            <div className="space-y-1">
              {NAV.map(({ id, label }) => (
                <button
                  key={id}
                  onClick={() => go(id)}
                  className={`w-full text-left px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    activeTab === id
                      ? 'bg-white/15 text-white font-semibold'
                      : 'text-white/60 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>

            {/* Sélecteur de thème étendu dans le drawer */}
            <div className="pt-3 border-t border-white/10">
              <ThemeToggle compact={false} />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
