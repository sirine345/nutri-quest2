#!/usr/bin/env python3
"""
Script de patch pour App.jsx — nutri-quest2
Usage: python patch_app.py
Place ce fichier dans C:\\Users\\fzahi\\Desktop\\nutri-quest2\\src\\
"""
import sys, os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
if not os.path.exists(src):
    print(f"ERREUR: App.jsx introuvable dans {os.path.dirname(__file__)}")
    sys.exit(1)

with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} caractères depuis App.jsx")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        result = code.replace(old, new, 1)
        fixes += 1
        print(f"  ✅ {name}")
        return result
    else:
        errors.append(name)
        print(f"  ⚠️  Non trouvé: {name}")
        return code

print("\n=== Application des patches ===\n")

# ─── 1. Labo: 3 missions ───
code = p(code,
    '    { bg: "lab", speaker: "max", text: "Deux missions : évaluer tes habitudes alimentaires, puis construire ta Fabrique à Menus." },',
    '    { bg: "lab", speaker: "max", text: "Trois missions : évaluer tes habitudes alimentaires, construire ta Fabrique à Menus, et composer ton assiette idéale !" },',
    "1. Labo: 3 missions")

# ─── 2. Emoji son ───
code = p(code,
    '{muted ? "" : ""}',
    '{muted ? "🔇" : "🔊"}',
    "2. Emoji son 🔇/🔊")

# ─── 3. QCM2 btn couleur rose ───
code = p(code,
    'const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };\n  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:600',
    'const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#FA8072", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"white" };\n  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:600',
    "3. QCM2 bouton couleur rose")

# ─── 4. Mini-jeu fond blanc ───
code = p(code,
    "backgroundImage:\"url('/fond1.png')\", backgroundSize:\"cover\", backgroundPosition:\"center\", fontFamily:\"Arial, sans-serif\" }}>",
    "background:\"white\", fontFamily:\"Arial, sans-serif\" }}>",
    "4. Mini-jeu fond blanc")

# ─── 5. Mini-jeu grid 50/50 ───
code = p(code,
    'gridTemplateColumns:"280px 1fr 120px", height:"100vh", paddingTop:50',
    'gridTemplateColumns:"1fr 1fr", height:"100vh", paddingTop:50',
    "5. Mini-jeu layout 50/50")

# ─── 6. Mini-jeu colonne assiettes (fond blanc + texte foncé) ───
code = p(code,
    '''        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"space-between", padding:16, paddingTop:20, paddingBottom:16 }}>
          <div style={{ textAlign:"center" }}>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:42, fontWeight:900, color:"white", letterSpacing:2, textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:0, lineHeight:1.1 }}>Compose ton repas</h1>
            <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto" }} />
            <p style={{ color:"rgba(255,255,255,0.9)", fontSize:14, margin:0, fontWeight:700 }}>Glisse les aliments sur les assiettes · la boisson sur le verre</p>
          </div>''',
    '''        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"space-between", padding:16, paddingTop:20, paddingBottom:16, background:"white" }}>
          <div style={{ textAlign:"center" }}>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"#1A3A5C", letterSpacing:1, margin:0, lineHeight:1.1 }}>Compose ton repas</h1>
            <div style={{ width:60, height:4, background:"#FA8072", borderRadius:99, margin:"8px auto" }} />
            <p style={{ color:"#888", fontSize:13, margin:0, fontWeight:600 }}>Glisse les aliments sur les assiettes · la boisson sur le verre</p>
          </div>''',
    "6. Mini-jeu colonne assiettes style")

# ─── 7. Mini-jeu labels assiettes couleur ───
for old_txt, new_txt, nom in [
    ('color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Entrée</div>',
     'color:"#c4622d", fontWeight:900, textTransform:"uppercase", letterSpacing:1 }}>Entrée</div>',
     "7a. label Entrée"),
    ('color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Plat principal</div>',
     'color:"#c4622d", fontWeight:900, textTransform:"uppercase", letterSpacing:1 }}>Plat principal</div>',
     "7b. label Plat"),
    ('color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Dessert</div>',
     'color:"#c4622d", fontWeight:900, textTransform:"uppercase", letterSpacing:1 }}>Dessert</div>',
     "7c. label Dessert"),
    ('color:"white", fontWeight:800, letterSpacing:1, textTransform:"uppercase", textShadow:"1px 1px 0 rgba(0,0,0,0.4)"',
     'color:"#888", fontWeight:800, letterSpacing:1, textTransform:"uppercase"',
     "7d. label Boisson"),
]:
    code = p(code, old_txt, new_txt, nom)

