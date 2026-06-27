#!/usr/bin/env python3
"""
Script de patch 3 — nutri-quest2
Corrections ciblées et précises
"""
import sys, os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} caractères")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        result = code.replace(old, new, 1)
        fixes += 1
        print(f"  ✅ {name}")
        return result
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    # Debug
    words = old.strip()[:40]
    idx = code.find(words)
    if idx > 0:
        print(f"     Partiel à {idx}: {code[idx:idx+80]!r}")
    return code

def p_all(code, old, new, name):
    global fixes
    n = code.count(old)
    if n > 0:
        result = code.replace(old, new)
        fixes += 1
        print(f"  ✅ {name} ({n}x)")
        return result
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

print("\n=== Patches ===\n")

# ══════════════════════════════════════════════
# FIX 1 — QCM2 step 1: bouton retour invisible
# Le bouton a opacity:0.4 ET color:"white" → texte blanc invisible
# ══════════════════════════════════════════════
code = p(code,
    '<button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>',
    '<button onClick={onBack} style={{ ...btn, background:"#f5f5f5", color:"#aaa", border:"3px solid #ddd" }}>← Retour</button>',
    "1. QCM2 step1 bouton retour visible")

# ══════════════════════════════════════════════
# FIX 2 — Liens CB et CM: dictionnaire médical
# ══════════════════════════════════════════════
code = p_all(code,
    'href="https://www.has-sante.fr/jcms/c_1179700/fr/evaluation-diagnostique-de-la-denutrition-proteino-energetique-des-adultes-hospitalises"',
    'href="https://www.larousse.fr/encyclopedie/medical/circonférence_brachiale/12491"',
    "2a. CB lien Larousse médical")

# Différencier CB et CM maintenant
code = p(code,
    '>📎 Comment mesurer la CB ? — Haute Autorité de Santé</a>',
    '>📎 Définition circonférence brachiale — Dictionnaire médical Larousse</a>',
    "2b. CB texte lien")

code = p(code,
    '>📎 Comment mesurer le mollet ? — Haute Autorité de Santé</a>',
    '>📎 Définition circonférence du mollet — Dictionnaire médical Larousse</a>',
    "2c. CM texte lien")

# Corriger le lien CM (même URL que CB pour l'instant, on met un lien différent)
code = p(code,
    '>📎 Définition circonférence du mollet — Dictionnaire médical Larousse</a>',
    '>📎 Définition circonférence du mollet — Dictionnaire médical Vidal</a>',
    "2d. CM texte lien Vidal")

# Changer le href du CM
code = p(code,
    'href="https://www.larousse.fr/encyclopedie/medical/circonférence_brachiale/12491" target="_blank" rel="noopener noreferrer" style={{ color:"#7b1fa2", textDecoration:"underline", fontStyle:"italic" }}>📎 Définition circonférence du mollet — Dictionnaire médical Vidal</a>',
    'href="https://www.vidal.fr/maladies/muscles-os-articulations/sarcopenie/definition.html" target="_blank" rel="noopener noreferrer" style={{ color:"#7b1fa2", textDecoration:"underline", fontStyle:"italic" }}>📎 Définition circonférence du mollet — Dictionnaire médical Vidal</a>',
    "2e. CM href Vidal")

# ══════════════════════════════════════════════
# FIX 3 — Supprimer la page "Profil créé !" de Qcm2Screen
# et la remplacer par la navigation directe vers ProfilFinalScreen
# ══════════════════════════════════════════════
# La page "done" actuelle dans Qcm2Screen renvoie vers onDone
# Le problème : goBack() depuis recos revient au QCM2
# Solution : dans App, quand onDone de Qcm2Screen est appelé avec "sante",
# on va vers scene_sante. Depuis ProfilFinalScreen le retour va vers "select"

# Corriger goBack dans RecommandationsQcm1Screen et Qcm2Screen
# pour ne pas revenir au début du QCM
code = p(code,
    '    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;',
    '    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => setPhase("select")} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;',
    "3a. recos_qcm1 retour → select")

code = p(code,
    '    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;',
    '    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} onBack={() => setPhase("select")} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;',
    "3b. recos_qcm2 retour → select")

