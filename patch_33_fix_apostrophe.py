"""
PATCH 33 — Remplace l'apostrophe problématique dans t'amuser
Usage: python patch_33_fix_apostrophe.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = "Maintenant que tu as ton planning de la semaine, viens t'amuser en <strong style={{ color:\"#FA8072\" }}>composant ton assiette idéale</strong> dans le mini-jeu ! 🎮"
NEW = "Maintenant que tu as ton planning, viens {"+"\"t'amuser\"} en <strong style={{ color:\"#FA8072\" }}>composant ton assiette idéale</strong> dans le mini-jeu ! 🎮"

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ Apostrophe corrigée")
else:
    # Essai direct sur la ligne
    lines = code.split('\n')
    for i, l in enumerate(lines):
        if "t'amuser" in l and 'planning' in l:
            lines[i] = l.replace("viens t'amuser en", "viens {\"t'amuser\"} en")
            print(f"✅ Ligne {i+1} corrigée")
            break
    code = '\n'.join(lines)

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
