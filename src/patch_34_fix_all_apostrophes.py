"""
PATCH 34 — Corrige toutes les apostrophes problématiques dans les textes JSX
Usage: python patch_34_fix_all_apostrophes.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0

replacements = [
    # Ligne 1907 - texte JSX direct avec apostrophe
    ("              Génial ! J'ai hâte de voir ! 😍\n",
     "              {\"Génial ! J'ai hâte de voir ! 😍\"}\n"),
    # Ligne 2391
    ("            D'accord Max, j'ai hâte de voir ! 👀\n",
     "            {\"D'accord Max, j'ai hâte de voir ! 👀\"}\n"),
    # t'amuser fix - enlever les backslashes
    ('viens {\\"t\'amuser\\"} en',
     "viens {\"t'amuser\"} en"),
    # Alternate t'amuser format
    ("viens {\"t\\'amuser\"} en",
     "viens {\"t'amuser\"} en"),
]

code = ''.join(lines)

for old, new in replacements:
    if old in code:
        code = code.replace(old, new)
        fixes += 1
        print(f"✅ Corrigé: {old[:50].strip()}")
    else:
        print(f"⚠️  Non trouvé: {old[:50].strip()}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
