#!/usr/bin/env python3
"""Patch 5 — Supprime le useEffect illégal lignes 2392-2407"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

OLD = '''  if (done) {
    // Redirect immédiat — la page "Profil créé" est remplacée par ProfilFinalScreen
    useEffect(() => {
      const compoVal = answers[" Composition du repas"];
      const cuisineVal = answers["\u200d En cuisine"];
      if (onDone) onDone(compoVal, "sante", answers);
    }, []);
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"Arial, sans-serif" }}>
        <div style={{ textAlign:"center", color:"#888" }}>
          <div style={{ fontSize:32, marginBottom:12 }}>⏳</div>
          <div style={{ fontSize:16, fontWeight:700 }}>Chargement de votre profil...</div>
        </div>
      </div>
    );
  }'''

if OLD in code:
    code = code.replace(OLD, '', 1)
    print("✅ Bloc if(done)+useEffect supprimé")
else:
    print("⚠️ Non trouvé — suppression par lignes")
    lines = code.split('\n')
    # Supprimer lignes 2391-2407 (index 2390-2406)
    new_lines = lines[:2390] + lines[2407:]
    code = '\n'.join(new_lines)
    print(f"✅ Lignes 2391-2407 supprimées")

# Aussi corriger le useEffect original pour appeler "sante"
OLD2 = '      if (onDone) onDone(compoVal, cuisineVal, answers);'
NEW2 = '      if (onDone) onDone(compoVal, "sante", answers);'
if OLD2 in code:
    code = code.replace(OLD2, NEW2, 1)
    print("✅ useEffect original → appelle sante")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
