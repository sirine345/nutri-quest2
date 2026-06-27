from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'App.jsx')
if not path.exists():
    print('❌ Fichier introuvable :', path)
    sys.exit(1)

text = path.read_text(encoding='utf-8')
backup = path.with_name(path.name + '.backup_avant_qcm2_gameplay_v6')
backup.write_text(text, encoding='utf-8')

START_MARK = '/* ══ FIN QCM2 — PROFIL GAMEPLAY AVEC MAX ══ */'
END_MARK = '/* ══ FIN QCM2 — FIN PROFIL GAMEPLAY AVEC MAX ══ */'

# Supprime une ancienne insertion incomplete si elle existe
while START_MARK in text and END_MARK in text:
    a = text.index(START_MARK)
    b = text.index(END_MARK, a) + len(END_MARK)
    text = text[:a] + text[b:]

component = r'''
/* ══ FIN QCM2 — PROFIL GAMEPLAY AVEC MAX ══ */
function Qcm2GameProfileScreen({ answers = {}, playerName, playerInfos, onBack, onRestart, onChoose }) {
  const [page, setPage] = useState(0);
  const avatarSrc = playerInfos?.sexe === "Garçon" ? "/garcon.png" : "/fille.png";

  const personnes = answers[" Nombre de personnes"] || "2 personnes";
  const pratiques = answers[" Pratiques alimentaires"] || "Non, je mange de tout";
  const composition = answers[" Composition du repas"] || "Entrée + Plat + Dessert";
  const cuisine = answers["‍ En cuisine"] || answers[" En cuisine"] || "J'aime y passer du temps";
  const repas = answers[" Nombre de repas"] || "Midi et soir";

  const habits = [
    { icon:"/fruit.png", name:"Organisation des repas", value:80, note:"Tres bien !", color:"#00BFA5" },
    { icon:"/assiette1.png", name:"Composition", value:70, note:"Bien joue !", color:"#FFC400" },
    { icon:"/marmitte.png", name:"Cuisine maison", value:cuisine.includes("temps") ? 85 : 55, note:cuisine.includes("temps") ? "Excellent !" : "A renforcer", color:"#00BFA5" },
    { icon:"/eau.png", name:"Equilibre semaine", value:65, note:"Pas mal !", color:"#FF8A3D" },
    { icon:"/legume2.png", name:"Adaptation profil", value:75, note:"Personnalise", color:"#00BFA5" },
  ];

  const smallButton = {
    background:"rgba(255,255,255,0.96)", border:"3px solid #10233A", borderRadius:16,
    padding:"12px 18px", color:"#10233A", fontWeight:900, cursor:"pointer",
    boxShadow:"4px 4px 0 rgba(0,0,0,0.25)"
  };

  const dialogue = page === 0
    ? "Wow ! Tu viens de completer ton profil alimentaire. Regardons ensemble tes habitudes."
    : "Super travail ! Grace a tes reponses, je peux te proposer des recommandations et des recettes adaptees a toi.";

  return (
    <div style={{ position:"fixed", inset:0, overflow:"hidden", fontFamily:"Arial, sans-serif", backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", backgroundPosition:"center" }}>
      <div style={{ position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(4,36,24,0.25), rgba(8,57,83,0.20))" }} />

      <button onClick={onBack} style={{ ...smallButton, position:"absolute", top:18, left:22, zIndex:20 }}>← Retour</button>
      <div style={{ position:"absolute", top:22, right:88, zIndex:20, background:"#FF7D6E", color:"white", borderRadius:999, padding:"12px 20px", fontWeight:900, boxShadow:"0 8px 20px rgba(0,0,0,0.25)" }}>Mon profil</div>

      <div style={{ position:"absolute", top:18, left:"50%", transform:"translateX(-50%)", zIndex:5, background:"linear-gradient(180deg,#FF8A5B,#FF674D)", color:"white", borderRadius:28, padding:"18px 70px", border:"4px solid rgba(255,255,255,0.25)", boxShadow:"0 10px 35px rgba(0,0,0,0.28)", textAlign:"center" }}>
        <div style={{ fontSize:34, fontWeight:1000, textShadow:"3px 3px 0 rgba(0,0,0,0.25)" }}>★ PROFIL CREE !</div>
        <div style={{ fontSize:15, fontWeight:900, marginTop:4 }}>Voici ton profil alimentaire personnalise</div>
      </div>

      <img src="/e.png" alt="Max" style={{ position:"absolute", left:30, bottom:0, height:"76vh", zIndex:4, filter:"drop-shadow(8px 12px 0 rgba(0,0,0,0.25))" }} />
      <div style={{ position:"absolute", left:245, top:210, zIndex:8, width:230, background:"#FFFDF7", border:"3px solid rgba(0,0,0,0.18)", borderRadius:"28px 28px 28px 6px", padding:"22px", color:"#10233A", fontWeight:800, lineHeight:1.55, boxShadow:"0 8px 25px rgba(0,0,0,0.22)" }}>
        {dialogue}
        <div style={{ position:"absolute", bottom:-38, left:28, background:"#00BFA5", color:"white", borderRadius:999, padding:"8px 22px", fontWeight:1000 }}>Max</div>
      </div>

      <div style={{ position:"absolute", left:42, bottom:56, display:"flex", alignItems:"center", gap:14, zIndex:8 }}>
        <div style={{ width:88, height:88, borderRadius:"50%", border:"6px solid white", background:"#E0F7F5", overflow:"hidden", boxShadow:"0 8px 22px rgba(0,0,0,0.25)" }}>
          <img src={avatarSrc} alt="Avatar" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        </div>
        <div style={{ width:240, background:"#FFFDF7", border:"3px solid rgba(0,0,0,0.16)", borderRadius:"22px 22px 22px 6px", padding:"16px 18px", color:"#10233A", fontWeight:850, lineHeight:1.4, boxShadow:"0 8px 22px rgba(0,0,0,0.20)" }}>
          {page === 0 ? "D'accord Max, je suis curieux de voir !" : "Ouiii ! J'ai hate de voir mes conseils personnalises !"}
          <span style={{ float:"right", color:"#FF674D", fontSize:20 }}>♥</span>
        </div>
      </div>

      {page === 0 ? (
        <div style={{ position:"absolute", right:70, top:145, width:"56vw", maxWidth:760, zIndex:6, background:"rgba(11,35,58,0.92)", border:"3px solid rgba(255,255,255,0.22)", borderRadius:24, padding:"24px 28px 28px", boxShadow:"0 18px 50px rgba(0,0,0,0.35)" }}>
          <h2 style={{ margin:"0 0 20px", color:"white", textAlign:"center", fontSize:22, fontWeight:1000, textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>RECAPITULATIF DE TES HABITUDES</h2>
          <div style={{ background:"rgba(255,255,255,0.96)", borderRadius:18, overflow:"hidden", padding:"10px 14px" }}>
            {habits.map((h, i) => (
              <div key={h.name} style={{ display:"grid", gridTemplateColumns:"52px 1.4fr 1.2fr 55px 100px", alignItems:"center", gap:12, padding:"12px 8px", borderBottom:i===habits.length-1?"none":"1px solid #E8EDF2" }}>
                <img src={h.icon} alt="" style={{ width:38, height:38, objectFit:"contain" }} />
                <div style={{ fontWeight:1000, color:"#10233A" }}>{h.name}</div>
                <div style={{ height:14, background:"#E8EDF2", borderRadius:999, overflow:"hidden" }}><div style={{ width:h.value+"%", height:"100%", background:h.color, borderRadius:999 }} /></div>
                <div style={{ fontWeight:1000, color:"#10233A" }}>{h.value}%</div>
                <div style={{ fontWeight:1000, color:h.color, fontSize:13 }}>{h.note}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:16, background:"#FFF6D9", borderRadius:14, padding:"12px 18px", color:"#10233A", fontWeight:800 }}>★ Ton profil est unique : chaque petit pas compte pour ta sante !</div>
          <button onClick={() => { playSound("good"); setPage(1); }} style={{ position:"absolute", right:-32, bottom:-34, background:"linear-gradient(180deg,#22C55E,#00A86B)", color:"white", border:"4px solid white", borderRadius:20, padding:"20px 58px", fontSize:18, fontWeight:1000, cursor:"pointer", boxShadow:"0 0 0 4px rgba(34,197,94,0.35), 0 12px 28px rgba(0,0,0,0.35)" }}>Suivant →</button>
        </div>
      ) : (
        <div style={{ position:"absolute", right:62, top:150, width:"56vw", maxWidth:770, zIndex:6 }}>
          <div style={{ background:"linear-gradient(180deg,#B97934,#8B4F22)", border:"5px solid #5B3216", borderRadius:24, padding:"20px 26px 28px", boxShadow:"0 16px 45px rgba(0,0,0,0.35)" }}>
            <h2 style={{ margin:"0 0 18px", textAlign:"center", color:"white", fontSize:30, fontWeight:1000, textShadow:"3px 3px 0 rgba(0,0,0,0.35)" }}>AU PROGRAMME :</h2>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:18 }}>
              <div onClick={() => onChoose && onChoose("recos")} style={{ background:"#FFF9E9", border:"3px solid rgba(255,255,255,0.8)", borderRadius:20, padding:"22px", textAlign:"center", cursor:"pointer", boxShadow:"inset 0 0 0 2px rgba(0,0,0,0.05)" }}>
                <img src="/panier.png" alt="" style={{ height:90, objectFit:"contain" }} />
                <div style={{ color:"#008B7A", fontWeight:1000, fontSize:20, marginTop:8 }}>RECOMMANDATIONS PERSONNALISEES</div>
                <p style={{ color:"#10233A", fontWeight:700, marginBottom:0 }}>Des conseils nutritionnels adaptes a ton profil.</p>
              </div>
              <div onClick={() => onChoose && onChoose("recettes")} style={{ background:"#FFF9E9", border:"3px solid rgba(255,255,255,0.8)", borderRadius:20, padding:"22px", textAlign:"center", cursor:"pointer", boxShadow:"inset 0 0 0 2px rgba(0,0,0,0.05)" }}>
                <img src="/salade.png" alt="" style={{ height:90, objectFit:"contain" }} />
                <div style={{ color:"#E65100", fontWeight:1000, fontSize:20, marginTop:8 }}>RECETTES PERSONNALISEES</div>
                <p style={{ color:"#10233A", fontWeight:700, marginBottom:0 }}>Des idees de recettes equilibrees rien que pour toi.</p>
              </div>
            </div>
            <button onClick={() => onChoose && onChoose("recos")} style={{ marginTop:22, width:"100%", background:"linear-gradient(180deg,#FFB000,#FF7A00)", color:"white", border:"4px solid #FFF2B8", borderRadius:22, padding:"20px", fontSize:21, fontWeight:1000, cursor:"pointer", boxShadow:"0 0 22px rgba(255,176,0,0.65), 0 10px 28px rgba(0,0,0,0.35)", textShadow:"2px 2px 0 rgba(0,0,0,0.22)" }}>Clique ici pour decouvrir tes recommandations ! ↓</button>
          </div>
        </div>
      )}

      <div style={{ position:"absolute", left:80, right:80, bottom:12, zIndex:12, background:"rgba(8,35,65,0.96)", color:"white", borderRadius:24, padding:"16px 28px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 -8px 30px rgba(0,0,0,0.25)" }}>
        <div style={{ display:"flex", alignItems:"center", gap:16 }}><div style={{ fontSize:46 }}>🏆</div><div><div style={{ fontSize:18, fontWeight:1000 }}>Mission accomplie</div><div style={{ opacity:0.85, fontWeight:700 }}>Ton aventure continue...</div></div></div>
        <div style={{ display:"flex", alignItems:"center", gap:12, fontWeight:900 }}>
          {["QCM 1","QCM 2","Profil","Recommandations","Recettes"].map((label,i)=>(
            <div key={label} style={{ textAlign:"center", opacity:i>2?0.55:1 }}><div style={{ margin:"0 auto 6px", width:34, height:34, borderRadius:"50%", display:"flex", alignItems:"center", justifyContent:"center", background:i<2?"#22C55E":i===2?"#3157FF":"#5D7189", border:i===2?"4px solid #FFE66D":"none" }}>{i<2?"✓":i===2?"★":"🔒"}</div><div style={{ fontSize:12 }}>{label}</div></div>
          ))}
        </div>
        <button onClick={onRestart} style={{ background:"rgba(255,255,255,0.10)", color:"white", border:"2px solid rgba(255,255,255,0.35)", borderRadius:14, padding:"10px 14px", fontWeight:900, cursor:"pointer" }}>Recommencer</button>
      </div>
    </div>
  );
}
/* ══ FIN QCM2 — FIN PROFIL GAMEPLAY AVEC MAX ══ */
'''

