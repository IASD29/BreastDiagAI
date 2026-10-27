import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

export default function MedicalDisclaimer({ compact = false }) {
  if (compact) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/25 text-amber-700 dark:text-amber-300 text-xs font-medium">
        <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
        <span>Outil d'aide à la décision • Ne remplace pas l'avis d'un professionnel de santé</span>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-amber-500/25 bg-amber-500/[0.05] p-4.5 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="p-2 bg-amber-500/15 rounded-xl text-amber-600 dark:text-amber-400 shrink-0 mt-0.5">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h4 className="text-sm font-bold text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
            Avertissement Médical et Déontologique
          </h4>
          <p className="text-xs text-text-muted mt-1 leading-relaxed">
            <strong>BreastDiagAI</strong> est un système d'aide à l'évaluation diagnostique basé sur le Machine Learning à des fins académiques et d'assistance. 
            Les résultats obtenus ne constituent en aucun cas une prescription ou un avis médical officiel. 
            Seul un médecin spécialiste (oncologue, radiologue, gynécologue) après mammographie, échographie ou biopsie est habilité à poser un diagnostic définitif.
          </p>
        </div>
      </div>
    </div>
  );
}
