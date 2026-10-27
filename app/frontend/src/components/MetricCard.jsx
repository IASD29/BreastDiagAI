import React from 'react';

/**
 * Carte de métrique KPI avec adaptation complète au thème (Clair / Nuit)
 * Utilise les variables CSS centralisées : var(--surface), var(--border), var(--text), etc.
 */
export default function MetricCard({ title, value, subtitle, icon: Icon, color = 'pink', badge }) {
  const colorStyles = {
    pink: {
      border: 'border-primary-border',
      iconBg: 'bg-primary-light text-primary',
      value: 'text-primary',
    },
    emerald: {
      border: 'border-success-border',
      iconBg: 'bg-success-bg text-success',
      value: 'text-success',
    },
    rose: {
      border: 'border-danger-border',
      iconBg: 'bg-danger-bg text-danger',
      value: 'text-danger',
    },
    blue: {
      border: 'border-info-border',
      iconBg: 'bg-info-bg text-info',
      value: 'text-info',
    },
  };

  const style = colorStyles[color] || colorStyles.pink;

  return (
    <div className={`card p-6 flex flex-col justify-between transition-all duration-300 hover:shadow-theme-lg border ${style.border}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
          {title}
        </span>
        {Icon && (
          <div className={`p-2.5 rounded-xl ${style.iconBg} shrink-0`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-4">
        <div className="flex items-baseline gap-2">
          <span className={`text-3xl font-extrabold tracking-tight ${style.value}`}>
            {value}
          </span>
          {badge && (
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-surface-2 text-text-muted border border-border">
              {badge}
            </span>
          )}
        </div>
        {subtitle && (
          <p className="text-xs text-text-muted mt-1 font-medium">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}
