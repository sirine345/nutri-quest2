"""
PATCH 09 — RecommandationsQcm1Screen : refonte complète
- Header avec fond saumon + Max + message personnalisé
- Suppression des pourcentages incompréhensibles
- 4 cartes carrées avec en-tête colorée et conseils dedans
Usage: python patch_09_recos_qcm1_redesign.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

start_marker = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
end_marker   = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

if start_marker not in code or end_marker not in code:
    print("⚠️  Marqueurs non trouvés")
    sys.exit(1)

before = code[:code.index(start_marker)]
after  = code[code.index(end_marker):]

NEW_RECOS = '''/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {

  const RECOS_CONFIG = {
    legumes: {
      titre: "Fruits & légumes",
      couleurHeader: "#4caf50",
      bgHeader: "#e8f5e9",
      icon: "/legume2.png",
      icon2: "/fruit.png",
      pourquoi: "Le PNNS recommande au moins 5 portions (400g) par jour. Les fruits et légumes apportent vitamines, minéraux et fibres essentiels à la santé.",
      conseils: [
        "Ajoutez un légume à chaque repas (cru ou cuit)",
        "Mangez au moins un fruit entier par jour",
        "Préférez les légumes frais ou surgelés nature",
        "Les jus de fruits ne remplacent pas les fruits entiers",
      ],
      profil: "legumes",
    },
    legumineuses: {
      titre: "Légumes secs",
      couleurHeader: "#795548",
      bgHeader: "#efebe9",
      icon: "/legumesec.png",
      pourquoi: "Le PNNS recommande au moins 2 portions par semaine. Lentilles, pois chiches et haricots secs sont riches en fibres et protéines végétales.",
      conseils: [
        "Remplacez la viande par des légumineuses 2x/semaine",
        "Les lentilles corail cuisent en 10 min sans trempage",
        "Utilisez les pois chiches en conserve pour aller vite",
        "Pensez au houmous comme en-cas sain",
      ],
      profil: "legumineuses",
    },
    poisson: {
      titre: "Poisson",
      couleurHeader: "#0288d1",
      bgHeader: "#e1f5fe",
      icon: "/poisson.png",
      pourquoi: "Le PNNS recommande 2 portions par semaine, dont 1 poisson gras (sardine, maquereau, saumon). Riches en oméga-3, ils protègent le cœur et le cerveau.",
      conseils: [
        "Alternez poissons gras et maigres chaque semaine",
        "Les sardines en conserve comptent aussi !",
        "Remplacez la viande rouge par du poisson 2x/sem",
        "Évitez les poissons panés industriels",
      ],
      profil: "poisson",
    },
    charcuterie: {
      titre: "Charcuterie",
      couleurHeader: "#e53935",
      bgHeader: "#fbe9e7",
      icon: "/charcuterie.png",
      pourquoi: "La charcuterie est classée cancérigène groupe 1 par l'OMS. Le PNNS recommande de la limiter à 150g/semaine maximum (jambon, saucisson, saucisses…).",
      conseils: [
        "Remplacez la charcuterie par des œufs ou du poulet",
        "Lisez les étiquettes : sel et graisses sont cachés",
        "Choisissez du jambon blanc plutôt que du saucisson",
        "Réduisez progressivement pour ne pas vous frustrer",
      ],
      profil: "charcuterie",
    },
    fastFood: {
      titre: "Fast food",
      couleurHeader: "#e65100",
      bgHeader: "#fbe9e7",
      icon: "/fast_food.png",
      pourquoi: "Les aliments ultra-transformés sont liés à l'obésité, au diabète et aux maladies cardiovasculaires. Le PNNS recommande de privilégier le fait maison.",
      conseils: [
        "Cuisinez en grande quantité et congelez les restes",
        "Préparez des repas simples en 20 min (œufs, légumes)",
        "Si fast food : préférez les salades et l'eau",
        "Planifiez vos repas en début de semaine",
      ],
      profil: "fastFood",
    },
    sucres: {
      titre: "Sucreries",
      couleurHeader: "#f57c00",
      bgHeader: "#fff3e0",
      icon: "/sucrerie.png",
      pourquoi: "Les sucres ajoutés favorisent les caries, le surpoids et le diabète de type 2. Le PNNS recommande de les limiter au maximum.",
      conseils: [
        "Remplacez les sucreries par des fruits frais",
        "Le sucre ajouté se cache partout : lisez les étiquettes",
        "Cuisinez vos desserts vous-même (moins de sucre)",
        "Remplacez les boissons sucrées par de l'eau",
      ],
      profil: "sucres",
    },
  };

  // Calcul des recos à afficher selon le profil nutrition
  const recoKeys = [];
  if ((nutrition.legumes||0) < 60 || (nutrition.fruits||0) < 60) recoKeys.push("legumes");
  if ((nutrition.legumineuses||0) < 50) recoKeys.push("legumineuses");
  if ((nutrition.poisson||0) < 50) recoKeys.push("poisson");
  if ((nutrition.charcuterie||0) > 20) recoKeys.push("charcuterie");
  if ((nutrition.fastFood||0) > 20) recoKeys.push("fastFood");
  if ((nutrition.sucres||0) > 20) recoKeys.push("sucres");

  // On garde max 4 recos pour les cartes
  const recos = recoKeys.slice(0, 4).map(k => RECOS_CONFIG[k]);

  return (
    <div style={{ position:"fixed", inset:0, background:"#f5f5f5", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon avec Max — même style que page Profil */}
      <div style={{ background:"#FA8072", padding:"20px 32px 28px", position:"relative", overflow:"hidden" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.25)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"6px 14px", marginBottom:16, position:"relative", zIndex:2 }}>← Retour</button>

        <div style={{ display:"flex", alignItems:"flex-end", gap:20, position:"relative", zIndex:2 }}>
          {/* Max */}
          <img src="/e.png" alt="Max" style={{ width:110, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))", flexShrink:0 }} />
          {/* Bulle dialogue */}
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"14px 18px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", flex:1, maxWidth:600 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:4 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.6 }}>
              Voici tes <strong style={{ color:"#FA8072" }}>recommandations personnalisées</strong> basées sur tes habitudes alimentaires. Chaque conseil est tiré des recommandations officielles du <strong>Programme National Nutrition Santé</strong>.
            </div>
          </div>
        </div>

        {/* Titre */}
        <div style={{ marginTop:20, position:"relative", zIndex:2 }}>
          <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>Résultats · QCM Habitudes alimentaires</div>
          <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:32, fontWeight:900, color:"white", textShadow:"2px 2px 0 rgba(0,0,0,0.2)", margin:0, lineHeight:1.1 }}>
            Mes Recommandations<br/><span style={{ color:"#ffdd44" }}>Personnalisées</span>
          </h1>
        </div>
      </div>

      {/* Intro */}
      <div style={{ background:"white", padding:"16px 32px", borderBottom:"2px solid #eee" }}>
        {recos.length === 0
          ? <div style={{ fontSize:15, fontWeight:800, color:"#2e7d32" }}>🎉 Excellentes habitudes ! Tes résultats sont proches des recommandations du PNNS.</div>
          : <div style={{ fontSize:13, color:"#555", lineHeight:1.6 }}>
              <strong>{recos.length} point{recos.length > 1 ? "s" : ""} à améliorer</strong> ont été identifiés dans tes habitudes alimentaires. Clique sur une carte pour voir les conseils détaillés.
            </div>
        }
      </div>

      {/* Grille 2x2 de cartes */}
      <div style={{ padding:"24px 32px 32px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        {recos.map((reco, i) => (
          <div key={i} style={{ background:"white", borderRadius:18, overflow:"hidden", boxShadow:"0 4px 20px rgba(0,0,0,0.1)", border:"2px solid " + reco.couleurHeader + "33" }}>

            {/* En-tête colorée */}
            <div style={{ background:reco.bgHeader, borderBottom:"2px solid " + reco.couleurHeader + "44", padding:"16px 18px", display:"flex", alignItems:"center", gap:12 }}>
              <img src={reco.icon} alt="" style={{ width:44, height:44, objectFit:"contain", filter:"drop-shadow(1px 2px 4px rgba(0,0,0,0.15))" }} />
              {reco.icon2 && <img src={reco.icon2} alt="" style={{ width:34, height:34, objectFit:"contain", marginLeft:-10, filter:"drop-shadow(1px 2px 4px rgba(0,0,0,0.15))" }} />}
              <div>
                <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, color:reco.couleurHeader }}>{reco.titre}</div>
                <div style={{ fontSize:11, color:"#666", marginTop:2 }}>Recommandation PNNS</div>
              </div>
            </div>

            {/* Contenu */}
            <div style={{ padding:"16px 18px" }}>
              {/* Pourquoi */}
              <div style={{ fontSize:12, color:"#444", lineHeight:1.65, marginBottom:14, padding:"10px 12px", background:"#fafafa", borderRadius:8, borderLeft:"3px solid " + reco.couleurHeader }}>
                {reco.pourquoi}
              </div>

              {/* Conseils */}
              <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
                {reco.conseils.map((c, j) => (
                  <div key={j} style={{ display:"flex", gap:10, alignItems:"flex-start" }}>
                    <div style={{ width:22, height:22, borderRadius:6, background:reco.bgHeader, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:11, fontWeight:900, color:reco.couleurHeader, marginTop:1 }}>{j+1}</div>
                    <span style={{ fontSize:12, color:"#333", lineHeight:1.55 }}>{c}</span>
                  </div>
                ))}
              </div>

              {/* Bouton recettes */}
              <button onClick={() => onVoirRecettes(reco.profil)}
                style={{ marginTop:14, background:reco.couleurHeader, color:"white", border:"none", borderRadius:10, padding:"10px 16px", fontSize:12, fontWeight:800, cursor:"pointer", width:"100%" }}>
                Voir les recettes associées →
              </button>
            </div>
          </div>
        ))}

        {/* Si moins de 4 recos, carte "Bravo" */}
        {recos.length > 0 && recos.length < 4 && (
          <div style={{ background:"white", borderRadius:18, overflow:"hidden", boxShadow:"0 4px 20px rgba(0,0,0,0.1)", border:"2px solid #9ACD3244", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"32px 24px", textAlign:"center" }}>
            <div style={{ fontSize:48, marginBottom:12 }}>🎉</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"#9ACD32", marginBottom:8 }}>Bonne nouvelle !</div>
            <div style={{ fontSize:13, color:"#666", lineHeight:1.6 }}>Pour les autres groupes alimentaires, tes habitudes sont déjà proches des recommandations du PNNS. Continue comme ça !</div>
          </div>
        )}
      </div>

    </div>
  );
}

'''

code = before + NEW_RECOS + after
out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ FIX 1 — RecommandationsQcm1Screen entièrement refaite")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
