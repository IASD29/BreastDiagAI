import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MobileNav from './components/MobileNav';
import Footer from './components/Footer';
import Home from './pages/Home';
import OurStory from './pages/OurStory';
import Predict from './pages/Predict';
import History from './pages/History';
import Analytics from './pages/Analytics';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [isBackendOnline, setIsBackendOnline] = useState(false);

  // Vérifier la connexion avec le backend FastAPI
  useEffect(() => {
    let isMounted = true;
    
    const checkConnection = async () => {
      const online = await api.checkHealth();
      if (isMounted) setIsBackendOnline(online);
    };

    checkConnection();
    const interval = setInterval(checkConnection, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-bg text-text transition-colors duration-200">
      
      {/* Barre de navigation mobile (< md) */}
      <MobileNav activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Barre latérale à gauche (>= md) avec bascule Clair / Nuit */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        isBackendOnline={isBackendOnline} 
      />

      {/* Zone de contenu principale à droite */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen overflow-x-hidden">
        
        {/* Contenu de la page sélectionnée */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-10 py-6 sm:py-8">
          {activeTab === 'home' && <Home setActiveTab={setActiveTab} />}
          {activeTab === 'story' && <OurStory setActiveTab={setActiveTab} />}
          {activeTab === 'predict' && <Predict setActiveTab={setActiveTab} />}
          {activeTab === 'history' && <History setActiveTab={setActiveTab} />}
          {activeTab === 'analytics' && <Analytics />}
        </main>

        {/* Pied de page adapté au mode sombre */}
        <Footer setActiveTab={setActiveTab} />
      </div>

    </div>
  );
}
