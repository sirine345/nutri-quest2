"""
PATCH — 
1. Supprime le MNA du QCM2 (steps 6-25 et states MNA)
2. Step 5 : toutes les réponses terminent le QCM2 (plus de redirection vers step 6)
3. Ajoute bouton "Retour au menu" après validation assiette dans MinijeuScreen
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# ─── FIX 1 : Step 5 — supprimer la redirection vers step 6 (MNA) ───
OLD_STEP5_BTN = 'if(repas===\"Midi uniquement\"||repas===\"Soir uniquement\"){setStep(6);}else{setDone(true);saveGame({ type:\"qcm2\", data: { answers: {...answers, \" Nombre de repas\": repas}, patient: { prenom: playerName, ...(playerInfos||{}) } } });}'
NEW_STEP5_BTN = 'setDone(true); saveGame({ type:"qcm2", data: { answers: {...answers, " Nombre de repas": repas}, patient: { prenom: playerName, ...(playerInfos||{}) } } });'

if OLD_STEP5_BTN in code:
    code = code.replace(OLD_STEP5_BTN, NEW_STEP5_BTN)
    fixes += 1; print("✅ FIX 1 — Step 5 : plus de redirection vers MNA")
else:
    print("⚠️ FIX 1 — Pattern step 5 non trouvé")

# ─── FIX 2 : Supprimer tous les states MNA dans Qcm2Screen ───
OLD_MNA_STATES = '''  // MNA dénutrition — Dépistage A-F
  const [mnaA, setMnaA] = useState(null); // appétit
  const [mnaB, setMnaB] = useState(null); // poids
  const [mnaC, setMnaC] = useState(null); // motricité
  const [mnaD, setMnaD] = useState(null); // maladie/stress
  const [mnaE, setMnaE] = useState(null); // neuropsycho
  const [mnaF, setMnaF] = useState(null); // IMC
  const [imcPoids, setImcPoids] = useState("");
  const [imcTaille, setImcTaille] = useState("");
  // MNA Évaluation globale G-R
  const [mnaG, setMnaG] = useState(null);
  const [mnaH, setMnaH] = useState(null);
  const [mnaI, setMnaI] = useState(null);
  const [mnaJ, setMnaJ] = useState(null);
  const [mnaK_lait, setMnaK_lait] = useState(null);
  const [mnaK_oeufs, setMnaK_oeufs] = useState(null);
  const [mnaK_viande, setMnaK_viande] = useState(null);
  const [mnaL, setMnaL] = useState(null);
  const [mnaM, setMnaM] = useState(null);
  const [mnaN, setMnaN] = useState(null);
  const [mnaO, setMnaO] = useState(null);
  const [mnaP, setMnaP] = useState(null);
  const [mnaQ, setMnaQ] = useState(null);
  const [mnaR, setMnaR] = useState(null);
  const mnaDepistage = () => (mnaA||0)+(mnaB||0)+(mnaC||0)+(mnaD||0)+(mnaE||0)+(mnaF||0);
  const mnaGlobale = () => (mnaG||0)+(mnaH||0)+(mnaI||0)+(mnaJ||0)+mnaKScore()+(mnaL||0)+(mnaM||0)+(mnaN||0)+(mnaO||0)+(mnaP||0)+(mnaQ||0)+(mnaR||0);
  const mnaKScore = () => { const n=[mnaK_lait,mnaK_oeufs,mnaK_viande].filter(v=>v===true).length; return n<=1?0:n===2?0.5:1; };'''

if OLD_MNA_STATES in code:
    code = code.replace(OLD_MNA_STATES, '  // MNA déplacé vers QCM Santé')
    fixes += 1; print("✅ FIX 2 — States MNA supprimés du QCM2")
else:
    print("⚠️ FIX 2 — States MNA non trouvés")

# ─── FIX 3 : Supprimer le commentaire MNA et tous les steps 6-25 du JSX ───
OLD_MNA_JSX_START = '      {/* ══ MNA DÉPISTAGE DÉNUTRITION (steps 6-11) + ÉVALUATION GLOBALE (12-19) ══ */}'
# Find this in code and remove everything up to closing </div>\n  );\n}
if OLD_MNA_JSX_START in code:
    start_idx = code.find(OLD_MNA_JSX_START)
    # Find the closing of QCM2 return: "    </div>\n  );\n}"
    # It's right before TransitionLLCScreen
    end_marker = '    </div>\n  );\n}\n\n\n/* ══ TRANSITION LLC → MEDAS ══ */'
    end_idx = code.find(end_marker)
    if end_idx != -1:
        # Remove from MNA start to </div>\n  );\n} (keep the closing tags)
        old_mna_block = code[start_idx:end_idx]
        code = code.replace(old_mna_block, '\n')
        fixes += 1; print("✅ FIX 3 — Bloc MNA JSX supprimé du QCM2")
    else:
        print("⚠️ FIX 3 — End marker non trouvé")
else:
    print("⚠️ FIX 3 — MNA JSX start non trouvé")

# ─── FIX 4 : Ajouter bouton "Retour au menu" dans MinijeuScreen après feedback ───
OLD_FEEDBACK = '''          {feedback && (
            <div style={{ background:feedbackColor==="#2e7d32"?"#e8f5e9":"#fbe9e7", border:`2px solid ${feedbackColor}`, borderRadius:12, padding:"12px 16px", fontSize:13, color:feedbackColor, fontWeight:700, textAlign:"center" }}>
              {feedback}
            </div>
          )}'''

NEW_FEEDBACK = '''          {feedback && (
            <div style={{ background:feedbackColor==="#2e7d32"?"#e8f5e9":"#fbe9e7", border:`2px solid ${feedbackColor}`, borderRadius:12, padding:"12px 16px", fontSize:13, color:feedbackColor, fontWeight:700, textAlign:"center" }}>
              {feedback}
            </div>
          )}
          <button onClick={onBack}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontSize:14, fontWeight:800, padding:"12px", cursor:"pointer", marginTop:4 }}>
            ← Retour au menu des missions
          </button>'''

if OLD_FEEDBACK in code:
    code = code.replace(OLD_FEEDBACK, NEW_FEEDBACK)
    fixes += 1; print("✅ FIX 4 — Bouton retour menu ajouté dans mini-jeu")
else:
    print("⚠️ FIX 4 — Feedback block non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
