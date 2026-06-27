"""
PATCH — 3 fixes :
1. Supprimer le double bouton "Retour au menu des missions" dans MinijeuScreen
2. Boutons MEDAS deviennent verts au clic (selected state)
3. Bilan QCM Santé : pleine page + recettes cliquables avec détail
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

code = ''.join(lines)
fixes = 0

# ─── FIX 1 : Supprimer le bouton doublon (L935-938) ───
OLD_DOUBLE = '''          <button onClick={onBack}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontSize:14, fontWeight:800, padding:"12px", cursor:"pointer", marginTop:4 }}>
            ← Retour au menu des missions
          </button>
          <button onClick={onBack}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontSize:14, fontWeight:800, padding:"12px", cursor:"pointer", marginTop:4 }}>
            ← Retour au menu des missions
          </button>'''
NEW_DOUBLE = '''          <button onClick={onBack}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontSize:14, fontWeight:800, padding:"12px", cursor:"pointer", marginTop:4 }}>
            ← Retour au menu des missions
          </button>'''

if OLD_DOUBLE in code:
    code = code.replace(OLD_DOUBLE, NEW_DOUBLE)
    fixes += 1; print("✅ FIX 1 — Bouton doublon supprimé")
else:
    print("⚠️ FIX 1 — Doublon non trouvé")

# ─── FIX 2 : Boutons MEDAS avec selected state ───
# Add [selected, setSelected] = useState(null) to QcmMedasScreen
OLD_MEDAS_STATE = '''  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const q = MEDAS_QUESTIONS[step];
  const TOTAL = MEDAS_QUESTIONS.length;
  const qCard = { background:"white", padding:"28px 24px 24px", borderRadius:22, maxWidth:620, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };

  const handleAnswer = (isBon) => {
    const newAnswers = { ...answers, [q.id]: isBon ? 1 : 0 };
    setAnswers(newAnswers);
    if (step < TOTAL - 1) { setStep(s => s + 1); }
    else { const score = Object.values(newAnswers).reduce((a, b) => a + b, 0); onDone({ answers: newAnswers, score }); }
  };'''

NEW_MEDAS_STATE = '''  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selected, setSelected] = useState(null);
  const q = MEDAS_QUESTIONS[step];
  const TOTAL = MEDAS_QUESTIONS.length;
  const qCard = { background:"white", padding:"28px 24px 24px", borderRadius:22, maxWidth:620, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };

  const handleAnswer = (isBon) => {
    setSelected(isBon);
    setTimeout(() => {
      setSelected(null);
      const newAnswers = { ...answers, [q.id]: isBon ? 1 : 0 };
      setAnswers(newAnswers);
      if (step < TOTAL - 1) { setStep(s => s + 1); }
      else { const score = Object.values(newAnswers).reduce((a, b) => a + b, 0); onDone({ answers: newAnswers, score }); }
    }, 300);
  };'''

if OLD_MEDAS_STATE in code:
    code = code.replace(OLD_MEDAS_STATE, NEW_MEDAS_STATE)
    fixes += 1; print("✅ FIX 2a — State selected ajouté dans QcmMedas")

# Update button styles to show selected state
OLD_BTN_OUI = '''          <div onClick={() => handleAnswer(true)} style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#333" }}>{q.bon}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#eee", display:"flex", alignItems:"center", justifyContent:"center", color:"#aaa", fontWeight:900, fontSize:12, transition:"background 0.2s" }}>+1</div>
          </div>
          <div onClick={() => handleAnswer(false)} style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #ddd" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#555" }}>{q.mauvais}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#f0f0f0", display:"flex", alignItems:"center", justifyContent:"center", color:"#aaa", fontWeight:900, fontSize:12 }}>0</div>
          </div>'''

NEW_BTN_OUI = '''          <div onClick={() => handleAnswer(true)}
            style={{ background:selected===true?"#f0f9e0":"white", border:`2.5px solid ${selected===true?"#9ACD32":"#ddd"}`, borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222", transition:"all 0.2s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:selected===true?"#2E7D32":"#333" }}>{q.bon}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:selected===true?"#9ACD32":"#eee", display:"flex", alignItems:"center", justifyContent:"center", color:selected===true?"white":"#aaa", fontWeight:900, fontSize:12, transition:"all 0.2s" }}>+1</div>
          </div>
          <div onClick={() => handleAnswer(false)}
            style={{ background:selected===false?"#fbe9e7":"white", border:`2.5px solid ${selected===false?"#e53935":"#ddd"}`, borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #ddd", transition:"all 0.2s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:selected===false?"#e53935":"#555" }}>{q.mauvais}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:selected===false?"#e53935":"#f0f0f0", display:"flex", alignItems:"center", justifyContent:"center", color:selected===false?"white":"#aaa", fontWeight:900, fontSize:12, transition:"all 0.2s" }}>0</div>
          </div>'''

if OLD_BTN_OUI in code:
    code = code.replace(OLD_BTN_OUI, NEW_BTN_OUI)
    fixes += 1; print("✅ FIX 2b — Boutons MEDAS verts au clic")
else:
    print("⚠️ FIX 2b — Boutons MEDAS non trouvés")

# ─── FIX 3 : Bilan pleine page + recettes cliquables ───
OLD_BILAN = '''      {step===99 && (
        <div style={qCard}>
          <CloseBtn />
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>✅ Bilan de votre profil</h2>
          {hasPoids && <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:10, padding:"12px", marginBottom:12, fontSize:13, fontWeight:700, color:"#e53935" }}>⚠️ Perte de poids détectée — consultez votre médecin.</div>}
          {medasResult && <div style={{ background:medasResult.score>=10?"#e8f5e9":"#fff8e1", border:`2px solid ${medasResult.score>=10?"#2e7d32":"#f57c00"}`, borderRadius:10, padding:"12px", marginBottom:12, fontSize:13, fontWeight:700, color:medasResult.score>=10?"#2e7d32":"#f57c00" }}>🫒 Score MEDAS : {medasResult.score}/14</div>}
          <div style={{ background:"#f9f9f9", borderRadius:12, padding:"14px", marginBottom:16 }}>
            {[["Âge",age],["Sexe",sexe],["Évolution",evolution],["Vit seul(e)",seul],["Mode de vie",modeVie],["Traitement",traitement]].filter(([,v])=>v).map(([k,v])=>(
              <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"5px 0", borderBottom:"1px solid #eee", fontSize:13 }}>
                <span style={{ color:"#888" }}>{k}</span><span style={{ fontWeight:800 }}>{v}</span>
              </div>
            ))}
            {pathologies.length>0 && !pathologies.includes("Aucune") && (
              <div style={{ display:"flex", justifyContent:"space-between", padding:"5px 0", fontSize:13 }}>
                <span style={{ color:"#888" }}>Pathologies</span><span style={{ fontWeight:800, color:"#7C3AED" }}>{pathologies.join(", ")}</span>
              </div>
            )}
          </div>
          {hasLLC && medasResult && (
            <div style={{ marginBottom:16 }}>
              <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:"#9ACD32", marginBottom:12 }}>🫒 Recettes méditerranéennes recommandées</div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
                {RECETTES_DATA.filter(r => r.profils && r.profils.includes("mediterraneen")).slice(0,4).map((r,i) => (
                  <div key={i} style={{ background:"white", borderRadius:14, overflow:"hidden", border:"2px solid #9ACD3244", boxShadow:"0 2px 8px rgba(0,0,0,0.08)" }}>
                    <div style={{ height:80, overflow:"hidden" }}>
                      <img src={r.image} alt={r.titre} style={{ width:"100%", height:"100%", objectFit:"cover" }} onError={e=>e.target.style.display="none"} />
                    </div>
                    <div style={{ padding:"10px 12px" }}>
                      <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A", lineHeight:1.3, marginBottom:4 }}>{r.titre}</div>
                      <div style={{ fontSize:11, color:"#9ACD32", fontWeight:700 }}>⏱ {r.temps}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%" }}>Terminer mon profil santé →</button>
        </div>
      )}'''

NEW_BILAN = '''      {step===99 && (() => {
        const [openRec, setOpenRec] = useState(null);
        const medsRecs = RECETTES_DATA.filter(r => r.profils && r.profils.includes("mediterraneen"));

        if (openRec) return (
          <div style={{ position:"fixed", inset:0, background:"#F8FAFC", overflowY:"auto", zIndex:200 }}>
            <div style={{ position:"sticky", top:0, zIndex:10, background:"white", borderBottom:"1px solid #eee", padding:"12px 20px", display:"flex", alignItems:"center", gap:12 }}>
              <button onClick={() => setOpenRec(null)} style={{ background:"none", border:"1px solid #eee", borderRadius:10, color:"#333", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour au bilan</button>
              <span style={{ fontSize:14, fontWeight:900, color:"#9ACD32" }}>🫒 {openRec.titre}</span>
            </div>
            {openRec.image && <div style={{ height:220, overflow:"hidden" }}><img src={openRec.image} style={{ width:"100%", height:"100%", objectFit:"cover" }} /></div>}
            <div style={{ padding:"20px", maxWidth:680, margin:"0 auto" }}>
              <div style={{ background:"#E0F7F5", borderLeft:"4px solid #00BFA5", borderRadius:"0 12px 12px 0", padding:"12px 16px", marginBottom:20 }}>
                <div style={{ fontSize:11, fontWeight:800, color:"#00897B", textTransform:"uppercase", marginBottom:4 }}>💡 Bénéfice</div>
                <p style={{ margin:0, fontSize:13, color:"#004D40", lineHeight:1.6 }}>{openRec.benefice}</p>
              </div>
              <div style={{ background:"white", borderRadius:16, padding:"20px", marginBottom:16, border:"1px solid #eee" }}>
                <h3 style={{ fontSize:16, fontWeight:900, color:"#1A1A1A", marginBottom:14 }}>Ingrédients</h3>
                <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8 }}>
                  {openRec.ingredients.map((ing,i) => (
                    <div key={i} style={{ fontSize:13, color:"#444", padding:"6px 0", borderBottom:"1px solid #f5f5f5" }}>• {ing}</div>
                  ))}
                </div>
              </div>
              <div style={{ background:"white", borderRadius:16, padding:"20px", border:"1px solid #eee" }}>
                <h3 style={{ fontSize:16, fontWeight:900, color:"#1A1A1A", marginBottom:14 }}>Étapes</h3>
                {openRec.etapes.map((e,i) => (
                  <div key={i} style={{ display:"flex", gap:16, marginBottom:16, alignItems:"flex-start" }}>
                    <span style={{ fontSize:32, fontWeight:900, color:"#9ACD32", lineHeight:1, minWidth:28, flexShrink:0 }}>{i+1}</span>
                    <p style={{ margin:0, fontSize:14, color:"#333", lineHeight:1.7 }}>{e}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

        return (
          <div style={{ position:"fixed", inset:0, background:"#F8FAFC", overflowY:"auto", fontFamily:"Arial, sans-serif" }}>
            {/* Header */}
            <div style={{ background:"#7C3AED", padding:"20px 24px" }}>
              <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>QCM Santé — Résultats</div>
              <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:26, fontWeight:900, color:"white", margin:0 }}>✅ Mon profil santé</h1>
            </div>

            <div style={{ padding:"20px 24px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, maxWidth:900, margin:"0 auto" }}>

              {/* Alertes */}
              <div style={{ gridColumn:"1/-1", display:"flex", flexDirection:"column", gap:10 }}>
                {hasPoids && <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:12, padding:"14px 16px", fontSize:13, fontWeight:700, color:"#e53935" }}>⚠️ Perte de poids détectée — consultez votre médecin pour un bilan nutritionnel.</div>}
                {medasResult && <div style={{ background:medasResult.score>=10?"#e8f5e9":"#fff8e1", border:`2px solid ${medasResult.score>=10?"#2e7d32":"#f57c00"}`, borderRadius:12, padding:"14px 16px", fontSize:13, fontWeight:700, color:medasResult.score>=10?"#2e7d32":"#f57c00" }}>🫒 Score MEDAS : {medasResult.score}/14 — {medasResult.score>=10?"Forte adhésion au régime méditerranéen":medasResult.score>=6?"Adhésion modérée":"Faible adhésion — améliorez votre alimentation méditerranéenne"}</div>}
              </div>

              {/* Profil général */}
              <div style={{ background:"white", borderRadius:16, padding:"18px", border:"1px solid #eee", boxShadow:"0 2px 8px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#7C3AED", textTransform:"uppercase", letterSpacing:1, marginBottom:12 }}>👤 Profil général</div>
                {[["Âge",age],["Sexe",sexe],["Évolution",evolution],["Vit seul(e)",seul],["Mode de vie",modeVie],["Traitement",traitement]].filter(([,v])=>v).map(([k,v])=>(
                  <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"7px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                    <span style={{ color:"#888" }}>{k}</span><span style={{ fontWeight:800, color:"#333" }}>{v}</span>
                  </div>
                ))}
              </div>

              {/* Santé */}
              <div style={{ background:"white", borderRadius:16, padding:"18px", border:"1px solid #eee", boxShadow:"0 2px 8px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1, marginBottom:12 }}>🏥 Santé</div>
                <div style={{ padding:"7px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                  <span style={{ color:"#888" }}>Maladie chronique</span><br/>
                  <span style={{ fontWeight:800, color:"#333" }}>{maladie}</span>
                </div>
                {pathologies.length>0 && !pathologies.includes("Aucune") && (
                  <div style={{ padding:"7px 0", fontSize:13 }}>
                    <span style={{ color:"#888" }}>Pathologies</span><br/>
                    <span style={{ fontWeight:800, color:"#7C3AED" }}>{pathologies.join(", ")}</span>
                  </div>
                )}
              </div>

              {/* Recettes méditerranéennes */}
              {hasLLC && medasResult && (
                <div style={{ gridColumn:"1/-1" }}>
                  <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"#9ACD32", marginBottom:14 }}>🫒 Recettes méditerranéennes recommandées</div>
                  <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(200px, 1fr))", gap:14 }}>
                    {medsRecs.map((r,i) => (
                      <div key={i} onClick={() => setOpenRec(r)} style={{ background:"white", borderRadius:16, overflow:"hidden", border:"2px solid #9ACD3244", boxShadow:"0 2px 10px rgba(0,0,0,0.08)", cursor:"pointer", transition:"transform 0.15s, box-shadow 0.15s" }}
                        onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-4px)";e.currentTarget.style.boxShadow="0 8px 24px rgba(154,205,50,0.25)";}}
                        onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="0 2px 10px rgba(0,0,0,0.08)";}}>
                        <div style={{ height:110, overflow:"hidden", background:"#f0f9e0" }}>
                          <img src={r.image} alt={r.titre} style={{ width:"100%", height:"100%", objectFit:"cover" }} onError={e=>{e.target.style.display="none";}} />
                        </div>
                        <div style={{ padding:"12px 14px" }}>
                          <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A", lineHeight:1.3, marginBottom:6 }}>{r.titre}</div>
                          <div style={{ display:"flex", gap:6, flexWrap:"wrap" }}>
                            <span style={{ background:"#f0f9e0", borderRadius:8, padding:"3px 8px", fontSize:11, fontWeight:700, color:"#639922" }}>⏱ {r.temps}</span>
                            <span style={{ background:"#f0f9e0", borderRadius:8, padding:"3px 8px", fontSize:11, fontWeight:700, color:"#639922" }}>{r.type}</span>
                          </div>
                          <div style={{ marginTop:10, background:"#9ACD32", borderRadius:8, padding:"7px 10px", textAlign:"center", color:"white", fontSize:12, fontWeight:800 }}>Voir la recette →</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Bouton terminer */}
              <div style={{ gridColumn:"1/-1" }}>
                <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%", fontSize:16 }}>
                  Terminer mon profil santé →
                </button>
              </div>
            </div>
          </div>
        );
      })()}'''

if OLD_BILAN in code:
    code = code.replace(OLD_BILAN, NEW_BILAN)
    fixes += 1; print("✅ FIX 3 — Bilan pleine page + recettes cliquables")
else:
    print("⚠️ FIX 3 — Bilan non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
