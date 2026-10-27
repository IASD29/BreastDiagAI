import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

/**
 * Système de Thème BreastDiagAI :
 * 2 modes : 'light' (Clair, par défaut) et 'dark' (Nuit).
 * Mémorisation persistante dans localStorage et application via :
 * - Attribut HTML data-theme="light" | "dark"
 * - Classe CSS .dark
 */
const STORAGE_KEY = 'bdai-theme';

const ThemeContext = createContext({
  theme: 'light',
  isDark: false,
  toggleTheme: () => {},
  setTheme: () => {},
});

export const useTheme = () => useContext(ThemeContext);

export function ThemeProvider({ children }) {
  // Mode par défaut : 'light' (Clair)
  const [theme, setThemeState] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'dark' || saved === 'light') {
        return saved;
      }
    } catch (e) {
      /* localStorage inaccessible */
    }
    return 'light';
  });

  // Application synchrone sur l'élément racine
  const applyThemeToDOM = useCallback((newTheme) => {
    const root = document.documentElement;
    root.setAttribute('data-theme', newTheme);
    if (newTheme === 'dark') {
      root.classList.add('dark');
      root.style.colorScheme = 'dark';
    } else {
      root.classList.remove('dark');
      root.style.colorScheme = 'light';
    }
  }, []);

  useEffect(() => {
    applyThemeToDOM(theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}
  }, [theme, applyThemeToDOM]);

  const toggleTheme = useCallback(() => {
    setThemeState((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const setTheme = useCallback((targetTheme) => {
    if (targetTheme === 'dark' || targetTheme === 'light') {
      setThemeState(targetTheme);
    }
  }, []);

  const isDark = theme === 'dark';

  return (
    <ThemeContext.Provider value={{ theme, isDark, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
