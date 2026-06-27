"""
PATCH — Nettoie les doublons et ajoute onMinijeu proprement
Usage: python patch_clean_recos_qcm2.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Supprimer toutes les lignes qui contiennent 'phase === "recos_qcm2"' en doublons
# Garder seulement UNE ligne propre
recos_lines = [(i, l) for i, l in enumerate(lines) if 'phase === "recos_qcm2"' in l]
print(f"Lignes recos_qcm2 trouvées: {[i+1 for i,l in recos_lines]}")

# Supprimer toutes ces lignes
for i, _ in reversed(recos_lines):
    del lines[i]

# Pareil pour intro_recos_qcm2 et profil_qcm2 doublons
for phase in ['phase === "intro_recos_qcm2"', 'phase === "profil_qcm2"']:
    phase_lines = [(i, l) for i, l in enumerate(lines) if phase in l]
    print(f"{phase}: {[i+1 for i,l in phase_lines]}")
    if len(phase_lines) > 1:
        for i, _ in reversed(phase_lines[1:]):  # garde la première
            del lines[i]

# Trouver où insérer les nouvelles lignes — juste avant QcmSelectScreen return
insert_idx = next(i for i, l in enumerate(lines) if 'return <QcmSelectScreen' in l)

new_lines = [
    '    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("intro_recos_qcm2")} />;\n',
    '    if (phase === "intro_recos_qcm2") return <IntroRecosQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm2")} onVoirRecettes={() => { setFiltreRecetteProfil(null); goTo("recettes"); }} />;\n',
    '    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onMinijeu={() => { setPhase("minijeu"); setPhaseHistory([]); }} />;\n',
]

# Remove existing profil_qcm2 and intro_recos_qcm2 lines too
for phase in ['phase === "profil_qcm2"', 'phase === "intro_recos_qcm2"']:
    phase_lines = [(i, l) for i, l in enumerate(lines) if phase in l]
    for i, _ in reversed(phase_lines):
        del lines[i]

# Recalculate insert position
insert_idx = next(i for i, l in enumerate(lines) if 'return <QcmSelectScreen' in l)
for nl in reversed(new_lines):
    lines.insert(insert_idx, nl)

print("✅ Phases nettoyées et réinsérées avec onMinijeu")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
