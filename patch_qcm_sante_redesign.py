"""
PATCH — Redesign QcmSanteScreen style QCM1
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

START = 'function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {'
END = 'export default function App() {'

start_idx = content.find(START)
end_idx = content.find(END)

if start_idx == -1 or end_idx == -1:
    print("⚠️ Marqueurs non trouvés"); sys.exit(1)

NEW_SCREEN = '''function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {
  const [step, setStep] = useState(1);
  const [age, setAge] = useState(null);
  const [sexe, setSexe] = useState(null);
  const [silhouette, setSilhouette] = useState(null);
  const [evolution, setEvolution] = useState(null);
  const [seul, setSeul] = useState(null);
  const [autonomie, setAutonomie] = useState(null);
  const [maladieChroniqueOui, setMaladieChroniqueOui] = useState(null);
  const [pathologies, setPathologies] = useState([]);
  const [traitement, setTraitement] = useState(null);
  const [regimePrescrit, setRegimePrescrit] = useState(null);
  const [modeVie, setModeVie] = useState(null);
  const [showMedas, setShowMedas] = useState(false);
  const [showTransitionLLC, setShowTransitionLLC] = useState(false);
  const [medasDone, setMedasDone] = useState(false);
  const [medasResult, setMedasResult] = useState(null);

  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const hasPoidsPerte = evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince";
  const silhouettes = sexe === "Homme" ? SILHOUETTES_H : SILHOUETTES_F;
  const sil = silhouette ? getSilhouetteLabel(silhouette) : null;

  const TOTAL = 4;
  const displayStep = Math.min(step, TOTAL);

  const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"28px 24px", borderRadius:22, maxWidth:700, width:"100%", textAlign:"center", border:"3px solid #222", boxShadow:"5px 5px 0 #222" };
  const bubbleChoice = (selected, color="#7C3AED") => ({
    display:"flex", alignItems:"center", gap:14,
    border:`2.5px solid ${selected ? color : "#ddd"}`,
    borderRadius:99, padding:"12px 20px", fontSize:14, fontWeight:800,
    color: selected ? "white" : "#333", cursor:"pointer",
    background: selected ? color : "white",
    boxShadow:"3px 3px 0 #222", marginBottom:10, transition:"all 0.15s"
  });

  if (showTransitionLLC && !showMedas) {
    return <TransitionLLCScreen onStart={() => { setShowTransitionLLC(false); setShowMedas(true); }} />;
  }
  if (showMedas && !medasDone) {
    return <QcmMedasScreen onBack={() => setShowMedas(false)} playerName={playerName}
      onDone={(result) => { setMedasResult(result); setMedasDone(true); setShowMedas(false); setStep(99); }} />;
  }

  const handleFinish = () => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, medasResult, hasLLC, hasPoidsPerte };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email || "" } } });
    onDone(data);
  };

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_orange.png')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"80px 16px 40px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.92)" }} />

      {/* Header */}
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white", textShadow:"1px 1px 0 #222" }}>Mon profil santé — Question {displayStep} / {TOTAL}</div>
        <div style={{ display:"flex", gap:8 }}>
          {[1,2,3,4].map(s => (
            <div key={s} style={{ width:28, height:6, borderRadius:3, background: step>=s ? "#ffcc00" : "rgba(255,255,255,0.3)", transition:"background 0.3s" }} />
          ))}
        </div>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"4px 14px", cursor:"pointer" }}>✕</button>
      </div>

      {/* ÉTAPE 1 — Âge & silhouette */}
      {step === 1 && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:20, fontWeight:900, textAlign:"center" }}>👤 Profil général</h2>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Quelle est votre catégorie d&apos;âge ?</p>
            {["Moins de 40 ans","40 à 60 ans","60 à 74 ans","75 à 84 ans","85 ans et plus"].map(a => (
              <div key={a} onClick={() => setAge(a)} style={bubbleChoice(age===a)}>
                <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${age===a?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
                  {age===a && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
                </div>
                {a}
              </div>
            ))}
          </div>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Sexe</p>
            <div style={{ display:"flex", gap:12 }}>
              {["Homme","Femme"].map(s => (
                <div key={s} onClick={() => setSexe(s)} style={{ ...bubbleChoice(sexe===s), flex:1, textAlign:"center", justifyContent:"center", marginBottom:0 }}>{s}</div>
              ))}
            </div>
          </div>

          {sexe && (
            <div style={{ marginBottom:20 }}>
              <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:4 }}>Quelle silhouette vous ressemble le plus ?</p>
              <p style={{ color:"#aaa", fontSize:11, fontStyle:"italic", marginBottom:12 }}>Échelle de Stunkard — auto-perception, données non stockées</p>
              <div style={{ display:"flex", gap:6, overflowX:"auto", paddingBottom:8 }}>
                {silhouettes.map(s => (
                  <div key={s.score} onClick={() => setSilhouette(s.score)} style={{ flexShrink:0, display:"flex", flexDirection:"column", alignItems:"center", gap:4, cursor:"pointer" }}>
                    <div style={{ width:50, height:90, color:silhouette===s.score?"#7C3AED":"#aaa", border:`2.5px solid ${silhouette===s.score?"#7C3AED":"#eee"}`, borderRadius:10, padding:3, background:silhouette===s.score?"#f3eeff":"#fafafa", display:"flex", alignItems:"center", justifyContent:"center" }}
                      dangerouslySetInnerHTML={{ __html: s.svg.replace(/fill="currentColor"/g, `fill="${silhouette===s.score?"#7C3AED":"#bbb"}"`) }} />
                    <div style={{ fontSize:11, fontWeight:900, color:silhouette===s.score?"#7C3AED":"#aaa" }}>{s.score}</div>
                  </div>
                ))}
              </div>
              {sil && <div style={{ marginTop:8, background:sil.bg, border:`2px solid ${sil.color}`, borderRadius:10, padding:"8px 14px", fontSize:13, fontWeight:700, color:sil.color }}>Silhouette {silhouette} — {sil.label}</div>}
            </div>
          )}

          {silhouette && (
            <div style={{ marginBottom:20 }}>
              <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Cette silhouette est-elle différente de celle d&apos;il y a 6 mois ?</p>
              {["Beaucoup plus mince","Un peu plus mince","Identique","Un peu plus corpulent(e)","Beaucoup plus corpulent(e)"].map(e => (
                <div key={e} onClick={() => setEvolution(e)} style={bubbleChoice(evolution===e)}>
                  <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${evolution===e?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
                    {evolution===e && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
                  </div>
                  {e}
                </div>
              ))}
            </div>
          )}

          {evolution && (
            <>
              <div style={{ marginBottom:20 }}>
                <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Vivez-vous seul(e) ?</p>
                <div style={{ display:"flex", gap:12 }}>
                  {["Oui","Non"].map(v => (
                    <div key={v} onClick={() => setSeul(v)} style={{ ...bubbleChoice(seul===v), flex:1, textAlign:"center", justifyContent:"center", marginBottom:0 }}>{v}</div>
                  ))}
                </div>
              </div>
              <div style={{ marginBottom:20 }}>
                <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Faites-vous vos courses et vos repas vous-même ?</p>
                {["Courses et repas","Courses seulement","Repas seulement","Ni l'un ni l'autre"].map(a => (
                  <div key={a} onClick={() => setAutonomie(a)} style={bubbleChoice(autonomie===a)}>
                    <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${autonomie===a?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
                      {autonomie===a && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
                    </div>
                    {a}
                  </div>
                ))}
              </div>
            </>
          )}

          <div style={{ display:"flex", justifyContent:"space-between" }}>
            <button onClick={onBack} style={{ ...btn, background:"white" }}>← Retour</button>
            {age && sexe && silhouette && evolution && seul && autonomie && (
              <button onClick={() => setStep(2)} style={btn}>Suivant →</button>
            )}
          </div>
        </div>
      )}

      {/* ÉTAPE 2 — Santé */}
      {step === 2 && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:20, fontWeight:900, textAlign:"center" }}>🏥 Santé générale</h2>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Avez-vous une maladie chronique connue ?</p>
            <div style={{ display:"flex", gap:12 }}>
              {["Oui","Non"].map(v => (
                <div key={v} onClick={() => setMaladieChroniqueOui(v)} style={{ ...bubbleChoice(maladieChroniqueOui===v), flex:1, textAlign:"center", justifyContent:"center", marginBottom:0 }}>{v}</div>
              ))}
            </div>
          </div>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:4 }}>Avez-vous l&apos;une de ces pathologies ?</p>
            <p style={{ color:"#aaa", fontSize:11, marginBottom:10 }}>Plusieurs réponses possibles</p>
            {["LLC (Leucémie Lymphoïde Chronique)","Diabète","Hypertension","Maladie cardiovasculaire","Insuffisance rénale","Cancer (autre)","Aucune"].map(p => {
              const checked = pathologies.includes(p);
              return (
                <div key={p} onClick={() => {
                  if (p === "Aucune") { setPathologies(["Aucune"]); return; }
                  setPathologies(prev => { const f = prev.filter(x=>x!=="Aucune"); return f.includes(p)?f.filter(x=>x!==p):[...f,p]; });
                }} style={{ display:"flex", alignItems:"center", gap:12, border:`2.5px solid ${checked?"#7C3AED":"#ddd"}`, borderRadius:12, padding:"11px 16px", cursor:"pointer", background:checked?"#f3eeff":"white", marginBottom:8, fontSize:13, fontWeight:700 }}>
                  <div style={{ width:20, height:20, borderRadius:5, border:`2.5px solid ${checked?"#7C3AED":"#ccc"}`, background:checked?"#7C3AED":"white", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:12, color:"white" }}>{checked?"✓":""}</div>
                  {p}
                  {p.includes("LLC") && <span style={{ marginLeft:"auto", fontSize:11, background:"#f3eeff", border:"1px solid #7C3AED", borderRadius:20, padding:"2px 8px", color:"#7C3AED", fontWeight:900 }}>QCM spécifique</span>}
                </div>
              );
            })}
          </div>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Suivez-vous un traitement régulier ?</p>
            <div style={{ display:"flex", gap:12 }}>
              {["Oui","Non"].map(v => (
                <div key={v} onClick={() => setTraitement(v)} style={{ ...bubbleChoice(traitement===v), flex:1, textAlign:"center", justifyContent:"center", marginBottom:0 }}>{v}</div>
              ))}
            </div>
          </div>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Votre médecin vous a-t-il conseillé un régime particulier ?</p>
            <div style={{ display:"flex", gap:12 }}>
              {["Oui","Non"].map(v => (
                <div key={v} onClick={() => setRegimePrescrit(v)} style={{ ...bubbleChoice(regimePrescrit===v), flex:1, textAlign:"center", justifyContent:"center", marginBottom:0 }}>{v}</div>
              ))}
            </div>
          </div>

          {hasLLC && (
            <div style={{ background:"#f3eeff", border:"2px solid #7C3AED", borderRadius:12, padding:"12px 16px", marginBottom:14 }}>
              <div style={{ fontSize:13, fontWeight:900, color:"#7C3AED" }}>⚠️ LLC détectée — un questionnaire sur le régime méditerranéen vous sera proposé.</div>
            </div>
          )}

          <div style={{ display:"flex", justifyContent:"space-between" }}>
            <button onClick={() => setStep(1)} style={{ ...btn, background:"white" }}>← Retour</button>
            {maladieChroniqueOui && pathologies.length > 0 && traitement && regimePrescrit && (
              <button onClick={() => setStep(3)} style={btn}>Suivant →</button>
            )}
          </div>
        </div>
      )}

      {/* ÉTAPE 3 — Activité */}
      {step === 3 && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:20, fontWeight:900, textAlign:"center" }}>🏃 Activité physique</h2>

          <div style={{ marginBottom:20 }}>
            <p style={{ color:"#555", fontSize:13, fontWeight:800, marginBottom:8 }}>Quel est votre mode de vie ?</p>
            {["Très actif","Actif","Sédentaire"].map(m => (
              <div key={m} onClick={() => setModeVie(m)} style={bubbleChoice(modeVie===m)}>
                <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${modeVie===m?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
                  {modeVie===m && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
                </div>
                {m}
              </div>
            ))}
          </div>

          <div style={{ display:"flex", justifyContent:"space-between" }}>
            <button onClick={() => setStep(2)} style={{ ...btn, background:"white" }}>← Retour</button>
            {modeVie && (
              <button onClick={() => {
                if (hasLLC) { setShowTransitionLLC(true); }
                else { setStep(99); }
              }} style={btn}>
                {hasLLC ? "Suivant → QCM méditerranéen" : "Voir mon bilan →"}
              </button>
            )}
          </div>
        </div>
      )}

      {/* ÉTAPE 99 — Bilan */}
      {step === 99 && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:20, fontWeight:900, textAlign:"center" }}>✅ Bilan de votre profil</h2>

          {hasPoidsPerte && (
            <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:12, padding:"14px 16px", marginBottom:14 }}>
              <div style={{ fontSize:13, fontWeight:900, color:"#e53935" }}>⚠️ Perte de poids détectée</div>
              <div style={{ fontSize:13, color:"#555", marginTop:4, lineHeight:1.6 }}>Votre silhouette a évolué vers la maigreur. Consultez votre médecin pour un bilan nutritionnel.</div>
            </div>
          )}

          {medasResult && (
            <div style={{ background:medasResult.score>=10?"#e8f5e9":medasResult.score>=6?"#fff8e1":"#fbe9e7", border:`2px solid ${medasResult.score>=10?"#2e7d32":medasResult.score>=6?"#f57c00":"#e53935"}`, borderRadius:12, padding:"14px 16px", marginBottom:14 }}>
              <div style={{ fontSize:13, fontWeight:900, color:medasResult.score>=10?"#2e7d32":medasResult.score>=6?"#f57c00":"#e53935" }}>
                🫒 Score MEDAS : {medasResult.score}/14 — {medasResult.score>=10?"Forte adhésion au régime méditerranéen":medasResult.score>=6?"Adhésion modérée":"Faible adhésion"}
              </div>
            </div>
          )}

          <div style={{ background:"#f9f9f9", borderRadius:12, padding:"16px", marginBottom:20 }}>
            {[["Âge",age],["Sexe",sexe],["Évolution silhouette",evolution],["Vit seul(e)",seul],["Mode de vie",modeVie],["Traitement",traitement]].map(([k,v])=>v&&(
              <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"6px 0", borderBottom:"1px solid #eee", fontSize:13 }}>
                <span style={{ color:"#888" }}>{k}</span>
                <span style={{ fontWeight:800, color:"#333" }}>{v}</span>
              </div>
            ))}
            {pathologies.length>0 && !pathologies.includes("Aucune") && (
              <div style={{ display:"flex", justifyContent:"space-between", padding:"6px 0", fontSize:13 }}>
                <span style={{ color:"#888" }}>Pathologies</span>
                <span style={{ fontWeight:800, color:"#7C3AED", textAlign:"right", maxWidth:"60%" }}>{pathologies.join(", ")}</span>
              </div>
            )}
          </div>

          <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%" }}>
            Terminer mon profil santé →
          </button>
        </div>
      )}
    </div>
  );
}

'''

content = content[:start_idx] + NEW_SCREEN + content[end_idx:]

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ QcmSanteScreen redesigné style QCM1")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
