import React, { useState } from 'react';
import {
  Home, Stethoscope, History, BarChart3, HeartHandshake,
  ChevronLeft, ChevronRight, ShieldCheck
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import ribbonSvg from '../assets/ribbon.svg';

const NAV = [
  { id: 'home',      label: 'Accueil',        icon: Home,           sub: 'Vue générale' },
  { id: 'predict',   label: 'Diagnostic IA',  icon: Stethoscope,    sub: 'Nouvelle analyse' },
  { id: 'story',     label: 'Notre Histoire', icon: HeartHandshake, sub: 'Genèse du projet' },
  { id: 'history',   label: 'Historique',     icon: History,        sub: 'Analyses passées' },
  { id: 'analytics', label: 'Statistiques',   icon: BarChart3,      sub: 'Données & graphiques' },
];

export default function Sidebar({ activeTab, setActiveTab }) {
  const [collapsed, setCollapsed] = useState(false);

  const go = (id) => {
    setActiveTab(id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <aside
      className={`
        hidden md:flex flex-col h-screen sticky top-0 shrink-0
        bg-[var(--sidebar-bg)] border-r border-[var(--sidebar-border)]
        transition-all duration-300 ease-in-out z-30 shadow-lg
        ${collapsed ? 'w-[72px]' : 'w-[230px]'}
      `}
    >
      {/* ── Logo ── */}
      <div
        className="flex items-center gap-3 px-4 h-16 border-b border-white/5 cursor-pointer select-none"
        onClick={() => go('home')}
      >
        <img
          src={ribbonSvg}
          alt="ribbon"
          className="w-7 h-7 shrink-0 transition-transform duration-200 hover:scale-110"
        />
        {!collapsed && (
          <div className="animate-fade-in min-w-0">
            <p className="text-sm font-semibold text-white leading-none truncate">
              BreastDiag<span className="text-pink-400">AI</span>
            </p>
            <p className="text-[10px] text-white/40 mt-0.5 truncate">Octobre Rose 🎗️</p>
          </div>
        )}
      </div>

      {/* ── Navigation ── */}
      <nav className="flex-1 py-4 px-2 space-y-0.5 overflow-y-auto no-scrollbar">
        {!collapsed && (
          <p className="px-3 mb-2 text-[10px] font-semibold uppercase tracking-widest text-white/30">
            Navigation
          </p>
        )}
        {NAV.map(({ id, label, icon: Icon, sub }) => {
          const active = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => go(id)}
              title={collapsed ? label : undefined}
              className={`
                w-full flex items-center gap-3 rounded-xl px-3 py-2.5 text-left
                transition-all duration-150 group relative
                ${active
                  ? 'bg-white/15 text-white font-medium shadow-xs'
                  : 'text-white/60 hover:text-white hover:bg-white/5'}
              `}
            >
              {/* Active indicator */}
              {active && (
                <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 rounded-r-full bg-pink-400" />
              )}

              <Icon className={`w-4 h-4 shrink-0 transition-colors ${active ? 'text-pink-300' : 'text-white/60'}`} />

              {!collapsed && (
                <div className="min-w-0 animate-fade-in">
                  <p className="text-xs font-medium leading-none truncate">{label}</p>
                  <p className={`text-[10px] mt-0.5 truncate ${active ? 'text-pink-200/80' : 'text-white/30'}`}>
                    {sub}
                  </p>
                </div>
              )}
            </button>
          );
        })}
      </nav>

      {/* ── Section basse : Bascule Thème Clair / Nuit ── */}
      <div className="px-3 pb-4 space-y-3 border-t border-white/5 pt-3">
        {/* Bouton unique Soleil / Lune */}
        <ThemeToggle compact={collapsed} />

        {/* Bouton de réduction */}
        <button
          onClick={() => setCollapsed(c => !c)}
          title={collapsed ? "Agrandir le menu" : "Réduire le menu"}
          className="w-full flex items-center justify-center gap-2 rounded-xl py-2 px-2.5
                     text-white/40 hover:text-white/80 hover:bg-white/5 transition-all text-xs"
        >
          {collapsed
            ? <ChevronRight className="w-4 h-4 shrink-0" />
            : <>
                <ChevronLeft className="w-4 h-4 shrink-0" />
                <span className="text-[11px] font-medium">Réduire le menu</span>
              </>
          }
        </button>

        {/* Badge médical éthique */}
        {!collapsed && (
          <div className="px-3 py-2.5 rounded-xl bg-white/[0.03] border border-white/5 animate-fade-in">
            <div className="flex items-center gap-1.5 text-white/50 text-[10px]">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400/80 shrink-0" />
              <span className="font-medium">Aide à la décision</span>
            </div>
            <p className="text-[9px] text-white/30 mt-1 leading-relaxed">
              Ne remplace pas l'avis d'un professionnel de santé
            </p>
          </div>
        )}
      </div>
    </aside>
  );
}
