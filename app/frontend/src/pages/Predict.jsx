import React, { useState } from 'react';
import { Stethoscope, RotateCcw, Sparkles, AlertCircle, HelpCircle, ChevronRight, FileText } from 'lucide-react';
import { api } from '../services/api';
import { ConfidenceRing, MedicalDisclaimer, SectionHeader } from '../components/UI';
import Button from '../components/ui/Button';
import IconButton from '../components/ui/IconButton';

const FIELDS = [
  { key: 'radius_mean',    label: 'Rayon moyen',           unit: 'mm',  required: true,  tip: 'Distance moyenne du centre au périmètre des cellules' },
  { key: 'area_worst',     label: 'Aire maximale',         unit: 'mm²', required: true,  tip: 'Aire des 3 plus grandes cellules observées' },
  { key: 'radius_worst',   label: 'Rayon maximal',         unit: 'mm',  required: true,  tip: 'Rayon des 3 plus grandes cellules' },
  { key: 'texture_mean',   label: 'Texture moyenne',       unit: '',    required: false, tip: 'Écart-type des niveaux de gris' },
  { key: 'perimeter_mean', label: 'Périmètre moyen',       unit: 'mm',  required: false, tip: 'Périmètre moyen du noyau cellulaire' },
  { key: 'concavity_mean', label: 'Concavité moyenne',     unit: '',    required: false, tip: 'Sévérité des portions concaves du contour' },
];

const PRESETS = {
  benign:    { radius_mean: '12.45', area_worst: '546.7', radius_worst: '13.84', texture_mean: '15.70', perimeter_mean: '78.27', concavity_mean: '0.038', notes: 'Cas bénin typique (référence WDBC)' },
  malignant: { radius_mean: '17.99', area_worst: '1682.0', radius_worst: '25.38', texture_mean: '20.38', perimeter_mean: '122.8', concavity_mean: '0.282', notes: 'Cas malin typique (référence WDBC)' },
};

const EMPTY = { radius_mean: '', area_worst: '', radius_worst: '', texture_mean: '', perimeter_mean: '', concavity_mean: '', notes: '' };

