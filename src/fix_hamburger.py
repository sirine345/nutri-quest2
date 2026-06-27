path = r'C:\Users\fzahi\Desktop\nutri-quest2\src\App.jsx'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

old = '''        <div style={{ padding:"16px 20px", borderTop:"2px solid #eee" }}>
          <button onClick={handleSave}
            style={{ background:"#FA8072", border:"none", borderRadius:12, padding:"12px", fontSize:15, fontWeight:800, color:"white", cursor:"pointer", width:"100%" }}>
            {saved ? " Sauvegardé !" : "Sauvegarder"}
          </button>
        </div>'''

new = '''        <div style={{ padding:"16px 20px", borderTop:"2px solid #eee", display:"flex", flexDirection:"column", gap:10 }}>
          <button onClick={handleSave}
            style={{ background:"#FA8072", border:"none", borderRadius:12, padding:"12px", fontSize:15, fontWeight:800, color:"white", cursor:"pointer", width:"100%" }}>
            {saved ? " Sauvegardé !" : "Sauvegarder"}
          </button>
          <button onClick={() => setShowProfil(p => !p)}
            style={{ background:"#7C3AED", border:"none", borderRadius:12, padding:"12px", fontSize:14, fontWeight:800, color:"white", cursor:"pointer", width:"100%" }}>
            {showProfil ? "Masquer mon profil santé" : "📊 Voir mon profil santé"}
          </button>
          {showProfil && profilData && (
            <div style={{ background:"#f8f8ff", borderRadius:14, padding:"14px", border:"1px solid #7C3AED33" }}>
              <div style={{ fontSize:13, fontWeight:900, color:"#7C3AED", marginBottom:12 }}>Mon profil santé</div>

              {/* Infos générales */}
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:12 }}>
                {[
                  ["🎂", "Âge", profilData.age||"—"],
                  ["👤", "Sexe", profilData.sexe||"—"],
                  ["🏃", "Mode de vie", profilData.mode_vie||"—"],
                  ["📅", "Inscrit le", profilData.created_at ? new Date(profilData.created_at).toLocaleDateString("fr-FR") : "—"],
                ].map(([icon, label, val], i) => (
                  <div key={i} style={{ background:"white", borderRadius:10, padding:"10px 12px", border:"1px solid #eee" }}>
                    <div style={{ fontSize:10, color:"#aaa", fontWeight:700, textTransform:"uppercase", marginBottom:2 }}>{icon} {label}</div>
                    <div style={{ fontSize:13, fontWeight:800, color:"#333" }}>{val}</div>
                  </div>
                ))}
              </div>

              {/* Pathologies */}
              {profilData.pathologies && profilData.pathologies !== "[]" && (
                <div style={{ background:"#f3eeff", borderRadius:10, padding:"10px 12px", marginBottom:12, border:"1px solid #7C3AED33" }}>
                  <div style={{ fontSize:10, color:"#7C3AED", fontWeight:700, textTransform:"uppercase", marginBottom:6 }}>Pathologies déclarées</div>
                  <div style={{ fontSize:12, color:"#333", fontWeight:600 }}>{profilData.pathologies}</div>
                </div>
              )}

              {/* Scores PNNS mini barres */}
              <div style={{ fontSize:10, color:"#aaa", fontWeight:700, textTransform:"uppercase", marginBottom:8 }}>Scores nutritionnels PNNS</div>
              {[
                ["Légumes", profilData.score_legumes||0, "#9ACD32", 70],
                ["Fruits", profilData.score_fruits||0, "#FA8072", 70],
                ["Poisson", profilData.score_poisson||0, "#1976d2", 60],
                ["Charcuterie", profilData.score_charcuterie||0, "#e53935", 20],
                ["Fast-food", profilData.score_fastfood||0, "#f57c00", 20],
              ].map(([label, val, color, target], i) => {
                const pct = Math.min(val, 100);
                const ok = label === "Charcuterie" || label === "Fast-food" ? val <= target : val >= target;
                return (
                  <div key={i} style={{ marginBottom:8 }}>
                    <div style={{ display:"flex", justifyContent:"space-between", fontSize:11, fontWeight:700, color:"#555", marginBottom:3 }}>
                      <span>{label}</span>
                      <span style={{ color: ok ? "#9ACD32" : "#e53935" }}>{val}% {ok ? "✓" : "↓"}</span>
                    </div>
                    <div style={{ height:7, background:"#f0f0f0", borderRadius:99, position:"relative" }}>
                      <div style={{ height:"100%", width:pct+"%", background:color, borderRadius:99 }} />
                      <div style={{ position:"absolute", top:-3, left:target+"%", width:2, height:13, background:"#222", borderRadius:1 }} />
                    </div>
                  </div>
                );
              })}

              {/* Score MEDAS */}
              {profilData.score_medas != null && (
                <div style={{ marginTop:12, background: profilData.score_medas >= 10 ? "#e8f5e9" : profilData.score_medas >= 6 ? "#fff8e1" : "#fbe9e7", borderRadius:10, padding:"10px 12px", border:"1px solid #eee" }}>
                  <div style={{ fontSize:10, color:"#aaa", fontWeight:700, textTransform:"uppercase", marginBottom:4 }}>Score MEDAS</div>
                  <div style={{ fontSize:22, fontWeight:900, color: profilData.score_medas >= 10 ? "#2e7d32" : profilData.score_medas >= 6 ? "#f57c00" : "#e53935" }}>
                    {profilData.score_medas}<span style={{ fontSize:13, color:"#aaa" }}>/14</span>
                  </div>
                  <div style={{ fontSize:11, color:"#666", marginTop:2 }}>
                    {profilData.score_medas >= 10 ? "Forte adhésion méditerranéenne ✓" : profilData.score_medas >= 6 ? "Adhésion modérée" : "Faible adhésion"}
                  </div>
                </div>
              )}
            </div>
          )}
          {showProfil && !profilData && (
            <div style={{ background:"#fff8e1", borderRadius:10, padding:"12px", fontSize:12, color:"#854F0B", border:"1px solid #ffcc0044" }}>
              ⚠️ Complète les QCM pour voir ton profil santé !
            </div>
          )}
        </div>'''

if old in content:
    content = content.replace(old, new)
    # Ajouter showProfil et profilData dans le state du HamburgerMenu
    old2 = "  const [saved, setSaved] = useState(false);"
    new2 = """  const [saved, setSaved] = useState(false);
  const [showProfil, setShowProfil] = useState(false);
  const [profilData, setProfilData] = useState(null);

  React.useEffect(() => {
    if (showProfil && playerInfos?.email) {
      fetch("http://127.0.0.1:8000/dashboard/stats")
        .then(r => r.json())
        .then(d => {
          const me = (d.participants||[]).find(p => p.prenom === playerName || p.prenom === playerInfos.email);
          if (me) setProfilData(me);
        })
        .catch(() => {});
    }
  }, [showProfil]);"""
    if old2 in content:
        content = content.replace(old2, new2)
        print("OK state ajoute")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK profil sante ajoute dans hamburger !')
else:
    print('ERREUR bloc bouton non trouve')
