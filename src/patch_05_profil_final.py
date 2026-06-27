"""
PATCH 05 — Profil : 2 colonnes aérées, explication texte claire, barre avec écart PNNS
Usage: python patch_05_profil_final.py App.jsx
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
  const vals = Object.values(nutrition);
  const avg = vals.length > 0 ? Math.round(vals.reduce((a,b) => a+b, 0) / vals.length) : 0;

  // Chaque catégorie avec : score obtenu, objectif PNNS, et texte explicatif dynamique
  const CATEGORIES = [
    {
      label: "Fruits & Légumes",
      img: "/legume2.png",
      couleur: "#4caf50",
      score: Math.round(((nutrition.legumes||0) + (nutrition.fruits||0)) / 2),
      attendu: 70,
      inverted: false,
      unite: "portions/jour",
      objectifTexte: "5 portions/jour recommandées (PNNS)",
      getText: (s) => {
        if (s >= 70) return "Tu atteins les 5 portions de fruits et légumes par jour recommandées par le PNNS. Excellent !";
        if (s >= 40) return "Tu consommes des fruits et légumes régulièrement, mais pas encore les 5 portions/jour recommandées par le PNNS.";
        return "Ta consommation de fruits et légumes est insuffisante. Le PNNS recommande 5 portions (400g) par jour pour réduire les risques de maladies.";
      }
    },
    {
      label: "Légumineuses",
      img: "/legumesec.png",
      couleur: "#795548",
      score: nutrition.legumineuses || 0,
      attendu: 60,
      inverted: false,
      unite: "fois/semaine",
      objectifTexte: "2 fois/semaine recommandées (PNNS)",
      getText: (s) => {
        if (s >= 60) return "Tu consommes bien les légumineuses (lentilles, pois chiches…). Elles apportent protéines végétales et fibres.";
        if (s >= 30) return "Tu manges parfois des légumineuses, mais le PNNS recommande d'en consommer au moins 2 fois par semaine.";
        return "Les légumineuses sont peu présentes dans ton alimentation. Elles sont riches en fibres et protéines végétales — à intégrer !";
      }
    },
    {
      label: "Poisson",
      img: "/poisson.png",
      couleur: "#0288d1",
      score: nutrition.poisson || 0,
      attendu: 60,
      inverted: false,
      unite: "fois/semaine",
      objectifTexte: "2 fois/semaine dont 1 poisson gras (PNNS)",
      getText: (s) => {
        if (s >= 60) return "Tes apports en poisson sont bons. Les oméga-3 des poissons gras (sardine, maquereau) protègent ton cœur.";
        return "Le PNNS recommande 2 portions/semaine de poisson, dont au moins 1 poisson gras riche en oméga-3.";
      }
    },
    {
      label: "Féculents complets",
      img: "/feculent.png",
      couleur: "#f57c00",
      score: nutrition.feculents || 0,
      attendu: 60,
      inverted: false,
      unite: "repas/jour",
      objectifTexte: "À chaque repas, en version complète (PNNS)",
      getText: (s) => {
        if (s >= 60) return "Tu consommes bien les féculents complets. Leurs fibres ralentissent l'absorption du sucre et rassasient mieux.";
        return "Le PNNS recommande des féculents complets à chaque repas (pain complet, pâtes complètes, riz brun) pour leurs fibres.";
      }
    },
    {
      label: "Produits laitiers",
      img: "/lait2.png",
      couleur: "#1976d2",
      score: nutrition.laitiers || 0,
      attendu: 60,
      inverted: false,
      unite: "portions/jour",
      objectifTexte: "2 produits laitiers/jour (PNNS)",
      getText: (s) => {
        if (s >= 60) return "Tes apports en calcium via les produits laitiers sont bons. Essentiel pour les os et les dents.";
        return "Le PNNS recommande 2 produits laitiers par jour (yaourt, fromage, lait) pour couvrir tes besoins en calcium.";
      }
    },
    {
      label: "Charcuterie & Fast food",
      img: "/charcuterie.png",
      couleur: "#e53935",
      score: Math.round(((nutrition.charcuterie||0) + (nutrition.fastFood||0) + (nutrition.sucres||0)) / 3),
      attendu: 20,
      inverted: true,
      unite: "fois/semaine",
      objectifTexte: "À limiter au maximum (PNNS)",
      getText: (s) => {
        if (s <= 20) return "Tu limites bien la charcuterie, le fast food et les sucreries. L'OMS classe la charcuterie cancérigène groupe 1.";
        if (s <= 50) return "Ta consommation de charcuterie, fast food ou sucreries est modérée — essaie de réduire encore un peu.";
        return "Ces aliments sont consommés trop fréquemment. La charcuterie est classée cancérigène groupe 1 par l'OMS. Limitez à 150g/semaine.";
      }
    },
  ];

  const globalColor = avg >= 70 ? "#2e7d32" : avg >= 40 ? "#f57c00" : "#e53935";
  const globalBg    = avg >= 70 ? "#e8f5e9"  : avg >= 40 ? "#fff3e0"  : "#fbe9e7";
  const globalLabel = avg >= 70 ? "Excellentes habitudes !" : avg >= 40 ? "Habitudes correctes" : "Des progrès à faire";

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", zIndex:0 }} />
      <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.62)", zIndex:0 }} />

      <div style={{ position:"relative", zIndex:1, minHeight:"100vh" }}>
        {/* Header */}
        <div style={{ padding:"16px 20px 0" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 16px" }}>← Retour</button>
        </div>

        {/* Titre style page 1 */}
        <div style={{ textAlign:"center", padding:"16px 20px 20px" }}>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:40, fontWeight:900, color:"#FA8072", textShadow:"3px 3px 0 #b2dfdb", margin:"0 0 6px", lineHeight:1.1 }}>
            Mon Profil<br/>Nutritionnel
          </h1>
          <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto 12px" }} />
          <p style={{ color:"rgba(255,255,255,0.85)", fontSize:14, margin:0 }}>
            Bonjour <strong style={{ color:"#FA8072" }}>{playerName}</strong> — voici ton bilan alimentaire
          </p>
        </div>

        {/* Score global */}
        <div style={{ margin:"0 20px 24px", background:"white", borderRadius:20, padding:"18px 20px", display:"flex", alignItems:"center", gap:16, boxShadow:"0 6px 24px rgba(0,0,0,0.2)" }}>
          <div style={{ width:64, height:64, borderRadius:"50%", background:globalColor, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", flexShrink:0, boxShadow:`0 4px 16px ${globalColor}66` }}>
            <span style={{ fontSize:20, fontWeight:900, color:"white", lineHeight:1 }}>{avg}%</span>
          </div>
          <div style={{ flex:1 }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:globalColor, marginBottom:4 }}>{globalLabel}</div>
            <div style={{ fontSize:12, color:"#666", lineHeight:1.5 }}>
              {avg >= 70 ? "Tes habitudes sont proches des recommandations du PNNS. Continue !" :
               avg >= 40 ? "Tu es sur la bonne voie. Quelques ajustements suffiront." :
               "Ne t'inquiète pas — tes recommandations personnalisées vont t'aider à progresser."}
            </div>
          </div>
        </div>

        {/* Grille 2 colonnes */}
        <div style={{ padding:"0 20px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:24 }}>
          {CATEGORIES.map(cat => {
            const pct    = cat.inverted ? Math.max(0, 100 - cat.score) : Math.min(cat.score, 100);
            const attPct = cat.inverted ? 100 - cat.attendu : cat.attendu;
            const ok     = cat.inverted ? cat.score <= cat.attendu : cat.score >= cat.attendu;
            const texte  = cat.getText(cat.score);
            return (
              <div key={cat.label} style={{ background:"white", borderRadius:18, overflow:"hidden", boxShadow:"0 6px 20px rgba(0,0,0,0.15)", display:"flex", flexDirection:"column" }}>
                {/* Image */}
                <div style={{ background: ok ? cat.couleur+"22" : "#fbe9e7", padding:"18px 0 10px", display:"flex", alignItems:"center", justifyContent:"center", position:"relative" }}>
                  <img src={cat.img} alt={cat.label} style={{ height:72, objectFit:"contain", filter:"drop-shadow(1px 3px 6px rgba(0,0,0,0.2))" }} />
                  <div style={{ position:"absolute", top:8, right:8, background: ok ? cat.couleur : "#e53935", borderRadius:20, padding:"2px 8px", fontSize:9, fontWeight:900, color:"white" }}>
                    {ok ? "✓ OK" : "↑ À améliorer"}
                  </div>
                </div>
                {/* Contenu */}
                <div style={{ padding:"12px 14px 14px", flex:1, display:"flex", flexDirection:"column", gap:8 }}>
                  <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:12, fontWeight:900, color:"#1A1A1A" }}>{cat.label}</div>

                  {/* Barre avec objectif */}
                  <div>
                    <div style={{ position:"relative", height:10, background:"#f0f0f0", borderRadius:99, marginBottom:4 }}>
                      <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99 }} />
                      <div style={{ position:"absolute", top:-3, left:`${attPct}%`, transform:"translateX(-50%)", width:3, height:16, background:"#222", borderRadius:2, zIndex:2 }} />
                    </div>
                    <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, fontWeight:800 }}>
                      <span style={{ color:cat.couleur }}>Ton score : {cat.score}%</span>
                      <span style={{ color:"#555" }}>│ Objectif PNNS</span>
                    </div>
                  </div>

                  {/* Objectif texte */}
                  <div style={{ fontSize:10, color:"#888", fontStyle:"italic" }}>{cat.objectifTexte}</div>

                  {/* Explication */}
                  <div style={{ background: ok ? cat.couleur+"15" : "#fbe9e7", borderRadius:8, padding:"8px 10px", fontSize:10, color:"#444", lineHeight:1.55, marginTop:"auto" }}>
                    {texte}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Boutons */}
        <div style={{ padding:"0 20px 32px", display:"flex", flexDirection:"column", gap:12 }}>
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            Mes recommandations PNNS →
          </button>
          <button onClick={() => onVoirRecettes("mediterraneen")}
            style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, padding:"13px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
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

print("✅ FIX 1 — Page Profil : 2 colonnes aérées + explication claire + barre PNNS")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
