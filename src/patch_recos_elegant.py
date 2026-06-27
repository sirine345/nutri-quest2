#!/usr/bin/env python3
"""
Refonte élégante de RecommandationsQcm1Screen
Design propre, sobre, professionnel
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

START = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
END = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

idx_start = code.find(START)
idx_end = code.find(END)

if idx_start == -1 or idx_end == -1:
    print(f"Marqueurs non trouvés: start={idx_start} end={idx_end}")
else:
    print(f"Section trouvée")

    NEW = '''/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const [expanded, setExpanded] = useState(null);

  const bonnes = ['legumes','fruits','feculents','legumineuses','fruitsACoque','laitiers','poisson','oeufs','volaille'];
  const mauvaises = ['charcuterie','fastFood','sucres','snacks'];
  const scoreGlobal = Math.round(
    (bonnes.reduce((s,k) => s + (nutrition[k]||0), 0) / bonnes.length * 0.7) +
    ((100 - mauvaises.reduce((s,k) => s + (nutrition[k]||0), 0) / mauvaises.length) * 0.3)
  );

  const RECOS = [
    { key:"legumes",      icon:"/legume2.png",      label:"Légumes frais",       bon: v=>v>=60, conseil:"Visez au moins 2 portions par jour. Variez les couleurs pour maximiser les apports en vitamines.", cible:60, couleur:"#639922", bg:"#EAF3DE", profil:"legumes" },
    { key:"fruits",       icon:"/fruit.png",         label:"Fruits",              bon: v=>v>=60, conseil:"2 fruits entiers par jour minimum. Les jus ne remplacent pas les fruits entiers.", cible:60, couleur:"#D4537E", bg:"#FBEAF0", profil:"legumes" },
    { key:"legumineuses", icon:"/legumesec.png",     label:"Légumineuses",        bon: v=>v>=50, conseil:"Lentilles, pois chiches, haricots — au moins 2 fois par semaine. Riches en fibres et protéines végétales.", cible:50, couleur:"#795548", bg:"#EFEBE9", profil:"legumineuses" },
    { key:"poisson",      icon:"/poisson.png",       label:"Poisson",             bon: v=>v>=50, conseil:"2 portions par semaine, dont un poisson gras (sardine, maquereau, saumon) pour les oméga-3.", cible:50, couleur:"#378ADD", bg:"#E6F1FB", profil:"poisson" },
    { key:"feculents",    icon:"/feculent.png",      label:"Féculents complets",  bon: v=>v>=50, conseil:"Préférez le pain complet, le riz brun et les pâtes complètes. Plus riches en fibres que les raffinés.", cible:50, couleur:"#BA7517", bg:"#FAEEDA", profil:"rapide" },
    { key:"charcuterie",  icon:"/charcuterie.png",   label:"Charcuterie",         bon: v=>v<=20, conseil:"Maximum 150g par semaine. Classée cancérigène groupe 1 par l'OMS. Remplacez par des œufs ou de la volaille.", cible:20, couleur:"#E24B4A", bg:"#FCEBEB", profil:"charcuterie", inverse:true },
    { key:"fastFood",     icon:"/fast_food.png",     label:"Fast food",           bon: v=>v<=20, conseil:"Liés à l'obésité et au diabète de type 2. Privilégiez le fait maison, même simple (œufs, légumes sautés).", cible:20, couleur:"#E24B4A", bg:"#FCEBEB", profil:"fastFood", inverse:true },
    { key:"sucres",       icon:"/sucrerie.png",      label:"Sucreries",           bon: v=>v<=20, conseil:"Les sucres ajoutés favorisent les caries et le diabète. Remplacez par des fruits frais ou des fruits secs.", cible:20, couleur:"#D4537E", bg:"#FBEAF0", profil:"sucres", inverse:true },
  ];

  const aAmeliorer = RECOS.filter(r => !r.bon(nutrition[r.key]||0));
  const bienFait   = RECOS.filter(r =>  r.bon(nutrition[r.key]||0));

  const scoreLabel = scoreGlobal >= 75 ? "Très bien" : scoreGlobal >= 50 ? "Correct" : "À améliorer";
  const scoreCouleur = scoreGlobal >= 75 ? "#639922" : scoreGlobal >= 50 ? "#BA7517" : "#E24B4A";

  return (
    <div style={{ position:"fixed", inset:0, background:"#faf7f2", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* ── Header sobre ── */}
      <div style={{ background:"#1a1a1a", padding:"0" }}>
        <div style={{ padding:"16px 24px", display:"flex", alignItems:"center", gap:16 }}>
          <button onClick={onBack}
            style={{ background:"none", border:"1px solid rgba(255,255,255,0.25)", borderRadius:8, color:"rgba(255,255,255,0.8)", fontSize:13, fontWeight:600, cursor:"pointer", padding:"7px 14px", letterSpacing:0.3 }}>
            ← Retour
          </button>
          <div style={{ flex:1 }}>
            <div style={{ fontSize:11, color:"rgba(255,255,255,0.4)", textTransform:"uppercase", letterSpacing:2, marginBottom:2 }}>Programme National Nutrition Santé</div>
            <div style={{ fontSize:18, fontWeight:700, color:"white", letterSpacing:0.3 }}>Vos recommandations personnalisées</div>
          </div>
        </div>

        {/* Score strip */}
        <div style={{ display:"flex", borderTop:"1px solid rgba(255,255,255,0.08)" }}>
          {/* Score global */}
          <div style={{ padding:"18px 24px", borderRight:"1px solid rgba(255,255,255,0.08)", minWidth:120 }}>
            <div style={{ fontSize:11, color:"rgba(255,255,255,0.4)", textTransform:"uppercase", letterSpacing:1.5, marginBottom:6 }}>Score global</div>
            <div style={{ fontSize:36, fontWeight:700, color:scoreCouleur, lineHeight:1 }}>{scoreGlobal}</div>
            <div style={{ fontSize:11, color:"rgba(255,255,255,0.5)", marginTop:3 }}>/100 — {scoreLabel}</div>
          </div>
          {/* Barre score */}
          <div style={{ flex:1, padding:"18px 24px", display:"flex", flexDirection:"column", justifyContent:"flex-end" }}>
            <div style={{ height:4, background:"rgba(255,255,255,0.1)", borderRadius:2, overflow:"hidden", marginBottom:10 }}>
              <div style={{ height:"100%", width:`${scoreGlobal}%`, background:scoreCouleur, borderRadius:2, transition:"width 1s ease" }} />
            </div>
            <div style={{ display:"flex", gap:16 }}>
              <div style={{ fontSize:11, color:"rgba(255,255,255,0.5)" }}>
                <span style={{ color:"#9ACD32", fontWeight:700 }}>{bienFait.length}</span> acquis
              </div>
              <div style={{ fontSize:11, color:"rgba(255,255,255,0.5)" }}>
                <span style={{ color:"#FA8072", fontWeight:700 }}>{aAmeliorer.length}</span> à améliorer
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ padding:"24px", maxWidth:680, margin:"0 auto" }}>

        {/* ── Points à améliorer ── */}
        {aAmeliorer.length > 0 && (
          <div style={{ marginBottom:32 }}>
            <div style={{ fontSize:11, fontWeight:700, color:"#888", textTransform:"uppercase", letterSpacing:2, marginBottom:16 }}>
              Points à améliorer
            </div>
            {aAmeliorer.map(r => {
              const val = nutrition[r.key] || 0;
              const isOpen = expanded === r.key;
              const pct = r.inverse ? Math.max(0, 100-val) : val;
              return (
                <div key={r.key} style={{ background:"white", borderRadius:12, marginBottom:10, overflow:"hidden", border:"1px solid #e8e0d5" }}>
                  <div onClick={() => setExpanded(isOpen ? null : r.key)}
                    style={{ padding:"16px 20px", display:"flex", alignItems:"center", gap:14, cursor:"pointer" }}>
                    {/* Image aliment */}
                    <div style={{ width:44, height:44, borderRadius:10, background:r.bg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                      <img src={r.icon} alt="" style={{ width:30, height:30, objectFit:"contain" }} />
                    </div>
                    {/* Label + barre */}
                    <div style={{ flex:1, minWidth:0 }}>
                      <div style={{ fontSize:14, fontWeight:700, color:"#1a1a1a", marginBottom:7 }}>{r.label}</div>
                      <div style={{ position:"relative", height:5, background:"#f0ece6", borderRadius:3, overflow:"hidden" }}>
                        <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background: pct >= 60 ? "#639922" : pct >= 35 ? "#BA7517" : "#E24B4A", borderRadius:3, transition:"width 0.6s ease" }} />
                        {/* Ligne objectif */}
                        <div style={{ position:"absolute", top:0, left:`${r.cible}%`, width:2, height:"100%", background:"#1a1a1a", opacity:0.3 }} />
                      </div>
                      <div style={{ display:"flex", justifyContent:"space-between", marginTop:4 }}>
                        <span style={{ fontSize:11, color:"#999" }}>Actuel : {val}%</span>
                        <span style={{ fontSize:11, color:"#999" }}>Objectif : {r.inverse?"≤":"≥"}{r.cible}%</span>
                      </div>
                    </div>
                    {/* Flèche */}
                    <div style={{ color:"#ccc", fontSize:12, transform:isOpen?"rotate(180deg)":"none", transition:"transform 0.2s", flexShrink:0 }}>▼</div>
                  </div>

                  {/* Détail déplié */}
                  {isOpen && (
                    <div style={{ padding:"0 20px 20px", borderTop:"1px solid #f0ece6" }}>
                      <p style={{ fontSize:13, color:"#555", lineHeight:1.75, margin:"14px 0 14px" }}>{r.conseil}</p>
                      <button onClick={() => onVoirRecettes(r.profil)}
                        style={{ background:"#1a1a1a", border:"none", borderRadius:8, color:"white", fontSize:13, fontWeight:600, padding:"10px 18px", cursor:"pointer", letterSpacing:0.3 }}>
                        Voir les recettes associées →
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* ── Ce qui va bien ── */}
        {bienFait.length > 0 && (
          <div style={{ marginBottom:24 }}>
            <div style={{ fontSize:11, fontWeight:700, color:"#888", textTransform:"uppercase", letterSpacing:2, marginBottom:16 }}>
              Habitudes acquises
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(140px,1fr))", gap:8 }}>
              {bienFait.map(r => (
                <div key={r.key} style={{ background:"white", border:"1px solid #e8e0d5", borderRadius:10, padding:"12px 14px", display:"flex", alignItems:"center", gap:10 }}>
                  <div style={{ width:32, height:32, borderRadius:8, background:r.bg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                    <img src={r.icon} alt="" style={{ width:22, height:22, objectFit:"contain" }} />
                  </div>
                  <div>
                    <div style={{ fontSize:11, fontWeight:700, color:"#1a1a1a", lineHeight:1.3 }}>{r.label}</div>
                    <div style={{ fontSize:11, color:"#639922", fontWeight:700, marginTop:1 }}>{nutrition[r.key]||0}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Message si tout va bien ── */}
        {aAmeliorer.length === 0 && (
          <div style={{ background:"white", border:"1px solid #e8e0d5", borderRadius:12, padding:"28px 24px", textAlign:"center", marginBottom:24 }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#EAF3DE", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 14px" }}>
              <img src="/legume2.png" style={{ width:34, height:34, objectFit:"contain" }} />
            </div>
            <div style={{ fontSize:17, fontWeight:700, color:"#1a1a1a", marginBottom:6 }}>Excellentes habitudes</div>
            <p style={{ fontSize:13, color:"#777", lineHeight:1.7, margin:0 }}>Vos résultats sont conformes aux recommandations du PNNS. Continuez ainsi !</p>
          </div>
        )}

        {/* ── Encart PNNS ── */}
        <div style={{ background:"white", border:"1px solid #e8e0d5", borderRadius:12, padding:"18px 20px" }}>
          <div style={{ fontSize:11, fontWeight:700, color:"#888", textTransform:"uppercase", letterSpacing:2, marginBottom:10 }}>Repères PNNS</div>
          {[
            ["Fruits & légumes", "Au moins 5 portions par jour (400g)"],
            ["Poisson", "2 fois par semaine dont 1 gras"],
            ["Légumineuses", "Au moins 2 fois par semaine"],
            ["Viande rouge", "Maximum 500g par semaine"],
            ["Charcuterie", "Maximum 150g par semaine"],
          ].map(([label, val]) => (
            <div key={label} style={{ display:"flex", justifyContent:"space-between", padding:"7px 0", borderBottom:"1px solid #f5f0ea" }}>
              <span style={{ fontSize:13, color:"#555", fontWeight:600 }}>{label}</span>
              <span style={{ fontSize:13, color:"#888" }}>{val}</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */'''

    code = code[:idx_start] + NEW + code[idx_end + len(END):]
    print("✅ RecommandationsQcm1Screen refaite")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
