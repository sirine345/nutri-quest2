"""
PATCH — 
1. Transition LLC → design stylé aux couleurs du jeu
2. QcmMedasScreen → même design que QcmSanteScreen (cartes + ✕ + suivant)
3. MNA déclenché si age >= 75 ans ET perte de poids dans QcmSanteScreen
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ─── FIX 1 : Remplacer TransitionLLCScreen ───
OLD_TRANSITION_START = 'function TransitionLLCScreen({ onStart }) {'
OLD_TRANSITION_END = 'function QcmMedasScreen({ onBack, onDone, playerName }) {'

si = content.find(OLD_TRANSITION_START)
ei = content.find(OLD_TRANSITION_END)

NEW_TRANSITION = '''function TransitionLLCScreen({ onStart }) {
  const [phase, setPhase] = useState(0);
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 300);
    const t2 = setTimeout(() => setPhase(2), 1000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);
  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"40px 24px" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:24, maxWidth:520, width:"100%",
        opacity:phase>=1?1:0, transform:phase>=1?"translateY(0)":"translateY(30px)", transition:"all 0.7s cubic-bezier(0.34,1.56,0.64,1)" }}>
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, width:"100%" }}>
          <img src="/e.png" alt="Max" style={{ width:110, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))", flexShrink:0 }} />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.3)", flex:1,
            opacity:phase>=2?1:0, transform:phase>=2?"translateY(0)":"translateY(16px)", transition:"all 0.5s ease 0.2s" }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
              Tu as mentionné la <strong style={{ color:"#7C3AED" }}>LLC</strong>. 🫒<br/>
              <span style={{ fontSize:14, fontWeight:600, color:"#555" }}>Des études montrent que le <strong>régime méditerranéen</strong> est particulièrement bénéfique. Je vais évaluer ton adhésion — 14 questions rapides !</span>
            </div>
          </div>
        </div>
        <button onClick={onStart} style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px 48px", cursor:"pointer", boxShadow:"5px 5px 0 #222", width:"100%",
          opacity:phase>=2?1:0, transition:"opacity 0.5s ease 0.4s" }}>
          Commencer le questionnaire méditerranéen →
        </button>
      </div>
    </div>
  );
}

'''

content = content[:si] + NEW_TRANSITION + content[ei:]
print("✅ FIX 1 — TransitionLLCScreen redesignée")

# ─── FIX 2 : Remplacer QcmMedasScreen ───
OLD_MEDAS_START = 'function QcmMedasScreen({ onBack, onDone, playerName }) {'
OLD_MEDAS_END = 'function QcmSanteScreen({'

si2 = content.find(OLD_MEDAS_START)
ei2 = content.find(OLD_MEDAS_END)

NEW_MEDAS = '''function QcmMedasScreen({ onBack, onDone, playerName }) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});

  const q = MEDAS_QUESTIONS[step];
  const TOTAL = MEDAS_QUESTIONS.length;

  const btn = { padding:"13px 30px", fontSize:15, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", padding:"28px 24px 24px", borderRadius:22, maxWidth:620, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };

  const handleAnswer = (isBon) => {
    const newAnswers = { ...answers, [q.id]: isBon ? 1 : 0 };
    setAnswers(newAnswers);
    if (step < TOTAL - 1) { setStep(s => s + 1); }
    else { const score = Object.values(newAnswers).reduce((a, b) => a + b, 0); onDone({ answers: newAnswers, score }); }
  };

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"70px 16px 20px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.92)" }} />

      {/* Header */}
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#9ACD32", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", zIndex:100, boxShadow:"0 3px 0 #222" }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white" }}>🫒 Régime méditerranéen — {step+1} / {TOTAL}</div>
        <div style={{ display:"flex", gap:4 }}>
          {Array.from({length:TOTAL}).map((_,i) => (
            <div key={i} style={{ width:16, height:5, borderRadius:3, background:step>i?"#ffcc00":"rgba(255,255,255,0.4)", transition:"background 0.3s" }} />
          ))}
        </div>
      </div>

      <div style={{ ...qCard, position:"relative", zIndex:1 }}>
        <button onClick={onBack} style={{ position:"absolute", top:12, right:12, width:34, height:34, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:18, fontWeight:900, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>

        <div style={{ textAlign:"center", marginBottom:12 }}>
          <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#f0f9e0", border:"2px solid #9ACD32", borderRadius:20, padding:"4px 14px", marginBottom:10 }}>
            <span style={{ fontSize:11, fontWeight:900, color:"#639922", textTransform:"uppercase", letterSpacing:1 }}>Question {step+1}/{TOTAL}</span>
          </div>
          <h2 style={{ fontSize:"1.25em", color:"#FA8072", fontWeight:900, margin:"0 0 6px", lineHeight:1.4 }}>{q.q}</h2>
          {q.note && <p style={{ fontSize:12, color:"#888", fontStyle:"italic", margin:"0 0 16px" }}>{q.note}</p>}
        </div>

        <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
          <div onClick={() => handleAnswer(true)}
            style={{ background:"#f0f9e0", border:"2.5px solid #9ACD32", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222", transition:"all 0.15s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#2E7D32" }}>{q.bon}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#9ACD32", display:"flex", alignItems:"center", justifyContent:"center", color:"white", fontWeight:900, fontSize:12, flexShrink:0 }}>+1</div>
          </div>
          <div onClick={() => handleAnswer(false)}
            style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #ddd", transition:"all 0.15s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:"#555" }}>{q.mauvais}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:"#f0f0f0", display:"flex", alignItems:"center", justifyContent:"center", color:"#aaa", fontWeight:900, fontSize:12, flexShrink:0 }}>0</div>
          </div>
        </div>

        {step > 0 && (
          <button onClick={() => setStep(s => s-1)} style={{ marginTop:16, background:"none", border:"none", color:"#888", fontSize:13, fontWeight:700, cursor:"pointer" }}>← Question précédente</button>
        )}
      </div>
    </div>
  );
}

'''

content = content[:si2] + NEW_MEDAS + content[ei2:]
print("✅ FIX 2 — QcmMedasScreen redesigné style QcmSante")

# ─── FIX 3 : Déclencher MNA si age >= 75 ET perte de poids ───
# In QcmSanteScreen, step 10 button: if hasPoids AND age >= 75 → show MNA before bilan
OLD_STEP10_NAV = '''<Nav onPrev={()=>setStep(9)} onNext={()=>{ if(hasLLC){setShowTransitionLLC(true);}else{setStep(99);} }} canNext={!!regime && !!modeVie} />'''

NEW_STEP10_NAV = '''<Nav onPrev={()=>setStep(9)} onNext={()=>{
  const is75plus = age==="75 à 84 ans" || age==="85 ans et plus";
  const needsMNA = is75plus && hasPoids;
  if(hasLLC){ setShowTransitionLLC(true); }
  else if(needsMNA){ setStep(11); }
  else{ setStep(99); }
}} canNext={!!regime && !!modeVie} />'''

if OLD_STEP10_NAV in content:
    content = content.replace(OLD_STEP10_NAV, NEW_STEP10_NAV)
    print("✅ FIX 3 — Déclencheur MNA ajouté (age >= 75 + perte de poids)")
else:
    print("⚠️ FIX 3 — Nav step 10 non trouvée")

# ─── FIX 4 : Ajouter l'écran MNA (step 11) dans QcmSanteScreen ───
OLD_BILAN = '''      {/* Bilan */}
      {step===99 && ('''

NEW_BILAN = '''      {/* Step 11 — MNA Dénutrition */}
      {step===11 && (
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
      )}

      {/* Bilan */}
      {step===99 && ('''

if OLD_BILAN in content:
    content = content.replace(OLD_BILAN, NEW_BILAN)
    print("✅ FIX 4 — Écran MNA ajouté dans QcmSanteScreen (step 11)")
else:
    print("⚠️ FIX 4 — Bilan marker non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"\nFichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
