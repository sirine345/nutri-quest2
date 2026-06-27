#!/usr/bin/env python3
"""
Patch ciblé : Page recommandations QCM1
1. Design dans les couleurs du jeu (orange/vert/rose)
2. Supprimer le bloc "régime méditerranéen" du bas
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

fixes = 0

def p(code, old, new, name):
    global fixes
    if old in code:
        fixes += 1
        print(f"  ✅ {name}")
        return code.replace(old, new, 1)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

print("\n=== Patches ===\n")

# ── 1. Header de RecommandationsQcm1Screen : fond blanc → orange ──
code = p(code,
    '''      <div style={{ background:"#F8FAFC", borderBottom:"1px solid #E8EDF2" }}>
        <div style={{ padding:"14px 20px", display:"flex", alignItems:"center", gap:12 }}>
          <button onClick={onBack} style={{ background:"none", border:"1px solid #E8EDF2", borderRadius:10, color:"#1A3A5C", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px", display:"flex", alignItems:"center", gap:6 }}>← Retour</button>
        </div>
        <div style={{ padding:"8px 20px 24px" }}>
          <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#E0F7F5", borderRadius:20, padding:"4px 12px", marginBottom:12 }}>
            <div style={{ width:6, height:6, borderRadius:"50%", background:"#00BFA5" }} />
            <span style={{ fontSize:11, fontWeight:800, color:"#00897B", textTransform:"uppercase", letterSpacing:1 }}>PNNS — Recommandations personnalisées</span>
          </div>
          <h1 style={{ fontSize:28, fontWeight:900, color:"#1A1A1A", margin:"0 0 6px", lineHeight:1.2 }}>Vos recommandations</h1>
          <p style={{ color:"#6B7280", fontSize:14, margin:0 }}>Basées sur vos habitudes alimentaires déclarées</p>
        </div>
        {/* Score pills */}
        <div style={{ display:"flex", gap:10, padding:"0 20px 20px", overflowX:"auto" }}>
          {[["Légumes & Fruits", nutrition.legumes||0, "#00BFA5","#E0F7F5"],["Protéines", nutrition.poisson||0, "#7C3AED","#F3EEFF"],["À surveiller", Math.max(nutrition.charcuterie||0, nutrition.fastFood||0, nutrition.sucres||0), "#FF6B35","#FFF0EB"]].map(([label, val, col, bg]) => (
            <div key={label} style={{ background:bg, borderRadius:14, padding:"12px 16px", textAlign:"center", minWidth:90, flexShrink:0 }}>
              <div style={{ fontSize:20, fontWeight:900, color:col }}>{val}%</div>
              <div style={{ fontSize:10, color:col, fontWeight:700, marginTop:2 }}>{label}</div>
            </div>
          ))}
        </div>
      </div>''',
    '''      {/* Header orange style jeu */}
      <div style={{ background:"#c4622d", borderBottom:"3px solid #222", boxShadow:"0 3px 0 #222" }}>
        <div style={{ padding:"12px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"7px 14px", boxShadow:"2px 2px 0 #222" }}>← Retour</button>
          <span style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:700, textTransform:"uppercase", letterSpacing:1 }}>PNNS</span>
        </div>
        <div style={{ padding:"4px 20px 20px" }}>
          <h1 style={{ fontSize:28, fontWeight:900, color:"white", margin:"0 0 6px", lineHeight:1.2, textShadow:"2px 2px 0 rgba(0,0,0,0.2)" }}>
            Vos recommandations
          </h1>
          <p style={{ color:"rgba(255,255,255,0.8)", fontSize:14, margin:"0 0 16px" }}>Basées sur vos habitudes alimentaires</p>
          {/* Score pills */}
          <div style={{ display:"flex", gap:10, overflowX:"auto" }}>
            {[
              ["Légumes & Fruits", nutrition.legumes||0, "#9ACD32"],
              ["Protéines", nutrition.poisson||0, "#FA8072"],
              ["À surveiller", Math.max(nutrition.charcuterie||0, nutrition.fastFood||0, nutrition.sucres||0), "#ffcc00"]
            ].map(([label, val, col]) => (
              <div key={label} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:12, padding:"10px 14px", textAlign:"center", minWidth:90, flexShrink:0 }}>
                <div style={{ fontSize:22, fontWeight:900, color:col, textShadow:"1px 1px 0 rgba(0,0,0,0.2)" }}>{val}%</div>
                <div style={{ fontSize:10, color:"white", fontWeight:700, marginTop:2 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>''',
    "1. Header RecommandationsQcm1 style orange")

# ── 2. Fond de la page : blanc → crème ──
code = p(code,
    '<div style={{ position:"fixed", inset:0, background:"#F2F7F2", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>\n      {/* Header vert */}\n      {/* Header Medaviz style */}',
    '<div style={{ position:"fixed", inset:0, background:"#f4dcbf", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>',
    "2. Fond RecommandationsQcm1 crème")

# ── 3. Zone contenu : fond blanc → transparent/crème ──
code = p(code,
    '<div style={{ padding:"20px", background:"#F8FAFC", minHeight:"calc(100% - 200px)" }}>',
    '<div style={{ padding:"20px", minHeight:"calc(100% - 200px)" }}>',
    "3. Zone contenu fond transparent")

# ── 4. Supprimer le bloc "régime méditerranéen" en bas de RecommandationsQcm1Screen ──
code = p(code,
    '''        {/* Bloc méditerranéen */}
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
        </div>''',
    '',
    "4. Supprimer bloc méditerranéen QCM1")

# ── 5. Cartes recommandations : style site (bordure noire, fond blanc) ──
code = p(code,
    'style={{ background:"#fff", borderRadius:20, marginBottom:12, boxShadow: open ? "0 8px 32px rgba(26,58,92,0.12)" : "0 2px 12px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2", overflow:"hidden", transition:"box-shadow 0.2s" }}>',
    'style={{ background:"white", borderRadius:16, marginBottom:12, boxShadow:"4px 4px 0 #222", border:"3px solid #222", overflow:"hidden", transition:"box-shadow 0.2s" }}>',
    "5. Cartes recommandations style site")

# ── 6. Message "Excellentes habitudes" style site ──
code = p(code,
    'style={{ background:"white", borderRadius:20, padding:"32px 24px", textAlign:"center", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>',
    'style={{ background:"white", borderRadius:16, padding:"32px 24px", textAlign:"center", boxShadow:"4px 4px 0 #222", border:"3px solid #222" }}>',
    "6. Bloc excellentes habitudes style site")

print(f"\n{'='*40}")
print(f"Fixes: {fixes}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
