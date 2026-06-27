"""
PATCH 07 — Profil : pleine largeur, cartes avec fond coloré visible, bien délimitées
Usage: python patch_07_profil_layout.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

start_marker = "/* ══ PAGE PROFIL QCM1 ══ */"
end_marker   = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"

if start_marker not in code or end_marker not in code:
    print("⚠️  Marqueurs non trouvés")
    sys.exit(1)

before = code[:code.index(start_marker)]
after  = code[code.index(end_marker):]

NEW_PROFIL = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {

  const CATEGORIES = [
    { label:"Fruits & légumes", img:"/legume2.png", couleur:"#4caf50", bg:"#e8f5e9",
      score: Math.round(((nutrition.legumes||0)+(nutrition.fruits||0))/2),
      attendu:70, inverted:false,
      desc:(s)=> s>=70?"Tu atteins les 5 portions/jour recommandées ✓":s>=40?"Consommation modérée — objectif : 5 portions/jour":"Tu en manges rarement — objectif : 5 portions/jour" },
    { label:"Poisson", img:"/poisson.png", couleur:"#0288d1", bg:"#e1f5fe",
      score: nutrition.poisson||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Tu atteins les 2 fois/semaine recommandées ✓":"Rarement consommé — objectif : 2 fois/semaine" },
    { label:"Légumineuses", img:"/legumesec.png", couleur:"#795548", bg:"#efebe9",
      score: nutrition.legumineuses||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Tu atteins les 2 fois/semaine recommandées ✓":"Peu consommé — objectif : 2 fois/semaine" },
    { label:"Féculents complets", img:"/feculent.png", couleur:"#f57c00", bg:"#fff3e0",
      score: nutrition.feculents||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Bonne consommation à chaque repas ✓":"Objectif : féculents complets à chaque repas" },
    { label:"Produits laitiers", img:"/lait2.png", couleur:"#1976d2", bg:"#e3f2fd",
      score: nutrition.laitiers||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"2 portions/jour atteintes ✓":"Objectif : 2 produits laitiers par jour" },
    { label:"Charcuterie & fast food", img:"/charcuterie.png", couleur:"#e53935", bg:"#fbe9e7",
      score: Math.round(((nutrition.charcuterie||0)+(nutrition.fastFood||0))/2),
      attendu:20, inverted:true,
      desc:(s)=> s<=20?"Très bien — tu limites ces aliments ✓":s<=50?"Consommation modérée — essaie de réduire":"Trop fréquent — max 150g charcuterie/sem (OMS)" },
  ];

  const augmenter = CATEGORIES.filter(c => !c.inverted && c.score < c.attendu);
  const atteint   = CATEGORIES.filter(c => c.inverted ? c.score <= c.attendu : c.score >= c.attendu);
  const reduire   = CATEGORIES.filter(c => c.inverted && c.score > c.attendu);
  const nbOK = atteint.length;
  const total = CATEGORIES.length;

  const MiniCard = ({ cat }) => {
    const pct    = cat.inverted ? Math.max(0, 100-cat.score) : Math.min(cat.score, 100);
    const attPct = cat.inverted ? 100-cat.attendu : cat.attendu;
    return (
      <div style={{ background:cat.bg, borderRadius:12, padding:"12px 14px", border:`2px solid ${cat.couleur}44`, marginBottom:8 }}>
        <div style={{ display:"flex", alignItems:"center", gap:10, marginBottom:8 }}>
          <img src={cat.img} alt={cat.label} style={{ width:36, height:36, objectFit:"contain", flexShrink:0 }} />
          <div>
            <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A" }}>{cat.label}</div>
            <div style={{ fontSize:11, color:"#555", marginTop:2, lineHeight:1.4 }}>{cat.desc(cat.score)}</div>
          </div>
        </div>
        <div style={{ position:"relative", height:8, background:"rgba(0,0,0,0.1)", borderRadius:99 }}>
          <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99 }} />
          <div style={{ position:"absolute", top:-4, left:`${attPct}%`, transform:"translateX(-50%)", width:3, height:16, background:"#222", borderRadius:2, zIndex:2 }} />
        </div>
        <div style={{ display:"flex", justifyContent:"space-between", fontSize:10, marginTop:4 }}>
          <span style={{ color:cat.couleur, fontWeight:800 }}>Ta consommation</span>
          <span style={{ color:"#555", fontWeight:700 }}>│ Objectif PNNS</span>
        </div>
      </div>
    );
  };

  const ColTitle = ({ emoji, label, color }) => (
    <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:14, paddingBottom:10, borderBottom:`2px solid ${color}44` }}>
      <span style={{ fontSize:18 }}>{emoji}</span>
      <span style={{ fontSize:12, fontWeight:900, color:color, textTransform:"uppercase", letterSpacing:"0.5px" }}>{label}</span>
    </div>
  );

  return (
    <div style={{ position:"fixed", inset:0, background:"#f5f5f5", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon pleine largeur */}
      <div style={{ background:"#FA8072", padding:"20px 32px 22px" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.25)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"6px 14px", marginBottom:14 }}>← Retour</button>
        <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>Bilan alimentaire · QCM Habitudes</div>
        <div style={{ fontSize:26, fontWeight:900, color:"white", marginBottom:4 }}>Bonjour {playerName} 👋</div>
        <div style={{ fontSize:14, color:"rgba(255,255,255,0.9)" }}>Voici tes résultats personnalisés basés sur tes réponses</div>
      </div>

      {/* Bandeau score global */}
      <div style={{ background:"white", borderBottom:"2px solid #eee", padding:"16px 32px", display:"flex", alignItems:"center", gap:20 }}>
        <div style={{ textAlign:"center", flexShrink:0 }}>
          <div style={{ fontSize:36, fontWeight:900, lineHeight:1, color: nbOK>=total*0.8?"#2e7d32":nbOK>=total*0.5?"#f57c00":"#e53935" }}>
            {nbOK}<span style={{ fontSize:18, color:"#999" }}>/{total}</span>
          </div>
          <div style={{ fontSize:11, color:"#888", fontWeight:700, marginTop:2 }}>groupes atteints</div>
        </div>
        <div style={{ width:2, height:52, background:"#eee", flexShrink:0 }} />
        <div>
          <div style={{ fontSize:15, fontWeight:900, color:"#1A1A1A", marginBottom:4 }}>
            {nbOK} groupe{nbOK>1?"s":""} sur {total} atteignent l'objectif PNNS
          </div>
          <div style={{ fontSize:12, color:"#666", lineHeight:1.6 }}>
            Le PNNS fixe des objectifs de consommation pour chaque groupe alimentaire. Le trait noir sur chaque barre indique l'objectif à atteindre.
          </div>
        </div>
      </div>

      {/* 3 colonnes pleine largeur */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:0, background:"white", borderBottom:"2px solid #eee" }}>

        <div style={{ padding:"20px 24px", borderRight:"2px solid #eee" }}>
          <ColTitle emoji="📈" label="À augmenter" color="#2e7d32" />
          {augmenter.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Aucun groupe à augmenter — bravo !</div>
            : augmenter.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

        <div style={{ padding:"20px 24px", borderRight:"2px solid #eee" }}>
          <ColTitle emoji="✅" label="Objectif atteint" color="#0288d1" />
          {atteint.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Continue tes efforts !</div>
            : atteint.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

        <div style={{ padding:"20px 24px" }}>
          <ColTitle emoji="⬇️" label="À réduire" color="#e53935" />
          {reduire.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Rien à réduire — excellent !</div>
            : reduire.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

      </div>

      {/* Encart PNNS */}
      <div style={{ background:"#fff8f0", padding:"16px 32px", borderBottom:"2px solid #eee" }}>
        <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"1px", marginBottom:6 }}>Ce que dit le PNNS</div>
        <div style={{ fontSize:13, color:"#444", lineHeight:1.7 }}>
          Le Programme National Nutrition Santé recommande <strong>5 portions de fruits et légumes par jour</strong>, <strong>2 portions de poisson par semaine</strong> dont 1 poisson gras, et de <strong>limiter la charcuterie à 150g/semaine</strong> maximum (classée cancérigène groupe 1 par l'OMS).
        </div>
      </div>

      {/* Boutons */}
      <div style={{ padding:"20px 32px 32px", background:"white", display:"flex", gap:14 }}>
        <button onClick={onVoirRecos}
          style={{ flex:2, background:"#FA8072", border:"none", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.4)" }}>
          Voir mes recommandations PNNS →
        </button>
        <button onClick={() => onVoirRecettes("mediterraneen")}
          style={{ flex:1, background:"white", border:"2px solid #FA8072", borderRadius:14, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, padding:"14px", cursor:"pointer" }}>
          🫒 Recettes adaptées →
        </button>
      </div>

    </div>
  );
}

'''

code = before + NEW_PROFIL + after
out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ FIX 1 — Profil : pleine largeur, cartes colorées, bien délimitées")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
