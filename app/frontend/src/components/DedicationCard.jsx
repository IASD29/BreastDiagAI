import React from 'react';
import { Heart } from 'lucide-react';
import ribbonSvg from '../assets/ribbon.svg';

/**
 * ============================================================================
 * NOTE DE CONFIDENTIALITÉ & ÉTHIQUE (CONTENU SENSIBLE) :
 * Ce composant rend hommage à Attig Rania, source d'inspiration humaine
 * fondamentale derrière le projet BreastDiagAI.
 * 
 * Tout ajustement, diffusion étendue, modification du libellé ou ajout
 * d'informations personnelles requiert obligatoirement le consentement formel,
 * éclairé et préalable de la personne concernée et de sa famille.
 * ============================================================================
 */

export default function DedicationCard({ className = '' }) {
  return (
    <aside
      role="region"
      aria-label="Dédicace et hommage"
      className={`
        relative overflow-hidden rounded-3xl p-7 sm:p-9
        bg-gradient-to-br from-rose-50/70 via-surface to-pink-50/40
        dark:from-[#1d1322] dark:via-surface dark:to-[#170f1c]
        border border-primary-border/60
        shadow-[0_4px_24px_rgba(190,24,93,0.06)] dark:shadow-[0_4px_24px_rgba(0,0,0,0.35)]
        animate-fade-up transition-all duration-300
        ${className}
      `}
    >
      {/* Ruban symbolique en filigrane très doux (non intrusif) */}
      <img
        src={ribbonSvg}
        alt=""
        aria-hidden="true"
        className="pointer-events-none select-none absolute -right-6 -bottom-8 w-44 h-48 opacity-[0.045] dark:opacity-[0.06] transform -rotate-12"
      />

      <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center gap-5 sm:gap-7">
        
        {/* Médaillon discret avec cœur solidaire */}
        <div
          className="shrink-0 p-3.5 rounded-2xl bg-primary-light border border-primary-border text-primary shadow-xs"
          aria-hidden="true"
        >
          <Heart className="w-6 h-6 fill-primary/20 text-primary" />
        </div>

        {/* Message d'hommage doux et digne */}
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-widest text-primary">
              Dédicace
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-primary/40" />
            <span className="text-xs text-text-muted font-medium">
              Une histoire humaine
            </span>
          </div>

          <p className="font-serif italic text-base sm:text-lg text-text leading-relaxed">
            « Dédié avec respect et affection à <strong className="font-semibold text-primary not-italic">Attig Rania</strong>, dont le parcours a donné une âme et un sens profond à BreastDiagAI. Pour elle, et pour toutes les mères. »
          </p>

          <p className="text-xs text-text-dim leading-normal pt-0.5">
            Témoignage de gratitude et d’engagement fraternel de toute l’équipe.
          </p>
        </div>

      </div>
    </aside>
  );
}
