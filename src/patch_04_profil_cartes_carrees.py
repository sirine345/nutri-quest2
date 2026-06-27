"""
PATCH 04 — Cartes carrées : image en haut, barre + objectif PNNS en bas
Usage: python patch_04_profil_cartes_carrees.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

start_marker = "/* ══ PAGE PROFIL QCM1 ══ */"
end_marker   = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"

if start_marker in code and end_marker in code:
    before = code[:code.index(start_marker)]
    after  = code[code.index(end_marker):]

    NEW_PROFIL = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {
  const vals = Object.values(nutrition);
  const avg = vals.length > 0 ? Math.round(vals.reduce((a,b) => a+b, 0) / vals.length) : 0;

  const CATEGORIES = [
    { label:"Fruits &\\nLégumes",  img:"/legume2.png",    couleur:"#4caf50", score:Math.round(((nutrition.legumes||0)+(nutrition.fruits||0))/2), attendu:70, inverted:false },
    { label:"Légumineuses",        img:"/legumesec.png",  couleur:"#795548", score:nutrition.legumineuses||0, attendu:60, inverted:false },
    { label:"Poisson",             img:"/poisson.png",    couleur:"#0288d1", score:nutrition.poisson||0, attendu:60, inverted:false },
    { label:"Féculents",           img:"/feculent.png",   couleur:"#f57c00", score:nutrition.feculents||0, attendu:60, inverted:false },
    { label:"Laitiers",            img:"/lait2.png",      couleur:"#1976d2", score:nutrition.laitiers||0, attendu:60, inverted:false },
    { label:"À limiter",           img:"/fast_food.png",  couleur:"#e53935", score:Math.round(((nutrition.charcuterie||0)+(nutrition.fastFood||0)+(nutrition.sucres||0))/3), attendu:20, inverted:true },
  ];

  const globalColor = avg >= 70 ? "#2e7d32" : avg >= 40 ? "#f57c00" : "#e53935";
  const globalLabel = avg >= 70 ? "Excellent !" : avg >= 40 ? "Correct" : "À améliorer";

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", zIndex:0 }} />
      <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.62)", zIndex:0 }} />

      <div style={{ position:"relative", zIndex:1, minHeight:"100vh" }}>
        {/* Header */}
        <div style={{ padding:"16px 20px 0", display:"flex", alignItems:"center" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 16px" }}>← Retour</button>
        </div>

        {/* Titre */}
        <div style={{ textAlign:"center", padding:"16px 20px 16px" }}>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:38, fontWeight:900, color:"#FA8072", textShadow:"3px 3px 0 #b2dfdb", margin:"0 0 6px", lineHeight:1.1 }}>
            Mon Profil<br/>Nutritionnel
          </h1>
          <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto" }} />
          <p style={{ color:"rgba(255,255,255,0.85)", fontSize:14, margin:0 }}>Bonjour <strong style={{ color:"#FA8072" }}>{playerName}</strong></p>
        </div>

        {/* Score global */}
        <div style={{ margin:"0 20px 20px", background:"white", borderRadius:20, padding:"14px 18px", display:"flex", alignItems:"center", gap:14, boxShadow:"0 4px 16px rgba(0,0,0,0.2)" }}>
          <div style={{ width:56, height:56, borderRadius:"50%", background:globalColor, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
            <span style={{ fontSize:18, fontWeight:900, color:"white" }}>{avg}%</span>
          </div>
          <div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:globalColor }}>{globalLabel}</div>
            <div style={{ fontSize:12, color:"#666", marginTop:2 }}>Score moyen de tes habitudes alimentaires</div>
          </div>
        </div>

        {/* Grille cartes carrées */}
        <div style={{ padding:"0 20px", display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:10, marginBottom:20 }}>
          {CATEGORIES.map(cat => {
            const pct    = cat.inverted ? Math.max(0, 100 - cat.score) : Math.min(cat.score, 100);
            const attPct = cat.inverted ? 100 - cat.attendu : cat.attendu;
            const ok     = cat.inverted ? cat.score <= cat.attendu : cat.score >= cat.attendu;
            return (
              <div key={cat.label} style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 4px 14px rgba(0,0,0,0.15)", border:`2px solid ${ok ? cat.couleur : "#e53935"}` }}>
                {/* Image */}
                <div style={{ background: ok ? cat.couleur+"18" : "#fbe9e7", height:90, display:"flex", alignItems:"center", justifyContent:"center" }}>
                  <img src={cat.img} alt={cat.label} style={{ height:68, objectFit:"contain", filter:"drop-shadow(1px 3px 4px rgba(0,0,0,0.2))" }} />
                </div>
                {/* Bas de carte */}
                <div style={{ padding:"8px 8px 10px" }}>
                  <div style={{ fontSize:10, fontWeight:900, color:"#1A1A1A", marginBottom:6, lineHeight:1.3, whiteSpace:"pre-line" }}>{cat.label}</div>
                  {/* Barre score vs objectif */}
                  <div style={{ position:"relative", height:10, background:"#f0f0f0", borderRadius:99, marginBottom:4 }}>
                    <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99 }} />
                    {/* Trait objectif */}
                    <div style={{ position:"absolute", top:-2, left:`${attPct}%`, transform:"translateX(-50%)", width:2, height:14, background:"#222", borderRadius:2, zIndex:2 }} />
                  </div>
                  <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, color:"#888" }}>
                    <span style={{ color:cat.couleur, fontWeight:900 }}>{cat.score}%</span>
                    <span style={{ color:"#333", fontWeight:800 }}>obj.{cat.inverted ? `≤${cat.attendu}` : `≥${cat.attendu}`}</span>
                  </div>
                  {/* Badge */}
                  <div style={{ marginTop:5, textAlign:"center", background: ok ? "#e8f5e9" : "#fbe9e7", borderRadius:8, padding:"3px 0", fontSize:9, fontWeight:900, color: ok ? "#2e7d32" : "#c62828" }}>
                    {ok ? "✓ Objectif atteint" : "↑ À améliorer"}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Boutons */}
        <div style={{ padding:"0 20px 30px", display:"flex", flexDirection:"column", gap:12 }}>
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            Mes recommandations PNNS →
          </button>
          <button onClick={() => onVoirRecettes("mediterraneen")}
            style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, padding:"13px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            🫒 Voir les recettes adaptées →
          </button>
        </div>
      </div>
    </div>
  );
}

'''
    code = before + NEW_PROFIL + after
    print("✅ FIX 1 — Cartes carrées avec image + barre objectif PNNS")

    out = sys.argv[1].replace('.jsx', '_patched.jsx')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Fichier : {out}")
    print("→ Copy-Item App_patched.jsx App.jsx -Force")
else:
    print("⚠️  Marqueurs non trouvés")