# ══════════════════════════════════════════════
# FIX 4 — Remplacer la page "Profil créé !" (done screen de Qcm2Screen)
# par un redirect direct vers ProfilFinalScreen via onDone
# ══════════════════════════════════════════════
OLD_DONE = '''  if (done) {
    const cuisineVal = answers["‍ En cuisine"];
    const compoVal = answers[" Composition du repas"];
    return (
      <div style={{ position:"fixed", inset:0, background:"#F2F7F2", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        {/* Header Medaviz */}
        <div style={{ background:"#F8FAFC", borderBottom:"1px solid #E8EDF2" }}>
          <div style={{ padding:"14px 20px" }}>
            <button onClick={onBack} style={{ background:"none", border:"1px solid #E8EDF2", borderRadius:10, color:"#1A3A5C", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour</button>
          </div>
          <div style={{ padding:"8px 20px 24px" }}>
            <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#FFF0EB", borderRadius:20, padding:"4px 12px", marginBottom:12 }}>
              <div style={{ width:6, height:6, borderRadius:"50%", background:"#FF6B35" }} />
              <span style={{ fontSize:11, fontWeight:800, color:"#E65100", textTransform:"uppercase", letterSpacing:1 }}>Fabrique à Menus</span>
            </div>
            <h1 style={{ fontSize:28, fontWeight:900, color:"#1A1A1A", margin:"0 0 4px" }}>Profil créé !</h1>
            <p style={{ color:"#6B7280", fontSize:14, margin:0 }}>Récapitulatif de vos préférences alimentaires</p>
          </div>
        </div>

        <div style={{ padding:"20px", display:"flex", flexDirection:"column", gap:14 }}>
          {/* Recap réponses */}
          <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 2px 10px rgba(0,0,0,0.07)" }}>
            <div style={{ background:"#E65100", padding:"14px 18px" }}>
              <div style={{ fontSize:14, fontWeight:900, color:"white" }}>Vos réponses</div>
            </div>
            <div style={{ padding:"16px 18px" }}>
              {Object.entries(answers).map(([k,v])=>(
                <div key={k} style={{ display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 0", borderBottom:"1px solid #F5F5F5" }}>
                  <span style={{ fontSize:13, color:"#888", fontWeight:600 }}>{k}</span>
                  <span style={{ fontSize:13, color:"#333", fontWeight:800, textAlign:"right", maxWidth:"55%" }}>{String(v)}</span>
                </div>
              ))}
              <div style={{ marginTop:14, background:"#FFF8E1", borderRadius:10, padding:"12px 14px", fontSize:13, color:"#E65100", fontWeight:600, lineHeight:1.5 }}>
                💡 Tous les repas de la semaine comptent pour adopter une alimentation équilibrée.
              </div>
            </div>
          </div>

          {/* Actions cards - Medaviz style */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
            <div onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "recos", answers); }}
              style={{ background:"white", borderRadius:20, padding:"20px", border:"1px solid #E8EDF2", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", cursor:"pointer", transition:"box-shadow 0.2s, transform 0.2s" }}
              onMouseEnter={e=>{e.currentTarget.style.boxShadow="0 8px 32px rgba(26,58,92,0.12)";e.currentTarget.style.transform="translateY(-2px)";}}
              onMouseLeave={e=>{e.currentTarget.style.boxShadow="0 2px 16px rgba(26,58,92,0.06)";e.currentTarget.style.transform="translateY(0)";}}>
              <div style={{ width:40, height:40, borderRadius:12, background:"#E0F7F5", marginBottom:12, display:"flex", alignItems:"center", justifyContent:"center" }}>
                <div style={{ width:16, height:16, borderRadius:"50%", background:"#00BFA5" }} />
              </div>
              <div style={{ fontSize:14, fontWeight:800, color:"#1A1A1A", marginBottom:4 }}>Recommandations</div>
              <div style={{ fontSize:12, color:"#6B7280", lineHeight:1.5, marginBottom:12 }}>Conseils nutritionnels personnalisés selon vos réponses.</div>
              <div style={{ fontSize:12, fontWeight:800, color:"#00BFA5" }}>Découvrir →</div>
            </div>
            <div onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "recettes", answers); }}
              style={{ background:"white", borderRadius:20, padding:"20px", border:"1px solid #E8EDF2", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", cursor:"pointer", transition:"box-shadow 0.2s, transform 0.2s" }}
              onMouseEnter={e=>{e.currentTarget.style.boxShadow="0 8px 32px rgba(26,58,92,0.12)";e.currentTarget.style.transform="translateY(-2px)";}}
              onMouseLeave={e=>{e.currentTarget.style.boxShadow="0 2px 16px rgba(26,58,92,0.06)";e.currentTarget.style.transform="translateY(0)";}}>
              <div style={{ width:40, height:40, borderRadius:12, background:"#FFF0EB", marginBottom:12, display:"flex", alignItems:"center", justifyContent:"center" }}>
                <div style={{ width:16, height:16, borderRadius:5, background:"#FF6B35" }} />
              </div>
              <div style={{ fontSize:14, fontWeight:800, color:"#1A1A1A", marginBottom:4 }}>
                {answers[" En cuisine"] === "Je n'ai pas le temps" ? "Recettes rapides" : "Idées de recettes"}
              </div>
              <div style={{ fontSize:12, color:"#6B7280", lineHeight:1.5, marginBottom:12 }}>
                {answers[" En cuisine"] === "Je n'ai pas le temps" ? "Recettes équilibrées en moins de 30 min." : "Recettes selon vos préférences."}
              </div>
              <div style={{ fontSize:12, fontWeight:800, color:"#FF6B35" }}>Découvrir →</div>
            </div>
          </div>
          <div style={{ display:"flex", gap:10 }}>
            <button onClick={()=>{setStep(1);setDone(false);setPersons(2);setVslider(0);setCompo(null);setCuisine(null);setRepas(null);setAnswers({});}}
              style={{ flex:1, background:"white", border:"1px solid #E8EDF2", borderRadius:12, padding:"12px", fontSize:13, fontWeight:700, color:"#374151", cursor:"pointer" }}>Recommencer</button>
            <button onClick={onBack}
              style={{ flex:1, background:"white", border:"1px solid #E8EDF2", borderRadius:12, padding:"12px", fontSize:13, fontWeight:700, color:"#374151", cursor:"pointer" }}>← Menu</button>
          </div>

          {/* Continuer */}
          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "sante", answers); }}
            style={{ background:"#1A3A5C", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"18px", cursor:"pointer", width:"100%", boxShadow:"0 4px 20px rgba(26,58,92,0.25)" }}
            onMouseEnter={e => e.currentTarget.style.opacity = "0.9"}
            onMouseLeave={e => e.currentTarget.style.opacity = "1"}>
            Continuer vers mon profil santé →
          </button>
        </div>
      </div>
    );
  }'''

