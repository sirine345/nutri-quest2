#!/usr/bin/env python3
"""
Patch 4 — Corrections critiques:
1. Fix hooks violation dans Qcm2Screen (useEffect dans if done)
2. Fix bouton retour step 1 QCM2
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} caractères")

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

# ══════════════════════════════════════════════════════
# FIX 1 — Supprimer le useEffect dans if(done) de Qcm2Screen
# C'est une violation des règles des hooks React
# Remplacer par un redirect via useEffect placé AVANT le return conditionnel
# ══════════════════════════════════════════════════════

# D'abord trouver et supprimer le bloc if(done) avec useEffect dedans
OLD_DONE_BROKEN = '''  if (done) {
    // Redirect immédiat — la page "Profil créé" est remplacée par ProfilFinalScreen
    useEffect(() => {
      const compoVal = answers[" Composition du repas"];
      const cuisineVal = answers["\\u200d En cuisine"];
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

# Remplacer par: useEffect propre avant le rendering conditionnel
NEW_DONE_FIXED = '''  // Redirect quand done — useEffect doit être au top level, pas dans un if
  useEffect(() => {
    if (done) {
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, "sante", answers);
    }
  }, [done]); // eslint-disable-line

  if (done) {
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"Arial, sans-serif" }}>
        <div style={{ textAlign:"center", color:"#888" }}>
          <div style={{ fontSize:32, marginBottom:12 }}>⏳</div>
          <div style={{ fontSize:16, fontWeight:700 }}>Chargement de votre profil...</div>
        </div>
      </div>
    );
  }'''

code = p(code, OLD_DONE_BROKEN, NEW_DONE_FIXED, "1. Fix hooks violation useEffect dans if(done)")

# ══════════════════════════════════════════════════════
# FIX 2 — Bouton retour step 1 QCM2 toujours invisible
# Le problème : btn a color:"white" ET background:"#f5f5f5"
# → texte blanc sur fond clair = invisible
# Solution : style inline complet qui override btn
# ══════════════════════════════════════════════════════
code = p(code,
    '<button onClick={onBack} style={{ ...btn, background:"#f5f5f5", color:"#aaa", border:"3px solid #ddd" }}>← Retour</button>\n            <button onClick={()=>next(1,{" Nombre de personnes"',
    '<button onClick={onBack} style={{ marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #ddd", cursor:"pointer", background:"#f5f5f5", borderRadius:12, boxShadow:"4px 4px 0 #ddd", color:"#aaa" }}>← Retour</button>\n            <button onClick={()=>next(1,{" Nombre de personnes"',
    "2. Bouton retour step1 QCM2 style complet")

# ══════════════════════════════════════════════════════
# FIX 3 — Aussi corriger le useEffect existant dans Qcm2Screen
# qui était là avant (l'original) pour éviter les conflits
# L'original était:
#   useEffect(() => {
#     if (done) {
#       saveGame(...)
#       if (onDone) onDone(...)
#     }
#   }, [done]);
# On doit le supprimer car il est maintenant dupliqué
# ══════════════════════════════════════════════════════
OLD_ORIGINAL_EFFECT = '''  // Notify parent when done (in effect to avoid setState-during-render)
  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const cuisineVal = answers["\\u200d En cuisine"];
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, cuisineVal, answers);
    }
  }, [done]); // eslint-disable-line'''

NEW_ORIGINAL_EFFECT = '''  // Notify parent when done — géré par le useEffect ci-dessus'''

code = p(code, OLD_ORIGINAL_EFFECT, NEW_ORIGINAL_EFFECT, "3. Supprimer useEffect original dupliqué")

# ══════════════════════════════════════════════════════
# RÉSULTAT
# ══════════════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"Fixes: {fixes} ✅  |  Erreurs: {len(errors)}")
if errors:
    print(f"Non trouvés: {', '.join(errors)}")

out = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(out, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit !")
