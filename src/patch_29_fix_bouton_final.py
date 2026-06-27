"""
PATCH 29 — Déplacer le bouton Max+assiette APRÈS le planning, supprimer l'ancien
Usage: python patch_29_fix_bouton_final.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Supprimer les lignes 2043-2058 (le bouton mal placé, 0-indexed: 2042-2057)
# Et remplacer la fin de l'onglet semaine par la bonne version

start_del = None
end_del   = None
for i, l in enumerate(lines):
    if '{/* Bouton suivant vers mini-jeu */}' in l:
        start_del = i
    if start_del and '          </div>' in l and i > start_del + 10:
        end_del = i
        break

if start_del and end_del:
    del lines[start_del:end_del+1]
    print(f"✅ Ancien bouton supprimé (lignes {start_del+1}-{end_del+1})")
else:
    print("⚠️  Bouton à supprimer non trouvé")

# Maintenant trouver "Choisis tes dates" et ajouter le bouton APRÈS le planning
NEW_END = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton suivant — apparaît toujours en bas */}
          <div style={{ marginTop:32, background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
            <div style={{ display:"flex", alignItems:"center", gap:16, marginBottom:16, textAlign:"left" }}>
              <img src="/e.png" alt="Max" style={{ height:110, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
              <div style={{ background:"#fff8f0", border:"2px solid #FA8072", borderRadius:"14px 14px 14px 4px", padding:"14px 16px" }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"0.1em", marginBottom:6 }}>Max</div>
                <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                  Maintenant que tu as ton planning de la semaine, viens t'amuser en <strong style={{ color:"#FA8072" }}>composant ton assiette idéale</strong> dans le mini-jeu ! 🎮
                </div>
              </div>
            </div>
            <button onClick={() => onBack()}
              style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Suivant → Composer mon assiette
            </button>
          </div>

        </div>
      )}

    </div>
  );
}
'''

# Find and replace the old closing
old_closing = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}
        </div>
      )}

    </div>
  );
}'''

code = ''.join(lines)
if old_closing in code:
    code = code.replace(old_closing, NEW_END)
    print("✅ Bouton Max + assiette ajouté après le planning")
else:
    print("⚠️  Fermeture non trouvée")

# Fix onBack in recos_qcm2 to go to select (cuisine)
import re
m = re.search(r'if \(phase === "recos_qcm2"\)[^\n]+', code)
if m:
    line = m.group(0)
    print(f"Phase recos_qcm2: {line[:80]}")
    if 'minijeu' in line:
        new_line = line.replace('onBack={() => goTo("minijeu")', 'onBack={() => { setPhase("select"); setPhaseHistory([]); }}')
        code = code.replace(line, new_line)
        print("✅ onBack corrigé vers select")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
