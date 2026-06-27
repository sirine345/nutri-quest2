#!/usr/bin/env python3
"""Patch 4 — Fix hooks violation et bouton retour"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        fixes += 1
        print(f"  ✅ {name}")
        return code.replace(old, new, 1)
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

print("\n=== Patches ===\n")

# ── 1. Supprimer le useEffect illégal dans if(done) + garder seulement l'original ──
# Le problème: il y a DEUX blocs if(done) et le 2ème a un useEffect dedans
# On remplace le 2ème if(done) (le cassé) par rien car l'original au-dessus suffit

OLD_BROKEN = '''  if (done) {
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

code = p(code, OLD_BROKEN, '', "1. Supprimer if(done) avec useEffect illégal")

# ── 2. Corriger l'original useEffect pour appeler "sante" au lieu de cuisineVal ──
OLD_EFFECT = '''  // Notify parent when done (in effect to avoid setState-during-render)
  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const cuisineVal = answers["\u200d En cuisine"];
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, cuisineVal, answers);
    }
  }, [done]); // eslint-disable-line'''

NEW_EFFECT = '''  // Notify parent when done
  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, "sante", answers);
    }
  }, [done]); // eslint-disable-line'''

code = p(code, OLD_EFFECT, NEW_EFFECT, "2. useEffect → appelle sante")

# ── 3. Bouton retour step1 QCM2 — style complet sans dépendre de btn ──
OLD_BTN = 'onBack} style={{ ...btn, background:"#f5f5f5", color:"#aaa", border:"3px solid #ddd" }}>← Retour</button>}'
NEW_BTN = 'onBack} style={{ marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, borderRadius:12, cursor:"pointer", background:"#f5f5f5", color:"#555", border:"3px solid #ddd", boxShadow:"4px 4px 0 #ddd" }}>← Retour</button>}'
code = p(code, OLD_BTN, NEW_BTN, "3. Bouton retour step1 visible")

print(f"\n{'='*40}")
print(f"Fixes: {fixes} ✅  Erreurs: {len(errors)}")
if errors:
    print(f"Manquants: {errors}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx écrit ({len(code)} chars)")
