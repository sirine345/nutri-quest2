"""
PATCH — Ajoute le bouton Max + Composer mon assiette dans l'onglet semaine
Usage: python patch_add_bouton_semaine.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}
        </div>
      )}'''

NEW = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton Max → mini-jeu */}
          <div style={{ marginTop:32, background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222" }}>
            <div style={{ display:"flex", alignItems:"center", gap:16, marginBottom:16 }}>
              <img src="/e.png" alt="Max" style={{ height:100, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
              <div style={{ background:"#fff8f0", border:"2px solid #FA8072", borderRadius:"14px 14px 14px 4px", padding:"14px 16px", flex:1 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"0.1em", marginBottom:6 }}>Max</div>
                <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                  {"Tu as tout ce qu'il faut ! Viens maintenant composer ton assiette idéale dans le mini-jeu 🎮"}
                </div>
              </div>
            </div>
            <button onClick={() => onMinijeu && onMinijeu()}
              style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Composer mon assiette →
            </button>
          </div>

        </div>
      )}'''

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ Bouton Max + mini-jeu ajouté dans l'onglet semaine")
else:
    print("⚠️  Marqueur non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
