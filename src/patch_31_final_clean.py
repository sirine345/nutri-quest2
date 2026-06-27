"""
PATCH 31 — Supprime le bloc Prochaine mission restant + ajoute bouton Max dans onglet semaine
Usage: python patch_31_final_clean.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# FIX 1 — Supprimer lignes 2322-2336 (0-indexed: 2321-2335) = bloc Prochaine mission restant
# Repérer par le contenu exact
start_del = None
end_del = None
for i, l in enumerate(lines):
    if '        <div style={{ background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #2' in l and start_del is None:
        # Vérifier que c'est bien le bloc Prochaine mission (pas un autre)
        context = ''.join(lines[i:i+5])
        if 'Prochaine mission' in context or '🎮' in context:
            start_del = i
    if start_del and '      </div>' in l and i > start_del + 5:
        end_del = i
        break

if start_del and end_del:
    del lines[start_del:end_del+1]
    print(f"✅ FIX 1 — Bloc Prochaine mission supprimé (lignes {start_del+1}-{end_del+1})")
else:
    # Try direct approach - find by exact content
    code = ''.join(lines)
    OLD_BLOC = '''        <div style={{ background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
          <div style={{ fontSize:32, marginBottom:10 }}>🎮</div>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, color:"#FA8072", marginBottom:8 }}>
            Prochaine mission !
          </div>
          <div style={{ fontSize:15, color:"#555", lineHeight:1.6, marginBottom:20 }}>
            Tu as découvert tes recettes personnalisées. Maintenant, viens composer ton assiette idéale dans le mini-jeu !
          </div>
          <button onClick={onBack}
            style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            🥗 Composer mon assiette →
          </button>
        </div>
      </div>

    </div>
  );
}'''
    if OLD_BLOC in code:
        code = code.replace(OLD_BLOC, '''    </div>
  );
}''')
        lines = code.splitlines(keepends=True)
        print("✅ FIX 1 — Bloc supprimé (méthode 2)")
    else:
        print("⚠️  FIX 1 — Bloc non trouvé, essai ligne par ligne")
        code = ''.join(lines)

# FIX 2 — Ajouter bouton Max dans onglet semaine, juste avant la fermeture
code = ''.join(lines)

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

          {/* Bouton Max + suivant — tout en bas */}
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
    print("✅ FIX 2 — Bouton Max ajouté dans onglet semaine")
else:
    # Try without double newline
    OLD2 = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

        </div>
      )}

    </div>
  );
}'''
    if OLD2 in code:
        code = code.replace(OLD2, NEW_CLOSE)
        print("✅ FIX 2 — Bouton Max ajouté (v2)")
    else:
        print("⚠️  FIX 2 — Fermeture non trouvée")
        # Show what we have
        idx = code.find('Choisis tes dates ci-dessus')
        print(f"Contexte: {repr(code[idx:idx+200])}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
