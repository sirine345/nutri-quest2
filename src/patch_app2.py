#!/usr/bin/env python3
"""
Script de patch 2 pour App.jsx — nutri-quest2
Corrections: boutons retour, liens CB/CM, page profil, scène Max santé
Usage: python patch_app2.py
Place ce fichier dans C:\\Users\\fzahi\\Desktop\\nutri-quest2\\src\\
"""
import sys, os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
if not os.path.exists(src):
    print(f"ERREUR: App.jsx introuvable dans {os.path.dirname(__file__)}")
    sys.exit(1)

with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} caractères depuis App.jsx")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        result = code.replace(old, new, 1)
        fixes += 1
        print(f"  ✅ {name}")
        return result
    else:
        errors.append(name)
        print(f"  ⚠️  Non trouvé: {name}")
        return code

def p_all(code, old, new, name):
    """Replace all occurrences"""
    global fixes
    count = code.count(old)
    if count > 0:
        result = code.replace(old, new)
        fixes += 1
        print(f"  ✅ {name} ({count} occurrences)")
        return result
    else:
        errors.append(name)
        print(f"  ⚠️  Non trouvé: {name}")
        return code

print("\n=== Application des patches ===\n")

# ─── 1. Corriger liens CB et CM (404 → lien HAS qui marche) ───
code = p_all(code,
    'href="https://www.sfncm.org/images/stories/docs/MNA/MNA_french.pdf"',
    'href="https://www.has-sante.fr/jcms/c_1179700/fr/evaluation-diagnostique-de-la-denutrition-proteino-energetique-des-adultes-hospitalises"',
    "1. Liens CB/CM → HAS")

# ─── 2. Texte des liens CB/CM ───
code = p_all(code,
    '>📎 Guide de mesure CB — SFNCM (source officielle)</a>',
    '>📎 Comment mesurer la CB ? — Haute Autorité de Santé</a>',
    "2a. Texte lien CB")
code = p_all(code,
    '>📎 Guide de mesure mollet — SFNCM (source officielle)</a>',
    '>📎 Comment mesurer le mollet ? — Haute Autorité de Santé</a>',
    "2b. Texte lien CM")

# ─── 3. Boutons "← Retour" dans QCM2 — texte manquant ───
# Le problème vient du btn style color:"white" — le texte est blanc sur fond blanc
# On garde le style mais on s'assure que les boutons retour sont bien visibles
# Remplacer tous les boutons retour dans Qcm2Screen par un style visible
code = p_all(code,
    'style={{ ...btn, background:"white" }}>← Retour</button>',
    'style={{ ...btn, background:"white", color:"#333", border:"3px solid #ccc" }}>← Retour</button>',
    "3. Boutons Retour visibles")

# ─── 4. Ajouter la scène Max → QCM Santé dans SCENES_BY_NODE ───
# Ajouter une scène de transition dans la cuisine
old_scenes = '''const SCENES_BY_NODE = {
  0: [
    { bg: "exterior", speaker: "narrator", text: "Une ville animée. Fast-foods et marchés se côtoient. L'alimentation de toute une génération est en jeu..." },
    { bg: "exterior", speaker: "narrator", text: "Un message sur ton téléphone : Rejoins-moi. Ta cuisine, 14h. — Max" },
  ],
  1: [
    { bg: "kitchen", speaker: "max", text: "Ah, tu es là ! Je m'appelle Max, coach nutrition. J'ai besoin de toi." },
    { bg: "kitchen", speaker: "max", text: "Cette cuisine cache des secrets. Chaque aliment a un impact sur ton corps." },
    { bg: "kitchen", speaker: "player", text: "..." },
    { bg: "kitchen", speaker: "max", text: "Ce n'est pas un cours. Ici, on joue. Et chaque choix compte." },
  ],'''

new_scenes = '''const SCENES_BY_NODE = {
  0: [
    { bg: "exterior", speaker: "narrator", text: "Une ville animée. Fast-foods et marchés se côtoient. L'alimentation de toute une génération est en jeu..." },
    { bg: "exterior", speaker: "narrator", text: "Un message sur ton téléphone : Rejoins-moi. Ta cuisine, 14h. — Max" },
  ],
  1: [
    { bg: "kitchen", speaker: "max", text: "Ah, tu es là ! Je m'appelle Max, coach nutrition. J'ai besoin de toi." },
    { bg: "kitchen", speaker: "max", text: "Cette cuisine cache des secrets. Chaque aliment a un impact sur ton corps." },
    { bg: "kitchen", speaker: "player", text: "..." },
    { bg: "kitchen", speaker: "max", text: "Ce n'est pas un cours. Ici, on joue. Et chaque choix compte." },
  ],'''

