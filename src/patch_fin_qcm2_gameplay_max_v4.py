from pathlib import Path
import sys, shutil, time

app_path = Path(sys.argv[1] if len(sys.argv) > 1 else "App.jsx")
if not app_path.exists():
    raise SystemExit(f"❌ Fichier introuvable : {app_path}")

text = app_path.read_text(encoding="utf-8")
backup = app_path.with_name(app_path.name + ".backup_qcm2_game_max")
shutil.copyfile(app_path, backup)

component_marker = "function Qcm2GameProfileScreen("
component_code = r'''
/* ══ FIN QCM2 — PROFIL GAMEPLAY AVEC MAX ══ */
function Qcm2GameProfileScreen({ answers, playerName, playerInfos, onBack, onRestart, onChoose }) {
  const [page, setPage] = useState(0);
  const avatarSrc = playerInfos?.sexe === "Garçon" ? "/garcon.png" : "/fille.png";

  const personnes = answers?.[" Nombre de personnes"] || "2 personnes";
  const pratiques = answers?.[" Pratiques alimentaires"] || "Non, je mange de tout";
  const composition = answers?.[" Composition du repas"] || "Entrée + Plat + Dessert";
  const cuisine = answers?.["‍ En cuisine"] || answers?.[" En cuisine"] || "J'aime y passer du temps";
  const repas = answers?.[" Nombre de repas"] || "Midi et soir";

  const stats = [
    { img:"/legume2.png", label:"Fruits et légumes", pct:80, note:"Très bien !", color:"#00BFA5" },
    { img:"/feculent.png", label:"Céréales complètes", pct:60, note:"Pas mal !", color:"#FFC107" },
    { img:"/poisson.png", label:"Protéines", pct:75, note:"Bien joué !", color:"#00BFA5" },
    { img:"/lait2.png", label:"Produits laitiers", pct:40, note:"À améliorer", color:"#FF8A3D" },
    { img:"/gateau.png", label:"Sucre & produits sucrés", pct:20, note:"Attention", color:"#FF4D3D" },
    { img:"/eau.png", label:"Hydratation", pct:85, note:"Excellent !", color:"#00BFA5" },
  ];

  const Bubble = ({ children, side="left" }) => (
    <div style={{
      background:"rgba(255,255,255,0.95)", border:"3px solid #1A3A5C", borderRadius: side === "left" ? "24px 24px 24px 6px" : "24px 24px 6px 24px",
      padding:"18px 20px", color:"#10233A", fontSize:15, fontWeight:800, lineHeight:1.55,
      boxShadow:"6px 6px 0 rgba(0,0,0,0.25)", maxWidth:310
    }}>{children}</div>
  );

  const TopButtons = () => (
    <>
      <button onClick={onBack} style={{ position:"absolute", top:18, left:22, zIndex:20, background:"white", border:"3px solid #1A3A5C", borderRadius:16, padding:"10px 20px", color:"#1A3A5C", fontSize:14, fontWeight:900, cursor:"pointer", boxShadow:"3px 3px 0 rgba(0,0,0,0.22)" }}>← Retour</button>
      <div style={{ position:"absolute", top:18, right:78, zIndex:20, background:"#FA8072", borderRadius:20, padding:"10px 18px", color:"white", fontSize:13, fontWeight:900, boxShadow:"3px 3px 0 rgba(0,0,0,0.18)" }}>Mon profil</div>
    </>
  );

  if (page === 0) {
    return (
      <div style={{ position:"fixed", inset:0, overflow:"hidden", fontFamily:"Arial, sans-serif", backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", backgroundPosition:"center" }}>
        <div style={{ position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(7,45,32,0.25), rgba(255,255,255,0.10), rgba(0,50,80,0.30))" }} />
        <TopButtons />

        <div style={{ position:"absolute", top:22, left:"50%", transform:"translateX(-50%)", zIndex:10, background:"linear-gradient(180deg,#FF8B55,#FF5F3A)", border:"4px solid rgba(255,255,255,0.55)", borderRadius:28, padding:"18px 70px", textAlign:"center", boxShadow:"0 10px 0 rgba(0,0,0,0.18), 0 18px 45px rgba(255,107,53,0.35)" }}>
          <div style={{ color:"#FFF6C7", fontSize:28, fontWeight:900, textShadow:"2px 2px 0 rgba(0,0,0,0.22)" }}>⭐ PROFIL CRÉÉ !</div>
          <div style={{ color:"white", fontSize:15, fontWeight:900, marginTop:4 }}>Voici ton profil alimentaire personnalisé</div>
        </div>

        <div style={{ position:"absolute", left:18, bottom:0, width:310, height:560, zIndex:4 }}>
          <img src="/e.png" alt="Max" style={{ width:"100%", height:"100%", objectFit:"contain", objectPosition:"bottom", filter:"drop-shadow(8px 10px 0 rgba(0,0,0,0.20))" }} />
        </div>
        <div style={{ position:"absolute", left:250, top:210, zIndex:7 }}><Bubble>Wow ! Tu viens de compléter ton profil alimentaire. Regardons ensemble tes habitudes.</Bubble><div style={{ marginTop:10, background:"#00BFA5", color:"white", borderRadius:20, padding:"8px 20px", width:"fit-content", fontWeight:900 }}>Max</div></div>

        <div style={{ position:"absolute", left:35, bottom:40, display:"flex", alignItems:"center", gap:18, zIndex:8 }}>
          <div style={{ width:86, height:86, borderRadius:"50%", background:"white", border:"5px solid #7FFFD4", overflow:"hidden", boxShadow:"5px 5px 0 rgba(0,0,0,0.22)" }}>
            <img src={avatarSrc} alt="Avatar" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
          </div>
          <Bubble side="right">D'accord Max, je suis curieux de voir ! ❤</Bubble>
        </div>

        <div style={{ position:"absolute", right:70, top:140, width:640, zIndex:5, background:"linear-gradient(180deg,rgba(11,42,72,0.96),rgba(7,28,52,0.96))", border:"3px solid rgba(255,255,255,0.25)", borderRadius:24, padding:"22px", boxShadow:"0 18px 50px rgba(0,0,0,0.35)" }}>
          <h2 style={{ color:"white", textAlign:"center", margin:"0 0 18px", fontSize:21, fontWeight:900, letterSpacing:1 }}>RÉCAPITULATIF DE TES HABITUDES</h2>
          <div style={{ background:"rgba(255,255,255,0.95)", borderRadius:18, padding:"12px 18px" }}>
            {stats.map((s, i) => (
              <div key={s.label} style={{ display:"grid", gridTemplateColumns:"42px 1fr 170px 50px 105px", alignItems:"center", gap:10, padding:"10px 0", borderBottom:i===stats.length-1?"none":"1px solid #E8EDF2" }}>
                <img src={s.img} alt="" style={{ width:34, height:34, objectFit:"contain" }} />
                <div style={{ fontSize:14, fontWeight:900, color:"#10233A" }}>{s.label}</div>
                <div style={{ height:13, background:"#E5E7EB", borderRadius:20, overflow:"hidden" }}><div style={{ width:`${s.pct}%`, height:"100%", background:s.color, borderRadius:20 }} /></div>
                <div style={{ fontSize:13, fontWeight:900, color:"#10233A" }}>{s.pct}%</div>
                <div style={{ fontSize:12, fontWeight:900, color:s.color, textAlign:"right" }}>{s.note}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:16, background:"#FFF6D6", border:"2px solid #FFE08A", borderRadius:14, padding:"12px 16px", color:"#263238", fontSize:14, fontWeight:800 }}>⭐ Ton profil est unique, chaque petit pas compte pour ta santé !</div>
        </div>

        <div style={{ position:"absolute", right:70, bottom:28, zIndex:10 }}>
          <button onClick={() => { playSound("next"); setPage(1); }} style={{ background:"linear-gradient(180deg,#22D86B,#00A84F)", color:"white", border:"4px solid white", borderRadius:18, padding:"18px 58px", fontSize:18, fontWeight:900, cursor:"pointer", boxShadow:"0 0 0 4px #14B85A, 0 0 28px #A7FF83, 6px 6px 0 rgba(0,0,0,0.25)" }}>Suivant →</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, overflow:"hidden", fontFamily:"Arial, sans-serif", backgroundImage:"url('/fond_jaune.png')", backgroundSize:"cover", backgroundPosition:"center" }}>
      <div style={{ position:"absolute", inset:0, background:"linear-gradient(180deg, rgba(113,205,255,0.25), rgba(255,255,255,0.18))" }} />
      <TopButtons />

      <div style={{ position:"absolute", left:18, bottom:86, width:330, height:540, zIndex:4 }}>
        <img src="/e.png" alt="Max" style={{ width:"100%", height:"100%", objectFit:"contain", objectPosition:"bottom", filter:"drop-shadow(8px 10px 0 rgba(0,0,0,0.22))" }} />
      </div>
      <div style={{ position:"absolute", left:250, top:96, zIndex:7, transform:"rotate(-3deg)" }}><Bubble>Super travail ! 🎉 Grâce à tes réponses, je peux te proposer des recommandations et des recettes 100% adaptées à toi. Prêt(e) à découvrir tout ça ? ⭐</Bubble></div>
      <div style={{ position:"absolute", left:35, bottom:170, display:"flex", alignItems:"center", gap:18, zIndex:8 }}>
        <div style={{ width:86, height:86, borderRadius:"50%", background:"white", border:"5px solid #7FFFD4", overflow:"hidden", boxShadow:"5px 5px 0 rgba(0,0,0,0.22)" }}>
          <img src={avatarSrc} alt="Avatar" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        </div>
        <Bubble side="right">Ouiii ! J'ai hâte de voir mes recommandations personnalisées ! 😍</Bubble>
      </div>

      <div style={{ position:"absolute", right:88, top:110, width:560, zIndex:5 }}>
        <div style={{ background:"linear-gradient(180deg,#9A5B26,#6F3E18)", border:"5px solid #5B3214", borderRadius:24, padding:"18px", boxShadow:"10px 12px 0 rgba(0,0,0,0.25)" }}>
          <div style={{ color:"white", textAlign:"center", fontSize:30, fontWeight:900, textShadow:"2px 3px 0 rgba(0,0,0,0.35)", marginBottom:16 }}>AU PROGRAMME :</div>
          <div style={{ background:"#FFF5D8", borderRadius:18, padding:18, display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>
            <div onClick={() => onChoose("recos")} style={{ background:"white", border:"3px solid #F3D99B", borderRadius:18, padding:"24px 18px", textAlign:"center", cursor:"pointer", boxShadow:"0 6px 0 rgba(0,0,0,0.12)" }}>
              <img src="/panier.png" alt="" style={{ width:86, height:86, objectFit:"contain" }} />
              <div style={{ color:"#00796B", fontSize:18, fontWeight:900, marginTop:8 }}>RECOMMANDATIONS PERSONNALISÉES</div>
              <div style={{ color:"#1A3A5C", fontSize:14, fontWeight:700, marginTop:8 }}>Des conseils nutritionnels adaptés à ton profil.</div>
            </div>
            <div onClick={() => onChoose("recettes")} style={{ background:"white", border:"3px solid #F3D99B", borderRadius:18, padding:"24px 18px", textAlign:"center", cursor:"pointer", boxShadow:"0 6px 0 rgba(0,0,0,0.12)" }}>
              <img src="/salade.png" alt="" style={{ width:86, height:86, objectFit:"contain" }} />
              <div style={{ color:"#E65100", fontSize:18, fontWeight:900, marginTop:8 }}>RECETTES PERSONNALISÉES</div>
              <div style={{ color:"#1A3A5C", fontSize:14, fontWeight:700, marginTop:8 }}>Des idées de recettes équilibrées rien que pour toi.</div>
            </div>
          </div>
          <button onClick={() => onChoose("recos")} style={{ marginTop:18, width:"100%", background:"linear-gradient(180deg,#FFB02E,#FF7A00)", color:"white", border:"4px solid white", borderRadius:18, padding:"18px 20px", fontSize:19, fontWeight:900, cursor:"pointer", boxShadow:"0 0 0 4px #FFB000, 0 0 26px #FFF176, 6px 6px 0 rgba(0,0,0,0.20)" }}>Clique ici pour découvrir tes recommandations et recettes ! ↓</button>
        </div>
      </div>

      <div style={{ position:"absolute", left:90, right:90, bottom:18, height:86, background:"linear-gradient(180deg,#0E3A66,#082846)", borderRadius:24, zIndex:10, boxShadow:"0 -8px 28px rgba(0,0,0,0.25)", display:"flex", alignItems:"center", padding:"0 38px", gap:28, color:"white" }}>
        <div style={{ fontSize:40 }}>🏆</div>
        <div style={{ minWidth:190 }}><div style={{ fontSize:18, fontWeight:900 }}>Mission accomplie</div><div style={{ fontSize:13, opacity:.85, fontWeight:700 }}>Ton aventure continue...</div></div>
        {["QCM 1","QCM 2","Profil","Recommandations","Recettes"].map((lab, i) => (
          <div key={lab} style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6, flex:1 }}>
            <div style={{ width:34, height:34, borderRadius:"50%", background:i<3?"#12C96F":"#334E68", border:i===2?"4px solid #FFDF4D":"3px solid rgba(255,255,255,0.35)", display:"flex", alignItems:"center", justifyContent:"center", fontWeight:900 }}>{i<2?"✓":i===2?"★":"🔒"}</div>
            <div style={{ fontSize:11, fontWeight:900, opacity:i<3?1:.65 }}>{lab}</div>
          </div>
        ))}
        <button onClick={onRestart} style={{ background:"rgba(255,255,255,0.10)", border:"2px solid rgba(255,255,255,0.35)", color:"white", borderRadius:12, padding:"10px 12px", fontWeight:900, cursor:"pointer" }}>Recommencer</button>
      </div>
    </div>
  );
}

'''

