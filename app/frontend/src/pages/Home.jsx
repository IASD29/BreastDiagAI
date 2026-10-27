import React from 'react';
import { ArrowRight, TrendingUp, Zap, Heart } from 'lucide-react';
import { SectionHeader, StatCard, MedicalDisclaimer } from '../components/UI';
import Button from '../components/ui/Button';
import ribbonSvg from '../assets/ribbon.svg';

export default function Home({ setActiveTab }) {
  return (
    <div className="py-8 space-y-12 animate-fade-up">

      {/* ── Hero Octobre Rose ── */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-rose-950 via-[#180b14] to-[#0f0a12] p-8 sm:p-12 border border-white/10 shadow-theme-lg">
        {/* Lueur d'ambiance */}
        <div className="absolute -top-32 -right-32 w-80 h-80 rounded-full bg-pink-600/20 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-20 -left-20 w-64 h-64 rounded-full bg-rose-900/20 blur-2xl pointer-events-none" />

        <div className="relative grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-pink-500/15 border border-pink-500/30 text-pink-300 text-xs font-medium">
              <img src={ribbonSvg} alt="" className="w-4 h-4" />
              <span>Octobre Rose · Aide au Diagnostic</span>
            </div>

            <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-white leading-tight text-balance">
              L'intelligence artificielle{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-300 via-pink-400 to-rose-400">
                au service de la vie
              </span>
            </h1>

            <p className="text-white/70 text-base leading-relaxed max-w-lg font-light">
              BreastDiagAI est un outil académique d'aide au diagnostic du cancer du sein,
              combinant la précision du Machine Learning à une dimension profondément humaine.
            </p>

            <div className="flex flex-wrap gap-3.5 pt-2">
              <Button
                variant="primary"
                size="lg"
                icon={Zap}
                onClick={() => setActiveTab('predict')}
                className="shadow-primary-glow"
              >
                <span>Lancer une analyse</span>
                <ArrowRight className="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" />
              </Button>
              <Button
                variant="ghost"
                size="lg"
                onClick={() => setActiveTab('story')}
                className="text-white/80 hover:text-white hover:bg-white/10 border border-white/15"
              >
                Notre histoire
              </Button>
            </div>
          </div>

          {/* Right: Ruban d'espoir */}
          <div className="lg:col-span-5 flex justify-center">
            <div className="glass p-6 text-center space-y-3 max-w-xs w-full bg-white/5 border border-white/10 shadow-xl">
              <img src={ribbonSvg} alt="Ruban Rose" className="w-16 h-16 mx-auto filter drop-shadow-md animate-float-subtle" />
              <h3 className="text-white font-semibold text-lg">Octobre Rose 🎗️</h3>
              <p className="text-white/60 text-sm leading-relaxed">
                Le dépistage précoce sauve des vies. Ensemble, faisons la différence.
              </p>
              <div className="inline-block px-3 py-1.5 rounded-full bg-pink-500/20 text-pink-300 text-xs font-semibold border border-pink-500/30">
                90% de rémission si détecté tôt
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Chiffres Clés ── */}
      <section className="space-y-5">
        <SectionHeader
          eyebrow="Sensibilisation"
          title="Pourquoi le dépistage précoce est vital"
          description="Le cancer du sein touche 1 femme sur 8. La technologie peut accélérer la détection et sauver des vies."
        />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard label="Femmes touchées" value="1 / 8" sub="Au cours de leur vie" icon={Heart} accent="brand" />
          <StatCard label="Rémission précoce" value="90%" sub="Si détecté à un stade 1" icon={TrendingUp} accent="emerald" />
          <StatCard label="Analyse IA" value="< 1s" sub="Évaluation instantanée" icon={Zap} accent="sky" />
        </div>
      </section>

      {/* ── Comment ça marche ── */}
      <section className="card p-8 space-y-8 border border-border">
        <SectionHeader
          eyebrow="Fonctionnement"
          title="Comment BreastDiagAI analyse-t-il ?"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { n: '01', t: 'Saisie des données', d: 'Renseignez les mesures biométriques issues de la biopsie (rayon, aire, concavité...).' },
            { n: '02', t: 'Analyse algorithmique', d: 'Le modèle évalue la morphologie cellulaire et calcule un score de probabilité de malignité.' },
            { n: '03', t: 'Rapport explicatif', d: 'Résultat clair (Bénin / Malin) avec score de confiance, explication et sauvegarde automatique.' },
          ].map(({ n, t, d }) => (
            <div key={n} className="space-y-3 animate-fade-up">
              <span className="text-3xl font-extrabold text-primary/30">{n}</span>
              <h3 className="text-sm font-semibold text-text">{t}</h3>
              <p className="text-xs text-text-muted leading-relaxed">{d}</p>
            </div>
          ))}
        </div>
        <div className="pt-2">
          <Button
            variant="primary"
            size="md"
            icon={ArrowRight}
            iconPosition="right"
            onClick={() => setActiveTab('predict')}
          >
            Accéder au formulaire de diagnostic
          </Button>
        </div>
      </section>

      {/* Avertissement */}
      <MedicalDisclaimer />

    </div>
  );
}
