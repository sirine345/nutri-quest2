"""
PATCH 22 — RecommandationsQcm2Screen : Fabrique à menus option C
Grands personnages, grande police, onglets, planning semaine
Usage: python patch_22_recos_qcm2_fabrique.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

def find_func_end(lines, start):
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth <= 0 and i > start:
            return i
    return len(lines) - 1

starts = [i for i, l in enumerate(lines) if 'function RecommandationsQcm2Screen' in l]
if not starts:
    print("⚠️  RecommandationsQcm2Screen non trouvé")
    sys.exit(1)

start_idx = starts[0]
block_start = start_idx
for offset in range(1, 4):
    if start_idx - offset >= 0 and '/* ══' in lines[start_idx - offset]:
        block_start = start_idx - offset
        break

block_end = find_func_end(lines, start_idx)
print(f"Remplacement lignes {block_start+1}–{block_end+1}")

NEW_BLOCK = '''/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */
function RecommandationsQcm2Screen({ answers, playerName, avatarChoice, onBack }) {
  const [onglet, setOnglet] = React.useState("pour_vous");
  const [dateDebut, setDateDebut] = React.useState("");
  const [dateFin, setDateFin] = React.useState("");
  const [planning, setPlanning] = React.useState(null);

  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";
  const pratiques = answers[" Pratiques alimentaires"] || "";
  const cuisine   = answers["‍ En cuisine"] || "";
  const compo     = answers[" Composition du repas"] || "";

  const sansPorc    = pratiques.toLowerCase().includes("porc");
  const sansViande  = pratiques.toLowerCase().includes("viande");
  const pasTemps    = cuisine.toLowerCase().includes("pas le temps");
  const aimeTemps   = cuisine.toLowerCase().includes("aime");
  const veutEntree  = compo.toLowerCase().includes("entrée");
  const veutDessert = compo.toLowerCase().includes("dessert");

  const toutes = RECETTES_DATA || [];

  const filtrees = toutes.filter(r => {
    if (sansPorc    && r.profils && r.profils.includes("porc")) return false;
    if (sansViande  && r.profils && r.profils.includes("viande")) return false;
    if (pasTemps    && r.temps > 20) return false;
    return true;
  });

  const pourVous = filtrees.length > 0 ? filtrees : toutes;

  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;
    const start = new Date(dateDebut);
    const end   = new Date(dateFin);
    const jours = [];
    const noms  = ["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"];
    const mois  = ["jan","fév","mar","avr","mai","juin","juil","aoû","sep","oct","nov","déc"];
    let cur = new Date(start);
    let idx = 0;
    while (cur <= end && jours.length < 14) {
      const recDej  = pourVous[idx % pourVous.length];
      const recDin  = pourVous[(idx + 1) % pourVous.length];
      jours.push({
        nom: noms[cur.getDay()],
        date: `${cur.getDate()} ${mois[cur.getMonth()]}`,
        dej:  recDej?.name  || "Salade composée",
        din:  recDin?.name  || "Soupe + pain",
      });
      cur.setDate(cur.getDate() + 1);
      idx += 2;
    }
    setPlanning(jours);
  };

  const RecetteCard = ({ r }) => (
    <div style={{ background:"white", borderRadius:18, overflow:"hidden", border:"1.5px solid #eee", boxShadow:"0 2px 12px rgba(0,0,0,0.06)" }}>
      <div style={{ height:130, background:"#f5f5f5", display:"flex", alignItems:"center", justifyContent:"center", position:"relative", overflow:"hidden" }}>
        <img src={r.image || "/repas.png"} alt={r.name} style={{ width:"100%", height:"100%", objectFit:"cover" }}
          onError={e => { e.target.style.display="none"; }} />
        {r.profils && r.profils.includes("rapide") && (
          <span style={{ position:"absolute", top:10, left:10, fontSize:12, fontWeight:900, background:"#FA8072", color:"white", padding:"4px 10px", borderRadius:20 }}>⚡ Rapide</span>
        )}
        {(sansPorc || sansViande) && (
          <span style={{ position:"absolute", top:10, right:10, fontSize:12, fontWeight:900, background:"#4caf50", color:"white", padding:"4px 10px", borderRadius:20 }}>✓ Adapté</span>
        )}
      </div>
      <div style={{ padding:"14px 16px" }}>
        <div style={{ fontSize:16, fontWeight:900, color:"#1A1A1A", fontFamily:"Arial Black, Arial, sans-serif", marginBottom:6 }}>{r.name}</div>
        {r.temps && <div style={{ fontSize:13, color:"#888", marginBottom:4 }}>⏱️ {r.temps} min</div>}
        {r.description && <div style={{ fontSize:13, color:"#555", lineHeight:1.6, marginTop:4 }}>{r.description?.slice(0,80)}…</div>}
      </div>
    </div>
  );

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon avec personnages */}
      <div style={{ background:"#FA8072", padding:"20px 32px 24px" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:14, fontWeight:800, cursor:"pointer", padding:"7px 16px", marginBottom:16 }}>← Retour</button>
        <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"white", marginBottom:16 }}>
          Ma fabrique à menus personnalisés 🍽️
        </div>
        <div style={{ display:"flex", alignItems:"flex-end", gap:24 }}>
          {/* Max grand */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8, flexShrink:0 }}>
            <img src="/e.png" alt="Max" style={{ height:180, objectFit:"contain", filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.25))" }} />
            <span style={{ fontSize:13, fontWeight:900, color:"white", background:"rgba(255,255,255,0.2)", padding:"4px 14px", borderRadius:20 }}>Max</span>
          </div>
          {/* Bulle Max */}
          <div style={{ flex:1 }}>
            <div style={{ background:"white", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"4px 4px 0 rgba(0,0,0,0.2)", marginBottom:8 }}>
              <div style={{ fontSize:11, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.1em", color:"#c4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
              <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                Voici tes recettes personnalisées ! 🌟<br/>
                <span style={{ fontSize:14, fontWeight:600, color:"#555" }}>
                  {sansPorc ? "J'ai retiré toutes les recettes avec du porc. " : ""}
                  {sansViande ? "J'ai sélectionné des recettes végétariennes. " : ""}
                  {pasTemps ? "J'ai choisi des recettes rapides (moins de 20 min) !" : ""}
                  {aimeTemps ? "J'ai inclus des recettes élaborées pour profiter du plaisir de cuisiner !" : ""}
                </span>
              </div>
            </div>
          </div>
          {/* Avatar grand */}
          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8, flexShrink:0 }}>
            <div style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:"14px 14px 4px 14px", padding:"12px 14px", fontSize:14, color:"white", fontWeight:700, textAlign:"center", maxWidth:130, lineHeight:1.5, marginBottom:4 }}>
              Génial ! J'ai hâte de voir ! 😍
            </div>
            <img src={avatarSrc} alt={playerName} style={{ height:150, objectFit:"contain", filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.25))" }} />
            <span style={{ fontSize:13, fontWeight:900, color:"white", background:"rgba(255,255,255,0.2)", padding:"4px 14px", borderRadius:20 }}>{playerName}</span>
          </div>
        </div>
      </div>

      {/* Onglets */}
      <div style={{ display:"flex", background:"white", borderBottom:"2px solid #eee", position:"sticky", top:0, zIndex:10 }}>
        {[
          { id:"pour_vous", label:"❤️ Recettes pour vous" },
          { id:"toutes",    label:"🍽️ Toutes les recettes" },
          { id:"semaine",   label:"📅 Ma semaine type" },
        ].map(o => (
          <button key={o.id} onClick={() => setOnglet(o.id)}
            style={{ flex:1, padding:"14px 8px", fontSize:14, fontWeight:900, fontFamily:"Arial Black, Arial, sans-serif", cursor:"pointer", border:"none", background:"none", borderBottom: onglet===o.id ? "3px solid #FA8072" : "3px solid transparent", color: onglet===o.id ? "#FA8072" : "#888", transition:"all 0.2s" }}>
            {o.label}
          </button>
        ))}
      </div>

      {/* Contenu onglet "Recettes pour vous" */}
      {onglet === "pour_vous" && (
        <div style={{ padding:"24px 32px" }}>
          {/* Badges filtres actifs */}
          <div style={{ display:"flex", flexWrap:"wrap", gap:8, marginBottom:20 }}>
            <span style={{ fontSize:13, color:"#888", fontWeight:700, alignSelf:"center" }}>Filtres actifs :</span>
            {sansPorc    && <span style={{ background:"#e1f5fe", color:"#0277bd", fontSize:13, fontWeight:800, padding:"5px 14px", borderRadius:20, border:"1.5px solid #0277bd44" }}>Sans porc</span>}
            {sansViande  && <span style={{ background:"#e8f5e9", color:"#2e7d32", fontSize:13, fontWeight:800, padding:"5px 14px", borderRadius:20, border:"1.5px solid #2e7d3244" }}>Sans viande</span>}
            {pasTemps    && <span style={{ background:"#fff3e0", color:"#e65100", fontSize:13, fontWeight:800, padding:"5px 14px", borderRadius:20, border:"1.5px solid #e6510044" }}>Rapide ≤ 20 min</span>}
            {!sansPorc && !sansViande && !pasTemps && <span style={{ background:"#f5f5f5", color:"#888", fontSize:13, padding:"5px 14px", borderRadius:20 }}>Toutes pratiques</span>}
          </div>

          {/* Suggestions si composition incomplète */}
          {!veutEntree && (
            <div style={{ background:"#fff8e1", borderRadius:14, padding:"14px 18px", marginBottom:20, border:"1.5px solid #f57c0044" }}>
              <div style={{ fontSize:15, fontWeight:900, color:"#e65100", marginBottom:6 }}>💡 Et si tu essayais des entrées ?</div>
              <div style={{ fontSize:14, color:"#555", lineHeight:1.6 }}>Tu n'as pas coché "Entrée" dans ta composition habituelle. Voici quelques idées légères pour commencer le repas.</div>
            </div>
          )}
          {!veutDessert && (
            <div style={{ background:"#fce4ec", borderRadius:14, padding:"14px 18px", marginBottom:20, border:"1.5px solid #e91e6344" }}>
              <div style={{ fontSize:15, fontWeight:900, color:"#c2185b", marginBottom:6 }}>🍮 Des idées de desserts sains ?</div>
              <div style={{ fontSize:14, color:"#555", lineHeight:1.6 }}>Tu ne prends pas souvent de dessert. Voici des options légères et nutritives pour terminer le repas.</div>
            </div>
          )}

          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
            {pourVous.slice(0, 8).map((r, i) => <RecetteCard key={i} r={r} />)}
          </div>
          {pourVous.length === 0 && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#888", fontSize:16 }}>
              Aucune recette ne correspond à tes filtres actuels.
            </div>
          )}
        </div>
      )}

      {/* Contenu onglet "Toutes les recettes" */}
      {onglet === "toutes" && (
        <div style={{ padding:"24px 32px" }}>
          <div style={{ fontSize:16, fontWeight:900, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", marginBottom:20 }}>
            Toutes les recettes ({toutes.length})
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
            {toutes.map((r, i) => <RecetteCard key={i} r={r} />)}
          </div>
        </div>
      )}

      {/* Contenu onglet "Ma semaine type" */}
      {onglet === "semaine" && (
        <div style={{ padding:"24px 32px" }}>
          <div style={{ fontSize:16, fontWeight:900, color:"#FA8072", fontFamily:"Arial Black, Arial, sans-serif", marginBottom:8 }}>
            Génère ton planning de la semaine
          </div>
          <div style={{ fontSize:14, color:"#666", marginBottom:20, lineHeight:1.6 }}>
            Choisis tes dates et je te propose 3 repas par jour avec des recettes adaptées à tes préférences.
          </div>

          {/* Sélection dates */}
          <div style={{ background:"white", borderRadius:18, padding:"20px 24px", marginBottom:24, border:"2px solid #eee", display:"flex", alignItems:"center", gap:16, flexWrap:"wrap" }}>
            <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
              <label style={{ fontSize:13, fontWeight:800, color:"#555" }}>Date de début</label>
              <input type="date" value={dateDebut} onChange={e => setDateDebut(e.target.value)}
                style={{ fontSize:15, padding:"10px 14px", borderRadius:10, border:"2px solid #eee", fontFamily:"Arial, sans-serif", cursor:"pointer" }} />
            </div>
            <div style={{ fontSize:20, color:"#FA8072", fontWeight:900, marginTop:18 }}>→</div>
            <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
              <label style={{ fontSize:13, fontWeight:800, color:"#555" }}>Date de fin</label>
              <input type="date" value={dateFin} onChange={e => setDateFin(e.target.value)}
                style={{ fontSize:15, padding:"10px 14px", borderRadius:10, border:"2px solid #eee", fontFamily:"Arial, sans-serif", cursor:"pointer" }} />
            </div>
            <button onClick={genererPlanning}
              style={{ marginTop:18, background:"#FA8072", border:"2px solid #222", borderRadius:12, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"11px 24px", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>
              Générer mon planning →
            </button>
          </div>

          {/* Planning généré */}
          {planning && (
            <div style={{ display:"flex", flexDirection:"column", gap:14 }}>
              {planning.map((j, i) => (
                <div key={i} style={{ background:"white", borderRadius:16, border:"2px solid #eee", overflow:"hidden" }}>
                  {/* En-tête jour */}
                  <div style={{ background:"#FA8072", padding:"12px 20px", display:"flex", alignItems:"center", gap:10 }}>
                    <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"white" }}>{j.nom}</span>
                    <span style={{ fontSize:14, color:"rgba(255,255,255,0.85)" }}>{j.date}</span>
                  </div>
                  {/* 3 repas */}
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:0 }}>
                    {[
                      { emoji:"🌅", repas:"Petit-déjeuner", plat:"Yaourt + fruit + pain complet" },
                      { emoji:"☀️", repas:"Déjeuner",       plat:j.dej },
                      { emoji:"🌙", repas:"Dîner",          plat:j.din },
                    ].map((r, ri) => (
                      <div key={ri} style={{ padding:"14px 16px", borderRight: ri < 2 ? "1px solid #f0f0f0" : "none" }}>
                        <div style={{ fontSize:22, marginBottom:6 }}>{r.emoji}</div>
                        <div style={{ fontSize:12, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:"0.5px", marginBottom:4 }}>{r.repas}</div>
                        <div style={{ fontSize:14, fontWeight:700, color:"#1A1A1A", lineHeight:1.5 }}>{r.plat}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {!planning && (
            <div style={{ textAlign:"center", padding:"40px 20px", color:"#aaa", fontSize:15 }}>
              Choisis tes dates ci-dessus pour générer ton planning 📅
            </div>
          )}
        </div>
      )}

    </div>
  );
}

'''

lines[block_start:block_end+1] = [NEW_BLOCK]
print("✅ FIX 1 — RecommandationsQcm2Screen : fabrique à menus complète")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
