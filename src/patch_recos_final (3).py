#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

# Trouver les marqueurs par position
START_TAG = "function RecommandationsQcm1Screen("
END_TAG   = "function RecommandationsQcm2Screen("

idx_start = code.find(START_TAG)
idx_end   = code.find(END_TAG)

# Remonter au commentaire avant la fonction
idx_start = code.rfind("/*", 0, idx_start)

print(f"START: {idx_start}, END: {idx_end}")

if idx_start == -1 or idx_end == -1:
    print("Marqueurs non trouvés")
else:
    COMMENT_END = code.rfind("/*", 0, idx_end)
    print(f"Comment END: {COMMENT_END}")

    NEW = '''/* \u2550\u2550 \u00c9CRAN RECOMMANDATIONS QCM1 \u2550\u2550 */
function RecommandationsQcm1Screen({ nutrition, onBack, onVoirRecettes }) {
  const [expanded, setExpanded] = useState(null);

  const bonnes    = ['legumes','fruits','feculents','legumineuses','fruitsACoque','laitiers','poisson','oeufs','volaille'];
  const mauvaises = ['charcuterie','fastFood','sucres','snacks'];
  const scoreGlobal = Math.round(
    (bonnes.reduce((s,k) => s + (nutrition[k]||0), 0) / bonnes.length * 0.7) +
    ((100 - mauvaises.reduce((s,k) => s + (nutrition[k]||0), 0) / mauvaises.length) * 0.3)
  );

  const RECOS = [
    { key:"legumes",      icon:"/legume2.png",    label:"L\u00e9gumes frais",      bon:v=>v>=60, badge:"Pas assez",         imgBg:"#EAF3DE", badgeBg:"#EAF3DE", badgeC:"#3B6D11", conseil:"2 portions/jour minimum. Varie les couleurs pour maximiser les vitamines et antioxydants.", detailBg:"#EAF3DE", detailBorder:"#9ACD32", detailC:"#27500A", btnBg:"#639922", profil:"legumes" },
    { key:"fruits",       icon:"/fruit.png",       label:"Fruits",             bon:v=>v>=60, badge:"Pas assez",         imgBg:"#FBEAF0", badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"2 fruits entiers par jour minimum. Varie les esp\u00e8ces selon les saisons.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"legumes" },
    { key:"legumineuses", icon:"/legumesec.png",   label:"L\u00e9gumineuses",       bon:v=>v>=50, badge:"Pas assez",         imgBg:"#EFEBE9", badgeBg:"#EFEBE9", badgeC:"#5D4037", conseil:"Lentilles, pois chiches, haricots \u2014 2 fois/semaine minimum. Riches en fibres et prot\u00e9ines v\u00e9g\u00e9tales.", detailBg:"#EFEBE9", detailBorder:"#795548", detailC:"#3E2723", btnBg:"#795548", profil:"legumineuses" },
    { key:"poisson",      icon:"/poisson.png",     label:"Poisson",            bon:v=>v>=50, badge:"Pas assez",         imgBg:"#E1F5FE", badgeBg:"#E1F5FE", badgeC:"#0C447C", conseil:"2 fois/semaine dont 1 gras (sardine, maquereau, saumon). Les conserves comptent aussi !", detailBg:"#E1F5FE", detailBorder:"#378ADD", detailC:"#042C53", btnBg:"#378ADD", profil:"poisson" },
    { key:"feculents",    icon:"/feculent.png",    label:"F\u00e9culents complets", bon:v=>v>=50, badge:"Pas assez",         imgBg:"#FAEEDA", badgeBg:"#FAEEDA", badgeC:"#633806", conseil:"Pr\u00e9f\u00e8re le pain complet, riz brun, p\u00e2tes compl\u00e8tes. Plus riches en fibres que les versions raffin\u00e9es.", detailBg:"#FAEEDA", detailBorder:"#BA7517", detailC:"#412402", btnBg:"#BA7517", profil:"rapide" },
    { key:"charcuterie",  icon:"/charcuterie.png", label:"Charcuterie",        bon:v=>v<=20, badge:"Tu en manges trop",  imgBg:"#FFF0EB", badgeBg:"#FFF0EB", badgeC:"#993C1D", conseil:"Max 150g/semaine. Class\u00e9e canc\u00e9rig\u00e8ne groupe 1 par l'OMS. Remplace par des \u0153ufs ou de la volaille.", detailBg:"#FFF0EB", detailBorder:"#FA8072", detailC:"#4A1B0C", btnBg:"#c4622d", profil:"charcuterie", inverse:true },
    { key:"fastFood",     icon:"/fast_food.png",   label:"Fast food",          bon:v=>v<=20, badge:"Trop fr\u00e9quent",    imgBg:"#FCEBEB", badgeBg:"#FCEBEB", badgeC:"#791F1F", conseil:"Li\u00e9 \u00e0 l'ob\u00e9sit\u00e9 et au diab\u00e8te de type 2. M\u00eame un repas simple maison vaut bien mieux.", detailBg:"#FCEBEB", detailBorder:"#E24B4A", detailC:"#501313", btnBg:"#E24B4A", profil:"fastFood", inverse:true },
    { key:"sucres",       icon:"/sucrerie.png",    label:"Sucreries",          bon:v=>v<=20, badge:"Trop fr\u00e9quent",    imgBg:"#FBEAF0", badgeBg:"#FBEAF0", badgeC:"#72243E", conseil:"Les sucres ajout\u00e9s favorisent les caries et le diab\u00e8te. Remplace par des fruits frais ou secs.", detailBg:"#FBEAF0", detailBorder:"#D4537E", detailC:"#4B1528", btnBg:"#D4537E", profil:"sucres", inverse:true },
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
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.15)", border:"1.5px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:11, fontWeight:800, padding:"5px 12px", cursor:"pointer", width:"fit-content", marginBottom:12 }}>
            \u2190 Retour
          </button>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:34, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 #b2dfdb", lineHeight:1.1, marginBottom:4 }}>
            Tes recommandations
          </div>
          <div style={{ fontSize:13, color:"#FFF5EE", opacity:0.85 }}>
            Bas\u00e9es sur tes habitudes alimentaires d\u00e9clar\u00e9es
          </div>
        </div>
      </div>

      {/* Scores */}
      <div style={{ display:"flex", gap:12, padding:"14px 18px", background:"#FFF8F0", borderBottom:"1.5px solid #f0e8de" }}>
        {[
          [scoreGlobal+"/100", "Ton score",  scoreC],
          [bienFait.length,    "D\u00e9j\u00e0 bien",  "#9ACD32"],
          [aAmeliorer.length,  "\u00c0 corriger", "#FF6B35"],
        ].map(([val, label, c], i) => (
          <div key={i} style={{ flex:1, background:"white", borderRadius:10, border:"1.5px solid #ede8e0", padding:11, textAlign:"center" }}>
            <div style={{ fontSize:22, fontWeight:900, color:c, lineHeight:1, fontFamily:"Arial Black, Arial" }}>{val}</div>
            <div style={{ fontSize:9, color:"#bbb", marginTop:3, textTransform:"uppercase", letterSpacing:1, fontWeight:700 }}>{label}</div>
          </div>
        ))}
      </div>

      <div style={{ padding:"16px 18px" }}>

        {/* A am\u00e9liorer */}
        {aAmeliorer.length > 0 && (
          <div style={{ marginBottom:22 }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#FA8072", textShadow:"1px 1px 0 #b2dfdb", marginBottom:3 }}>
              Ce que tu peux am\u00e9liorer
            </div>
            <div style={{ fontSize:11, color:"#bbb", marginBottom:12 }}>Clique sur une carte pour voir le conseil</div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:10 }}>
              {aAmeliorer.map(r => {
                const isOpen = expanded === r.key;
                return (
                  <div key={r.key} onClick={() => setExpanded(isOpen ? null : r.key)}
                    style={{ background:"white", borderRadius:14, border:`1.5px solid ${isOpen ? r.detailBorder : "#ede8e0"}`, cursor:"pointer", overflow:"hidden", transition:"all .15s" }}>
                    <div style={{ width:"100%", height:100, background:r.imgBg, display:"flex", alignItems:"center", justifyContent:"center" }}>
                      <img src={r.icon} alt="" style={{ width:72, height:72, objectFit:"contain" }} />
                    </div>
                    <div style={{ padding:"11px 13px" }}>
                      <span style={{ display:"inline-block", background:r.badgeBg, color:r.badgeC, borderRadius:20, padding:"3px 10px", fontSize:10, fontWeight:800, marginBottom:5 }}>{r.badge}</span>
                      <div style={{ fontSize:13, fontWeight:800, color:"#1a1a1a" }}>{r.label}</div>
                      {isOpen && (
                        <>
                          <div style={{ background:r.detailBg, borderLeft:`3px solid ${r.detailBorder}`, borderRadius:8, padding:"9px 11px", marginTop:9, fontSize:11, color:r.detailC, lineHeight:1.7 }}>
                            {r.conseil}
                          </div>
                          <button onClick={e=>{ e.stopPropagation(); onVoirRecettes(r.profil); }}
                            style={{ marginTop:8, background:r.btnBg, border:"none", borderRadius:8, color:"white", fontSize:11, fontWeight:800, padding:9, cursor:"pointer", width:"100%" }}>
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
          <div style={{ marginBottom:20 }}>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#FA8072", textShadow:"1px 1px 0 #b2dfdb", marginBottom:10 }}>
              Ce que tu fais d\u00e9j\u00e0 bien
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:8 }}>
              {bienFait.map(r => (
                <div key={r.key} style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:10, padding:"10px 12px", display:"flex", alignItems:"center", gap:8 }}>
                  <div style={{ width:30, height:30, borderRadius:7, background:r.imgBg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                    <img src={r.icon} alt="" style={{ width:20, height:20, objectFit:"contain" }} />
                  </div>
                  <span style={{ fontSize:12, fontWeight:700, color:"#3B6D11", flex:1 }}>{r.label}</span>
                  <span style={{ width:16, height:16, borderRadius:"50%", background:"#9ACD32", color:"white", fontSize:8, fontWeight:900, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>\u2713</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {aAmeliorer.length === 0 && (
          <div style={{ background:"white", border:"1.5px solid #C0DD97", borderRadius:12, padding:"24px 20px", textAlign:"center", marginBottom:20 }}>
            <div style={{ fontFamily:"Arial Black, Arial", fontSize:17, fontWeight:900, color:"#3B6D11", marginBottom:6 }}>Excellentes habitudes !</div>
            <p style={{ fontSize:12, color:"#777", lineHeight:1.7, margin:0 }}>Tes r\u00e9sultats sont conformes aux recommandations du PNNS. Continue comme \u00e7a !</p>
          </div>
        )}

        {/* Banni\u00e8re basse PNNS */}
        <div style={{ position:"relative", height:100, overflow:"hidden", borderRadius:12, border:"1.5px solid #ede8e0" }}>
          <img src="/fond_vert3.png" alt="" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"center 30%" }} />
          <div style={{ position:"absolute", inset:0, background:"rgba(250,128,114,0.78)" }} />
          <div style={{ position:"absolute", inset:0, padding:"14px 18px", display:"flex", alignItems:"center", gap:20 }}>
            <div style={{ fontFamily:"Arial Black, Arial", fontSize:13, color:"white", textShadow:"1px 1px 0 rgba(0,0,0,0.2)", flexShrink:0, lineHeight:1.3 }}>Rep\u00e8res<br/>PNNS</div>
            <div style={{ display:"flex", flexWrap:"wrap", flex:1, gap:"5px 16px" }}>
              {[["Fruits & l\u00e9gumes","5 portions/jour"],["Poisson","2\u00d7/sem dont 1 gras"],["L\u00e9gumineuses","2\u00d7/semaine"],["Charcuterie","Max 150g/sem"]].map(([k,v]) => (
                <div key={k}>
                  <div style={{ fontSize:10, color:"white", fontWeight:700 }}>{k}</div>
                  <div style={{ fontSize:9, color:"rgba(255,255,255,0.6)", marginTop:1 }}>{v}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

'''

    code = code[:idx_start] + NEW + code[COMMENT_END:]
    print("Remplacement effectue")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"App.jsx ({len(code)} chars) ecrit")
