"""
PATCH 10 — Recos QCM1 : enlever boutons recettes dans cartes + ajouter bouton retour menu
Usage: python patch_10_recos_boutons.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# FIX 1 — Enlever le bouton recettes dans chaque carte
OLD_BTN_RECO = '''              {/* Bouton recettes */}
              <button onClick={() => onVoirRecettes(reco.profil)}
                style={{ marginTop:14, background:reco.couleurHeader, color:"white", border:"none", borderRadius:10, padding:"10px 16px", fontSize:12, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Voir les recettes associées →
              </button>'''

if OLD_BTN_RECO in code:
    code = code.replace(OLD_BTN_RECO, '')
    fixes += 1
    print("✅ FIX 1 — Boutons recettes supprimés des cartes")
else:
    # sans le commentaire
    OLD_BTN_RECO2 = '''              <button onClick={() => onVoirRecettes(reco.profil)}
                style={{ marginTop:14, background:reco.couleurHeader, color:"white", border:"none", borderRadius:10, padding:"10px 16px", fontSize:12, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Voir les recettes associées →
              </button>'''
    if OLD_BTN_RECO2 in code:
        code = code.replace(OLD_BTN_RECO2, '')
        fixes += 1
        print("✅ FIX 1 — Boutons recettes supprimés des cartes (v2)")
    else:
        print("⚠️  FIX 1 — Bouton recettes non trouvé")

# FIX 2 — Ajouter bouton "Retour au menu" en bas de la page recos
OLD_CLOSING = '''    </div>

  );
}

/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */'''

NEW_CLOSING = '''      {/* Bouton retour menu */}
      <div style={{ padding:"0 32px 32px", background:"#f5f5f5" }}>
        <button onClick={onBack}
          style={{ width:"100%", background:"white", border:"3px solid #FA8072", borderRadius:14, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer" }}>
          ← Retour au menu cuisine
        </button>
      </div>

    </div>

  );
}

/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */'''

if OLD_CLOSING in code:
    code = code.replace(OLD_CLOSING, NEW_CLOSING)
    fixes += 1
    print("✅ FIX 2 — Bouton retour menu ajouté en bas")
else:
    print("⚠️  FIX 2 — Marqueur fermeture non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/2 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
