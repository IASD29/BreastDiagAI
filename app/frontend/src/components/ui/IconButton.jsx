import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * Composant IconButton réutilisable & accessible
 * 
 * Props :
 * @param {React.ComponentType | React.ReactNode} icon - Icône Lucide
 * @param {string} label - Titre et aria-label obligatoires pour l'accessibilité
 * @param {'default' | 'primary' | 'danger' | 'ghost' | 'success'} variant - Thème visuel
 * @param {'sm' | 'md' | 'lg'} size - Taille du bouton
 * @param {boolean} loading - Affiche un loader à la place de l'icône
 * @param {boolean} disabled - Désactivation
 */
export default function IconButton({
  icon: Icon,
  label,
  variant = 'default',
  size = 'md',
  loading = false,
  disabled = false,
  className = '',
  onClick,
  type = 'button',
  ...props
}) {
  const isDisabled = disabled || loading;

  const sizeStyles = {
    sm: 'w-8 h-8 rounded-lg',
    md: 'w-9 h-9 rounded-xl',
    lg: 'w-11 h-11 rounded-2xl',
  };

  const iconSizes = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  const variantStyles = {
    default: `
      bg-surface text-text-muted
      border border-border
      hover:text-text hover:bg-surface-2 hover:border-primary/40
      shadow-xs hover:shadow-theme
    `,
    primary: `
      bg-primary-light text-primary
      border border-primary-border
      hover:bg-primary hover:text-white
      shadow-[0_2px_10px_rgba(219,39,119,0.2)]
      hover:shadow-[0_4px_16px_rgba(219,39,119,0.4)]
    `,
    danger: `
      bg-danger-bg text-danger
      border border-danger-border
      hover:bg-danger hover:text-white
      shadow-[0_2px_10px_rgba(239,68,68,0.2)]
      hover:shadow-[0_4px_16px_rgba(239,68,68,0.4)]
    `,
    success: `
      bg-success-bg text-success
      border border-success-border
      hover:bg-success hover:text-white
      shadow-[0_2px_10px_rgba(16,185,129,0.2)]
      hover:shadow-[0_4px_16px_rgba(16,185,129,0.4)]
    `,
    ghost: `
      bg-transparent text-text-muted
      border border-transparent
      hover:text-text hover:bg-surface-2
    `,
  };

  return (
    <button
      type={type}
      onClick={isDisabled ? undefined : onClick}
      disabled={isDisabled}
      aria-label={label}
      title={label}
      aria-busy={loading}
      className={`
        group relative inline-flex items-center justify-center select-none
        btn-motion-spring
        ${sizeStyles[size]}
        ${variantStyles[variant]}
        ${isDisabled
          ? 'opacity-40 cursor-not-allowed transform-none pointer-events-none'
          : 'hover:-translate-y-0.5 active:translate-y-0.5 active:scale-[0.92] cursor-pointer'
        }
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-bg
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <Loader2 className={`${iconSizes[size]} animate-spin-smooth`} />
      ) : React.isValidElement(Icon) ? (
        <span className="transition-transform duration-200 group-hover:scale-110 group-hover:rotate-6">
          {Icon}
        </span>
      ) : Icon ? (
        <Icon className={`${iconSizes[size]} transition-transform duration-200 group-hover:scale-110 group-hover:rotate-6`} />
      ) : null}
    </button>
  );
}
