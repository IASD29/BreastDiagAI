import React, { useEffect } from 'react';
import { X, CheckCircle2, AlertTriangle, Info } from 'lucide-react';

// ─── Skeleton Loader ────────────────────────────────────────────────────────
export function Skeleton({ className = '' }) {
  return <div className={`skeleton ${className}`} />;
}

export function SkeletonCard() {
  return (
    <div className="card p-5 space-y-3 animate-fade-in border border-border">
      <Skeleton className="h-4 w-1/3 bg-surface-2" />
      <Skeleton className="h-8 w-1/2 bg-surface-2" />
      <Skeleton className="h-3 w-2/3 bg-surface-2" />
    </div>
  );
}

// ─── Jauge circulaire de confiance animée ───────────────────────────────────
export function ConfidenceRing({ value = 0, label = '', color = 'var(--primary)', size = 120 }) {
  const r = 44;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-1 animate-fade-up">
      <div className="relative" style={{ width: size, height: size }}>
        {/* SVG ring */}
        <svg width={size} height={size} viewBox="0 0 100 100" className="-rotate-90">
          {/* Rail de fond */}
          <circle cx="50" cy="50" r={r} fill="none" stroke="currentColor"
            strokeWidth="8" className="text-border" />
          {/* Progression colorée */}
          <circle cx="50" cy="50" r={r} fill="none" stroke={color}
            strokeWidth="8" strokeLinecap="round"
            strokeDasharray={circ}
            strokeDashoffset={offset}
            style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.22,1,0.36,1)' }}
          />
        </svg>
        {/* Texte centré en superposition absolue */}
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-0.5">
          <span className="text-2xl font-bold tracking-tight leading-none" style={{ color }}>
            {value}%
          </span>
          {label && (
            <span className="text-[10px] font-medium leading-none text-center px-1" style={{ color: 'var(--text-muted)' }}>
              {label}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Toast Notification ─────────────────────────────────────────────────────
const toastIcons = {
  success: <CheckCircle2 className="w-4 h-4 text-success shrink-0" />,
  error:   <AlertTriangle className="w-4 h-4 text-danger shrink-0" />,
  info:    <Info className="w-4 h-4 text-primary shrink-0" />,
};

export function Toast({ message, type = 'info', onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 4000);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-fade-up">
      <div className="glass flex items-center gap-3 px-4 py-3 shadow-theme min-w-[260px] max-w-sm rounded-2xl border border-border">
        {toastIcons[type]}
        <p className="text-sm text-text flex-1">{message}</p>
        <button onClick={onClose} className="text-text-muted hover:text-text transition-colors">
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}

// ─── Dot Loader ─────────────────────────────────────────────────────────────
export function DotLoader() {
  return (
    <div className="flex items-center gap-1.5">
      {[0, 1, 2].map(i => (
        <span key={i}
          className="w-2 h-2 rounded-full bg-primary animate-bounce-dot"
          style={{ animationDelay: `${i * 0.16}s` }}
        />
      ))}
    </div>
  );
}

// ─── Empty State ─────────────────────────────────────────────────────────────
export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4 animate-fade-in text-center">
      <div className="p-4 rounded-2xl bg-primary-light text-primary border border-primary-border">
        <Icon className="w-8 h-8" />
      </div>
      <div>
        <h3 className="font-semibold text-text">{title}</h3>
        {description && <p className="text-sm text-text-muted mt-1">{description}</p>}
      </div>
      {action}
    </div>
  );
}

// ─── Section Header ──────────────────────────────────────────────────────────
export function SectionHeader({ eyebrow, title, description }) {
  return (
    <div className="space-y-1 animate-fade-up">
      {eyebrow && (
        <span className="text-xs font-semibold uppercase tracking-widest text-primary">
          {eyebrow}
        </span>
      )}
      <h2 className="text-2xl font-bold tracking-tight text-text">
        {title}
      </h2>
      {description && (
        <p className="text-sm text-text-muted leading-relaxed max-w-xl">
          {description}
        </p>
      )}
    </div>
  );
}

// ─── Stat Card ───────────────────────────────────────────────────────────────
export function StatCard({ label, value, sub, icon: Icon, accent = 'brand' }) {
  const accents = {
    brand:   'text-primary bg-primary-light border-primary-border',
    emerald: 'text-success bg-success-bg border-success-border',
    rose:    'text-danger bg-danger-bg border-danger-border',
    sky:     'text-info bg-info-bg border-info-border',
  };

  return (
    <div className="card p-5 flex items-start justify-between gap-4 animate-fade-up hover:shadow-theme-lg transition-base border border-border">
      <div className="space-y-1 min-w-0">
        <p className="text-xs font-medium text-text-muted uppercase tracking-wider">{label}</p>
        <p className="text-2xl font-bold tracking-tight text-text truncate">{value}</p>
        {sub && <p className="text-xs text-text-dim">{sub}</p>}
      </div>
      {Icon && (
        <div className={`p-2.5 rounded-xl shrink-0 border ${accents[accent] || accents.brand}`}>
          <Icon className="w-5 h-5" />
        </div>
      )}
    </div>
  );
}

// ─── Medical Disclaimer ──────────────────────────────────────────────────────
export function MedicalDisclaimer({ compact = false }) {
  if (compact) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-700 dark:text-amber-300 text-xs font-medium">
        <AlertTriangle className="w-3.5 h-3.5 shrink-0 text-amber-600 dark:text-amber-400" />
        <span>Outil d'aide à la décision — ne remplace pas l'avis d'un médecin</span>
      </div>
    );
  }
  return (
    <div className="flex items-start gap-3 p-4 rounded-2xl bg-amber-500/[0.06] border border-amber-500/25 animate-fade-in">
      <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
      <div>
        <p className="text-sm font-semibold text-amber-800 dark:text-amber-300">Avertissement médical</p>
        <p className="text-xs text-text-muted mt-0.5 leading-relaxed">
          BreastDiagAI est un outil académique d'aide à la décision. Les résultats ne constituent pas un diagnostic médical officiel. Consultez toujours un professionnel de santé qualifié.
        </p>
      </div>
    </div>
  );
}
