"""
PATCH — Mission 4 QCM Santé :
1. Ajoute la 4ème mission sur la carte frigo
2. Après mini-jeu : bouton retour → QcmSelectScreen avec Max + mission 4 débloquée
3. Phase qcm_sante déjà dans le switcher → on s'assure qu'elle est bien branchée
4. MNA reste dans QcmSanteScreen (déjà là), on l'enlève du QCM2
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# ─── FIX 1 : Ajouter mission 4 dans MISSIONS ───
OLD_MISSIONS = '''  const MISSIONS = [
    { id:0, label:"Habitudes alimentaires", sub:"17 questions · QCM", color:"#FA8072", top:"30%", left:"9%", action:onStartQcm1 },
    { id:1, label:"Fabrique à Menus", sub:"5 questions · QCM", color:"#ffcc00", top:"47%", left:"22%", action:onStartQcm2 },
    { id:2, label:"Compose ton assiette", sub:"Mini-jeu interactif", color:"#9ACD32", top:"68%", left:"53%", action:onStartMinijeu },
  ];'''

NEW_MISSIONS = '''  const MISSIONS = [
    { id:0, label:"Habitudes alimentaires", sub:"17 questions · QCM", color:"#FA8072", top:"30%", left:"9%", action:onStartQcm1 },
    { id:1, label:"Fabrique à Menus", sub:"5 questions · QCM", color:"#ffcc00", top:"47%", left:"22%", action:onStartQcm2 },
    { id:2, label:"Compose ton assiette", sub:"Mini-jeu interactif", color:"#9ACD32", top:"68%", left:"53%", action:onStartMinijeu },
    { id:3, label:"Mon profil santé", sub:"QCM · Profil & pathologies", color:"#7C3AED", top:"25%", left:"65%", action:onStartSante },
  ];'''

if OLD_MISSIONS in code:
    code = code.replace(OLD_MISSIONS, NEW_MISSIONS)
    fixes += 1; print("✅ FIX 1 — Mission 4 ajoutée sur la carte")
else:
    print("⚠️ FIX 1 — MISSIONS non trouvée")

# ─── FIX 2 : Ajouter onStartSante dans QcmSelectScreen signature ───
OLD_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu }) {'
NEW_SIG = 'function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked }) {'
if OLD_SIG in code:
    code = code.replace(OLD_SIG, NEW_SIG)
    fixes += 1; print("✅ FIX 2 — Signature QcmSelectScreen mise à jour")

# ─── FIX 3 : Verrouiller mission 4 si pas encore débloquée ───
OLD_MAP = '''      {MISSIONS.map((m) => (
        <div key={m.id} style={{ position:"absolute", top:m.top, left:m.left, zIndex:10 }}
          onMouseEnter={() => setHovered(m.id)}
          onMouseLeave={() => setHovered(null)}>
          <div style={{ position:"absolute", bottom:"110%", left:"-70px", width:"180px", background:"white", border:`3px solid ${m.color}`, borderRadius:14, padding:"8px 12px", textAlign:"center", opacity: hovered === m.id ? 1 : 0, transition:"opacity 0.15s", pointerEvents:"none" }}>
            <div style={{ fontSize:12, fontWeight:900, color:m.color }}>{m.label}</div>
            <div style={{ fontSize:11, color:"#888", marginTop:2 }}>{m.sub}</div>
          </div>
          <div onClick={() => { playSound("click"); m.action && m.action(); }}
            style={{ width:90, height:90, borderRadius:"50%", background: m.color, border:"3px solid white", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center", fontSize:18, fontWeight:900, color:"white", boxShadow:`0 4px 16px ${m.color}88`, transform: hovered===m.id ? "scale(1.2)" : "scale(1)", transition:"transform 0.2s" }}>
            {m.id + 1}
          </div>
        </div>
      ))}'''

NEW_MAP = '''      {MISSIONS.map((m) => {
        const isLocked = m.id === 3 && !mission4Unlocked;
        return (
          <div key={m.id} style={{ position:"absolute", top:m.top, left:m.left, zIndex:10 }}
            onMouseEnter={() => setHovered(m.id)}
            onMouseLeave={() => setHovered(null)}>
            <div style={{ position:"absolute", bottom:"110%", left:"-70px", width:"180px", background:"white", border:`3px solid ${isLocked?"#ccc":m.color}`, borderRadius:14, padding:"8px 12px", textAlign:"center", opacity: hovered === m.id ? 1 : 0, transition:"opacity 0.15s", pointerEvents:"none" }}>
              <div style={{ fontSize:12, fontWeight:900, color:isLocked?"#ccc":m.color }}>{isLocked?"🔒 Mission verrouillée":m.label}</div>
              <div style={{ fontSize:11, color:"#888", marginTop:2 }}>{m.sub}</div>
            </div>
            <div onClick={() => { if(isLocked) return; playSound("click"); m.action && m.action(); }}
              style={{ width:90, height:90, borderRadius:"50%", background: isLocked?"#bbb":m.color, border:"3px solid white", cursor:isLocked?"not-allowed":"pointer", display:"flex", alignItems:"center", justifyContent:"center", fontSize:18, fontWeight:900, color:"white", boxShadow:`0 4px 16px ${isLocked?"#bbb":m.color}88`, transform: hovered===m.id && !isLocked ? "scale(1.2)" : "scale(1)", transition:"transform 0.2s", opacity:isLocked?0.5:1 }}>
              {isLocked ? "🔒" : m.id + 1}
            </div>
          </div>
        );
      })}'''

if OLD_MAP in code:
    code = code.replace(OLD_MAP, NEW_MAP)
    fixes += 1; print("✅ FIX 3 — Mission 4 verrouillée jusqu'à fin mini-jeu")
else:
    print("⚠️ FIX 3 — MAP non trouvée")

# ─── FIX 4 : Ajouter state mission4Unlocked dans App ───
OLD_STATE = '  const [completedNodes, setCompletedNodes] = useState([]);'
NEW_STATE = '  const [completedNodes, setCompletedNodes] = useState([]);\n  const [mission4Unlocked, setMission4Unlocked] = useState(false);'
if OLD_STATE in code:
    code = code.replace(OLD_STATE, NEW_STATE)
    fixes += 1; print("✅ FIX 4 — State mission4Unlocked ajouté")

# ─── FIX 5 : MinijeuScreen — bouton retour → débloque mission 4 et affiche message Max ───
OLD_BACK_BTN = '          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>← Retour</button>'
NEW_BACK_BTN = '          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>← Retour au menu</button>'
if OLD_BACK_BTN in code:
    code = code.replace(OLD_BACK_BTN, NEW_BACK_BTN)
    fixes += 1; print("✅ FIX 5 — Bouton retour mini-jeu mis à jour")

# ─── FIX 6 : Phase minijeu dans App — onBack débloque mission 4 ───
OLD_MINIJEU_PHASE = '    if (phase === "minijeu") return <MinijeuScreen playerName={playerName} playerInfos={playerInfos}'
# Find the full line
import re
m = re.search(r'if \(phase === "minijeu"\) return <MinijeuScreen[^\n]+', code)
if m:
    old_line = m.group(0)
    new_line = old_line.replace(
        'onBack={() => goBack()}',
        'onBack={() => { setMission4Unlocked(true); setPhase("select_mission4"); setPhaseHistory([]); }}'
    )
    if new_line != old_line:
        code = code.replace(old_line, new_line)
        fixes += 1; print("✅ FIX 6 — onBack mini-jeu débloque mission 4")
    else:
        print("⚠️ FIX 6 — onBack pas trouvé dans ligne minijeu")

# ─── FIX 7 : Ajouter phase select_mission4 (QcmSelectScreen avec message Max) ───
OLD_SELECT = '    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()}'
m2 = re.search(r'if \(phase === "qcm_sante"\) return <QcmSanteScreen[^\n]+', code)
if m2:
    old_sante = m2.group(0)
    # Add select_mission4 phase before qcm_sante
    new_insert = '''    if (phase === "select_mission4") return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/frigo.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center" }}>
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.45)" }} />
        <div style={{ position:"relative", zIndex:1, display:"flex", flexDirection:"column", alignItems:"center", gap:24, maxWidth:500, width:"100%" }}>
          <div style={{ display:"flex", alignItems:"flex-end", gap:16 }}>
            <img src="/e.png" alt="Max" style={{ width:120, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))" }} />
            <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", flex:1 }}>
              <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
              <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                Bravo ! Tu as composé ton assiette ! 🎉<br/>
                <span style={{ fontSize:14, fontWeight:600, color:"#555" }}>Il te reste une dernière mission — et pas des moindres : ton <strong>profil de santé</strong>. Prêt(e) ?</span>
              </div>
            </div>
          </div>
          <button onClick={() => { playSound("click"); setPhase("qcm_sante"); }}
            style={{ background:"#7C3AED", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:18, fontWeight:900, padding:"18px 48px", cursor:"pointer", boxShadow:"5px 5px 0 #222" }}>
            🏥 Commencer ma dernière mission →
          </button>
          <button onClick={() => setPhase("select")}
            style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:10, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"8px 20px" }}>
            Retour au menu principal
          </button>
        </div>
      </div>
    );
    ''' + old_sante
    code = code.replace(old_sante, new_insert)
    fixes += 1; print("✅ FIX 7 — Phase select_mission4 avec Max ajoutée")

# ─── FIX 8 : Passer mission4Unlocked au QcmSelectScreen ───
OLD_SELECT_RENDER = 'return <QcmSelectScreen playerName={playerName}\n      onStartQcm1={() => { playSound("click"); goTo("qcm1"); }}\n      onStartQcm2={() => { playSound("click"); goTo("qcm2"); }}\n      onStartMinijeu={() => { playSound("click"); goTo("minijeu"); }} />;'
NEW_SELECT_RENDER = 'return <QcmSelectScreen playerName={playerName}\n      onStartQcm1={() => { playSound("click"); goTo("qcm1"); }}\n      onStartQcm2={() => { playSound("click"); goTo("qcm2"); }}\n      onStartMinijeu={() => { playSound("click"); goTo("minijeu"); }}\n      onStartSante={() => { playSound("click"); goTo("qcm_sante"); }}\n      mission4Unlocked={mission4Unlocked} />;'
if OLD_SELECT_RENDER in code:
    code = code.replace(OLD_SELECT_RENDER, NEW_SELECT_RENDER)
    fixes += 1; print("✅ FIX 8 — Props mission4 passés au QcmSelectScreen")
else:
    # Try finding it with regex
    m3 = re.search(r'return <QcmSelectScreen playerName=\{playerName\}[^;]+;', code, re.DOTALL)
    if m3:
        old_render = m3.group(0)
        if 'onStartSante' not in old_render:
            new_render = old_render.rstrip(';').rstrip() + '\n      onStartSante={() => { playSound("click"); goTo("qcm_sante"); }}\n      mission4Unlocked={mission4Unlocked} />;'
            code = code.replace(old_render, new_render)
            fixes += 1; print("✅ FIX 8 — Props mission4 ajoutés (v2)")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"\n{fixes} fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
