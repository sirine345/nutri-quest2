"""
PATCH 41 — Fix TOUS les problèmes restants:
1. Regex avec caractères accentués (vraie cause du 500)
2. Apostrophes dans textes JSX
Usage: python patch_41_fix_all_remaining.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0

# FIX 1 — Regex ligne 2076 avec àâéèêëîïôùûüç → simplifier
for i, l in enumerate(lines):
    if 'ing.match' in l and ('àâé' in l or '\xc3' in l):
        lines[i] = "    const m = ing.match(/^([\\d]+(?:[.,][\\d]+)?)\\s*([a-zA-Z]+(?:\\s?[a-z]+)?)?\\s+(.+)$/);\n"
        fixes += 1
        print(f"✅ FIX 1 — Regex ligne {i+1} simplifiée")
        break

# FIX 2 — Apostrophes dans textes JSX
TEXT_FIXES = [
    ("Tu n'as pas coché", "Tu n&apos;as pas coché"),
    ("manque d'appétit", "manque d&apos;appétit"),
    ("Avez-vous l'une de ces pathologies", "Avez-vous l&apos;une de ces pathologies"),
    ("Qu'est-ce qui vous empêche", "Qu&apos;est-ce qui vous empêche"),
    ("Le patient présente-t-il une perte d'appétit", "Le patient présente-t-il une perte d&apos;appétit"),
    ("catégorie d'âge", "catégorie d&apos;âge"),
    ("celle d'il y a 6 mois", "celle d&apos;il y a 6 mois"),
    ("A-t-il moins mangé ces 3 derniers mois par manque d'appétit", "A-t-il moins mangé ces 3 derniers mois par manque d&apos;appétit"),
]

for old, new in TEXT_FIXES:
    replaced = False
    for i, l in enumerate(lines):
        if old in l:
            lines[i] = l.replace(old, new)
            fixes += 1
            print(f"✅ FIX 2 — L{i+1}: {old[:50]}")
            replaced = True
    if not replaced:
        print(f"⚠️  Non trouvé: {old[:50]}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