# Les scènes sont déjà bien — on va plutôt ajouter une scène "sante" déclenchée avant QcmSanteScreen
code = p(code, old_scenes, new_scenes, "4. Scènes (inchangées)")

# ─── 5. Ajouter SceneSanteScreen — Max dans la cuisine invite au profil santé ───
# On insère ce composant juste avant QcmSanteScreen
INSERT_BEFORE = '/* ══ QCM SANTÉ ══ */'
SCENE_SANTE = '''/* ══ SCÈNE TRANSITION → PROFIL SANTÉ ══ */
function SceneSanteScreen({ playerName, avatarChoice, onStart }) {
  const [phase, setPhase] = useState(0);
  const avatarSrc = avatarChoice === "garcon" ? "/garcon.png" : "/fille.png";

  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 300);
    const t2 = setTimeout(() => setPhase(2), 1200);
    const t3 = setTimeout(() => setPhase(3), 2200);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, []);

  const dialogues = [
    { text: `${playerName}, viens ! J'ai encore besoin de toi dans la cuisine.`, delay: 1200 },
    { text: "Pour te donner des conseils vraiment personnalisés, j'ai besoin d'en savoir plus sur toi.", delay: 2200 },
    { text: "Quelques questions sur ta santé et ton mode de vie. Promis, c'est rapide !", delay: 3200 },
  ];
  const [dialogueIdx, setDialogueIdx] = useState(0);
  useEffect(() => {
    if (phase < 2) return;
    const timers = dialogues.map((d, i) =>
      setTimeout(() => setDialogueIdx(i), (i) * 1800)
    );
    return () => timers.forEach(clearTimeout);
  }, [phase]);

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      {/* Fond cuisine */}
      <div style={{ position:"absolute", inset:0 }}>
        <img src="/cuisine2.png" alt="cuisine" style={{ width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.25)" }} />
      </div>

      {/* Personnage joueur à gauche (petit) */}
      <div style={{
        position:"absolute", bottom:0, left:"2%",
        width:300, height:500,
        opacity: phase >= 1 ? 1 : 0,
        transform: phase >= 1 ? "translateX(0)" : "translateX(-60px)",
        transition:"all 0.8s cubic-bezier(0.34,1.56,0.64,1)",
        filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))"
      }}>
        <img src={avatarSrc} style={{ width:"100%", height:"100%", objectFit:"contain" }} alt="Joueur" />
      </div>

      {/* Max GRAND à droite */}
      <div style={{
        position:"absolute", bottom:0, right:"-2%",
        width:680, height:900,
        opacity: phase >= 1 ? 1 : 0,
        transform: phase >= 1 ? "translateX(0)" : "translateX(80px)",
        transition:"all 0.8s cubic-bezier(0.34,1.56,0.64,1) 0.2s",
        filter:"drop-shadow(6px 6px 0 rgba(0,0,0,0.35))"
      }}>
        <img src="/e.png" alt="Max" style={{ width:"100%", height:"100%", objectFit:"contain", objectPosition:"top" }} />
      </div>

      {/* Bulle dialogue Max */}
      <div style={{
        position:"absolute", bottom:"55%", right:"38%",
        maxWidth:420, zIndex:10,
        opacity: phase >= 2 ? 1 : 0,
        transform: phase >= 2 ? "translateY(0) scale(1)" : "translateY(20px) scale(0.9)",
        transition:"all 0.5s cubic-bezier(0.34,1.56,0.64,1)",
      }}>
        <div style={{
          background:"#fff8f0", border:"3px solid #222",
          borderRadius:"20px 20px 4px 20px",
          padding:"18px 22px", boxShadow:"5px 5px 0 rgba(0,0,0,0.25)"
        }}>
          <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
          <p style={{ margin:0, fontSize:15, color:"#222", lineHeight:1.7, fontWeight:600, minHeight:48 }}>
            {dialogues[dialogueIdx]?.text || dialogues[0].text}
          </p>
        </div>
        {/* Indicateur dots */}
        <div style={{ display:"flex", gap:6, marginTop:8, justifyContent:"flex-end" }}>
          {dialogues.map((_, i) => (
            <div key={i} style={{ width:8, height:8, borderRadius:"50%", background: i === dialogueIdx ? "#c4622d" : "rgba(255,255,255,0.5)", border:"2px solid rgba(255,255,255,0.7)", transition:"background 0.3s" }} />
          ))}
        </div>
      </div>

      {/* Bouton */}
      <div style={{
        position:"absolute", bottom:40, left:"50%", transform:"translateX(-50%)",
        opacity: phase >= 3 ? 1 : 0,
        transition:"opacity 0.5s ease",
        zIndex:20
      }}>
        <button onClick={onStart}
          style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontSize:18, fontWeight:900, padding:"18px 48px", cursor:"pointer", boxShadow:"5px 5px 0 #222", letterSpacing:0.5, whiteSpace:"nowrap" }}
          onMouseEnter={e=>{ e.currentTarget.style.transform="translateY(-3px)"; e.currentTarget.style.boxShadow="7px 7px 0 #222"; }}
          onMouseLeave={e=>{ e.currentTarget.style.transform="translateY(0)"; e.currentTarget.style.boxShadow="5px 5px 0 #222"; }}>
          Compléter mon profil santé →
        </button>
      </div>

      {/* Label */}
      <div style={{ position:"absolute", top:20, left:"50%", transform:"translateX(-50%)", background:"rgba(196,98,45,0.9)", borderRadius:20, padding:"6px 20px", fontSize:13, fontWeight:800, color:"white", letterSpacing:1, zIndex:20, whiteSpace:"nowrap" }}>
        🏥 Profil Santé
      </div>
    </div>
  );
}

/* ══ QCM SANTÉ ══ */'''

