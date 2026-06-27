"""
PATCH — Remplace onBack par onMinijeu sur le bouton Composer mon assiette
Usage: python patch_fix_onclick_minijeu.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0
for i, l in enumerate(lines):
    if 'Composer mon assiette' in lines[i] if i < len(lines) else False:
        pass
    # Find the button onClick just before "Composer mon assiette"
    if 'onClick={onBack}' in l and i+2 < len(lines) and 'Composer mon assiette' in lines[i+2]:
        lines[i] = l.replace('onClick={onBack}', 'onClick={() => onMinijeu && onMinijeu()}')
        fixes += 1
        print(f"✅ L{i+1} — onClick remplacé par onMinijeu")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
