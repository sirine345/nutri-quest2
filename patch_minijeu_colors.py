"""
PATCH — Couleurs site + suppression bilan PNNS dans MinijeuScreen
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# 1. Header : bleu marine → saumon #FA8072
old = 'background:"#1A3A5C", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0'
new = 'background:"#FA8072", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Header saumon")

# 2. Bouton retour : bleu ciel → blanc/saumon
old = 'background:"#87CEEB", border:"2px solid #1A3A5C", borderRadius:8, color:"#1A3A5C"'
new = 'background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:8, color:"white"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Bouton retour blanc")

# 3. Titre colonne gauche : bleu marine → saumon
old = 'fontSize:13, fontWeight:900, color:"#1A3A5C", marginBottom:12, textTransform:"uppercase", letterSpacing:1'
new = 'fontSize:13, fontWeight:900, color:"#FA8072", marginBottom:12, textTransform:"uppercase", letterSpacing:1'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Titre gauche saumon")

# 4. Catégories : bleu ciel → vert anis #9ACD32
old = 'fontSize:11, fontWeight:900, color:"#87CEEB", textTransform:"uppercase"'
new = 'fontSize:11, fontWeight:900, color:"#9ACD32", textTransform:"uppercase"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Catégories vert anis")

# 5. Border catégories
old = 'paddingBottom:4, borderBottom:"2px solid #e8f4ff"'
new = 'paddingBottom:4, borderBottom:"2px solid #f0f9e0"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Border catégories")

# 6. Rebord assiette : bleu ciel → saumon + vert anis pour assiette plat
old = 'border:"4px solid #87CEEB", boxShadow:"0 4px 16px rgba(135,206,235,0.4)"'
new = 'border:"4px solid #FA8072", boxShadow:"0 4px 16px rgba(250,128,114,0.25)"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Rebord assiette saumon")

# 7. Texte "Dépose ici" dans assiette
old = 'fontSize:11, color:"#87CEEB", textAlign:"center", fontWeight:700'
new = 'fontSize:11, color:"#FA8072", textAlign:"center", fontWeight:700'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Texte assiette")

# 8. Rebord boisson
old = 'border:"3px solid #87CEEB", background:glass?glass.color+"22":"#f0f8ff"'
new = 'border:"3px solid #9ACD32", background:glass?glass.color+"22":"#f5f9ee"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Rebord boisson vert")

# 9. Titre droite
old = 'fontSize:13, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Mon plateau'
new = 'fontSize:13, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Mon plateau'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Titre plateau")

# 10. Titres assiettes individuelles
old = 'fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Entrée'
new = 'fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Entrée'
if old in code:
    code = code.replace(old, new); fixes += 1
old = 'fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Plat principal'
new = 'fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Plat principal'
if old in code:
    code = code.replace(old, new); fixes += 1
old = 'fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Dessert'
new = 'fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Dessert'
if old in code:
    code = code.replace(old, new); fixes += 1
old = 'fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Boisson'
new = 'fontSize:11, fontWeight:900, color:"#9ACD32", textTransform:"uppercase", letterSpacing:1 }}>Boisson'
if old in code:
    code = code.replace(old, new); fixes += 1
print(f"✅ Titres assiettes colorés")

# 11. Supprimer le bilan PNNS entier
OLD_PNNS = '''          {/* Bilan PNNS */}
          <div style={{ background:"#f0f8ff", borderRadius:14, padding:"14px 16px", border:"2px solid #87CEEB" }}>
            <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1, marginBottom:10 }}>Équilibre PNNS</div>
            {[{ key:"legumes", label:"Légumes & fruits", color:"#4caf50" },{ key:"feculents", label:"Féculents", color:"#EF9F27" },{ key:"proteines", label:"Protéines", color:"#378ADD" },{ key:"laitiers", label:"Laitiers", color:"#87CEEB" },{ key:"eau", label:"Boisson", color:"#1A3A5C" }].map(b => (
              <div key={b.key} style={{ marginBottom:8 }}>
                <div style={{ display:"flex", justifyContent:"space-between", fontSize:11, color:"#555", marginBottom:3, fontWeight:700 }}>
                  <span>{b.label}</span><span>{bars[b.key]}%</span>
                </div>
                <div style={{ height:8, background:"#dde8f0", borderRadius:99, overflow:"hidden" }}>
                  <div style={{ height:"100%", width:bars[b.key]+"%", background:b.color, borderRadius:99, transition:"width 0.3s" }} />
                </div>
              </div>
            ))}
          </div>'''
if OLD_PNNS in code:
    code = code.replace(OLD_PNNS, ''); fixes += 1; print("✅ Bilan PNNS supprimé")
else:
    print("⚠️ Bilan PNNS non trouvé")

# 12. Bouton valider : bleu marine → saumon
old = 'background:"#1A3A5C", border:"none", borderRadius:12, color:"white", fontSize:15, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"0 4px 12px rgba(26,58,92,0.3)"'
new = 'background:"#FA8072", border:"3px solid #222", borderRadius:12, color:"white", fontSize:15, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222"'
if old in code:
    code = code.replace(old, new); fixes += 1; print("✅ Bouton valider saumon")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
