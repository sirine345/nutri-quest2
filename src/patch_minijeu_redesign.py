"""
PATCH — Redesign MinijeuScreen selon demandes prof :
- Fond blanc, pas de décor
- Aliments prennent la moitié gauche, grand format
- Assiettes à droite (2 en haut + 1 en dessous si besoin)
- Fond assiettes blanc, rebord bleu ciel
- Aliments rangés par catégories PNNS
Usage: python patch_minijeu_redesign.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Find MinijeuScreen and replace FOODS_LIST + function
OLD_FOODS = '''const FOODS_LIST = [
  { id:"legumes",     emoji:"/legume2.png", name:"Légumes",     type:"plate", pnns:"legumes",   good:true  },
  { id:"feculents",   emoji:"/feculent.png", name:"Féculents",   type:"plate", pnns:"feculents", good:true  },
  { id:"poisson",     emoji:"/poisson.png", name:"Poisson",     type:"plate", pnns:"proteines", good:true  },
  { id:"viande",      emoji:"/viande.png", name:"Viande",      type:"plate", pnns:"proteines", good:true  },
  { id:"fruits",      emoji:"/fruit.png", name:"Fruits",      type:"plate", pnns:"fruits",    good:true  },
  { id:"oeuf",        emoji:"/oeuf.png", name:"Oeuf",        type:"plate", pnns:"proteines", good:true  },
  { id:"charcuterie", emoji:"/charcuterie.png", name:"Charcuterie", type:"plate", pnns:"bad",       good:false },
  { id:"fastfood",    emoji:"/fast_food.png", name:"Fast food",   type:"plate", pnns:"bad",       good:false },
  { id:"legumesec",   emoji:"/legumesec.png", name:"Légum. secs", type:"plate", pnns:"legumes",   good:true  },
  { id:"fromage",     emoji:"/fromage.png", name:"Fromage",     type:"plate", pnns:"laitiers",  good:true  },
  { id:"salade",      emoji:"/salade.png", name:"Salade",      type:"entree", pnns:"legumes",  good:true  },
  { id:"soupe",       emoji:"/soupe.png", name:"Soupe",       type:"entree", pnns:"legumes",  good:true  },
  { id:"crudites",    emoji:"/crudité.png", name:"Crudités",    type:"entree", pnns:"legumes",  good:true  },
  { id:"avocat",      emoji:"/avocat.png", name:"Avocat",      type:"entree", pnns:"legumes",  good:true  },
  { id:"yaourt",      emoji:"/yaourt.png", name:"Yaourt",      type:"dessert", pnns:"laitiers", good:true  },
  { id:"compote",     emoji:"/compote.png", name:"Compote",     type:"dessert", pnns:"fruits",  good:true  },
  { id:"gateau",      emoji:"/gateau.png", name:"Gâteau",      type:"dessert", pnns:"bad",     good:false },
  { id:"fraise",      emoji:"/fruit.png", name:"Fruit rouge", type:"dessert", pnns:"fruits",  good:true  },
  { id:"eau",  emoji:"/eau.png", name:"Eau",       type:"glass", pnns:"eau",  good:true,  color:"#85B7EB" },
  { id:"jus",  emoji:"/jus_de_fruit.png", name:"Jus fruit", type:"glass", pnns:"jus",  good:true,  color:"#EF9F27" },
  { id:"soda", emoji:"/soda.png", name:"Soda",      type:"glass", pnns:"bad",  good:false, color:"#E24B4A" },
  { id:"lait", emoji:"/lait2.png", name:"Lait",      type:"glass", pnns:"lait", good:true,  color:"#B5D4F4" },
];'''

NEW_FOODS = '''const FOODS_LIST = [
  // Fruits & légumes
  { id:"legumes",     emoji:"/legume2.png",      name:"Légumes",       type:"plate",  pnns:"legumes",   good:true,  categorie:"Fruits & légumes" },
  { id:"fruits",      emoji:"/fruit.png",         name:"Fruits",        type:"plate",  pnns:"fruits",    good:true,  categorie:"Fruits & légumes" },
  { id:"salade",      emoji:"/salade.png",        name:"Salade",        type:"entree", pnns:"legumes",   good:true,  categorie:"Fruits & légumes" },
  { id:"crudites",    emoji:"/crudité.png",       name:"Crudités",      type:"entree", pnns:"legumes",   good:true,  categorie:"Fruits & légumes" },
  { id:"avocat",      emoji:"/avocat.png",        name:"Avocat",        type:"entree", pnns:"legumes",   good:true,  categorie:"Fruits & légumes" },
  { id:"soupe",       emoji:"/soupe.png",         name:"Soupe",         type:"entree", pnns:"legumes",   good:true,  categorie:"Fruits & légumes" },
  { id:"compote",     emoji:"/compote.png",       name:"Compote",       type:"dessert",pnns:"fruits",    good:true,  categorie:"Fruits & légumes" },
  // Viande, volaille, œufs, poisson
  { id:"viande",      emoji:"/viande.png",        name:"Viande",        type:"plate",  pnns:"proteines", good:true,  categorie:"Viande, volaille, œuf, poisson" },
  { id:"poisson",     emoji:"/poisson.png",       name:"Poisson",       type:"plate",  pnns:"proteines", good:true,  categorie:"Viande, volaille, œuf, poisson" },
  { id:"oeuf",        emoji:"/oeuf.png",          name:"Œuf",           type:"plate",  pnns:"proteines", good:true,  categorie:"Viande, volaille, œuf, poisson" },
  { id:"charcuterie", emoji:"/charcuterie.png",   name:"Charcuterie",   type:"plate",  pnns:"bad",       good:false, categorie:"Viande, volaille, œuf, poisson" },
  // Céréales & dérivés
  { id:"feculents",   emoji:"/feculent.png",      name:"Féculents",     type:"plate",  pnns:"feculents", good:true,  categorie:"Céréales & dérivés" },
  // Pomme de terre & légumes secs
  { id:"legumesec",   emoji:"/legumesec.png",     name:"Légumes secs",  type:"plate",  pnns:"legumes",   good:true,  categorie:"Pomme de terre & légumes secs" },
  // Lait & produits laitiers
  { id:"fromage",     emoji:"/fromage.png",       name:"Fromage",       type:"plate",  pnns:"laitiers",  good:true,  categorie:"Lait & produits laitiers" },
  { id:"yaourt",      emoji:"/yaourt.png",        name:"Yaourt",        type:"dessert",pnns:"laitiers",  good:true,  categorie:"Lait & produits laitiers" },
  // Matières grasses
  // Sucres & produits sucrés
  { id:"gateau",      emoji:"/gateau.png",        name:"Gâteau",        type:"dessert",pnns:"bad",       good:false, categorie:"Sucres & produits sucrés" },
  { id:"fraise",      emoji:"/fruit.png",         name:"Fruit rouge",   type:"dessert",pnns:"fruits",    good:true,  categorie:"Sucres & produits sucrés" },
  // Fast food
  { id:"fastfood",    emoji:"/fast_food.png",     name:"Fast food",     type:"plate",  pnns:"bad",       good:false, categorie:"Sucres & produits sucrés" },
  // Boissons
  { id:"eau",         emoji:"/eau.png",           name:"Eau",           type:"glass",  pnns:"eau",       good:true,  color:"#85B7EB", categorie:"Boissons" },
  { id:"jus",         emoji:"/jus_de_fruit.png",  name:"Jus de fruit",  type:"glass",  pnns:"jus",       good:true,  color:"#EF9F27", categorie:"Boissons" },
  { id:"soda",        emoji:"/soda.png",          name:"Soda",          type:"glass",  pnns:"bad",       good:false, color:"#E24B4A", categorie:"Boissons" },
  { id:"lait",        emoji:"/lait2.png",         name:"Lait",          type:"glass",  pnns:"lait",      good:true,  color:"#B5D4F4", categorie:"Boissons" },
];

const CATEGORIES_PNNS = [
  "Fruits & légumes",
  "Viande, volaille, œuf, poisson",
  "Céréales & dérivés",
  "Pomme de terre & légumes secs",
  "Lait & produits laitiers",
  "Sucres & produits sucrés",
  "Boissons",
];'''

if OLD_FOODS in code:
    code = code.replace(OLD_FOODS, NEW_FOODS)
    print("✅ FOODS_LIST + catégories PNNS")
else:
    print("⚠️ FOODS_LIST non trouvée")

# Now replace MinijeuScreen return JSX
OLD_RETURN = '''  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond1.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <span style={{ color:"white", fontWeight:900, fontSize:14 }}>Compose ton repas</span>
        <div style={{ display:"flex", gap:10 }}>
          <button onClick={reset} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"4px 12px", cursor:"pointer" }}>Réinitialiser</button>
          <button onClick={onBack} style={{ background:"#ffcc00", border:"2px solid #222", borderRadius:8, color:"#222", fontSize:12, fontWeight:800, padding:"4px 12px", cursor:"pointer", boxShadow:"2px 2px 0 #222" }}>← Menu</button>
        </div>
      </div>
      <div style={{ position:"relative", zIndex:1, display:"grid", gridTemplateColumns:"280px 1fr 120px", height:"100vh", paddingTop:50 }}>
        <div style={{ background:"rgba(255,255,255,0.95)", borderRight:"3px solid #222", overflowY:"auto", padding:16 }}>
          {[{ label:"Entrée", type:"entree" },{ label:"Plat", type:"plate" },{ label:"Dessert", type:"dessert" },{ label:"Boisson", type:"glass" }].filter(s => {
            if (s.type === "entree" && !showEntree) return false;
            if (s.type === "dessert" && !showDessert) return false;
            return true;
          }).map(section => (
            <details key={section.type} open style={{ marginBottom:12 }}>
              <summary style={{ fontSize:11, fontWeight:900, textTransform:"uppercase", letterSpacing:2, color:"#c4622d", marginBottom:8, cursor:"pointer", listStyle:"none", display:"flex", justifyContent:"space-between", alignItems:"center", padding:"4px 0" }}>{section.label} <span></span></summary>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginTop:6 }}>
                {FOODS_LIST.filter(f=>f.type===section.type).map(food => {
                  const used = usedIds.includes(food.id);
                  return (
                    <div key={food.id} draggable={!used} onDragStart={() => !used && setDragId(food.id)} onDragEnd={() => setDragId(null)}
                      style={{ background:used?"#f0f0f0":"white", border:`2px solid ${used?"#ccc":food.good?"#9ACD32":"#E24B4A"}`, borderRadius:12, padding:"10px 6px", textAlign:"center", cursor:used?"not-allowed":"grab", opacity:used?0.4:1, transition:"opacity 0.2s" }}>
                      {food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:52, height:52, objectFit:"contain" }} /> : <div style={{ fontSize:36 }}>{food.emoji}</div>}
                      <div style={{ fontSize:11, fontWeight:800, color:"#333", marginTop:4 }}>{food.name}</div>
                    </div>
                  );
                })}
              </div>
            </details>
          ))}
          <div style={{ marginTop:12, fontSize:11, color:"#888", lineHeight:1.6 }}><span style={{ color:"#9ACD32", fontWeight:700 }}>Vert</span> = recommandé PNNS<br/><span style={{ color:"#E24B4A", fontWeight:700 }}>Rouge</span> = déconseillé</div>
        </div>
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"space-between", padding:16, paddingTop:20, paddingBottom:16 }}>
          <div style={{ textAlign:"center" }}>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:42, fontWeight:900, color:"white", letterSpacing:2, textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:0, lineHeight:1.1 }}>Compose ton repas</h1>
            <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto" }} />
            <p style={{ color:"rgba(255,255,255,0.9)", fontSize:14, margin:0, fontWeight:700 }}>Glisse les aliments sur les assiettes · la boisson sur le verre</p>
          </div>
          <div style={{ display:"flex", alignItems:"center", gap:32 }}>
            {showEntree && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
                <div style={{ fontSize:13, color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Entrée</div>
                <AssietteDrop zone="entree" items={entree} onRemove={removeFromEntree} size={180} maxItems={2} />
              </div>
            )}
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
              <div style={{ fontSize:13, color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Plat principal</div>
              <AssietteDrop zone="plate" items={plate} onRemove={removeFromPlate} size={240} maxItems={5} />
            </div>
            {showDessert && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
                <div style={{ fontSize:13, color:"white", fontWeight:900, textTransform:"uppercase", letterSpacing:1, textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>Dessert</div>
                <AssietteDrop zone="dessert" items={dessert} onRemove={removeFromDessert} size={180} maxItems={2} />
              </div>
            )}
          </div>
          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
            <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("glass")} onClick={removeGlass}
              style={{ width:55, height:85, borderRadius:"0 0 10px 10px", border:"3px solid white", background:glass?glass.color+"99":"rgba(255,255,255,0.2)", overflow:"hidden", cursor:glass?"pointer":"default", position:"relative", boxShadow:"0 4px 12px rgba(0,0,0,0.2)" }}>
              {glass && <div style={{ position:"absolute", bottom:0, left:0, right:0, height:"80%", background:glass.color, opacity:0.7, borderRadius:"0 0 8px 8px" }} />}
              {glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center" }}>{glass.emoji.endsWith(".png") ? <img src={glass.emoji} style={{ width:30, height:30, objectFit:"contain" }} /> : <span style={{ fontSize:24 }}>{glass.emoji}</span>}</div>}
            </div>
            <div style={{ fontSize:11, color:"white", fontWeight:800, letterSpacing:1, textTransform:"uppercase", textShadow:"1px 1px 0 rgba(0,0,0,0.4)" }}>{glass ? glass.name : "Boisson"}</div>
            <button onClick={valider} style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:12, color:"#222", fontSize:15, fontWeight:800, padding:"11px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222", marginBottom:"40px" }}>Valider mon repas</button>
            {feedback && (<div style={{ background:"white", border:"3px solid #222", borderRadius:12, padding:"12px 20px", maxWidth:420, fontSize:13, lineHeight:1.6, color:feedbackColor, fontWeight:700, boxShadow:"4px 4px 0 #222", textAlign:"center", marginBottom:"40px" }}>{feedback}</div>)}
          </div>
        </div>
        <div style={{ background:"rgba(255,255,255,0.95)", borderLeft:"3px solid #222", padding:"60px 14px 12px", display:"flex", flexDirection:"column", gap:10 }}>
          <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:1, color:"#c4622d", marginBottom:8 }}>Équilibre PNNS</div>
          {[{ key:"legumes", label:"Légumes", color:"#639922" },{ key:"feculents", label:"Féculents", color:"#EF9F27" },{ key:"proteines", label:"Protéines", color:"#378ADD" },{ key:"fruits", label:"Fruits", color:"#D4537E" },{ key:"laitiers", label:"Laitiers", color:"#B5D4F4" },{ key:"eau", label:"Boisson", color:"#85B7EB" }].map(b => (
            <div key={b.key}>
              <div style={{ fontSize:10, color:"#555", marginBottom:3, fontWeight:700 }}>{b.label}</div>
              <div style={{ height:8, background:"#eee", borderRadius:99, overflow:"hidden", border:"1px solid #ddd" }}><div style={{ height:"100%", width:bars[b.key]+"%", background:b.color, borderRadius:99, transition:"width 0.3s" }} /></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );'''

NEW_RETURN = '''  return (
    <div style={{ position:"fixed", inset:0, background:"white", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>
      {/* Header */}
      <div style={{ background:"#1A3A5C", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0 }}>
        <span style={{ color:"white", fontWeight:900, fontSize:15 }}>🍽️ Compose ton repas</span>
        <div style={{ display:"flex", gap:10 }}>
          <button onClick={reset} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>Réinitialiser</button>
          <button onClick={onBack} style={{ background:"#87CEEB", border:"2px solid #1A3A5C", borderRadius:8, color:"#1A3A5C", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>← Retour</button>
        </div>
      </div>

      {/* Corps : 50% aliments | 50% assiettes */}
      <div style={{ flex:1, display:"grid", gridTemplateColumns:"1fr 1fr", overflow:"hidden" }}>

        {/* GAUCHE — Aliments par catégorie */}
        <div style={{ borderRight:"2px solid #e0e0e0", overflowY:"auto", padding:"16px" }}>
          <div style={{ fontSize:13, fontWeight:900, color:"#1A3A5C", marginBottom:12, textTransform:"uppercase", letterSpacing:1 }}>Glisse les aliments sur ton assiette</div>
          {CATEGORIES_PNNS.map(cat => {
            const foods = FOODS_LIST.filter(f => f.categorie === cat);
            if (foods.length === 0) return null;
            return (
              <div key={cat} style={{ marginBottom:18 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#87CEEB", textTransform:"uppercase", letterSpacing:1, marginBottom:8, paddingBottom:4, borderBottom:"2px solid #e8f4ff" }}>{cat}</div>
                <div style={{ display:"grid", gridTemplateColumns:"repeat(4, 1fr)", gap:8 }}>
                  {foods.map(food => {
                    const used = usedIds.includes(food.id);
                    return (
                      <div key={food.id} draggable={!used} onDragStart={() => !used && setDragId(food.id)} onDragEnd={() => setDragId(null)}
                        style={{ background:used?"#f5f5f5":"white", border:`2px solid ${used?"#ddd":food.good?"#87CEEB":"#E24B4A"}`, borderRadius:12, padding:"10px 6px", textAlign:"center", cursor:used?"not-allowed":"grab", opacity:used?0.5:1, transition:"all 0.15s", boxShadow:used?"none":"0 2px 6px rgba(0,0,0,0.08)" }}>
                        <img src={food.emoji} style={{ width:48, height:48, objectFit:"contain" }} />
                        <div style={{ fontSize:10, fontWeight:800, color:"#333", marginTop:4, lineHeight:1.2 }}>{food.name}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
          <div style={{ fontSize:11, color:"#aaa", marginTop:8, lineHeight:1.6 }}>
            <span style={{ color:"#87CEEB", fontWeight:700 }}>Bleu</span> = recommandé · <span style={{ color:"#E24B4A", fontWeight:700 }}>Rouge</span> = à limiter
          </div>
        </div>

        {/* DROITE — Assiettes */}
        <div style={{ overflowY:"auto", padding:"16px", display:"flex", flexDirection:"column", gap:16 }}>
          <div style={{ fontSize:13, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Mon plateau</div>

          {/* Assiettes en grille : 2 en haut + boisson, puis dessert en bas */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>
            {showEntree && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Entrée</div>
                <AssietteDrop zone="entree" items={entree} onRemove={removeFromEntree} size={180} maxItems={2} />
              </div>
            )}
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Plat principal</div>
              <AssietteDrop zone="plate" items={plate} onRemove={removeFromPlate} size={180} maxItems={5} />
            </div>
            {showDessert && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Dessert</div>
                <AssietteDrop zone="dessert" items={dessert} onRemove={removeFromDessert} size={180} maxItems={2} />
              </div>
            )}
            {/* Boisson */}
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1 }}>Boisson</div>
              <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("glass")} onClick={removeGlass}
                style={{ width:80, height:120, borderRadius:"0 0 16px 16px", border:"3px solid #87CEEB", background:glass?glass.color+"22":"#f0f8ff", overflow:"hidden", cursor:glass?"pointer":"default", position:"relative", boxShadow:"0 2px 8px rgba(135,206,235,0.3)" }}>
                {glass && <div style={{ position:"absolute", bottom:0, left:0, right:0, height:"70%", background:glass.color, opacity:0.5, borderRadius:"0 0 14px 14px" }} />}
                {glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center" }}><img src={glass.emoji} style={{ width:40, height:40, objectFit:"contain" }} /></div>}
                {!glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:11, color:"#87CEEB", fontWeight:700, textAlign:"center", padding:4 }}>Dépose ici</div>}
              </div>
              <div style={{ fontSize:11, color:"#666", fontWeight:700 }}>{glass ? glass.name : "—"}</div>
            </div>
          </div>

          {/* Bilan PNNS */}
          <div style={{ background:"#f0f8ff", borderRadius:14, padding:"14px 16px", border:"2px solid #87CEEB" }}>
            <div style={{ fontSize:11, fontWeight:900, color:"#1A3A5C", textTransform:"uppercase", letterSpacing:1, marginBottom:10 }}>Équilibre PNNS</div>
            {[{ key:"legumes", label:"Légumes & fruits", color:"#4caf50" },{ key:"feculents", label:"Féculents", color:"#EF9F27" },{ key:"proteines", label:"Protéines", color:"#378ADD" },{ key:"laitiers", label:"Laitiers", color:"#87CEEB" },{ key:"eau", label:"Boisson", color:"#1A3A5C" }].map(b => (
              <div key={b.key} style={{ marginBottom:8 }}>
                <div style={{ display:"flex", justifyContent:"space-between", fontSize:11, color:"#555", marginBottom:3, fontWeight:700 }}>
                  <span>{b.label}</span><span>{bars[b.key]}%</span>
                </div>
                <div style={{ height:8, background:"#dde8f0", borderRadius:99, overflow:"hidden" }}>
                  <div style={{ height:"100%", width:bars[b.key]+"%", background:b.color, borderRadius:99, transition:"width 0.3s" }} />
                </div>
              </div>
            ))}
          </div>

          {/* Bouton valider */}
          <button onClick={valider} style={{ background:"#1A3A5C", border:"none", borderRadius:12, color:"white", fontSize:15, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"0 4px 12px rgba(26,58,92,0.3)" }}>
            ✅ Valider mon repas
          </button>
          {feedback && (
            <div style={{ background:feedbackColor==="#2e7d32"?"#e8f5e9":"#fbe9e7", border:`2px solid ${feedbackColor}`, borderRadius:12, padding:"12px 16px", fontSize:13, color:feedbackColor, fontWeight:700, textAlign:"center" }}>
              {feedback}
            </div>
          )}
        </div>
      </div>
    </div>
  );'''

if OLD_RETURN in code:
    code = code.replace(OLD_RETURN, NEW_RETURN)
    print("✅ MinijeuScreen redesigné")
else:
    print("⚠️ Return non trouvé - vérifier les espaces")

# Fix AssietteDrop to use white background + blue border
OLD_ASSIETTE = '''  const AssietteDrop = ({ zone, items, onRemove, size, maxItems }) => (
    <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop(zone)}
      style={{ width:size, height:size, position:"relative", flexShrink:0 }}>
      <img src="/assiette1.png" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"contain", pointerEvents:"none" }} alt="assiette" />
      <div style={{ position:"absolute", inset:0, display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:size*0.2 }}>
        {items.length === 0 && <span style={{ fontSize:11, color:"rgba(0,0,0,0.3)", textAlign:"center" }}>Dépose ici</span>}
        {items.length >= maxItems && <span style={{ fontSize:10, color:"#FA8072", textAlign:"center", fontWeight:800 }}>Max !</span>}
        {items.map(food => (
          <span key={food.id} onClick={()=>onRemove(food.id)} title="Clic pour retirer" style={{ cursor:"pointer", position:"relative", zIndex:1 }}>
            {food.emoji.endsWith(".png") ? <img src={food.emoji} style={{ width:size*0.18, height:size*0.18, objectFit:"contain" }} /> : <span style={{ fontSize:size*0.1 }}>{food.emoji}</span>}
          </span>
        ))}
      </div>
    </div>
  );'''

NEW_ASSIETTE = '''  const AssietteDrop = ({ zone, items, onRemove, size, maxItems }) => (
    <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop(zone)}
      style={{ width:size, height:size, position:"relative", flexShrink:0, borderRadius:"50%", background:"white", border:"4px solid #87CEEB", boxShadow:"0 4px 16px rgba(135,206,235,0.4)", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:size*0.1 }}>
        {items.length === 0 && <span style={{ fontSize:11, color:"#87CEEB", textAlign:"center", fontWeight:700 }}>Dépose ici</span>}
        {items.length >= maxItems && <span style={{ fontSize:10, color:"#FA8072", textAlign:"center", fontWeight:800 }}>Max !</span>}
        {items.map(food => (
          <span key={food.id} onClick={()=>onRemove(food.id)} title="Clic pour retirer" style={{ cursor:"pointer", position:"relative", zIndex:1 }}>
            <img src={food.emoji} style={{ width:size*0.2, height:size*0.2, objectFit:"contain" }} />
          </span>
        ))}
      </div>
    </div>
  );'''

if OLD_ASSIETTE in code:
    code = code.replace(OLD_ASSIETTE, NEW_ASSIETTE)
    print("✅ AssietteDrop : fond blanc + rebord bleu ciel")
else:
    print("⚠️ AssietteDrop non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\nFichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
