"""
PATCH — Bouton Dashboard dans le menu quand toutes les missions sont terminées
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Ajouter santeCompleted dans props QcmSelectScreen
OLD_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked, completedMissions = [] }) {'
NEW_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked, completedMissions = [], onDashboard }) {'
if OLD_SIG in code:
    code = code.replace(OLD_SIG, NEW_SIG)
    fixes += 1; print("✅ FIX 1 — onDashboard ajouté dans signature")

# 2. Ajouter bouton dashboard si toutes missions terminées
OLD_MSG = '''      <div style={{ position:"absolute", bottom:24, left:0, right:0, zIndex:20, textAlign:"center" }}>
        <span style={{ fontSize:25, color:"#e72222", fontWeight:800, background:"rgba(255,255,255,0.85)", borderRadius:20, padding:"8px 24px", boxShadow:"0 2px 10px rgba(0,0,0,0.15)" }}>
          Clique sur un point pour commencer ta mission !
        </span>
      </div>'''

NEW_MSG = '''      <div style={{ position:"absolute", bottom:24, left:0, right:0, zIndex:20, textAlign:"center" }}>
        {completedMissions.length === 4 ? (
          <button onClick={onDashboard}
            style={{ fontSize:18, fontWeight:900, fontFamily:"Arial Black, Arial, sans-serif", background:"#ffdd44", border:"3px solid #222", borderRadius:20, padding:"12px 32px", boxShadow:"5px 5px 0 #222", cursor:"pointer", color:"#222" }}>
            📊 Consulter mon dashboard →
          </button>
        ) : (
          <span style={{ fontSize:25, color:"#e72222", fontWeight:800, background:"rgba(255,255,255,0.85)", borderRadius:20, padding:"8px 24px", boxShadow:"0 2px 10px rgba(0,0,0,0.15)" }}>
            Clique sur un point pour commencer ta mission !
          </span>
        )}
      </div>'''

if OLD_MSG in code:
    code = code.replace(OLD_MSG, NEW_MSG)
    fixes += 1; print("✅ FIX 2 — Bouton dashboard ajouté")
else:
    print("⚠️ FIX 2 — Message non trouvé")

# 3. Passer onDashboard au QcmSelectScreen depuis App
OLD_SELECT_CALL = '      onStartSante={() => { playSound("click"); goTo("qcm_sante"); }}\n      mission4Unlocked={mission4Unlocked}\n      completedMissions={completedMissions} />;'
NEW_SELECT_CALL = '      onStartSante={() => { playSound("click"); goTo("qcm_sante"); }}\n      mission4Unlocked={mission4Unlocked}\n      completedMissions={completedMissions}\n      onDashboard={() => alert("Dashboard en cours de développement !")} />;'
if OLD_SELECT_CALL in code:
    code = code.replace(OLD_SELECT_CALL, NEW_SELECT_CALL)
    fixes += 1; print("✅ FIX 3 — onDashboard branché")
else:
    print("⚠️ FIX 3 — Call non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
