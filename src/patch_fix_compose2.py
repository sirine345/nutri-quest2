"""
Fix — Bouton composer assiette va vers minijeu directement
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Le onBack de recos_qcm2 va vers intro_recos_qcm2 car c'est dans l'historique
# Il faut vider l'historique et aller vers minijeu
OLD = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goTo("minijeu")} />;'
NEW = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => { setPhase("minijeu"); setPhaseHistory([]); }} />;'

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ onBack redirige vers minijeu (historique vidé)")
else:
    print("⚠️  Non trouvé, essai v2...")
    import re
    m = re.search(r'if \(phase === "recos_qcm2"\)[^\n]+', code)
    if m:
        old_line = m.group(0)
        new_line = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => { setPhase("minijeu"); setPhaseHistory([]); }} />;'
        code = code.replace(old_line, new_line)
        print("✅ Corrigé (v2)")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
