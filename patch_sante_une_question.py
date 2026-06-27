"""
PATCH — QcmSanteScreen : une question par carte, bouton suivant + ✕
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

START = 'function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {'
END = 'export default function App() {'

si = content.find(START)
ei = content.find(END)
if si == -1 or ei == -1:
    print("⚠️ Marqueurs non trouvés"); sys.exit(1)

NEW = '''function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {
  const [step, setStep] = useState(1);
  const [age, setAge] = useState(null);
  const [sexe, setSexe] = useState(null);
  const [silhouette, setSilhouette] = useState(null);
  const [evolution, setEvolution] = useState(null);
  const [seul, setSeul] = useState(null);
  const [autonomie, setAutonomie] = useState(null);
  const [maladie, setMaladie] = useState(null);
  const [pathologies, setPathologies] = useState([]);
  const [traitement, setTraitement] = useState(null);
  const [regime, setRegime] = useState(null);
  const [modeVie, setModeVie] = useState(null);
  const [showMedas, setShowMedas] = useState(false);
  const [showTransitionLLC, setShowTransitionLLC] = useState(false);
  const [medasDone, setMedasDone] = useState(false);
  const [medasResult, setMedasResult] = useState(null);

  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const hasPoids = evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince";
  const silhouettes = sexe === "Homme" ? SILHOUETTES_H : SILHOUETTES_F;
  const sil = silhouette ? getSilhouetteLabel(silhouette) : null;
  const TOTAL = 10;

  const btn = { padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"28px 24px 24px", borderRadius:22, maxWidth:660, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };
  const bubble = (selected) => ({
    display:"flex", alignItems:"center", gap:14,
    border:`2.5px solid ${selected?"#7C3AED":"#ddd"}`,
    borderRadius:99, padding:"12px 20px", fontSize:14, fontWeight:800,
    color:selected?"white":"#333", cursor:"pointer",
    background:selected?"#7C3AED":"white",
    boxShadow:"3px 3px 0 #222", marginBottom:10
  });
  const radio = (selected) => (
    <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${selected?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
      {selected && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
    </div>
  );
  const CloseBtn = () => (
    <button onClick={onBack} style={{ position:"absolute", top:12, right:12, width:34, height:34, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:18, fontWeight:900, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
  );
  const Nav = ({ onPrev, onNext, canNext }) => (
    <div style={{ display:"flex", justifyContent:"space-between", marginTop:20 }}>
      <button onClick={onPrev} style={{ ...btn, background:"white" }}>← Retour</button>
      <button onClick={onNext} style={{ ...btn, opacity:canNext?1:0.4, pointerEvents:canNext?"auto":"none" }}>Suivant →</button>
    </div>
  );

  if (showTransitionLLC && !showMedas) return <TransitionLLCScreen onStart={() => { setShowTransitionLLC(false); setShowMedas(true); }} />;
  if (showMedas && !medasDone) return <QcmMedasScreen onBack={() => setShowMedas(false)} playerName={playerName} onDone={(r) => { setMedasResult(r); setMedasDone(true); setShowMedas(false); setStep(99); }} />;

  const handleFinish = () => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladie, pathologies, traitement, regime, modeVie, medasResult, hasLLC, hasPoids };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom:playerName, email:playerInfos?.email||"" } } });
    onDone(data);
  };

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_orange.png')", backgroundSize:"cover", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"70px 16px 20px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.92)" }} />

      {/* Header */}
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", zIndex:100, boxShadow:"0 3px 0 #222" }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white" }}>🏥 Mon profil santé — {Math.min(step,TOTAL)} / {TOTAL}</div>
        <div style={{ display:"flex", gap:5 }}>
          {Array.from({length:TOTAL}).map((_,i) => (
            <div key={i} style={{ width:22, height:5, borderRadius:3, background:step>i?"#ffcc00":"rgba(255,255,255,0.3)", transition:"background 0.3s" }} />
          ))}
        </div>
      </div>

      {/* Q1 — Âge */}
      {step===1 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🎂</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Quelle est votre catégorie d&apos;âge ?</h2>
          {["Moins de 40 ans","40 à 60 ans","60 à 74 ans","75 à 84 ans","85 ans et plus"].map(a => (
            <div key={a} onClick={()=>setAge(a)} style={bubble(age===a)}>{radio(age===a)}{a}</div>
          ))}
          <Nav onPrev={onBack} onNext={()=>setStep(2)} canNext={!!age} />
        </div>
      )}

      {/* Q2 — Sexe */}
      {step===2 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>👤</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Sexe</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Homme","Femme"].map(s => (
              <div key={s} onClick={()=>setSexe(s)} style={{ ...bubble(sexe===s), flex:1, justifyContent:"center" }}>{s}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(1)} onNext={()=>setStep(3)} canNext={!!sexe} />
        </div>
      )}

      {/* Q3 — Silhouette */}
      {step===3 && (
        <div style={qCard}>
          <CloseBtn />
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:4 }}>Quelle silhouette vous ressemble le plus ?</h2>
          <p style={{ color:"#aaa", fontSize:11, fontStyle:"italic", textAlign:"center", marginBottom:16 }}>Échelle de Stunkard — auto-perception, données non stockées</p>
          <div style={{ display:"flex", gap:6, overflowX:"auto", paddingBottom:8, justifyContent:"center" }}>
            {(sexe==="Homme"?SILHOUETTES_H:SILHOUETTES_F).map(s => (
              <div key={s.score} onClick={()=>setSilhouette(s.score)} style={{ flexShrink:0, display:"flex", flexDirection:"column", alignItems:"center", gap:4, cursor:"pointer" }}>
                <div style={{ width:52, height:95, border:`2.5px solid ${silhouette===s.score?"#7C3AED":"#eee"}`, borderRadius:10, background:silhouette===s.score?"#f3eeff":"#fafafa", display:"flex", alignItems:"center", justifyContent:"center", padding:3 }}
                  dangerouslySetInnerHTML={{ __html: s.svg.replace(/fill="currentColor"/g,`fill="${silhouette===s.score?"#7C3AED":"#bbb"}"`) }} />
                <div style={{ fontSize:11, fontWeight:900, color:silhouette===s.score?"#7C3AED":"#aaa" }}>{s.score}</div>
              </div>
            ))}
          </div>
          {sil && <div style={{ margin:"12px 0", background:sil.bg, border:`2px solid ${sil.color}`, borderRadius:10, padding:"8px 14px", fontSize:13, fontWeight:700, color:sil.color, textAlign:"center" }}>Silhouette {silhouette} — {sil.label}</div>}
          <Nav onPrev={()=>setStep(2)} onNext={()=>setStep(4)} canNext={!!silhouette} />
        </div>
      )}

      {/* Q4 — Évolution */}
      {step===4 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>⚖️</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Cette silhouette est-elle différente de celle d&apos;il y a 6 mois ?</h2>
          {["Beaucoup plus mince","Un peu plus mince","Identique","Un peu plus corpulent(e)","Beaucoup plus corpulent(e)"].map(e => (
            <div key={e} onClick={()=>setEvolution(e)} style={bubble(evolution===e)}>{radio(evolution===e)}{e}</div>
          ))}
          <Nav onPrev={()=>setStep(3)} onNext={()=>setStep(5)} canNext={!!evolution} />
        </div>
      )}

      {/* Q5 — Seul */}
      {step===5 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🏠</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Vivez-vous seul(e) ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setSeul(v)} style={{ ...bubble(seul===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(4)} onNext={()=>setStep(6)} canNext={!!seul} />
        </div>
      )}

      {/* Q6 — Autonomie */}
      {step===6 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🛒</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Faites-vous vos courses et vos repas vous-même ?</h2>
          {["Courses et repas","Courses seulement","Repas seulement","Ni l'un ni l'autre"].map(a => (
            <div key={a} onClick={()=>setAutonomie(a)} style={bubble(autonomie===a)}>{radio(autonomie===a)}{a}</div>
          ))}
          <Nav onPrev={()=>setStep(5)} onNext={()=>setStep(7)} canNext={!!autonomie} />
        </div>
      )}

      {/* Q7 — Maladie chronique */}
      {step===7 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🏥</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Avez-vous une maladie chronique connue ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setMaladie(v)} style={{ ...bubble(maladie===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(6)} onNext={()=>setStep(8)} canNext={!!maladie} />
        </div>
      )}

      {/* Q8 — Pathologies */}
      {step===8 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>📋</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:4 }}>Avez-vous l&apos;une de ces pathologies ?</h2>
          <p style={{ color:"#aaa", fontSize:12, textAlign:"center", marginBottom:14 }}>Plusieurs réponses possibles</p>
          {["LLC (Leucémie Lymphoïde Chronique)","Diabète","Hypertension","Maladie cardiovasculaire","Insuffisance rénale","Cancer (autre)","Aucune"].map(p => {
            const checked = pathologies.includes(p);
            return (
              <div key={p} onClick={()=>{ if(p==="Aucune"){setPathologies(["Aucune"]);return;} setPathologies(prev=>{const f=prev.filter(x=>x!=="Aucune");return f.includes(p)?f.filter(x=>x!==p):[...f,p];}); }}
                style={{ display:"flex", alignItems:"center", gap:12, border:`2.5px solid ${checked?"#7C3AED":"#ddd"}`, borderRadius:12, padding:"11px 16px", cursor:"pointer", background:checked?"#f3eeff":"white", marginBottom:8, fontSize:13, fontWeight:700 }}>
                <div style={{ width:20, height:20, borderRadius:5, border:`2.5px solid ${checked?"#7C3AED":"#ccc"}`, background:checked?"#7C3AED":"white", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:12, color:"white" }}>{checked?"✓":""}</div>
                {p}
                {p.includes("LLC") && <span style={{ marginLeft:"auto", fontSize:10, background:"#f3eeff", border:"1px solid #7C3AED", borderRadius:20, padding:"2px 8px", color:"#7C3AED", fontWeight:900 }}>QCM spécifique</span>}
              </div>
            );
          })}
          <Nav onPrev={()=>setStep(7)} onNext={()=>setStep(9)} canNext={pathologies.length>0} />
        </div>
      )}

      {/* Q9 — Traitement */}
      {step===9 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>💊</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Suivez-vous un traitement régulier ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setTraitement(v)} style={{ ...bubble(traitement===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(8)} onNext={()=>setStep(10)} canNext={!!traitement} />
        </div>
      )}

      {/* Q10 — Régime + Mode de vie */}
      {step===10 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🥗</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Votre médecin vous a-t-il conseillé un régime particulier ?</h2>
          <div style={{ display:"flex", gap:16, marginBottom:20 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setRegime(v)} style={{ ...bubble(regime===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <h2 style={{ fontSize:"1.2em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:12 }}>Quel est votre mode de vie ?</h2>
          {["Très actif","Actif","Sédentaire"].map(m => (
            <div key={m} onClick={()=>setModeVie(m)} style={bubble(modeVie===m)}>{radio(modeVie===m)}{m}</div>
          ))}
          {hasLLC && <div style={{ background:"#f3eeff", border:"2px solid #7C3AED", borderRadius:10, padding:"10px 14px", fontSize:13, fontWeight:700, color:"#7C3AED", marginTop:8 }}>⚠️ LLC détectée — un QCM sur le régime méditerranéen va suivre.</div>}
          <Nav onPrev={()=>setStep(9)} onNext={()=>{ if(hasLLC){setShowTransitionLLC(true);}else{setStep(99);} }} canNext={!!regime && !!modeVie} />
        </div>
      )}

      {/* Bilan */}
      {step===99 && (
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
          <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%" }}>Terminer mon profil santé →</button>
        </div>
      )}
    </div>
  );
}

'''

content = content[:si] + NEW + content[ei:]
out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ QcmSanteScreen : une question par carte + ✕ + bouton suivant")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
