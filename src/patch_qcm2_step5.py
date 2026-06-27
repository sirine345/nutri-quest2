"""
PATCH — Réinsère step 5 (Nombre de repas) dans QCM2 et corrige la fin
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Step 4 button calls next(4,...) which does setStep(5) but step 5 doesn't exist
# Fix: step 4 button should call setDone(true) directly instead of going to step 5

OLD_STEP4_BTN = "            <button onClick={()=>cuisine&&next(4,{\"‍ En cuisine\":cuisine})} style={{ ...btn, opacity:!cuisine?0.4:1, poi"

# Find the full line
import re
m = re.search(r'<button onClick=\{\(\)=>cuisine&&next\(4,\{[^\}]+\}\)\}[^\n]+', code)
if m:
    old_btn = m.group(0)
    print(f"Found step 4 btn: {old_btn[:80]}")

# Add step 5 (Nombre de repas) before the closing </div> of Qcm2Screen
OLD_CLOSING = '''    </div>
  );
}


/* ══ TRANSITION LLC → MEDAS ══ */'''

NEW_CLOSING = '''      {step === 5 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/oeuf.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Nombre de repas</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>En semaine, vous préparez à manger :</p>
          {["Midi uniquement","Midi et soir","Soir uniquement"].map(o=>(
            <div key={o} onClick={()=>setRepas(o)} style={bubbleStyle(repas===o)}>
              <div style={{ width:18, height:18, borderRadius:"50%", border:"2.5px solid", borderColor:repas===o?"white":"#74b87a", background:"white", display:"flex", alignItems:"center", justifyContent:"center" }}>
                {repas===o&&<div style={{ width:8, height:8, borderRadius:"50%", background:"#74b87a" }} />}
              </div>
              {repas===o}
            </div>
          ))}
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={()=>setStep(4)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={()=>{ if(!repas) return; setAnswers(prev=>({...prev," Nombre de repas":repas})); setDone(true); }} style={{ ...btn, opacity:!repas?0.4:1, pointerEvents:!repas?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button onClick={onBack} style={{ position:"absolute", top:10, right:10, width:35, height:35, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:20, fontWeight:"bold", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
          </div>
        </div>
      )}

    </div>
  );
}


/* ══ TRANSITION LLC → MEDAS ══ */'''

if OLD_CLOSING in code:
    code = code.replace(OLD_CLOSING, NEW_CLOSING)
    print("✅ Step 5 Nombre de repas réinséré")
else:
    print("⚠️ Closing marker non trouvé")

# Also add repas state if missing
if 'const [repas, setRepas]' not in code:
    OLD_STATES_QCM2 = '  const [done, setDone] = useState(false);'
    NEW_STATES_QCM2 = '  const [done, setDone] = useState(false);\n  const [repas, setRepas] = useState(null);'
    if OLD_STATES_QCM2 in code:
        code = code.replace(OLD_STATES_QCM2, NEW_STATES_QCM2)
        print("✅ State repas ajouté")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
