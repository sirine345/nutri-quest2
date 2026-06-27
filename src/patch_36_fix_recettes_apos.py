"""
PATCH 36 — Corrige l'apostrophe ligne 2336 dans RecettesScreen
Usage: python patch_36_fix_recettes_apos.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

replacements = [
    (">Essayez d'autres filtres</div>", ">Essayez d&apos;autres filtres</div>"),
    ("← Toutes les recettes\n          </button>", "← Toutes les recettes\n          </button>"),
    ("Voir sur {r.source} →\n            </a>", "Voir sur {r.source} →\n            </a>"),
    (">Voir la recette →\n                </div>", ">Voir la recette →\n                </div>"),
    ("← Retour\n          </button>", "← Retour\n          </button>"),
]

for old, new in replacements:
    if old != new and old in code:
        code = code.replace(old, new)
        fixes += 1
        print(f"✅ {old[:50]}")

# Main fix
old = ">Essayez d'autres filtres</div>"
new = ">Essayez d&apos;autres filtres</div>"
if old in code:
    code = code.replace(old, new)
    fixes += 1
    print("✅ Apostrophe ligne 2336 corrigée")
else:
    print("⚠️  Non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
