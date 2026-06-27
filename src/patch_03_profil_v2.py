"""
PATCH 03 — Page Profil v2 : fond i.jpg, catégories, score vs attendu
Usage: python patch_03_profil_v2.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

start_marker = "/* ══ PAGE PROFIL QCM1 ══ */"
end_marker   = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"

if start_marker in code and end_marker in code:
    before = code[:code.index(start_marker)]
    after  = code[code.index(end_marker):]

    NEW_PROFIL = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {
  const vals = Object.values(nutrition);
  const avg = vals.length > 0 ? Math.round(vals.reduce((a,b) => a+b, 0) / vals.length) : 0;

  // Catégories avec score obtenu et score PNNS attendu
  const CATEGORIES = [
    {
      label: "Fruits & Légumes",
      img: "/legume2.png",
      img2: "/fruit.png",
      couleur: "#4caf50",
      bg: "#e8f5e9",
      score: Math.round(((nutrition.legumes||0) + (nutrition.fruits||0)) / 2),
      attendu: 70,
      desc: "5 portions/jour recommandées",
      conseil: (s) => s >= 70 ? "Excellent ! Tu atteins les recommandations PNNS." : s >= 40 ? "Bien, mais essaie d'ajouter 1 fruit ou légume de plus par jour." : "Moins de 5 portions/jour — c'est le point le plus important à améliorer !"
    },
    {
      label: "Légumineuses",
      img: "/legumesec.png",
      couleur: "#795548",
      bg: "#efebe9",
      score: nutrition.legumineuses || 0,
      attendu: 60,
      desc: "2 fois/semaine recommandées",
      conseil: (s) => s >= 60 ? "Super ! Tu consommes bien les légumes secs." : s >= 30 ? "Essaie d'ajouter des lentilles ou pois chiches 1 fois de plus/semaine." : "Les légumineuses sont riches en fibres et protéines — à intégrer !"
    },
    {
      label: "Poisson",
      img: "/poisson.png",
      couleur: "#0288d1",
      bg: "#e1f5fe",
      score: nutrition.poisson || 0,
      attendu: 60,
      desc: "2 fois/semaine recommandées",
      conseil: (s) => s >= 60 ? "Parfait ! Tes apports en oméga-3 sont bons." : "Vise 2 portions/semaine, dont 1 poisson gras (sardine, saumon)."
    },
    {
      label: "Féculents complets",
      img: "/feculent.png",
      couleur: "#f57c00",
      bg: "#fff3e0",
      score: nutrition.feculents || 0,
      attendu: 60,
      desc: "À chaque repas, version complète",
      conseil: (s) => s >= 60 ? "Bien ! Les fibres des céréales complètes sont essentielles." : "Remplace pain blanc et pâtes blanches par leurs versions complètes."
    },
    {
      label: "Produits laitiers",
      img: "/lait2.png",
      couleur: "#1976d2",
      bg: "#e3f2fd",
      score: nutrition.laitiers || 0,
      attendu: 60,
      desc: "2 produits laitiers/jour",
      conseil: (s) => s >= 60 ? "Tes apports en calcium sont couverts !" : "2 produits laitiers/jour pour couvrir tes besoins en calcium."
    },
    {
      label: "À limiter",
      img: "/fast_food.png",
      img2: "/charcuterie.png",
      couleur: "#e53935",
      bg: "#fbe9e7",
      score: Math.round(((nutrition.charcuterie||0) + (nutrition.fastFood||0) + (nutrition.sucres||0)) / 3),
      attendu: 20,
      inverted: true,
      desc: "Charcuterie, fast-food, sucreries",
      conseil: (s) => s <= 20 ? "Excellent ! Tu limites bien les aliments à éviter." : s <= 50 ? "Essaie de réduire encore charcuterie et fast-food." : "Ces aliments sont trop fréquents — ils augmentent les risques cardiovasculaires."
    },
  ];

  const globalColor = avg >= 70 ? "#2e7d32" : avg >= 40 ? "#f57c00" : "#e53935";
  const globalBg    = avg >= 70 ? "#e8f5e9"  : avg >= 40 ? "#fff3e0"  : "#fbe9e7";
  const globalLabel = avg >= 70 ? "Excellentes habitudes !" : avg >= 40 ? "Habitudes correctes" : "Des progrès à faire";

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      {/* Fond i.jpg comme page 1 */}
      <div style={{ position:"relative", minHeight:"100vh" }}>
        <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", zIndex:0 }} />
        <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.62)", zIndex:0 }} />

        <div style={{ position:"relative", zIndex:1 }}>
          {/* Header */}
          <div style={{ padding:"16px 20px 0", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
            <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 16px" }}>← Retour</button>
          </div>

          {/* Titre style page 1 */}
          <div style={{ textAlign:"center", padding:"18px 20px 20px" }}>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:38, fontWeight:900, color:"#FA8072", textShadow:"3px 3px 0 #b2dfdb", margin:"0 0 6px", lineHeight:1.1 }}>
              Mon Profil<br/>Nutritionnel
            </h1>
            <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto" }} />
            <p style={{ color:"rgba(255,255,255,0.85)", fontSize:14, margin:0, fontWeight:600 }}>
              Bonjour <strong style={{ color:"#FA8072" }}>{playerName}</strong> — voici tes résultats
            </p>
          </div>

          {/* Score global */}
          <div style={{ margin:"0 20px 20px", background:globalBg, border:`3px solid ${globalColor}`, borderRadius:20, padding:"16px 20px", display:"flex", alignItems:"center", gap:16 }}>
            <div style={{ width:70, height:70, borderRadius:"50%", background:globalColor, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", flexShrink:0, boxShadow:`0 4px 16px ${globalColor}66` }}>
              <span style={{ fontSize:22, fontWeight:900, color:"white" }}>{avg}%</span>
            </div>
            <div>
              <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:globalColor }}>{globalLabel}</div>
              <div style={{ fontSize:12, color:"#555", marginTop:4, lineHeight:1.5 }}>
                {avg >= 70 ? "Tes habitudes sont proches des recommandations du PNNS !" :
                 avg >= 40 ? "Tu es sur la bonne voie, quelques ajustements suffisent." :
                 "Pas de panique — tes recommandations personnalisées vont t'aider."}
              </div>
            </div>
          </div>

          {/* Cartes catégories */}
          <div style={{ padding:"0 20px", display:"flex", flexDirection:"column", gap:12, marginBottom:20 }}>
            {CATEGORIES.map(cat => {
              const pct = cat.inverted
                ? Math.max(0, 100 - cat.score)
                : Math.min(cat.score, 100);
              const attPct = cat.inverted
                ? 100 - cat.attendu
                : cat.attendu;
              const ok = cat.inverted ? cat.score <= cat.attendu : cat.score >= cat.attendu;

              return (
                <div key={cat.label} style={{ background:"white", borderRadius:16, padding:"14px 16px", boxShadow:"0 4px 16px rgba(0,0,0,0.12)", border:`2px solid ${ok ? cat.couleur+"66" : "#e5353566"}` }}>
                  <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:10 }}>
                    {/* Images */}
                    <div style={{ display:"flex", gap:-6, flexShrink:0 }}>
                      <img src={cat.img} alt="" style={{ width:44, height:44, objectFit:"contain", filter:"drop-shadow(1px 2px 3px rgba(0,0,0,0.2))" }} />
                      {cat.img2 && <img src={cat.img2} alt="" style={{ width:36, height:36, objectFit:"contain", marginLeft:-8, filter:"drop-shadow(1px 2px 3px rgba(0,0,0,0.2))" }} />}
                    </div>
                    <div style={{ flex:1 }}>
                      <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#1A1A1A" }}>{cat.label}</div>
                      <div style={{ fontSize:11, color:"#888", marginTop:1 }}>{cat.desc}</div>
                    </div>
                    {/* Badge ok/ko */}
                    <div style={{ background: ok ? "#e8f5e9" : "#fbe9e7", border:`2px solid ${ok ? "#4caf50" : "#e53935"}`, borderRadius:20, padding:"3px 10px", fontSize:11, fontWeight:900, color: ok ? "#2e7d32" : "#c62828", flexShrink:0 }}>
                      {ok ? "✓ OK" : "↑ À améliorer"}
                    </div>
                  </div>

                  {/* Barre score vs attendu */}
                  <div style={{ position:"relative", height:14, background:"#f0f0f0", borderRadius:99, overflow:"visible", marginBottom:6 }}>
                    {/* Barre obtenu */}
                    <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99, transition:"width 0.8s ease" }} />
                    {/* Marqueur attendu */}
                    <div style={{ position:"absolute", top:-3, left:`${attPct}%`, transform:"translateX(-50%)", width:3, height:20, background:"#222", borderRadius:2, zIndex:2 }} />
                    <div style={{ position:"absolute", top:-18, left:`${attPct}%`, transform:"translateX(-50%)", fontSize:9, fontWeight:900, color:"#333", whiteSpace:"nowrap" }}>
                      objectif PNNS
                    </div>
                  </div>
                  <div style={{ display:"flex", justifyContent:"space-between", fontSize:10, color:"#888", marginBottom:8 }}>
                    <span style={{ color:cat.couleur, fontWeight:800 }}>Ton score : {cat.score}%</span>
                    <span>Objectif : {cat.inverted ? `≤ ${cat.attendu}%` : `≥ ${cat.attendu}%`}</span>
                  </div>

                  {/* Conseil */}
                  <div style={{ background:cat.bg, borderRadius:8, padding:"8px 10px", fontSize:11, color:"#444", lineHeight:1.5 }}>
                    💡 {cat.conseil(cat.score)}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Boutons */}
          <div style={{ padding:"0 20px 30px", display:"flex", flexDirection:"column", gap:12 }}>
            <button onClick={onVoirRecos}
              style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"4px 4px 0 #222", letterSpacing:0.5 }}>
              Mes recommandations PNNS →
            </button>
            <button onClick={() => onVoirRecettes("mediterraneen")}
              style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, padding:"13px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🫒 Voir les recettes adaptées →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

'''
    code = before + NEW_PROFIL + after
    fixes += 1
    print("✅ FIX 1 — Page Profil v2 : fond i.jpg, catégories, score vs objectif PNNS")
else:
    print("⚠️  FIX 1 — Marqueurs non trouvés")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/1 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
