"""
PATCH 35 — Corrige toutes les apostrophes dans les textes JSX directs
Usage: python patch_35_fix_jsx_apostrophes.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# Toutes les lignes de texte JSX avec apostrophes à corriger
replacements = [
    # Ligne 254
    ("Bonjour <strong>{playerName}</strong> ! Choisis ton personnage pour commencer l'aventure",
     "Bonjour <strong>{playerName}</strong> ! Choisis ton personnage pour commencer l&apos;aventure"),
    # Ligne 348
    ("          Commencer l'aventure →",
     "          Commencer l&apos;aventure →"),
    # Ligne 1907
    ("              Génial ! J'ai hâte de voir ! 😍",
     "              {\"Génial ! J'ai hâte de voir ! 😍\"}"),
    # Ligne 2391
    ("            D'accord Max, j'ai hâte de voir ! 👀",
     "            {\"D'accord Max, j'ai hâte de voir ! 👀\"}"),
    # Ligne 4412
    ("          C'est parti ! →",
     "          C&apos;est parti ! →"),
    # Ligne 2050 - fix the broken t'amuser
    ('viens {\\"t\'amuser\\"} en',
     "viens {\"t'amuser\"} en"),
    ("viens {\"t\\'amuser\"} en",
     "viens {\"t'amuser\"} en"),
]

for old, new in replacements:
    if old in code:
        code = code.replace(old, new)
        fixes += 1
        print(f"✅ Corrigé: {old[:60].strip()}")

# Ligne 1504 - "Le trait noir" - check if it has apostrophe issue
if "Le trait noir sur chaque barre indique l" in code:
    old = "Le PNNS fixe des objectifs de consommation pour chaque groupe alimentaire. Le trait noir"
    # This one might be fine as it doesn't have apostrophe
    pass

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
