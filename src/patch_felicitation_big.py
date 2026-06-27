"""
PATCH — Page félicitations plus grande
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = '''      <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:24, maxWidth:520, width:"100%", textAlign:"center" }}>

          {/* Badge étoiles */}
          <div style={{ background:"linear-gradient(135deg, #ffdd44, #FA8072)", borderRadius:"50%", width:140, height:140, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", boxShadow:"0 0 40px rgba(255,220,50,0.6), 0 8px 32px rgba(0,0,0,0.4)", border:"4px solid #fff" }}>
            <div style={{ fontSize:48 }}>🏆</div>
            <div style={{ fontSize:22, color:"white" }}>★★★★★</div>
          </div>

          {/* Titre */}
          <div>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:"0 0 8px" }}>
              Félicitations {playerName} ! 🎉
            </h1>
            <p style={{ color:"rgba(255,255,255,0.85)", fontSize:16, margin:0, lineHeight:1.6 }}>
              Tu as complété toutes les missions nutritionnelles !<br/>
              Ton profil complet a été enregistré.
            </p>
          </div>

          {/* Récap badges */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12, width:"100%" }}>
            {[
              { icon:"🥗", label:"Habitudes alimentaires", color:"#FA8072" },
              { icon:"👨‍🍳", label:"Fabrique à Menus", color:"#ffcc00" },
              { icon:"🍽️", label:"Compose ton assiette", color:"#9ACD32" },
              { icon:"🏥", label:"Profil santé", color:"#7C3AED" },
            ].map((b,i) => (
              <div key={i} style={{ background:"rgba(255,255,255,0.15)", border:`2px solid ${b.color}`, borderRadius:14, padding:"12px 16px", display:"flex", alignItems:"center", gap:10 }}>
                <span style={{ fontSize:24 }}>{b.icon}</span>
                <div style={{ textAlign:"left" }}>
                  <div style={{ fontSize:12, fontWeight:800, color:"white" }}>{b.label}</div>
                  <div style={{ fontSize:11, color:"#ffdd44", fontWeight:700 }}>★★★★★ Complété</div>
                </div>
              </div>
            ))}
          </div>

          {/* Boutons */}
          <div style={{ display:"flex", flexDirection:"column", gap:12, width:"100%" }}>
            <button onClick={() => alert("Dashboard en cours de développement !")}
              style={{ background:"#ffdd44", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"5px 5px 0 #222" }}>
              📊 Accéder à mon dashboard →
            </button>
            <button onClick={() => { setPhase("select"); setPhaseHistory([]); }}
              style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:12, color:"white", fontSize:14, fontWeight:700, padding:"12px", cursor:"pointer" }}>
              ← Retour au menu
            </button>
          </div>

        </div>'''

NEW = '''      <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:32, maxWidth:780, width:"100%", textAlign:"center" }}>

          {/* Badge étoiles */}
          <div style={{ background:"linear-gradient(135deg, #ffdd44, #FA8072)", borderRadius:"50%", width:200, height:200, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", boxShadow:"0 0 60px rgba(255,220,50,0.7), 0 12px 40px rgba(0,0,0,0.5)", border:"5px solid #fff" }}>
            <div style={{ fontSize:70 }}>🏆</div>
            <div style={{ fontSize:28, color:"white", letterSpacing:4 }}>★★★★★</div>
          </div>

          {/* Titre */}
          <div>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:52, fontWeight:900, color:"white", textShadow:"4px 4px 0 rgba(0,0,0,0.3)", margin:"0 0 12px", lineHeight:1.1 }}>
              Félicitations {playerName} ! 🎉
            </h1>
            <p style={{ color:"rgba(255,255,255,0.9)", fontSize:20, margin:0, lineHeight:1.6 }}>
              Tu as complété toutes les missions nutritionnelles !<br/>
              Ton profil complet a été enregistré.
            </p>
          </div>

          {/* Récap badges */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, width:"100%" }}>
            {[
              { icon:"🥗", label:"Habitudes alimentaires", color:"#FA8072" },
              { icon:"👨‍🍳", label:"Fabrique à Menus", color:"#ffcc00" },
              { icon:"🍽️", label:"Compose ton assiette", color:"#9ACD32" },
              { icon:"🏥", label:"Profil santé", color:"#7C3AED" },
            ].map((b,i) => (
              <div key={i} style={{ background:"rgba(255,255,255,0.18)", border:`3px solid ${b.color}`, borderRadius:20, padding:"20px 24px", display:"flex", alignItems:"center", gap:16, boxShadow:`0 4px 20px ${b.color}44` }}>
                <span style={{ fontSize:40 }}>{b.icon}</span>
                <div style={{ textAlign:"left" }}>
                  <div style={{ fontSize:16, fontWeight:900, color:"white", marginBottom:4 }}>{b.label}</div>
                  <div style={{ fontSize:14, color:"#ffdd44", fontWeight:800, letterSpacing:2 }}>★★★★★ Complété</div>
                </div>
              </div>
            ))}
          </div>

          {/* Boutons */}
          <div style={{ display:"flex", flexDirection:"column", gap:14, width:"100%" }}>
            <button onClick={() => alert("Dashboard en cours de développement !")}
              style={{ background:"#ffdd44", border:"4px solid #222", borderRadius:16, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, padding:"20px", cursor:"pointer", boxShadow:"6px 6px 0 #222" }}>
              📊 Accéder à mon dashboard →
            </button>
            <button onClick={() => { setPhase("select"); setPhaseHistory([]); }}
              style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:14, color:"white", fontSize:16, fontWeight:700, padding:"14px", cursor:"pointer" }}>
              ← Retour au menu
            </button>
          </div>

        </div>'''

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ Page félicitations agrandie")
else:
    print("⚠️ Marqueur non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
