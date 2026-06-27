from pathlib import Path
import re, sys

APP = Path('src/App.jsx')
if not APP.exists():
    APP = Path('App.jsx')
if not APP.exists():
    raise SystemExit("ERREUR: mets ce fichier patch à la racine de ton projet, puis lance: python patch_fin_qcm2_game.py")

text = APP.read_text(encoding='utf-8')
backup = APP.with_suffix(APP.suffix + '.backup_fin_qcm2_game')
backup.write_text(text, encoding='utf-8')

NEW_COMPONENT = r'''

/* ══ FIN QCM2 — PROFIL GAMEPLAY AVEC MAX ══ */
function Qcm2GameProfileScreen({ answers, playerName, avatarSrc, onBack, onReset, onNext }) {
  const [step, setStep] = useState(0);
  const rows = [
    ["Nombre de personnes", answers[" Nombre de personnes"] || "Non précisé", "👥"],
    ["Pratiques alimentaires", answers[" Pratiques alimentaires"] || "Non précisé", "🥗"],
    ["Composition du repas", answers[" Composition du repas"] || "Non précisé", "🍽️"],
    ["En cuisine", answers["‍ En cuisine"] || answers[" En cuisine"] || "Non précisé", "👩‍🍳"],
    ["Nombre de repas", answers[" Nombre de repas"] || "Non précisé", "🗓️"],
  ];
  const cuisine = answers["‍ En cuisine"] || answers[" En cuisine"] || "";
  const pratiques = answers[" Pratiques alimentaires"] || "";
  const compo = answers[" Composition du repas"] || "";
  const maxText = step === 0
    ? `Bravo ${playerName || "aventurier"} ! Ton profil alimentaire est créé. Regarde : chaque réponse va m'aider à construire des conseils vraiment adaptés à toi.`
    : `Super ! Maintenant je peux débloquer tes recommandations et tes recettes personnalisées. Clique sur Suivant pour ouvrir ton tableau de mission.`;

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden", backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", backgroundPosition:"center" }}>
      <div style={{ position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(7,42,35,0.72), rgba(9,64,74,0.55))" }} />
      <button onClick={onBack} style={{ position:"absolute", top:22, left:24, zIndex:5, background:"white", border:"3px solid #222", borderRadius:14, padding:"10px 20px", fontSize:15, fontWeight:900, color:"#1A3A5C", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>← Retour</button>
      <div style={{ position:"absolute", top:22, right:24, zIndex:5, display:"flex", alignItems:"center", gap:10 }}>
        <div style={{ background:"#FA8072", color:"white", border:"3px solid white", borderRadius:22, padding:"8px 16px", fontSize:13, fontWeight:900, boxShadow:"3px 3px 0 #222" }}>Mon profil</div>
      </div>

      <div style={{ position:"relative", zIndex:2, height:"100%", display:"grid", gridTemplateColumns:"360px 1fr", gap:22, padding:"78px 34px 28px", boxSizing:"border-box" }}>
        <div style={{ position:"relative", minHeight:0 }}>
          <img src="/e.png" alt="Max" style={{ position:"absolute", bottom:0, left:0, width:330, maxHeight:"74vh", objectFit:"contain", filter:"drop-shadow(8px 10px 0 rgba(0,0,0,0.35))", animation:"maxIn 0.55s ease both" }} />
          <div style={{ position:"absolute", top:72, left:188, width:230, background:"#FFFDF4", border:"3px solid #222", borderRadius:"24px 24px 24px 6px", padding:"18px 20px", boxShadow:"6px 6px 0 rgba(0,0,0,0.25)", lineHeight:1.55, fontSize:15, fontWeight:800, color:"#102033" }}>
            {maxText}
            <div style={{ marginTop:12, display:"inline-block", background:"#00BFA5", color:"white", borderRadius:20, padding:"5px 14px", fontSize:12, fontWeight:900 }}>Max</div>
          </div>
          <div style={{ position:"absolute", bottom:28, left:265, display:"flex", alignItems:"flex-end", gap:12 }}>
            <img src={avatarSrc || "/fille.png"} alt="Avatar" style={{ width:82, height:82, borderRadius:"50%", objectFit:"cover", background:"white", border:"4px solid #7FFFD4", boxShadow:"4px 4px 0 #222" }} />
            <div style={{ width:210, background:"white", border:"3px solid #222", borderRadius:"22px 22px 22px 6px", padding:"14px 16px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", fontSize:14, fontWeight:800, color:"#1A3A5C", lineHeight:1.45 }}>
              {step === 0 ? "Ok Max, montre-moi mon profil !" : "Trop bien, je veux voir la suite !"} <span style={{ color:"#FA8072" }}>♥</span>
            </div>
          </div>
        </div>

        <div style={{ display:"flex", flexDirection:"column", minWidth:0 }}>
          <div style={{ alignSelf:"center", background:"linear-gradient(180deg,#FF8A50,#F4511E)", border:"4px solid rgba(255,255,255,0.8)", borderRadius:28, padding:"14px 48px", color:"white", textAlign:"center", boxShadow:"0 10px 0 rgba(0,0,0,0.18)", marginBottom:16 }}>
            <div style={{ fontSize:34, fontWeight:1000, textTransform:"uppercase", textShadow:"2px 2px 0 #9b2d0d" }}>⭐ Profil créé !</div>
            <div style={{ fontSize:15, fontWeight:800, opacity:0.95 }}>Voici ton profil alimentaire personnalisé</div>
          </div>

          <div style={{ flex:1, background:"rgba(7,26,48,0.90)", border:"4px solid rgba(255,255,255,0.22)", borderRadius:28, padding:22, boxShadow:"0 18px 50px rgba(0,0,0,0.35)", minHeight:0, overflow:"auto" }}>
            <div style={{ color:"white", fontSize:20, fontWeight:1000, textAlign:"center", marginBottom:16, textTransform:"uppercase", letterSpacing:1 }}>Récapitulatif de tes habitudes</div>
            <div style={{ background:"#FFFDF7", borderRadius:20, overflow:"hidden", border:"3px solid #222" }}>
              {rows.map((r, i) => (
                <div key={r[0]} style={{ display:"grid", gridTemplateColumns:"46px 1fr auto", alignItems:"center", gap:12, padding:"13px 16px", borderBottom:i<rows.length-1?"2px solid #EEE":"none" }}>
                  <div style={{ width:36, height:36, borderRadius:12, background:i%2?"#FFF0EB":"#E0F7F5", display:"flex", alignItems:"center", justifyContent:"center", fontSize:20 }}>{r[2]}</div>
                  <div style={{ fontSize:14, color:"#6B7280", fontWeight:900 }}>{r[0]}</div>
                  <div style={{ fontSize:14, color:"#111827", fontWeight:1000, textAlign:"right", maxWidth:360 }}>{String(r[1])}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop:16, display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:12 }}>
              <div style={{ background:"#E0F7F5", border:"3px solid #00BFA5", borderRadius:18, padding:14, color:"#00695C", fontWeight:900, textAlign:"center" }}>🎯 Mission<br/><span style={{ fontSize:12 }}>profil validé</span></div>
              <div style={{ background:"#FFF8E1", border:"3px solid #FFC107", borderRadius:18, padding:14, color:"#8A5A00", fontWeight:900, textAlign:"center" }}>🍽️ Repas<br/><span style={{ fontSize:12 }}>{compo || "personnalisé"}</span></div>
              <div style={{ background:"#FFF0EB", border:"3px solid #FF6B35", borderRadius:18, padding:14, color:"#B43B15", fontWeight:900, textAlign:"center" }}>⚡ Cuisine<br/><span style={{ fontSize:12 }}>{cuisine || pratiques || "adaptée"}</span></div>
            </div>
          </div>

          <div style={{ display:"flex", gap:12, marginTop:16 }}>
            <button onClick={onReset} style={{ flex:1, background:"white", border:"3px solid #222", borderRadius:16, padding:"14px", fontSize:14, fontWeight:900, cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>Recommencer</button>
            <button onClick={() => step === 0 ? setStep(1) : onNext()} style={{ flex:2, background:"linear-gradient(180deg,#19D66B,#00A84F)", color:"white", border:"3px solid white", borderRadius:18, padding:"16px", fontSize:17, fontWeight:1000, cursor:"pointer", boxShadow:"0 0 22px rgba(0,255,120,0.55), 5px 5px 0 #222" }}>{step === 0 ? "Suivant →" : "Ouvrir mes recommandations →"}</button>
          </div>
        </div>
      </div>
    </div>
  );
}
'''

