"""
PATCH 12 — Pages post-QCM2 : Page Récap (style A) + Page Au Programme (style B)
Usage: python patch_12_post_qcm2_pages.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ══════════════════════════════════════════════════════
# FIX 1 — Ajouter ProfilQcm2Screen et AuProgrammeScreen
# AVANT /* ══ SÉLECTION QCM ══ */
# ══════════════════════════════════════════════════════

MARKER = "/* ══ SÉLECTION QCM ══ */"

NEW_SCREENS = '''/* ══ PAGE RÉCAP QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const nbRepas    = answers[" Nombre de repas"] || "—";
  const pratiques  = answers[" Pratiques alimentaires"] || "—";
  const compo      = answers[" Composition du repas"] || "—";
  const cuisine    = answers["‍ En cuisine"] || "—";
  const nbPersons  = answers[" Nombre de personnes"] || "—";

  const LIGNES = [
    { label:"Nombre de personnes", value:nbPersons,  icon:"ti-users",          color:"#1976d2" },
    { label:"Pratiques alimentaires", value:pratiques, icon:"ti-leaf",          color:"#4caf50" },
    { label:"Composition du repas",   value:compo,    icon:"ti-bowl-chopsticks",color:"#f57c00" },
    { label:"Temps en cuisine",       value:cuisine,  icon:"ti-clock",          color:"#795548" },
    { label:"Nombre de repas/jour",   value:nbRepas,  icon:"ti-calendar",       color:"#FA8072" },
  ];

  const getScore = () => {
    let score = 60;
    if (pratiques.includes("sans viande") || pratiques.includes("sans porc")) score += 5;
    if (cuisine === "J'aime y passer du temps") score += 10;
    if (nbRepas === "Midi et soir") score += 15;
    else if (nbRepas === "Midi uniquement" || nbRepas === "Soir uniquement") score -= 10;
    return Math.min(Math.max(score, 0), 100);
  };

  const score = getScore();
  const scoreColor = score >= 70 ? "#4caf50" : score >= 50 ? "#f57c00" : "#e53935";
  const scoreLabel = score >= 70 ? "Très bien !" : score >= 50 ? "Pas mal !" : "À améliorer";

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header étoile */}
      <div style={{ background:"#FA8072", padding:"14px 20px", textAlign:"center" }}>
        <button onClick={onBack} style={{ position:"absolute", left:16, top:14, background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px" }}>← Retour</button>
        <div style={{ fontSize:20, fontWeight:900, color:"white", display:"flex", alignItems:"center", justifyContent:"center", gap:8, fontFamily:"Arial Black, Arial, sans-serif" }}>
          ⭐ Profil créé ! ⭐
        </div>
        <div style={{ fontSize:12, color:"rgba(255,255,255,0.9)", marginTop:4 }}>Voici ton profil alimentaire personnalisé</div>
      </div>

      {/* Contenu principal */}
      <div style={{ display:"grid", gridTemplateColumns:"180px 1fr", minHeight:"calc(100vh - 110px)" }}>

        {/* Colonne gauche : Max + Avatar */}
        <div style={{ background:"#fff8f0", borderRight:"2px solid #eee", padding:"20px 16px", display:"flex", flexDirection:"column", alignItems:"center", gap:14 }}>

          {/* Max */}
          <img src="/e.png" alt="Max" style={{ width:120, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"#e8f5e9", border:"2px solid #9ACD32", borderRadius:"12px 12px 12px 4px", padding:"10px 12px", fontSize:11, color:"#2e7d32", lineHeight:1.6, textAlign:"center" }}>
            Wow ! Tu viens de compléter ton profil alimentaire ! Regardons ensemble tes habitudes. 🌟
          </div>
          <div style={{ fontSize:11, fontWeight:900, color:"#FA8072", background:"#fff0ee", border:"1px solid #FA807244", borderRadius:20, padding:"3px 12px" }}>Max</div>

          <div style={{ width:"100%", height:1, background:"#eee" }} />

          {/* Avatar joueur */}
          <img src={avatarSrc} alt="Avatar" style={{ width:80, filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"white", border:"2px solid #1976d2", borderRadius:"12px 12px 4px 12px", padding:"10px 12px", fontSize:11, color:"#1976d2", lineHeight:1.6, textAlign:"center" }}>
            D'accord Max, je suis curieux(se) de voir ! 👀
          </div>
          <div style={{ fontSize:11, fontWeight:900, color:"#1976d2", background:"#e3f2fd", border:"1px solid #1976d244", borderRadius:20, padding:"3px 12px" }}>{playerName}</div>
        </div>

        {/* Colonne droite : récap */}
        <div style={{ padding:"20px 24px" }}>
          <div style={{ fontSize:13, fontWeight:900, color:"#555", textTransform:"uppercase", letterSpacing:"1px", marginBottom:16 }}>Récapitulatif de tes habitudes</div>

          {/* Score global */}
          <div style={{ background:"white", borderRadius:14, padding:"14px 18px", marginBottom:16, border:"2px solid " + scoreColor + "44", display:"flex", alignItems:"center", gap:14 }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:scoreColor, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
              <span style={{ fontSize:16, fontWeight:900, color:"white" }}>{score}%</span>
            </div>
            <div>
              <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:scoreColor }}>{scoreLabel}</div>
              <div style={{ fontSize:11, color:"#888", marginTop:2 }}>Score global de ton profil alimentaire</div>
            </div>
          </div>

          {/* Lignes réponses */}
          <div style={{ display:"flex", flexDirection:"column", gap:10, marginBottom:16 }}>
            {LIGNES.map((l, i) => (
              <div key={i} style={{ background:"white", borderRadius:12, padding:"12px 16px", border:"1.5px solid " + l.color + "33", display:"flex", alignItems:"center", gap:12 }}>
                <div style={{ width:36, height:36, borderRadius:10, background:l.color + "18", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                  <i className={"ti " + l.icon} style={{ fontSize:18, color:l.color }} />
                </div>
                <div style={{ flex:1 }}>
                  <div style={{ fontSize:11, color:"#888", marginBottom:2 }}>{l.label}</div>
                  <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A" }}>{l.value}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Message */}
          <div style={{ background:"#fff8e1", borderRadius:10, padding:"10px 14px", fontSize:12, color:"#f57c00", display:"flex", alignItems:"center", gap:8 }}>
            ⭐ Ton profil est unique, chaque petit pas compte pour ta santé !
          </div>
        </div>
      </div>

      {/* Bouton suivant */}
      <div style={{ background:"white", borderTop:"2px solid #eee", padding:"16px 24px", display:"flex", justifyContent:"flex-end" }}>
        <button onClick={onSuivant}
          style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:12, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"13px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
          Suivant →
        </button>
      </div>
    </div>
  );
}

/* ══ PAGE AU PROGRAMME (post-QCM2) ══ */
function AuProgrammeScreen({ playerName, avatarChoice, onRecos, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const STEPS = ["QCM 1", "QCM 2", "Profil", "Recos", "Recettes"];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"16px 24px", display:"flex", alignItems:"center", gap:16 }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px", flexShrink:0 }}>← Retour</button>
        <div style={{ flex:1 }}>
          <div style={{ fontSize:11, color:"rgba(255,255,255,0.8)", marginBottom:2 }}>Super travail ! 🎉</div>
          <div style={{ fontSize:14, fontWeight:700, color:"white", lineHeight:1.5 }}>
            Grâce à tes réponses, je peux te proposer des recommandations et des recettes 100% adaptées à toi !
          </div>
        </div>
        <img src={avatarSrc} alt="Avatar" style={{ width:60, filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
      </div>

      {/* Contenu */}
      <div style={{ padding:"24px 32px" }}>

        {/* Max + bulle */}
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, marginBottom:28 }}>
          <img src="/e.png" alt="Max" style={{ width:130, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
          <div style={{ background:"white", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.15)", flex:1 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:14, fontWeight:700, color:"#222", lineHeight:1.7 }}>
              Prêt(e) à découvrir tout ça ? 🌟<br/>
              <span style={{ fontSize:13, fontWeight:600, color:"#555" }}>Tes recommandations et recettes sont personnalisées en fonction de tes habitudes alimentaires, tes préférences et ton profil.</span>
            </div>
          </div>
        </div>

        {/* Titre */}
        <div style={{ textAlign:"center", marginBottom:20 }}>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 rgba(0,0,0,0.08)" }}>Au programme :</div>
        </div>

        {/* 2 cartes */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:20 }}>
          <div style={{ background:"white", border:"2px solid #9ACD3266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#e8f5e9", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center" }}>
              <i className="ti ti-clipboard-list" style={{ fontSize:28, color:"#9ACD32" }} />
            </div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#639922", marginBottom:6 }}>Recommandations personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil alimentaire</div>
          </div>
          <div style={{ background:"white", border:"2px solid #FA807266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#fff0ee", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center" }}>
              <i className="ti ti-salad" style={{ fontSize:28, color:"#FA8072" }} />
            </div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#c4622d", marginBottom:6 }}>Recettes personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
          </div>
        </div>

        {/* Bouton principal */}
        <button onClick={onRecos}
          style={{ width:"100%", background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"4px 4px 0 #222", marginBottom:24 }}>
          Clique ici pour découvrir tes recommandations et recettes ! 🍽️
        </button>

        {/* Barre progression mission */}
        <div style={{ background:"white", borderRadius:14, padding:"12px 20px", border:"1.5px solid #eee", display:"flex", alignItems:"center", gap:12 }}>
          <span style={{ fontSize:20 }}>🏆</span>
          <div>
            <div style={{ fontSize:11, fontWeight:900, color:"#c4622d" }}>Mission accomplie</div>
            <div style={{ fontSize:10, color:"#888" }}>Ton aventure continue...</div>
          </div>
          <div style={{ flex:1, display:"flex", alignItems:"center", justifyContent:"flex-end", gap:4 }}>
            {STEPS.map((s, i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:3 }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:2 }}>
                  <div style={{ width:22, height:22, borderRadius:"50%", background:i<3?"#9ACD32":i===3?"#FA8072":"#eee", border:"2px solid " + (i<3?"#639922":i===3?"#c4622d":"#ddd"), display:"flex", alignItems:"center", justifyContent:"center" }}>
                    {i < 2 ? <i className="ti ti-check" style={{ fontSize:11, color:"white" }} /> : <div style={{ width:6, height:6, borderRadius:"50%", background:i===2?"white":i===3?"white":"#ccc" }} />}
                  </div>
                  <div style={{ fontSize:8, color:"#888", whiteSpace:"nowrap" }}>{s}</div>
                </div>
                {i < STEPS.length - 1 && <div style={{ width:12, height:1.5, background:"#ddd", marginBottom:10 }} />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

'''

if MARKER in code:
    code = code.replace(MARKER, NEW_SCREENS + MARKER)
    fixes += 1
    print("✅ FIX 1 — ProfilQcm2Screen + AuProgrammeScreen ajoutés")
else:
    print("⚠️  FIX 1 — Marqueur SÉLECTION QCM non trouvé")

# ══════════════════════════════════════════════════════
# FIX 2 — Dans App() : ajouter les phases et modifier le flux QCM2
# ══════════════════════════════════════════════════════

OLD_QCM2_PHASE = '    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) { setQcm2Answers(ans); setQcm2AnswersForRecos(ans); } if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); }} />;'

NEW_QCM2_PHASE = '''    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) { setQcm2Answers(ans); setQcm2AnswersForRecos(ans); } if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); else goTo("profil_qcm2"); }} />;
    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("au_programme")} />;
    if (phase === "au_programme") return <AuProgrammeScreen playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onRecos={() => goTo("recos_qcm2")} />;'''

if OLD_QCM2_PHASE in code:
    code = code.replace(OLD_QCM2_PHASE, NEW_QCM2_PHASE)
    fixes += 1
    print("✅ FIX 2 — Phases profil_qcm2 et au_programme ajoutées dans App")
else:
    # Try without qcm2AnswersForRecos
    OLD_QCM2_PHASE2 = '    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) setQcm2Answers(ans); if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); }} />;'
    NEW_QCM2_PHASE2 = '''    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) setQcm2Answers(ans); if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); else goTo("profil_qcm2"); }} />;
    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("au_programme")} />;
    if (phase === "au_programme") return <AuProgrammeScreen playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onRecos={() => goTo("recos_qcm2")} />;'''
    if OLD_QCM2_PHASE2 in code:
        code = code.replace(OLD_QCM2_PHASE2, NEW_QCM2_PHASE2)
        fixes += 1
        print("✅ FIX 2 — Phases ajoutées (v2)")
    else:
        print("⚠️  FIX 2 — Phase qcm2 non trouvée")

# ══════════════════════════════════════════════════════
# FIX 3 — Dans Qcm2Screen done : le bouton "Continuer vers mon profil santé"
# redirige vers qcm_sante directement (pas via onDone avec cuisine="sante")
# On modifie le bouton dans la page done du Qcm2Screen
# ══════════════════════════════════════════════════════

OLD_CONTINUER = '''          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "sante", answers); }}
            style={{ background:"#1A3A5C", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"18px", cursor:"pointer", width:"100%", boxShadow:"0 4px 20px rgba(26,58,92,0.25)" }}
            onMouseEnter={e => e.currentTarget.style.opacity = "0.9"}
            onMouseLeave={e => e.currentTarget.style.opacity = "1"}>
            Continuer vers mon profil santé →
          </button>'''

NEW_CONTINUER = '''          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "sante", answers); }}
            style={{ background:"#1A3A5C", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"18px", cursor:"pointer", width:"100%", boxShadow:"0 4px 20px rgba(26,58,92,0.25)" }}
            onMouseEnter={e => e.currentTarget.style.opacity = "0.9"}
            onMouseLeave={e => e.currentTarget.style.opacity = "1"}>
            Continuer vers mon profil santé →
          </button>
          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "profil_qcm2", answers); }}
            style={{ background:"white", border:"2px solid #9ACD32", borderRadius:14, color:"#639922", fontSize:14, fontWeight:900, padding:"14px", cursor:"pointer", width:"100%" }}>
            Voir mon profil alimentaire →
          </button>'''

if OLD_CONTINUER in code:
    code = code.replace(OLD_CONTINUER, NEW_CONTINUER)
    fixes += 1
    print("✅ FIX 3 — Bouton 'Voir mon profil alimentaire' ajouté dans QCM2 done")
else:
    print("⚠️  FIX 3 — Bouton continuer non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/3 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