NEW_DONE = '''  if (done) {
    // Redirect immédiat — la page "Profil créé" est remplacée par ProfilFinalScreen
    useEffect(() => {
      const compoVal = answers[" Composition du repas"];
      const cuisineVal = answers["\u200d En cuisine"];
      if (onDone) onDone(compoVal, "sante", answers);
    }, []);
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"Arial, sans-serif" }}>
        <div style={{ textAlign:"center", color:"#888" }}>
          <div style={{ fontSize:32, marginBottom:12 }}>⏳</div>
          <div style={{ fontSize:16, fontWeight:700 }}>Chargement de votre profil...</div>
        </div>
      </div>
    );
  }'''

code = p(code, OLD_DONE, NEW_DONE, "4. Remplacement page Profil créé par redirect")

# ══════════════════════════════════════════════
# FIX 5 — "Recettes pour vous" sans connexion requise
# Supprimer le message "(connectez-vous pour voir vos recettes)"
# et afficher les recettes méditerranéennes par défaut
# ══════════════════════════════════════════════
code = p(code,
    '{id==="vous" && !filtreProfilInitial && <span style={{ fontSize:10, color:"#bbb", marginLeft:6 }}>(connectez-vous pour voir vos recettes)</span>}',
    '',
    "5. Supprimer message connexion recettes")

# Quand onglet "Pour vous" sans profil, montrer les recettes méditerranéennes
code = p(code,
    'if(isPourVous && filtreProfilInitial) setFiltreProfil(filtreProfilInitial);\n              else if(!isPourVous) setFiltreProfil(null);',
    'if(isPourVous) setFiltreProfil(filtreProfilInitial || "mediterraneen");\n              else setFiltreProfil(null);',
    "5b. Recettes pour vous = méditerranéen par défaut")