# Insere le composant juste avant Qcm2Screen
anchor = 'function Qcm2Screen'
idx = text.find(anchor)
if idx == -1:
    print('❌ function Qcm2Screen introuvable')
    sys.exit(1)
text = text[:idx] + component + '\n\n' + text[idx:]

# Retrouve Qcm2Screen apres insertion
qstart = text.find(anchor, idx + len(component))
if qstart == -1:
    print('❌ Qcm2Screen introuvable apres insertion')
    sys.exit(1)

# Trouve le if(done) de rendu, celui qui contient return (
search_pos = qstart
while True:
    if_pos = text.find('if (done)', search_pos)
    if if_pos == -1:
        print('❌ Bloc if (done) introuvable dans Qcm2Screen')
        sys.exit(1)
    next_part = text[if_pos:if_pos+120]
    if 'return' in next_part:
        break
    search_pos = if_pos + 1

brace = text.find('{', if_pos)
if brace == -1:
    print('❌ Accolade du if(done) introuvable')
    sys.exit(1)

def find_matching_brace(s, open_idx):
    depth = 0
    in_str = None
    esc = False
    in_line = False
    in_block = False
    for i in range(open_idx, len(s)):
        c = s[i]
        n = s[i+1] if i+1 < len(s) else ''
        if in_line:
            if c == '\n': in_line = False
            continue
        if in_block:
            if c == '*' and n == '/': in_block = False
            continue
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_str:
                in_str = None
            continue
        if c == '/' and n == '/':
            in_line = True; continue
        if c == '/' and n == '*':
            in_block = True; continue
        if c in ('"', "'", '`'):
            in_str = c; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1

end = find_matching_brace(text, brace)
if end == -1:
    print('❌ Fin du bloc if(done) introuvable')
    sys.exit(1)

replacement = '''if (done) {
    return (
      <Qcm2GameProfileScreen
        answers={answers}
        playerName={playerName}
        playerInfos={playerInfos}
        onBack={onBack}
        onRestart={() => { setStep(1); setDone(false); setPersons(2); setVslider(0); setCompo(null); setCuisine(null); setRepas(null); setAnswers({}); }}
        onChoose={(mode) => { if (onDone) onDone(answers[" Composition du repas"], mode, answers); }}
      />
    );
  }'''
text = text[:if_pos] + replacement + text[end+1:]

path.write_text(text, encoding='utf-8')
print('✅ Composant gameplay Max ajoute')
print('✅ Page de fin QCM2 remplacee')
print('💾 Sauvegarde creee :', backup.name)
print('➡️ Lance : cd .. puis npm run dev')
