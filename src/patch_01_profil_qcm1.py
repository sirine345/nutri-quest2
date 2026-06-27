"""
PATCH 01 — Page Profil + Recommandations après QCM1
Usage: python patch_01_profil_qcm1.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ── BLOC A : Nouveau composant ProfilQcm1Screen ──
NOUVEAU_COMPOSANT = '''
/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {
  const vals = Object.values(nutrition);
  const avg = vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;

  const getLevel = (score, inverted = false) => {
    if (inverted) {
      if (score <= 20) return { label:"Excellent", color:"#2e7d32", bg:"#e8f5e9" };
      if (score <= 50) return { label:"Modéré", color:"#f57c00", bg:"#fff3e0" };
      return { label:"Élevé", color:"#c62828", bg:"#fbe9e7" };
    }
    if (score >= 70) return { label:"Excellent", color:"#2e7d32", bg:"#e8f5e9" };
    if (score >= 40) return { label:"Correct", color:"#f57c00", bg:"#fff3e0" };
    return { label:"À améliorer", color:"#c62828", bg:"#fbe9e7" };
  };

  const globalLevel = getLevel(avg);

  const NUTRIMENTS = [
    { key:"legumes",      label:"Légumes frais",     icon:"🥦", inverted:false },
    { key:"fruits",       label:"Fruits",             icon:"🍎", inverted:false },
    { key:"legumineuses", label:"Légumes secs",       icon:"🫘", inverted:false },
    { key:"feculents",    label:"Féculents complets", icon:"🌾", inverted:false },
    { key:"poisson",      label:"Poisson",            icon:"🐟", inverted:false },
    { key:"laitiers",     label:"Produits laitiers",  icon:"🥛", inverted:false },
    { key:"charcuterie",  label:"Charcuterie",        icon:"🥓", inverted:true  },
    { key:"fastFood",     label:"Fast food",          icon:"🍔", inverted:true  },
    { key:"sucres",       label:"Sucreries",          icon:"🍬", inverted:true  },
  ];

  return (
    <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <div style={{ background:"#FA8072" }}>
        <div style={{ padding:"14px 20px" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour</button>
        </div>
        <div style={{ padding:"8px 20px 28px" }}>
          <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"rgba(255,255,255,0.2)", borderRadius:20, padding:"4px 12px", marginBottom:12 }}>
            <span style={{ fontSize:11, fontWeight:800, color:"white", textTransform:"uppercase", letterSpacing:1 }}>Bilan alimentaire</span>
          </div>
          <h1 style={{ fontSize:28, fontWeight:900, color:"white", margin:"0 0 6px" }}>Mon profil nutritionnel</h1>
          <p style={{ color:"rgba(255,255,255,0.85)", fontSize:14, margin:0 }}>Bonjour <strong>{playerName}</strong> — voici tes résultats</p>
        </div>
      </div>

      <div style={{ padding:"20px" }}>
        <div style={{ background:globalLevel.bg, border:`2px solid ${globalLevel.color}`, borderRadius:20, padding:"20px 24px", marginBottom:20, display:"flex", alignItems:"center", gap:20 }}>
          <div style={{ width:72, height:72, borderRadius:"50%", background:globalLevel.color, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
            <span style={{ fontSize:24, fontWeight:900, color:"white" }}>{avg}%</span>
          </div>
          <div>
            <div style={{ fontSize:18, fontWeight:900, color:globalLevel.color }}>Score global : {globalLevel.label}</div>
            <div style={{ fontSize:13, color:"#555", marginTop:4, lineHeight:1.5 }}>
              {avg >= 70 ? "Tes habitudes alimentaires sont excellentes ! Continue comme ça." :
               avg >= 40 ? "De bonnes habitudes, mais quelques points à améliorer." :
               "Plusieurs habitudes sont à revoir — les recommandations vont t'aider !"}
            </div>
          </div>
        </div>

        <div style={{ background:"white", borderRadius:20, padding:"20px", marginBottom:20, boxShadow:"0 2px 12px rgba(0,0,0,0.06)", border:"1px solid #E8EDF2" }}>
          <div style={{ fontSize:14, fontWeight:900, color:"#1A1A1A", marginBottom:16 }}>Détail par groupe alimentaire</div>
          {NUTRIMENTS.map(n => {
            const score = nutrition[n.key] || 0;
            const lv = getLevel(score, n.inverted);
            const barScore = n.inverted ? Math.max(0, 100 - score) : score;
            return (
              <div key={n.key} style={{ marginBottom:14 }}>
                <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:4 }}>
                  <span style={{ fontSize:13, fontWeight:700, color:"#333" }}>{n.icon} {n.label}</span>
                  <span style={{ fontSize:11, fontWeight:900, color:lv.color, background:lv.bg, borderRadius:20, padding:"2px 10px" }}>{lv.label}</span>
                </div>
                <div style={{ height:8, background:"#f0f0f0", borderRadius:99, overflow:"hidden" }}>
                  <div style={{ height:"100%", width:`${barScore}%`, background:lv.color, borderRadius:99, transition:"width 0.6s ease" }} />
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.4)" }}>
            Voir mes recommandations PNNS →
          </button>
          <button onClick={() => onVoirRecettes("mediterraneen")}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:14, color:"#FA8072", fontSize:14, fontWeight:800, padding:"14px", cursor:"pointer" }}>
            🫒 Découvrir les recettes adaptées →
          </button>
        </div>
      </div>
    </div>
  );
}

'''

# Insère avant /* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
MARKER = '/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */'
if MARKER in code:
    code = code.replace(MARKER, NOUVEAU_COMPOSANT + MARKER)
    fixes += 1
    print("✅ FIX 1 — Composant ProfilQcm1Screen ajouté")
else:
    print("⚠️  FIX 1 — Marqueur non trouvé")

# ── BLOC B : onShowRecos redirige vers profil_qcm1 au lieu de recos_qcm1 ──
OLD_SHOW_RECOS = 'onShowRecos={(nut) => { setQcm1Nutrition(nut); goTo("recos_qcm1"); }}'
NEW_SHOW_RECOS = 'onShowRecos={(nut) => { setQcm1Nutrition(nut); goTo("profil_qcm1"); }}'
if OLD_SHOW_RECOS in code:
    code = code.replace(OLD_SHOW_RECOS, NEW_SHOW_RECOS)
    fixes += 1
    print("✅ FIX 2 — QCM1 redirige vers profil_qcm1")
else:
    print("⚠️  FIX 2 — onShowRecos non trouvé")

# ── BLOC C : Ajouter la phase profil_qcm1 dans le screen switcher ──
OLD_RECOS_LINE = 'if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'
NEW_RECOS_LINE = '''if (phase === "profil_qcm1") return <ProfilQcm1Screen nutrition={qcm1Nutrition} playerName={playerName} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm1")} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;
    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'''
if OLD_RECOS_LINE in code:
    code = code.replace(OLD_RECOS_LINE, NEW_RECOS_LINE)
    fixes += 1
    print("✅ FIX 3 — Phase profil_qcm1 ajoutée dans App")
else:
    print("⚠️  FIX 3 — Ligne recos_qcm1 non trouvée")

# Écriture
out = sys.argv[1].replace('.jsx', '_patched.jsx') if len(sys.argv) > 1 else 'App_patched.jsx'
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/3 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Renomme-le en App.jsx et remplace l'original")
