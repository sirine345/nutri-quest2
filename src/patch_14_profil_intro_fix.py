"""
PATCH 14 — Fix visuel ProfilQcm2Screen + IntroRecosQcm2Screen
- Page profil : s'affiche bien AVANT intro
- Max = /e.png
- Avatar plus grand
- Meilleures images dans cartes
Usage: python patch_14_profil_intro_fix.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

# Trouver et remplacer les deux composants
start1 = "/* ══ PAGE PROFIL QCM2 ══ */"
start2 = "/* ══ INTRO RECOMMANDATIONS QCM2 ══ */"
end2   = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

if start1 not in code or start2 not in code or end2 not in code:
    print("⚠️  Marqueurs non trouvés")
    sys.exit(1)

before = code[:code.index(start1)]
after  = code[code.index(end2):]

NEW_BOTH = '''/* ══ PAGE PROFIL QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const cuisine   = answers["\u200d En cuisine"] || answers["‍ En cuisine"];
  const pratiques = answers[" Pratiques alimentaires"];
  const compo     = answers[" Composition du repas"];
  const nbPersons = answers[" Nombre de personnes"];
  const nbRepas   = answers[" Nombre de repas"];

  const HABITUDES = [
    { label:"Composition du repas",    img:"/repas.png",      valeur:compo||"—",     couleur:"#4caf50", tag: compo ? "Noté !" : "—",           ok:!!compo },
    { label:"Pratiques alimentaires",  img:"/aliment.png",    valeur:pratiques||"—", couleur: pratiques==="Je mange de tout"?"#4caf50":pratiques?"#0288d1":"#aaa", tag: pratiques==="Je mange de tout"?"Très bien !":pratiques?"Pris en compte":"—", ok:!!pratiques },
    { label:"Temps en cuisine",        img:"/marmitte.png",   valeur:cuisine||"—",   couleur:cuisine==="Je n'ai pas le temps"?"#f57c00":"#4caf50", tag:cuisine==="Je n'ai pas le temps"?"Recettes rapides !":cuisine?"Super !":"—", ok:!!cuisine },
    { label:"Nombre de repas/jour",    img:"/oeuf.png",       valeur:nbRepas||"—",   couleur:nbRepas==="Midi et soir"?"#4caf50":"#f57c00", tag:nbRepas==="Midi et soir"?"Très bien !":nbRepas?"À améliorer":"—", ok:nbRepas==="Midi et soir" },
    { label:"Personnes à table",       img:"/assiette.png",   valeur:nbPersons||"—", couleur:"#9ACD32", tag:"Noté !", ok:true },
  ];

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0 }}>
        <img src="/cuisine2.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      </div>

      {/* Header */}
      <div style={{ position:"relative", zIndex:10, background:"#FA8072", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"center", boxShadow:"0 3px 0 #222" }}>
        <button onClick={onBack} style={{ position:"absolute", left:16, background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"5px 14px" }}>← Retour</button>
        <div style={{ display:"flex", alignItems:"center", gap:8 }}>
          <span style={{ fontSize:20 }}>⭐</span>
          <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>PROFIL CRÉÉ !</span>
          <span style={{ fontSize:20 }}>⭐</span>
        </div>
      </div>

      <div style={{ position:"relative", zIndex:5, display:"grid", gridTemplateColumns:"220px 1fr", height:"calc(100vh - 52px)", padding:"16px", gap:16, overflow:"hidden" }}>

        {/* Colonne gauche : Max + Avatar */}
        <div style={{ display:"flex", flexDirection:"column", justifyContent:"space-between" }}>
          {/* Max */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"16px 16px 16px 4px", padding:"12px 14px", boxShadow:"4px 4px 0 rgba(0,0,0,0.4)", fontSize:13, fontWeight:700, color:"#222", lineHeight:1.65 }}>
              Wow ! Tu viens de compléter ton profil alimentaire !<br/>
              <span style={{ fontSize:12, color:"#FA8072", fontWeight:800 }}>Regardons ensemble tes habitudes 🍽️</span>
            </div>
            <img src="/e.png" alt="Max" style={{ width:160, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"#FA8072", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222", alignSelf:"center" }}>Max</div>
          </div>

          {/* Avatar joueur */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <img src={avatarSrc} alt="Joueur" style={{ width:110, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"4px 16px 16px 16px", padding:"10px 12px", boxShadow:"3px 3px 0 rgba(0,0,0,0.4)", fontSize:12, fontWeight:700, color:"#222", lineHeight:1.5 }}>
              D'accord Max, je suis curieux(se) de voir ! 👀
            </div>
          </div>
        </div>

        {/* Tableau récap */}
        <div style={{ background:"rgba(15,15,15,0.88)", borderRadius:20, border:"3px solid #ffcc00", padding:"20px 24px", boxShadow:"0 8px 32px rgba(0,0,0,0.6)", overflowY:"auto" }}>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:"#ffcc00", textAlign:"center", marginBottom:20, textTransform:"uppercase", letterSpacing:1 }}>
            📋 Récapitulatif de tes habitudes
          </div>

          {HABITUDES.map((h, i) => (
            <div key={i} style={{ display:"flex", alignItems:"center", gap:14, marginBottom:14, background:"rgba(255,255,255,0.07)", borderRadius:12, padding:"12px 16px", border:"1px solid rgba(255,255,255,0.1)" }}>
              <img src={h.img} alt="" style={{ width:38, height:38, objectFit:"contain", flexShrink:0 }} />
              <div style={{ flex:1 }}>
                <div style={{ fontSize:12, fontWeight:800, color:"rgba(255,255,255,0.9)", marginBottom:6 }}>{h.label}</div>
                <div style={{ position:"relative", height:10, background:"rgba(255,255,255,0.15)", borderRadius:99 }}>
                  <div style={{ position:"absolute", left:0, top:0, height:"100%", width:h.ok?"75%":"25%", background:h.couleur, borderRadius:99 }} />
                </div>
              </div>
              <div style={{ minWidth:130, textAlign:"right", flexShrink:0 }}>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.6)", marginBottom:2 }}>{h.valeur}</div>
                <div style={{ fontSize:12, fontWeight:900, color:h.couleur }}>{h.tag}</div>
              </div>
            </div>
          ))}

          <div style={{ marginTop:14, background:"rgba(255,204,0,0.15)", border:"2px solid #ffcc00", borderRadius:10, padding:"10px 14px", fontSize:12, color:"#ffdd44", fontWeight:700, textAlign:"center" }}>
            ⭐ Ton profil est unique — chaque petit pas compte pour ta santé !
          </div>
        </div>
      </div>

      {/* Bouton Suivant */}
      <div style={{ position:"fixed", bottom:20, right:24, zIndex:20 }}>
        <button onClick={onSuivant} style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px 32px", cursor:"pointer", boxShadow:"5px 5px 0 #222" }}>
          Suivant → 🍽️
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
      <div style={{ position:"absolute", inset:0 }}>
        <img src="/cuisine2.png" alt="" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      </div>

      {/* Header */}
      <div style={{ position:"relative", zIndex:10, background:"#74b87a", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"center", boxShadow:"0 3px 0 #222" }}>
        <button onClick={onBack} style={{ position:"absolute", left:16, background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"5px 14px" }}>← Retour</button>
        <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>🌟 AU PROGRAMME</span>
      </div>

      <div style={{ position:"relative", zIndex:5, display:"grid", gridTemplateColumns:"220px 1fr", height:"calc(100vh - 52px)", padding:"16px", gap:16, overflow:"hidden" }}>

        {/* Gauche : Max + Avatar */}
        <div style={{ display:"flex", flexDirection:"column", justifyContent:"space-between" }}>
          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"16px 16px 16px 4px", padding:"12px 14px", boxShadow:"4px 4px 0 rgba(0,0,0,0.4)", fontSize:13, fontWeight:700, color:"#222", lineHeight:1.65 }}>
              Super travail ! 🎉<br/>
              Grâce à tes réponses, je peux te proposer des <strong style={{ color:"#FA8072" }}>recommandations</strong> et des <strong style={{ color:"#9ACD32" }}>recettes</strong> 100% adaptées à toi !<br/>
              <span style={{ fontSize:12, color:"#888" }}>Prêt(e) à découvrir tout ça ?</span>
            </div>
            <img src="/e.png" alt="Max" style={{ width:160, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"#FA8072", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222", alignSelf:"center" }}>Max</div>
          </div>

          <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-start", gap:6 }}>
            <img src={avatarSrc} alt="Joueur" style={{ width:110, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.4))" }} />
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"4px 16px 16px 16px", padding:"10px 12px", boxShadow:"3px 3px 0 rgba(0,0,0,0.4)", fontSize:12, fontWeight:700, color:"#222", lineHeight:1.5 }}>
              Ouiii ! J'ai hâte de voir mes recommandations ! 😍
            </div>
          </div>
        </div>

        {/* Droite : panneau programme */}
        <div style={{ display:"flex", flexDirection:"column", justifyContent:"center", gap:16 }}>
          <div style={{ background:"rgba(15,15,15,0.88)", borderRadius:20, border:"3px solid #ffcc00", padding:"24px", boxShadow:"0 8px 32px rgba(0,0,0,0.6)" }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:"#ffcc00", textAlign:"center", marginBottom:20, textTransform:"uppercase", letterSpacing:1 }}>
              🗒️ Au programme :
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>
              <div onClick={onVoirRecos}
                style={{ background:"rgba(255,255,255,0.08)", border:"3px solid #FA8072", borderRadius:16, padding:"24px 16px", textAlign:"center", cursor:"pointer" }}
                onMouseEnter={e=>e.currentTarget.style.background="rgba(250,128,114,0.15)"}
                onMouseLeave={e=>e.currentTarget.style.background="rgba(255,255,255,0.08)"}>
                <img src="/legume2.png" alt="" style={{ width:64, height:64, objectFit:"contain", marginBottom:12, filter:"drop-shadow(2px 4px 6px rgba(0,0,0,0.3))" }} />
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#FA8072", marginBottom:8 }}>RECOMMANDATIONS PERSONNALISÉES</div>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.75)", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil</div>
              </div>
              <div onClick={onVoirRecettes}
                style={{ background:"rgba(255,255,255,0.08)", border:"3px solid #9ACD32", borderRadius:16, padding:"24px 16px", textAlign:"center", cursor:"pointer" }}
                onMouseEnter={e=>e.currentTarget.style.background="rgba(154,205,50,0.15)"}
                onMouseLeave={e=>e.currentTarget.style.background="rgba(255,255,255,0.08)"}>
                <img src="/salade_grecque.png" alt="" style={{ width:64, height:64, objectFit:"contain", marginBottom:12, filter:"drop-shadow(2px 4px 6px rgba(0,0,0,0.3))" }} />
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#9ACD32", marginBottom:8 }}>RECETTES PERSONNALISÉES</div>
                <div style={{ fontSize:11, color:"rgba(255,255,255,0.75)", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
              </div>
            </div>
          </div>

          <button onClick={onVoirRecos}
            style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"5px 5px 0 #222", textAlign:"center" }}>
            ✨ Clique ici pour découvrir tes recommandations et recettes !
          </button>

          {/* Barre progression */}
          <div style={{ display:"flex", alignItems:"center", justifyContent:"center", gap:0 }}>
            {[
              { label:"QCM 1", done:true },
              { label:"QCM 2", done:true },
              { label:"Profil", done:true },
              { label:"Recos", done:false, active:true },
              { label:"Recettes", done:false },
            ].map((step, i, arr) => (
              <div key={i} style={{ display:"flex", alignItems:"center" }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:4 }}>
                  <div style={{ width:34, height:34, borderRadius:"50%", background:step.done?"#9ACD32":step.active?"#FA8072":"rgba(255,255,255,0.25)", border:"3px solid #222", display:"flex", alignItems:"center", justifyContent:"center", fontSize:14, color:"white", fontWeight:900, boxShadow:"2px 2px 0 #222" }}>
                    {step.done ? "✓" : step.active ? "●" : "○"}
                  </div>
                  <div style={{ fontSize:10, fontWeight:800, color:step.done?"#9ACD32":step.active?"#FA8072":"rgba(255,255,255,0.5)", whiteSpace:"nowrap" }}>{step.label}</div>
                </div>
                {i < arr.length-1 && <div style={{ width:40, height:3, background:step.done?"#9ACD32":"rgba(255,255,255,0.2)", margin:"0 4px", marginBottom:16 }} />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

'''

code = before + NEW_BOTH + after
out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ FIX 1 — ProfilQcm2Screen + IntroRecosQcm2Screen refaits")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
