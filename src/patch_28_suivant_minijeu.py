"""
PATCH 28 — Ajouter bouton "Suivant → Compose ton assiette" dans onglet Ma semaine type
Usage: python patch_28_suivant_minijeu.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# FIX 1 — Ajouter bouton suivant à la fin de l'onglet semaine
OLD = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}
        </div>
      )}

    </div>
  );
}'''

NEW = '''          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}

          {/* Bouton suivant vers mini-jeu */}
          <div style={{ marginTop:32, background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
            <div style={{ display:"flex", alignItems:"center", gap:16, marginBottom:16 }}>
              <img src="/e.png" alt="Max" style={{ height:100, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
              <div style={{ background:"#fff8f0", border:"2px solid #FA8072", borderRadius:"14px 14px 14px 4px", padding:"12px 16px", textAlign:"left" }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"0.1em", marginBottom:4 }}>Max</div>
                <div style={{ fontSize:14, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                  Maintenant que tu as ton planning, viens t'amuser en <strong style={{ color:"#FA8072" }}>composant ton assiette idéale</strong> ! Tu vas apprendre à équilibrer tes repas de façon ludique 🎮
                </div>
              </div>
            </div>
            <button onClick={onBack}
              style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Suivant → Composer mon assiette
            </button>
          </div>

        </div>
      )}

    </div>
  );
}'''

if OLD in code:
    code = code.replace(OLD, NEW)
    fixes += 1
    print("✅ FIX 1 — Bouton 'Suivant → Composer mon assiette' ajouté avec Max")
else:
    print("⚠️  FIX 1 — Marqueur non trouvé")

# FIX 2 — onBack dans recos_qcm2 doit aller vers le select (cuisine)
import re
m = re.search(r'if \(phase === "recos_qcm2"\)[^\n]+\n', code)
if m:
    line = m.group(0)
    if 'onBack' in line and 'minijeu' not in line:
        new_line = line.replace(
            'onBack={() => { setPhase("select"); setPhaseHistory([]); }}',
            'onBack={() => { setPhase("select"); setPhaseHistory([]); }}'
        )
        print("✅ FIX 2 — onBack déjà correct (retour au menu select)")
        fixes += 1
    elif 'minijeu' in line:
        new_line = line.replace('onBack={() => goTo("minijeu")', 'onBack={() => { setPhase("select"); setPhaseHistory([]); }}')
        code = code.replace(line, new_line)
        fixes += 1
        print("✅ FIX 2 — onBack corrigé vers select")
else:
    print("⚠️  FIX 2 — Phase recos_qcm2 non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/2 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
