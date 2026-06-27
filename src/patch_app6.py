#!/usr/bin/env python3
"""
Patch 6 :
1. Agrandir les aliments dans le mini-jeu
2. QCM dénutrition (MNA) après QCM Santé si symptômes
3. LLC déclenche MEDAS depuis QCM Santé (déjà fait, vérif)
4. Recettes pour vous = profil QCM1+QCM2, sans méditerranéen pour non-LLC
5. Recommandations QCM2 adaptées (repas, végétarien, etc.)
"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

fixes = 0
errors = []

def p(code, old, new, name):
    global fixes
    if old in code:
        fixes += 1
        print(f"  ✅ {name}")
        return code.replace(old, new, 1)
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

def p_all(code, old, new, name):
    global fixes
    n = code.count(old)
    if n > 0:
        fixes += 1
        print(f"  ✅ {name} ({n}x)")
        return code.replace(old, new)
    errors.append(name)
    print(f"  ⚠️  Non trouvé: {name}")
    return code

print("\n=== Patches ===\n")

# ══════════════════════════════════════════════
# FIX 1 — Agrandir les aliments dans compose ton repas
# Passer de 38x38 → 60x60, grid 2 colonnes au lieu de 3
# ══════════════════════════════════════════════
code = p(code,
    'display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:5',
    'display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:8',
    "1a. Grid aliments 2 colonnes")

code = p_all(code,
    'food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:38, height:38, objectFit:"contain" }} /> : <div style={{ fontSize:24 }}>{food.emoji}</div>',
    'food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:60, height:60, objectFit:"contain" }} /> : <div style={{ fontSize:38 }}>{food.emoji}</div>',
    "1b. Taille images aliments 60x60")

code = p_all(code,
    'fontSize:9, fontWeight:800, color:"#444", marginTop:2, lineHeight:1.2',
    'fontSize:11, fontWeight:800, color:"#444", marginTop:4, lineHeight:1.2',
    "1c. Taille texte aliments")

code = p_all(code,
    'padding:"7px 4px"',
    'padding:"10px 6px"',
    "1d. Padding cartes aliments")

# ══════════════════════════════════════════════
# FIX 2 — Recettes pour vous = pas méditerranéen par défaut
# Basées sur QCM1 (score faible) + QCM2 (végétarien, sans porc, rapide)
# Supprimer le fallback "mediterraneen" pour non-LLC
# ══════════════════════════════════════════════
code = p(code,
    'if(isPourVous) setFiltreProfil(filtreProfilInitial || "mediterraneen");\n              else setFiltreProfil(null);',
    'if(isPourVous) setFiltreProfil(filtreProfilInitial || null);\n              else setFiltreProfil(null);',
    "2. Recettes pour vous sans méditerranéen forcé")

# ══════════════════════════════════════════════
# FIX 3 — QCM Santé: déclencher MNA après le bilan
# si perte d'appétit / perte de poids / autonomie limitée
# Ajouter bouton MNA dans le bilan final (step 99) de QcmSanteScreen
# et faire en sorte que handleFinish passe via MNA si nécessaire
# ══════════════════════════════════════════════

# On ajoute un state showMnaAfterSante et on déclenche Qcm2Screen en mode MNA
# Chercher handleFinish dans QcmSanteScreen
OLD_HANDLE = '''  const handleFinish = () => {
   const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, freins, medasResult };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email || "" } } });
    onDone(data);
  };'''

NEW_HANDLE = '''  const handleFinish = (withMna = false) => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, freins, medasResult };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email || "" } } });
    onDone(data, withMna);
  };

  // Afficher le QCM MNA si déclenché après le bilan
  const [showMnaPost, setShowMnaPost] = useState(false);
  if (showMnaPost) {
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        <div style={{ background:"#e53935", padding:"14px 20px", display:"flex", alignItems:"center", gap:12 }}>
          <button onClick={()=>setShowMnaPost(false)} style={{ background:"rgba(255,255,255,0.2)", border:"none", borderRadius:8, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"6px 14px" }}>← Retour</button>
          <span style={{ color:"white", fontWeight:900, fontSize:15 }}>🏥 Bilan MNA — Dénutrition</span>
        </div>
        {/* Intégrer les questions MNA directement ici via un composant dédié */}
        <MnaScreen onBack={()=>setShowMnaPost(false)} onDone={(mnaResult)=>{ handleFinish(false); }} playerName={playerName} playerInfos={playerInfos} />
      </div>
    );
  }'''

code = p(code, OLD_HANDLE, NEW_HANDLE, "3a. handleFinish avec option MNA")

# Ajouter le composant MnaScreen (version légère — juste les 6 questions dépistage)
INSERT_BEFORE_SANTE = '/* ══ QCM SANTÉ ══ */'
MNA_SCREEN = '''/* ══ COMPOSANT MNA POST-SANTÉ ══ */
function MnaScreen({ onBack, onDone, playerName, playerInfos }) {
  const [step, setStep] = useState(0);
  const [scores, setScores] = useState({});

  const QUESTIONS_MNA = [
    {
      id:"A", label:"Appétit",
      question:"Le patient a-t-il mangé moins ces 3 derniers mois par manque d'appétit, problèmes digestifs, difficultés de mastication ou de déglutition ?",
      options:[[0,"Baisse sévère"],[1,"Légère baisse"],[2,"Pas de baisse"]]
    },
    {
      id:"B", label:"Perte de poids",
      question:"Perte de poids récente (< 3 mois) ?",
      options:[[0,"Perte > 3 kg"],[1,"Ne sait pas"],[2,"Perte entre 1 et 3 kg"],[3,"Pas de perte de poids"]]
    },
    {
      id:"C", label:"Motricité",
      question:"Motricité du patient ?",
      options:[[0,"Au lit ou au fauteuil"],[1,"Autonome à l'intérieur"],[2,"Sort du domicile"]]
    },
    {
      id:"D", label:"Stress / Maladie aiguë",
      question:"Maladie aiguë ou stress psychologique ces 3 derniers mois ?",
      options:[[0,"Oui"],[2,"Non"]]
    },
    {
      id:"E", label:"Neuropsychologie",
      question:"Problèmes neuropsychologiques ?",
      options:[[0,"Démence ou dépression sévère"],[1,"Démence légère"],[2,"Pas de problème"]]
    },
    {
      id:"F", label:"IMC",
      question:"Indice de masse corporelle (kg/m²) ?",
      options:[[0,"IMC < 19"],[1,"19 ≤ IMC < 21"],[2,"21 ≤ IMC < 23"],[3,"IMC ≥ 23"]]
    },
  ];

  const q = QUESTIONS_MNA[step];
  const total = Object.values(scores).reduce((a,b)=>a+b,0);

  if (step >= QUESTIONS_MNA.length) {
    const label = total >= 12 ? "État nutritionnel normal" : total >= 8 ? "Risque de malnutrition" : "Mauvais état nutritionnel";
    const color = total >= 12 ? "#2e7d32" : total >= 8 ? "#f57c00" : "#c62828";
    saveGame({ type:"qcm2_mna", data:{ mna:{ depistage:total, label }, patient:{ prenom:playerName, ...(playerInfos||{}) } } });
    return (
      <div style={{ padding:"24px" }}>
        <div style={{ background:total>=12?"#e8f5e9":total>=8?"#fff8e1":"#fbe9e7", border:`2px solid ${color}`, borderRadius:16, padding:"20px", textAlign:"center" }}>
          <div style={{ fontSize:36, fontWeight:900, color }}>{total} / 14</div>
          <div style={{ fontSize:16, fontWeight:900, color, marginTop:6 }}>{label}</div>
          <div style={{ fontSize:13, color:"#555", marginTop:10, lineHeight:1.6 }}>
            {total>=12 ? "Votre état nutritionnel est normal. Continuez à manger varié et équilibré." : total>=8 ? "Un risque de malnutrition est détecté. Consultez un professionnel de santé." : "Un mauvais état nutritionnel est probable. Consultez un médecin rapidement."}
          </div>
        </div>
        <button onClick={()=>onDone({ total, label })}
          style={{ marginTop:20, background:color, border:"none", borderRadius:12, color:"white", fontSize:15, fontWeight:800, padding:"14px", cursor:"pointer", width:"100%" }}>
          Terminer →
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding:"20px" }}>
      <div style={{ background:"#e53935", color:"white", borderRadius:12, padding:"8px 14px", fontSize:11, fontWeight:900, display:"inline-block", marginBottom:12, letterSpacing:1 }}>
        MNA Dépistage {q.id} / 6
      </div>
      <div style={{ background:"white", borderRadius:16, padding:"20px", boxShadow:"0 2px 10px rgba(0,0,0,0.07)", marginBottom:16 }}>
        <div style={{ fontSize:15, fontWeight:900, color:"#1A1A1A", marginBottom:16, lineHeight:1.5 }}>{q.question}</div>
        {q.options.map(([val, label]) => (
          <div key={val} onClick={()=>{ setScores(s=>({...s,[q.id]:val})); setStep(s=>s+1); }}
            style={{ display:"flex", alignItems:"center", justifyContent:"space-between", border:"2px solid #E8EDF2", borderRadius:12, padding:"13px 16px", marginBottom:8, cursor:"pointer", fontSize:13, fontWeight:700, color:"#333", transition:"all 0.15s" }}
            onMouseEnter={e=>{e.currentTarget.style.background="#f0f9ff";e.currentTarget.style.borderColor="#4caf50";}}
            onMouseLeave={e=>{e.currentTarget.style.background="white";e.currentTarget.style.borderColor="#E8EDF2";}}>
            <span>{label}</span>
            <span style={{ background:"#f0f0f0", borderRadius:20, padding:"2px 10px", fontSize:11, fontWeight:900, color:"#666" }}>{val} pt{val>1?"s":""}</span>
          </div>
        ))}
      </div>
      {step > 0 && (
        <button onClick={()=>setStep(s=>s-1)}
          style={{ background:"none", border:"none", color:"#888", fontSize:13, fontWeight:700, cursor:"pointer" }}>
          ← Question précédente
        </button>
      )}
    </div>
  );
}

/* ══ QCM SANTÉ ══ */'''

code = p(code, INSERT_BEFORE_SANTE, MNA_SCREEN, "3b. Composant MnaScreen ajouté")

# ── Modifier le bilan QCM Santé (step 99) pour proposer MNA si symptômes ──
OLD_ALERTE = '''            {/* Alerte MNA si signes de dénutrition */}
            {(evolution==="Beaucoup plus mince" || evolution==="Un peu plus mince" || autonomie==="Ni l\'un ni l\'autre" || autonomie==="Repas seulement") && (
              <div style={{ background:"#fff8e1", border:"2px solid #f57c00", borderRadius:14, padding:"14px 16px", marginBottom:12 }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#e65100", marginBottom:6 }}>⚠️ Signes possibles de dénutrition</div>
                <div style={{ fontSize:12, color:"#555", lineHeight:1.6, marginBottom:8 }}>Perte de poids ou difficultés alimentaires détectées. Un bilan MNA est recommandé par la Haute Autorité de Santé.</div>
                <div style={{ fontSize:11, color:"#888", fontStyle:"italic" }}>💡 Pour accéder au QCM MNA : retournez au menu → Fabrique à Menus → indiquez "1 repas par jour".</div>
              </div>
            )}
            <button onClick={handleFinish} style={{ ...btn, width:"100%", background:"#c4622d", color:"white", border:"3px solid #a03010" }}>
              Terminer mon profil santé →
            </button>'''

NEW_ALERTE = '''            {/* Alerte MNA si signes de dénutrition */}
            {(evolution==="Beaucoup plus mince" || evolution==="Un peu plus mince" || autonomie==="Ni l\'un ni l\'autre" || autonomie==="Repas seulement") && (
              <div style={{ background:"#fff8e1", border:"2px solid #f57c00", borderRadius:14, padding:"14px 16px", marginBottom:12 }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#e65100", marginBottom:6 }}>⚠️ Signes possibles de dénutrition détectés</div>
                <div style={{ fontSize:12, color:"#555", lineHeight:1.6, marginBottom:10 }}>Perte de poids ou difficultés alimentaires repérées. Un bilan MNA est recommandé.</div>
                <button onClick={()=>setShowMnaPost(true)}
                  style={{ background:"#f57c00", border:"none", borderRadius:10, color:"white", fontSize:13, fontWeight:800, padding:"10px 20px", cursor:"pointer", width:"100%" }}>
                  Faire le bilan MNA maintenant →
                </button>
              </div>
            )}
            <button onClick={()=>handleFinish()} style={{ ...btn, width:"100%", background:"#c4622d", color:"white", border:"3px solid #a03010" }}>
              Terminer mon profil santé →
            </button>'''

code = p(code, OLD_ALERTE, NEW_ALERTE, "3c. Bouton MNA dans bilan QCM Santé")

# ══════════════════════════════════════════════
# FIX 4 — RecommandationsQcm2Screen: conseils adaptés
# Ajouter conseil "3 repas par jour" si 1 repas
# ══════════════════════════════════════════════
OLD_RECOS2 = '''  const profilRecos = [];
  if (pratiques === "Je mange sans viande") profilRecos.push({ key:"vegetarien", label:"Végétarien", couleur:"#558B2F", bg:"#F1F8E9", texte:"Recettes équilibrées sans viande ni poisson, riches en protéines végétales.", conseils:["Misez sur les légumineuses pour les protéines","Variez : pâtes, riz, quinoa, boulgour","Les œufs et fromages complètent les apports"], profil:"vegetarien" });
  if (cuisine === "Je n'ai pas le temps") profilRecos.push({ key:"rapide", label:"Recettes rapides", couleur:"#E65100", bg:"#FBE9E7", texte:"Des recettes équilibrées en moins de 30 minutes.", conseils:["Gardez des conserves de légumineuses","Les sardines : rapides et nutritives","Préparez en grande quantité, congelez"], profil:"rapide" });
  if (pratiques === "Je mange sans porc") profilRecos.push({ key:"sans_porc", label:"Sans porc", couleur:"#0277BD", bg:"#E1F5FE", texte:"Toutes les recettes adaptées sans porc ni charcuterie.", conseils:["Volaille et poisson en alternatives","Les légumineuses pour les protéines végétales"], profil:"sans_porc" });'''

NEW_RECOS2 = '''  const profilRecos = [];

  // Conseil 3 repas si 1 seul repas déclaré
  if (nbRepas === "Midi uniquement" || nbRepas === "Soir uniquement") {
    profilRecos.push({
      key:"repas", label:"Importance des 3 repas", couleur:"#e53935", bg:"#fbe9e7",
      texte:"Vous ne prenez qu'un repas principal par jour. Le PNNS recommande 3 repas équilibrés par jour pour couvrir vos besoins nutritionnels et éviter les grignotages.",
      conseils:[
        "Prenez un petit déjeuner même léger : une tartine + un fruit + un laitage",
        "Ne sautez pas de repas : cela entraîne des compensations souvent néfastes",
        "Si vous manquez d'appétit le matin, commencez par un yaourt et un fruit",
        "Structurez vos repas : entrée légère + plat équilibré + dessert fruité",
        "Hydratez-vous tout au long de la journée (1,5L d'eau minimum)"
      ],
      profil:"rapide"
    });
  }

  if (pratiques === "Je mange sans viande") profilRecos.push({ key:"vegetarien", label:"Végétarien", couleur:"#558B2F", bg:"#F1F8E9", texte:"Recettes équilibrées sans viande ni poisson, riches en protéines végétales.", conseils:["Misez sur les légumineuses pour les protéines","Variez : pâtes, riz, quinoa, boulgour","Les œufs et fromages complètent les apports"], profil:"vegetarien" });
  if (cuisine === "Je n'ai pas le temps") profilRecos.push({ key:"rapide", label:"Recettes rapides", couleur:"#E65100", bg:"#FBE9E7", texte:"Des recettes équilibrées en moins de 30 minutes.", conseils:["Gardez des conserves de légumineuses","Les sardines : rapides et nutritives","Préparez en grande quantité, congelez"], profil:"rapide" });
  if (pratiques === "Je mange sans porc") profilRecos.push({ key:"sans_porc", label:"Sans porc", couleur:"#0277BD", bg:"#E1F5FE", texte:"Toutes les recettes adaptées sans porc ni charcuterie.", conseils:["Volaille et poisson en alternatives","Les légumineuses pour les protéines végétales"], profil:"sans_porc" });'''

code = p(code, OLD_RECOS2, NEW_RECOS2, "4. Conseils QCM2 adaptés (3 repas)")

# ══════════════════════════════════════════════
# FIX 5 — Supprimer bloc méditerranéen de RecommandationsQcm2Screen
# (réservé aux LLC dans QCM Santé)
# ══════════════════════════════════════════════
OLD_MED_QCM2 = '''        {/* Méditerranéen */}
        <div style={{ background:"white", borderRadius:20, overflow:"hidden", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>
          <div style={{ padding:"20px", display:"flex", gap:14, alignItems:"flex-start" }}>
            <div style={{ width:48, height:48, borderRadius:14, background:"#E0F7F5", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
              <div style={{ width:20, height:20, borderRadius:"50%", background:"#00BFA5" }} />
            </div>
            <div style={{ flex:1 }}>
              <div style={{ display:"inline-flex", background:"#E0F7F5", borderRadius:20, padding:"3px 10px", marginBottom:8 }}>
                <span style={{ fontSize:10, fontWeight:800, color:"#00897B", textTransform:"uppercase", letterSpacing:1 }}>Recommandé PNNS</span>
              </div>
              <div style={{ fontSize:16, fontWeight:800, color:"#1A1A1A", marginBottom:6 }}>Le régime méditerranéen</div>
              <p style={{ fontSize:13, color:"#6B7280", lineHeight:1.6, margin:"0 0 14px" }}>Fruits, légumes, poisson et huile d'olive au quotidien — équilibre alimentaire optimal.</p>
              <button onClick={() => onVoirRecettes("mediterraneen")}
                style={{ background:"#00BFA5", color:"white", border:"none", borderRadius:12, padding:"12px 20px", fontSize:13, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Découvrir les recettes →
              </button>
            </div>
          </div>
        </div>'''

NEW_MED_QCM2 = '''        {/* Conseil équilibre général */}
        <div style={{ background:"white", borderRadius:20, overflow:"hidden", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>
          <div style={{ padding:"20px" }}>
            <div style={{ fontSize:14, fontWeight:800, color:"#1A1A1A", marginBottom:8 }}>🥗 Équilibre alimentaire PNNS</div>
            <p style={{ fontSize:13, color:"#6B7280", lineHeight:1.6, margin:"0 0 14px" }}>Le PNNS recommande 5 fruits et légumes/jour, 2 portions de poisson/semaine, des légumineuses 2x/semaine et de limiter la viande rouge à 500g/semaine.</p>
            <button onClick={() => onVoirRecettes("legumes")}
              style={{ background:"#4CAF50", color:"white", border:"none", borderRadius:12, padding:"12px 20px", fontSize:13, fontWeight:800, cursor:"pointer", width:"100%" }}>
              Voir les recettes équilibrées →
            </button>
          </div>
        </div>'''

code = p(code, OLD_MED_QCM2, NEW_MED_QCM2, "5. Supprimer méditerranéen QCM2, remplacer par PNNS général")

print(f"\n{'='*40}")
print(f"Fixes: {fixes} ✅  Erreurs: {len(errors)}")
if errors:
    print(f"Manquants: {', '.join(errors)}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"✅ App.jsx ({len(code)} chars) écrit")