# ══════════════════════════════════════════════
# FIX 6 — ProfilFinalScreen: bouton "Voir mes recommandations"
# doit aller vers l'onglet recos, pas vers goBack
# Le onVoirRecos actuel est appelé avec "recettes" depuis l'onglet recos
# mais depuis le bouton principal, pas d'argument → aller vers onglet "recos"
# ══════════════════════════════════════════════
code = p(code,
    "onVoirRecos={(type) => { if(type===\"recettes\") goTo(\"recettes\"); else goTo(\"recos_qcm1\"); }}",
    "onVoirRecos={(type) => { if(type===\"recettes\") goTo(\"recettes\"); else if(type===\"recos\") goTo(\"recos_qcm1\"); }}",
    "6. ProfilFinalScreen onVoirRecos")

# ══════════════════════════════════════════════
# FIX 7 — Bouton "Voir mon profil" depuis QCM1
# Le bouton ajouté au patch précédent ne marche pas
# car onDone est appelé avec nutrition mais sans navigation
# On supprime ce bouton mal fait et on utilise onShowRecos pour aller au profil
# ══════════════════════════════════════════════
code = p(code,
    "          <button onClick={() => { if(onDone) onDone(nutrition); if(onBack) { setTimeout(()=>{ }, 100); } }} style={{ ...btn, background:\"#1A3A5C\", color:\"white\", border:\"3px solid #0d2340\" }}>👤 Voir mon profil →</button>",
    "",
    "7. Supprimer bouton profil cassé QCM1")

# ══════════════════════════════════════════════
# FIX 8 — SceneSanteScreen : s'assurer qu'elle s'affiche
# dans la cuisine (le fond cuisine2.png est déjà là)
# Vérifier que la phase "scene_sante" est bien routée
# ══════════════════════════════════════════════
# Vérification — chercher si scene_sante existe dans le code
if 'phase === "scene_sante"' in code:
    print("  ✅ 8. scene_sante phase existe")
    fixes += 1
else:
    print("  ⚠️  8. scene_sante phase MANQUANTE")
    errors.append("8. scene_sante manquante")

# ══════════════════════════════════════════════
# FIX 9 — ProfilFinalScreen onBack → select (pas goBack)
# ══════════════════════════════════════════════
code = p(code,
    "onBack={() => goBack()}\n    />;",
    "onBack={() => setPhase(\"select\")}\n    />;",
    "9. ProfilFinalScreen retour → select")

# ══════════════════════════════════════════════
# FIX 10 — Dans ProfilFinalScreen, bouton recos tab
# → switcher sur l'onglet "recos" directement
# ══════════════════════════════════════════════
code = p(code,
    "            <button onClick={onVoirRecos}\n              style={{ background:\"#FA8072\", border:\"none\", borderRadius:14, color:\"white\", fontSize:15, fontWeight:900, padding:\"16px\", cursor:\"pointer\", width:\"100%\", boxShadow:\"0 4px 16px rgba(250,128,114,0.35)\" }}>\n              Voir mes recommandations →\n            </button>",
    "            <button onClick={()=>setTab(\"recos\")}\n              style={{ background:\"#FA8072\", border:\"none\", borderRadius:14, color:\"white\", fontSize:15, fontWeight:900, padding:\"16px\", cursor:\"pointer\", width:\"100%\", boxShadow:\"0 4px 16px rgba(250,128,114,0.35)\" }}>\n              Voir mes recommandations →\n            </button>",
    "10. Bouton recos → onglet recos dans ProfilFinal")

# ══════════════════════════════════════════════
# FIX 11 — Bouton recettes depuis onglet recos de ProfilFinal
# ══════════════════════════════════════════════
code = p(code,
    "            <button onClick={()=>{ if(typeof onVoirRecos===\"function\") onVoirRecos(\"recettes\"); }}",
    "            <button onClick={()=>{ onVoirRecos(\"recettes\"); }}",
    "11. Bouton recettes dans onglet recos")

# ══════════════════════════════════════════════
# RÉSULTAT
# ══════════════════════════════════════════════
print(f"\n{'='*50}")
print(f"Patches: {fixes} ✅  |  Erreurs: {len(errors)} ⚠️")
if errors:
    print(f"Non trouvés: {', '.join(errors)}")

out = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(out, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit !")
