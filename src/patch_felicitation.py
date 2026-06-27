"""
PATCH — Page félicitations après QCM Santé avec badge + bouton dashboard
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Ajouter state santeCompleted dans App
OLD_STATE = '  const [mission4Unlocked, setMission4Unlocked] = useState(false);'
NEW_STATE = '  const [mission4Unlocked, setMission4Unlocked] = useState(false);\n  const [santeCompleted, setSanteCompleted] = useState(false);'
if OLD_STATE in code:
    code = code.replace(OLD_STATE, NEW_STATE)
    fixes += 1; print("✅ FIX 1 — State santeCompleted ajouté")

# 2. Changer onDone de qcm_sante pour aller vers félicitations
OLD_DONE = 'if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setPhase("select"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;'
NEW_DONE = 'if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setSanteCompleted(true); setPhase("felicitations"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;'
if OLD_DONE in code:
    code = code.replace(OLD_DONE, NEW_DONE)
    fixes += 1; print("✅ FIX 2 — onDone redirige vers félicitations")

# 3. Ajouter la phase félicitations dans le switcher
OLD_SELECT = '    if (phase === "qcm_sante") return'
NEW_FELICIT = '''    if (phase === "felicitations") return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"40px 24px" }}>
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
        <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:24, maxWidth:520, width:"100%", textAlign:"center" }}>

          {/* Badge étoiles */}
          <div style={{ background:"linear-gradient(135deg, #ffdd44, #FA8072)", borderRadius:"50%", width:140, height:140, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", boxShadow:"0 0 40px rgba(255,220,50,0.6), 0 8px 32px rgba(0,0,0,0.4)", border:"4px solid #fff" }}>
            <div style={{ fontSize:48 }}>🏆</div>
            <div style={{ fontSize:22, color:"white" }}>★★★★★</div>
          </div>

          {/* Titre */}
          <div>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:"0 0 8px" }}>
              Félicitations {playerName} ! 🎉
            </h1>
            <p style={{ color:"rgba(255,255,255,0.85)", fontSize:16, margin:0, lineHeight:1.6 }}>
              Tu as complété toutes les missions nutritionnelles !<br/>
              Ton profil complet a été enregistré.
            </p>
          </div>

          {/* Récap badges */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12, width:"100%" }}>
            {[
              { icon:"🥗", label:"Habitudes alimentaires", color:"#FA8072" },
              { icon:"👨‍🍳", label:"Fabrique à Menus", color:"#ffcc00" },
              { icon:"🍽️", label:"Compose ton assiette", color:"#9ACD32" },
              { icon:"🏥", label:"Profil santé", color:"#7C3AED" },
            ].map((b,i) => (
              <div key={i} style={{ background:"rgba(255,255,255,0.15)", border:`2px solid ${b.color}`, borderRadius:14, padding:"12px 16px", display:"flex", alignItems:"center", gap:10 }}>
                <span style={{ fontSize:24 }}>{b.icon}</span>
                <div style={{ textAlign:"left" }}>
                  <div style={{ fontSize:12, fontWeight:800, color:"white" }}>{b.label}</div>
                  <div style={{ fontSize:11, color:"#ffdd44", fontWeight:700 }}>★★★★★ Complété</div>
                </div>
              </div>
            ))}
          </div>

          {/* Boutons */}
          <div style={{ display:"flex", flexDirection:"column", gap:12, width:"100%" }}>
            <button onClick={() => alert("Dashboard en cours de développement !")}
              style={{ background:"#ffdd44", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"5px 5px 0 #222" }}>
              📊 Accéder à mon dashboard →
            </button>
            <button onClick={() => { setPhase("select"); setPhaseHistory([]); }}
              style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:12, color:"white", fontSize:14, fontWeight:700, padding:"12px", cursor:"pointer" }}>
              ← Retour au menu
            </button>
          </div>

        </div>
      </div>
    );
    if (phase === "qcm_sante") return'''

if OLD_SELECT in code:
    code = code.replace(OLD_SELECT, NEW_FELICIT)
    fixes += 1; print("✅ FIX 3 — Page félicitations ajoutée")
else:
    print("⚠️ FIX 3 — Marker non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
