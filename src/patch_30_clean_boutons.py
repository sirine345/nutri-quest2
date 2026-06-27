"""
PATCH 30 — Supprimer tous les blocs "Prochaine mission" parasites
et garder uniquement le bouton dans l'onglet Ma semaine type
Usage: python patch_30_clean_boutons.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Supprimer les blocs "Bouton prochaine mission" aux lignes 2339-2354 et 2437-2452
# (0-indexed: 2338-2353 et 2436-2451)
# On repère par le commentaire {/* Bouton prochaine mission */}

blocks_to_remove = []
i = 0
while i < len(lines):
    if '{/* Bouton prochaine mission */}' in lines[i] or '      {/* Bouton prochaine mission */}' in lines[i]:
        start = i
        # Cherche la fermeture </div> du bloc (2 niveaux)
        depth = 0
        j = i
        while j < len(lines):
            depth += lines[j].count('<div') - lines[j].count('</div>')
            if depth <= 0 and j > i:
                blocks_to_remove.append((start, j))
                i = j + 1
                break
            j += 1
        else:
            i += 1
    else:
        i += 1

print(f"Blocs à supprimer: {len(blocks_to_remove)}")
for s, e in blocks_to_remove:
    print(f"  Lignes {s+1}–{e+1}")

# Supprimer de la fin vers le début
for start, end in reversed(blocks_to_remove):
    del lines[start:end+1]

# Supprimer aussi le bloc "Bouton suivant vers mini-jeu" dans l'onglet semaine (ligne ~2043)
# et le remplacer par le bon
code = ''.join(lines)

# Vérifier s'il reste encore des "Prochaine mission"
import re
remaining = [m.start() for m in re.finditer('Prochaine mission', code)]
print(f"Restants après suppression: {len(remaining)}")

# Maintenant ajouter le bouton UNIQUEMENT dans l'onglet semaine, tout en bas
# Juste avant la fermeture de l'onglet semaine
OLD_SEMAINE_END = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton suivant — apparaît toujours en bas */}'''

NEW_SEMAINE_END = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton Max + Composer assiette — tout en bas de l'onglet semaine */}'''

if OLD_SEMAINE_END in code:
    code = code.replace(OLD_SEMAINE_END, NEW_SEMAINE_END)
    print("✅ Commentaire mis à jour")

# Vérifier que le bouton Max est bien là
if 'Maintenant que tu as ton planning' in code:
    print("✅ Bouton Max déjà présent dans l'onglet semaine")
else:
    # L'ajouter
    OLD_CLOSE = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

        </div>
      )}

    </div>
  );
}'''
    NEW_CLOSE = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton Max + suivant */}
          <div style={{ marginTop:32, background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222" }}>
            <div style={{ display:"flex", alignItems:"center", gap:16, marginBottom:16 }}>
              <img src="/e.png" alt="Max" style={{ height:120, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
              <div style={{ background:"#fff8f0", border:"2px solid #FA8072", borderRadius:"14px 14px 14px 4px", padding:"14px 16px", flex:1 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"0.1em", marginBottom:6 }}>Max</div>
                <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                  Maintenant que tu as ton planning de la semaine, viens t'amuser en <strong style={{ color:"#FA8072" }}>composant ton assiette idéale</strong> dans le mini-jeu ! 🎮
                </div>
              </div>
            </div>
            <button onClick={() => onBack()}
              style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Suivant → Composer mon assiette
            </button>
          </div>

        </div>
      )}

    </div>
  );
}'''
    if OLD_CLOSE in code:
        code = code.replace(OLD_CLOSE, NEW_CLOSE)
        print("✅ Bouton Max ajouté dans l'onglet semaine")
    else:
        print("⚠️  Fermeture onglet semaine non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
