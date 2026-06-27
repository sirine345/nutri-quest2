"""
Fix — Ajoute la phase recos_qcm2 dans le screen switcher
Usage: python patch_fix_recos_qcm2_phase.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Find the default return (QcmSelectScreen) and add phases before it
OLD = '    return <QcmSelectScreen playerName={playerName}'
NEW = '''    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => { setPhase("select"); setPhaseHistory([]); }} />;
    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("intro_recos_qcm2")} />;
    if (phase === "intro_recos_qcm2") return <IntroRecosQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm2")} onVoirRecettes={() => { setFiltreRecetteProfil(null); goTo("recettes"); }} />;
    return <QcmSelectScreen playerName={playerName}'''

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ Phases recos_qcm2, profil_qcm2, intro_recos_qcm2 ajoutées")
else:
    print("⚠️  Marqueur non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
