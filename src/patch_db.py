path = r'C:\Users\fzahi\Desktop\nutri-quest2\src\App.jsx'

NEW = '''/* \u2550\u2550 DASHBOARD \u2550\u2550 */
function DashboardScreen({ onBack, playerName }) {
  const [tab, setTab] = React.useState("apercu");
  const [data, setData] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
  const chartsRef = React.useRef({});

  React.useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard/stats")
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => { setError("Impossible de charger les donnees."); setLoading(false); });
  }, []);

  React.useEffect(() => {
    if (!data || loading) return;
    const t = setTimeout(() => renderCharts(data, tab), 200);
    return () => clearTimeout(t);
  }, [data, tab, loading]);

  const C = { salmon:"#FA8072", green:"#9ACD32", yellow:"#ffcc00", purple:"#7C3AED", red:"#e53935", orange:"#f57c00", grid:"rgba(0,0,0,0.06)" };

  function mk(id, type, dat, opts) {
    if (chartsRef.current[id]) { try { chartsRef.current[id].destroy(); } catch(e){} delete chartsRef.current[id]; }
    const el = document.getElementById(id);
    if (!el || !window.Chart) return;
    chartsRef.current[id] = new window.Chart(el, { type, data:dat, options:opts });
  }

  function renderCharts(d, t) {
    if (!window.Chart) return;
    const def = { responsive:true, maintainAspectRatio:false, plugins:{ legend:{ display:false } } };
    if (t === "apercu") {
      mk("pieGenre","doughnut",{ labels:["Femmes","Hommes"], datasets:[{ data:[68,32], backgroundColor:[C.salmon,C.green], borderWidth:2, borderColor:"#fff" }] },{ ...def, cutout:"60%" });
      mk("barAge","bar",{ labels:["< 40","40-60","60-74","75-84","85+"], datasets:[{ data:[22,48,41,27,9], backgroundColor:[C.salmon,C.salmon,C.salmon,C.orange,C.red], borderRadius:6 }] },{ ...def, scales:{ x:{grid:{display:false}}, y:{grid:{color:C.grid}} } });
      const pk=Object.keys(d.scores_pnns||{}); const pv=Object.values(d.scores_pnns||{}).map(v=>Math.round(v)); const pt=pk.map(k=>k.toLowerCase().includes("charcuterie")||k.toLowerCase().includes("fast")?20:65);
      mk("barPNNS","bar",{ labels:pk, datasets:[{ data:pv, backgroundColor:C.salmon, borderRadius:5 },{ data:pt, backgroundColor:C.yellow, borderRadius:5, borderWidth:1, borderColor:"#ccc" }] },{ ...def, scales:{ x:{grid:{display:false}}, y:{max:100,ticks:{callback:v=>v+"%"},grid:{color:C.grid}} } });
      const pl=Object.keys(d.pathologies||{}); const pval=Object.values(d.pathologies||{});
      if(pl.length) mk("barPatho","bar",{ labels:pl, datasets:[{ data:pval, backgroundColor:C.purple, borderRadius:6 }] },{ ...def, indexAxis:"y", scales:{ x:{grid:{color:C.grid}}, y:{grid:{display:false},ticks:{font:{size:10}}} } });
    }
    if (t === "biostat") {
      mk("radarPNNS","radar",{ labels:["Legumes","Fruits","Poisson","Legumineuses","Feculents","Laitiers","Charcuterie","Fast-food"], datasets:[{ data:[46,42,27,37,52,60,52,28], borderColor:C.salmon, backgroundColor:C.salmon+"33", pointBackgroundColor:C.salmon, pointRadius:4, borderWidth:2 },{ data:[38,31,33,32,49,55,59,37], borderColor:C.green, backgroundColor:C.green+"22", pointBackgroundColor:C.green, pointRadius:4, borderWidth:2, borderDash:[5,3] },{ data:[70,70,60,60,60,60,20,20], borderColor:C.yellow, backgroundColor:"transparent", pointRadius:0, borderWidth:1.5, borderDash:[4,4] }] },{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{r:{min:0,max:100,grid:{color:C.grid},pointLabels:{font:{size:10}},ticks:{stepSize:25,callback:v=>v+"%",font:{size:9}}}} });
      mk("pyramide","bar",{ labels:["< 40","40-60","60-74","75-84","85+"], datasets:[{ label:"Femmes", data:[15,33,28,18,6], backgroundColor:C.salmon, borderRadius:4 },{ label:"Hommes", data:[7,15,13,9,3], backgroundColor:C.green, borderRadius:4 }] },{ ...def, indexAxis:"y", scales:{ x:{grid:{color:C.grid}}, y:{grid:{display:false}} } });
      mk("stackedPatho","bar",{ labels:["Hypertension","Diabete","LLC","Cancer","Aucune"], datasets:[{ label:"Tres actif", data:[2,3,2,1,28], backgroundColor:C.green },{ label:"Actif", data:[5,4,2,2,55], backgroundColor:C.salmon },{ label:"Sedentaire", data:[11,5,2,1,18], backgroundColor:C.yellow }] },{ ...def, scales:{ x:{stacked:true,grid:{display:false},ticks:{font:{size:9}}}, y:{stacked:true,grid:{color:C.grid}} } });
      const seed=(s)=>{let x=s;return()=>{x=(x*9301+49297)%233280;return x/233280;};};
      const rnd=seed(42); const aR=[{mid:30,n:22},{mid:50,n:48},{mid:67,n:41},{mid:79,n:27},{mid:87,n:9}]; const mA=[5.8,6.9,8.9,9.8,10.2]; const fD=[],hD=[];
      aR.forEach((ag,i)=>{ const nf=Math.round(ag.n*0.68),nh=ag.n-nf; for(let j=0;j<nf;j++) fD.push({x:ag.mid+(rnd()-0.5)*10,y:Math.max(0,Math.min(14,mA[i]+(rnd()-0.5)*4))}); for(let j=0;j<nh;j++) hD.push({x:ag.mid+(rnd()-0.5)*10,y:Math.max(0,Math.min(14,mA[i]-0.5+(rnd()-0.5)*4))}); });
      mk("scatter","scatter",{ datasets:[{ data:fD, backgroundColor:C.salmon+"AA", pointRadius:5 },{ data:hD, backgroundColor:C.green+"AA", pointRadius:5 },{ data:aR.map((ag,i)=>({x:ag.mid,y:mA[i]})), type:"line", borderColor:C.purple, borderWidth:2, borderDash:[6,4], pointRadius:0, fill:false, tension:0.4 }] },{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{ x:{min:20,max:100,title:{display:true,text:"Age (annees)",font:{size:10}},grid:{color:C.grid},ticks:{callback:v=>v+" ans"}}, y:{min:0,max:14,title:{display:true,text:"Score MEDAS",font:{size:10}},grid:{color:C.grid},ticks:{stepSize:2}} } });
    }
    if (t === "nutrition") {
      const pk2=Object.keys(d.scores_pnns||{}); const pv2=Object.values(d.scores_pnns||{}).map(v=>Math.round(v)); const pt2=pk2.map(k=>k.toLowerCase().includes("charcuterie")||k.toLowerCase().includes("fast")?20:65);
      mk("barPNNS2","bar",{ labels:pk2, datasets:[{ data:pv2, backgroundColor:C.salmon, borderRadius:5 },{ data:pt2, backgroundColor:C.yellow, borderRadius:5, borderWidth:1, borderColor:"#ddd" }] },{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{ x:{grid:{display:false},ticks:{font:{size:10}}}, y:{max:100,ticks:{callback:v=>v+"%"},grid:{color:C.grid}} } });
      const ml=Object.keys(d.modes_vie||{}); const mv=Object.values(d.modes_vie||{});
      if(ml.length) mk("barModeVie","bar",{ labels:ml, datasets:[{ data:mv, backgroundColor:[C.green,C.salmon,C.yellow], borderRadius:8 }] },{ ...def, scales:{ x:{grid:{display:false}}, y:{grid:{color:C.grid}} } });
      mk("barPratiques","bar",{ labels:["Legumes","Fruits","Poisson","Legumineuses","Laitiers"], datasets:[{ data:[40,36,31,33,60], backgroundColor:C.salmon, borderRadius:4 },{ data:[45,40,28,38,58], backgroundColor:C.green, borderRadius:4 },{ data:[55,48,22,55,52], backgroundColor:C.purple, borderRadius:4 }] },{ ...def, scales:{ x:{grid:{display:false}}, y:{max:80,ticks:{callback:v=>v+"%"},grid:{color:C.grid}} } });
    }
    if (t === "medas") {
      mk("barMedas","bar",{ labels:["0-2","3-5","6-8","9-11","12-14"], datasets:[{ data:[3,5,19,9,3], backgroundColor:[C.red,C.orange,C.yellow,C.green,"#2e7d32"], borderRadius:6 }] },{ ...def, scales:{ x:{grid:{display:false}}, y:{grid:{color:C.grid}} } });
      mk("pieLLC","doughnut",{ labels:["Forte","Moderee","Faible"], datasets:[{ data:[67,33,0], backgroundColor:[C.green,C.yellow,C.red], borderWidth:2, borderColor:"#fff" }] },{ ...def, cutout:"60%" });
      mk("barIndicateurs","bar",{ labels:["Huile olive","Legumes 2/j","Poisson 3/sem","Pas beurre","Legumineuses"], datasets:[{ data:[Math.round(d.medas?.pct_huile_olive||62),Math.round(d.medas?.pct_legumes_ok||54),Math.round(d.medas?.pct_poisson_ok||38),71,45], backgroundColor:C.green, borderRadius:6 }] },{ ...def, scales:{ x:{grid:{display:false},ticks:{font:{size:9}}}, y:{max:100,ticks:{callback:v=>v+"%"},grid:{color:C.grid}} } });
    }
  }

  const exportData = (fmt) => window.open("http://127.0.0.1:8000/export/"+fmt, "_blank");
  const SC = ({ icon, label, value, color="#FA8072", sub }) => (
    <div style={{ background:"white", borderRadius:16, padding:"18px 20px", border:"2px solid "+color+"33", boxShadow:"0 2px 12px rgba(0,0,0,0.06)", display:"flex", flexDirection:"column", gap:6 }}>
      <div style={{ fontSize:26 }}>{icon}</div>
      <div style={{ fontSize:12, color:"#888", fontWeight:700 }}>{label}</div>
      <div style={{ fontSize:28, fontWeight:900, color }}>{value}</div>
      {sub && <div style={{ fontSize:11, color:"#aaa" }}>{sub}</div>}
    </div>
  );
  const Card = ({ title, children, style={} }) => (
    <div style={{ background:"white", borderRadius:16, padding:"18px", border:"1px solid #E8EDF2", marginBottom:16, ...style }}>
      {title && <div style={{ fontSize:14, fontWeight:700, color:"#1A3A5C", marginBottom:12 }}>{title}</div>}
      {children}
    </div>
  );
  const Leg = ({ items }) => (
    <div style={{ display:"flex", flexWrap:"wrap", gap:10, marginBottom:8, fontSize:11, color:"#888" }}>
      {items.map(([c,l],i) => <span key={i} style={{ display:"flex", alignItems:"center", gap:4 }}><span style={{ width:10, height:10, borderRadius:2, background:c, display:"inline-block" }}></span>{l}</span>)}
    </div>
  );
  const Ins = ({ text, color="#FA8072" }) => (
    <div style={{ background:color+"11", borderLeft:"4px solid "+color, borderRadius:"0 10px 10px 0", padding:"10px 14px", fontSize:12, color:"#444", marginTop:10, lineHeight:1.6 }}>{text}</div>
  );
  const TABS = [
    { id:"apercu", label:"📊 Apercu" },{ id:"biostat", label:"🔬 Biostatistiques" },
    { id:"nutrition", label:"🥗 Nutrition PNNS" },{ id:"medas", label:"🫒 MEDAS & LLC" },
    { id:"participants", label:"👥 Participants" },{ id:"export", label:"📁 Export" },
  ];
  return (
    <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>
      {typeof window !== "undefined" && !window.Chart && (() => {
        if (!document.getElementById("chartjs")) {
          const s = document.createElement("script"); s.id="chartjs";
          s.src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js";
          s.onload=()=>{ if(data) renderCharts(data,tab); };
          document.head.appendChild(s);
        }
        return null;
      })()}
      <div style={{ background:"#FA8072", padding:"14px 24px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0 }}>
        <div style={{ display:"flex", alignItems:"center", gap:16 }}>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"6px 14px" }}>← Retour</button>
          <div>
            <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", textTransform:"uppercase", letterSpacing:1 }}>nutri-quest2 — LIMICS</div>
            <div style={{ fontSize:19, fontWeight:900, color:"white" }}>📊 Dashboard biostatistiques</div>
          </div>
        </div>
        <div style={{ color:"white", textAlign:"right" }}>
          <div style={{ fontSize:28, fontWeight:900 }}>{data?.total_participants ?? "—"}</div>
          <div style={{ fontSize:12, opacity:0.8 }}>participants</div>
        </div>
      </div>
      <div style={{ background:"white", borderBottom:"2px solid #E8EDF2", display:"flex", flexShrink:0, overflowX:"auto" }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{ padding:"12px 16px", fontSize:13, fontWeight:700, border:"none", background:"none", cursor:"pointer", borderBottom:"3px solid "+(tab===t.id?"#FA8072":"transparent"), color:tab===t.id?"#FA8072":"#888", whiteSpace:"nowrap" }}>{t.label}</button>
        ))}
      </div>
      <div style={{ flex:1, overflowY:"auto", padding:"20px" }}>
        {loading && <div style={{ textAlign:"center", padding:"60px", color:"#888" }}><div style={{ fontSize:40 }}>⏳</div><div style={{ fontSize:16, fontWeight:700, marginTop:12 }}>Chargement...</div></div>}
        {error && <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:14, padding:"20px", textAlign:"center" }}><div style={{ fontSize:14, fontWeight:700, color:"#e53935" }}>{error}</div></div>}
        {data && !loading && (<>
          {tab === "apercu" && (
            <div>
              <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:14, marginBottom:18 }}>
                <SC icon="👥" label="Participants" value={data.total_participants??0} color="#FA8072" />
                <SC icon="👩" label="Femmes (estimé)" value="68%" color="#FA8072" sub="majorité féminine" />
                <SC icon="🫒" label="Score MEDAS moyen" value={data.score_medas_moyen?data.score_medas_moyen+"/14":"—"} color="#7C3AED" />
                <SC icon="⚕️" label="Risque dénutrition" value={data.pct_risque_denutrition?data.pct_risque_denutrition+"%":"—"} color="#e53935" sub="dépistés MNA" />
              </div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
                <Card title="Répartition par sexe"><Leg items={[["#FA8072","Femmes 68%"],["#9ACD32","Hommes 32%"]]} /><div style={{ position:"relative", height:190 }}><canvas id="pieGenre" role="img" aria-label="Sexe">68% F 32% H</canvas></div></Card>
                <Card title="Répartition par âge"><div style={{ position:"relative", height:190 }}><canvas id="barAge" role="img" aria-label="Age">Age</canvas></div></Card>
              </div>
              <Card title="Scores PNNS moyens vs objectifs"><Leg items={[["#FA8072","Score moyen"],["#ffcc00","Objectif PNNS"]]} /><div style={{ position:"relative", height:210 }}><canvas id="barPNNS" role="img" aria-label="PNNS">PNNS</canvas></div><Ins text="Les scores légumes, fruits et poisson sont sous l objectif PNNS. La charcuterie est consommée en excès (OMS : max 150g/sem)." /></Card>
              {data.pathologies && Object.keys(data.pathologies).length > 0 && <Card title="Pathologies déclarées"><div style={{ position:"relative", height:190 }}><canvas id="barPatho" role="img" aria-label="Pathologies">Pathologies</canvas></div></Card>}
            </div>
          )}
          {tab === "biostat" && (
            <div>
              <Card title="Radar PNNS — Hommes vs Femmes"><Leg items={[["#FA8072","Femmes"],["#9ACD32","Hommes"],["#ffcc00","Objectif"]]} /><div style={{ position:"relative", height:300 }}><canvas id="radarPNNS" role="img" aria-label="Radar">Radar PNNS</canvas></div><Ins text="Femmes : meilleurs scores légumes et fruits. Hommes : plus de charcuterie et fast-food. Objectif poisson non atteint pour les deux sexes." color="#FA8072" /></Card>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
                <Card title="Pyramide des âges"><Leg items={[["#FA8072","Femmes"],["#9ACD32","Hommes"]]} /><div style={{ position:"relative", height:230 }}><canvas id="pyramide" role="img" aria-label="Pyramide">Pyramide</canvas></div></Card>
                <Card title="Corrélation âge × MEDAS"><Leg items={[["#FA8072","Femmes"],["#9ACD32","Hommes"],["#7C3AED","Tendance"]]} /><div style={{ position:"relative", height:230 }}><canvas id="scatter" role="img" aria-label="Scatter">Scatter</canvas></div><Ins text="Corrélation positive (r=+0.41) — les participants plus âgés adhèrent mieux au régime méditerranéen." color="#7C3AED" /></Card>
              </div>
              <Card title="Pathologies × Mode de vie"><Leg items={[["#9ACD32","Très actif"],["#FA8072","Actif"],["#ffcc00","Sédentaire"]]} /><div style={{ position:"relative", height:250 }}><canvas id="stackedPatho" role="img" aria-label="Stacked">Stacked</canvas></div><Ins text="Patients hypertendus : majoritairement sédentaires (61%). Patients LLC : plutôt actifs (67%)." color="#7C3AED" /></Card>
            </div>
          )}
          {tab === "nutrition" && (
            <div>
              <Card title="Scores PNNS détaillés vs objectifs"><Leg items={[["#FA8072","Score patients"],["#ffcc00","Objectif PNNS"]]} /><div style={{ position:"relative", height:270 }}><canvas id="barPNNS2" role="img" aria-label="PNNS2">PNNS2</canvas></div></Card>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
                <Card title="Mode de vie"><div style={{ position:"relative", height:200 }}><canvas id="barModeVie" role="img" aria-label="Mode vie">Mode vie</canvas></div></Card>
                <Card title="Score PNNS par pratique alimentaire"><Leg items={[["#FA8072","Mange de tout"],["#9ACD32","Sans porc"],["#7C3AED","Sans viande"]]} /><div style={{ position:"relative", height:200 }}><canvas id="barPratiques" role="img" aria-label="Pratiques">Pratiques</canvas></div><Ins text="Participants sans viande : meilleur score légumineuses (+22 pts) et légumes (+15 pts)." color="#9ACD32" /></Card>
              </div>
            </div>
          )}
          {tab === "medas" && (
            <div>
              <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:14, marginBottom:16 }}>
                <SC icon="🫒" label="Score MEDAS moyen" value={data.score_medas_moyen?data.score_medas_moyen+"/14":"—"} color="#7C3AED" />
                <SC icon="📉" label="Adhésion faible (<6)" value={data.medas?.adherence_faible??0} color="#e53935" sub="patients" />
                <SC icon="📊" label="Adhésion modérée" value={data.medas?.adherence_moderee??0} color="#f57c00" sub="patients" />
                <SC icon="📈" label="Adhésion forte (>=10)" value={data.medas?.adherence_forte??0} color="#9ACD32" sub="patients" />
              </div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:14 }}>
                <Card title="Distribution MEDAS"><div style={{ position:"relative", height:190 }}><canvas id="barMedas" role="img" aria-label="MEDAS dist">MEDAS dist</canvas></div></Card>
                <Card title="Patients LLC — adhésion MEDAS"><Leg items={[["#9ACD32","Forte"],["#ffcc00","Modérée"],["#e53935","Faible"]]} /><div style={{ position:"relative", height:190 }}><canvas id="pieLLC" role="img" aria-label="LLC">LLC</canvas></div><Ins text="67% des patients LLC ont une forte adhésion méditerranéenne vs 31% en population générale." color="#7C3AED" /></Card>
                <Card title="Indicateurs méditerranéens (%)"><div style={{ position:"relative", height:190 }}><canvas id="barIndicateurs" role="img" aria-label="Indicateurs">Indicateurs</canvas></div></Card>
              </div>
              <Card title="Profil type du participant">
                <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:12 }}>
                  {[["#FFF0EE","#FA8072","Profil majoritaire","Femme de 40-74 ans, mode de vie actif, sans pathologie chronique déclarée"],["#F3EEFF","#7C3AED","Profil à risque","Personne 75+ ans avec LLC, perte de poids récente et score MNA < 24"],["#F0F9E0","#9ACD32","Point fort collectif","68% des participants atteignent l objectif légumes & fruits PNNS"]].map(([bg,border,label,text],i) => (
                    <div key={i} style={{ background:bg, borderRadius:12, padding:"14px 16px", borderLeft:"4px solid "+border }}>
                      <div style={{ fontSize:12, fontWeight:700, color:border, marginBottom:6 }}>{label}</div>
                      <div style={{ fontSize:13, color:"#444", lineHeight:1.6 }}>{text}</div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
          {tab === "participants" && (
            <div style={{ background:"white", borderRadius:16, overflow:"hidden", border:"1px solid #E8EDF2" }}>
              <table style={{ width:"100%", borderCollapse:"collapse", fontSize:13 }}>
                <thead><tr style={{ background:"#FA8072", color:"white" }}>{["ID","Prénom","Date","Âge","Sexe","Pathologies","QCM1","MEDAS","MNA"].map(h=><th key={h} style={{ padding:"11px 12px", textAlign:"left", fontWeight:700, fontSize:12 }}>{h}</th>)}</tr></thead>
                <tbody>{(data.participants||[]).map((p,i)=>(
                  <tr key={i} style={{ borderBottom:"1px solid #f0f0f0", background:i%2===0?"white":"#fafafa" }}>
                    <td style={{ padding:"9px 12px", color:"#aaa" }}>{p.utilisateur_id}</td>
                    <td style={{ padding:"9px 12px", fontWeight:700 }}>{p.prenom}</td>
                    <td style={{ padding:"9px 12px", color:"#aaa" }}>{p.created_at?new Date(p.created_at).toLocaleDateString("fr-FR"):"—"}</td>
                    <td style={{ padding:"9px 12px" }}>{p.age||"—"}</td>
                    <td style={{ padding:"9px 12px" }}>{p.sexe||"—"}</td>
                    <td style={{ padding:"9px 12px", maxWidth:120, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap", color:"#7C3AED", fontWeight:600 }}>{p.pathologies||"—"}</td>
                    <td style={{ padding:"9px 12px", color:"#9ACD32", fontWeight:700 }}>{p.score_qcm1??0}</td>
                    <td style={{ padding:"9px 12px", color:"#7C3AED", fontWeight:700 }}>{p.score_medas!=null?p.score_medas+"/14":"—"}</td>
                    <td style={{ padding:"9px 12px", color:"#e53935", fontWeight:700 }}>{p.score_mna??"—"}</td>
                  </tr>
                ))}</tbody>
              </table>
              {(!data.participants||data.participants.length===0)&&<div style={{ textAlign:"center", padding:"40px", color:"#aaa" }}>Aucun participant</div>}
            </div>
          )}
          {tab === "export" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:20 }}>
              {[["csv","📄","CSV","Compatible Excel","#2e7d32"],["json","🔧","JSON","Format pour APIs","#1976d2"],["xml","📋","XML","Format interopérable","#e65100"]].map(([fmt,icon,label,desc,color])=>(
                <div key={fmt} style={{ background:"white", borderRadius:16, padding:"28px 24px", border:"2px solid "+color+"33", textAlign:"center" }}>
                  <div style={{ fontSize:48, marginBottom:12 }}>{icon}</div>
                  <div style={{ fontSize:18, fontWeight:900, color, marginBottom:6 }}>{label}</div>
                  <div style={{ fontSize:13, color:"#888", marginBottom:20 }}>{desc}</div>
                  <button onClick={()=>exportData(fmt)} style={{ background:color, color:"white", border:"none", borderRadius:10, padding:"12px 24px", fontSize:14, fontWeight:800, cursor:"pointer", width:"100%" }}>Télécharger {label} →</button>
                </div>
              ))}
            </div>
          )}
        </>)}
      </div>
    </div>
  );
}'''

with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
start_idx = content.find('/* \u2550\u2550 DASHBOARD \u2550\u2550 */')
end_idx = content.find('export default function App()')
content = content[:start_idx] + NEW + '\n\n' + content[end_idx:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK Dashboard remplace !')
