"""
PATCH — Ajoute onMinijeu dans la signature de RecommandationsQcm2Screen
Usage: python patch_add_onminijeu_signature.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = 'function RecommandationsQcm2Screen({ answers, playerName, avatarChoice, onBack }) {'
NEW = 'function RecommandationsQcm2Screen({ answers, playerName, avatarChoice, onBack, onMinijeu }) {'

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ onMinijeu ajouté dans la signature de RecommandationsQcm2Screen")
else:
    print("⚠️  Signature non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
