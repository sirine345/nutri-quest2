"""
PATCH — Étoiles sur les cercles des missions terminées
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Ajouter state completedMissions dans App
OLD_STATE = '  const [mission4Unlocked, setMission4Unlocked] = useState(false);'
NEW_STATE = '  const [mission4Unlocked, setMission4Unlocked] = useState(false);\n  const [completedMissions, setCompletedMissions] = useState([]);'
if OLD_STATE in code:
    code = code.replace(OLD_STATE, NEW_STATE)
    fixes += 1; print("✅ FIX 1 — State completedMissions ajouté")

# 2. Marquer mission 0 (qcm1) comme terminée quand onDone est appelé
OLD_QCM1_DONE = 'onShowRecos={(nut) => { setQcm1Nutrition(nut); goTo("profil_qcm1"); }}'
NEW_QCM1_DONE = 'onDone={(nut) => { setQcm1Nutrition(nut); setCompletedMissions(prev => prev.includes(0)?prev:[...prev,0]); }} onShowRecos={(nut) => { setQcm1Nutrition(nut); goTo("profil_qcm1"); }}'
if OLD_QCM1_DONE in code:
    code = code.replace(OLD_QCM1_DONE, NEW_QCM1_DONE)
    fixes += 1; print("✅ FIX 2 — Mission 1 marquée terminée")

# 3. Marquer mission 1 (qcm2) comme terminée
OLD_QCM2_DONE = 'if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos" || cuisine==="profil_qcm2") goTo("profil_qcm2")'
NEW_QCM2_DONE = 'setCompletedMissions(prev => prev.includes(1)?prev:[...prev,1]); if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos" || cuisine==="profil_qcm2") goTo("profil_qcm2")'
if OLD_QCM2_DONE in code:
    code = code.replace(OLD_QCM2_DONE, NEW_QCM2_DONE)
    fixes += 1; print("✅ FIX 3 — Mission 2 marquée terminée")

# 4. Marquer mission 2 (minijeu) comme terminée quand onBack
OLD_MINIJEU = 'onBack={() => { setMission4Unlocked(true); setPhase("select_mission4"); setPhaseHistory([]); }}'
NEW_MINIJEU = 'onBack={() => { setMission4Unlocked(true); setCompletedMissions(prev => prev.includes(2)?prev:[...prev,2]); setPhase("select_mission4"); setPhaseHistory([]); }}'
if OLD_MINIJEU in code:
    code = code.replace(OLD_MINIJEU, NEW_MINIJEU)
    fixes += 1; print("✅ FIX 4 — Mission 3 marquée terminée")

# 5. Marquer mission 3 (sante) comme terminée
OLD_SANTE_DONE = 'onDone={(data) => { setSanteData(data); setSanteCompleted(true); setPhase("felicitations"); setPhaseHistory([]); }}'
NEW_SANTE_DONE = 'onDone={(data) => { setSanteData(data); setSanteCompleted(true); setCompletedMissions(prev => prev.includes(3)?prev:[...prev,3]); setPhase("felicitations"); setPhaseHistory([]); }}'
if OLD_SANTE_DONE in code:
    code = code.replace(OLD_SANTE_DONE, NEW_SANTE_DONE)
    fixes += 1; print("✅ FIX 5 — Mission 4 marquée terminée")

# 6. Passer completedMissions au QcmSelectScreen
OLD_SELECT_CALL = '      mission4Unlocked={mission4Unlocked} />;'
NEW_SELECT_CALL = '      mission4Unlocked={mission4Unlocked}\n      completedMissions={completedMissions} />;'
if OLD_SELECT_CALL in code:
    code = code.replace(OLD_SELECT_CALL, NEW_SELECT_CALL)
    fixes += 1; print("✅ FIX 6 — completedMissions passé au QcmSelectScreen")

# 7. Ajouter completedMissions dans signature QcmSelectScreen
OLD_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked }) {'
NEW_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked, completedMissions = [] }) {'
if OLD_SIG in code:
    code = code.replace(OLD_SIG, NEW_SIG)
    fixes += 1; print("✅ FIX 7 — Signature mise à jour")

# 8. Afficher étoiles sur les cercles terminés
OLD_CIRCLE = '''            <div onClick={() => { if(isLocked) return; playSound("click"); m.action && m.action(); }}
              style={{ width:90, height:90, borderRadius:"50%", background: isLocked?"#bbb":m.color, border:"3px solid white", cursor:isLocked?"not-allowed":"pointer", display:"flex", alignItems:"center", justifyContent:"center", fontSize:18, fontWeight:900, color:"white", boxShadow:`0 4px 16px ${isLocked?"#bbb":m.color}88`, transform: hovered===m.id && !isLocked ? "scale(1.2)" : "scale(1)", transition:"transform 0.2s", opacity:isLocked?0.5:1 }}>
              {isLocked ? "🔒" : m.id + 1}
            </div>'''

NEW_CIRCLE = '''            <div onClick={() => { if(isLocked) return; playSound("click"); m.action && m.action(); }}
              style={{ width:90, height:90, borderRadius:"50%", background: isLocked?"#bbb":m.color, border:"3px solid white", cursor:isLocked?"not-allowed":"pointer", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", fontSize:completedMissions.includes(m.id)?11:18, fontWeight:900, color:"white", boxShadow:`0 4px 16px ${isLocked?"#bbb":m.color}88`, transform: hovered===m.id && !isLocked ? "scale(1.2)" : "scale(1)", transition:"transform 0.2s", opacity:isLocked?0.5:1 }}>
              {isLocked ? "🔒" : completedMissions.includes(m.id) ? (
                <><div style={{ fontSize:20 }}>✓</div><div style={{ fontSize:10, letterSpacing:1 }}>★★★★★</div></>
              ) : m.id + 1}
            </div>'''

if OLD_CIRCLE in code:
    code = code.replace(OLD_CIRCLE, NEW_CIRCLE)
    fixes += 1; print("✅ FIX 8 — Étoiles affichées sur missions terminées")
else:
    print("⚠️ FIX 8 — Cercle non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
