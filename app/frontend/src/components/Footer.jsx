import React from 'react';
import { Heart, Ribbon, ShieldCheck } from 'lucide-react';
import ribbonSvg from '../assets/ribbon.svg';

export default function Footer({ setActiveTab }) {
  return (
    <footer className="mt-16 border-t border-border bg-surface text-text-muted transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Col 1 : Vision & Projet */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <img src={ribbonSvg} alt="Ruban Rose" className="w-6 h-8 object-contain" />
              <span className="text-xl font-bold text-primary">
                BreastDiagAI
              </span>
            </div>
            <p className="text-sm leading-relaxed max-w-md text-text-muted">
              Outil académique d'aide à la décision diagnostique pour le cancer du sein, 
              conçu pour allier la puissance du Machine Learning à la chaleur et la sensibilité de l'accompagnement humain.
            </p>
            <div className="p-3 bg-surface-2 rounded-xl border border-border shadow-xs flex items-center gap-3 max-w-md">
              <Ribbon className="w-5 h-5 text-primary shrink-0" />
              <p className="text-xs text-text font-medium">
                Soutien indéfectible à la campagne <strong>Octobre Rose</strong> pour le dépistage précoce.
              </p>
            </div>
          </div>

          {/* Col 2 : Liens rapides */}
          <div>
            <h4 className="text-xs font-bold text-text tracking-wider uppercase mb-3">
              Navigation
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <button onClick={() => { setActiveTab('home'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="hover:text-primary transition-colors">
                  Accueil & Sensibilisation
                </button>
              </li>
              <li>
                <button onClick={() => { setActiveTab('story'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="hover:text-primary transition-colors">
                  Notre Histoire
                </button>
              </li>
              <li>
                <button onClick={() => { setActiveTab('predict'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="hover:text-primary transition-colors">
                  Diagnostic Prédictif
                </button>
              </li>
              <li>
                <button onClick={() => { setActiveTab('history'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="hover:text-primary transition-colors">
                  Historique des Analyses
                </button>
              </li>
              <li>
                <button onClick={() => { setActiveTab('analytics'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="hover:text-primary transition-colors">
                  Analyses & Visualisations EDA
                </button>
              </li>
            </ul>
          </div>

          {/* Col 3 : Cadre éthique */}
          <div>
            <h4 className="text-xs font-bold text-text tracking-wider uppercase mb-3">
              Cadre & Déontologie
            </h4>
            <div className="space-y-3 text-xs leading-relaxed text-text-muted">
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-success shrink-0 mt-0.5" />
                <span className="text-text font-medium">Projet académique fondé sur le dataset Wisconsin (WDBC).</span>
              </div>
              <p>
                Ce système ne constitue pas un dispositif médical certifié et ne pose aucun acte médical direct.
              </p>
            </div>
          </div>

        </div>

        <div className="mt-10 pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between text-xs text-text-muted gap-4">
          <p>© {new Date().getFullYear()} BreastDiagAI • Projet Académique • Tous droits réservés.</p>
          <p className="flex items-center gap-1.5">
            Conçu avec <Heart className="w-3.5 h-3.5 text-primary fill-primary" /> pour toutes les mères, sœurs et proches
          </p>
        </div>
      </div>
    </footer>
  );
}
