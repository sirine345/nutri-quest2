"""
PATCH — Fix 2 bugs :
1. QCM2 step 5 : {repas===o} → {o}
2. QCM Santé step 11 : useState dans IIFE → déplacé dans le composant
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# ─── FIX 1 : {repas===o} → {o} ───
OLD_REPAS = '              {repas===o}\n            </div>'
NEW_REPAS = '              {o}\n            </div>'
if OLD_REPAS in code:
    code = code.replace(OLD_REPAS, NEW_REPAS)
    fixes += 1; print("✅ FIX 1 — {repas===o} → {o}")

# ─── FIX 2 : Déplacer states MNA hors du IIFE ───
# Add mnaStep and mnaAnswers to QcmSanteScreen states
OLD_SANTE_STATES = '  const [openRec, setOpenRec] = useState(null);\n  const hasLLC = pathologies.some(p => p.includes("LLC"));'
NEW_SANTE_STATES = '  const [openRec, setOpenRec] = useState(null);\n  const [mnaStep, setMnaStep] = useState(0);\n  const [mnaAnswers, setMnaAnswers] = useState({});\n  const hasLLC = pathologies.some(p => p.includes("LLC"));'
if OLD_SANTE_STATES in code:
    code = code.replace(OLD_SANTE_STATES, NEW_SANTE_STATES)
    fixes += 1; print("✅ FIX 2a — States MNA ajoutés dans QcmSanteScreen")

# Replace the IIFE step 11 with proper JSX (no useState inside)
OLD_STEP11 = '''      {step===11 && (() => {
        const MNA_QS = [
          { q:"Le patient présente-t-il une perte d'appétit ces 3 derniers mois ?", opts:[[0,"Baisse sévère"],[1,"Légère baisse"],[2,"Pas de baisse"]], key:"appetit" },
          { q:"Perte de poids récente (< 3 mois) ?", opts:[[0,"Perte > 3 kg"],[1,"Ne sait pas"],[2,"Perte 1-3 kg"],[3,"Pas de perte"]], key:"poids" },
          { q:"Motricité ?", opts:[[0,"Au lit ou fauteuil"],[1,"Autonome à l'intérieur"],[2,"Sort du domicile"]], key:"motricite" },
          { q:"Maladie aiguë ou stress psychologique ces 3 derniers mois ?", opts:[[0,"Oui"],[2,"Non"]], key:"stress" },
          { q:"Problèmes neuropsychologiques ?", opts:[[0,"Démence ou dépression sévère"],[1,"Démence légère"],[2,"Pas de problème"]], key:"neuro" },
          { q:"IMC (Indice de Masse Corporelle) ?", opts:[[0,"< 19"],[1,"19-21"],[2,"21-23"],[3,"≥ 23"]], key:"imc" },
        ];
        const [mnaStep, setMnaStep] = useState(0);
        const [mnaAnswers, setMnaAnswers] = useState({});'''

NEW_STEP11_START = '''      {step===11 && (() => {
        const MNA_QS = [
          { q:"Le patient présente-t-il une perte d'appétit ces 3 derniers mois ?", opts:[[0,"Baisse sévère"],[1,"Légère baisse"],[2,"Pas de baisse"]], key:"appetit" },
          { q:"Perte de poids récente (< 3 mois) ?", opts:[[0,"Perte > 3 kg"],[1,"Ne sait pas"],[2,"Perte 1-3 kg"],[3,"Pas de perte"]], key:"poids" },
          { q:"Motricité ?", opts:[[0,"Au lit ou fauteuil"],[1,"Autonome à l'intérieur"],[2,"Sort du domicile"]], key:"motricite" },
          { q:"Maladie aiguë ou stress psychologique ces 3 derniers mois ?", opts:[[0,"Oui"],[2,"Non"]], key:"stress" },
          { q:"Problèmes neuropsychologiques ?", opts:[[0,"Démence ou dépression sévère"],[1,"Démence légère"],[2,"Pas de problème"]], key:"neuro" },
          { q:"IMC (Indice de Masse Corporelle) ?", opts:[[0,"< 19"],[1,"19-21"],[2,"21-23"],[3,"≥ 23"]], key:"imc" },
        ];'''

if OLD_STEP11 in code:
    code = code.replace(OLD_STEP11, NEW_STEP11_START)
    fixes += 1; print("✅ FIX 2b — useState supprimés du IIFE step 11")
else:
    print("⚠️ FIX 2b — Step 11 IIFE non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
