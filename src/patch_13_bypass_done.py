"""
PATCH 13 — Bypasse l'écran "done" de QCM2 et va directement vers profil_qcm2
Le done screen s'affiche à l'intérieur de Qcm2Screen quand done===true
Il faut faire en sorte que quand done===true, on appelle onDone("profil_qcm2") directement
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# Le useEffect qui déclenche onDone quand done===true
# Actuellement il appelle onDone(compoVal, cuisineVal, answers)
# On veut qu'il appelle onDone(compoVal, "profil_qcm2", answers) directement

OLD_EFFECT = '''  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const cuisineVal = answers["‍ En cuisine"];
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, cuisineVal, answers);
    }
  }, [done]); // eslint-disable-line'''

NEW_EFFECT = '''  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, "profil_qcm2", answers);
    }
  }, [done]); // eslint-disable-line'''

if OLD_EFFECT in code:
    code = code.replace(OLD_EFFECT, NEW_EFFECT)
    fixes += 1
    print("✅ FIX 1 — useEffect QCM2 redirige vers profil_qcm2 directement")
else:
    print("⚠️  FIX 1 — useEffect non trouvé, essai variante...")
    # Try with \r\n
    OLD_EFFECT2 = OLD_EFFECT.replace('\n', '\r\n')
    if OLD_EFFECT2 in code:
        code = code.replace(OLD_EFFECT2, NEW_EFFECT)
        fixes += 1
        print("✅ FIX 1 — useEffect QCM2 patché (CRLF)")
    else:
        print("⚠️  FIX 1 — Toujours pas trouvé")

# Aussi : quand repas="Midi et soir" → setDone(true) directement
# Il faut aussi intercepter ça
OLD_REPAS_DONE = 'else{setDone(true);saveGame({ type:"qcm2", data: { answers: {...answers, " Nombre de repas": repas}, patient: { prenom: playerName, ...(playerInfos||{}) } } });}'
NEW_REPAS_DONE = 'else{ saveGame({ type:"qcm2", data: { answers: {...answers, " Nombre de repas": repas}, patient: { prenom: playerName, ...(playerInfos||{}) } } }); if(onDone) onDone(answers[" Composition du repas"], "profil_qcm2", {...answers, " Nombre de repas": repas}); }'

if OLD_REPAS_DONE in code:
    code = code.replace(OLD_REPAS_DONE, NEW_REPAS_DONE)
    fixes += 1
    print("✅ FIX 2 — Chemin rapide (repas=midi et soir) aussi redirigé")
else:
    print("⚠️  FIX 2 — Chemin rapide non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/2 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
