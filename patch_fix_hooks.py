"""
PATCH — Déplace useState openRec au niveau du composant QcmSanteScreen
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Ajouter useState openRec dans les states du composant
OLD_STATES = '''  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const hasPoids = evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince";'''

NEW_STATES = '''  const [openRec, setOpenRec] = useState(null);
  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const hasPoids = evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince";'''

if OLD_STATES in code:
    code = code.replace(OLD_STATES, NEW_STATES)
    fixes += 1; print("✅ FIX 1 — openRec déplacé dans les states")

# 2. Supprimer le useState du IIFE
OLD_IIFE = '''      {step===99 && (() => {
        const [openRec, setOpenRec] = useState(null);
        const medsRecs = RECETTES_DATA.filter(r => r.profils && r.profils.includes("mediterraneen"));'''

NEW_IIFE = '''      {step===99 && (() => {
        const medsRecs = RECETTES_DATA.filter(r => r.profils && r.profils.includes("mediterraneen"));'''

if OLD_IIFE in code:
    code = code.replace(OLD_IIFE, NEW_IIFE)
    fixes += 1; print("✅ FIX 2 — useState supprimé du IIFE")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