if component_marker not in text:
    insert_at = text.find("function Qcm2Screen(")
    if insert_at == -1:
        raise SystemExit("❌ Impossible de trouver function Qcm2Screen")
    text = text[:insert_at] + component_code + text[insert_at:]

start = text.find('  if (done) {\n    const cuisineVal = answers["')
if start == -1:
    raise SystemExit("❌ Bloc de fin QCM2 introuvable")
end_marker = '\n\n  return (\n    <div style={{ position:"fixed", inset:0, backgroundImage:"url(\'/fond_blanc.jpg\')"'
end = text.find(end_marker, start)
if end == -1:
    raise SystemExit("❌ Fin du bloc QCM2 introuvable")

new_done_block = '''  if (done) {
    return (
      <Qcm2GameProfileScreen
        answers={answers}
        playerName={playerName}
        playerInfos={playerInfos}
        onBack={onBack}
        onRestart={() => { setStep(1); setDone(false); setPersons(2); setVslider(0); setCompo(null); setCuisine(null); setRepas(null); setAnswers({}); }}
        onChoose={(mode) => { if(onDone) onDone(answers[" Composition du repas"], mode, answers); }}
      />
    );
  }
'''
text = text[:start] + new_done_block + text[end:]

app_path.write_text(text, encoding="utf-8")
print("✅ Page fin QCM2 remplacée par une scène gameplay avec Max + avatar")
print(f"💾 Sauvegarde créée : {backup.name}")
print("➡️ Lance : cd .. puis npm run dev")
