"""
Fix — Bouton "Suivant → Composer mon assiette" redirige vers minijeu
Usage: python patch_fix_compose_assiette.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Le bouton appelle onBack() — on change la phase recos_qcm2 pour que onBack → minijeu
OLD = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => { setPhase("select"); setPhaseHistory([]); }} />;'
NEW = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goTo("minijeu")} />;'

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ Bouton 'Composer mon assiette' redirige vers le mini-jeu")
else:
    print("⚠️  Ligne non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