code = p(code, INSERT_BEFORE, SCENE_SANTE, "5. SceneSanteScreen ajoutée")

# ─── 6. Ajouter phase "scene_sante" dans App() ───
# Dans le switch des phases, ajouter la scène santé avant le QCM santé
old_phase = '    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setPhase("select"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;'
new_phase = '''    if (phase === "scene_sante") return <SceneSanteScreen playerName={playerName} avatarChoice={avatarChoice} onStart={() => { setPhaseHistory(h => [...h, "scene_sante"]); setPhase("qcm_sante"); }} />;
    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setPhase("profil_final"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;'''
code = p(code, old_phase, new_phase, "6. Phase scene_sante dans App")

# ─── 7. QCM2 → "Continuer vers mon profil santé" déclenche scene_sante ───
old_sante_btn = 'else if(cuisine==="sante") goTo("qcm_sante");'
new_sante_btn = 'else if(cuisine==="sante") goTo("scene_sante");'
code = p(code, old_sante_btn, new_sante_btn, "7. QCM2 → scene_sante")

# ─── 8. Ajouter ProfilFinalScreen — personnage gauche + réponses droite ───
INSERT_BEFORE_APP = '/* ══ APP ══ */'
PROFIL_SCREEN = '''/* ══ PAGE PROFIL FINAL ══ */
function ProfilFinalScreen({ playerName, playerInfos, santeData, qcm1Nutrition, qcm2Answers, avatarChoice, onVoirRecos, onBack }) {
  const avatarSrc = avatarChoice === "garcon" ? "/garcon.png" : "/fille.png";
  const [tab, setTab] = useState("profil"); // "profil" | "recos"

  const qcm1Items = qcm1Nutrition ? Object.entries(qcm1Nutrition).map(([k,v]) => ({
    label: k, score: v,
    color: v >= 60 ? "#2e7d32" : v >= 30 ? "#f57c00" : "#e53935",
    bg: v >= 60 ? "#e8f5e9" : v >= 30 ? "#fff8e1" : "#fbe9e7",
  })) : [];

  return (
    <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>
      {/* Header */}
      <div style={{ background:"#1A3A5C", padding:"14px 20px", display:"flex", alignItems:"center", gap:12, flexShrink:0 }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"1px solid rgba(255,255,255,0.3)", borderRadius:10, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour</button>
        <h1 style={{ fontSize:20, fontWeight:900, color:"white", margin:0 }}>Mon Profil Complet</h1>
        <div style={{ marginLeft:"auto", display:"flex", gap:8 }}>
          {[["profil","👤 Mon Profil"],["recos","💡 Recommandations"]].map(([id,label]) => (
            <button key={id} onClick={()=>setTab(id)}
              style={{ padding:"8px 16px", fontSize:12, fontWeight:800, border:"none", borderRadius:20, cursor:"pointer", background:tab===id?"white":"rgba(255,255,255,0.15)", color:tab===id?"#1A3A5C":"white", transition:"all 0.15s" }}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Contenu */}
      {tab === "profil" && (
        <div style={{ flex:1, display:"grid", gridTemplateColumns:"1fr 1fr", overflow:"hidden" }}>
          {/* Gauche — Personnage */}
          <div style={{ background:"linear-gradient(135deg, #1A3A5C 0%, #2d5a8e 100%)", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"flex-end", position:"relative", overflow:"hidden" }}>
            {/* Fond décoratif */}
            <div style={{ position:"absolute", inset:0, background:"url('/cuisine2.png') center/cover", opacity:0.15 }} />
            {/* Nom */}
            <div style={{ position:"absolute", top:24, left:0, right:0, textAlign:"center", zIndex:2 }}>
              <div style={{ fontSize:28, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.3)" }}>{playerName}</div>
              {santeData?.age && <div style={{ fontSize:14, color:"rgba(255,255,255,0.7)", marginTop:4 }}>{santeData.age} · {santeData.sexe || ""}</div>}
              <div style={{ display:"flex", gap:8, justifyContent:"center", marginTop:12, flexWrap:"wrap", padding:"0 20px" }}>
                {santeData?.modeVie && <span style={{ background:"rgba(255,255,255,0.2)", borderRadius:20, padding:"4px 12px", fontSize:11, color:"white", fontWeight:700 }}>{santeData.modeVie}</span>}
                {santeData?.pathologies?.length > 0 && !santeData.pathologies.includes("Aucune") && santeData.pathologies.map(p => (
                  <span key={p} style={{ background:"rgba(250,128,114,0.4)", borderRadius:20, padding:"4px 12px", fontSize:10, color:"white", fontWeight:700 }}>{p}</span>
                ))}
              </div>
            </div>
            {/* Avatar grand */}
            <img src={avatarSrc} alt={playerName}
              style={{ width:"80%", maxWidth:340, position:"relative", zIndex:2, filter:"drop-shadow(8px 8px 0 rgba(0,0,0,0.4))" }} />
          </div>

          {/* Droite — Réponses */}
          <div style={{ overflowY:"auto", padding:"20px" }}>
            {/* QCM1 scores */}
            {qcm1Items.length > 0 && (
              <div style={{ background:"white", borderRadius:16, padding:"18px", marginBottom:14, boxShadow:"0 2px 10px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#1A3A5C", marginBottom:12, textTransform:"uppercase", letterSpacing:1 }}>📊 Habitudes alimentaires</div>
                <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
                  {qcm1Items.slice(0,8).map(item => (
                    <div key={item.label} style={{ display:"flex", alignItems:"center", gap:10 }}>
                      <div style={{ fontSize:11, color:"#888", width:100, flexShrink:0, textTransform:"capitalize" }}>{item.label}</div>
                      <div style={{ flex:1, height:8, background:"#f0f0f0", borderRadius:99, overflow:"hidden" }}>
                        <div style={{ height:"100%", width:`${item.score}%`, background:item.color, borderRadius:99, transition:"width 0.5s" }} />
                      </div>
                      <div style={{ fontSize:11, fontWeight:800, color:item.color, width:32, textAlign:"right" }}>{item.score}%</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Profil santé */}
            {santeData && Object.keys(santeData).length > 0 && (
              <div style={{ background:"white", borderRadius:16, padding:"18px", marginBottom:14, boxShadow:"0 2px 10px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#1A3A5C", marginBottom:12, textTransform:"uppercase", letterSpacing:1 }}>🏥 Profil Santé</div>
                {[
                  ["Âge", santeData.age],
                  ["Sexe", santeData.sexe],
                  ["Mode de vie", santeData.modeVie],
                  ["Vie seul(e)", santeData.seul],
                  ["Autonomie", santeData.autonomie],
                  ["Traitement", santeData.traitement],
                  ["Régime prescrit", santeData.regimePrescrit],
                ].filter(([,v]) => v).map(([k,v]) => (
                  <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                    <span style={{ color:"#888" }}>{k}</span>
                    <span style={{ fontWeight:700, color:"#333" }}>{v}</span>
                  </div>
                ))}
                {santeData.pathologies?.length > 0 && !santeData.pathologies.includes("Aucune") && (
                  <div style={{ marginTop:10, display:"flex", flexWrap:"wrap", gap:6 }}>
                    {santeData.pathologies.map(p => (
                      <span key={p} style={{ background:"#fbe9e7", border:"1px solid #e53935", borderRadius:20, padding:"3px 10px", fontSize:11, color:"#e53935", fontWeight:700 }}>{p}</span>
                    ))}
                  </div>
                )}
                {santeData.medasResult && (
                  <div style={{ marginTop:12, background: santeData.medasResult.score >= 10 ? "#e8f5e9" : "#fff8e1", borderRadius:10, padding:"10px 12px" }}>
                    <div style={{ fontSize:12, fontWeight:800, color: santeData.medasResult.score >= 10 ? "#2e7d32" : "#f57c00" }}>
                      🫒 Score MEDAS : {santeData.medasResult.score}/14 — {santeData.medasResult.score >= 10 ? "Forte adhésion méditerranéen" : "Adhésion modérée"}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* QCM2 */}
            {qcm2Answers && Object.keys(qcm2Answers).length > 0 && (
              <div style={{ background:"white", borderRadius:16, padding:"18px", marginBottom:14, boxShadow:"0 2px 10px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#1A3A5C", marginBottom:12, textTransform:"uppercase", letterSpacing:1 }}>🍽 Fabrique à Menus</div>
                {Object.entries(qcm2Answers).filter(([k]) => !k.includes("mna")).map(([k,v]) => (
                  <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"8px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                    <span style={{ color:"#888", fontSize:12 }}>{k.trim()}</span>
                    <span style={{ fontWeight:700, color:"#333", fontSize:12, maxWidth:"55%", textAlign:"right" }}>{String(v)}</span>
                  </div>
                ))}
              </div>
            )}

            <button onClick={onVoirRecos}
              style={{ background:"#FA8072", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer", width:"100%", boxShadow:"0 4px 16px rgba(250,128,114,0.35)" }}>
              Voir mes recommandations →
            </button>
          </div>
        </div>
      )}

      {/* Onglet Recommandations */}
      {tab === "recos" && (
        <div style={{ flex:1, overflowY:"auto", padding:"20px", maxWidth:700, margin:"0 auto", width:"100%" }}>
          <div style={{ textAlign:"center", marginBottom:24 }}>
            <div style={{ fontSize:22, fontWeight:900, color:"#1A3A5C", marginBottom:6 }}>💡 Vos recommandations personnalisées</div>
            <div style={{ fontSize:14, color:"#888" }}>Basées sur l'ensemble de vos réponses</div>
          </div>
          {/* Recommandations QCM1 */}
          {qcm1Nutrition && (
            <div style={{ background:"white", borderRadius:16, padding:"20px", marginBottom:16, boxShadow:"0 2px 10px rgba(0,0,0,0.06)" }}>
              <div style={{ fontSize:14, fontWeight:900, color:"#00897B", marginBottom:12 }}>🥗 Habitudes alimentaires</div>
              {(qcm1Nutrition.legumes||0) < 60 && <div style={{ fontSize:13, color:"#555", padding:"8px 0", borderBottom:"1px solid #f5f5f5" }}>• Augmentez votre consommation de <strong>légumes et fruits</strong> (objectif : 5/jour)</div>}
              {(qcm1Nutrition.legumineuses||0) < 50 && <div style={{ fontSize:13, color:"#555", padding:"8px 0", borderBottom:"1px solid #f5f5f5" }}>• Mangez plus de <strong>légumineuses</strong> (lentilles, pois chiches…) — 2x/semaine</div>}
              {(qcm1Nutrition.poisson||0) < 50 && <div style={{ fontSize:13, color:"#555", padding:"8px 0", borderBottom:"1px solid #f5f5f5" }}>• Consommez <strong>du poisson</strong> au moins 2 fois par semaine</div>}
              {(qcm1Nutrition.charcuterie||0) > 20 && <div style={{ fontSize:13, color:"#e53935", padding:"8px 0", borderBottom:"1px solid #f5f5f5" }}>• Réduisez la <strong>charcuterie</strong> (max 150g/semaine — cancérigène OMS groupe 1)</div>}
              {(qcm1Nutrition.fastFood||0) > 20 && <div style={{ fontSize:13, color:"#e53935", padding:"8px 0", borderBottom:"1px solid #f5f5f5" }}>• Limitez le <strong>fast food</strong> (ultra-transformés liés à l'obésité)</div>}
              {(qcm1Nutrition.sucres||0) > 20 && <div style={{ fontSize:13, color:"#f57c00", padding:"8px 0" }}>• Réduisez les <strong>sucreries</strong> (risque diabète de type 2)</div>}
            </div>
          )}
          {/* Recommandations santé */}
          {santeData?.modeVie === "Sédentaire" && (
            <div style={{ background:"#fff8e1", borderRadius:16, padding:"20px", marginBottom:16, border:"2px solid #f57c00" }}>
              <div style={{ fontSize:14, fontWeight:900, color:"#e65100", marginBottom:8 }}>🏃 Activité physique</div>
              <div style={{ fontSize:13, color:"#555", lineHeight:1.7 }}>Mode de vie sédentaire détecté. L'OMS recommande 150 min d'activité modérée par semaine. Commencez par 10 min de marche par jour !</div>
            </div>
          )}
          {santeData?.medasResult && santeData.medasResult.score < 10 && (
            <div style={{ background:"#e8f5e9", borderRadius:16, padding:"20px", marginBottom:16, border:"2px solid #4caf50" }}>
              <div style={{ fontSize:14, fontWeight:900, color:"#2e7d32", marginBottom:8 }}>🫒 Régime méditerranéen (MEDAS)</div>
              <div style={{ fontSize:13, color:"#555", lineHeight:1.7 }}>Score MEDAS de {santeData.medasResult.score}/14. Pour améliorer votre adhésion : huile d'olive en priorité, plus de poisson, légumineuses 3x/sem, fruits à coque quotidien.</div>
            </div>
          )}
          <div style={{ background:"#E0F7F5", borderRadius:16, padding:"20px", border:"1px solid #00BFA5" }}>
            <div style={{ fontSize:14, fontWeight:900, color:"#00897B", marginBottom:8 }}>🫒 Le régime méditerranéen</div>
            <div style={{ fontSize:13, color:"#555", lineHeight:1.7, marginBottom:12 }}>Fruits, légumes, légumineuses, poisson et huile d'olive — reconnu pour réduire les risques cardiovasculaires et favoriser la longévité.</div>
            <button onClick={()=>{ if(typeof onVoirRecos==="function") onVoirRecos("recettes"); }}
              style={{ background:"#00BFA5", border:"none", borderRadius:10, color:"white", fontSize:13, fontWeight:800, padding:"10px 20px", cursor:"pointer", width:"100%" }}>
              🍳 Voir les recettes recommandées →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══ APP ══ */'''

