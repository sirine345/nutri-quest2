"""
PATCH — Fix dashboard : condition plus souple + tracking mission 2
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Changer condition : afficher le bouton si mission 3 (sante) est terminée
OLD_COND = '{completedMissions.length === 4 ? ('
NEW_COND = '{completedMissions.includes(3) ? ('
if OLD_COND in code:
    code = code.replace(OLD_COND, NEW_COND)
    fixes += 1; print("✅ FIX 1 — Condition dashboard : includes(3)")

# 2. Tracker mission 1 (QCM2) quand onDone est appelé
OLD_QCM2_PHASE = "if(cuisine===\"recettes\") goTo(\"recettes\"); else if(cuisine===\"recos\" || cuisine===\"profil_qcm2\") goTo(\"profil_qcm2\")"
NEW_QCM2_PHASE = "setCompletedMissions(prev => prev.includes(1)?prev:[...prev,1]); if(cuisine===\"recettes\") goTo(\"recettes\"); else if(cuisine===\"recos\" || cuisine===\"profil_qcm2\") goTo(\"profil_qcm2\")"
if OLD_QCM2_PHASE in code:
    code = code.replace(OLD_QCM2_PHASE, NEW_QCM2_PHASE)
    fixes += 1; print("✅ FIX 2 — Mission QCM2 trackée")
else:
    print("⚠️ FIX 2 — QCM2 onDone non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
