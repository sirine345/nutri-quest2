"""
PATCH 06 — Page Profil design final : header A + colonnes B + score clair
Usage: python patch_06_profil_design_final.py App.jsx
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
    {
      label: "Fruits & légumes", img: "/legume2.png",
      couleur: "#4caf50",
      score: Math.round(((nutrition.legumes||0) + (nutrition.fruits||0)) / 2),
      attendu: 70, inverted: false,
      descCourte: (s) => s >= 70 ? "Tu atteins les 5 portions/jour recommandées" : s >= 40 ? "Consommation modérée — objectif : 5 portions/jour" : "Tu en manges rarement — objectif : 5 portions/jour",
    },
    {
      label: "Poisson", img: "/poisson.png",
      couleur: "#0288d1",
      score: nutrition.poisson || 0,
      attendu: 60, inverted: false,
      descCourte: (s) => s >= 60 ? "Tu atteins les 2 fois/semaine recommandées" : "Rarement consommé — objectif : 2 fois/semaine",
    },
    {
      label: "Légumineuses", img: "/legumesec.png",
      couleur: "#795548",
      score: nutrition.legumineuses || 0,
      attendu: 60, inverted: false,
      descCourte: (s) => s >= 60 ? "Tu atteins les 2 fois/semaine recommandées" : "Peu consommé — objectif : 2 fois/semaine",
    },
    {
      label: "Féculents complets", img: "/feculent.png",
      couleur: "#f57c00",
      score: nutrition.feculents || 0,
      attendu: 60, inverted: false,
      descCourte: (s) => s >= 60 ? "Bonne consommation à chaque repas" : "Objectif : féculents complets à chaque repas",
    },
    {
      label: "Produits laitiers", img: "/lait2.png",
      couleur: "#1976d2",
      score: nutrition.laitiers || 0,
      attendu: 60, inverted: false,
      descCourte: (s) => s >= 60 ? "2 portions/jour atteintes" : "Objectif : 2 produits laitiers par jour",
    },
    {
      label: "Charcuterie & fast food", img: "/charcuterie.png",
      couleur: "#e53935",
      score: Math.round(((nutrition.charcuterie||0) + (nutrition.fastFood||0)) / 2),
      attendu: 20, inverted: true,
      descCourte: (s) => s <= 20 ? "Très bien — tu limites ces aliments" : s <= 50 ? "Consommation modérée — essaie de réduire" : "Trop fréquent — max 150g charcuterie/sem (OMS)",
    },
  ];

  const augmenter = CATEGORIES.filter(c => !c.inverted && c.score < c.attendu);
  const atteint   = CATEGORIES.filter(c => c.inverted ? c.score <= c.attendu : c.score >= c.attendu);
  const reduire   = CATEGORIES.filter(c => c.inverted && c.score > c.attendu);

  const nbOK = atteint.length;
  const total = CATEGORIES.length;

  const MiniCard = ({ cat }) => {
    const pct    = cat.inverted ? Math.max(0, 100 - cat.score) : Math.min(cat.score, 100);
    const attPct = cat.inverted ? 100 - cat.attendu : cat.attendu;
    return (
      <div style={{ background:"var(--color-background-primary)", borderRadius:10, padding:"10px 12px", border:"0.5px solid var(--color-border-tertiary)" }}>
        <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:6 }}>
          <img src={cat.img} alt={cat.label} style={{ width:28, height:28, objectFit:"contain" }} />
          <div>
            <div style={{ fontSize:12, fontWeight:500, color:"var(--color-text-primary)", lineHeight:1.3 }}>{cat.label}</div>
            <div style={{ fontSize:10, color:"var(--color-text-secondary)", marginTop:1, lineHeight:1.4 }}>{cat.descCourte(cat.score)}</div>
          </div>
        </div>
        <div style={{ position:"relative", height:5, background:"var(--color-background-tertiary)", borderRadius:99 }}>
          <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99 }} />
          <div style={{ position:"absolute", top:-3, left:`${attPct}%`, transform:"translateX(-50%)", width:2, height:11, background:"var(--color-text-primary)", borderRadius:2 }} />
        </div>
        <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, marginTop:3, color:"var(--color-text-secondary)" }}>
          <span style={{ color:cat.couleur, fontWeight:500 }}>Ta consommation</span>
          <span>│ Objectif PNNS</span>
        </div>
      </div>
    );
  };

  return (
    <div style={{ position:"fixed", inset:0, background:"var(--color-background-secondary)", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <div style={{ maxWidth:700, margin:"0 auto" }}>

        {/* Header */}
        <div style={{ background:"#FA8072", padding:"20px 20px 18px" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px", marginBottom:12 }}>← Retour</button>
          <div style={{ fontSize:11, fontWeight:500, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1px", marginBottom:6 }}>Bilan alimentaire · QCM Habitudes</div>
          <div style={{ fontSize:22, fontWeight:500, color:"white", marginBottom:2 }}>Bonjour {playerName}</div>
          <div style={{ fontSize:13, color:"rgba(255,255,255,0.85)" }}>Voici tes résultats personnalisés basés sur tes réponses</div>
        </div>

        {/* Score global clair */}
        <div style={{ padding:"16px 20px", borderBottom:"0.5px solid var(--color-border-tertiary)", background:"var(--color-background-secondary)", display:"flex", alignItems:"center", gap:16 }}>
          <div style={{ flexShrink:0, textAlign:"center" }}>
            <div style={{ fontSize:28, fontWeight:500, color: nbOK >= total*0.8 ? "var(--color-text-success)" : nbOK >= total*0.5 ? "var(--color-text-warning)" : "var(--color-text-danger)", lineHeight:1 }}>
              {nbOK}<span style={{ fontSize:16, color:"var(--color-text-secondary)" }}>/{total}</span>
            </div>
            <div style={{ fontSize:10, color:"var(--color-text-secondary)", marginTop:2 }}>groupes OK</div>
          </div>
          <div style={{ width:"0.5px", height:44, background:"var(--color-border-tertiary)", flexShrink:0 }} />
          <div style={{ flex:1 }}>
            <div style={{ fontSize:14, fontWeight:500, color:"var(--color-text-primary)", marginBottom:4 }}>
              {nbOK} groupe{nbOK > 1 ? "s" : ""} alimentaire{nbOK > 1 ? "s" : ""} sur {total} atteignent l'objectif PNNS
            </div>
            <div style={{ fontSize:12, color:"var(--color-text-secondary)", lineHeight:1.5 }}>
              Le PNNS fixe des objectifs de consommation pour chaque groupe. Plus tu t'en approches, mieux c'est pour ta santé.
            </div>
          </div>
        </div>

        {/* 3 colonnes */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", borderBottom:"0.5px solid var(--color-border-tertiary)" }}>

          {/* À augmenter */}
          <div style={{ padding:"14px 14px", borderRight:"0.5px solid var(--color-border-tertiary)" }}>
            <div style={{ display:"flex", alignItems:"center", gap:6, marginBottom:10 }}>
              <span style={{ fontSize:13 }}>📈</span>
              <span style={{ fontSize:11, fontWeight:500, color:"var(--color-text-success)", textTransform:"uppercase", letterSpacing:"0.5px" }}>À augmenter</span>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
              {augmenter.length === 0
                ? <div style={{ fontSize:11, color:"var(--color-text-secondary)", fontStyle:"italic" }}>Aucun — bravo !</div>
                : augmenter.map(cat => <MiniCard key={cat.label} cat={cat} />)
              }
            </div>
          </div>

          {/* Objectif atteint */}
          <div style={{ padding:"14px 14px", borderRight:"0.5px solid var(--color-border-tertiary)" }}>
            <div style={{ display:"flex", alignItems:"center", gap:6, marginBottom:10 }}>
              <span style={{ fontSize:13 }}>✅</span>
              <span style={{ fontSize:11, fontWeight:500, color:"var(--color-text-info)", textTransform:"uppercase", letterSpacing:"0.5px" }}>Objectif atteint</span>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
              {atteint.length === 0
                ? <div style={{ fontSize:11, color:"var(--color-text-secondary)", fontStyle:"italic" }}>Continue tes efforts !</div>
                : atteint.map(cat => <MiniCard key={cat.label} cat={cat} />)
              }
            </div>
          </div>

          {/* À réduire */}
          <div style={{ padding:"14px 14px" }}>
            <div style={{ display:"flex", alignItems:"center", gap:6, marginBottom:10 }}>
              <span style={{ fontSize:13 }}>⬇️</span>
              <span style={{ fontSize:11, fontWeight:500, color:"var(--color-text-danger)", textTransform:"uppercase", letterSpacing:"0.5px" }}>À réduire</span>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
              {reduire.length === 0
                ? <div style={{ fontSize:11, color:"var(--color-text-secondary)", fontStyle:"italic" }}>Rien à réduire — excellent !</div>
                : reduire.map(cat => <MiniCard key={cat.label} cat={cat} />)
              }
            </div>
          </div>

        </div>

        {/* Encart PNNS */}
        <div style={{ padding:"14px 20px", background:"var(--color-background-secondary)", borderBottom:"0.5px solid var(--color-border-tertiary)" }}>
          <div style={{ fontSize:11, fontWeight:500, color:"var(--color-text-secondary)", textTransform:"uppercase", letterSpacing:"0.5px", marginBottom:6 }}>Ce que dit le PNNS</div>
          <div style={{ fontSize:12, color:"var(--color-text-primary)", lineHeight:1.6 }}>
            Le Programme National Nutrition Santé recommande 5 portions de fruits et légumes par jour, 2 portions de poisson par semaine dont 1 poisson gras, et de limiter la charcuterie à 150g/semaine maximum (classée cancérigène groupe 1 par l'OMS).
          </div>
        </div>

        {/* Boutons */}
        <div style={{ padding:"16px 20px 28px", display:"flex", flexDirection:"column", gap:10, background:"var(--color-background-secondary)" }}>
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"none", borderRadius:12, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.4)" }}>
            Voir mes recommandations PNNS →
          </button>
          <button onClick={() => onVoirRecettes("mediterraneen")}
            style={{ background:"var(--color-background-primary)", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, padding:"13px", cursor:"pointer" }}>
            🫒 Recettes adaptées à mon profil →
          </button>
        </div>

      </div>
    </div>
  );
}

'''

code = before + NEW_PROFIL + after
out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ FIX 1 — Page Profil design final appliqué")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
