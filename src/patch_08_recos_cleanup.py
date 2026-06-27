"""
PATCH 08 — Profil : enlever bouton recettes / Recos QCM1 : enlever bloc méditerranéen
Usage: python patch_08_recos_cleanup.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# FIX 1 — Enlever le bouton "Recettes adaptées" dans ProfilQcm1Screen
OLD_BTN = '''        <button onClick={() => onVoirRecettes("mediterraneen")}
          style={{ flex:1, background:"white", border:"2px solid #FA8072", borderRadius:14, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, padding:"14px", cursor:"pointer" }}>
          🫒 Recettes adaptées →
        </button>'''
NEW_BTN = ''
if OLD_BTN in code:
    code = code.replace(OLD_BTN, NEW_BTN)
    fixes += 1
    print("✅ FIX 1 — Bouton 'Recettes adaptées' supprimé du Profil")
else:
    print("⚠️  FIX 1 — Bouton recettes non trouvé")

# Aussi enlever le flex:2 du bouton recommandations qui devient seul
OLD_FLEX = 'style={{ flex:2, background:"#FA8072"'
NEW_FLEX = 'style={{ flex:1, background:"#FA8072"'
if OLD_FLEX in code:
    code = code.replace(OLD_FLEX, NEW_FLEX, 1)
    fixes += 1
    print("✅ FIX 2 — Bouton recommandations passe en flex:1")

# FIX 3 — Enlever le bloc méditerranéen dans RecommandationsQcm1Screen
# Le bloc commence par "/* Bloc méditerranéen */" ou par le div avec salade_grecque
OLD_BLOC = '''        {/* Bloc méditerranéen */}
        <div style={{ background:"white", borderRadius:20, overflow:"hidden", marginTop:12, boxShadow:"0 4px 20px rgba(0,0,0,0.08)", border:"3px solid #9ACD32" }}>
          <div style={{ position:"relative", height:100, overflow:"hidden" }}>
            <img src="/salade_grecque.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
            <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)", display:"flex", alignItems:"center", padding:"0 20px" }}>
              <div>
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"#7FFFD4", textShadow:"1px 1px 0 rgba(0,0,0,0.5)" }}>🫒 Régime Méditerranéen</div>
                <div style={{ fontSize:12, color:"rgba(255,255,255,0.85)", marginTop:2 }}>Recommandé par le PNNS</div>
              </div>
            </div>
          </div>
          <div style={{ padding:"16px 20px" }}>
            <p style={{ fontSize:13, color:"#6B7280", lineHeight:1.6, margin:"0 0 14px" }}>Fruits, légumes, légumineuses, poisson et huile d'olive — réduit les risques cardiovasculaires.</p>
            <button onClick={() => onVoirRecettes("mediterraneen")}
              style={{ background:"#9ACD32", color:"white", border:"none", borderRadius:12, padding:"13px 20px", fontSize:13, fontWeight:900, cursor:"pointer", width:"100%", fontFamily:"Arial Black, Arial, sans-serif" }}>
              Découvrir les recettes →
            </button>
          </div>
        </div>'''

if OLD_BLOC in code:
    code = code.replace(OLD_BLOC, '')
    fixes += 1
    print("✅ FIX 3 — Bloc méditerranéen supprimé des Recommandations QCM1")
else:
    # Try without the comment
    OLD_BLOC2 = '''        <div style={{ background:"white", borderRadius:20, overflow:"hidden", marginTop:12, boxShadow:"0 4px 20px rgba(0,0,0,0.08)", border:"3px solid #9ACD32" }}>
          <div style={{ position:"relative", height:100, overflow:"hidden" }}>
            <img src="/salade_grecque.png"'''
    if OLD_BLOC2 in code:
        # Find full block
        start_idx = code.index(OLD_BLOC2)
        # Find the closing div - count nested divs
        depth = 0
        i = start_idx
        while i < len(code):
            if code[i:i+4] == '<div':
                depth += 1
            elif code[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_idx = i + 6
                    code = code[:start_idx] + code[end_idx:]
                    fixes += 1
                    print("✅ FIX 3 — Bloc méditerranéen supprimé (méthode 2)")
                    break
            i += 1
    else:
        print("⚠️  FIX 3 — Bloc méditerranéen non trouvé, cherche le bloc générique...")
        # Try finding the generic mediterranean block in RecommandationsQcm1Screen
        OLD_MED = '''        {/* Bloc méditerranéen */}
        <div style={{ background:"white", borderRadius:20, overflow:"hidden", marginTop:8, boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>
          <div style={{ padding:"20px", display:"flex", gap:14, alignItems:"flex-start" }}>
            <div style={{ width:48, height:48, borderRadius:14, background:"#E0F7F5", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
              <div style={{ width:20, height:20, borderRadius:"50%", background:"#00BFA5" }} />
            </div>
            <div style={{ flex:1 }}>
              <div style={{ display:"inline-flex", background:"#E0F7F5", borderRadius:20, padding:"3px 10px", marginBottom:8 }}>
                <span style={{ fontSize:10, fontWeight:800, color:"#00897B", textTransform:"uppercase", letterSpacing:1 }}>Recommandé PNNS</span>
              </div>
              <div style={{ fontSize:16, fontWeight:800, color:"#1A1A1A", marginBottom:6 }}>Le régime méditerranéen</div>
              <p style={{ fontSize:13, color:"#6B7280", lineHeight:1.6, margin:"0 0 14px" }}>Fruits, légumes, légumineuses, poisson et huile d'olive — réduit les risques cardiovasculaires.</p>
              <button onClick={() => onVoirRecettes("mediterraneen")}
                style={{ background:"#00BFA5", color:"white", border:"none", borderRadius:12, padding:"12px 20px", fontSize:13, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Découvrir les recettes →
              </button>
            </div>
          </div>
        </div>'''
        if OLD_MED in code:
            code = code.replace(OLD_MED, '')
            fixes += 1
            print("✅ FIX 3 — Bloc méditerranéen générique supprimé")
        else:
            print("⚠️  FIX 3 — Aucun bloc méditerranéen trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes} fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
