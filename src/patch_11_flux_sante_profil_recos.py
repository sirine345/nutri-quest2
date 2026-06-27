"""
PATCH 11 — Flux complet après QCM Santé :
  - MNA déclenché si silhouette "plus mince" ou âge 75+
  - MEDAS déclenché si LLC (déjà en place, on garde)
  - Après tout → ProfilSanteScreen (avatar + réponses QCM Santé)
  - Puis → RecommandationsSanteScreen personnalisée
Usage: python patch_11_flux_sante_profil_recos.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ══════════════════════════════════════════════════════
# FIX 1 — Dans QcmSanteScreen : modifier le déclenchement MNA
# Actuellement MNA n'est pas déclenché depuis QCM Santé
# On ajoute : si évolution "mince" ou âge 75+ → showMna
# ══════════════════════════════════════════════════════

# Ajouter état showMna après les états existants dans QcmSanteScreen
OLD_SANTE_STATES = '''  const [showMedas, setShowMedas] = useState(false);
  const [showTransitionLLC, setShowTransitionLLC] = useState(false);
  const [medasDone, setMedasDone] = useState(false);
  const [medasResult, setMedasResult] = useState(null);'''

NEW_SANTE_STATES = '''  const [showMedas, setShowMedas] = useState(false);
  const [showTransitionLLC, setShowTransitionLLC] = useState(false);
  const [medasDone, setMedasDone] = useState(false);
  const [medasResult, setMedasResult] = useState(null);
  const [showMna, setShowMna] = useState(false);
  const [mnaResult, setMnaResult] = useState(null);
  const [mnaDone, setMnaDone] = useState(false);'''

if OLD_SANTE_STATES in code:
    code = code.replace(OLD_SANTE_STATES, NEW_SANTE_STATES)
    fixes += 1
    print("✅ FIX 1 — États MNA ajoutés dans QcmSanteScreen")
else:
    print("⚠️  FIX 1 — États non trouvés")

# ══════════════════════════════════════════════════════
# FIX 2 — Ajouter logique MNA avant le handleFinish dans QcmSanteScreen
# Déclencher MNA si silhouette "mince" ou âge 75+
# ══════════════════════════════════════════════════════

OLD_HAS_LLC = '''  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const isAge75plus = age === "75 à 84 ans" || age === "85 ans et plus";'''

NEW_HAS_LLC = '''  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const isAge75plus = age === "75 à 84 ans" || age === "85 ans et plus";
  const hasMnaRisk = (evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince") || isAge75plus;'''

if OLD_HAS_LLC in code:
    code = code.replace(OLD_HAS_LLC, NEW_HAS_LLC)
    fixes += 1
    print("✅ FIX 2 — Logique hasMnaRisk ajoutée")
else:
    print("⚠️  FIX 2 — hasLLC non trouvé")

# ══════════════════════════════════════════════════════
# FIX 3 — Afficher QCM MNA depuis QcmSanteScreen si risque détecté
# Ajouter AVANT le return principal de QcmSanteScreen
# ══════════════════════════════════════════════════════

OLD_LLC_TRANSITION = '''  // Show LLC transition
  if (showTransitionLLC && !showMedas) {
    return <TransitionLLCScreen onStart={() => { setShowTransitionLLC(false); setShowMedas(true); }} />;
  }

  // Show MEDAS if LLC selected
  if (showMedas && !medasDone) {
    return <QcmMedasScreen onBack={() => setShowMedas(false)} playerName={playerName}
      onDone={(result) => { setMedasResult(result); setMedasDone(true); setShowMedas(false); setStep(99); }} />;
  }'''

NEW_LLC_TRANSITION = '''  // Show MNA if risk detected (perte de poids ou 75+)
  if (showMna && !mnaDone) {
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        <div style={{ background:"#e53935", padding:"14px 20px", display:"flex", alignItems:"center", gap:12 }}>
          <button onClick={() => setShowMna(false)} style={{ background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px" }}>← Retour</button>
          <div style={{ fontSize:13, fontWeight:800, color:"white" }}>Questionnaire MNA — Dépistage dénutrition</div>
        </div>
        <Qcm2Screen
          onBack={() => setShowMna(false)}
          playerName={playerName}
          playerInfos={playerInfos}
          onDone={(compo, cuisine, ans) => {
            setMnaResult({ answers: ans });
            setMnaDone(true);
            setShowMna(false);
            if (hasLLC) { setShowTransitionLLC(true); } else { setStep(99); }
          }}
          _mnaOnly={true}
        />
      </div>
    );
  }

  // Show LLC transition
  if (showTransitionLLC && !showMedas) {
    return <TransitionLLCScreen onStart={() => { setShowTransitionLLC(false); setShowMedas(true); }} />;
  }

  // Show MEDAS if LLC selected
  if (showMedas && !medasDone) {
    return <QcmMedasScreen onBack={() => setShowMedas(false)} playerName={playerName}
      onDone={(result) => { setMedasResult(result); setMedasDone(true); setShowMedas(false); setStep(99); }} />;
  }'''

if OLD_LLC_TRANSITION in code:
    code = code.replace(OLD_LLC_TRANSITION, NEW_LLC_TRANSITION)
    fixes += 1
    print("✅ FIX 3 — Déclenchement MNA ajouté dans QcmSanteScreen")
else:
    print("⚠️  FIX 3 — Bloc LLC transition non trouvé")

# ══════════════════════════════════════════════════════
# FIX 4 — Dans step 3 (Activité), modifier le bouton "Voir mon bilan"
# pour déclencher MNA si risque, sinon LLC, sinon bilan direct
# ══════════════════════════════════════════════════════

OLD_STEP3_BTN = '''                <button onClick={() => { if(hasLLC) { setShowTransitionLLC(true); } else { setStep(99); } }} style={{ flex:2, background:"#1A3A5C", color:"white", border:"none", borderRadius:12, padding:"13px", fontSize:14, fontWeight:800, cursor:"pointer" }}>
                  {hasLLC ? "Suivant → QCM méditerranéen" : "Voir mon bilan →"}
                </button>'''

NEW_STEP3_BTN = '''                <button onClick={() => {
                  if (hasMnaRisk && !mnaDone) { setShowMna(true); }
                  else if (hasLLC) { setShowTransitionLLC(true); }
                  else { setStep(99); }
                }} style={{ flex:2, background:"#1A3A5C", color:"white", border:"none", borderRadius:12, padding:"13px", fontSize:14, fontWeight:800, cursor:"pointer" }}>
                  {hasMnaRisk && !mnaDone ? "Suivant → Questionnaire dénutrition" : hasLLC ? "Suivant → QCM méditerranéen" : "Voir mon bilan →"}
                </button>'''

if OLD_STEP3_BTN in code:
    code = code.replace(OLD_STEP3_BTN, NEW_STEP3_BTN)
    fixes += 1
    print("✅ FIX 4 — Bouton étape 3 mis à jour avec logique MNA")
else:
    print("⚠️  FIX 4 — Bouton étape 3 non trouvé")

# ══════════════════════════════════════════════════════
# FIX 5 — handleFinish : passer mnaResult et avatarChoice
# ══════════════════════════════════════════════════════

OLD_HANDLE = '''  const handleFinish = () => {
   const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, freins, medasResult };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email || "" } } });
    onDone(data);
  };'''

NEW_HANDLE = '''  const handleFinish = () => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui, pathologies, traitement, regimePrescrit, modeVie, freins, medasResult, mnaResult, hasMnaRisk, hasLLC };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom: playerName, email: playerInfos?.email || "" } } });
    onDone(data);
  };'''

if OLD_HANDLE in code:
    code = code.replace(OLD_HANDLE, NEW_HANDLE)
    fixes += 1
    print("✅ FIX 5 — handleFinish enrichi avec mnaResult et flags")
else:
    print("⚠️  FIX 5 — handleFinish non trouvé")

# ══════════════════════════════════════════════════════
# FIX 6 — Ajouter ProfilSanteScreen et RecommandationsSanteScreen
# AVANT /* ══ APP ══ */
# ══════════════════════════════════════════════════════

MARKER_APP = "/* ══ APP ══ */"

NEW_SCREENS = '''/* ══ PAGE PROFIL SANTÉ ══ */
function ProfilSanteScreen({ santeData, playerName, avatarChoice, onVoirRecos, onBack }) {
  const { age, sexe, silhouette, evolution, seul, autonomie, maladieChroniqueOui,
          pathologies, traitement, regimePrescrit, modeVie, freins,
          medasResult, mnaResult, hasMnaRisk, hasLLC } = santeData || {};

  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const InfoRow = ({ label, value }) => value ? (
    <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 0", borderBottom:"1px solid #f0f0f0" }}>
      <span style={{ fontSize:13, color:"#888", fontWeight:600 }}>{label}</span>
      <span style={{ fontSize:13, color:"#1A1A1A", fontWeight:800, textAlign:"right", maxWidth:"55%" }}>{Array.isArray(value) ? value.join(", ") : String(value)}</span>
    </div>
  ) : null;

  return (
    <div style={{ position:"fixed", inset:0, background:"#f5f5f5", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon */}
      <div style={{ background:"#FA8072", padding:"20px 32px 28px" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.25)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"6px 14px", marginBottom:16 }}>← Retour</button>
        <div style={{ display:"flex", alignItems:"flex-end", gap:20 }}>
          <img src={avatarSrc} alt="Avatar" style={{ width:100, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))", flexShrink:0 }} />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"14px 18px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", flex:1 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:4 }}>Profil de santé</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.6 }}>
              Bonjour <strong style={{ color:"#FA8072" }}>{playerName}</strong> ! Voici le résumé de ton profil de santé basé sur tes réponses.
            </div>
          </div>
        </div>
        <div style={{ marginTop:20 }}>
          <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>Résultats · QCM Profil Santé</div>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.2)", margin:0 }}>
            Mon Profil <span style={{ color:"#ffdd44" }}>Santé</span>
          </h1>
        </div>
      </div>

      <div style={{ padding:"24px 32px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>

        {/* Profil général */}
        <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 4px 16px rgba(0,0,0,0.08)" }}>
          <div style={{ background:"#e3f2fd", borderBottom:"2px solid #1976d244", padding:"14px 18px", display:"flex", alignItems:"center", gap:10 }}>
            <span style={{ fontSize:20 }}>👤</span>
            <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#1976d2" }}>Profil général</span>
          </div>
          <div style={{ padding:"14px 18px" }}>
            <InfoRow label="Âge" value={age} />
            <InfoRow label="Sexe" value={sexe} />
            <InfoRow label="Silhouette" value={silhouette ? `N°${silhouette}` : null} />
            <InfoRow label="Évolution corporelle" value={evolution} />
            <InfoRow label="Vit seul(e)" value={seul} />
            <InfoRow label="Autonomie" value={autonomie} />
          </div>
        </div>

        {/* Santé */}
        <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 4px 16px rgba(0,0,0,0.08)" }}>
          <div style={{ background:"#fbe9e7", borderBottom:"2px solid #e5393544", padding:"14px 18px", display:"flex", alignItems:"center", gap:10 }}>
            <span style={{ fontSize:20 }}>🏥</span>
            <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#e53935" }}>Santé</span>
          </div>
          <div style={{ padding:"14px 18px" }}>
            <InfoRow label="Maladie chronique" value={maladieChroniqueOui} />
            <InfoRow label="Pathologies" value={pathologies && pathologies.length > 0 && !pathologies.includes("Aucune") ? pathologies : null} />
            <InfoRow label="Traitement régulier" value={traitement} />
            <InfoRow label="Régime prescrit" value={regimePrescrit} />
          </div>
        </div>

        {/* Activité */}
        <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 4px 16px rgba(0,0,0,0.08)" }}>
          <div style={{ background:"#e8f5e9", borderBottom:"2px solid #4caf5044", padding:"14px 18px", display:"flex", alignItems:"center", gap:10 }}>
            <span style={{ fontSize:20 }}>🏃</span>
            <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#2e7d32" }}>Activité physique</span>
          </div>
          <div style={{ padding:"14px 18px" }}>
            <InfoRow label="Mode de vie" value={modeVie} />
            <InfoRow label="Freins" value={freins && freins.length > 0 ? freins : null} />
          </div>
        </div>

        {/* Résultats spéciaux */}
        <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 4px 16px rgba(0,0,0,0.08)" }}>
          <div style={{ background:"#f3eeff", borderBottom:"2px solid #7C3AED44", padding:"14px 18px", display:"flex", alignItems:"center", gap:10 }}>
            <span style={{ fontSize:20 }}>📊</span>
            <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#7C3AED" }}>Bilans complémentaires</span>
          </div>
          <div style={{ padding:"14px 18px" }}>
            {medasResult ? (
              <div style={{ background: medasResult.score >= 10 ? "#e8f5e9" : medasResult.score >= 6 ? "#fff8e1" : "#fbe9e7", borderRadius:10, padding:"10px 12px", marginBottom:10 }}>
                <div style={{ fontSize:12, fontWeight:900, color: medasResult.score >= 10 ? "#2e7d32" : medasResult.score >= 6 ? "#f57c00" : "#e53935" }}>
                  🫒 Score MEDAS : {medasResult.score}/14
                </div>
                <div style={{ fontSize:11, color:"#555", marginTop:3 }}>
                  {medasResult.score >= 10 ? "Forte adhésion au régime méditerranéen" : medasResult.score >= 6 ? "Adhésion modérée" : "Faible adhésion — à améliorer"}
                </div>
              </div>
            ) : hasLLC ? (
              <div style={{ fontSize:12, color:"#888", fontStyle:"italic" }}>QCM méditerranéen non effectué</div>
            ) : null}
            {mnaResult ? (
              <div style={{ background:"#e3f2fd", borderRadius:10, padding:"10px 12px" }}>
                <div style={{ fontSize:12, fontWeight:900, color:"#1976d2" }}>🔍 Dépistage dénutrition effectué</div>
                <div style={{ fontSize:11, color:"#555", marginTop:3 }}>Résultats pris en compte dans tes recommandations</div>
              </div>
            ) : hasMnaRisk ? (
              <div style={{ fontSize:12, color:"#888", fontStyle:"italic" }}>Dépistage dénutrition non effectué</div>
            ) : (
              <div style={{ fontSize:12, color:"#888", fontStyle:"italic" }}>Aucun bilan complémentaire nécessaire</div>
            )}
          </div>
        </div>

      </div>

      {/* Bouton */}
      <div style={{ padding:"0 32px 32px" }}>
        <button onClick={onVoirRecos}
          style={{ width:"100%", background:"#FA8072", border:"none", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.4)" }}>
          Voir mes recommandations personnalisées →
        </button>
      </div>
    </div>
  );
}

/* ══ PAGE RECOMMANDATIONS SANTÉ ══ */
function RecommandationsSanteScreen({ santeData, qcm2Answers, playerName, onBack, onVoirRecettes }) {
  const { modeVie, freins, pathologies, hasLLC, hasMnaRisk, medasResult, mnaResult, regimePrescrit } = santeData || {};
  const cuisine = qcm2Answers?.["‍ En cuisine"];
  const pratiques = qcm2Answers?.[" Pratiques alimentaires"];
  const nbRepas = qcm2Answers?.[" Nombre de repas"];

  const PLANNING_SEMAINE = [
    { jour:"Lundi",    midi:"Lentilles aux lardons",         soir:"Omelette aux champignons" },
    { jour:"Mardi",    midi:"Shakshuka + pain complet",      soir:"Soupe + tartines sardines" },
    { jour:"Mercredi", midi:"Quiche poireaux-roquefort",     soir:"Salade grecque + œuf" },
    { jour:"Jeudi",    midi:"Curry aux lentilles",           soir:"Velouté pois cassés" },
    { jour:"Vendredi", midi:"Brochettes thon fenouil",       soir:"Flan courgettes" },
    { jour:"Samedi",   midi:"Burger pois chiches",           soir:"Ragoût haricots blancs" },
    { jour:"Dimanche", midi:"Poulet curry express",          soir:"Tarte ratatouille" },
  ];

  const recos = [];

  // LLC → régime méditerranéen
  if (hasLLC) {
    recos.push({
      titre: "Régime méditerranéen",
      couleurHeader: "#2e7d32",
      bgHeader: "#e8f5e9",
      icon: "/salade_grecque.png",
      pourquoi: medasResult
        ? `Ton score MEDAS est de ${medasResult.score}/14. ${medasResult.score >= 10 ? "Excellente adhésion au régime méditerranéen — continue !" : medasResult.score >= 6 ? "Adhésion modérée. Quelques ajustements peuvent améliorer ta protection cardiovasculaire." : "Faible adhésion. Le régime méditerranéen est fortement recommandé pour les personnes atteintes de LLC."}`
        : "Le régime méditerranéen est particulièrement bénéfique pour les personnes atteintes de LLC. Il réduit l'inflammation et protège le système cardiovasculaire.",
      conseils: [
        "Utilisez l'huile d'olive comme matière grasse principale",
        "Mangez du poisson au moins 2 fois par semaine",
        "Privilégiez les légumineuses 3 fois par semaine",
        "Limitez la viande rouge à 1-2 fois par semaine",
        "Consommez des fruits à coque quotidiennement (amandes, noix)",
      ],
      profil: "mediterraneen",
    });
  }

  // Pas le temps → recettes rapides + planning
  if (cuisine === "Je n'ai pas le temps") {
    recos.push({
      titre: "Manger équilibré sans perdre de temps",
      couleurHeader: "#e65100",
      bgHeader: "#fff3e0",
      icon: "/marmitte.png",
      pourquoi: "Tu n'as pas beaucoup de temps pour cuisiner. Bonne nouvelle : des repas équilibrés peuvent se préparer en moins de 20 minutes !",
      conseils: [
        "Cuisinez en grande quantité le week-end et congelez",
        "Les conserves (sardines, lentilles, pois chiches) sont vos alliées",
        "Shakshuka, omelette, curry lentilles : prêts en 15-20 min",
        "Préparez vos légumes à l'avance pour la semaine",
      ],
      profil: "rapide",
      hasPlanning: true,
    });
  }

  // Saute des repas
  if (nbRepas === "Midi uniquement" || nbRepas === "Soir uniquement") {
    recos.push({
      titre: "Tous les repas sont importants",
      couleurHeader: "#f57c00",
      bgHeader: "#fff8e1",
      icon: "/repas.png",
      pourquoi: nbRepas === "Midi uniquement"
        ? "Tu ne prends pas de dîner. Le soir, un repas léger mais complet aide à récupérer et à ne pas grignoter."
        : "Tu ne prends pas de déjeuner. Sauter le repas du midi entraîne souvent une fatigue l'après-midi et des fringales.",
      conseils: nbRepas === "Midi uniquement"
        ? ["Une soupe + tartines = repas complet en 10 min", "Un œuf + salade verte = protéines et légumes", "Des lentilles en conserve réchauffées = rapide et nutritif", "Un yaourt + fruit = dessert équilibré"]
        : ["Une salade composée + pain complet = repas rapide", "Des restes du dîner réchauffés = pratique", "Un sandwich pain complet + légumes + protéines", "Une soupe thermos à emporter"],
      profil: "rapide",
    });
  }

  // Sans porc
  if (pratiques === "Je mange sans porc") {
    recos.push({
      titre: "Recettes adaptées sans porc",
      couleurHeader: "#0288d1",
      bgHeader: "#e1f5fe",
      icon: "/poisson.png",
      pourquoi: "Toutes les recettes proposées sont adaptées à ton alimentation sans porc. Volaille, poisson et légumineuses sont tes meilleures alternatives protéinées.",
      conseils: [
        "La volaille (poulet, dinde) remplace avantageusement le porc",
        "Le poisson apporte des oméga-3 essentiels",
        "Les légumineuses sont riches en protéines végétales",
        "Vérifiez les étiquettes : la charcuterie cache souvent du porc",
      ],
      profil: "sans_porc",
    });
  }

  // Sans viande
  if (pratiques === "Je mange sans viande") {
    recos.push({
      titre: "Végétarien équilibré",
      couleurHeader: "#558b2f",
      bgHeader: "#f1f8e9",
      icon: "/legumesec.png",
      pourquoi: "Une alimentation végétarienne bien construite couvre tous tes besoins nutritionnels. L'association légumineuses + céréales complètes fournit des protéines complètes.",
      conseils: [
        "Associez légumineuses + céréales à chaque repas (protéines complètes)",
        "Les œufs et produits laitiers complètent les apports",
        "Variez : lentilles, pois chiches, haricots, tofu",
        "Pensez au fer : épinards, lentilles, légumineuses",
      ],
      profil: "vegetarien",
    });
  }

  // Sédentaire
  if (modeVie === "Sédentaire") {
    recos.push({
      titre: "Adapter son alimentation à un mode de vie sédentaire",
      couleurHeader: "#7C3AED",
      bgHeader: "#f3eeff",
      icon: "/aliment.png",
      pourquoi: "Un mode de vie sédentaire nécessite d'adapter ses apports caloriques. Privilégiez des aliments rassasiants et riches en nutriments pour éviter les grignotages.",
      conseils: [
        "Privilégiez les féculents complets (rassasiants plus longtemps)",
        "Augmentez les légumes et légumineuses (fibres = satiété)",
        "Limitez les aliments ultra-transformés et sucreries",
        "Buvez suffisamment d'eau (souvent confondu avec la faim)",
      ],
      profil: "legumes",
    });
  }

  // Dénutrition
  if (hasMnaRisk) {
    recos.push({
      titre: "Maintenir un bon apport nutritionnel",
      couleurHeader: "#c62828",
      bgHeader: "#fbe9e7",
      icon: "/oeuf.png",
      pourquoi: "Une perte de poids récente ou un âge avancé augmentent le risque de dénutrition. Il est essentiel de maintenir des apports suffisants en protéines et en calories.",
      conseils: [
        "Ne sautez aucun repas — 3 repas structurés par jour minimum",
        "Enrichissez vos plats : fromage râpé, œuf battu, beurre",
        "Privilégiez les aliments riches en protéines : viande, œufs, poisson",
        "Optez pour 3-4 produits laitiers par jour",
        "Si appétit faible : fractionnez en 5-6 petits repas",
        "Consultez votre médecin si la perte de poids continue",
      ],
      profil: "senior",
    });
  }

  // Si aucune reco spécifique
  if (recos.length === 0) {
    recos.push({
      titre: "Continuez vos bonnes habitudes !",
      couleurHeader: "#9ACD32",
      bgHeader: "#f0f9e0",
      icon: "/legume2.png",
      pourquoi: "Ton profil ne présente pas de point d'alerte particulier. Continue à manger varié et équilibré selon les recommandations du PNNS.",
      conseils: [
        "5 fruits et légumes par jour",
        "2 fois du poisson par semaine",
        "Des féculents complets à chaque repas",
        "Limitez la charcuterie et le fast food",
      ],
      profil: "mediterraneen",
    });
  }

  // Trouver le planning pour "pas le temps"
  const recoPasTemps = recos.find(r => r.hasPlanning);

  return (
    <div style={{ position:"fixed", inset:0, background:"#f5f5f5", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon avec Max */}
      <div style={{ background:"#FA8072", padding:"20px 32px 28px" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.25)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"6px 14px", marginBottom:16 }}>← Retour</button>
        <div style={{ display:"flex", alignItems:"flex-end", gap:20 }}>
          <img src="/e.png" alt="Max" style={{ width:110, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))", flexShrink:0 }} />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"14px 18px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", flex:1 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:4 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.6 }}>
              Voici tes <strong style={{ color:"#FA8072" }}>recommandations personnalisées</strong> basées sur ton profil de santé et tes habitudes alimentaires.
            </div>
          </div>
        </div>
        <div style={{ marginTop:20 }}>
          <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>Résultats · Profil Santé</div>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.2)", margin:0, lineHeight:1.1 }}>
            Mes Recommandations<br/><span style={{ color:"#ffdd44" }}>Personnalisées</span>
          </h1>
        </div>
      </div>

      {/* Cartes recommandations */}
      <div style={{ padding:"24px 32px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        {recos.slice(0, 4).map((reco, i) => (
          <div key={i} style={{ background:"white", borderRadius:18, overflow:"hidden", boxShadow:"0 4px 20px rgba(0,0,0,0.1)", border:`2px solid ${reco.couleurHeader}33` }}>
            <div style={{ background:reco.bgHeader, borderBottom:`2px solid ${reco.couleurHeader}44`, padding:"16px 18px", display:"flex", alignItems:"center", gap:12 }}>
              <img src={reco.icon} alt="" style={{ width:44, height:44, objectFit:"contain", filter:"drop-shadow(1px 2px 4px rgba(0,0,0,0.15))" }} />
              <div>
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:reco.couleurHeader, lineHeight:1.3 }}>{reco.titre}</div>
                <div style={{ fontSize:11, color:"#666", marginTop:2 }}>Recommandation personnalisée</div>
              </div>
            </div>
            <div style={{ padding:"16px 18px" }}>
              <div style={{ fontSize:12, color:"#444", lineHeight:1.65, marginBottom:14, padding:"10px 12px", background:"#fafafa", borderRadius:8, borderLeft:`3px solid ${reco.couleurHeader}` }}>
                {reco.pourquoi}
              </div>
              <div style={{ display:"flex", flexDirection:"column", gap:8, marginBottom:14 }}>
                {reco.conseils.map((c, j) => (
                  <div key={j} style={{ display:"flex", gap:10, alignItems:"flex-start" }}>
                    <div style={{ width:22, height:22, borderRadius:6, background:reco.bgHeader, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:11, fontWeight:900, color:reco.couleurHeader, marginTop:1 }}>{j+1}</div>
                    <span style={{ fontSize:12, color:"#333", lineHeight:1.55 }}>{c}</span>
                  </div>
                ))}
              </div>
              <button onClick={() => onVoirRecettes(reco.profil)}
                style={{ background:reco.couleurHeader, color:"white", border:"none", borderRadius:10, padding:"10px 16px", fontSize:12, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Voir les recettes associées →
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Planning semaine si "pas le temps" */}
      {recoPasTemps && (
        <div style={{ margin:"0 32px 32px", background:"white", borderRadius:18, overflow:"hidden", boxShadow:"0 4px 20px rgba(0,0,0,0.1)" }}>
          <div style={{ background:"#fff3e0", borderBottom:"2px solid #e6510044", padding:"16px 20px" }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:"#e65100" }}>📅 Planning repas — 1 semaine</div>
            <div style={{ fontSize:12, color:"#666", marginTop:4 }}>Des idées de repas équilibrés et rapides pour toute la semaine</div>
          </div>
          <div style={{ padding:"16px 20px" }}>
            {PLANNING_SEMAINE.map((j, i) => (
              <div key={i} style={{ display:"grid", gridTemplateColumns:"80px 1fr 1fr", gap:12, padding:"10px 0", borderBottom: i < PLANNING_SEMAINE.length-1 ? "1px solid #f0f0f0" : "none", alignItems:"center" }}>
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:12, fontWeight:900, color:"#e65100" }}>{j.jour}</div>
                <div style={{ fontSize:12, color:"#333", background:"#fff3e0", borderRadius:8, padding:"6px 10px" }}>🌞 {j.midi}</div>
                <div style={{ fontSize:12, color:"#333", background:"#e3f2fd", borderRadius:8, padding:"6px 10px" }}>🌙 {j.soir}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bouton retour menu */}
      <div style={{ padding:"0 32px 32px" }}>
        <button onClick={onBack}
          style={{ width:"100%", background:"white", border:"3px solid #FA8072", borderRadius:14, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer" }}>
          ← Retour au menu cuisine
        </button>
      </div>
    </div>
  );
}

'''

if MARKER_APP in code:
    code = code.replace(MARKER_APP, NEW_SCREENS + MARKER_APP)
    fixes += 1
    print("✅ FIX 6 — ProfilSanteScreen + RecommandationsSanteScreen ajoutés")
else:
    print("⚠️  FIX 6 — Marqueur APP non trouvé")

# ══════════════════════════════════════════════════════
# FIX 7 — Dans App() : ajouter états et phases pour profil/recos santé
# ══════════════════════════════════════════════════════

OLD_SANTE_DATA = "  const [santeData, setSanteData] = useState({});"
NEW_SANTE_DATA = """  const [santeData, setSanteData] = useState({});
  const [qcm2AnswersForRecos, setQcm2AnswersForRecos] = useState({});"""

if OLD_SANTE_DATA in code:
    code = code.replace(OLD_SANTE_DATA, NEW_SANTE_DATA)
    fixes += 1
    print("✅ FIX 7 — État qcm2AnswersForRecos ajouté dans App")

# ══════════════════════════════════════════════════════
# FIX 8 — Dans App() screen switcher : ajouter les nouvelles phases
# et modifier qcm_sante pour aller vers profil_sante
# ══════════════════════════════════════════════════════

OLD_QCM_SANTE_PHASE = '    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setPhase("select"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;'

NEW_QCM_SANTE_PHASE = '''    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); goTo("profil_sante"); }} playerName={playerName} playerInfos={playerInfos} />;
    if (phase === "profil_sante") return <ProfilSanteScreen santeData={santeData} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onVoirRecos={() => goTo("recos_sante")} />;
    if (phase === "recos_sante") return <RecommandationsSanteScreen santeData={santeData} qcm2Answers={qcm2Answers} playerName={playerName} onBack={() => { setPhase("select"); setPhaseHistory([]); }} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;'''

if OLD_QCM_SANTE_PHASE in code:
    code = code.replace(OLD_QCM_SANTE_PHASE, NEW_QCM_SANTE_PHASE)
    fixes += 1
    print("✅ FIX 8 — Phases profil_sante et recos_sante ajoutées dans App")
else:
    print("⚠️  FIX 8 — Phase qcm_sante non trouvée")

# ══════════════════════════════════════════════════════
# FIX 9 — Dans QCM2, sauvegarder les answers pour les recos
# Modifier le onDone de qcm2 pour stocker qcm2Answers
# ══════════════════════════════════════════════════════

OLD_QCM2_DONE = '    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) setQcm2Answers(ans); if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); }} />;'

NEW_QCM2_DONE = '    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) { setQcm2Answers(ans); setQcm2AnswersForRecos(ans); } if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); }} />;'

if OLD_QCM2_DONE in code:
    code = code.replace(OLD_QCM2_DONE, NEW_QCM2_DONE)
    fixes += 1
    print("✅ FIX 9 — QCM2 answers sauvegardées pour recos santé")
else:
    print("⚠️  FIX 9 — Phase qcm2 non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/9 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