NEW_RECO = r'''
function RecommandationsQcm2Screen({ answers, onBack, onVoirRecettes }) {
  const cuisine = answers["‍ En cuisine"] || answers[" En cuisine"] || "";
  const pratiques = answers[" Pratiques alimentaires"] || "";
  const nbRepas = answers[" Nombre de repas"] || "";
  const showPetitDej = nbRepas === "Midi uniquement" || nbRepas === "Soir uniquement";
  const profilPrincipal = pratiques === "Je mange sans viande" ? "vegetarien" : pratiques === "Je mange sans porc" ? "sans_porc" : cuisine === "Je n'ai pas le temps" ? "rapide" : "mediterraneen";

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden", backgroundImage:"url('/fond_jaune.png')", backgroundSize:"cover", backgroundPosition:"center" }}>
      <div style={{ position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(15,72,100,0.25), rgba(5,90,65,0.25))" }} />
      <button onClick={onBack} style={{ position:"absolute", top:22, left:24, zIndex:5, background:"white", border:"3px solid #222", borderRadius:14, padding:"10px 20px", fontSize:15, fontWeight:900, color:"#1A3A5C", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>← Retour</button>
      <div style={{ position:"relative", zIndex:2, height:"100%", display:"grid", gridTemplateColumns:"360px 1fr", gap:28, padding:"74px 40px 34px", boxSizing:"border-box" }}>
        <div style={{ position:"relative" }}>
          <img src="/e.png" alt="Max" style={{ position:"absolute", bottom:30, left:0, width:340, maxHeight:"78vh", objectFit:"contain", filter:"drop-shadow(8px 10px 0 rgba(0,0,0,0.30))", animation:"maxIn 0.55s ease both" }} />
          <div style={{ position:"absolute", top:48, left:190, width:285, background:"#FFFDF4", border:"3px solid #222", borderRadius:"26px 26px 26px 8px", padding:"22px", boxShadow:"6px 6px 0 rgba(0,0,0,0.25)", color:"#102033", fontSize:16, fontWeight:900, lineHeight:1.55 }}>
            Super travail ! 🎉<br/><br/>Grâce à tes réponses, j'ai préparé deux coffres : tes recommandations personnalisées et tes recettes adaptées. Clique sur une carte pour les découvrir.
            <div style={{ marginTop:12, display:"inline-block", background:"#00BFA5", color:"white", borderRadius:20, padding:"5px 14px", fontSize:12, fontWeight:1000 }}>Max</div>
          </div>
        </div>

        <div style={{ display:"flex", flexDirection:"column", justifyContent:"center", gap:18 }}>
          <div style={{ alignSelf:"center", background:"linear-gradient(180deg,#B87836,#6B3F18)", border:"4px solid #F7D28A", borderRadius:18, padding:"14px 50px", color:"white", boxShadow:"0 8px 0 rgba(0,0,0,0.25)", fontSize:34, fontWeight:1000, textTransform:"uppercase", textShadow:"2px 2px 0 #3b210c" }}>Au programme :</div>
          <div style={{ background:"rgba(117,70,25,0.92)", border:"5px solid #8B4A18", borderRadius:28, padding:26, boxShadow:"0 20px 50px rgba(0,0,0,0.35)" }}>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:22 }}>
              <div onClick={() => onVoirRecettes(profilPrincipal)} style={{ background:"#FFFDF4", border:"4px solid #F7D28A", borderRadius:24, padding:24, minHeight:210, cursor:"pointer", textAlign:"center", boxShadow:"inset 0 0 0 2px rgba(255,255,255,0.7), 6px 6px 0 rgba(0,0,0,0.20)", transition:"transform 0.2s" }} onMouseEnter={e=>e.currentTarget.style.transform="translateY(-6px)"} onMouseLeave={e=>e.currentTarget.style.transform="translateY(0)"}>
                <div style={{ fontSize:60, marginBottom:10 }}>📋</div>
                <div style={{ color:"#00897B", fontSize:22, fontWeight:1000, lineHeight:1.15 }}>RECOMMANDATIONS<br/>PERSONNALISÉES</div>
                <p style={{ color:"#1A3A5C", fontSize:14, fontWeight:800, lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil.</p>
              </div>
              <div onClick={() => onVoirRecettes(profilPrincipal)} style={{ background:"#FFFDF4", border:"4px solid #F7D28A", borderRadius:24, padding:24, minHeight:210, cursor:"pointer", textAlign:"center", boxShadow:"inset 0 0 0 2px rgba(255,255,255,0.7), 6px 6px 0 rgba(0,0,0,0.20)", transition:"transform 0.2s" }} onMouseEnter={e=>e.currentTarget.style.transform="translateY(-6px)"} onMouseLeave={e=>e.currentTarget.style.transform="translateY(0)"}>
                <div style={{ fontSize:60, marginBottom:10 }}>🥗</div>
                <div style={{ color:"#E65100", fontSize:22, fontWeight:1000, lineHeight:1.15 }}>RECETTES<br/>PERSONNALISÉES</div>
                <p style={{ color:"#1A3A5C", fontSize:14, fontWeight:800, lineHeight:1.5 }}>Des idées de repas équilibrés rien que pour toi.</p>
              </div>
            </div>
            {showPetitDej && <div style={{ marginTop:18, background:"#FFF8E1", border:"3px solid #FFC107", borderRadius:18, padding:14, textAlign:"center", color:"#8A5A00", fontWeight:900 }}>⭐ Bonus débloqué : idées petit déjeuner, car tu as indiqué ne prendre qu'un repas principal.</div>}
            <button onClick={() => onVoirRecettes(profilPrincipal)} style={{ marginTop:22, width:"100%", background:"linear-gradient(180deg,#FFB629,#FF6B00)", color:"white", border:"4px solid #FFF2B0", borderRadius:22, padding:"18px", fontSize:19, fontWeight:1000, cursor:"pointer", boxShadow:"0 0 24px rgba(255,170,0,0.8), 5px 5px 0 #222" }}>Clique ici pour découvrir tes recommandations et recettes ! 👆</button>
          </div>
          <div style={{ alignSelf:"center", background:"rgba(7,26,48,0.92)", borderRadius:24, padding:"16px 34px", color:"white", fontWeight:900, boxShadow:"0 8px 30px rgba(0,0,0,0.25)" }}>🏆 Mission accomplie · QCM 1 ✓ · QCM 2 ✓ · Profil ⭐ · Recommandations 🔒 · Recettes 🔒</div>
        </div>
      </div>
    </div>
  );
}
'''

