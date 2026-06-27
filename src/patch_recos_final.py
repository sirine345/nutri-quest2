#!/usr/bin/env python3
"""Refonte finale RecommandationsQcm1Screen — design avec fonds images"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

START = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
END   = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

idx_start = code.find(START)
idx_end   = code.find(END)

if idx_start == -1 or idx_end == -1:
    print(f"Marqueurs non trouvés: start={idx_start} end={idx_end}")
else:
    print(f"Section trouvée")

    NEW = '''/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const [expanded, setExpanded] = useState(null);

  const bonnes   = ['legumes','fruits','feculents','legumineuses','fruitsACoque','laitiers','poisson','oeufs','volaille'];
  const mauvaises = ['charcuterie','fastFood','sucres','snacks'];
  const scoreGlobal = Math.round(
    (bonnes.reduce((s,k) => s + (nutrition[k]||0), 0) / bonnes.length * 0.7) +
    ((100 - mauvaises.reduce((s,k) => s + (nutrition[k]||0), 0) / mauvaises.length) * 0.3)
  );

  const RECOS = [
    { key:"legumes",      icon:"/legume2.png",    label:"Légumes frais",      bon:v=>v>=60, badge:"Pas assez",       badgeBg:"#EAF3DE", badgeC:"#3B6D11", conseil:"2 portions/jour minimum. Varie les couleurs : vert, orange, rouge pour maximiser les vitamines et antioxydants.", detailBg:"#EAF3DE", detailBorder:"#9ACD32", detailC:"#27500A", btnBg:"#639922", profil:"legumes" },
    { key:"fruits",       icon:"/fruit.png",      label:"Fruits",             bon:v=>v>=60, badge:"Pas assez",       badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"2 fruits entiers par jour min. Varie les espèces selon les saisons pour profiter de tous les antioxydants.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"legumes" },
    { key:"legumineuses", icon:"/legumesec.png",  label:"Légumineuses",       bon:v=>v>=50, badge:"Pas assez",       badgeBg:"#EFEBE9", badgeC:"#5D4037", conseil:"Lentilles, pois chiches, haricots — 2 fois/semaine min. Riches en fibres et protéines végétales.", detailBg:"#EFEBE9", detailBorder:"#795548", detailC:"#3E2723", btnBg:"#795548", profil:"legumineuses" },
    { key:"poisson",      icon:"/poisson.png",    label:"Poisson",            bon:v=>v>=50, badge:"Pas assez",       badgeBg:"#E1F5FE", badgeC:"#0C447C", conseil:"2 fois/semaine dont 1 gras (sardine, maquereau, saumon). Les conserves comptent aussi !", detailBg:"#E1F5FE", detailBorder:"#378ADD", detailC:"#042C53", btnBg:"#378ADD", profil:"poisson" },
    { key:"feculents",    icon:"/feculent.png",   label:"Féculents complets", bon:v=>v>=50, badge:"Pas assez",       badgeBg:"#FAEEDA", badgeC:"#633806", conseil:"Préfère le pain complet, riz brun, pâtes complètes. Plus riches en fibres que les variantes raffinées.", detailBg:"#FAEEDA", detailBorder:"#BA7517", detailC:"#412402", btnBg:"#BA7517", profil:"rapide" },
    { key:"charcuterie",  icon:"/charcuterie.png",label:"Charcuterie",        bon:v=>v<=20, badge:"Tu en manges trop",badgeBg:"#FFF0EB", badgeC:"#993C1D", conseil:"Max 150g/semaine. Classée cancérigène groupe 1 par l'OMS. Remplace par des œufs ou de la volaille.", detailBg:"#FFF0EB", detailBorder:"#FA8072", detailC:"#4A1B0C", btnBg:"#c4622d", profil:"charcuterie", inverse:true },
    { key:"fastFood",     icon:"/fast_food.png",  label:"Fast food",          bon:v=>v<=20, badge:"Trop fréquent",   badgeBg:"#FCEBEB", badgeC:"#791F1F", conseil:"Lié à l'obésité et au diabète de type 2. Même un repas simple maison vaut bien mieux.", detailBg:"#FCEBEB", detailBorder:"#E24B4A", detailC:"#501313", btnBg:"#E24B4A", profil:"fastFood", inverse:true },
    { key:"sucres",       icon:"/sucrerie.png",   label:"Sucreries",          bon:v=>v<=20, badge:"Trop fréquent",   badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"Les sucres ajoutés favorisent les caries et le diabète. Remplace par des fruits frais ou secs.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"sucres", inverse:true },
  ];

  const aAmeliorer = RECOS.filter(r => !r.bon(nutrition[r.key]||0));
  const bienFait   = RECOS.filter(r =>  r.bon(nutrition[r.key]||0));

  const scoreC = scoreGlobal >= 75 ? "#9ACD32" : scoreGlobal >= 50 ? "#ffcc00" : "#FA8072";

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* ── Bannière haute avec fond image ── */}
      <div style={{ position:"relative", height:170, overflow:"hidden", borderBottom:"3px solid #222" }}>
        <img src="/fond_jaune.png" alt="" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"center" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)" }} />
        <div style={{ position:"absolute", inset:0, display:"flex", flexDirection:"column", justifyContent:"flex-end", padding:"16px 20px" }}>
          <button onClick={onBack}
            style={{ background:"rgba(255,255,255,0.18)", border:"1.5px solid rgba(255,255,255,0.45)", borderRadius:8, color:"white", fontSize:11, fontWeight:800, padding:"5px 12px", cursor:"pointer", width:"fit-content", marginBottom:10, letterSpacing:0.3 }}>
            ← Retour
          </button>
          <div style={{ fontSize:22, fontWeight:900, color:"white", textShadow:"1px 2px 6px rgba(0,0,0,0.5)", lineHeight:1.2 }}>Tes recommandations</div>
          <div style={{ fontSize:11, color:"rgba(255,255,255,0.75)", marginTop:3 }}>Basées sur tes habitudes alimentaires déclarées</div>
        </div>
      </div>

      {/* ── Bande score ── */}
      <div style={{ background:"#1a1a1a", display:"flex", borderBottom:"3px solid #222" }}>
        {[
          [scoreGlobal+"/100", "Ton score", scoreC],
          [bienFait.length,    "Déjà bien", "#9ACD32"],
          [aAmeliorer.length,  "À corriger", "#FA8072"],
        ].map(([val, label, c], i) => (
          <div key={i} style={{ flex:1, padding:"12px 10px", textAlign:"center", borderRight: i<2 ? "1px solid #333" : "none" }}>
            <div style={{ fontSize:20, fontWeight:900, color:c, lineHeight:1 }}>{val}</div>
            <div style={{ fontSize:9, color:"#666", marginTop:3, textTransform:"uppercase", letterSpacing:1, fontWeight:700 }}>{label}</div>
          </div>
        ))}
      </div>

      <div style={{ padding:"14px 16px" }}>

        {/* ── À améliorer ── */}
        {aAmeliorer.length > 0 && (
          <div style={{ marginBottom:20 }}>
            <div style={{ fontSize:10, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:2, marginBottom:3 }}>Ce que tu peux améliorer</div>
            <div style={{ fontSize:11, color:"#bbb", marginBottom:11 }}>Clique sur une carte pour voir le conseil personnalisé</div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:9 }}>
              {aAmeliorer.map(r => {
                const isOpen = expanded === r.key;
                return (
                  <div key={r.key}
                    onClick={() => setExpanded(isOpen ? null : r.key)}
                    style={{ background:"white", borderRadius:11, border:`1.5px solid ${isOpen ? r.detailBorder : "#ede8e0"}`, padding:13, cursor:"pointer", transition:"border-color .15s" }}>
                    <div style={{ display:"flex", alignItems:"center", gap:9, marginBottom:7 }}>
                      <div style={{ width:34, height:34, borderRadius:8, background:r.badgeBg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                        <img src={r.icon} alt="" style={{ width:24, height:24, objectFit:"contain" }} />
                      </div>
                      <div>
                        <div style={{ fontSize:13, fontWeight:800, color:"#1a1a1a" }}>{r.label}</div>
                        <div style={{ fontSize:9, color:"#bbb", fontWeight:700, textTransform:"uppercase", letterSpacing:.5, marginTop:1 }}>
                          {r.inverse ? "Trop élevé" : "Insuffisant"}
                        </div>
                      </div>
                    </div>
                    <span style={{ display:"inline-block", background:r.badgeBg, color:r.badgeC, borderRadius:20, padding:"3px 9px", fontSize:10, fontWeight:800 }}>{r.badge}</span>
                    {isOpen && (
                      <>
                        <div style={{ background:r.detailBg, borderLeft:`3px solid ${r.detailBorder}`, borderRadius:8, padding:"10px 11px", marginTop:9, fontSize:11, color:r.detailC, lineHeight:1.7 }}>
                          {r.conseil}
                        </div>
                        <button onClick={e=>{ e.stopPropagation(); onVoirRecettes(r.profil); }}
                          style={{ marginTop:8, background:r.btnBg, border:"none", borderRadius:7, color:"white", fontSize:11, fontWeight:800, padding:"9px 12px", cursor:"pointer", width:"100%", letterSpacing:.3 }}>
                          Voir les recettes →
                        </button>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── Déjà bien ── */}
        {bienFait.length > 0 && (
          <div style={{ marginBottom:20 }}>
            <div style={{ fontSize:10, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:2, marginBottom:3 }}>Ce que tu fais déjà bien</div>
            <div style={{ fontSize:11, color:"#bbb", marginBottom:11 }}>Continue — ces habitudes sont dans les recommandations PNNS</div>
            <div style={{ display:"flex", flexWrap:"wrap", gap:7 }}>
              {bienFait.map(r => (
                <span key={r.key} style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:20, padding:"6px 12px", fontSize:11, fontWeight:700, color:"#3B6D11", display:"inline-flex", alignItems:"center", gap:5 }}>
                  <span style={{ width:14, height:14, borderRadius:"50%", background:"#9ACD32", color:"white", fontSize:8, fontWeight:900, display:"inline-flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>✓</span>
                  {r.label}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ── Message si tout est parfait ── */}
        {aAmeliorer.length === 0 && (
          <div style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:12, padding:"24px 20px", textAlign:"center", marginBottom:20 }}>
            <div style={{ fontSize:17, fontWeight:800, color:"#3B6D11", marginBottom:6 }}>Excellentes habitudes !</div>
            <p style={{ fontSize:12, color:"#777", lineHeight:1.7, margin:0 }}>Tes résultats sont conformes aux recommandations du PNNS. Continue comme ça !</p>
          </div>
        )}

        {/* ── Bannière basse avec fond labo ── */}
        <div style={{ position:"relative", height:120, overflow:"hidden", borderRadius:12, border:"2px solid #222" }}>
          <img src="/laboratoire.png" alt="" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"top" }} />
          <div style={{ position:"absolute", inset:0, background:"rgba(26,58,92,0.80)" }} />
          <div style={{ position:"absolute", inset:0, padding:"14px 18px", display:"flex", flexDirection:"column", justifyContent:"center" }}>
            <div style={{ fontSize:9, color:"rgba(255,255,255,0.45)", textTransform:"uppercase", letterSpacing:2, fontWeight:700, marginBottom:9 }}>Repères officiels PNNS</div>
            <div style={{ display:"flex", flexWrap:"wrap", gap:0 }}>
              {[
                ["Fruits & légumes","5 portions/jour"],
                ["Poisson","2×/sem dont 1 gras"],
                ["Légumineuses","2×/semaine min"],
                ["Charcuterie","Max 150g/sem"],
              ].map(([k,v]) => (
                <div key={k} style={{ flex:"1 0 130px", paddingRight:12, marginBottom:4 }}>
                  <div style={{ fontSize:11, color:"rgba(255,255,255,0.9)", fontWeight:700 }}>{k}</div>
                  <div style={{ fontSize:10, color:"rgba(255,255,255,0.45)", marginTop:1 }}>{v}</div>
                </div>
              ))}
            </div>
          </div>
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
