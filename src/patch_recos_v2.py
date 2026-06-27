#!/usr/bin/env python3
"""
Refonte visuelle complète de RecommandationsQcm1Screen
Design gameplay : score animé, badges, cartes colorées, progression
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

# Trouver et remplacer toute la fonction RecommandationsQcm1Screen
START = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
END = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

idx_start = code.find(START)
idx_end = code.find(END)

if idx_start == -1 or idx_end == -1:
    print(f"⚠️  Marqueurs non trouvés: start={idx_start} end={idx_end}")
else:
    print(f"✅ Section trouvée: L{code[:idx_start].count(chr(10))+1} → L{code[:idx_end].count(chr(10))+1}")

    NEW_SECTION = '''/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const [expanded, setExpanded] = useState(null);
  const [animDone, setAnimDone] = useState(false);

  // Calcul du score global
  const bonnes = ['legumes','fruits','feculents','legumineuses','fruitsACoque','laitiers','poisson','oeufs','volaille'];
  const mauvaises = ['charcuterie','fastFood','sucres','snacks'];
  const scoreGlobal = Math.round(
    (bonnes.reduce((s,k) => s + (nutrition[k]||0), 0) / bonnes.length * 0.7) +
    ((100 - mauvaises.reduce((s,k) => s + (nutrition[k]||0), 0) / mauvaises.length) * 0.3)
  );

  useEffect(() => { setTimeout(() => setAnimDone(true), 300); }, []);

  // Badge selon score
  const badge = scoreGlobal >= 75
    ? { label:"Champion nutrition !", emoji:"🏆", color:"#2e7d32", bg:"#e8f5e9", grad:"linear-gradient(135deg,#2e7d32,#4caf50)" }
    : scoreGlobal >= 50
    ? { label:"Bon équilibre !", emoji:"⭐", color:"#f57c00", bg:"#fff3e0", grad:"linear-gradient(135deg,#e65100,#ff9800)" }
    : { label:"Des progrès à faire", emoji:"💪", color:"#c62828", bg:"#fbe9e7", grad:"linear-gradient(135deg,#b71c1c,#e53935)" };

  // Points à améliorer
  const RECOS_CONFIG = [
    { key:"legumes",      icon:"🥦", label:"Légumes frais",      bon: v=>v>=60, conseil:"Visez 2 portions par jour (épinards, carottes, brocolis...)", cible:"≥ 60%", couleur:"#4CAF50", bg:"#E8F5E9" },
    { key:"fruits",       icon:"🍎", label:"Fruits",             bon: v=>v>=60, conseil:"Au moins 2 fruits entiers par jour. Évitez les jus.", cible:"≥ 60%", couleur:"#E91E63", bg:"#FCE4EC" },
    { key:"legumineuses", icon:"🫘", label:"Légumineuses",       bon: v=>v>=50, conseil:"Lentilles, pois chiches, haricots — 2 fois par semaine minimum.", cible:"≥ 50%", couleur:"#795548", bg:"#EFEBE9" },
    { key:"poisson",      icon:"🐟", label:"Poisson",            bon: v=>v>=50, conseil:"2 fois par semaine, dont un poisson gras (sardine, saumon...)", cible:"≥ 50%", couleur:"#0288D1", bg:"#E1F5FE" },
    { key:"feculents",    icon:"🌾", label:"Féculents complets", bon: v=>v>=50, conseil:"Préférez pain complet, riz brun, pâtes complètes à chaque repas.", cible:"≥ 50%", couleur:"#FF9800", bg:"#FFF3E0" },
    { key:"charcuterie",  icon:"⚠️", label:"Charcuterie",       bon: v=>v<=20, conseil:"Maximum 150g/semaine. Classée cancérigène groupe 1 par l'OMS.", cible:"≤ 20%", couleur:"#F44336", bg:"#FFEBEE", inverse:true },
    { key:"fastFood",     icon:"🍔", label:"Fast food",          bon: v=>v<=20, conseil:"Ultra-transformés liés à l'obésité. Cuisinez maison au maximum.", cible:"≤ 20%", couleur:"#F44336", bg:"#FFEBEE", inverse:true },
    { key:"sucres",       icon:"🍭", label:"Sucreries",          bon: v=>v<=20, conseil:"Sucres ajoutés = risque diabète. Remplacez par des fruits frais.", cible:"≤ 20%", couleur:"#E91E63", bg:"#FCE4EC", inverse:true },
  ];

  const aAmeliorer = RECOS_CONFIG.filter(r => !r.bon(nutrition[r.key]||0));
  const bienFait   = RECOS_CONFIG.filter(r =>  r.bon(nutrition[r.key]||0));

  return (
    <div style={{ position:"fixed", inset:0, background:"#f4dcbf", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* ── HEADER avec score animé ── */}
      <div style={{ background:"#c4622d", borderBottom:"3px solid #222", boxShadow:"0 3px 0 #222" }}>
        <div style={{ padding:"12px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
          <button onClick={onBack}
            style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 14px", boxShadow:"2px 2px 0 #222" }}>
            ← Retour
          </button>
          <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:700, textTransform:"uppercase", letterSpacing:1 }}>QCM 1 — Résultats</div>
        </div>

        {/* Score global + badge */}
        <div style={{ padding:"0 20px 24px", display:"flex", alignItems:"center", gap:20 }}>
          {/* Jauge circulaire simulée */}
          <div style={{ position:"relative", width:90, height:90, flexShrink:0 }}>
            <svg viewBox="0 0 36 36" style={{ transform:"rotate(-90deg)", width:"100%", height:"100%" }}>
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="3" />
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="#ffdd44" strokeWidth="3"
                strokeDasharray={`${animDone ? scoreGlobal : 0} 100`}
                style={{ transition:"stroke-dasharray 1.2s ease", strokeLinecap:"round" }} />
            </svg>
            <div style={{ position:"absolute", inset:0, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center" }}>
              <div style={{ fontSize:22, fontWeight:900, color:"#ffdd44", lineHeight:1 }}>{animDone ? scoreGlobal : 0}</div>
              <div style={{ fontSize:9, color:"rgba(255,255,255,0.7)", fontWeight:700 }}>/ 100</div>
            </div>
          </div>

          <div style={{ flex:1 }}>
            <div style={{ fontSize:22, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.2)", lineHeight:1.2, marginBottom:6 }}>
              {badge.emoji} {badge.label}
            </div>
            <div style={{ fontSize:13, color:"rgba(255,255,255,0.85)", lineHeight:1.5 }}>
              {aAmeliorer.length === 0
                ? "Toutes vos habitudes sont conformes aux recommandations PNNS !"
                : `${aAmeliorer.length} point${aAmeliorer.length>1?"s":""} à améliorer · ${bienFait.length} acquis`}
            </div>
          </div>
        </div>

        {/* Barre de progression */}
        <div style={{ height:6, background:"rgba(0,0,0,0.2)", margin:"0" }}>
          <div style={{ height:"100%", width:`${animDone?scoreGlobal:0}%`, background:"#9ACD32", transition:"width 1.2s ease", borderRadius:"0 3px 3px 0" }} />
        </div>
      </div>

      <div style={{ padding:"16px" }}>

        {/* ── CE QUI VA BIEN ── */}
        {bienFait.length > 0 && (
          <div style={{ marginBottom:16 }}>
            <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:10 }}>
              <div style={{ flex:1, height:2, background:"#9ACD32", borderRadius:99 }} />
              <span style={{ fontSize:11, fontWeight:900, color:"#2e7d32", textTransform:"uppercase", letterSpacing:1, whiteSpace:"nowrap" }}>✅ Habitudes acquises</span>
              <div style={{ flex:1, height:2, background:"#9ACD32", borderRadius:99 }} />
            </div>
            <div style={{ display:"flex", gap:8, flexWrap:"wrap" }}>
              {bienFait.map(r => (
                <div key={r.key} style={{ background:"white", border:"2px solid #9ACD32", borderRadius:20, padding:"6px 14px", display:"flex", alignItems:"center", gap:6, boxShadow:"2px 2px 0 #2e7d32" }}>
                  <span style={{ fontSize:16 }}>{r.icon}</span>
                  <span style={{ fontSize:12, fontWeight:800, color:"#2e7d32" }}>{r.label}</span>
                  <span style={{ fontSize:11, color:"#4caf50", fontWeight:700 }}>{nutrition[r.key]||0}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── POINTS À AMÉLIORER ── */}
        {aAmeliorer.length > 0 && (
          <div style={{ marginBottom:16 }}>
            <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:10 }}>
              <div style={{ flex:1, height:2, background:"#FA8072", borderRadius:99 }} />
              <span style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:1, whiteSpace:"nowrap" }}>💡 À améliorer</span>
              <div style={{ flex:1, height:2, background:"#FA8072", borderRadius:99 }} />
            </div>
            {aAmeliorer.map((r, i) => {
              const val = nutrition[r.key] || 0;
              const isOpen = expanded === r.key;
              return (
                <div key={r.key}
                  style={{ background:"white", border:"3px solid #222", borderRadius:14, marginBottom:10, overflow:"hidden", boxShadow:"4px 4px 0 #222", transition:"box-shadow 0.15s" }}>
                  {/* En-tête carte */}
                  <div onClick={() => setExpanded(isOpen ? null : r.key)}
                    style={{ padding:"14px 16px", display:"flex", alignItems:"center", gap:12, cursor:"pointer", background: isOpen ? r.bg : "white" }}>
                    {/* Icône catégorie */}
                    <div style={{ width:44, height:44, borderRadius:12, background:r.bg, border:`2px solid ${r.couleur}`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:22, flexShrink:0 }}>
                      {r.icon}
                    </div>
                    {/* Info */}
                    <div style={{ flex:1, minWidth:0 }}>
                      <div style={{ fontSize:14, fontWeight:900, color:"#1A1A1A", marginBottom:3 }}>{r.label}</div>
                      {/* Mini barre score */}
                      <div style={{ display:"flex", alignItems:"center", gap:8 }}>
                        <div style={{ flex:1, height:6, background:"#f0f0f0", borderRadius:99, overflow:"hidden", border:"1px solid #ddd" }}>
                          <div style={{ height:"100%", width:`${val}%`, background: val > 50 ? "#4caf50" : val > 25 ? "#ff9800" : "#f44336", borderRadius:99, transition:"width 0.8s ease" }} />
                        </div>
                        <span style={{ fontSize:12, fontWeight:900, color: val > 50 ? "#4caf50" : val > 25 ? "#ff9800" : "#f44336", flexShrink:0 }}>{val}%</span>
                        <span style={{ fontSize:10, color:"#aaa", flexShrink:0 }}>objectif {r.cible}</span>
                      </div>
                    </div>
                    {/* Chevron */}
                    <div style={{ fontSize:14, color:"#888", transform: isOpen ? "rotate(180deg)" : "none", transition:"transform 0.2s", flexShrink:0 }}>▼</div>
                  </div>

                  {/* Détail déplié */}
                  {isOpen && (
                    <div style={{ padding:"0 16px 16px", borderTop:`2px solid ${r.couleur}22`, background:r.bg }}>
                      <div style={{ display:"flex", alignItems:"flex-start", gap:10, padding:"12px 0" }}>
                        <div style={{ fontSize:18, flexShrink:0 }}>💡</div>
                        <p style={{ margin:0, fontSize:13, color:"#333", lineHeight:1.7, fontWeight:600 }}>{r.conseil}</p>
                      </div>
                      {/* Bouton recettes */}
                      <button onClick={() => onVoirRecettes(r.key)}
                        style={{ background:r.couleur, border:"2px solid #222", borderRadius:10, color:"white", fontSize:13, fontWeight:800, padding:"10px 16px", cursor:"pointer", width:"100%", boxShadow:"3px 3px 0 #222", transition:"transform 0.1s" }}
                        onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-2px)";e.currentTarget.style.boxShadow="4px 4px 0 #222";}}
                        onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="3px 3px 0 #222";}}>
                        Voir les recettes {r.label.toLowerCase()} →
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* ── Message si tout est bon ── */}
        {aAmeliorer.length === 0 && (
          <div style={{ background:"white", border:"3px solid #9ACD32", borderRadius:16, padding:"28px 20px", textAlign:"center", boxShadow:"4px 4px 0 #2e7d32", marginBottom:16 }}>
            <div style={{ fontSize:48, marginBottom:10 }}>🏆</div>
            <div style={{ fontSize:20, fontWeight:900, color:"#2e7d32", marginBottom:8 }}>Excellentes habitudes !</div>
            <p style={{ fontSize:14, color:"#555", lineHeight:1.6, margin:0 }}>Vos résultats sont conformes aux recommandations du PNNS. Continuez comme ça !</p>
          </div>
        )}

        {/* ── Conseil du jour ── */}
        <div style={{ background:"#1A3A5C", border:"3px solid #222", borderRadius:14, padding:"16px", boxShadow:"4px 4px 0 #222" }}>
          <div style={{ fontSize:12, fontWeight:900, color:"#ffdd44", textTransform:"uppercase", letterSpacing:1, marginBottom:8 }}>💡 Le saviez-vous ?</div>
          <p style={{ margin:0, fontSize:13, color:"rgba(255,255,255,0.9)", lineHeight:1.7 }}>
            Le PNNS recommande de consommer au moins <strong style={{color:"#9ACD32"}}>5 fruits et légumes</strong> par jour, 
            du <strong style={{color:"#FA8072"}}>poisson 2 fois/semaine</strong> et des <strong style={{color:"#ffcc00"}}>légumineuses 2 fois/semaine</strong>.
          </p>
        </div>

      </div>
    </div>
  );
}

/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */'''

    code = code[:idx_start] + NEW_SECTION + code[idx_end + len(END):]
    print(f"✅ RecommandationsQcm1Screen entièrement refaite")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
