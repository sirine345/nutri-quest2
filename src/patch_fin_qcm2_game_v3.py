# -*- coding: utf-8 -*-
from pathlib import Path
import sys

TARGET = Path(sys.argv[1] if len(sys.argv) > 1 else "App.jsx")
if not TARGET.exists():
    raise SystemExit(f"❌ Fichier introuvable : {TARGET}")

text = TARGET.read_text(encoding="utf-8")
backup = TARGET.with_name(TARGET.name + ".backup_fin_qcm2_game_v3")
if not backup.exists():
    backup.write_text(text, encoding="utf-8")

start = text.find("function RecommandationsQcm2Screen")
if start == -1:
    raise SystemExit("❌ Je ne trouve pas function RecommandationsQcm2Screen dans App.jsx")

end_marker = "/* ══ COMPOSANT INGRÉDIENTS"
end = text.find(end_marker, start)
if end == -1:
    raise SystemExit("❌ Je ne trouve pas le marqueur après RecommandationsQcm2Screen")

new_component = r'''function RecommandationsQcm2Screen({ answers = {}, playerName = "Joueur", avatarSrc = "/avatar.png", avatarGender = "fille", onBack, onVoirRecettes }) {
  const [step, setStep] = useState(0);
  const cuisine = answers[" En cuisine"] || answers["En cuisine"] || "Je veux des idées simples";
  const pratiques = answers[" Pratiques alimentaires"] || answers["Pratiques alimentaires"] || "Aucune restriction";
  const nbRepas = answers[" Nombre de repas"] || answers["Nombre de repas"] || "Rythme variable";

  const profilRecos = [];
  if (pratiques === "Je mange sans viande") profilRecos.push({ key:"vegetarien", label:"Vegetarien", couleur:"#558B2F", bg:"#F1F8E9", texte:"Recettes equilibrees sans viande ni poisson, riches en proteines vegetales.", conseils:["Mise sur les lentilles, pois chiches et haricots", "Ajoute des oeufs ou laitages si tu en consommes", "Varie les cereales : riz, quinoa, boulgour"], profil:"vegetarien", img:"/legumesec.png" });
  if (cuisine === "Je n'ai pas le temps") profilRecos.push({ key:"rapide", label:"Mission rapide", couleur:"#E65100", bg:"#FBE9E7", texte:"Des recettes equilibrees en moins de 30 minutes.", conseils:["Garde des conserves utiles : thon, pois chiches, lentilles", "Prepare une base pour deux repas", "Choisis des recettes simples mais completes"], profil:"rapide", img:"/sardine.png" });
  if (pratiques === "Je mange sans porc") profilRecos.push({ key:"sans_porc", label:"Sans porc", couleur:"#0277BD", bg:"#E1F5FE", texte:"Des idees adaptees sans porc ni charcuterie.", conseils:["Remplace par volaille, poisson, oeufs ou legumes secs", "Evite les charcuteries cachees dans certains plats", "Lis rapidement la liste des ingredients"], profil:"sans_porc", img:"/poisson.png" });
  if (profilRecos.length === 0) profilRecos.push({ key:"pnns", label:"Profil equilibre", couleur:"#00A88F", bg:"#E0F7F5", texte:"Ton profil peut progresser avec des repas plus reguliers et plus complets.", conseils:["Ajoute des legumes dans un maximum de repas", "Garde l'eau comme boisson principale", "Associe feculent complet + proteine + legumes"], profil:"mediterraneen", img:"/assiette1.png" });

  const showPetitDej = nbRepas === "Midi uniquement" || nbRepas === "Soir uniquement";
  const missionScore = Math.min(100, 55 + profilRecos.length * 12 + (showPetitDej ? 5 : 15));
  const mainReco = profilRecos[0];
  const avatar = avatarSrc || (avatarGender === "garcon" ? "/garcon.png" : "/fille.png");

  const card = { background:"rgba(255,255,255,0.92)", border:"3px solid #222", borderRadius:24, boxShadow:"7px 7px 0 rgba(0,0,0,0.22)" };
  const btn = { border:"3px solid #222", borderRadius:16, padding:"14px 22px", fontSize:15, fontWeight:900, cursor:"pointer", boxShadow:"4px 4px 0 #222" };

  if (step === 0) {
    return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/laboratoire.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
        <div style={{ position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(26,58,92,0.78), rgba(0,0,0,0.28))" }} />
        <button onClick={onBack} style={{ position:"absolute", top:18, left:18, zIndex:5, ...btn, background:"white", color:"#1A3A5C", padding:"9px 16px" }}>Retour</button>

        <img src={avatar} alt="Avatar" style={{ position:"absolute", left:"1%", bottom:-40, width:390, height:520, objectFit:"contain", zIndex:2, filter:"drop-shadow(8px 8px 0 rgba(0,0,0,0.28))" }} />
        <img src="/e.png" alt="Max" style={{ position:"absolute", right:"2%", bottom:-35, width:350, height:520, objectFit:"cover", objectPosition:"top", zIndex:2, filter:"drop-shadow(8px 8px 0 rgba(0,0,0,0.30))" }} />

        <div style={{ position:"relative", zIndex:3, width:"58vw", margin:"28px auto 0", display:"flex", flexDirection:"column", gap:18 }}>
          <div style={{ ...card, padding:"20px 26px", background:"#FFF8E8" }}>
            <div style={{ fontSize:12, fontWeight:900, color:"#C4622D", letterSpacing:2, textTransform:"uppercase" }}>Max - Analyse du profil</div>
            <h1 style={{ margin:"6px 0 8px", fontSize:46, lineHeight:1, color:"#1A1A1A", fontWeight:900 }}>Mission QCM2 terminee</h1>
            <p style={{ margin:0, fontSize:18, lineHeight:1.5, color:"#333", fontWeight:700 }}>
              Bravo {playerName} ! J'ai analyse tes reponses. Ton profil alimentaire est pret : maintenant on transforme tes habitudes en mission de progression.
            </p>
          </div>

          <div style={{ display:"grid", gridTemplateColumns:"1.05fr .95fr", gap:18 }}>
            <div style={{ ...card, padding:22 }}>
              <div style={{ fontSize:14, fontWeight:900, color:"#6B7280", textTransform:"uppercase", letterSpacing:1 }}>Carte profil</div>
              <div style={{ display:"flex", gap:16, alignItems:"center", marginTop:14 }}>
                <div style={{ width:100, height:100, borderRadius:24, border:"3px solid #222", background:mainReco.bg, display:"flex", alignItems:"center", justifyContent:"center", boxShadow:"4px 4px 0 rgba(0,0,0,0.18)" }}>
                  <img src={mainReco.img} alt="profil" style={{ maxWidth:78, maxHeight:78, objectFit:"contain" }} />
                </div>
                <div style={{ flex:1 }}>
                  <div style={{ fontSize:28, fontWeight:900, color:mainReco.couleur }}>{mainReco.label}</div>
                  <p style={{ margin:"7px 0 0", color:"#444", lineHeight:1.45, fontSize:14, fontWeight:700 }}>{mainReco.texte}</p>
                </div>
              </div>
              <div style={{ marginTop:18, height:18, background:"#E8EDF2", border:"3px solid #222", borderRadius:20, overflow:"hidden" }}>
                <div style={{ height:"100%", width:missionScore + "%", background:"linear-gradient(90deg,#9ACD32,#7FFFD4)" }} />
              </div>
              <div style={{ marginTop:8, fontSize:13, fontWeight:900, color:"#1A3A5C" }}>Progression PNNS : {missionScore}%</div>
            </div>

            <div style={{ ...card, padding:22, background:"#F0F9E0" }}>
              <div style={{ fontSize:16, fontWeight:900, color:"#558B2F", marginBottom:12 }}>Dialogue</div>
              <div style={{ background:"white", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px", boxShadow:"4px 4px 0 rgba(0,0,0,0.15)", fontWeight:800, lineHeight:1.55 }}>
                Max : "Ton profil me donne des indices. Prochaine etape : je vais te debloquer des recommandations et des recettes personnalisees."
              </div>
              <div style={{ marginTop:14, background:"#FFF0EB", border:"3px solid #222", borderRadius:"20px 20px 4px 20px", padding:"14px", boxShadow:"4px 4px 0 rgba(0,0,0,0.15)", fontWeight:800, lineHeight:1.55 }}>
                Toi : "Ok Max, montre-moi ce que je peux ameliorer !"
              </div>
            </div>
          </div>

          <button onClick={() => { playSound("good"); setStep(1); }} style={{ ...btn, alignSelf:"center", background:"#FFDD44", color:"#222", fontSize:18, padding:"17px 34px" }}>
            Continuer vers les recommandations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.35)" }} />
      <button onClick={() => setStep(0)} style={{ position:"fixed", top:18, left:18, zIndex:5, ...btn, background:"white", color:"#1A3A5C", padding:"9px 16px" }}>Retour profil</button>

      <div style={{ position:"relative", zIndex:2, maxWidth:1120, margin:"0 auto", padding:"34px 24px 50px" }}>
        <div style={{ display:"flex", alignItems:"flex-end", gap:18, marginBottom:20 }}>
          <img src="/e.png" alt="Max" style={{ width:120, height:150, objectFit:"cover", objectPosition:"top", filter:"drop-shadow(5px 5px 0 rgba(0,0,0,0.28))" }} />
          <div style={{ ...card, background:"#FFF8E8", padding:"18px 24px", flex:1 }}>
            <div style={{ fontSize:12, fontWeight:900, color:"#C4622D", letterSpacing:2, textTransform:"uppercase" }}>Max - Recompense debloquee</div>
            <h1 style={{ margin:"6px 0", fontSize:42, lineHeight:1, fontWeight:900, color:"#1A1A1A" }}>Clique ici pour avoir tes recommandations et recettes personnalisees</h1>
            <p style={{ margin:0, fontSize:16, fontWeight:700, color:"#444", lineHeight:1.5 }}>Chaque carte correspond a une mission adaptee a ton profil. Tu peux ouvrir directement les recettes associees.</p>
          </div>
        </div>

        {showPetitDej && (
          <div style={{ ...card, padding:22, marginBottom:18, background:"#FFF0EB" }}>
            <div style={{ fontSize:22, fontWeight:900, color:"#E65100", marginBottom:8 }}>Mission bonus : petit dejeuner</div>
            <p style={{ margin:"0 0 14px", fontWeight:700, color:"#444" }}>Comme tu as indique ne pas prendre tous les repas principaux, Max te conseille de securiser ton energie des le matin.</p>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(3, 1fr)", gap:10 }}>
              {PETIT_DEJ_DATA.slice(0,3).map((jour, i) => (
                <div key={i} style={{ background:"white", border:"2px solid #222", borderRadius:16, padding:12, fontSize:13, fontWeight:800 }}>
                  <div style={{ color:"#E65100", marginBottom:6 }}>{jour.jour}</div>
                  <div style={{ color:"#555", lineHeight:1.45 }}>{jour.items.slice(0,2).join(" + ")}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit, minmax(280px, 1fr))", gap:18 }}>
          {profilRecos.map((reco) => (
            <div key={reco.key} style={{ ...card, background:reco.bg, padding:20 }}>
              <div style={{ display:"flex", gap:14, alignItems:"center", marginBottom:14 }}>
                <div style={{ width:72, height:72, borderRadius:20, background:"white", border:"3px solid #222", display:"flex", alignItems:"center", justifyContent:"center", boxShadow:"4px 4px 0 rgba(0,0,0,0.18)" }}>
                  <img src={reco.img} alt="" style={{ maxWidth:56, maxHeight:56, objectFit:"contain" }} />
                </div>
                <div>
                  <div style={{ fontSize:12, fontWeight:900, color:reco.couleur, textTransform:"uppercase", letterSpacing:1 }}>Carte mission</div>
                  <div style={{ fontSize:24, fontWeight:900, color:"#1A1A1A" }}>{reco.label}</div>
                </div>
              </div>
              <p style={{ margin:"0 0 12px", color:"#444", fontSize:14, lineHeight:1.55, fontWeight:700 }}>{reco.texte}</p>
              <div style={{ display:"flex", flexDirection:"column", gap:8, marginBottom:16 }}>
                {reco.conseils.map((c, i) => (
                  <div key={i} style={{ background:"rgba(255,255,255,0.8)", border:"2px solid rgba(0,0,0,0.12)", borderRadius:12, padding:"9px 11px", fontSize:13, fontWeight:800, color:"#333" }}>{i+1}. {c}</div>
                ))}
              </div>
              <button onClick={() => { playSound("badge"); onVoirRecettes(reco.profil); }} style={{ ...btn, width:"100%", background:reco.couleur, color:"white" }}>
                Debloquer mes recettes
              </button>
            </div>
          ))}

          <div style={{ ...card, background:"#E0F7F5", padding:20 }}>
            <div style={{ fontSize:12, fontWeight:900, color:"#00897B", textTransform:"uppercase", letterSpacing:1 }}>Recommande PNNS</div>
            <div style={{ fontSize:26, fontWeight:900, color:"#1A1A1A", margin:"6px 0" }}>Mode mediterraneen</div>
            <p style={{ margin:"0 0 16px", color:"#444", fontSize:14, lineHeight:1.55, fontWeight:700 }}>Fruits, legumes, poisson, huile d'olive et repas equilibres : une base solide pour progresser.</p>
            <button onClick={() => { playSound("badge"); onVoirRecettes("mediterraneen"); }} style={{ ...btn, width:"100%", background:"#00BFA5", color:"white" }}>
              Voir les recettes mediterraneennes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}


'''

text = text[:start] + new_component + text[end:]

old_call = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'
new_call = 'if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarSrc={avatarChoice === "fille" ? "/fille.png" : "/garcon.png"} avatarGender={avatarChoice} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'
if old_call in text:
    text = text.replace(old_call, new_call)
else:
    # Already patched or formatted differently: do nothing.
    pass

TARGET.write_text(text, encoding="utf-8")
print("✅ Patch QCM2 gameplay v3 applique !")
print(f"💾 Sauvegarde creee : {backup.name}")
print("➡️ Lance : cd .. puis npm run dev")