# insert component before QCM 2 marker
if 'function Qcm2GameProfileScreen' not in text:
    marker = '/* ══ QCM 2 ══ */'
    if marker not in text:
        raise SystemExit('ERREUR: impossible de trouver le marqueur QCM 2.')
    text = text.replace(marker, NEW_COMPONENT + '\n' + marker, 1)

# Replace if(done) block with gameplay component
needle = '  if (done) {'
start = text.find(needle)
if start == -1:
    raise SystemExit('ERREUR: impossible de trouver le bloc if(done).')
# find matching brace for if block
brace_start = text.find('{', start)
depth = 0
end = None
for i in range(brace_start, len(text)):
    if text[i] == '{':
        depth += 1
    elif text[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
if end is None:
    raise SystemExit('ERREUR: bloc if(done) non fermé.')
new_done = '''  if (done) {
    return (
      <Qcm2GameProfileScreen
        answers={answers}
        playerName={playerName}
        avatarSrc={playerInfos?.avatarSrc}
        onBack={onBack}
        onReset={() => { setStep(1); setDone(false); setPersons(2); setVslider(0); setCompo(null); setCuisine(null); setRepas(null); setAnswers({}); }}
        onNext={() => { if(onDone) onDone(answers[" Composition du repas"], "recos", answers); }}
      />
    );
  }'''
text = text[:start] + new_done + text[end:]

# prevent instant navigation inside useEffect: remove parent onDone calls in effect only
text = text.replace('''      const cuisineVal = answers["‍ En cuisine"];
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, cuisineVal, answers);''', '''      // La navigation se fait maintenant depuis l'écran gameplay de profil.''')

# Replace RecommandationsQcm2Screen function with gameplay hub using brace matching
m = re.search(r'function RecommandationsQcm2Screen\s*\(', text)
if not m:
    raise SystemExit('ERREUR: impossible de trouver RecommandationsQcm2Screen.')
start2 = m.start()
brace2 = text.find('{', start2)
depth = 0
end2 = None
for i in range(brace2, len(text)):
    if text[i] == '{':
        depth += 1
    elif text[i] == '}':
        depth -= 1
        if depth == 0:
            end2 = i + 1
            break
if end2 is None:
    raise SystemExit('ERREUR: fonction RecommandationsQcm2Screen non fermée.')
text = text[:start2] + NEW_RECO.strip() + text[end2:]

# Pass avatarSrc from App to Qcm2Screen via playerInfos extension
old = '<Qcm2Screen playerName={playerName} playerInfos={playerInfos}'
new = '<Qcm2Screen playerName={playerName} playerInfos={{...(playerInfos||{}), avatarSrc: avatarChoice === "fille" ? "/fille.png" : "/garcon.png"}}'
text = text.replace(old, new, 1)

APP.write_text(text, encoding='utf-8')
print('✅ Patch terminé !')
print(f'💾 Sauvegarde créée : {backup}')
print('➡️ Lance maintenant : npm run dev')
