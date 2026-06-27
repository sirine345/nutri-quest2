#!/usr/bin/env python3
"""RECOS QCM1 V2 - textes plus grands, titres corriges"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

START_TAG = "function RecommandationsQcm1Screen("
END_TAG   = "function RecommandationsQcm2Screen("

idx_fn_start = code.find(START_TAG)
idx_fn_end   = code.find(END_TAG)
idx_start    = code.rfind("\n/*", 0, idx_fn_start)
idx_end      = code.rfind("\n/*", 0, idx_fn_end)

print(f"START: {idx_start}, END: {idx_end}")

NEW = """
/* \u2550\u2550 \u00c9CRAN RECOMMANDATIONS QCM1 \u2550\u2550 */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const [expanded, setExpanded] = useState(null);

  const bonnes    = ['legumes','fruits','feculents','legumineuses','fruitsACoque','laitiers','poisson','oeufs','volaille'];
  const mauvaises = ['charcuterie','fastFood','sucres','snacks'];
  const scoreGlobal = Math.round(
    (bonnes.reduce((s,k) => s + (nutrition[k]||0), 0) / bonnes.length * 0.7) +
    ((100 - mauvaises.reduce((s,k) => s + (nutrition[k]||0), 0) / mauvaises.length) * 0.3)
  );

  const RECOS = [
    { key:"legumes",      icon:"/legume2.png",    label:"L\u00e9gumes frais",      bon:v=>v>=60, badge:"Pas assez",          imgBg:"#EAF3DE", badgeBg:"#EAF3DE", badgeC:"#3B6D11", conseil:"Vise au moins 2 portions par jour. Varie les couleurs : vert, orange, rouge pour maximiser les vitamines et antioxydants.", detailBg:"#EAF3DE", detailBorder:"#9ACD32", detailC:"#27500A", btnBg:"#639922", profil:"legumes" },
    { key:"fruits",       icon:"/fruit.png",       label:"Fruits",             bon:v=>v>=60, badge:"Pas assez",          imgBg:"#FBEAF0", badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"Mange au moins 2 fruits entiers par jour. Pr\u00e9f\u00e8re les fruits entiers aux jus pour conserver les fibres.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"legumes" },
    { key:"legumineuses", icon:"/legumesec.png",   label:"L\u00e9gumineuses",       bon:v=>v>=50, badge:"Pas assez",          imgBg:"#EFEBE9", badgeBg:"#EFEBE9", badgeC:"#5D4037", conseil:"Lentilles, pois chiches, haricots : au moins 2 fois par semaine. Excellentes sources de prot\u00e9ines v\u00e9g\u00e9tales et de fibres.", detailBg:"#EFEBE9", detailBorder:"#795548", detailC:"#3E2723", btnBg:"#795548", profil:"legumineuses" },
    { key:"poisson",      icon:"/poisson.png",     label:"Poisson",            bon:v=>v>=50, badge:"Pas assez",          imgBg:"#E1F5FE", badgeBg:"#E1F5FE", badgeC:"#0C447C", conseil:"Consomme du poisson 2 fois par semaine, dont au moins un poisson gras (sardine, maquereau, saumon) pour les om\u00e9ga-3.", detailBg:"#E1F5FE", detailBorder:"#378ADD", detailC:"#042C53", btnBg:"#378ADD", profil:"poisson" },
    { key:"feculents",    icon:"/feculent.png",    label:"F\u00e9culents complets", bon:v=>v>=50, badge:"Pas assez",          imgBg:"#FAEEDA", badgeBg:"#FAEEDA", badgeC:"#633806", conseil:"Pr\u00e9f\u00e8re le pain complet, le riz brun et les p\u00e2tes compl\u00e8tes. Ils sont bien plus riches en fibres.", detailBg:"#FAEEDA", detailBorder:"#BA7517", detailC:"#412402", btnBg:"#BA7517", profil:"rapide" },
    { key:"charcuterie",  icon:"/charcuterie.png", label:"Charcuterie",        bon:v=>v<=20, badge:"Tu en manges trop",   imgBg:"#FFF0EB", badgeBg:"#FFF0EB", badgeC:"#993C1D", conseil:"Maximum 150g par semaine. La charcuterie est class\u00e9e canc\u00e9rig\u00e8ne groupe 1 par l'OMS. Remplace-la par des oeufs ou de la volaille.", detailBg:"#FFF0EB", detailBorder:"#FA8072", detailC:"#4A1B0C", btnBg:"#c4622d", profil:"charcuterie", inverse:true },
    { key:"fastFood",     icon:"/fast_food.png",   label:"Fast food",          bon:v=>v<=20, badge:"Trop fr\u00e9quent",     imgBg:"#FCEBEB", badgeBg:"#FCEBEB", badgeC:"#791F1F", conseil:"Le fast food est li\u00e9 \u00e0 l'ob\u00e9sit\u00e9 et au diab\u00e8te de type 2. M\u00eame un repas simple pr\u00e9par\u00e9 maison vaut bien mieux.", detailBg:"#FCEBEB", detailBorder:"#E24B4A", detailC:"#501313", btnBg:"#E24B4A", profil:"fastFood", inverse:true },
    { key:"sucres",       icon:"/sucrerie.png",    label:"Sucreries",          bon:v=>v<=20, badge:"Trop fr\u00e9quent",     imgBg:"#FBEAF0", badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"Les sucres ajout\u00e9s favorisent les caries et le diab\u00e8te. Remplace-les par des fruits frais ou des fruits secs.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"sucres", inverse:true },
  ];

  const aAmeliorer = RECOS.filter(r => !r.bon(nutrition[r.key]||0));
  const bienFait   = RECOS.filter(r =>  r.bon(nutrition[r.key]||0));
  const scoreC = scoreGlobal >= 75 ? "#9ACD32" : scoreGlobal >= 50 ? "#ffcc00" : "#FA8072";

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF8F0", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Banni\u00e8re haute */}
      <div style={{ position:"relative", height:200, overflow:"hidden", borderBottom:"3px solid #222" }}>
        <img src="/i.jpg" alt="" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover" }} />
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.55)" }} />
        <div style={{ position:"absolute", inset:0, display:"flex", flexDirection:"column", justifyContent:"flex-end", padding:"20px 24px" }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"1.5px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:13, fontWeight:800, padding:"6px 14px", cursor:"pointer", width:"fit-content", marginBottom:12 }}>
            \u2190 Retour
          </button>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:34, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 #b2dfdb", lineHeight:1.1, marginBottom:6 }}>
            Tes recommandations
          </div>
          <div style={{ fontSize:15, color:"#FFF5EE", opacity:0.9 }}>
            Bas\u00e9es sur tes habitudes alimentaires d\u00e9clar\u00e9es
          </div>
        </div>
      </div>

      {/* Bande scores */}
      <div style={{ display:"flex", gap:12, padding:"14px 18px", background:"#FFF8F0", borderBottom:"1.5px solid #f0e8de" }}>
        {[
          [scoreGlobal+"/100", "Ton score",  scoreC],
          [bienFait.length,    "D\u00e9j\u00e0 bien",  "#9ACD32"],
          [aAmeliorer.length,  "\u00c0 corriger", "#FF6B35"],
        ].map(([val, label, c], i) => (
          <div key={i} style={{ flex:1, background:"white", borderRadius:10, border:"1.5px solid #ede8e0", padding:"12px 8px", textAlign:"center" }}>
            <div style={{ fontSize:24, fontWeight:900, color:c, lineHeight:1, fontFamily:"Arial Black, Arial" }}>{val}</div>
            <div style={{ fontSize:11, color:"#888", marginTop:4, fontWeight:700 }}>{label}</div>
          </div>
        ))}
      </div>

      <div style={{ padding:"18px" }}>

        {/* \u00c0 am\u00e9liorer */}
        {aAmeliorer.length > 0 && (
          <div style={{ marginBottom:26 }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"#FA8072", textShadow:"1px 1px 0 #b2dfdb", marginBottom:4 }}>
              Ce que tu peux am\u00e9liorer
            </div>
            <div style={{ fontSize:13, color:"#aaa", marginBottom:14 }}>Clique sur une carte pour voir le conseil personnalis\u00e9</div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
              {aAmeliorer.map(r => {
                const isOpen = expanded === r.key;
                return (
                  <div key={r.key} onClick={() => setExpanded(isOpen ? null : r.key)}
                    style={{ background:"white", borderRadius:14, border:"1.5px solid " + (isOpen ? r.detailBorder : "#ede8e0"), cursor:"pointer", overflow:"hidden", transition:"all .15s" }}>
                    <div style={{ width:"100%", height:110, background:r.imgBg, display:"flex", alignItems:"center", justifyContent:"center" }}>
                      <img src={r.icon} alt="" style={{ width:80, height:80, objectFit:"contain" }} />
                    </div>
                    <div style={{ padding:"12px 14px" }}>
                      <span style={{ display:"inline-block", background:r.badgeBg, color:r.badgeC, borderRadius:20, padding:"4px 12px", fontSize:12, fontWeight:800, marginBottom:6 }}>{r.badge}</span>
                      <div style={{ fontSize:15, fontWeight:800, color:"#1a1a1a" }}>{r.label}</div>
                      {isOpen && (
                        <>
                          <div style={{ background:r.detailBg, borderLeft:"3px solid " + r.detailBorder, borderRadius:8, padding:"10px 12px", marginTop:10, fontSize:13, color:r.detailC, lineHeight:1.75 }}>
                            {r.conseil}
                          </div>
                          <button onClick={e=>{ e.stopPropagation(); onVoirRecettes(r.profil); }}
                            style={{ marginTop:10, background:r.btnBg, border:"none", borderRadius:8, color:"white", fontSize:13, fontWeight:800, padding:"10px", cursor:"pointer", width:"100%" }}>
                            Voir les recettes \u2192
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* D\u00e9j\u00e0 bien */}
        {bienFait.length > 0 && (
          <div style={{ marginBottom:22 }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, color:"#FA8072", textShadow:"1px 1px 0 #b2dfdb", marginBottom:12 }}>
              Ce que tu fais d\u00e9j\u00e0 bien
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:9 }}>
              {bienFait.map(r => (
                <div key={r.key} style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:10, padding:"11px 13px", display:"flex", alignItems:"center", gap:10 }}>
                  <div style={{ width:34, height:34, borderRadius:8, background:r.imgBg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                    <img src={r.icon} alt="" style={{ width:22, height:22, objectFit:"contain" }} />
                  </div>
                  <span style={{ fontSize:13, fontWeight:700, color:"#3B6D11", flex:1 }}>{r.label}</span>
                  <span style={{ width:18, height:18, borderRadius:"50%", background:"#9ACD32", color:"white", fontSize:10, fontWeight:900, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>\u2713</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {aAmeliorer.length === 0 && (
          <div style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:12, padding:"28px 22px", textAlign:"center", marginBottom:22 }}>
            <div style={{ fontFamily:"Arial Black, Arial", fontSize:20, fontWeight:900, color:"#3B6D11", marginBottom:8 }}>Excellentes habitudes !</div>
            <p style={{ fontSize:14, color:"#777", lineHeight:1.75, margin:0 }}>Tes r\u00e9sultats sont conformes aux recommandations du PNNS. Continue comme \u00e7a !</p>
          </div>
        )}

        {/* Banni\u00e8re basse PNNS */}
        <div style={{ position:"relative", height:110, overflow:"hidden", borderRadius:12, border:"1.5px solid #ede8e0" }}>
          <img src="/fond_vert3.png" alt="" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"center 30%" }} />
          <div style={{ position:"absolute", inset:0, background:"rgba(250,128,114,0.78)" }} />
          <div style={{ position:"absolute", inset:0, padding:"14px 18px", display:"flex", alignItems:"center", gap:20 }}>
            <div style={{ fontFamily:"Arial Black, Arial", fontSize:15, color:"white", textShadow:"1px 1px 0 rgba(0,0,0,0.2)", flexShrink:0, lineHeight:1.4 }}>Rep\u00e8res<br/>PNNS</div>
            <div style={{ display:"flex", flexWrap:"wrap", flex:1, gap:"6px 18px" }}>
              {[["Fruits & l\u00e9gumes","5 portions / jour"],["Poisson","2x / sem dont 1 gras"],["L\u00e9gumineuses","2x / semaine min"],["Charcuterie","Max 150g / semaine"]].map(([k,v]) => (
                <div key={k}>
                  <div style={{ fontSize:12, color:"white", fontWeight:800 }}>{k}</div>
                  <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", marginTop:1 }}>{v}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

"""

code = code[:idx_start] + NEW + code[idx_end:]
print(f"Nouvelle taille: {len(code)}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print("SUCCES - App.jsx ecrit !")
