#!/usr/bin/env python3
"""
Patch 7 :
1. Page recettes : supprimer onglets catégories (Tartines, Salades...)
   Garder seulement "Toutes les recettes" et "Recettes personnalisées"
2. Harmoniser le design avec le reste du site (fond crème/orange, pas blanc/bleu)
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        fixes += 1
        print(f"  ✅ {name}")
        return code.replace(old, new, 1)
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

print("\n=== Patches ===\n")

# ══════════════════════════════════════════════
# FIX 1 — Remplacer tout le header RecettesScreen (vue liste)
# Supprimer le header bleu foncé + onglets catégories
# Remplacer par un design dans les couleurs du site (orange/crème)
# ══════════════════════════════════════════════

OLD_HEADER = '''      {/* Header hero */}
      <div style={{ background:"#1A3A5C", padding:"0" }}>
        <div style={{ padding:"14px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
          <button onClick={onBack}
            style={{ display:"flex", alignItems:"center", gap:6, background:"rgba(255,255,255,0.12)", border:"1px solid rgba(255,255,255,0.25)", borderRadius:10, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>
            ← Retour
          </button>
          <span style={{ fontSize:11, color:"rgba(255,255,255,0.5)", fontWeight:600, textTransform:"uppercase", letterSpacing:1 }}>mangerbouger.fr</span>
        </div>

        <div style={{ padding:"4px 20px 28px" }}>
          <div style={{ fontSize:11, fontWeight:800, color:"rgba(255,255,255,0.5)", textTransform:"uppercase", letterSpacing:2, marginBottom:8 }}>La Fabrique à Menus — PNNS</div>
          <h1 style={{ fontSize:30, fontWeight:900, color:"white", margin:"0 0 20px", lineHeight:1.15 }}>
            Recettes<br/>
            <span style={{ color:"#5DCAA5" }}>équilibrées</span>
          </h1>

          {/* Barre de recherche */}
          <div style={{ position:"relative" }}>
            <span style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", fontSize:16, opacity:0.5 }}>🔍</span>
            <input value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Rechercher une recette..."
              style={{ width:"100%", boxSizing:"border-box", background:"rgba(255,255,255,0.12)", border:"1px solid rgba(255,255,255,0.2)", borderRadius:12, padding:"12px 16px 12px 42px", fontSize:14, color:"white", outline:"none" }} />
          </div>

          {/* Stats */}
          {filtreProfil && (
            <div style={{ display:"inline-flex", alignItems:"center", gap:8, background:"rgba(255,255,255,0.15)", borderRadius:20, padding:"5px 14px", marginTop:14 }}>
              <span style={{ fontSize:12, color:"white", fontWeight:700 }}>Filtre : {filtreProfil}</span>
              <button onClick={() => setFiltreProfil(null)} style={{ background:"none", border:"none", color:"rgba(255,255,255,0.7)", cursor:"pointer", fontSize:14, fontWeight:900, padding:0 }}>✕</button>
            </div>
          )}
        </div>

        {/* Catégories scrollables */}
        <div style={{ display:"flex", gap:8, padding:"0 20px 0", overflowX:"auto", scrollbarWidth:"none", paddingBottom:0 }}>
          {["Tout", ...Object.keys(catIcons)].map(cat => (
            <button key={cat} onClick={() => setSelectedCat(cat)}
              style={{
                flexShrink:0, display:"flex", alignItems:"center", gap:6,
                background: selectedCat===cat ? "white" : "rgba(255,255,255,0.1)",
                color: selectedCat===cat ? (catColors[cat]||"#1A3A5C") : "rgba(255,255,255,0.8)",
                border: selectedCat===cat ? "none" : "1px solid rgba(255,255,255,0.2)",
                borderRadius:"20px 20px 0 0", padding:"9px 18px", fontSize:13, fontWeight:800, cursor:"pointer",
                transition:"all 0.15s"
              }}>
              {catIcons[cat] && <span style={{fontSize:14}}>{catIcons[cat]}</span>}
              {cat}
            </button>
          ))}
        </div>
      </div>'''

NEW_HEADER = '''      {/* Header — design site (orange/crème) */}
      <div style={{ background:"#c4622d", borderBottom:"3px solid #222" }}>
        <div style={{ padding:"12px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
          <button onClick={onBack}
            style={{ display:"flex", alignItems:"center", gap:6, background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 14px", boxShadow:"2px 2px 0 #222" }}>
            ← Retour
          </button>
          <span style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:700, textTransform:"uppercase", letterSpacing:1 }}>mangerbouger.fr</span>
        </div>

        <div style={{ padding:"4px 20px 20px" }}>
          <h1 style={{ fontSize:28, fontWeight:900, color:"white", margin:"0 0 14px", lineHeight:1.15, textShadow:"2px 2px 0 rgba(0,0,0,0.2)" }}>
            🍽 Recettes <span style={{ color:"#ffdd44" }}>équilibrées</span>
          </h1>

          {/* Barre de recherche */}
          <div style={{ position:"relative" }}>
            <span style={{ position:"absolute", left:12, top:"50%", transform:"translateY(-50%)", fontSize:15 }}>🔍</span>
            <input value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Rechercher une recette..."
              style={{ width:"100%", boxSizing:"border-box", background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, padding:"10px 14px 10px 38px", fontSize:13, color:"white", outline:"none" }} />
          </div>

          {filtreProfil && (
            <div style={{ display:"inline-flex", alignItems:"center", gap:8, background:"rgba(255,255,255,0.2)", borderRadius:20, padding:"4px 12px", marginTop:10, border:"1px solid rgba(255,255,255,0.4)" }}>
              <span style={{ fontSize:11, color:"white", fontWeight:700 }}>Filtre actif : {filtreProfil}</span>
              <button onClick={() => setFiltreProfil(null)} style={{ background:"none", border:"none", color:"rgba(255,255,255,0.8)", cursor:"pointer", fontSize:13, fontWeight:900, padding:0 }}>✕</button>
            </div>
          )}
        </div>
      </div>'''

code = p(code, OLD_HEADER, NEW_HEADER, "1. Header recettes design orange")

# ══════════════════════════════════════════════
# FIX 2 — Remplacer les onglets catégories + sous-filtres
# par seulement 2 onglets : "Toutes les recettes" / "Recettes personnalisées"
# ══════════════════════════════════════════════

OLD_ONGLETS = '''      {/* Onglets Pour vous / Toutes les recettes */}
      <div style={{ background:"white", borderBottom:"2px solid #E8EDF2", display:"flex" }}>
        {[["toutes","🍽 Toutes les recettes"],["vous","⭐ Recettes pour vous"]].map(([id,label]) => (
          <button key={id}
            onClick={()=>{
              const isPourVous = id==="vous";
              setFiltrePourVous(isPourVous);
              if(isPourVous) setFiltreProfil(filtreProfilInitial || null);
              else setFiltreProfil(null);
            }}
            style={{ flex:1, padding:"14px 12px", fontSize:13, fontWeight:800, border:"none", borderBottom:`3px solid ${filtrePourVous===(id==="vous")?"#FA8072":"transparent"}`, cursor:"pointer", background:"none", color:filtrePourVous===(id==="vous")?"#FA8072":"#6B7280", transition:"all 0.15s" }}>
            {label}
          </button>
        ))}
      </div>

      {/* Sous-filtres tags */}
      <div style={{ background:"white", borderBottom:"1px solid #E8EDF2", padding:"10px 20px", display:"flex", gap:8, alignItems:"center" }}>
        {["Tout","Sans cuisson","Cuisson rapide"].map(tag => (
          <button key={tag} onClick={() => setSelectedTag(tag)}
            style={{
              background: selectedTag===tag ? (tag==="Sans cuisson"?"#00BFA5":tag==="Cuisson rapide"?"#FF6B35":"#1A3A5C") : "transparent",
              color: selectedTag===tag ? "white" : "#6B7280",
              border: `1px solid ${selectedTag===tag ? "transparent" : "#E8EDF2"}`,
              borderRadius:20, padding:"5px 14px", fontSize:12, fontWeight:700, cursor:"pointer"
            }}>{tag}</button>
        ))}
        <span style={{ marginLeft:"auto", fontSize:12, color:"#9CA3AF", fontWeight:600 }}>{filtered.length} recette{filtered.length>1?"s":""}</span>
      </div>'''

NEW_ONGLETS = '''      {/* Onglets : Toutes / Personnalisées */}
      <div style={{ background:"#f4dcbf", borderBottom:"3px solid #222", display:"flex" }}>
        {[["toutes","🍽 Toutes les recettes"],["vous","⭐ Recettes personnalisées"]].map(([id,label]) => (
          <button key={id}
            onClick={()=>{
              const isPourVous = id==="vous";
              setFiltrePourVous(isPourVous);
              if(isPourVous) setFiltreProfil(filtreProfilInitial || null);
              else setFiltreProfil(null);
            }}
            style={{
              flex:1, padding:"14px 12px", fontSize:14, fontWeight:900,
              border:"none", borderBottom:`4px solid ${filtrePourVous===(id==="vous")?"#c4622d":"transparent"}`,
              cursor:"pointer", background:"none",
              color:filtrePourVous===(id==="vous")?"#c4622d":"#888",
              transition:"all 0.15s"
            }}>
            {label}
          </button>
        ))}
      </div>

      {/* Barre infos */}
      <div style={{ background:"#fff8f0", borderBottom:"2px solid #e8d5b0", padding:"8px 20px", display:"flex", alignItems:"center", gap:8 }}>
        <span style={{ fontSize:12, color:"#c4622d", fontWeight:700 }}>
          {filtrePourVous ? "Recettes adaptées à votre profil" : "Toutes les recettes PNNS — mangerbouger.fr"}
        </span>
        <span style={{ marginLeft:"auto", fontSize:12, color:"#c4622d", fontWeight:800, background:"#f4dcbf", borderRadius:20, padding:"2px 10px" }}>
          {filtered.length} recette{filtered.length>1?"s":""}
        </span>
      </div>'''

code = p(code, OLD_ONGLETS, NEW_ONGLETS, "2. Onglets recettes simplifiés + design site")

# ══════════════════════════════════════════════
# FIX 3 — Grille recettes : fond crème au lieu de blanc/gris
# ══════════════════════════════════════════════
code = p(code,
    '<div style={{ padding:"20px", display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(280px, 1fr))", gap:16, maxWidth:1200, margin:"0 auto" }}>',
    '<div style={{ padding:"20px", display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(280px, 1fr))", gap:16, maxWidth:1200, margin:"0 auto", background:"#f4dcbf", minHeight:"calc(100vh - 180px)" }}>',
    "3. Grille fond crème")

# ══════════════════════════════════════════════
# FIX 4 — Cartes recettes : bordure orange style site
# ══════════════════════════════════════════════
code = p(code,
    'style={{ background:"white", borderRadius:20, overflow:"hidden", cursor:"pointer", border:"1px solid #E8EDF2", transition:"transform 0.18s, box-shadow 0.18s", boxShadow:"0 2px 10px rgba(26,58,92,0.05)" }}',
    'style={{ background:"white", borderRadius:16, overflow:"hidden", cursor:"pointer", border:"3px solid #222", transition:"transform 0.18s, box-shadow 0.18s", boxShadow:"4px 4px 0 #222" }}',
    "4. Cartes recettes style site")

# ══════════════════════════════════════════════
# FIX 5 — Hover cartes recettes
# ══════════════════════════════════════════════
code = p(code,
    'onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-5px)";e.currentTarget.style.boxShadow="0 12px 32px rgba(26,58,92,0.14)";}}\n              onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="0 2px 10px rgba(26,58,92,0.05)";}}>',
    'onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-4px)";e.currentTarget.style.boxShadow="6px 6px 0 #222";}}\n              onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="4px 4px 0 #222";}}>',
    "5. Hover cartes recettes style site")

# ══════════════════════════════════════════════
# FIX 6 — "Aucune recette" message style site
# ══════════════════════════════════════════════
code = p(code,
    '<div style={{ gridColumn:"1/-1", textAlign:"center", padding:"60px 20px", color:"#9CA3AF" }}>',
    '<div style={{ gridColumn:"1/-1", textAlign:"center", padding:"60px 20px", color:"#c4622d" }}>',
    "6. Aucune recette couleur")

# ══════════════════════════════════════════════
# FIX 7 — Bouton "Voir la recette" style site
# ══════════════════════════════════════════════
code = p(code,
    '<div style={{ background:col, borderRadius:10, padding:"10px 14px", textAlign:"center", color:"white", fontSize:13, fontWeight:800 }}>\n                  Voir la recette →\n                </div>',
    '<div style={{ background:"#FA8072", border:"2px solid #222", borderRadius:10, padding:"10px 14px", textAlign:"center", color:"white", fontSize:13, fontWeight:800, boxShadow:"2px 2px 0 #222" }}>\n                  Voir la recette →\n                </div>',
    "7. Bouton voir recette style site")

# ══════════════════════════════════════════════
# FIX 8 — Vue détail recette: header style site
# ══════════════════════════════════════════════
code = p(code,
    '<div style={{ position:"sticky", top:0, zIndex:10, background:"white", borderBottom:"1px solid #E8EDF2", padding:"12px 20px", display:"flex", alignItems:"center", gap:12 }}>',
    '<div style={{ position:"sticky", top:0, zIndex:10, background:"#c4622d", borderBottom:"3px solid #222", padding:"12px 20px", display:"flex", alignItems:"center", gap:12, boxShadow:"0 3px 0 #222" }}>',
    "8. Header détail recette style site")

code = p(code,
    'style={{ display:"flex", alignItems:"center", gap:6, background:"none", border:"1px solid #E8EDF2", borderRadius:10, color:"#1A3A5C", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>\n            ← Toutes les recettes',
    'style={{ display:"flex", alignItems:"center", gap:6, background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 14px", boxShadow:"2px 2px 0 #222" }}>\n            ← Toutes les recettes',
    "9. Bouton retour détail recette")

# ══════════════════════════════════════════════
# FIX 9 — fond général de RecettesScreen: blanc → crème
# ══════════════════════════════════════════════
code = p(code,
    "position:\"fixed\", inset:0, background:\"#F8FAFC\", fontFamily:\"'Segoe UI', Arial, sans-serif\", overflowY:\"auto\" }}>",
    "position:\"fixed\", inset:0, background:\"#f4dcbf\", fontFamily:\"'Segoe UI', Arial, sans-serif\", overflowY:\"auto\" }}>",
    "9b. Fond RecettesScreen crème")

print(f"\n{'='*40}")
print(f"Fixes: {fixes} ✅  Erreurs: {len(errors)}")
if errors:
    print(f"Manquants: {', '.join(errors)}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