# ─── 8. Mini-jeu: remplacer colonne aliments par catégories PNNS ───
OLD_FOODS = '''        <div style={{ background:"rgba(255,255,255,0.95)", borderRight:"3px solid #222", overflowY:"auto", padding:16 }}>
          {[{ label:"Entrée", type:"entree" },{ label:"Plat", type:"plate" },{ label:"Dessert", type:"dessert" },{ label:"Boisson", type:"glass" }].filter(s => {
            if (s.type === "entree" && !showEntree) return false;
            if (s.type === "dessert" && !showDessert) return false;
            return true;
          }).map(section => (
            <details key={section.type} open style={{ marginBottom:12 }}>
              <summary style={{ fontSize:11, fontWeight:900, textTransform:"uppercase", letterSpacing:2, color:"#c4622d", marginBottom:8, cursor:"pointer", listStyle:"none", display:"flex", justifyContent:"space-between", alignItems:"center", padding:"4px 0" }}>{section.label} <span></span></summary>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginTop:6 }}>
                {FOODS_LIST.filter(f=>f.type===section.type).map(food => {
                  const used = usedIds.includes(food.id);
                  return (
                    <div key={food.id} draggable={!used} onDragStart={() => !used && setDragId(food.id)} onDragEnd={() => setDragId(null)}
                      style={{ background:used?"#f0f0f0":"white", border:`2px solid ${used?"#ccc":food.good?"#9ACD32":"#E24B4A"}`, borderRadius:12, padding:"10px 6px", textAlign:"center", cursor:used?"not-allowed":"grab", opacity:used?0.4:1, transition:"opacity 0.2s" }}>
                      {food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:52, height:52, objectFit:"contain" }} /> : <div style={{ fontSize:36 }}>{food.emoji}</div>}
                      <div style={{ fontSize:11, fontWeight:800, color:"#333", marginTop:4 }}>{food.name}</div>
                    </div>
                  );
                })}
              </div>
            </details>
          ))}
          <div style={{ marginTop:12, fontSize:11, color:"#888", lineHeight:1.6 }}><span style={{ color:"#9ACD32", fontWeight:700 }}>Vert</span> = recommandé PNNS<br/><span style={{ color:"#E24B4A", fontWeight:700 }}>Rouge</span> = déconseillé</div>
        </div>'''

NEW_FOODS = '''        {/* ── Colonne DROITE: Aliments par catégories PNNS ── */}
        <div style={{ background:"#FAFAFA", overflowY:"auto", padding:"12px 14px", borderLeft:"2px solid #E8EDF2" }}>
          <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:1, marginBottom:10 }}>🍽 Aliments — glisse sur les assiettes</div>
          {[
            { label:"Fruits & Légumes", color:"#4CAF50", bg:"#E8F5E9", ids:["legumes","fruits","salade","crudites","avocat","soupe","fraise","compote"] },
            { label:"Céréales, féculents & légumes secs", color:"#FF9800", bg:"#FFF3E0", ids:["feculents","legumesec"] },
            { label:"Lait & Produits laitiers", color:"#2196F3", bg:"#E3F2FD", ids:["fromage","yaourt"] },
            { label:"Viandes & Volailles", color:"#F44336", bg:"#FFEBEE", ids:["viande","charcuterie"] },
            { label:"Œufs", color:"#FFC107", bg:"#FFFDE7", ids:["oeuf"] },
            { label:"Poissons & Produits de la mer", color:"#009688", bg:"#E0F2F1", ids:["poisson"] },
            { label:"Matières grasses & Fast food", color:"#9C27B0", bg:"#F3E5F5", ids:["fastfood"] },
            { label:"Sucres & Produits sucrés", color:"#E91E63", bg:"#FCE4EC", ids:["gateau"] },
            { label:"Boissons", color:"#00BCD4", bg:"#E0F7FA", ids:["eau","jus","soda","lait"] },
          ].map(cat => {
            const catFoods = FOODS_LIST.filter(f => cat.ids.includes(f.id));
            if (catFoods.length === 0) return null;
            return (
              <div key={cat.label} style={{ marginBottom:12 }}>
                <div style={{ fontSize:9, fontWeight:900, textTransform:"uppercase", letterSpacing:0.5, color:cat.color, background:cat.bg, borderRadius:6, padding:"3px 8px", marginBottom:6, display:"inline-block" }}>{cat.label}</div>
                <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:5 }}>
                  {catFoods.map(food => {
                    const used = usedIds.includes(food.id);
                    return (
                      <div key={food.id} draggable={!used} onDragStart={() => !used && setDragId(food.id)} onDragEnd={() => setDragId(null)}
                        style={{ background:used?"#f0f0f0":"white", border:`2px solid ${used?"#ddd":food.good?cat.color:"#E24B4A"}`, borderRadius:10, padding:"7px 4px", textAlign:"center", cursor:used?"not-allowed":"grab", opacity:used?0.4:1, transition:"all 0.2s", boxShadow:used?"none":"0 1px 4px rgba(0,0,0,0.06)" }}>
                        {food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:38, height:38, objectFit:"contain" }} /> : <div style={{ fontSize:24 }}>{food.emoji}</div>}
                        <div style={{ fontSize:9, fontWeight:800, color:"#444", marginTop:2, lineHeight:1.2 }}>{food.name}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
          <div style={{ marginTop:6, fontSize:9, color:"#bbb", lineHeight:1.5 }}>
            Bordure <span style={{color:"#4CAF50",fontWeight:700}}>colorée</span> = PNNS · <span style={{color:"#E24B4A",fontWeight:700}}>Rouge</span> = déconseillé
          </div>
        </div>'''

