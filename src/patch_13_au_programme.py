"""
PATCH 13 — Ajouter IntroRecosQcm2Screen (page "Au programme") 
et corriger ProfilQcm2Screen pour rediriger vers au_programme
Usage: python patch_13_au_programme.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# FIX 1 — Ajouter IntroRecosQcm2Screen avant /* ══ SÉLECTION QCM ══ */
MARKER = "/* ══ SÉLECTION QCM ══ */"

NEW_SCREEN = '''/* ══ PAGE AU PROGRAMME QCM2 ══ */
function IntroRecosQcm2Screen({ answers, playerName, avatarChoice, onBack, onVoirRecos, onVoirRecettes }) {
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
              <span style={{ fontSize:13, fontWeight:600, color:"#555" }}>Tes recommandations et recettes sont personnalisées en fonction de tes habitudes alimentaires et tes préférences.</span>
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
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#e8f5e9", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center", fontSize:28 }}>📋</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#639922", marginBottom:6 }}>Recommandations personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil alimentaire</div>
          </div>
          <div style={{ background:"white", border:"2px solid #FA807266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#fff0ee", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center", fontSize:28 }}>🍽️</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#c4622d", marginBottom:6 }}>Recettes personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
          </div>
        </div>

        {/* Bouton principal */}
        <button onClick={onVoirRecos}
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
          <div style={{ flex:1, display:"flex", alignItems:"center", justifyContent:"flex-end", gap:2 }}>
            {STEPS.map((s, i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:2 }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:2 }}>
                  <div style={{ width:22, height:22, borderRadius:"50%", background:i<3?"#9ACD32":i===3?"#FA8072":"#eee", border:"2px solid "+(i<3?"#639922":i===3?"#c4622d":"#ddd"), display:"flex", alignItems:"center", justifyContent:"center" }}>
                    {i < 2 ? <span style={{ fontSize:10, color:"white" }}>✓</span> : <div style={{ width:6, height:6, borderRadius:"50%", background:i===2?"white":i===3?"white":"#ccc" }} />}
                  </div>
                  <div style={{ fontSize:8, color:"#888", whiteSpace:"nowrap" }}>{s}</div>
                </div>
                {i < STEPS.length-1 && <div style={{ width:10, height:1.5, background:"#ddd", marginBottom:10 }} />}
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
    code = code.replace(MARKER, NEW_SCREEN + MARKER)
    fixes += 1
    print("✅ FIX 1 — IntroRecosQcm2Screen ajouté")
else:
    print("⚠️  FIX 1 — Marqueur non trouvé")

# FIX 2 — Corriger ProfilQcm2Screen : onSuivant → au_programme
# Ligne 5537 dans l'original redirige vers intro_recos_qcm2, c'est déjà le bon nom
# Mais ProfilQcm2Screen appelle onSuivant(() => goTo("intro_recos_qcm2"))
# Vérifions si c'est déjà correct
OLD_PROFIL_SUIVANT = 'onSuivant={() => goTo("intro_recos_qcm2")}'
if OLD_PROFIL_SUIVANT in code:
    print("✅ FIX 2 — ProfilQcm2Screen → intro_recos_qcm2 déjà correct")
    fixes += 1
else:
    OLD2 = 'onSuivant={() => goTo("au_programme")}'
    NEW2 = 'onSuivant={() => goTo("intro_recos_qcm2")}'
    if OLD2 in code:
        code = code.replace(OLD2, NEW2)
        fixes += 1
        print("✅ FIX 2 — Redirection corrigée vers intro_recos_qcm2")
    else:
        print("⚠️  FIX 2 — onSuivant non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/2 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
