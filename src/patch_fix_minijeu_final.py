"""
Fix final — Bouton composer assiette vers minijeu
1. Supprime les doublons de phases recos_qcm2 et profil_qcm2
2. Ajoute onMinijeu prop au composant
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0

# FIX 1 — Supprimer les lignes dupliquées 5097-5099 (0-indexed: 5096-5098)
# Garder la ligne 5092 (première occurrence de recos_qcm2)
# Supprimer les lignes 5097, 5098, 5099
lines_to_remove = []
for i, l in enumerate(lines):
    # Lignes dupliquées ajoutées par patch_fix_recos_qcm2_phase.py
    if i >= 5094 and i <= 5099:
        if 'recos_qcm2' in l or 'profil_qcm2' in l or 'intro_recos_qcm2' in l:
            lines_to_remove.append(i)

for i in reversed(lines_to_remove):
    del lines[i]
    fixes += 1

print(f"✅ FIX 1 — {len(lines_to_remove)} ligne(s) dupliquée(s) supprimée(s)")

# FIX 2 — Modifier le bouton dans RecommandationsQcm2Screen
# Le bouton appelle onBack() — on le change pour appeler onMinijeu()
code = ''.join(lines)

OLD_BTN = '''            <button onClick={() => onBack()}
              style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Suivant → Composer mon assiette
            </button>'''

NEW_BTN = '''            <button onClick={() => onMinijeu && onMinijeu()}
              style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Suivant → Composer mon assiette
            </button>'''

if OLD_BTN in code:
    code = code.replace(OLD_BTN, NEW_BTN)
    fixes += 1
    print("✅ FIX 2 — Bouton appelle onMinijeu()")
else:
    # Try simpler replace
    OLD2 = '<button onClick={() => onBack()}\n              style={{ width:"100%", background:"#9ACD32"'
    NEW2 = '<button onClick={() => onMinijeu && onMinijeu()}\n              style={{ width:"100%", background:"#9ACD32"'
    if OLD2 in code:
        code = code.replace(OLD2, NEW2)
        fixes += 1
        print("✅ FIX 2 — Bouton corrigé (v2)")
    else:
        print("⚠️  FIX 2 — Bouton non trouvé")

# FIX 3 — Modifier la phase recos_qcm2 pour passer onMinijeu
import re
m = re.search(r'if \(phase === "recos_qcm2"\) return <RecommandationsQcm2Screen[^\n]+\n', code)
if m:
    old_line = m.group(0)
    # Add onMinijeu prop
    if 'onMinijeu' not in old_line:
        new_line = old_line.replace(
            'onBack={() => goBack()}',
            'onBack={() => goBack()} onMinijeu={() => { setPhase("minijeu"); setPhaseHistory([]); }}'
        )
        if new_line != old_line:
            code = code.replace(old_line, new_line)
            fixes += 1
            print("✅ FIX 3 — onMinijeu ajouté dans phase recos_qcm2")
        else:
            print("⚠️  FIX 3 — onBack non trouvé dans la ligne")
    else:
        print("✅ FIX 3 — onMinijeu déjà présent")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes} fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
