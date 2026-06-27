"""
PATCH 12 — Page Profil QCM2 + Page Intro Recommandations (style jeu)
après QCM2 : fond cuisine2, Max + avatar, bulles dialogue, barres habitudes
Usage: python patch_12_profil_qcm2_pages.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ══════════════════════════════════════════════════════
# FIX 1 — Ajouter ProfilQcm2Screen + IntroRecosQcm2Screen
# AVANT /* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */
# ══════════════════════════════════════════════════════

MARKER = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

if MARKER not in code:
    print("⚠️  Marqueur non trouvé")
    sys.exit(1)

NEW_SCREENS = '''/* ══ PAGE PROFIL QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const cuisine    = answers["‍ En cuisine"] || answers["\u200d En cuisine"];
  const pratiques  = answers[" Pratiques alimentaires"];
  const compo      = answers[" Composition du repas"];
  const nbPersons  = answers[" Nombre de personnes"];
  const nbRepas    = answers[" Nombre de repas"];

  const HABITUDES = [
    {
      label: "Composition du repas",
      img: "/repas.png",
      valeur: compo || "—",
      couleur: "#4caf50",
      label2: compo ? "Bon équilibre !" : "Non renseigné",
      ok: !!compo,
    },
    {
      label: "Pratiques alimentaires",
      img: "/aliment.png",
      valeur: pratiques || "—",
      couleur: pratiques === "Je mange sans viande" ? "#558b2f" : pratiques === "Je mange sans porc" ? "#0288d1" : "#4caf50",
      label2: pratiques === "Je mange de tout" ? "Très bien !" : pratiques ? "Pris en compte" : "Non renseigné",
      ok: !!pratiques,
    },
    {
      label: "Temps en cuisine",
      img: "/marmitte.png",
      valeur: cuisine || "—",
      couleur: cuisine === "Je n'ai pas le temps" ? "#f57c00" : "#4caf50",
      label2: cuisine === "Je n'ai pas le temps" ? "Recettes rapides !" : cuisine ? "Super !" : "Non renseigné",
      ok: !!cuisine,
    },
    {
      label: "Nombre de repas/jour",
      img: "/oeuf.png",
      valeur: nbRepas || "—",
      couleur: nbRepas === "Midi et soir" ? "#4caf50" : "#f57c00",
      label2: nbRepas === "Midi et soir" ? "Très bien !" : nbRepas ? "À améliorer" : "Non renseigné",
      ok: nbRepas === "Midi et soir",
    },
    {
      label: "Couverts à table",
      img: "/assiette.png",
      valeur: nbPersons || "—",
      couleur: "#9ACD32",
      label2: "Noté !",
      ok: true,
    },
  ];

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      {/* Fond cuisine */}
      <div style={{ position:"absolute", inset:0 }}>
        <img src="/cuisine2.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)" }} />
      </div>

      {/* Header */}
      <div style={{ position:"relative", zIndex:10, background:"#FA8072", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"5px 14px" }}>← Retour</button>
        <div style={{ display:"flex", alignItems:"center", gap:8 }}>
          <span style={{ fontSize:20 }}>⭐</span>
          <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>PROFIL CRÉÉ !</span>
          <span style={{ fontSize:20 }}>⭐</span>
        </div>
        <div style={{ fontSize:12, color:"rgba(255,255,255,0.8)" }}>Voici ton profil alimentaire</div>
      </div>

      {/* Contenu principal */}
      <div style={{ position:"relative", zIndex:5, display:"flex", height:"calc(100vh - 52px)", padding:"16px", gap:16, overflow:"hidden" }}>

        {/* Colonne gauche : Max + Avatar */}
        <div style={{ display:"flex", flexDirection:"column", justifyContent:"space-between", width:220, flexShrink:0 }}>
          {/* Max + bulle */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:8 }}>
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"16px 16px 16px 4px", padding:"12px 14px", boxShadow:"4px 4px 0 rgba(0,0,0,0.3)", maxWidth:180, fontSize:13, fontWeight:700, color:"#222", lineHeight:1.6 }}>
              Wow ! Tu viens de compléter ton profil alimentaire !<br/>
              <span style={{ fontSize:12, color:"#FA8072", fontWeight:800 }}>Regardons ensemble tes habitudes. 🍽️</span>
            </div>
            <img src="/e.png" alt="Max" style={{ width:140, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"#FA8072", border:"2px solid #222", borderRadius:20, padding:"4px 12px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222", alignSelf:"center" }}>Max</div>
          </div>

          {/* Avatar + bulle */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <img src={avatarSrc} alt="Joueur" style={{ width:90, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.3))" }} />
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"4px 16px 16px 16px", padding:"10px 12px", boxShadow:"3px 3px 0 rgba(0,0,0,0.3)", maxWidth:180, fontSize:12, fontWeight:700, color:"#222", lineHeight:1.5 }}>
              D'accord Max, je suis curieux(se) de voir ! 👀
            </div>
          </div>
        </div>

        {/* Tableau récap */}
        <div style={{ flex:1, background:"rgba(20,20,20,0.85)", borderRadius:20, border:"3px solid #ffcc00", padding:"20px 24px", boxShadow:"0 8px 32px rgba(0,0,0,0.5)", overflowY:"auto" }}>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"#ffcc00", textAlign:"center", marginBottom:20, textTransform:"uppercase", letterSpacing:1 }}>
            📋 Récapitulatif de tes habitudes
          </div>

          {HABITUDES.map((h, i) => (
            <div key={i} style={{ display:"flex", alignItems:"center", gap:14, marginBottom:16, background:"rgba(255,255,255,0.08)", borderRadius:12, padding:"12px 16px" }}>
              <img src={h.img} alt="" style={{ width:36, height:36, objectFit:"contain", flexShrink:0 }} />
              <div style={{ flex:1, minWidth:0 }}>
                <div style={{ fontSize:12, fontWeight:800, color:"white", marginBottom:6 }}>{h.label}</div>
                <div style={{ position:"relative", height:10, background:"rgba(255,255,255,0.15)", borderRadius:99 }}>
                  <div style={{ position:"absolute", left:0, top:0, height:"100%", width: h.ok ? "80%" : "30%", background:h.couleur, borderRadius:99, transition:"width 0.8s ease" }} />
                </div>
              </div>
              <div style={{ minWidth:110, textAlign:"right" }}>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", marginBottom:2 }}>{h.valeur}</div>
                <div style={{ fontSize:12, fontWeight:900, color:h.couleur }}>{h.label2}</div>
              </div>
            </div>
          ))}

          <div style={{ marginTop:16, background:"rgba(255,204,0,0.15)", border:"2px solid #ffcc00", borderRadius:10, padding:"10px 14px", fontSize:12, color:"#ffdd44", fontWeight:700, textAlign:"center" }}>
            ⭐ Ton profil est unique — chaque petit pas compte pour ta santé !
          </div>
        </div>

      </div>

      {/* Bouton Suivant */}
      <div style={{ position:"fixed", bottom:20, right:24, zIndex:20 }}>
        <button onClick={onSuivant}
          style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"5px 5px 0 #222", display:"flex", alignItems:"center", gap:8 }}>
          Suivant → <span style={{ fontSize:18 }}>🍽️</span>
        </button>
      </div>
    </div>
  );
}

/* ══ INTRO RECOMMANDATIONS QCM2 ══ */
function IntroRecosQcm2Screen({ answers, playerName, avatarChoice, onVoirRecos, onVoirRecettes, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      {/* Fond cuisine */}
      <div style={{ position:"absolute", inset:0 }}>
        <img src="/cuisine2.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)" }} />
      </div>

      {/* Header */}
      <div style={{ position:"relative", zIndex:10, background:"#74b87a", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"5px 14px" }}>← Retour</button>
        <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>🌟 AU PROGRAMME</span>
        <div style={{ width:80 }} />
      </div>

      {/* Contenu */}
      <div style={{ position:"relative", zIndex:5, display:"flex", height:"calc(100vh - 52px)", padding:"16px", gap:16, overflow:"hidden" }}>

        {/* Gauche : Max + Avatar */}
        <div style={{ display:"flex", flexDirection:"column", justifyContent:"space-between", width:220, flexShrink:0 }}>
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:8 }}>
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"16px 16px 16px 4px", padding:"12px 14px", boxShadow:"4px 4px 0 rgba(0,0,0,0.3)", maxWidth:190, fontSize:13, fontWeight:700, color:"#222", lineHeight:1.65 }}>
              Super travail ! 🎉<br/>
              Grâce à tes réponses, je peux te proposer des <strong style={{ color:"#FA8072" }}>recommandations</strong> et des <strong style={{ color:"#9ACD32" }}>recettes</strong> 100% adaptées à toi !<br/>
              <span style={{ fontSize:12, color:"#666" }}>Prêt(e) à découvrir tout ça ?</span>
            </div>
            <img src="/e.png" alt="Max" style={{ width:140, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"#FA8072", border:"2px solid #222", borderRadius:20, padding:"4px 12px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222", alignSelf:"center" }}>Max</div>
          </div>

          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <img src={avatarSrc} alt="Joueur" style={{ width:90, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.3))" }} />
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"4px 16px 16px 16px", padding:"10px 12px", boxShadow:"3px 3px 0 rgba(0,0,0,0.3)", maxWidth:190, fontSize:12, fontWeight:700, color:"#222", lineHeight:1.5 }}>
              Ouiii ! J'ai hâte de voir mes recommandations personnalisées ! 😍
            </div>
          </div>
        </div>

        {/* Droite : panneau programme */}
        <div style={{ flex:1, display:"flex", flexDirection:"column", justifyContent:"center", gap:20 }}>

          {/* Panneau "Au programme" */}
          <div style={{ background:"rgba(20,20,20,0.85)", borderRadius:20, border:"3px solid #ffcc00", padding:"24px", boxShadow:"0 8px 32px rgba(0,0,0,0.5)" }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"#ffcc00", textAlign:"center", marginBottom:20, textTransform:"uppercase", letterSpacing:1 }}>
              🗒️ Au programme :
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>
              {/* Carte Recommandations */}
              <div onClick={onVoirRecos} style={{ background:"rgba(255,255,255,0.1)", border:"3px solid #FA8072", borderRadius:16, padding:"20px 16px", textAlign:"center", cursor:"pointer", transition:"transform 0.2s", }}
                onMouseEnter={e=>e.currentTarget.style.transform="scale(1.04)"}
                onMouseLeave={e=>e.currentTarget.style.transform="scale(1)"}>
                <img src="/aliment.png" alt="" style={{ width:60, height:60, objectFit:"contain", marginBottom:10 }} />
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#FA8072", marginBottom:6 }}>RECOMMANDATIONS PERSONNALISÉES</div>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.8)", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil</div>
              </div>
              {/* Carte Recettes */}
              <div onClick={onVoirRecettes} style={{ background:"rgba(255,255,255,0.1)", border:"3px solid #9ACD32", borderRadius:16, padding:"20px 16px", textAlign:"center", cursor:"pointer", transition:"transform 0.2s" }}
                onMouseEnter={e=>e.currentTarget.style.transform="scale(1.04)"}
                onMouseLeave={e=>e.currentTarget.style.transform="scale(1)"}>
                <img src="/repas.png" alt="" style={{ width:60, height:60, objectFit:"contain", marginBottom:10 }} />
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#9ACD32", marginBottom:6 }}>RECETTES PERSONNALISÉES</div>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.8)", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
              </div>
            </div>
          </div>

          {/* Bouton principal */}
          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"5px 5px 0 #222", textAlign:"center", animation:"pulse 2s infinite" }}>
            ✨ Clique ici pour découvrir tes recommandations et recettes !
          </button>

          {/* Barre progression */}
          <div style={{ display:"flex", alignItems:"center", justifyContent:"center", gap:0 }}>
            {[
              { label:"QCM 1", done:true },
              { label:"QCM 2", done:true },
              { label:"Profil", done:true, active:false },
              { label:"Recos", done:false, active:true },
              { label:"Recettes", done:false },
            ].map((step, i, arr) => (
              <div key={i} style={{ display:"flex", alignItems:"center" }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:4 }}>
                  <div style={{ width:32, height:32, borderRadius:"50%", background: step.done ? "#9ACD32" : step.active ? "#FA8072" : "rgba(255,255,255,0.3)", border:"3px solid #222", display:"flex", alignItems:"center", justifyContent:"center", fontSize:13 }}>
                    {step.done ? "✓" : step.active ? "●" : "○"}
                  </div>
                  <div style={{ fontSize:9, fontWeight:800, color: step.done ? "#9ACD32" : step.active ? "#FA8072" : "rgba(255,255,255,0.6)", whiteSpace:"nowrap" }}>{step.label}</div>
                </div>
                {i < arr.length-1 && <div style={{ width:40, height:3, background: step.done ? "#9ACD32" : "rgba(255,255,255,0.2)", margin:"0 4px", marginBottom:16 }} />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

'''

before = code[:code.index(MARKER)]
after  = code[code.index(MARKER):]
code = before + NEW_SCREENS + after
fixes += 1
print("✅ FIX 1 — ProfilQcm2Screen + IntroRecosQcm2Screen ajoutés")

# ══════════════════════════════════════════════════════
# FIX 2 — Dans App() : ajouter les phases profil_qcm2 et intro_recos_qcm2
# ══════════════════════════════════════════════════════

OLD_RECOS_QCM2 = '    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'

NEW_RECOS_QCM2 = '''    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("intro_recos_qcm2")} />;
    if (phase === "intro_recos_qcm2") return <IntroRecosQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm2")} onVoirRecettes={() => { setFiltreRecetteProfil(null); goTo("recettes"); }} />;
    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'''

if OLD_RECOS_QCM2 in code:
    code = code.replace(OLD_RECOS_QCM2, NEW_RECOS_QCM2)
    fixes += 1
    print("✅ FIX 2 — Phases profil_qcm2 et intro_recos_qcm2 ajoutées dans App")
else:
    print("⚠️  FIX 2 — Phase recos_qcm2 non trouvée")

# ══════════════════════════════════════════════════════
# FIX 3 — Dans QCM2 (écran done), modifier le bouton Recommandations
# pour aller vers profil_qcm2 au lieu de recos_qcm2
# ══════════════════════════════════════════════════════

OLD_RECOS_BTN = 'if(onDone) onDone(answers[" Composition du repas"], "recos", answers);'
NEW_RECOS_BTN = 'if(onDone) onDone(answers[" Composition du repas"], "profil_qcm2", answers);'

if OLD_RECOS_BTN in code:
    code = code.replace(OLD_RECOS_BTN, NEW_RECOS_BTN)
    fixes += 1
    print("✅ FIX 3 — Bouton Recommandations QCM2 redirige vers profil_qcm2")
else:
    print("⚠️  FIX 3 — Bouton recos non trouvé")

# ══════════════════════════════════════════════════════
# FIX 4 — Dans App() onDone QCM2 : gérer la nouvelle phase profil_qcm2
# ══════════════════════════════════════════════════════

OLD_QCM2_ONDONE = 'if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante");'
NEW_QCM2_ONDONE = 'if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos" || cuisine==="profil_qcm2") goTo("profil_qcm2"); else if(cuisine==="sante") goTo("qcm_sante");'

if OLD_QCM2_ONDONE in code:
    code = code.replace(OLD_QCM2_ONDONE, NEW_QCM2_ONDONE)
    fixes += 1
    print("✅ FIX 4 — onDone QCM2 gère profil_qcm2")
else:
    print("⚠️  FIX 4 — onDone QCM2 non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/4 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
