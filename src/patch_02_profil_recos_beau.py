"""
PATCH 02 — Refonte page Profil (cartes aliments) + page Recommandations belle
Usage: python patch_02_profil_recos_beau.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ══ REMPLACEMENT COMPLET ProfilQcm1Screen ══
OLD_PROFIL = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {'''

NEW_PROFIL = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {'''

# Find the full ProfilQcm1Screen function and replace it entirely
import re

# Find start and end of ProfilQcm1Screen
start_marker = "/* ══ PAGE PROFIL QCM1 ══ */"
end_marker = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"

if start_marker in code and end_marker in code:
    before = code[:code.index(start_marker)]
    after = code[code.index(end_marker):]

    NEW_PROFIL_SCREEN = '''/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {
  const vals = Object.values(nutrition);
  const avg = vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;

  const getLevel = (score, inverted = false) => {
    if (inverted) {
      if (score <= 20) return { label:"Excellent", color:"#2e7d32", bg:"#e8f5e9" };
      if (score <= 50) return { label:"Modéré", color:"#f57c00", bg:"#fff3e0" };
      return { label:"Élevé ⚠️", color:"#c62828", bg:"#fbe9e7" };
    }
    if (score >= 70) return { label:"Excellent ✓", color:"#2e7d32", bg:"#e8f5e9" };
    if (score >= 40) return { label:"Correct", color:"#f57c00", bg:"#fff3e0" };
    return { label:"À améliorer", color:"#c62828", bg:"#fbe9e7" };
  };

  const globalLevel = getLevel(avg);

  const CARTES = [
    { key:"legumes",      label:"Légumes frais",     img:"/legume2.png",      inverted:false, conseil:"Visez 5 portions/jour (PNNS)" },
    { key:"fruits",       label:"Fruits",             img:"/fruit.png",        inverted:false, conseil:"Au moins 2 fruits entiers/jour" },
    { key:"legumineuses", label:"Légumes secs",       img:"/legumesec.png",    inverted:false, conseil:"2 fois/semaine recommandées" },
    { key:"feculents",    label:"Féculents complets", img:"/feculent.png",     inverted:false, conseil:"À chaque repas, version complète" },
    { key:"poisson",      label:"Poisson",            img:"/poisson.png",      inverted:false, conseil:"2 fois/semaine, dont 1 gras" },
    { key:"laitiers",     label:"Produits laitiers",  img:"/lait2.png",        inverted:false, conseil:"2 produits laitiers/jour" },
    { key:"volaille",     label:"Volaille",           img:"/volaille.png",     inverted:false, conseil:"Préférer à la viande rouge" },
    { key:"charcuterie",  label:"Charcuterie",        img:"/charcuterie.png",  inverted:true,  conseil:"Max 150g/semaine (OMS)" },
    { key:"fastFood",     label:"Fast food",          img:"/fast_food.png",    inverted:true,  conseil:"Limiter au maximum" },
    { key:"sucres",       label:"Sucreries",          img:"/sucrerie.png",     inverted:true,  conseil:"Limiter les sucres ajoutés" },
  ];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial Black, Arial, sans-serif", overflowY:"auto" }}>
      {/* Bannière */}
      <div style={{ position:"relative", height:200, overflow:"hidden" }}>
        <img src="/fond_rose.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)" }} />
        <div style={{ position:"absolute", top:0, left:0, right:0, padding:"14px 20px" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 16px" }}>← Retour</button>
        </div>
        <div style={{ position:"absolute", bottom:0, left:0, right:0, padding:"20px 24px" }}>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:36, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 rgba(0,0,0,0.4)", margin:"0 0 4px", letterSpacing:1 }}>
            Mon Profil Nutritionnel
          </h1>
          <p style={{ color:"rgba(255,255,255,0.9)", fontSize:14, margin:0, fontWeight:700 }}>Bonjour {playerName} — voici tes résultats personnalisés</p>
        </div>
      </div>

      <div style={{ padding:"20px" }}>
        {/* Score global */}
        <div style={{ background:globalLevel.bg, border:`3px solid ${globalLevel.color}`, borderRadius:20, padding:"20px 24px", marginBottom:24, display:"flex", alignItems:"center", gap:20, boxShadow:"0 4px 16px rgba(0,0,0,0.08)" }}>
          <div style={{ width:80, height:80, borderRadius:"50%", background:globalLevel.color, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", flexShrink:0, boxShadow:`0 4px 16px ${globalLevel.color}66` }}>
            <span style={{ fontSize:22, fontWeight:900, color:"white", lineHeight:1 }}>{avg}%</span>
            <span style={{ fontSize:9, fontWeight:800, color:"rgba(255,255,255,0.85)", textTransform:"uppercase", letterSpacing:1 }}>score</span>
          </div>
          <div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, color:globalLevel.color, marginBottom:6 }}>
              Score global : {globalLevel.label}
            </div>
            <div style={{ fontSize:13, color:"#555", lineHeight:1.6 }}>
              {avg >= 70 ? "Tes habitudes alimentaires sont excellentes ! Continue comme ça." :
               avg >= 40 ? "De bonnes habitudes, mais quelques points à améliorer." :
               "Plusieurs habitudes sont à revoir — les recommandations vont t'aider !"}
            </div>
          </div>
        </div>

        {/* Titre section */}
        <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"#FA8072", marginBottom:16, letterSpacing:0.5 }}>
          Tes groupes alimentaires
        </div>

        {/* Cartes aliments */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12, marginBottom:24 }}>
          {CARTES.map(c => {
            const score = nutrition[c.key] || 0;
            const lv = getLevel(score, c.inverted);
            const barScore = c.inverted ? Math.max(0, 100 - score) : score;
            return (
              <div key={c.key} style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 3px 12px rgba(0,0,0,0.08)", border:`2px solid ${lv.color}33` }}>
                {/* Image aliment */}
                <div style={{ height:80, background:lv.bg, display:"flex", alignItems:"center", justifyContent:"center", position:"relative" }}>
                  <img src={c.img} alt={c.label} style={{ height:65, objectFit:"contain", filter:"drop-shadow(2px 4px 4px rgba(0,0,0,0.15))" }} />
                  <div style={{ position:"absolute", top:8, right:8, background:lv.color, borderRadius:20, padding:"2px 8px", fontSize:9, fontWeight:900, color:"white", textTransform:"uppercase", letterSpacing:0.5 }}>
                    {lv.label}
                  </div>
                </div>
                {/* Contenu */}
                <div style={{ padding:"10px 12px" }}>
                  <div style={{ fontSize:12, fontWeight:900, color:"#1A1A1A", marginBottom:6 }}>{c.label}</div>
                  {/* Barre score */}
                  <div style={{ height:6, background:"#f0f0f0", borderRadius:99, overflow:"hidden", marginBottom:6 }}>
                    <div style={{ height:"100%", width:`${barScore}%`, background:lv.color, borderRadius:99 }} />
                  </div>
                  <div style={{ fontSize:10, color:"#888", lineHeight:1.4 }}>{c.conseil}</div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Boutons action */}
        <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"none", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.5)", letterSpacing:0.5 }}>
            Voir mes recommandations PNNS →
          </button>
          <button onClick={() => onVoirRecettes("mediterraneen")}
            style={{ background:"white", border:"3px solid #FA8072", borderRadius:14, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, padding:"14px", cursor:"pointer" }}>
            🫒 Recettes adaptées à mon profil →
          </button>
        </div>
      </div>
    </div>
  );
}

'''
    code = before + NEW_PROFIL_SCREEN + after
    fixes += 1
    print("✅ FIX 1 — Page Profil refaite avec cartes aliments")
else:
    print("⚠️  FIX 1 — Marqueurs non trouvés")

# ══ REMPLACEMENT COMPLET RecommandationsQcm1Screen ══
start_r = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
end_r   = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

if start_r in code and end_r in code:
    before_r = code[:code.index(start_r)]
    after_r  = code[code.index(end_r):]

    NEW_RECOS = '''/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const recos = [];
  if ((nutrition.legumes||0) < 60 || (nutrition.fruits||0) < 60) recos.push("legumes");
  if ((nutrition.legumineuses||0) < 50) recos.push("legumineuses");
  if ((nutrition.poisson||0) < 50) recos.push("poisson");
  if ((nutrition.charcuterie||0) > 20) recos.push("charcuterie");
  if ((nutrition.fastFood||0) > 20) recos.push("fastFood");
  if ((nutrition.sucres||0) > 20) recos.push("sucres");
  const getRecettes = (profil) => RECETTES_DATA.filter(r => r.profils && r.profils.includes(profil));

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      {/* Bannière */}
      <div style={{ position:"relative", height:200, overflow:"hidden" }}>
        <img src="/fond_vert3.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.4)" }} />
        <div style={{ position:"absolute", top:0, left:0, right:0, padding:"14px 20px" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 16px" }}>← Retour</button>
        </div>
        <div style={{ position:"absolute", bottom:0, left:0, padding:"20px 24px" }}>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:36, fontWeight:900, color:"#7FFFD4", textShadow:"2px 2px 0 rgba(0,0,0,0.4)", margin:"0 0 4px", letterSpacing:1 }}>
            Mes Recommandations
          </h1>
          <p style={{ color:"rgba(255,255,255,0.9)", fontSize:14, margin:0, fontWeight:700 }}>Personnalisées selon tes habitudes alimentaires</p>
        </div>
        {/* Images aliments déco */}
        <img src="/legume2.png" alt="" style={{ position:"absolute", right:60, bottom:-10, height:100, opacity:0.85, filter:"drop-shadow(2px 4px 8px rgba(0,0,0,0.3))" }} />
        <img src="/fruit.png" alt="" style={{ position:"absolute", right:10, bottom:-5, height:80, opacity:0.85, filter:"drop-shadow(2px 4px 8px rgba(0,0,0,0.3))" }} />
      </div>

      {/* Pills scores */}
      <div style={{ display:"flex", gap:10, padding:"16px 20px", overflowX:"auto" }}>
        {[
          ["🥦 Légumes & Fruits", nutrition.legumes||0, "#00BFA5","#E0F7F5"],
          ["🐟 Protéines", nutrition.poisson||0, "#7C3AED","#F3EEFF"],
          ["⚠️ À surveiller", Math.max(nutrition.charcuterie||0, nutrition.fastFood||0, nutrition.sucres||0), "#FF6B35","#FFF0EB"]
        ].map(([label, val, col, bg]) => (
          <div key={label} style={{ background:bg, borderRadius:14, padding:"12px 16px", textAlign:"center", minWidth:100, flexShrink:0, border:`2px solid ${col}33` }}>
            <div style={{ fontSize:20, fontWeight:900, color:col }}>{val}%</div>
            <div style={{ fontSize:10, color:col, fontWeight:800, marginTop:2 }}>{label}</div>
          </div>
        ))}
      </div>

      <div style={{ padding:"0 20px 20px" }}>
        {recos.length === 0 ? (
          <div style={{ background:"white", borderRadius:20, padding:"32px 24px", textAlign:"center", boxShadow:"0 4px 20px rgba(0,0,0,0.08)", border:"3px solid #9ACD32" }}>
            <div style={{ fontSize:48, marginBottom:12 }}>🎉</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"#9ACD32", marginBottom:8 }}>Excellentes habitudes !</div>
            <p style={{ fontSize:14, color:"#6B7280", lineHeight:1.6, margin:0 }}>Vos résultats sont proches des recommandations du PNNS. Continuez ainsi !</p>
          </div>
        ) : (
          <>
            <div style={{ fontSize:13, color:"#888", marginBottom:12, fontWeight:700 }}>{recos.length} point{recos.length > 1 ? "s" : ""} à améliorer</div>
            {recos.map(profil => (
              <RecoCard key={profil} reco={RECOMMANDATIONS[profil]} recettes={getRecettes(profil)} onVoirRecettes={onVoirRecettes} />
            ))}
          </>
        )}

        {/* Bloc méditerranéen */}
        <div style={{ background:"white", borderRadius:20, overflow:"hidden", marginTop:12, boxShadow:"0 4px 20px rgba(0,0,0,0.08)", border:"3px solid #9ACD32" }}>
          <div style={{ position:"relative", height:100, overflow:"hidden" }}>
            <img src="/salade_grecque.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
            <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)", display:"flex", alignItems:"center", padding:"0 20px" }}>
              <div>
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"#7FFFD4", textShadow:"1px 1px 0 rgba(0,0,0,0.5)" }}>🫒 Régime Méditerranéen</div>
                <div style={{ fontSize:12, color:"rgba(255,255,255,0.85)", marginTop:2 }}>Recommandé par le PNNS</div>
              </div>
            </div>
          </div>
          <div style={{ padding:"16px 20px" }}>
            <p style={{ fontSize:13, color:"#6B7280", lineHeight:1.6, margin:"0 0 14px" }}>Fruits, légumes, légumineuses, poisson et huile d'olive — réduit les risques cardiovasculaires.</p>
            <button onClick={() => onVoirRecettes("mediterraneen")}
              style={{ background:"#9ACD32", color:"white", border:"none", borderRadius:12, padding:"13px 20px", fontSize:13, fontWeight:900, cursor:"pointer", width:"100%", fontFamily:"Arial Black, Arial, sans-serif" }}>
              Découvrir les recettes →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

'''
    code = before_r + NEW_RECOS + after_r
    fixes += 1
    print("✅ FIX 2 — Page Recommandations refaite (belle, même thème)")
else:
    print("⚠️  FIX 2 — Marqueurs RecommandationsQcm1Screen non trouvés")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/2 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