export default function Predict({ setActiveTab }) {
  const [form, setForm]       = useState(EMPTY);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);
  const [result, setResult]   = useState(null);
  const [savedId, setSavedId] = useState(null);
  const [tooltip, setTooltip] = useState(null);

  const handleChange = e => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
    if (error) setError(null);
  };

  const reset = () => { setForm(EMPTY); setError(null); setResult(null); setSavedId(null); };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!form.radius_mean || !form.area_worst || !form.radius_worst) {
      setError('Les 3 mesures obligatoires sont requises : Rayon moyen, Aire maximale et Rayon maximal.');
      return;
    }
    setLoading(true); setError(null); setResult(null);
    try {
      const payload = {
        radius_mean:    parseFloat(form.radius_mean),
        area_worst:     parseFloat(form.area_worst),
        radius_worst:   parseFloat(form.radius_worst),
        texture_mean:   form.texture_mean   ? parseFloat(form.texture_mean)   : null,
        perimeter_mean: form.perimeter_mean ? parseFloat(form.perimeter_mean) : null,
        concavity_mean: form.concavity_mean ? parseFloat(form.concavity_mean) : null,
        notes: form.notes || null,
      };
      const res = await api.predict(payload);
      setResult(res.result);
      setSavedId(res.id);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isBenign = result?.diagnosis === 'Bénin';

  return (
    <div className="py-8 space-y-8 animate-fade-up max-w-5xl">

      <SectionHeader
        eyebrow="Diagnostic prédictif"
        title="Analyse morphologique par IA"
        description="Saisissez les biomarqueurs issus de la biopsie pour obtenir une estimation de malignité instantanée."
      />

      <MedicalDisclaimer compact />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

        {/* ── Formulaire de saisie ── */}
        <div className="lg:col-span-7 card p-6 space-y-6">

          {/* Boutons d'exemples pré-remplis */}
          <div className="flex items-center justify-between pb-4 border-b border-border">
            <p className="text-xs font-semibold text-text-muted uppercase tracking-wider">Exemples pré-remplis</p>
            <div className="flex items-center gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setForm(PRESETS.benign)}
                className="border-success-border text-success hover:bg-success-bg hover:text-success"
              >
                + Cas Bénin
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setForm(PRESETS.malignant)}
                className="border-danger-border text-danger hover:bg-danger-bg hover:text-danger"
              >
                + Cas Malin
              </Button>
              <IconButton
                icon={RotateCcw}
                label="Réinitialiser le formulaire"
                size="sm"
                onClick={reset}
              />
            </div>
          </div>

          {/* Alerte d'erreur */}
          {error && (
            <div className="flex items-start gap-2.5 px-4 py-3 rounded-xl bg-danger-bg border border-danger-border text-danger text-sm animate-fade-in">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Champs obligatoires */}
            <div className="space-y-3">
              <p className="text-xs font-semibold text-primary uppercase tracking-wider">
                Mesures obligatoires *
              </p>
              {FIELDS.filter(f => f.required).map(({ key, label, unit, tip }) => (
                <div key={key} className="relative">
                  <label className="block text-xs font-medium text-text-muted mb-1.5 flex items-center gap-1.5">
                    {label}
                    <button type="button"
                      onMouseEnter={() => setTooltip(key)}
                      onMouseLeave={() => setTooltip(null)}
                      className="text-text-dim hover:text-primary transition-colors">
                      <HelpCircle className="w-3.5 h-3.5" />
                    </button>
                    {tooltip === key && (
                      <div className="absolute left-28 top-0 z-20 px-3 py-2 rounded-xl bg-surface-3 text-text text-xs shadow-xl border border-border w-52 animate-fade-in">
                        {tip}
                      </div>
                    )}
                  </label>
                  <div className="relative">
                    <input type="number" step="any" name={key}
                      value={form[key]} onChange={handleChange}
                      placeholder="0.00" required
                      className="input-field pr-12" />
                    {unit && (
                      <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs text-text-dim font-mono">
                        {unit}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Champs complémentaires */}
            <div className="space-y-3 pt-2 border-t border-border">
              <p className="text-xs font-semibold text-text-muted uppercase tracking-wider">Mesures complémentaires</p>
              <div className="grid grid-cols-3 gap-3">
                {FIELDS.filter(f => !f.required).map(({ key, label }) => (
                  <div key={key}>
                    <label className="block text-[11px] font-medium text-text-muted mb-1">{label}</label>
                    <input type="number" step="any" name={key}
                      value={form[key]} onChange={handleChange}
                      placeholder="—"
                      className="input-field text-xs py-2" />
                  </div>
                ))}
              </div>

              <div>
                <label className="block text-xs font-medium text-text-muted mb-1.5">
                  Référence / Notes
                </label>
                <textarea name="notes" rows={2} value={form.notes} onChange={handleChange}
                  placeholder="ex: Dossier #A-204 — Contrôle annuel"
                  className="input-field text-xs resize-none" />
              </div>
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              icon={Sparkles}
              loading={loading}
              className="w-full justify-center shadow-lg"
            >
              {loading ? "Analyse en cours…" : "Lancer l'analyse"}
            </Button>
          </form>
        </div>

        {/* ── Panneau de Résultat ── */}
        <div className="lg:col-span-5 space-y-4">
          {result ? (
            <div className={`card p-6 space-y-6 animate-fade-up border-2 ${
              isBenign ? 'border-success-border bg-surface' : 'border-danger-border bg-surface'
            }`}>
              {/* En-tête */}
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-text-muted font-medium uppercase tracking-wider">Résultat — #{savedId}</p>
                  <h3 className={`text-2xl font-bold mt-0.5 ${isBenign ? 'text-success' : 'text-danger'}`}>
                    {result.diagnosis}
                  </h3>
                </div>
                <span className={`badge text-sm ${isBenign ? 'badge-benign' : 'badge-malignant'}`}>
                  {result.risk_level}
                </span>
              </div>

              {/* Jauge de confiance */}
              <div className="flex justify-center py-4">
                <ConfidenceRing
                  value={Math.round(result.confidence)}
                  label="Confiance IA"
                  color={isBenign ? 'var(--success)' : 'var(--danger)'}
                  size={140}
                />
              </div>

              {/* Barre de probabilité */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-medium text-text-muted">
                  <span>Bénin</span>
                  <span>Probabilité maligne : {(result.probability_malignant * 100).toFixed(1)}%</span>
                  <span>Malin</span>
                </div>
                <div className="w-full h-2 rounded-full bg-surface-2 overflow-hidden border border-border">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-emerald-400 to-rose-500 transition-all duration-1000"
                    style={{ width: `${result.probability_malignant * 100}%` }}
                  />
                </div>
              </div>

              {/* Explication clinique */}
              <div className="p-4 rounded-xl bg-surface-2 border border-border">
                <p className="text-xs text-text leading-relaxed">{result.explanation}</p>
              </div>

              {/* CTA vers l'historique */}
              <Button
                variant="secondary"
                size="md"
                icon={FileText}
                onClick={() => setActiveTab('history')}
                className="w-full justify-center"
              >
                <span>Voir dans l'historique</span>
                <ChevronRight className="w-4 h-4 ml-auto" />
              </Button>
            </div>
          ) : (
            /* En attente */
            <div className="card p-8 text-center space-y-4 animate-fade-in border-dashed">
              <div className="w-14 h-14 rounded-2xl bg-primary-light text-primary mx-auto flex items-center justify-center animate-float-subtle">
                <Stethoscope className="w-7 h-7" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-text">En attente d'analyse</h3>
                <p className="text-xs text-text-muted mt-1 leading-relaxed max-w-xs mx-auto">
                  Remplissez le formulaire ou chargez un exemple pour voir le résultat ici.
                </p>
              </div>
            </div>
          )}

          {/* Repères anatomopathologiques */}
          <div className="card p-4 space-y-3">
            <p className="text-xs font-semibold text-text-muted flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-primary" />
              Seuils de référence (WDBC)
            </p>
            <ul className="space-y-1.5 text-[11px] text-text-muted">
              <li><span className="font-medium text-text">Rayon moyen</span> : bénin &lt;12 mm · malin &gt;16 mm</li>
              <li><span className="font-medium text-text">Aire maximale</span> : bénin &lt;700 mm² · malin &gt;1100 mm²</li>
              <li><span className="font-medium text-text">Rayon maximal</span> : seuil critique ~16.5 mm</li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  );
}
