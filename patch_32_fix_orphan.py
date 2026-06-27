"""
PATCH 32 — Supprimer le bouton orphelin lignes 2339-2342
Usage: python patch_32_fix_orphan.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find and remove the orphan button
to_remove = []
for i, l in enumerate(lines):
    if '          <button onClick={onBack}' in l:
        context = ''.join(lines[i:i+4])
        if 'Composer mon assiette' in context and '🥗' in context:
            # Check it's not inside a proper div
            to_remove.append((i, i+3))
            print(f"Bouton orphelin trouvé ligne {i+1}")

for start, end in reversed(to_remove):
    del lines[start:end+1]
    print(f"✅ Supprimé lignes {start+1}-{end+1}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
