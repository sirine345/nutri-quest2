"""
PATCH — Ajoute getSilhouetteLabel avant TransitionLLCScreen
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

GET_SIL = '''function getSilhouetteLabel(score) {
  if (score <= 2) return { label:"Maigreur", color:"#1565c0", bg:"#e3f2fd" };
  if (score <= 4) return { label:"Corpulence normale", color:"#2e7d32", bg:"#e8f5e9" };
  if (score <= 6) return { label:"Surpoids modéré", color:"#f57c00", bg:"#fff3e0" };
  return { label:"Obésité probable", color:"#c62828", bg:"#fbe9e7" };
}

'''

if 'function getSilhouetteLabel' not in code:
    code = code.replace('function TransitionLLCScreen(', GET_SIL + 'function TransitionLLCScreen(')
    print("✅ getSilhouetteLabel ajoutée")
else:
    print("✅ getSilhouetteLabel déjà présente")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
