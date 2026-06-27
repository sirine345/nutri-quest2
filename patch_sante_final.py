"""
PATCH — 3 fixes QCM Santé :
1. Boutons MEDAS : blancs par défaut, vert au clic
2. Step 11 : vrai QCM dénutrition simplifié (6 questions)
3. Bilan step 99 : recettes méditerranéennes si LLC
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# ─── FIX 1 : Boutons MEDAS blancs → vert au clic ───
OLD_BTN_OUI = '''          <div onClick={() => handleAnswer(true)} style={{ background:"#f0f9e0", border:"2.5px solid #9ACD32", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#2E7D32" }}>{q.bon}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#9ACD32", display:"flex", alignItems:"center", justifyContent:"center", color:"white", fontWeight:900, fontSize:12 }}>+1</div>
          </div>
          <div onClick={() => handleAnswer(false)} style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #ddd" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#555" }}>{q.mauvais}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#f0f0f0", display:"flex", alignItems:"center", justifyContent:"center", color:"#aaa", fontWeight:900, fontSize:12 }}>0</div>
          </div>'''

NEW_BTN_OUI = '''          {[
            { label: q.bon, isBon: true },
            { label: q.mauvais, isBon: false }
          ].map(({ label, isBon }) => {
            const [hov, setHov] = useState(false);
            return (
              <div key={label}
                onClick={() => handleAnswer(isBon)}
                onMouseEnter={() => setHov(true)}
                onMouseLeave={() => setHov(false)}
                style={{ background: hov ? "#f0f9e0" : "white", border:`2.5px solid ${hov?"#9ACD32":"#ddd"}`, borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222", transition:"all 0.15s" }}>
                <span style={{ fontSize:14, fontWeight:800, color: hov ? "#2E7D32" : "#333" }}>{label}</span>
                {isBon && <div style={{ width:28, height:28, borderRadius:"50%", background: hov?"#9ACD32":"#eee", display:"flex", alignItems:"center", justifyContent:"center", color: hov?"white":"#aaa", fontWeight:900, fontSize:12, transition:"all 0.15s" }}>+1</div>}
              </div>
            );
          })}'''

# simpler approach - just change button styles
OLD_OUI = 'onClick={() => handleAnswer(true)} style={{ background:"#f0f9e0", border:"2.5px solid #9ACD32"'
NEW_OUI = 'onClick={() => handleAnswer(true)} style={{ background:"white", border:"2.5px solid #ddd"'
OLD_OUI_TXT = 'color:"#2E7D32" }}>{q.bon}</span>'
NEW_OUI_TXT = 'color:"#333" }}>{q.bon}</span>'
OLD_OUI_DOT = 'background:"#9ACD32", display:"flex", alignItems:"center", justifyContent:"center", color:"white", fontWeight:900, fontSize:12 }}>+1</div>'
NEW_OUI_DOT = 'background:"#eee", display:"flex", alignItems:"center", justifyContent:"center", color:"#aaa", fontWeight:900, fontSize:12, transition:"background 0.2s" }}>+1</div>'

if OLD_OUI in code:
    code = code.replace(OLD_OUI, NEW_OUI)
    code = code.replace(OLD_OUI_TXT, NEW_OUI_TXT)
    code = code.replace(OLD_OUI_DOT, NEW_OUI_DOT)
    fixes += 1; print("✅ FIX 1 — Boutons MEDAS blancs par défaut")

# ─── FIX 2 : Step 11 — vrai QCM dénutrition ───
OLD_STEP11 = '''      {step===11 && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <button onClick={onBack} style={{ position:"absolute", top:12, right:12, width:34, height:34, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:18, fontWeight:900, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
          <div style={{ textAlign:"center", marginBottom:16 }}>
            <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#fbe9e7", border:"2px solid #e53935", borderRadius:20, padding:"4px 14px", marginBottom:10 }}>
              <span style={{ fontSize:11, fontWeight:900, color:"#e53935", textTransform:"uppercase", letterSpacing:1 }}>Dépistage dénutrition</span>
            </div>
            <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, margin:0 }}>🔍 Évaluation nutritionnelle</h2>
            <p style={{ color:"#666", fontSize:13, marginTop:8, lineHeight:1.6 }}>
              En raison de votre âge et de la perte de poids détectée, nous allons effectuer un dépistage rapide de dénutrition (MNA).
            </p>
          </div>
          <div style={{ background:"#fff8e1", border:"2px solid #f57c00", borderRadius:12, padding:"14px 16px", marginBottom:20 }}>
            <div style={{ fontSize:13, fontWeight:900, color:"#f57c00", marginBottom:4 }}>⚠️ Perte de poids après {age}</div>
            <div style={{ fontSize:13, color:"#555", lineHeight:1.6 }}>
              Une perte de poids après 75 ans peut indiquer un risque de dénutrition. Ce questionnaire de 6 questions permet de l&apos;évaluer rapidement.
            </div>
          </div>
          <div style={{ display:"flex", justifyContent:"space-between" }}>
            <button onClick={() => setStep(10)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={() => setStep(99)} style={{ ...btn, background:"#f57c00", color:"white", border:"3px solid #e65100" }}>Passer ce dépistage</button>
            <button onClick={() => setStep(99)} style={{ ...btn }}>Continuer →</button>
          </div>
        </div>
      )}'''

NEW_STEP11 = '''      {step===11 && (() => {
        const MNA_QS = [
          { q:"Le patient présente-t-il une perte d'appétit ces 3 derniers mois ?", opts:[[0,"Baisse sévère"],[1,"Légère baisse"],[2,"Pas de baisse"]], key:"appetit" },
          { q:"Perte de poids récente (< 3 mois) ?", opts:[[0,"Perte > 3 kg"],[1,"Ne sait pas"],[2,"Perte 1-3 kg"],[3,"Pas de perte"]], key:"poids" },
          { q:"Motricité ?", opts:[[0,"Au lit ou fauteuil"],[1,"Autonome à l'intérieur"],[2,"Sort du domicile"]], key:"motricite" },
          { q:"Maladie aiguë ou stress psychologique ces 3 derniers mois ?", opts:[[0,"Oui"],[2,"Non"]], key:"stress" },
          { q:"Problèmes neuropsychologiques ?", opts:[[0,"Démence ou dépression sévère"],[1,"Démence légère"],[2,"Pas de problème"]], key:"neuro" },
          { q:"IMC (Indice de Masse Corporelle) ?", opts:[[0,"< 19"],[1,"19-21"],[2,"21-23"],[3,"≥ 23"]], key:"imc" },
        ];
        const [mnaStep, setMnaStep] = useState(0);
        const [mnaAnswers, setMnaAnswers] = useState({});
        const mnaQ = MNA_QS[mnaStep];
        const mnaScore = Object.values(mnaAnswers).reduce((a,b)=>a+b,0);
        const handleMna = (val) => {
          const newA = { ...mnaAnswers, [mnaQ.key]: val };
          setMnaAnswers(newA);
          if (mnaStep < MNA_QS.length-1) { setMnaStep(s=>s+1); }
          else { setStep(99); }
        };
        return (
          <div style={{ ...qCard, zIndex:1 }}>
            <CloseBtn />
            <div style={{ textAlign:"center", marginBottom:14 }}>
              <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#fbe9e7", border:"2px solid #e53935", borderRadius:20, padding:"4px 14px", marginBottom:10 }}>
                <span style={{ fontSize:11, fontWeight:900, color:"#e53935", textTransform:"uppercase", letterSpacing:1 }}>Dépistage dénutrition MNA — {mnaStep+1}/6</span>
              </div>
              <h2 style={{ fontSize:"1.2em", color:"#FA8072", fontWeight:900, margin:0, lineHeight:1.4 }}>{mnaQ.q}</h2>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
              {mnaQ.opts.map(([val, label]) => (
                <div key={val} onClick={() => handleMna(val)}
                  style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"14px 18px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222" }}>
                  <span style={{ fontSize:13, fontWeight:800, color:"#333" }}>{label}</span>
                  <span style={{ fontSize:12, background:"#f5f5f5", borderRadius:20, padding:"3px 10px", color:"#888", fontWeight:700 }}>{val} pt{val>1?"s":""}</span>
                </div>
              ))}
            </div>
            <div style={{ display:"flex", justifyContent:"space-between", marginTop:16 }}>
              <button onClick={() => mnaStep>0?setMnaStep(s=>s-1):setStep(10)} style={{ ...btn, background:"white" }}>← Retour</button>
              <button onClick={() => setStep(99)} style={{ fontSize:12, fontWeight:700, color:"#aaa", background:"none", border:"none", cursor:"pointer" }}>Passer →</button>
            </div>
          </div>
        );
      })()}'''

if OLD_STEP11 in code:
    code = code.replace(OLD_STEP11, NEW_STEP11)
    fixes += 1; print("✅ FIX 2 — QCM Dénutrition (6 questions MNA)")
else:
    print("⚠️ FIX 2 — Step 11 non trouvé")

# ─── FIX 3 : Bilan — recettes méditerranéennes si LLC ───
OLD_BILAN_BTN = '          <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%" }}>Terminer mon profil santé →</button>'

NEW_BILAN_BTN = '''          {hasLLC && medasResult && (
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
          <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%" }}>Terminer mon profil santé →</button>'''

if OLD_BILAN_BTN in code:
    code = code.replace(OLD_BILAN_BTN, NEW_BILAN_BTN)
    fixes += 1; print("✅ FIX 3 — Recettes méditerranéennes dans le bilan LLC")
else:
    print("⚠️ FIX 3 — Bouton bilan non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
