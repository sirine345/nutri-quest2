"""
PATCH — Dashboard intégré dans React + navigation
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Changer onDashboard pour naviguer vers la phase dashboard
OLD_DASHBOARD_CALL = "      onDashboard={() => alert(\"Dashboard en cours de développement !\")} />;"
NEW_DASHBOARD_CALL = "      onDashboard={() => { setPhase(\"dashboard\"); setPhaseHistory([]); }} />;"
if OLD_DASHBOARD_CALL in code:
    code = code.replace(OLD_DASHBOARD_CALL, NEW_DASHBOARD_CALL)
    fixes += 1; print("✅ FIX 1 — onDashboard navigue vers dashboard")

# 2. Changer le bouton dans félicitations
OLD_FELIT_BTN = '            style={{ background:"#ffdd44", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, padding:"20px", cursor:"pointer", boxShadow:"6px 6px 0 #222" }}>\n              📊 Accéder à mon dashboard →'
NEW_FELIT_BTN = '            onClick={() => { setPhase("dashboard"); setPhaseHistory([]); }}\n            style={{ background:"#ffdd44", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, padding:"20px", cursor:"pointer", boxShadow:"6px 6px 0 #222" }}>\n              📊 Accéder à mon dashboard →'

# simpler: find the alert in felicitations
OLD_ALERT = 'onClick={() => alert("Dashboard en cours de développement !")}'
NEW_ALERT = 'onClick={() => { setPhase("dashboard"); setPhaseHistory([]); }}'
if OLD_ALERT in code:
    code = code.replace(OLD_ALERT, NEW_ALERT)
    fixes += 1; print("✅ FIX 2 — Bouton félicitations vers dashboard")

# 3. Ajouter la phase dashboard dans le switcher (avant QcmSelectScreen)
OLD_SELECT = '    if (phase === "felicitations") return ('
NEW_DASHBOARD_PHASE = '''    if (phase === "dashboard") return <DashboardScreen onBack={() => { setPhase("select"); setPhaseHistory([]); }} playerName={playerName} />;
    if (phase === "felicitations") return ('''
if OLD_SELECT in code:
    code = code.replace(OLD_SELECT, NEW_DASHBOARD_PHASE)
    fixes += 1; print("✅ FIX 3 — Phase dashboard ajoutée")

# 4. Ajouter DashboardScreen avant export default function App
DASHBOARD_COMPONENT = '''
/* ══ DASHBOARD ══ */
function DashboardScreen({ onBack, playerName }) {
  const [tab, setTab] = useState("apercu");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard/stats")
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => { setError("Impossible de charger les données. Vérifiez que le serveur FastAPI est lancé."); setLoading(false); });
  }, []);

  const exportData = (format) => {
    window.open(`http://127.0.0.1:8000/export/${format}`, "_blank");
  };

  const TABS = [
    { id:"apercu", label:"📊 Aperçu" },
    { id:"participants", label:"👥 Participants" },
    { id:"nutrition", label:"🥗 Nutrition" },
    { id:"medas", label:"🫒 MEDAS" },
    { id:"export", label:"📁 Export" },
  ];

  const StatCard = ({ icon, label, value, color = "#FA8072", sub }) => (
    <div style={{ background:"white", borderRadius:16, padding:"20px 24px", border:`2px solid ${color}33`, boxShadow:"0 2px 12px rgba(0,0,0,0.06)", display:"flex", flexDirection:"column", gap:6 }}>
      <div style={{ fontSize:28 }}>{icon}</div>
      <div style={{ fontSize:13, color:"#888", fontWeight:700 }}>{label}</div>
      <div style={{ fontSize:32, fontWeight:900, color, fontFamily:"Arial Black, Arial, sans-serif" }}>{value}</div>
      {sub && <div style={{ fontSize:11, color:"#aaa" }}>{sub}</div>}
    </div>
  );

  const Bar = ({ label, value, max, color }) => (
    <div style={{ marginBottom:12 }}>
      <div style={{ display:"flex", justifyContent:"space-between", fontSize:13, fontWeight:700, color:"#555", marginBottom:4 }}>
        <span>{label}</span><span>{value}%</span>
      </div>
      <div style={{ height:10, background:"#f0f0f0", borderRadius:99 }}>
        <div style={{ height:"100%", width:`${Math.min(value,100)}%`, background:color, borderRadius:99, transition:"width 0.5s" }} />
      </div>
    </div>
  );

  return (
    <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>

      {/* Header */}
      <div style={{ background:"#1A3A5C", padding:"16px 24px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0 }}>
        <div style={{ display:"flex", alignItems:"center", gap:16 }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"1px solid rgba(255,255,255,0.3)", borderRadius:8, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"6px 14px" }}>← Retour</button>
          <div>
            <div style={{ fontSize:11, color:"rgba(255,255,255,0.6)", textTransform:"uppercase", letterSpacing:1 }}>nutri-quest2 — LIMICS</div>
            <div style={{ fontSize:20, fontWeight:900, color:"white", fontFamily:"Arial Black, Arial, sans-serif" }}>📊 Dashboard nutritionnel</div>
          </div>
        </div>
        <div style={{ fontSize:13, color:"rgba(255,255,255,0.7)" }}>Bienvenue, {playerName}</div>
      </div>

      {/* Tabs */}
      <div style={{ background:"white", borderBottom:"2px solid #E8EDF2", display:"flex", flexShrink:0 }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            style={{ padding:"12px 20px", fontSize:13, fontWeight:800, border:"none", background:"none", cursor:"pointer", borderBottom:`3px solid ${tab===t.id?"#FA8072":"transparent"}`, color:tab===t.id?"#FA8072":"#888", transition:"all 0.2s" }}>
            {t.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex:1, overflowY:"auto", padding:"24px" }}>

        {loading && (
          <div style={{ textAlign:"center", padding:"60px 20px", color:"#888" }}>
            <div style={{ fontSize:40, marginBottom:12 }}>⏳</div>
            <div style={{ fontSize:16, fontWeight:700 }}>Chargement des données...</div>
          </div>
        )}

        {error && (
          <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:14, padding:"20px", textAlign:"center" }}>
            <div style={{ fontSize:32, marginBottom:8 }}>⚠️</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#e53935" }}>{error}</div>
            <div style={{ fontSize:13, color:"#555", marginTop:8 }}>Lance le serveur FastAPI : <code>uvicorn main:app --reload</code></div>
          </div>
        )}

        {data && !loading && (

          <>
            {/* APERÇU */}
            {tab === "apercu" && (
              <div>
                <h2 style={{ fontSize:18, fontWeight:900, color:"#1A3A5C", marginBottom:20 }}>Vue d&apos;ensemble</h2>
                <div style={{ display:"grid", gridTemplateColumns:"repeat(4, 1fr)", gap:16, marginBottom:28 }}>
                  <StatCard icon="👥" label="Participants" value={data.total_participants ?? "—"} color="#FA8072" />
                  <StatCard icon="📋" label="Sessions" value={data.total_sessions ?? "—"} color="#9ACD32" />
                  <StatCard icon="🫒" label="Score MEDAS moyen" value={data.score_medas_moyen ? `${data.score_medas_moyen}/14` : "—"} color="#7C3AED" />
                  <StatCard icon="⚕️" label="Risque dénutrition" value={data.pct_risque_denutrition ? `${data.pct_risque_denutrition}%` : "—"} color="#e53935" sub="patients dépistés" />
                </div>

                {/* Scores PNNS moyens */}
                <div style={{ background:"white", borderRadius:16, padding:"24px", border:"1px solid #E8EDF2", marginBottom:20 }}>
                  <h3 style={{ fontSize:15, fontWeight:900, color:"#1A3A5C", marginBottom:16 }}>Scores PNNS moyens</h3>
                  {data.scores_pnns && Object.entries(data.scores_pnns).map(([key, val]) => (
                    <Bar key={key} label={key} value={Math.round(val)} max={100} color="#9ACD32" />
                  ))}
                </div>

                {/* Pathologies */}
                {data.pathologies && (
                  <div style={{ background:"white", borderRadius:16, padding:"24px", border:"1px solid #E8EDF2" }}>
                    <h3 style={{ fontSize:15, fontWeight:900, color:"#1A3A5C", marginBottom:16 }}>Pathologies déclarées</h3>
                    <div style={{ display:"flex", flexWrap:"wrap", gap:10 }}>
                      {Object.entries(data.pathologies).map(([path, count]) => (
                        <div key={path} style={{ background:"#f3eeff", border:"2px solid #7C3AED44", borderRadius:20, padding:"6px 16px", fontSize:13, fontWeight:700, color:"#7C3AED" }}>
                          {path} — {count}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* PARTICIPANTS */}
            {tab === "participants" && (
              <div>
                <h2 style={{ fontSize:18, fontWeight:900, color:"#1A3A5C", marginBottom:20 }}>Liste des participants</h2>
                <div style={{ background:"white", borderRadius:16, overflow:"hidden", border:"1px solid #E8EDF2" }}>
                  <table style={{ width:"100%", borderCollapse:"collapse", fontSize:13 }}>
                    <thead>
                      <tr style={{ background:"#1A3A5C", color:"white" }}>
                        {["ID","Prénom","Date","Âge","Sexe","Pathologies","Score QCM1","Score MEDAS","Score MNA"].map(h => (
                          <th key={h} style={{ padding:"12px 14px", textAlign:"left", fontWeight:800, fontSize:12 }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {(data.participants || []).map((p, i) => (
                        <tr key={i} style={{ borderBottom:"1px solid #f0f0f0", background:i%2===0?"white":"#fafafa" }}>
                          <td style={{ padding:"10px 14px", color:"#888" }}>{p.utilisateur_id}</td>
                          <td style={{ padding:"10px 14px", fontWeight:800 }}>{p.prenom}</td>
                          <td style={{ padding:"10px 14px", color:"#888" }}>{p.created_at ? new Date(p.created_at).toLocaleDateString("fr-FR") : "—"}</td>
                          <td style={{ padding:"10px 14px" }}>{p.age || "—"}</td>
                          <td style={{ padding:"10px 14px" }}>{p.sexe || "—"}</td>
                          <td style={{ padding:"10px 14px", maxWidth:150, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{p.pathologies || "—"}</td>
                          <td style={{ padding:"10px 14px", color:"#9ACD32", fontWeight:700 }}>{p.score_qcm1 ?? "—"}</td>
                          <td style={{ padding:"10px 14px", color:"#7C3AED", fontWeight:700 }}>{p.score_medas ?? "—"}/14</td>
                          <td style={{ padding:"10px 14px", color:"#e53935", fontWeight:700 }}>{p.score_mna ?? "—"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {(!data.participants || data.participants.length === 0) && (
                    <div style={{ textAlign:"center", padding:"40px", color:"#888" }}>Aucun participant pour le moment</div>
                  )}
                </div>
              </div>
            )}

            {/* NUTRITION */}
            {tab === "nutrition" && (
              <div>
                <h2 style={{ fontSize:18, fontWeight:900, color:"#1A3A5C", marginBottom:20 }}>Scores nutritionnels PNNS</h2>
                <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
                  {data.scores_pnns && Object.entries(data.scores_pnns).map(([key, val]) => (
                    <div key={key} style={{ background:"white", borderRadius:14, padding:"20px", border:"1px solid #E8EDF2" }}>
                      <div style={{ fontSize:14, fontWeight:900, color:"#1A3A5C", marginBottom:12 }}>{key}</div>
                      <div style={{ height:12, background:"#f0f0f0", borderRadius:99, marginBottom:8 }}>
                        <div style={{ height:"100%", width:`${Math.min(val,100)}%`, background: val >= 60 ? "#9ACD32" : val >= 40 ? "#ffcc00" : "#FA8072", borderRadius:99, transition:"width 0.5s" }} />
                      </div>
                      <div style={{ display:"flex", justifyContent:"space-between", fontSize:12 }}>
                        <span style={{ color:"#888" }}>Moyenne patients</span>
                        <span style={{ fontWeight:800, color: val >= 60 ? "#9ACD32" : val >= 40 ? "#f57c00" : "#e53935" }}>{Math.round(val)}%</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Mode de vie */}
                {data.modes_vie && (
                  <div style={{ background:"white", borderRadius:16, padding:"24px", border:"1px solid #E8EDF2", marginTop:20 }}>
                    <h3 style={{ fontSize:15, fontWeight:900, color:"#1A3A5C", marginBottom:16 }}>Mode de vie</h3>
                    <div style={{ display:"flex", gap:12, flexWrap:"wrap" }}>
                      {Object.entries(data.modes_vie).map(([mode, count]) => (
                        <div key={mode} style={{ background:"#f0f9e0", border:"2px solid #9ACD3244", borderRadius:12, padding:"12px 20px", textAlign:"center" }}>
                          <div style={{ fontSize:20, fontWeight:900, color:"#9ACD32" }}>{count}</div>
                          <div style={{ fontSize:12, color:"#555", fontWeight:700 }}>{mode}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* MEDAS */}
            {tab === "medas" && (
              <div>
                <h2 style={{ fontSize:18, fontWeight:900, color:"#1A3A5C", marginBottom:20 }}>Régime méditerranéen — Score MEDAS</h2>
                <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:16, marginBottom:20 }}>
                  <StatCard icon="📉" label="Adhésion faible (< 6)" value={data.medas?.adherence_faible ?? "—"} color="#e53935" sub="patients" />
                  <StatCard icon="📊" label="Adhésion modérée (6-9)" value={data.medas?.adherence_moderee ?? "—"} color="#f57c00" sub="patients" />
                  <StatCard icon="📈" label="Adhésion forte (≥ 10)" value={data.medas?.adherence_forte ?? "—"} color="#2e7d32" sub="patients" />
                </div>
                <div style={{ background:"white", borderRadius:16, padding:"24px", border:"1px solid #E8EDF2" }}>
                  <h3 style={{ fontSize:15, fontWeight:900, color:"#1A3A5C", marginBottom:16 }}>Indicateurs MEDAS (%)</h3>
                  {data.medas && (
                    <>
                      <Bar label="Huile d'olive principale" value={Math.round(data.medas.pct_huile_olive ?? 0)} max={100} color="#7C3AED" />
                      <Bar label="Légumes ≥ 2 portions/jour" value={Math.round(data.medas.pct_legumes_ok ?? 0)} max={100} color="#9ACD32" />
                      <Bar label="Poisson ≥ 3 fois/semaine" value={Math.round(data.medas.pct_poisson_ok ?? 0)} max={100} color="#0288d1" />
                    </>
                  )}
                </div>
              </div>
            )}

            {/* EXPORT */}
            {tab === "export" && (
              <div>
                <h2 style={{ fontSize:18, fontWeight:900, color:"#1A3A5C", marginBottom:8 }}>Export des données</h2>
                <p style={{ color:"#666", fontSize:14, marginBottom:24 }}>Téléchargez les données collectées dans le format de votre choix.</p>
                <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:20 }}>
                  {[
                    { format:"csv", icon:"📄", label:"CSV", desc:"Compatible Excel et tableurs", color:"#2e7d32" },
                    { format:"json", icon:"🔧", label:"JSON", desc:"Format standard pour APIs", color:"#1976d2" },
                    { format:"xml", icon:"📋", label:"XML", desc:"Format interopérable", color:"#e65100" },
                  ].map(({ format, icon, label, desc, color }) => (
                    <div key={format} style={{ background:"white", borderRadius:16, padding:"28px 24px", border:`2px solid ${color}33`, textAlign:"center", boxShadow:"0 2px 12px rgba(0,0,0,0.06)" }}>
                      <div style={{ fontSize:48, marginBottom:12 }}>{icon}</div>
                      <div style={{ fontSize:18, fontWeight:900, color, marginBottom:6 }}>{label}</div>
                      <div style={{ fontSize:13, color:"#888", marginBottom:20, lineHeight:1.5 }}>{desc}</div>
                      <button onClick={() => exportData(format)}
                        style={{ background:color, color:"white", border:"none", borderRadius:10, padding:"12px 24px", fontSize:14, fontWeight:800, cursor:"pointer", width:"100%" }}>
                        Télécharger {label} →
                      </button>
                    </div>
                  ))}
                </div>
                <div style={{ background:"#fff8e1", border:"2px solid #f57c00", borderRadius:12, padding:"16px 20px", marginTop:24, fontSize:13, color:"#555" }}>
                  <strong style={{ color:"#f57c00" }}>ℹ️ Info :</strong> Les exports contiennent toutes les données anonymisées des participants. Les données sensibles (MNA, MEDAS) sont incluses.
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

'''

# Insert before export default function App
OLD_EXPORT = 'export default function App() {'
if OLD_EXPORT in code:
    code = code.replace(OLD_EXPORT, DASHBOARD_COMPONENT + OLD_EXPORT)
    fixes += 1; print("✅ FIX 4 — DashboardScreen ajouté")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
