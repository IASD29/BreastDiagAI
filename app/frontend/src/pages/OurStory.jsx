import React from 'react';
import { 
  HeartHandshake, 
  Quote, 
  ShieldCheck, 
  ArrowRight, 
  Heart,
  Stethoscope,
  Activity,
  Layers
} from 'lucide-react';
import Button from '../components/ui/Button';
import ribbonSvg from '../assets/ribbon.svg';

export default function OurStory({ setActiveTab }) {
  return (
    <div className="space-y-16 py-6 sm:py-10 max-w-5xl mx-auto">
      
      {/* En-tête de page */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary-light text-primary border border-primary-border text-xs font-semibold">
          <Heart className="w-3.5 h-3.5 fill-primary text-primary" />
          <span>La genèse humaine du projet</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-text tracking-tight">
          Notre Histoire : Donner un sens aux algorithmes
        </h1>
        <p className="text-base sm:text-lg text-text-muted max-w-2xl mx-auto leading-relaxed">
          Avant d'être des lignes de code et des matrices de calcul, BreastDiagAI est né d'un parcours de vie bouleversant.
        </p>
      </div>

      {/* Récit principal */}
      <section className="card p-8 sm:p-12 space-y-10">
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          <div className="lg:col-span-7 space-y-6 text-text leading-relaxed text-sm sm:text-base">
            <h2 className="text-2xl font-bold text-text flex items-center gap-2.5">
              <span className="w-2.5 h-7 bg-primary rounded-full inline-block"></span>
              L'épreuve qui a tout déclenché
            </h2>
            
            <p>
              Ce projet est né d’une <strong>expérience personnelle profonde</strong> : la découverte fortuite d’une anomalie mammaire 
              chez la mère d’un membre de notre équipe. S’en est suivi un parcours médical particulièrement long, 
              éprouvant et angoissant pour toute la famille.
            </p>
            
            <p className="text-text-muted bg-surface-2 p-4 rounded-2xl border-l-4 border-primary">
              Chaque étape — de la <em>mammographie initiale</em> à <em>l’échographie ciblée</em>, puis aux longues journées 
              d’attente des résultats de la <em>biopsie</em> — a mis en lumière à quel point l'incertitude pèse lourdement 
              sur les épaules des patientes et de leurs proches.
            </p>

            <p>
              De cette traversée est née une interrogation fondamentale : 
              <strong className="text-primary font-semibold block mt-1">
                L’intelligence artificielle peut-elle aider à détecter plus rapidement les situations nécessitant une attention médicale prioritaire ?
              </strong>
            </p>
          </div>

          {/* Espace Illustration Symbolique */}
          <div className="lg:col-span-5 flex justify-center">
            <div className="relative w-full max-w-sm rounded-3xl bg-surface-2 p-8 border border-border shadow-theme text-center space-y-4">
              <div className="relative w-32 h-36 mx-auto flex items-center justify-center">
                <div className="absolute inset-0 bg-primary-light rounded-full blur-xl animate-pulse"></div>
                <img src={ribbonSvg} alt="Ruban Rose" className="relative z-10 w-24 h-28 object-contain filter drop-shadow-md animate-float-subtle" />
              </div>

              <div className="space-y-1">
                <span className="text-xs uppercase font-extrabold tracking-wider text-primary">Symbole de Résilience</span>
                <h4 className="text-base font-bold text-text">Solidarité & Bienveillance</h4>
              </div>

              <p className="text-xs text-text-muted leading-relaxed italic">
                « Ni froideur technique, ni précipitation : une technologie pensée avec le cœur pour éclairer le chemin du soin. »
              </p>
              
              <div className="pt-2 flex justify-center gap-2">
                <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-semibold bg-surface text-primary border border-primary-border shadow-xs">
                  <HeartHandshake className="w-3.5 h-3.5 text-primary" /> Solidarité
                </span>
                <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-semibold bg-surface text-primary border border-primary-border shadow-xs">
                  <ShieldCheck className="w-3.5 h-3.5 text-primary" /> Éthique
                </span>
              </div>
            </div>
          </div>

        </div>

        {/* Citation Visuellement Mise en Valeur */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-rose-900 via-brand-800 to-rose-950 text-white p-8 sm:p-10 shadow-lg border border-white/10">
          <Quote className="absolute top-4 right-6 w-20 h-20 text-white/10 rotate-12 pointer-events-none" />
          
          <div className="relative z-10 space-y-3">
            <span className="text-xs uppercase tracking-widest text-pink-200 font-bold">
              Notre Conviction Première
            </span>
            <blockquote className="text-xl sm:text-2xl lg:text-3xl font-serif italic font-medium leading-relaxed text-white">
              « Derrière les données et les algorithmes, il y a toujours une personne. Une femme. Une famille. Une histoire. »
            </blockquote>
            <p className="text-xs sm:text-sm text-pink-200 font-sans font-semibold pt-1">
              — L'équipe BreastDiagAI
            </p>
          </div>
        </div>

        {/* Notre Mission */}
        <div className="space-y-6 pt-2">
          <h2 className="text-2xl font-bold text-text">
            Notre Mission : Éclairer sans jamais remplacer
          </h2>
          
          <p className="text-text-muted leading-relaxed text-sm sm:text-base">
            <strong>BreastDiagAI</strong> n’a pas pour but de remplacer le médecin, mais d’offrir un 
            <strong> outil d’aide à la décision</strong> — capable d’estimer avec rigueur si une lésion 
            présente des caractéristiques bénignes ou malignes, et surtout d’<strong>expliquer pourquoi</strong>, 
            pour rendre le dépistage plus rapide, accessible et compréhensible.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            <div className="p-5 rounded-2xl bg-surface-2 border border-border space-y-2 hover:shadow-theme transition-base">
              <div className="w-10 h-10 rounded-xl bg-primary-light text-primary flex items-center justify-center font-bold">
                <Activity className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-text">Accélérer la Détection</h4>
              <p className="text-xs text-text-muted leading-relaxed">
                Apporter une pré-évaluation rapide des métriques cellulaires pour réduire les délais d'attente anxiogènes.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-surface-2 border border-border space-y-2 hover:shadow-theme transition-base">
              <div className="w-10 h-10 rounded-xl bg-primary-light text-primary flex items-center justify-center font-bold">
                <Layers className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-text">Rendre l'IA Explicable</h4>
              <p className="text-xs text-text-muted leading-relaxed">
                Démystifier la « boîte noire » : expliquer précisément les biomarqueurs influençant la décision.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-surface-2 border border-border space-y-2 hover:shadow-theme transition-base">
              <div className="w-10 h-10 rounded-xl bg-primary-light text-primary flex items-center justify-center font-bold">
                <Stethoscope className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-text">Préserver l'Humain</h4>
              <p className="text-xs text-text-muted leading-relaxed">
                Garantir que le médecin conserve la maîtrise absolue de la relation thérapeutique et du protocole de soins.
              </p>
            </div>
          </div>
        </div>

      </section>

      {/* Bouton d'action */}
      <div className="text-center space-y-4 pt-4">
        <Button
          variant="primary"
          size="lg"
          icon={ArrowRight}
          iconPosition="right"
          onClick={() => setActiveTab('predict')}
          className="shadow-primary-glow"
        >
          Accéder au module de prédiction
        </Button>
      </div>

    </div>
  );
}
