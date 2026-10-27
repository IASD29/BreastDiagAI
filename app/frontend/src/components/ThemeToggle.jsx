import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

/**
 * Bouton unique de bascule binaire :
 * - Mode Clair (Soleil)
 * - Mode Nuit (Lune)
 */
export default function ThemeToggle({ compact = false }) {
  const { isDark, toggleTheme } = useTheme();

  if (compact) {
    return (
      <button
        onClick={toggleTheme}
        type="button"
        aria-label={isDark ? 'Passer en mode clair' : 'Passer en mode nuit'}
        title={isDark ? 'Passer en mode clair' : 'Passer en mode nuit'}
        className="p-2 rounded-xl text-white/70 hover:text-white hover:bg-white/10 active:scale-95 transition-all duration-200 border border-white/10 flex items-center justify-center"
      >
        {isDark ? (
          <Sun className="w-4 h-4 text-amber-300 transition-transform duration-300 rotate-0 hover:rotate-45" />
        ) : (
          <Moon className="w-4 h-4 text-pink-300 transition-transform duration-300 -rotate-12 hover:rotate-0" />
        )}
      </button>
    );
  }

  return (
    <button
      onClick={toggleTheme}
      type="button"
      className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl border border-white/10 bg-white/[0.04] hover:bg-white/[0.08] active:scale-[0.99] transition-all duration-200 text-left group"
      title={isDark ? 'Passer en mode clair' : 'Passer en mode nuit'}
    >
      <div className="flex items-center gap-2.5">
        <div className={`p-1.5 rounded-lg transition-colors ${
          isDark ? 'bg-amber-400/15 text-amber-300' : 'bg-pink-400/15 text-pink-300'
        }`}>
          {isDark ? (
            <Sun className="w-4 h-4 transition-transform duration-300 group-hover:rotate-45" />
          ) : (
            <Moon className="w-4 h-4 transition-transform duration-300 group-hover:-rotate-12" />
          )}
        </div>
        <div className="flex flex-col">
          <span className="text-xs font-semibold text-white/90">
            {isDark ? 'Mode Nuit' : 'Mode Clair'}
          </span>
          <span className="text-[10px] text-white/40">
            {isDark ? 'Thème sombre actif' : 'Thème clair actif'}
          </span>
        </div>
      </div>

      {/* Switch visuel */}
      <div className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-200 flex items-center ${
        isDark ? 'bg-pink-600 justify-end' : 'bg-white/20 justify-start'
      }`}>
        <div className="w-4 h-4 rounded-full bg-white shadow-xs" />
      </div>
    </button>
  );
}