code = p(code, OLD_FOODS, NEW_FOODS, "8. Mini-jeu catégories PNNS")

# ─── 9. Supprimer colonne barres PNNS (remplacée par les catégories) ───
OLD_BARS = '''        <div style={{ background:"rgba(255,255,255,0.95)", borderLeft:"3px solid #222", padding:"60px 14px 12px", display:"flex", flexDirection:"column", gap:10 }}>
          <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:1, color:"#c4622d", marginBottom:8 }}>Équilibre PNNS</div>
          {[{ key:"legumes", label:"Légumes", color:"#639922" },{ key:"feculents", label:"Féculents", color:"#EF9F27" },{ key:"proteines", label:"Protéines", color:"#378ADD" },{ key:"fruits", label:"Fruits", color:"#D4537E" },{ key:"laitiers", label:"Laitiers", color:"#B5D4F4" },{ key:"eau", label:"Boisson", color:"#85B7EB" }].map(b => (
            <div key={b.key}>
              <div style={{ fontSize:10, color:"#555", marginBottom:3, fontWeight:700 }}>{b.label}</div>
              <div style={{ height:8, background:"#eee", borderRadius:99, overflow:"hidden", border:"1px solid #ddd" }}><div style={{ height:"100%", width:bars[b.key]+"%", background:b.color, borderRadius:99, transition:"width 0.3s" }} /></div>
            </div>
          ))}
        </div>'''
code = p(code, OLD_BARS, '', "9. Supprimer colonne barres PNNS")

# ─── 10. CB lien ───
code = p(code,
    '<h2 style={{ fontSize:"1.2em", color:"#FA8072", marginBottom:4, fontWeight:900 }}>Circonférence brachiale (CB en cm)</h2>\n          </div>\n          {[[0,"CB < 21"',
    '<h2 style={{ fontSize:"1.2em", color:"#FA8072", marginBottom:4, fontWeight:900 }}>Circonférence brachiale (CB en cm)</h2>\n            <p style={{ fontSize:11, margin:"6px 0 0", textAlign:"center" }}><a href="https://www.sfncm.org/images/stories/docs/MNA/MNA_french.pdf" target="_blank" rel="noopener noreferrer" style={{ color:"#7b1fa2", textDecoration:"underline", fontStyle:"italic" }}>📎 Guide de mesure CB — SFNCM (source officielle)</a></p>\n          </div>\n          {[[0,"CB < 21"',
    "10. CB lien SFNCM")

# ─── 11. CM lien ───
code = p(code,
    '<h2 style={{ fontSize:"1.2em", color:"#FA8072", marginBottom:4, fontWeight:900 }}>Circonférence du mollet (CM en cm)</h2>\n          </div>\n          {[[0,"CM < 31"',
    '<h2 style={{ fontSize:"1.2em", color:"#FA8072", marginBottom:4, fontWeight:900 }}>Circonférence du mollet (CM en cm)</h2>\n            <p style={{ fontSize:11, margin:"6px 0 0", textAlign:"center" }}><a href="https://www.sfncm.org/images/stories/docs/MNA/MNA_french.pdf" target="_blank" rel="noopener noreferrer" style={{ color:"#7b1fa2", textDecoration:"underline", fontStyle:"italic" }}>📎 Guide de mesure mollet — SFNCM (source officielle)</a></p>\n          </div>\n          {[[0,"CM < 31"',
    "11. CM lien SFNCM")

