#!/usr/bin/env python3
"""Refonte QcmSanteScreen - meme style que QCM1"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

START_TAG = "function QcmSanteScreen("
END_TAG   = "/* \u2550\u2550 COMPOSANT MNA POST-SANT\u00c9 \u2550\u2550 */"

idx_fn_start = code.find(START_TAG)
idx_end      = code.find(END_TAG)
idx_start    = code.rfind("\n/*", 0, idx_fn_start)

print(f"START: {idx_start}, END: {idx_end}")

if idx_start == -1 or idx_end == -1 or idx_fn_start == -1:
    # Fallback: chercher par fonction suivante
    END_TAG2 = "function MnaScreen("
    idx_end = code.find(END_TAG2)
    idx_end = code.rfind("\n/*", 0, idx_end)
    print(f"Fallback END: {idx_end}")

NEW = """
/* \u2550\u2550 QCM SANT\u00c9 \u2550\u2550 */
function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {
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
  const [freins, setFreins] = useState([]);
  const [medasResult, setMedasResult] = useState(null);
  const [showMnaPost, setShowMnaPost] = useState(false);

  const TOTAL_STEPS = 9;

  const btn = {
    padding:"14px 28px", fontSize:16, fontWeight:900,
    border:"3px solid #222", borderRadius:12,
    cursor:"pointer", boxShadow:"4px 4px 0 #222",
    fontFamily:"Arial, sans-serif", transition:"transform .1s"
  };

  const handleFinish = () => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, freins, medasResult };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email||"" } } });
    onDone(data);
  };

  if (showMnaPost) {
    return (
      <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        <div style={{ background:"#c4622d", padding:"14px 20px", display:"flex", alignItems:"center", gap:12, borderBottom:"3px solid #222" }}>
          <button onClick={()=>setShowMnaPost(false)} style={{ ...btn, background:"rgba(255,255,255,0.2)", color:"white", border:"2px solid rgba(255,255,255,0.4)", boxShadow:"none", fontSize:13, padding:"6px 14px" }}>← Retour</button>
          <span style={{ color:"white", fontWeight:900, fontSize:15 }}>Bilan MNA \u2014 D\u00e9nutrition</span>
        </div>
        <MnaScreen onBack={()=>setShowMnaPost(false)} onDone={()=>handleFinish()} playerName={playerName} playerInfos={playerInfos} />
      </div>
    );
  }

  // Styles options
  const optStyle = (sel) => ({
    background: sel ? "#c4622d" : "white",
    color: sel ? "white" : "#333",
    border: sel ? "3px solid #222" : "3px solid #ddd",
    borderRadius:12, padding:"13px 16px", fontSize:15, fontWeight:800,
    cursor:"pointer", boxShadow: sel ? "3px 3px 0 #222" : "2px 2px 0 #ddd",
    transition:"all .1s", textAlign:"center"
  });

  const chipStyle = (sel) => ({
    background: sel ? "#FA8072" : "white",
    color: sel ? "white" : "#555",
    border: sel ? "2px solid #222" : "2px solid #ddd",
    borderRadius:10, padding:"10px 14px", fontSize:14, fontWeight:700,
    cursor:"pointer", boxShadow: sel ? "2px 2px 0 #222" : "none",
    transition:"all .1s", textAlign:"center"
  });

  const togglePatho = (p) => {
    if (p === "Aucune") { setPathologies(["Aucune"]); return; }
    setPathologies(prev => {
      const without = prev.filter(x => x !== "Aucune");
      return without.includes(p) ? without.filter(x=>x!==p) : [...without, p];
    });
  };

  // Header commun
  const Header = ({ stepNum, titre, sous }) => (
    <div style={{ background:"#c4622d", borderBottom:"3px solid #222", boxShadow:"0 3px 0 #222" }}>
      <div style={{ padding:"12px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
        <button onClick={stepNum===1 ? onBack : ()=>setStep(s=>s-1)}
          style={{ ...btn, background:"rgba(255,255,255,0.2)", color:"white", border:"2px solid rgba(255,255,255,0.4)", boxShadow:"none", fontSize:13, padding:"6px 14px" }}>
          \u2190 Retour
        </button>
        <span style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:800, textTransform:"uppercase", letterSpacing:1 }}>
          {stepNum} / {TOTAL_STEPS}
        </span>
      </div>
      {/* Barre progression */}
      <div style={{ height:5, background:"rgba(0,0,0,0.2)" }}>
        <div style={{ height:"100%", width:`${(stepNum/TOTAL_STEPS)*100}%`, background:"#ffdd44", transition:"width .4s" }} />
      </div>
      <div style={{ padding:"14px 20px 18px" }}>
        <div style={{ fontSize:11, color:"rgba(255,255,255,0.6)", fontWeight:800, textTransform:"uppercase", letterSpacing:1.5, marginBottom:6 }}>Profil Sant\u00e9</div>
        <div style={{ fontFamily:"Arial Black, Arial", fontSize:22, fontWeight:900, color:"white", textShadow:"1px 1px 0 rgba(0,0,0,0.2)", lineHeight:1.2, marginBottom:4 }}>{titre}</div>
        {sous && <div style={{ fontSize:13, color:"rgba(255,255,255,0.75)" }}>{sous}</div>}
      </div>
    </div>
  );

  const Body = ({ children }) => (
    <div style={{ padding:"20px", background:"#FFF8F0", minHeight:"calc(100vh - 160px)" }}>
      {children}
    </div>
  );

  // ── STEP 1 : \u00c2ge ──
  if (step === 1) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={1} titre="Quelle est ta cat\u00e9gorie d'\u00e2ge ?" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10, marginBottom:20 }}>
          {[["Moins de 40 ans","🧑","/garcon.png"],["40 \u2014 60 ans","🧑","/garcon.png"],["60 \u2014 74 ans","🧓","/e.png"],["74 \u2014 85 ans","👴","/e.png"]].map(([label, emoji, img]) => (
            <div key={label} onClick={()=>{setAge(label);setStep(2);}}
              style={{ ...optStyle(age===label), display:"flex", flexDirection:"column", alignItems:"center", gap:8, padding:"18px 10px" }}>
              <span style={{ fontSize:32 }}>{emoji}</span>
              <span style={{ fontSize:14, fontWeight:800 }}>{label}</span>
            </div>
          ))}
          <div onClick={()=>{setAge("Plus de 85 ans");setStep(2);}}
            style={{ ...optStyle(age==="Plus de 85 ans"), gridColumn:"1/-1", display:"flex", alignItems:"center", justifyContent:"center", gap:10, padding:"16px" }}>
            <span style={{ fontSize:28 }}>👴</span>
            <span style={{ fontSize:15, fontWeight:800 }}>Plus de 85 ans</span>
          </div>
        </div>
      </Body>
    </div>
  );

  // ── STEP 2 : Sexe ──
  if (step === 2) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={2} titre="Quel est ton sexe ?" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
          <div onClick={()=>{setSexe("Homme");setStep(3);}}
            style={{ ...optStyle(sexe==="Homme"), padding:"28px 10px", display:"flex", flexDirection:"column", alignItems:"center", gap:10 }}>
            <img src="/garcon.png" style={{ width:80, height:120, objectFit:"contain" }} />
            <span style={{ fontSize:18, fontWeight:900 }}>Homme</span>
          </div>
          <div onClick={()=>{setSexe("Femme");setStep(3);}}
            style={{ ...optStyle(sexe==="Femme"), padding:"28px 10px", display:"flex", flexDirection:"column", alignItems:"center", gap:10 }}>
            <img src="/fille.png" style={{ width:80, height:120, objectFit:"contain" }} />
            <span style={{ fontSize:18, fontWeight:900 }}>Femme</span>
          </div>
        </div>
      </Body>
    </div>
  );

  // ── STEP 3 : Silhouette ──
  const SILHOUETTES = [
    { num:1, label:"Maigreur", w:22 },
    { num:3, label:"Normal", w:30 },
    { num:5, label:"Surpoids", w:38 },
    { num:7, label:"Ob\u00e9sit\u00e9", w:46 },
  ];
  if (step === 3) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={3} titre="Quelle silhouette te ressemble le plus ?" sous="Auto-\u00e9valuation — donn\u00e9es non stock\u00e9es" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:10, marginBottom:20 }}>
          {SILHOUETTES.map(s => (
            <div key={s.num} onClick={()=>{setSilhouette(s.num);setStep(4);}}
              style={{ ...optStyle(silhouette===s.num), padding:"16px 8px", display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
              <svg width="40" height="64" viewBox="0 0 40 64">
                <ellipse cx="20" cy="7" rx="7" ry="7" fill={silhouette===s.num?"white":"#c4622d"} opacity="0.9"/>
                <rect x={20-s.w/2} y="15" width={s.w} height="28" rx={s.w/3} fill={silhouette===s.num?"white":"#c4622d"} opacity="0.9"/>
                <rect x={20-s.w/2} y="43" width={s.w/2-2} height="18" rx="4" fill={silhouette===s.num?"white":"#c4622d"} opacity="0.9"/>
                <rect x={20+2} y="43" width={s.w/2-2} height="18" rx="4" fill={silhouette===s.num?"white":"#c4622d"} opacity="0.9"/>
              </svg>
              <span style={{ fontSize:13, fontWeight:800 }}>{s.label}</span>
            </div>
          ))}
        </div>
        <div style={{ background:"white", border:"2px solid #e8ddd5", borderRadius:10, padding:"12px 14px", fontSize:12, color:"#888", lineHeight:1.6 }}>
          \u2139\ufe0f Cette \u00e9valuation est indicative. Score 1-2\u00a0: maigreur / 3-4\u00a0: normal / 5-6\u00a0: surpoids / 7-9\u00a0: ob\u00e9sit\u00e9 probable.
        </div>
      </Body>
    </div>
  );

  // ── STEP 4 : \u00c9volution silhouette ──
  if (step === 4) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={4} titre="Ta silhouette a-t-elle chang\u00e9 depuis 6 mois ?" />
      <Body>
        <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
          {["Beaucoup plus mince","Un peu plus mince","Identique","Un peu plus corpulent(e)","Beaucoup plus corpulent(e)"].map(opt => (
            <div key={opt} onClick={()=>{setEvolution(opt);setStep(5);}}
              style={{ ...optStyle(evolution===opt), textAlign:"left", padding:"16px 18px" }}>
              {opt}
            </div>
          ))}
        </div>
      </Body>
    </div>
  );

  // ── STEP 5 : Mode de vie ──
  if (step === 5) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={5} titre="Comment d\u00e9crirais-tu ton mode de vie ?" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10, marginBottom:14 }}>
          {[["S\u00e9dentaire","🪑"],["L\u00e9g\u00e8rement actif","🚶"],["Actif","🚴"],["Tr\u00e8s actif","🏃"]].map(([label, emoji]) => (
            <div key={label} onClick={()=>setModeVie(label)}
              style={{ ...optStyle(modeVie===label), display:"flex", flexDirection:"column", alignItems:"center", gap:8, padding:"18px 10px" }}>
              <span style={{ fontSize:30 }}>{emoji}</span>
              <span style={{ fontSize:14, fontWeight:800 }}>{label}</span>
            </div>
          ))}
        </div>
        <div style={{ marginBottom:14 }}>
          <div style={{ fontSize:14, fontWeight:800, color:"#555", marginBottom:10 }}>Tu vis seul(e) ?</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
            {["Oui","Non"].map(opt => (
              <div key={opt} onClick={()=>setSeul(opt)} style={{ ...optStyle(seul===opt), padding:"14px" }}>{opt}</div>
            ))}
          </div>
        </div>
        <div style={{ marginBottom:20 }}>
          <div style={{ fontSize:14, fontWeight:800, color:"#555", marginBottom:10 }}>Tu fais tes courses et tes repas toi-m\u00eame ?</div>
          <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
            {["Oui, courses et repas","Courses seulement","Repas seulement","Non, aide ext\u00e9rieure"].map(opt => (
              <div key={opt} onClick={()=>setAutonomie(opt)} style={{ ...optStyle(autonomie===opt), padding:"13px 16px", textAlign:"left" }}>{opt}</div>
            ))}
          </div>
        </div>
        {modeVie && seul && autonomie && (
          <button onClick={()=>setStep(6)} style={{ ...btn, background:"#c4622d", color:"white", width:"100%", fontSize:16 }}>
            Continuer \u2192
          </button>
        )}
      </Body>
    </div>
  );

  // ── STEP 6 : Maladie chronique ──
  if (step === 6) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={6} titre="As-tu une maladie chronique connue ?" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:20 }}>
          <div onClick={()=>{setMaladieChroniqueOui(true);setStep(7);}}
            style={{ ...optStyle(maladieChroniqueOui===true), padding:"24px", display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
            <span style={{ fontSize:32 }}>✓</span>
            <span style={{ fontSize:16, fontWeight:900 }}>Oui</span>
          </div>
          <div onClick={()=>{setMaladieChroniqueOui(false);setPathologies(["Aucune"]);setStep(8);}}
            style={{ ...optStyle(maladieChroniqueOui===false), padding:"24px", display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
            <span style={{ fontSize:32 }}>✗</span>
            <span style={{ fontSize:16, fontWeight:900 }}>Non</span>
          </div>
        </div>
      </Body>
    </div>
  );

  // ── STEP 7 : Pathologies ──
  if (step === 7) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={7} titre="Laquelle de ces pathologies ?" sous="Plusieurs choix possibles" />
      <Body>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10, marginBottom:16 }}>
          {["LLC","Diab\u00e8te","Hypertension","Maladie r\u00e9nale","Cancer","Maladie cardiaque","Autre"].map(p => (
            <div key={p} onClick={()=>togglePatho(p)} style={{ ...chipStyle(pathologies.includes(p)), padding:"13px 10px" }}>{p}</div>
          ))}
          <div onClick={()=>togglePatho("Aucune")} style={{ ...chipStyle(pathologies.includes("Aucune")), gridColumn:"1/-1", padding:"13px" }}>
            Aucune de ces pathologies
          </div>
        </div>
        {pathologies.length > 0 && (
          <button onClick={()=>setStep(8)} style={{ ...btn, background:"#c4622d", color:"white", width:"100%", fontSize:16 }}>
            Continuer \u2192
          </button>
        )}
      </Body>
    </div>
  );

  // ── STEP 8 : Traitement + R\u00e9gime ──
  if (step === 8) return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <Header stepNum={8} titre="Traitement et r\u00e9gime alimentaire" />
      <Body>
        <div style={{ marginBottom:20 }}>
          <div style={{ fontSize:16, fontWeight:800, color:"#333", marginBottom:12 }}>Suis-tu un traitement r\u00e9gulier ?</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
            {["Oui","Non"].map(opt => (
              <div key={opt} onClick={()=>setTraitement(opt)} style={{ ...optStyle(traitement===opt), padding:"14px" }}>{opt}</div>
            ))}
          </div>
        </div>
        <div style={{ marginBottom:20 }}>
          <div style={{ fontSize:16, fontWeight:800, color:"#333", marginBottom:12 }}>Ton m\u00e9decin t'a-t-il conseill\u00e9 un r\u00e9gime particulier ?</div>
          <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
            {["Oui, sans sel","Oui, sans sucre","Oui, sans gluten","Oui, autre r\u00e9gime","Non"].map(opt => (
              <div key={opt} onClick={()=>setRegimePrescrit(opt)} style={{ ...optStyle(regimePrescrit===opt), padding:"13px 16px", textAlign:"left" }}>{opt}</div>
            ))}
          </div>
        </div>
        {traitement && regimePrescrit && (
          <button onClick={()=>setStep(9)} style={{ ...btn, background:"#c4622d", color:"white", width:"100%", fontSize:16 }}>
            Continuer \u2192
          </button>
        )}
      </Body>
    </div>
  );

  // ── STEP 9 : Bilan + MNA ──
  if (step === 9) {
    const signesDenutrition = evolution==="Beaucoup plus mince" || evolution==="Un peu plus mince" || autonomie==="Non, aide ext\u00e9rieure";
    return (
      <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        <Header stepNum={9} titre="Ton profil est complet !" sous="V\u00e9rifie tes informations avant de continuer" />
        <Body>
          {/* R\u00e9cap */}
          <div style={{ background:"white", border:"2px solid #e8ddd5", borderRadius:14, padding:"18px", marginBottom:14 }}>
            <div style={{ fontSize:12, fontWeight:800, color:"#c4622d", textTransform:"uppercase", letterSpacing:1.5, marginBottom:12 }}>R\u00e9capitulatif</div>
            {[
              ["\u00c2ge", age], ["Sexe", sexe], ["Mode de vie", modeVie],
              ["Vie seul(e)", seul], ["Autonomie", autonomie],
              ["Traitement", traitement], ["R\u00e9gime prescrit", regimePrescrit],
            ].filter(([,v])=>v).map(([k,v])=>(
              <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid #f5f0ea", fontSize:14 }}>
                <span style={{ color:"#888", fontWeight:600 }}>{k}</span>
                <span style={{ fontWeight:800, color:"#333" }}>{v}</span>
              </div>
            ))}
            {pathologies.length > 0 && !pathologies.includes("Aucune") && (
              <div style={{ marginTop:10, display:"flex", flexWrap:"wrap", gap:6 }}>
                {pathologies.map(p=>(
                  <span key={p} style={{ background:"#FFF0EB", border:"1.5px solid #FA8072", borderRadius:20, padding:"3px 10px", fontSize:12, color:"#c4622d", fontWeight:700 }}>{p}</span>
                ))}
              </div>
            )}
          </div>

          {/* Alerte MNA */}
          {signesDenutrition && (
            <div style={{ background:"#FFF8E1", border:"2px solid #f57c00", borderRadius:14, padding:"14px 16px", marginBottom:14 }}>
              <div style={{ fontSize:14, fontWeight:900, color:"#e65100", marginBottom:6 }}>⚠️ Signes possibles de d\u00e9nutrition d\u00e9tect\u00e9s</div>
              <div style={{ fontSize:13, color:"#555", lineHeight:1.6, marginBottom:10 }}>
                Une perte de poids ou des difficult\u00e9s alimentaires ont \u00e9t\u00e9 rep\u00e9r\u00e9es. Un bilan MNA est recommand\u00e9 par la Haute Autorit\u00e9 de Sant\u00e9.
              </div>
              <button onClick={()=>setShowMnaPost(true)}
                style={{ ...btn, background:"#f57c00", color:"white", border:"2px solid #e65100", width:"100%", boxShadow:"2px 2px 0 #e65100", fontSize:14, padding:"12px" }}>
                Faire le bilan MNA \u2192
              </button>
            </div>
          )}

          <button onClick={handleFinish}
            style={{ ...btn, background:"#c4622d", color:"white", width:"100%", fontSize:16 }}>
            Terminer mon profil sant\u00e9 \u2192
          </button>
        </Body>
      </div>
    );
  }

  return null;
}

"""

code = code[:idx_start] + NEW + code[idx_end:]
print(f"Nouvelle taille: {len(code)}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print("SUCCES - App.jsx ecrit !")
