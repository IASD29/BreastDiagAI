import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * Composant Button Motion & UI/UX Design System
 * 
 * Props :
 * @param {'primary' | 'secondary' | 'ghost' | 'danger' | 'success'} variant - Style visuel
 * @param {'sm' | 'md' | 'lg'} size - Taille et espacements
 * @param {React.ComponentType | React.ReactNode} icon - Icône Lucide ou nœud React
 * @param {'left' | 'right'} iconPosition - Position de l'icône
 * @param {boolean} loading - État de chargement avec spinner animé
 * @param {boolean} disabled - Désactivation
 * @param {boolean} shine - Active l'effet de reflet lumineux au hover (par défaut true pour primary)
 */
export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'left',
  loading = false,
  disabled = false,
  shine,
  className = '',
  type = 'button',
  onClick,
  ...props
}) {
  const isShineActive = shine !== undefined ? shine : variant === 'primary';
  const isDisabled = disabled || loading;

  // ── Tailles & Paddings généreux ──
  const sizeStyles = {
    sm: 'text-xs px-3.5 py-1.5 rounded-xl gap-1.5 font-medium min-h-[34px]',
    md: 'text-sm px-5 py-2.5 rounded-xl gap-2 font-semibold min-h-[42px]',
    lg: 'text-base px-7 py-3.5 rounded-2xl gap-2.5 font-bold min-h-[50px]',
  };

  const iconSizes = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  // ── Variantes visuelles (Glow, Glassmorphism, Dégradés) ──
  const variantStyles = {
    primary: `
      bg-gradient-to-r from-pink-600 via-rose-600 to-pink-500
      hover:from-pink-500 hover:via-rose-500 hover:to-pink-600
      text-white
      shadow-[0_4px_14px_0_rgba(219,39,119,0.3)]
      hover:shadow-[0_8px_25px_-2px_rgba(219,39,119,0.5)]
      border border-white/20
      dark:bg-gradient-to-r dark:from-pink-500 dark:via-rose-500 dark:to-pink-400
      dark:text-[#0f0a12]
      dark:shadow-[0_4px_16px_0_rgba(244,114,182,0.35)]
      dark:hover:shadow-[0_8px_28px_0_rgba(244,114,182,0.55)]
    `,
    secondary: `
      bg-surface text-text
      border border-border hover:border-primary/50
      hover:bg-surface-2
      shadow-theme hover:shadow-theme-lg
      hover:text-primary
      backdrop-blur-md
    `,
    ghost: `
      bg-transparent text-text-muted
      hover:text-text hover:bg-surface-2
      border border-transparent hover:border-border/60
    `,
    danger: `
      bg-danger text-white
      hover:bg-danger/90
      shadow-[0_4px_14px_0_rgba(239,68,68,0.3)]
      hover:shadow-[0_8px_25px_-2px_rgba(239,68,68,0.5)]
      border border-white/10
    `,
    success: `
      bg-success text-white
      hover:bg-success/90
      shadow-[0_4px_14px_0_rgba(16,185,129,0.3)]
      hover:shadow-[0_8px_25px_-2px_rgba(16,185,129,0.5)]
      border border-white/10
    `,
  };

  // Rendu de l'icône avec micro-interaction spring
  const renderIcon = () => {
    if (loading) {
      return <Loader2 className={`${iconSizes[size]} animate-spin-smooth shrink-0`} />;
    }
    if (!Icon) return null;

    if (React.isValidElement(Icon)) {
      return (
        <span className="shrink-0 transition-transform duration-200 group-hover:scale-110 group-hover:-rotate-3">
          {Icon}
        </span>
      );
    }

    const IconComponent = Icon;
    return (
      <IconComponent
        className={`${iconSizes[size]} shrink-0 transition-transform duration-200 group-hover:scale-110 group-hover:-rotate-3`}
      />
    );
  };

  return (
    <button
      type={type}
      onClick={isDisabled ? undefined : onClick}
      disabled={isDisabled}
      aria-busy={loading}
      className={`
        group relative inline-flex items-center justify-center select-none
        btn-motion-spring ${isShineActive ? 'btn-shine-container' : ''}
        ${sizeStyles[size]}
        ${variantStyles[variant]}
        ${isDisabled
          ? 'opacity-55 cursor-not-allowed transform-none shadow-none pointer-events-none'
          : 'hover:-translate-y-0.5 active:translate-y-0.5 active:scale-[0.96] cursor-pointer'
        }
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-bg
        ${className}
      `}
      {...props}
    >
      {/* Effet reflet lumineux (Shine) */}
      {isShineActive && !isDisabled && <span className="btn-shine-effect" />}

      {/* Icône à gauche */}
      {iconPosition === 'left' && renderIcon()}

      {/* Contenu textuel */}
      <span className={`inline-flex items-center truncate ${loading ? 'opacity-80' : ''}`}>
        {children}
      </span>

      {/* Icône à droite */}
      {iconPosition === 'right' && renderIcon()}
    </button>
  );
}
