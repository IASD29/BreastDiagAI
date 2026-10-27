import React, { useState, useEffect, useCallback } from 'react';
import {
  RefreshCw, Download, Trash2, Search,
  Calendar, Info, X
} from 'lucide-react';
import { api } from '../services/api';
import { EmptyState, SkeletonCard, SectionHeader, MedicalDisclaimer } from '../components/UI';
import Button from '../components/ui/Button';
import IconButton from '../components/ui/IconButton';

const SORT_OPTIONS = [
  { value: 'date_desc', label: 'Plus récentes' },
  { value: 'date_asc',  label: 'Plus anciennes' },
  { value: 'conf_desc', label: 'Confiance (↓)' },
  { value: 'conf_asc',  label: 'Confiance (↑)' },
];

export default function History({ setActiveTab }) {
  const [items, setItems]       = useState([]);
  const [total, setTotal]       = useState(0);
  const [loading, setLoading]   = useState(true);
  const [filter, setFilter]     = useState('Tous');
  const [sort, setSort]         = useState('date_desc');
  const [search, setSearch]     = useState('');
  const [selected, setSelected] = useState(null);
  const [deleting, setDeleting] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const d = await api.getPredictions({ diagnosis: filter, sortBy: sort, limit: 200 });
      setItems(d.items || []);
      setTotal(d.total || 0);
    } catch { /* silence */ }
    finally { setLoading(false); }
  }, [filter, sort]);

  useEffect(() => { load(); }, [load]);

  const handleDelete = async id => {
    try {
      await api.deletePrediction(id);
      setDeleting(null);
      if (selected?.id === id) setSelected(null);
      load();
    } catch (e) { alert(e.message); }
  };

  const exportCSV = () => {
    const header = ['ID','Date','Diagnostic','Confiance','Risque','Rayon moyen','Aire max','Rayon max','Notes'];
    const rows = visible.map(p => [
      p.id,
      new Date(p.created_at).toLocaleString('fr-FR'),
      p.diagnosis, p.confidence, p.risk_level,
      p.radius_mean, p.area_worst, p.radius_worst,
      `"${(p.notes||'').replace(/"/g,'""')}"`
    ]);
    const csv = [header, ...rows].map(r => r.join(',')).join('\n');
    const a   = document.createElement('a');
    a.href    = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
    a.download = `breastdiagai-${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
  };

  const visible = items.filter(i => {
    if (!search) return true;
    const t = search.toLowerCase();
    return String(i.id).includes(t) || i.diagnosis.toLowerCase().includes(t) || (i.notes||'').toLowerCase().includes(t);
  });

  return (
    <div className="py-8 space-y-6 animate-fade-up">

      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <SectionHeader eyebrow="Traçabilité" title="Historique des analyses" description={`${total} analyse${total > 1 ? 's' : ''} enregistrée${total > 1 ? 's' : ''} en base.`} />
        <div className="flex items-center gap-2.5 shrink-0">
          <Button
            variant="secondary"
            size="sm"
            icon={RefreshCw}
            loading={loading}
            onClick={load}
          >
            Actualiser
          </Button>
          <Button
            variant="primary"
            size="sm"
            icon={Download}
            disabled={!visible.length}
            onClick={exportCSV}
          >
            Exporter CSV
          </Button>
        </div>
      </div>

      {/* ── Contrôles de filtrage et recherche ── */}
      <div className="card p-4 flex flex-wrap gap-3 items-center border border-border">
        {/* Filtre Bénin / Malin */}
        <div className="flex bg-surface-2 border border-border rounded-xl p-1 text-xs font-semibold">
          {['Tous', 'Bénin', 'Malin'].map(opt => (
            <button key={opt} onClick={() => setFilter(opt)}
              className={`px-3 py-1.5 rounded-lg btn-motion-spring ${
                filter === opt
                  ? 'bg-surface text-text shadow-xs font-bold'
                  : 'text-text-muted hover:text-text hover:bg-surface/50'
              }`}>
              {opt}
            </button>
          ))}
        </div>

        {/* Recherche */}
        <div className="relative flex-1 min-w-[160px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-text-dim pointer-events-none" />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Rechercher par ID, diagnostic, notes…"
            className="input-field pl-8 py-2 text-xs" />
        </div>

        {/* Tri */}
        <select value={sort} onChange={e => setSort(e.target.value)}
          className="input-field py-2 text-xs w-auto">
          {SORT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      </div>

      {/* ── Tableau d'historique ── */}
      <div className="card overflow-hidden border border-border">
        {loading ? (
          <div className="p-4 space-y-2">
            {[1,2,3].map(i => <SkeletonCard key={i} />)}
          </div>
        ) : visible.length === 0 ? (
          <EmptyState
            icon={RefreshCw}
            title="Aucune analyse trouvée"
            description={search || filter !== 'Tous' ? 'Aucun résultat ne correspond à vos filtres.' : 'Lancez votre première analyse pour qu\'elle apparaisse ici.'}
            action={
              <Button variant="primary" size="md" onClick={() => setActiveTab('predict')}>
                Lancer une analyse
              </Button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="bg-surface-2 border-b border-border text-text-muted font-semibold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="py-3 px-4 text-left">ID</th>
                  <th className="py-3 px-4 text-left">Date</th>
                  <th className="py-3 px-4 text-left">Diagnostic</th>
                  <th className="py-3 px-4 text-right">Confiance</th>
                  <th className="py-3 px-4 text-right">Rayon moy.</th>
                  <th className="py-3 px-4 text-right">Aire max.</th>
                  <th className="py-3 px-4 text-left">Notes</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {visible.map(item => {
                  const benign = item.diagnosis === 'Bénin';
                  return (
                    <tr key={item.id}
                      className="hover:bg-surface-2/70 transition-colors cursor-pointer group"
                      onClick={() => setSelected(item)}>
                      <td className="py-3 px-4 font-mono text-text-dim">#{item.id}</td>
                      <td className="py-3 px-4 text-text-muted whitespace-nowrap">
                        {new Date(item.created_at).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`badge ${benign ? 'badge-benign' : 'badge-malignant'}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${benign ? 'bg-success' : 'bg-danger'}`} />
                          {item.diagnosis}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right font-semibold text-text">
                        {item.confidence}%
                      </td>
                      <td className="py-3 px-4 text-right text-text-muted">{item.radius_mean.toFixed(2)} mm</td>
                      <td className="py-3 px-4 text-right text-text-muted">{item.area_worst.toFixed(0)} mm²</td>
                      <td className="py-3 px-4 text-text-muted max-w-[160px] truncate">
                        {item.notes || <span className="text-text-dim">—</span>}
                      </td>
                      <td className="py-3 px-4 text-right" onClick={e => e.stopPropagation()}>
                        {deleting === item.id ? (
                          <div className="flex items-center gap-1.5 justify-end animate-fade-in">
                            <Button
                              variant="danger"
                              size="sm"
                              className="px-2.5 py-1 text-[11px] min-h-[28px]"
                              onClick={() => handleDelete(item.id)}
                            >
                              Confirmer
                            </Button>
                            <Button
                              variant="secondary"
                              size="sm"
                              className="px-2.5 py-1 text-[11px] min-h-[28px]"
                              onClick={() => setDeleting(null)}
                            >
                              Annuler
                            </Button>
                          </div>
                        ) : (
                          <IconButton
                            icon={Trash2}
                            variant="ghost"
                            size="sm"
                            label="Supprimer cette analyse"
                            onClick={() => setDeleting(item.id)}
                            className="opacity-0 group-hover:opacity-100 hover:text-danger hover:bg-danger-bg"
                          />
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* ── Fiche Détail (Modal) ── */}
      {selected && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-end sm:items-center justify-center p-4 animate-fade-in"
             onClick={() => setSelected(null)}>
          <div className="card bg-surface rounded-3xl w-full max-w-md p-6 space-y-5 shadow-theme-lg border border-border animate-fade-up"
               onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-text text-base">Analyse #{selected.id}</h3>
              <IconButton
                icon={X}
                variant="ghost"
                size="sm"
                label="Fermer"
                onClick={() => setSelected(null)}
              />
            </div>

            <div className={`flex items-center justify-between p-4 rounded-2xl border ${
              selected.diagnosis === 'Bénin'
                ? 'bg-success-bg border-success-border text-success'
                : 'bg-danger-bg border-danger-border text-danger'
            }`}>
              <div>
                <p className="text-[10px] uppercase font-semibold opacity-80">Diagnostic</p>
                <p className="text-2xl font-bold">
                  {selected.diagnosis}
                </p>
              </div>
              <div className="text-right">
                <p className="text-[10px] uppercase font-semibold opacity-80">Confiance</p>
                <p className="text-2xl font-bold text-text">{selected.confidence}%</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs">
              {[
                ['Rayon moyen', `${selected.radius_mean} mm`],
                ['Aire max.', `${selected.area_worst} mm²`],
                ['Rayon max.', `${selected.radius_worst} mm`],
              ].map(([l, v]) => (
                <div key={l} className="p-3 rounded-xl bg-surface-2 border border-border">
                  <p className="text-text-muted text-[10px]">{l}</p>
                  <p className="font-semibold text-text mt-0.5">{v}</p>
                </div>
              ))}
            </div>

            {selected.notes && (
              <div className="p-3 rounded-xl bg-surface-2 border border-border">
                <p className="text-[10px] text-text-muted mb-1">Notes cliniques</p>
                <p className="text-xs text-text">{selected.notes}</p>
              </div>
            )}

            <MedicalDisclaimer compact />

            <Button
              variant="secondary"
              size="md"
              onClick={() => setSelected(null)}
              className="w-full justify-center"
            >
              Fermer la fiche
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