# ─── 12. Recettes: state filtrePourVous ───
code = p(code,
    '  const [openRecette, setOpenRecette] = useState(null);\n  const [filtreProfil, setFiltreProfil] = useState(filtreProfilInitial || null);\n  const [search, setSearch] = useState("");',
    '  const [openRecette, setOpenRecette] = useState(null);\n  const [filtreProfil, setFiltreProfil] = useState(filtreProfilInitial || null);\n  const [search, setSearch] = useState("");\n  const [filtrePourVous, setFiltrePourVous] = useState(!!filtreProfilInitial);',
    "12. Recettes: state filtrePourVous")

# ─── 13. Recettes: onglets "Pour vous" / "Toutes" ───
code = p(code,
    '      {/* Sous-filtres tags */}\n      <div style={{ background:"white", borderBottom:"1px solid #E8EDF2", padding:"10px 20px", display:"flex", gap:8, alignItems:"center" }}>',
    '''      {/* Onglets Pour vous / Toutes les recettes */}
      <div style={{ background:"white", borderBottom:"2px solid #E8EDF2", display:"flex" }}>
        {[["toutes","🍽 Toutes les recettes"],["vous","⭐ Recettes pour vous"]].map(([id,label]) => (
          <button key={id}
            onClick={()=>{
              const isPourVous = id==="vous";
              setFiltrePourVous(isPourVous);
              if(isPourVous && filtreProfilInitial) setFiltreProfil(filtreProfilInitial);
              else if(!isPourVous) setFiltreProfil(null);
            }}
            style={{ flex:1, padding:"14px 12px", fontSize:13, fontWeight:800, border:"none", borderBottom:`3px solid ${filtrePourVous===(id==="vous")?"#FA8072":"transparent"}`, cursor:"pointer", background:"none", color:filtrePourVous===(id==="vous")?"#FA8072":"#6B7280", transition:"all 0.15s" }}>
            {label}
            {id==="vous" && !filtreProfilInitial && <span style={{ fontSize:10, color:"#bbb", marginLeft:6 }}>(connectez-vous pour voir vos recettes)</span>}
          </button>
        ))}
      </div>

      {/* Sous-filtres tags */}
      <div style={{ background:"white", borderBottom:"1px solid #E8EDF2", padding:"10px 20px", display:"flex", gap:8, alignItems:"center" }}>''',
    "13. Recettes: onglets Pour vous / Toutes")

# ─── 14. MNA après QCM Santé: alerte dénutrition ───
code = p(code,
    '            <button onClick={handleFinish} style={{ ...btn, width:"100%", background:"#c4622d", color:"white", border:"3px solid #a03010" }}>\n              Terminer mon profil santé →\n            </button>',
    '''            {/* ─ Alerte MNA si signes de dénutrition ─ */}
            {(evolution==="Beaucoup plus mince" || evolution==="Un peu plus mince" || autonomie==="Ni l\'un ni l\'autre" || autonomie==="Repas seulement") && (
              <div style={{ background:"#fff8e1", border:"2px solid #f57c00", borderRadius:14, padding:"14px 16px", marginBottom:12 }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#e65100", marginBottom:6 }}>⚠️ Signes possibles de dénutrition détectés</div>
                <div style={{ fontSize:12, color:"#555", lineHeight:1.6, marginBottom:6 }}>
                  Perte de poids ou difficultés alimentaires repérées dans votre profil. Un bilan MNA (Mini Nutritional Assessment) est recommandé par la Haute Autorité de Santé.
                </div>
                <div style={{ fontSize:11, color:"#888", fontStyle:"italic" }}>
                  💡 Pour accéder au QCM MNA : retournez au menu → Fabrique à Menus → indiquez "1 repas par jour".
                </div>
              </div>
            )}
            <button onClick={handleFinish} style={{ ...btn, width:"100%", background:"#c4622d", color:"white", border:"3px solid #a03010" }}>
              Terminer mon profil santé →
            </button>''',
    "14. Alerte MNA dénutrition dans QCM Santé")

# ═══ RÉSULTAT ═══
print(f"\n{'='*50}")
print(f"Patches appliqués: {fixes}")
if errors:
    print(f"Non trouvés ({len(errors)}): {', '.join(errors)}")
print(f"Taille sortie: {len(code)} caractères")

# Écriture
out_path = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx écrit avec succès !")
print(f"   → {out_path}")