code = p(code, INSERT_BEFORE_APP, PROFIL_SCREEN, "8. ProfilFinalScreen ajouté")

# ─── 9. Ajouter phase "profil_final" dans App() ───
old_app_phases = '    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'
new_app_phases = '''    if (phase === "profil_final") return <ProfilFinalScreen
      playerName={playerName} playerInfos={playerInfos} santeData={santeData}
      qcm1Nutrition={qcm1Nutrition} qcm2Answers={qcm2Answers} avatarChoice={avatarChoice}
      onVoirRecos={(type) => { if(type==="recettes") goTo("recettes"); else goTo("recos_qcm1"); }}
      onBack={() => goBack()}
    />;
    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'''
code = p(code, old_app_phases, new_app_phases, "9. Phase profil_final dans App")

# ─── 10. QCM Santé onDone → profil_final ───
code = p(code,
    'onDone={(data) => { setSanteData(data); setPhase("profil_final"); setPhaseHistory([]); }}',
    'onDone={(data) => { setSanteData(data); goTo("profil_final"); }}',
    "10. QCM Santé → profil_final")

# ─── 11. QCM1 → profil_final aussi après recos ───
# Ajouter accès profil depuis QCM1 résultats
code = p(code,
    '          <button onClick={() => { if(onShowRecos) onShowRecos(nutrition); }} style={{ ...btn, background:"#2e7d32", color:"white", border:"3px solid #1b5e20" }}> Mes recommandations PNNS →</button>',
    '''          <button onClick={() => { if(onShowRecos) onShowRecos(nutrition); }} style={{ ...btn, background:"#2e7d32", color:"white", border:"3px solid #1b5e20" }}> Mes recommandations PNNS →</button>
          <button onClick={() => { if(onDone) onDone(nutrition); if(onBack) { setTimeout(()=>{ }, 100); } }} style={{ ...btn, background:"#1A3A5C", color:"white", border:"3px solid #0d2340" }}>👤 Voir mon profil →</button>''',
    "11. Bouton profil depuis QCM1")

# ═══ RÉSULTAT ═══
print(f"\n{'='*50}")
print(f"Patches appliqués: {fixes}")
if errors:
    print(f"Non trouvés ({len(errors)}): {', '.join(errors)}")
print(f"Taille sortie: {len(code)} caractères")

out_path = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx écrit avec succès !")
