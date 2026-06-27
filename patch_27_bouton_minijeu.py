"""
PATCH 27 — Ajouter bouton "Prochaine mission" vers mini-jeu dans RecommandationsQcm2Screen
Usage: python patch_27_bouton_minijeu.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = '''    </div>
  );
}




'''

NEW = '''      {/* Bouton prochaine mission */}
      <div style={{ padding:"24px 32px 40px", background:"#FFF5EE" }}>
        <div style={{ background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
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
}




'''

# Find the specific closing of RecommandationsQcm2Screen
# It's the first occurrence after the function starts
func_start = code.find('function RecommandationsQcm2Screen')
closing = code.find('\n    </div>\n  );\n}\n\n\n\n\n', func_start)

if closing != -1:
    code = code[:closing] + NEW[:-1] + code[closing + len('\n    </div>\n  );\n}\n\n\n\n\n'):]
    print("✅ FIX 1 — Bouton 'Composer mon assiette' ajouté")
else:
    # Try simpler closing
    old2 = '    </div>\n  );\n}\n\n'
    idx2 = code.find(old2, func_start)
    if idx2 != -1:
        new2 = '''      {/* Bouton prochaine mission */}
      <div style={{ padding:"24px 32px 40px", background:"#FFF5EE" }}>
        <div style={{ background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
          <div style={{ fontSize:32, marginBottom:10 }}>🎮</div>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, color:"#FA8072", marginBottom:8 }}>Prochaine mission !</div>
          <div style={{ fontSize:15, color:"#555", lineHeight:1.6, marginBottom:20 }}>Tu as découvert tes recettes personnalisées. Viens maintenant composer ton assiette idéale !</div>
          <button onClick={onBack}
            style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            🥗 Composer mon assiette →
          </button>
        </div>
      </div>

    </div>
  );
}

'''
        code = code[:idx2] + new2 + code[idx2 + len(old2):]
        print("✅ FIX 1 — Bouton ajouté (v2)")
    else:
        print("⚠️  Fermeture non trouvée")

# Also update the phase switch to go to minijeu instead of back
# Find recos_qcm2 phase in App and add onBack going to minijeu
OLD_RECOS_QCM2 = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen'
if OLD_RECOS_QCM2 in code:
    # Find the full line
    import re
    m = re.search(r'if \(phase === "recos_qcm2"\) return <RecommandationsQcm2Screen[^;]+;', code)
    if m:
        old_line = m.group(0)
        # Replace onBack to go to minijeu
        if 'onBack={() => { setPhase("select")' in old_line:
            new_line = old_line.replace(
                'onBack={() => { setPhase("select"); setPhaseHistory([]); }}',
                'onBack={() => goTo("minijeu")}'
            )
            code = code.replace(old_line, new_line)
            print("✅ FIX 2 — onBack redirige vers minijeu")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
