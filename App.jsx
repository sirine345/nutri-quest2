import { useState, useEffect, useRef } from "react";

/* ══ STYLES GLOBAUX ══ */
const GlobalStyles = () => (
  <style>{`
    @keyframes fadeUp { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
    .i1 { animation: fadeUp 0.6s ease 0.1s both; }
    .i2 { animation: fadeUp 0.6s ease 0.3s both; }
    .i3 { animation: fadeUp 0.6s ease 0.5s both; }
    .i4 { animation: fadeUp 0.6s ease 0.65s both; }
    .i5 { animation: fadeUp 0.6s ease 0.8s both; }
    .n1 { animation: fadeUp 0.6s ease 0.1s both; }
    .n2 { animation: fadeUp 0.6s ease 0.3s both; }
    .n3 { animation: fadeUp 0.6s ease 0.5s both; }
    .n4 { animation: fadeUp 0.6s ease 0.7s both; }
    .name-input { border:none; border-bottom:2px solid #ddd; background:transparent; padding:14px 4px; font-size:32px; text-align:center; font-family:inherit; color:#1a1a1a; transition:border-color 0.2s; width:100%; max-width:500px; }
    .name-input:focus { outline:none; border-bottom-color:#FA8072; }
    .name-input::placeholder { color:#ccc; }
    @keyframes sceneFadeIn { from { opacity:0; transform:translateX(30px); } to { opacity:1; transform:translateX(0); } }
    @keyframes sceneFadeOut { from { opacity:1; } to { opacity:0; } }
    @keyframes dialogueSlideUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
    .scene-content { animation: sceneFadeIn 0.35s ease forwards; }
    .scene-content.fading { animation: sceneFadeOut 0.3s ease forwards; }
    .scene-content.hidden { opacity:0; }
    .dialogue-box { animation: dialogueSlideUp 0.4s ease 0.2s both; }
    @keyframes mapIn   { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
    @keyframes nodePop { 0%{transform:scale(0)} 70%{transform:scale(1.15)} 100%{transform:scale(1)} }
    @keyframes pulse   { 0%,100%{transform:scale(1)} 50%{transform:scale(1.1)} }
    @keyframes pathGrow { from{stroke-dashoffset:300} to{stroke-dashoffset:0} }
    .map-in  { animation: mapIn 0.5s ease both; }
    .node-pop { animation: nodePop 0.4s cubic-bezier(0.34,1.56,0.64,1) both; }
    .node-pulse { animation: pulse 1.6s ease-in-out infinite; }
    .path-anim { stroke-dasharray:300; animation: pathGrow 0.6s ease forwards; }
    @keyframes blink {
      0%,100% { opacity:1; transform:scale(1) translateX(-50%); box-shadow:0 0 0 0 rgba(255,220,50,0.7); }
      50% { opacity:0.85; transform:scale(1.1) translateX(-50%); box-shadow:0 0 0 12px rgba(255,220,50,0); }
    }
    @keyframes lightIn { from { opacity:0; } to { opacity:1; } }
    @keyframes floatCard0 { from { opacity:0; transform:translateY(60px) scale(0.7); } to { opacity:1; transform:translateY(0) scale(1); } }
    @keyframes floatCard1 { from { opacity:0; transform:translateY(80px) scale(0.7); } to { opacity:1; transform:translateY(0) scale(1); } }
    @keyframes floatCard2 { from { opacity:0; transform:translateY(100px) scale(0.7); } to { opacity:1; transform:translateY(0) scale(1); } }
    @keyframes floating { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(-8px); } }
    @keyframes maxIn { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }
  `}</style>
);

/* ══ saveGame ══ */
const saveGame = async (data) => {
  try {
    const res = await fetch("http://127.0.0.1:8000/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    console.log("Sauvegarde OK :", result);
  } catch (error) {
    console.error("Erreur save :", error);
  }
};

/* ══ SONS WEB AUDIO API ══ */
let _audioCtx = null;
function getAudioCtx() {
  if (!_audioCtx) _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (_audioCtx.state === "suspended") _audioCtx.resume();
  return _audioCtx;
}
function playSound(type) {
  try {
    const ac = getAudioCtx();
    if (type === "click") {
      const o = ac.createOscillator(), g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = "sine"; o.frequency.value = 440;
      g.gain.setValueAtTime(0.15, ac.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.08);
      o.start(); o.stop(ac.currentTime + 0.08);
    } else if (type === "good") {
      [523, 659, 784].forEach((freq, i) => {
        const o = ac.createOscillator(), g = ac.createGain();
        o.connect(g); g.connect(ac.destination);
        o.type = "sine"; o.frequency.value = freq;
        g.gain.setValueAtTime(0.15, ac.currentTime + i * 0.12);
        g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + i * 0.12 + 0.15);
        o.start(ac.currentTime + i * 0.12); o.stop(ac.currentTime + i * 0.12 + 0.2);
      });
    } else if (type === "badge") {
      [523, 659, 784, 1046].forEach((freq, i) => {
        const o = ac.createOscillator(), g = ac.createGain();
        o.connect(g); g.connect(ac.destination);
        o.type = "sine"; o.frequency.value = freq;
        g.gain.setValueAtTime(0.18, ac.currentTime + i * 0.1);
        g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + i * 0.1 + 0.3);
        o.start(ac.currentTime + i * 0.1); o.stop(ac.currentTime + i * 0.1 + 0.35);
      });
    } else if (type === "next") {
      const o = ac.createOscillator(), g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = "sine"; o.frequency.value = 392;
      g.gain.setValueAtTime(0.1, ac.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.12);
      o.start(); o.stop(ac.currentTime + 0.12);
    }
  } catch(e) {}
}
function useSfx() { return playSound; }

/* ══ VOIX WEB SPEECH API ══ */
function speak(text) {
  try {
    const synth = window.speechSynthesis;
    synth.cancel();
    if (!text) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "fr-FR";
    utter.rate = 0.88;
    utter.pitch = 1.05;
    utter.volume = 0.9;
    const voices = synth.getVoices();
    const frVoice = voices.find(v => v.lang.startsWith("fr"));
    if (frVoice) utter.voice = frVoice;
    synth.speak(utter);
  } catch(e) {}
}
function stopSpeech() {
  try { window.speechSynthesis.cancel(); } catch(e) {}
}

/* ══ SCÈNES ══ */
const SCENES_BY_NODE = {
  0: [
    { bg: "exterior", speaker: "narrator", text: "Une ville animée. Dans les rues, fast-foods et marchés se côtoient. L'alimentation de toute une génération est en jeu..." },
    { bg: "exterior", speaker: "narrator", text: "Tu reçois un message mystérieux sur ton téléphone : Rejoins-moi. Ta cuisine, 14h. — Max" },
  ],
  1: [
    { bg: "kitchen", speaker: "max", text: "Ah, tu es là ! Je t'attendais. Je m'appelle Max, coach nutrition. Et je vais avoir besoin de toi." },
    { bg: "kitchen", speaker: "max", text: "Regarde autour de toi. Cette cuisine cache des secrets. Chaque aliment a une histoire, un impact sur ton corps." },
    { bg: "kitchen", speaker: "player", text: "..." },
    { bg: "kitchen", speaker: "max", text: "Je sais ce que tu penses. Encore un cours de nutrition. Mais non. Ici, on va jouer. Et chaque choix compte." },
  ],
  2: [
    { bg: "market", speaker: "narrator", text: "Max t'emmène au marché. Les étals regorgent de couleurs : légumes frais, fruits de saison, poissons scintillants." },
    { bg: "market", speaker: "max", text: "Tu vois tout ça ? Des légumineuses, des céréales complètes, des fruits à coque... C'est ton arsenal. Ta puissance." },
    { bg: "market", speaker: "max", text: "Mais attention ! L'ennemi rôde aussi. Les aliments ultra-transformés, les sucres cachés, la charcuterie en excès..." },
    { bg: "market", speaker: "player", text: "Comment je sais quoi choisir ?" },
    { bg: "market", speaker: "max", text: "C'est exactement pour ça que je suis là ! Ensemble, on va construire ton profil nutritionnel." },
  ],
  3: [
    { bg: "lab", speaker: "narrator", text: "Vous entrez dans le laboratoire de Max. Des graphiques, des données nutritionnelles, des recettes partout." },
    { bg: "lab", speaker: "max", text: "Deux missions t'attendent. La première : évaluer tes habitudes alimentaires. La seconde : construire ta Fabrique à Menus." },
    { bg: "lab", speaker: "max", text: "Prêt(e) à commencer, {name} ? Ton alimentation n'attend plus !" },
  ],
};
const SCENES = Object.values(SCENES_BY_NODE).flat();

/* ══ DÉCORS ══ */
function BgExterior() {
  return <div style={{ position:"absolute", inset:0 }}><img src="/chambre.png" alt="chambre" style={{ width:"100%", height:"100%", objectFit:"fill" }} /></div>;
}
function BgKitchen() {
  return <div style={{ position:"absolute", inset:0 }}><img src="/cuisine2.png" alt="cuisine" style={{ width:"100%", height:"100%", objectFit:"cover" }} /></div>;
}
function BgMarket() {
  return <div style={{ position:"absolute", inset:0 }}><img src="/marché.png" alt="marché" style={{ width:"100%", height:"100%", objectFit:"cover" }} /></div>;
}
function BgLab() {
  return <div style={{ position:"absolute", inset:0 }}><img src="/laboratoire.png" alt="labo" style={{ width:"100%", height:"100%", objectFit:"cover" }} /></div>;
}
const BG_MAP = { exterior: BgExterior, kitchen: BgKitchen, market: BgMarket, lab: BgLab };

/* ══ PERSONNAGES ══ */
function CharMax({ talking }) {
  return (
    <div style={{ position:"absolute", bottom:0, right:"6%", width:550, height:750, filter:talking?"drop-shadow(4px 4px 0 rgba(0,0,0,0.35))":"drop-shadow(4px 4px 0 rgba(0,0,0,0.2))", transition:"filter 0.3s, transform 0.3s", transform:talking?"scale(1.03)":"scale(1)" }}>
      <img src="/e.png" alt="Max" style={{ width:"100%", height:"100%", objectFit:"cover", objectPosition:"top" }} />
    </div>
  );
}
function CharPlayer({ talking, avatarSrc }) {
  return (
    <div style={{ position:"absolute", bottom:0, left:"6%", width:800, height:700, filter:talking?"drop-shadow(4px 4px 0 rgba(196,98,45,0.5))":"drop-shadow(4px 4px 0 rgba(0,0,0,0.2))", transition:"filter 0.3s, transform 0.3s", transform:talking?"scale(1.03)":"scale(1)" }}>
      <img src={avatarSrc || "/avatar.png"} style={{ width:"100%", height:"100%", objectFit:"contain" }} alt="Joueur" />
    </div>
  );
}

/* ══ CHOIX AVATAR ══ */
function AvatarScreen({ playerName, onChoose }) {
  const [hovered, setHovered] = useState(null);
  const [selected, setSelected] = useState(null);
  const avatars = [
    { id: "fille",  src: "/fille.png",  label: "Fille",  color:"#FA8072" },
    { id: "garcon", src: "/garcon.png", label: "Garçon", color:"#9ACD32" },
  ];
  const handleChoose = (id) => {
    setSelected(id);
    setTimeout(() => onChoose(id), 500);
  };
  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert2.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.15)" }} />

      <div style={{ position:"relative", zIndex:1, display:"flex", flexDirection:"column", height:"100vh", padding:"20px 40px 16px", boxSizing:"border-box" }}>

        {/* Haut — Max + bulle */}
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, marginBottom:16, flexShrink:0 }}>
          <img src="/e.png" style={{ width:80, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))", flexShrink:0 }} alt="Max" />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"12px 18px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", fontSize:15, color:"#333", lineHeight:1.6, maxWidth:400 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:3 }}>Max — Coach Nutrition</div>
            Bonjour <strong>{playerName}</strong> ! Choisis ton personnage pour commencer l'aventure !
          </div>
        </div>

        {/* Titre */}
        <div style={{ textAlign:"center", marginBottom:16, flexShrink:0 }}>
          <h1 style={{ fontSize:56, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.2)", margin:0, lineHeight:1.1 }}>
            Choisis ton <span style={{ color:"#ffdd44" }}>personnage</span>
          </h1>
        </div>

        {/* Cartes avatars */}
        <div style={{ flex:1, display:"flex", gap:32, minHeight:0 }}>
          {avatars.map(av => (
            <div key={av.id}
              onClick={() => handleChoose(av.id)}
              onMouseEnter={() => setHovered(av.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                flex:1,
                background: selected===av.id ? av.color+"33" : hovered===av.id ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.15)",
                border: `4px solid ${selected===av.id ? av.color : hovered===av.id ? "white" : "rgba(255,255,255,0.4)"}`,
                borderRadius:24,
                cursor:"pointer",
                display:"flex",
                flexDirection:"column",
                alignItems:"center",
                justifyContent:"flex-end",
                padding:"16px 16px 24px",
                transition:"all 0.25s cubic-bezier(0.34,1.56,0.64,1)",
                transform: selected===av.id ? "scale(1.02)" : hovered===av.id ? "translateY(-6px) scale(1.01)" : "scale(1)",
                boxShadow: selected===av.id ? `0 20px 60px ${av.color}66` : hovered===av.id ? "0 16px 50px rgba(0,0,0,0.25)" : "0 4px 20px rgba(0,0,0,0.15)",
                overflow:"hidden",
                position:"relative",
                minHeight:0,
              }}>

              {selected===av.id && (
                <div style={{ position:"absolute", top:16, right:16, width:34, height:34, borderRadius:"50%", background:av.color, display:"flex", alignItems:"center", justifyContent:"center", fontSize:16, fontWeight:900, color:"white", boxShadow:"0 4px 12px rgba(0,0,0,0.3)" }}>✓</div>
              )}

              <img src={av.src} alt={av.label}
                style={{ width:"auto", height:"80%", maxWidth:"70%", objectFit:"contain", filter:"drop-shadow(4px 8px 12px rgba(0,0,0,0.3))", marginBottom:12, flexShrink:1 }} />

              <div style={{
                fontSize:20, fontWeight:900, letterSpacing:3, textTransform:"uppercase", flexShrink:0,
                color: selected===av.id ? av.color : "white",
                textShadow: selected===av.id ? `0 0 20px ${av.color}` : "2px 2px 0 rgba(0,0,0,0.3)",
              }}>
                {av.label}
              </div>
            </div>
          ))}
        </div>

        <p style={{ textAlign:"center", fontSize:14, color:"rgba(255,255,255,0.7)", marginTop:12, marginBottom:0, flexShrink:0 }}>
          Clique sur ton personnage pour continuer
        </p>
      </div>
    </div>
  );
}

/* ══ SPLASH ══ */
function SplashScreen({ onStart }) {
  const [phase, setPhase] = useState(0);
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 600);
    const t2 = setTimeout(() => setPhase(2), 1400);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);
  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.55)" }} />
      <div style={{ position:"relative", zIndex:1, textAlign:"center", display:"flex", flexDirection:"column", alignItems:"center", gap:16 }}>
        <h1 style={{ opacity:phase>=1?1:0, transform:phase>=1?"translateY(0) scale(1)":"translateY(30px) scale(0.8)", transition:"all 0.8s cubic-bezier(0.34,1.56,0.64,1)", fontFamily:"Arial Black, Arial, sans-serif", fontSize:125, fontWeight:900, color:"#FA8072", letterSpacing:2, textShadow:"3px 3px 0 #b2dfdb", margin:0, lineHeight:1.1 }}>
          Serious Game<br />Alimentation
        </h1>
        <div style={{ opacity:phase>=1?1:0, transition:"opacity 0.6s ease 0.3s", width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"4px 0" }} />
        <p style={{ opacity:phase>=1?1:0, transition:"opacity 0.6s ease 0.4s", color:"#FFF5EE", fontSize:35, margin:0 }}>Apprends à mieux manger grâce à des conseils adaptés.</p>
        <button onClick={onStart} style={{ opacity:phase>=2?1:0, transform:phase>=2?"scale(1)":"scale(0.7)", transition:"all 0.5s cubic-bezier(0.34,1.56,0.64,1) 0.1s", marginTop:16, background:"#9ACD32", border:"3px solid #222", borderRadius:12, color:"#222", fontSize:18, fontWeight:800, padding:"30px 65px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}
          onMouseEnter={e=>{e.target.style.transform="translate(-2px,-2px)";e.target.style.boxShadow="6px 6px 0 #222";}}
          onMouseLeave={e=>{e.target.style.transform="translate(0,0)";e.target.style.boxShadow="4px 4px 0 #222";}}>
          ▶ Commencer
        </button>
      </div>
    </div>
  );
}

/* ══ INTRO ══ */
function IntroScreen({ onStart }) {
  return (
    <div style={{ position:"fixed", inset:0, background:"#FAFAF8", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", justifyContent:"space-between", padding:"52px 80px", alignItems:"center", textAlign:"center" }}>
      <div className="i1" style={{ display:"inline-flex", alignItems:"center", gap:10, background:"#EAF3DE", borderRadius:30, padding:"8px 20px", width:"fit-content" }}>
        <span style={{ fontSize:16 }}>🌿</span>
      </div>
      <h1 className="i2" style={{ fontSize:90, fontWeight:900, color:"#1a1a1a", lineHeight:1.12, margin:0 }}>
        Transformez vos habitudes<br/>alimentaires{" "}
        <span style={{ color:"#FA8072" }}>en jeu captivant</span>
      </h1>
      <p className="i3" style={{ fontSize:20, color:"#555", lineHeight:1.85, margin:0, maxWidth:820 }}>
        Développez un mode de vie plus sain en relevant des défis nutritionnels, tout en vous amusant à choisir vos repas, répondre aux questionnaires, et suivre vos progrès.
      </p>
      <div className="i4" style={{ borderLeft:"4px solid #9ACD32", padding:"28px 36px", background:"#f5f9ee", borderRadius:"0 14px 14px 0", maxWidth:820 }}>
        <p style={{ fontSize:22, fontWeight:700, color:"#639922", letterSpacing:"2px", textTransform:"uppercase", margin:"0 0 12px" }}>Qu'est-ce que le PNNS ?</p>
        <p style={{ fontSize:25, color:"#555", lineHeight:1.85, margin:0 }}>
          Le <strong style={{ color:"#333" }}>Programme National Nutrition Santé</strong> est une initiative française visant à améliorer la santé publique à travers des actions nutritionnelles. Il promeut une alimentation équilibrée, l'activité physique régulière, et la prévention des maladies liées à la nutrition.
        </p>
      </div>
      <div className="i5" style={{ display:"flex", justifyContent:"flex-end", alignItems:"center", gap:20, width:"100%" }}>
        <span style={{ fontSize:14, color:"#bbb" }}>~ 10 minutes</span>
        <button onClick={() => { playSound("click"); onStart(); }}
          style={{ background:"#FA8072", border:"none", borderRadius:14, padding:"18px 48px", fontSize:24, fontWeight:800, color:"white", cursor:"pointer", transition:"transform 0.15s, box-shadow 0.15s" }}
          onMouseEnter={e=>{ e.currentTarget.style.transform="translateY(-3px)"; e.currentTarget.style.boxShadow="0 10px 30px rgba(250,128,114,0.4)"; }}
          onMouseLeave={e=>{ e.currentTarget.style.transform="translateY(0)"; e.currentTarget.style.boxShadow="none"; }}>
          Commencer l'aventure →
        </button>
      </div>
    </div>
  );
}

/* ══ SAISIE NOM ══ */
function NameScreen({ onConfirm }) {
  const [name, setName] = useState("");
  return (
    <div style={{ position:"fixed", inset:0, background:"#FAFAF8", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", justifyContent:"space-between", padding:"52px 80px", alignItems:"center", textAlign:"center" }}>
      <div className="n1" style={{ display:"inline-flex", alignItems:"center", gap:10, background:"#EAF3DE", borderRadius:30, padding:"8px 20px" }}>
        <span style={{ fontSize:16 }}>🌿</span>
        <span style={{ fontSize:13, fontWeight:700, color:"#639922", letterSpacing:2, textTransform:"uppercase" }}>Max — Coach Nutrition</span>
      </div>
      <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:36, width:"100%" }}>
        <h1 className="n2" style={{ fontSize:90, fontWeight:900, color:"#1a1a1a", lineHeight:1.12, margin:0 }}>
          Avant de commencer,<br/>
          <span style={{ color:"#FA8072" }}>comment tu t'appelles ?</span>
        </h1>
        <p className="n3" style={{ fontSize:22, color:"#999", margin:0 }}>
          Je vais personnaliser ton aventure nutrition !
        </p>
        <input autoFocus type="text" placeholder="Ton prénom..." value={name}
          onChange={e => setName(e.target.value)}
          onKeyDown={e => e.key === "Enter" && name.trim() && onConfirm(name.trim())}
          maxLength={20}
          className="name-input n4"
        />
      </div>
      <div style={{ display:"flex", justifyContent:"flex-end", alignItems:"center", gap:20, width:"100%" }}>
        <span style={{ fontSize:14, color:"#bbb" }}>Appuie sur Entrée ou clique →</span>
        <button onClick={() => name.trim() && onConfirm(name.trim())} disabled={!name.trim()}
          style={{ background:name.trim()?"#FA8072":"#eee", border:"none", borderRadius:14, padding:"18px 48px", fontSize:24, fontWeight:800, color:name.trim()?"white":"#bbb", cursor:name.trim()?"pointer":"not-allowed", transition:"all 0.2s" }}
          onMouseEnter={e=>{ if(name.trim()) { e.currentTarget.style.transform="translateY(-3px)"; e.currentTarget.style.boxShadow="0 10px 30px rgba(250,128,114,0.4)"; }}}
          onMouseLeave={e=>{ e.currentTarget.style.transform="translateY(0)"; e.currentTarget.style.boxShadow="none"; }}>
          C'est parti →
        </button>
      </div>
    </div>
  );
}

/* ══ SCÈNE ══ */
function SceneScreen({ sceneIndex, scenes, playerName, avatarSrc, onNext, onSkipAll }) {
  const sceneList = scenes || SCENES;
  const scene = sceneList[sceneIndex] || sceneList[0];
  const rawText = (scene.text || "").replace("{name}", playerName);
  const [fading, setFading] = useState(false);
  const [visible, setVisible] = useState(true);
  const [muted, setMuted] = useState(false);

  useEffect(() => {
    setVisible(false);
    const t = setTimeout(() => { setVisible(true); if (!muted) speak(rawText); }, 80);
    return () => { clearTimeout(t); stopSpeech(); };
  }, [sceneIndex]);

  const handleClick = () => {
    stopSpeech();
    setFading(true);
    setTimeout(() => { setFading(false); onNext(); }, 280);
  };

  const BgComp = BG_MAP[scene.bg] || BgKitchen;
  const isMax = scene.speaker === "max";
  const isPlayer = scene.speaker === "player";
  const isNarrator = scene.speaker === "narrator";
  const isLast = sceneIndex === (scenes || SCENES).length - 1;

  return (
    <div onClick={handleClick} style={{ position:"fixed", inset:0, background:"#1a0f05", display:"flex", flexDirection:"column", cursor:"pointer", userSelect:"none", fontFamily:"Arial, sans-serif" }}>

      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <span style={{ color:"white", fontWeight:900, fontSize:15, textShadow:"1px 1px 0 #222" }}>Scène {sceneIndex+1} / {(scenes||SCENES).length}</span>
        <div style={{ display:"flex", gap:8 }}>
          <button onClick={e=>{ e.stopPropagation(); muted ? (setMuted(false), speak(rawText)) : (setMuted(true), stopSpeech()); }} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:14, fontWeight:800, padding:"4px 10px", cursor:"pointer" }}>
            {muted ? "🔇" : "🔊"}
          </button>
          <button onClick={e=>{e.stopPropagation();stopSpeech();onSkipAll();}} style={{ background:"#ffcc00", border:"2px solid #222", borderRadius:8, color:"#222", fontSize:12, fontWeight:800, padding:"4px 14px", cursor:"pointer", boxShadow:"2px 2px 0 #222" }}>Passer l'intro →</button>
        </div>
      </div>

      <div className={`scene-content${fading?" fading":""}${!visible?" hidden":""}`} style={{ position:"relative", flex:1, overflow:"hidden", marginTop:44 }}>
        <BgComp />
        {isNarrator && <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.1)" }} />}

        {!isNarrator && (
          <>
            <CharPlayer talking={isPlayer} avatarSrc={avatarSrc} />
            <CharMax talking={isMax} />

            {/* Bulle MAX — bulle2.png, au-dessus de sa tête côté droit */}
            {isMax && (
              <div style={{
                position:"absolute", bottom:"58%", right:"4%",
                width:320, zIndex:30,
                animation:"dialogueSlideUp 0.3s ease both",
              }}>
                <div style={{
                  position:"relative",
                  backgroundImage:"url('/bulle2.png')",
                  backgroundSize:"100% 100%",
                  backgroundRepeat:"no-repeat",
                  width:"100%", minHeight:140,
                  display:"flex", alignItems:"center", justifyContent:"center",
                  padding:"28px 36px 44px",
                  boxSizing:"border-box",
                }}>
                  <p style={{ margin:0, fontSize:15, color:"#222", lineHeight:1.65, textAlign:"center", fontWeight:600 }}>
                    {rawText}
                  </p>
                </div>
                <div style={{ textAlign:"right", marginTop:4 }}>
                  <span style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222" }}>
                    {isLast?"▶ Jouer !":"Suivant ▼"}
                  </span>
                </div>
              </div>
            )}

            {/* Bulle JOUEUR — bulle.png, au-dessus de sa tête côté gauche */}
            {isPlayer && (
              <div style={{
                position:"absolute", bottom:"58%", left:"4%",
                width:320, zIndex:30,
                animation:"dialogueSlideUp 0.3s ease both",
              }}>
                <div style={{
                  position:"relative",
                  backgroundImage:"url('/bulle.png')",
                  backgroundSize:"100% 100%",
                  backgroundRepeat:"no-repeat",
                  width:"100%", minHeight:140,
                  display:"flex", alignItems:"center", justifyContent:"center",
                  padding:"28px 36px 44px",
                  boxSizing:"border-box",
                }}>
                  <p style={{ margin:0, fontSize:15, color:"#222", lineHeight:1.65, textAlign:"center", fontWeight:600 }}>
                    {rawText}
                  </p>
                </div>
                <div style={{ textAlign:"left", marginTop:4 }}>
                  <span style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222" }}>
                    {isLast?"▶ Jouer !":"Suivant ▼"}
                  </span>
                </div>
              </div>
            )}
          </>
        )}

        <div style={{ position:"absolute", bottom:0, left:0, right:0, height:4, background:"rgba(0,0,0,0.3)" }}>
          <div style={{ height:"100%", width:`${((sceneIndex+1)/(scenes||SCENES).length)*100}%`, background:"#7FFFD4", transition:"width 0.4s ease" }} />
        </div>
      </div>

      {isNarrator && (
        <div className="dialogue-box" style={{ background:"white", borderTop:"4px solid #222", padding:"18px 24px 20px", flexShrink:0, minHeight:130, position:"relative", boxShadow:"0 -4px 0 #222" }}>
          <p style={{ color:"#c4622d", fontSize:16, lineHeight:1.7, margin:0, fontStyle:"italic", minHeight:54, fontWeight:700 }}>
            {rawText}
          </p>
          <div style={{ position:"absolute", right:20, bottom:16, color:"#9ACD32", fontSize:13, fontWeight:800, border:"2px solid #9ACD32", borderRadius:8, padding:"3px 12px", background:"white" }}>
            {isLast?"▶ Jouer !":"Suivant ▼"}
          </div>
        </div>
      )}

      {!isNarrator && <div style={{ height:20, flexShrink:0 }} />}
    </div>
  );
}

/* ══ CARTE DU MONDE ══ */
function MapScreen({ onSelectNode, completedNodes, activeNode }) {
  const [hovered, setHovered] = useState(null);

  const NODES = [
    { id:0, icon:"🏠", label:"Chez toi",   desc:"Le point de départ de l'aventure",         color:"#FA8072",  bg:"#FFF0EB" },
    { id:1, icon:"🍳", label:"La Cuisine", desc:"Là où les habitudes alimentaires naissent", color:"#ffcc00",  bg:"#FFFBE6" },
    { id:2, icon:"🛒", label:"Le Marché",  desc:"Légumes, fruits, protéines… ton arsenal",   color:"#74b87a",  bg:"#EAF5EB" },
    { id:3, icon:"🔬", label:"Le Labo",    desc:"Analyse ton profil et lance les QCM",        color:"#9ACD32",  bg:"#F0F9E0" },
  ];

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_jaune.png')", backgroundSize:"cover", backgroundPosition:"center", backgroundRepeat:"no-repeat", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.35)" }} />

      {/* Titre */}
      <div className="map-in" style={{ position:"relative", zIndex:1, textAlign:"center", marginBottom:32 }}>
        <div style={{ fontSize:12, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.2em", color:"#7FFFD4", marginBottom:8 }}>Carte de l'aventure</div>
        <h2 style={{ fontSize:58, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:0, lineHeight:1.1 }}>
          Choisis ton prochain <span style={{ color:"#ffdd44" }}>lieu</span>
        </h2>
      </div>

      {/* Cartes lieux */}
      <div className="map-in" style={{ position:"relative", zIndex:1, display:"flex", gap:24, width:"90vw", maxWidth:1000, animationDelay:"0.1s" }}>
        {NODES.map((node, i) => {
          const done = completedNodes.includes(node.id);
          const isActive = activeNode === node.id;
          const locked = node.id > 0 && !completedNodes.includes(node.id - 1);
          const isHov = hovered === node.id;

          return (
            <div key={node.id}
              className="node-pop"
              onClick={() => !locked && onSelectNode(node.id)}
              onMouseEnter={() => setHovered(node.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                flex:1,
                background: locked ? "rgba(255,255,255,0.08)" : done ? node.bg : isHov ? "rgba(255,255,255,0.95)" : "rgba(255,255,255,0.88)",
                border: `3px solid ${locked ? "rgba(255,255,255,0.2)" : done ? node.color : isActive ? node.color : isHov ? node.color : "rgba(255,255,255,0.5)"}`,
                borderRadius:20,
                padding:"28px 20px 24px",
                cursor: locked ? "not-allowed" : "pointer",
                opacity: locked ? 0.5 : 1,
                transform: isHov && !locked ? "translateY(-8px) scale(1.03)" : isActive ? "scale(1.02)" : "scale(1)",
                transition:"all 0.25s cubic-bezier(0.34,1.56,0.64,1)",
                boxShadow: done ? `0 8px 30px ${node.color}55` : isHov && !locked ? "0 16px 40px rgba(0,0,0,0.3)" : "0 4px 16px rgba(0,0,0,0.2)",
                display:"flex", flexDirection:"column", alignItems:"center", gap:12, textAlign:"center",
                animationDelay:`${i*0.1}s`,
                position:"relative",
              }}>

              {/* Badge actif */}
              {isActive && !done && (
                <div style={{ position:"absolute", top:-12, left:"50%", transform:"translateX(-50%)", background:node.color, border:"2px solid white", borderRadius:20, padding:"3px 14px", fontSize:10, fontWeight:900, color:"white", whiteSpace:"nowrap", boxShadow:"0 2px 8px rgba(0,0,0,0.2)" }}>
                  ACTIF
                </div>
              )}

              {/* Badge terminé */}
              {done && (
                <div style={{ position:"absolute", top:-12, right:14, background:"#ffcc00", border:"2px solid white", borderRadius:"50%", width:28, height:28, display:"flex", alignItems:"center", justifyContent:"center", fontSize:14, fontWeight:900, boxShadow:"0 2px 8px rgba(0,0,0,0.2)" }}>
                  ✓
                </div>
              )}

              {/* Icône */}
              <div style={{
                width:70, height:70, borderRadius:"50%",
                background: locked ? "#888" : done ? node.color : isHov ? node.color : node.bg,
                border: `3px solid ${locked ? "#666" : node.color}`,
                display:"flex", alignItems:"center", justifyContent:"center",
                fontSize:32,
                boxShadow: !locked ? `0 4px 16px ${node.color}55` : "none",
                transition:"all 0.2s",
              }}>
                {locked ? "🔒" : node.icon}
              </div>

              {/* Label */}
              <div style={{ fontSize:16, fontWeight:900, color: locked ? "#aaa" : done ? node.color : "#222", letterSpacing:1 }}>
                {node.label}
              </div>

              {/* Description */}
              <div style={{ fontSize:12, color: locked ? "#888" : "#666", lineHeight:1.5, maxWidth:140 }}>
                {node.desc}
              </div>

              {/* Bouton */}
              {!locked && (
                <div style={{
                  marginTop:4, padding:"8px 20px",
                  background: done ? node.color : isActive ? node.color : "rgba(0,0,0,0.08)",
                  borderRadius:20, fontSize:12, fontWeight:900,
                  color: done || isActive ? "white" : "#555",
                  border: `2px solid ${done || isActive ? node.color : "rgba(0,0,0,0.1)"}`,
                  transition:"all 0.2s",
                }}>
                  {done ? "Rejouer →" : isActive ? "Continuer →" : "Découvrir →"}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Légende */}
      <div className="map-in" style={{ position:"relative", zIndex:1, marginTop:28, display:"flex", gap:20, animationDelay:"0.3s" }}>
        {[["#9ACD32","Terminé"],["#FA8072","En cours"],["rgba(255,255,255,0.3)","Verrouillé"]].map(([c,l]) => (
          <div key={l} style={{ display:"flex", alignItems:"center", gap:6, fontSize:12, color:"rgba(255,255,255,0.7)", fontWeight:700 }}>
            <div style={{ width:12, height:12, borderRadius:"50%", background:c, border:"1.5px solid rgba(255,255,255,0.4)" }} />
            {l}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ══ MINI-JEU COMPOSE TON ASSIETTE ══ */
const FOODS_LIST = [
  { id:"legumes",     emoji:"🥦", name:"Légumes",     type:"plate", pnns:"legumes",   good:true  },
  { id:"feculents",   emoji:"🍚", name:"Féculents",   type:"plate", pnns:"feculents", good:true  },
  { id:"poisson",     emoji:"🐟", name:"Poisson",     type:"plate", pnns:"proteines", good:true  },
  { id:"viande",      emoji:"🥩", name:"Viande",      type:"plate", pnns:"proteines", good:true  },
  { id:"fruits",      emoji:"🍎", name:"Fruits",      type:"plate", pnns:"fruits",    good:true  },
  { id:"oeuf",        emoji:"🥚", name:"Oeuf",        type:"plate", pnns:"proteines", good:true  },
  { id:"charcuterie", emoji:"🌭", name:"Charcuterie", type:"plate", pnns:"bad",       good:false },
  { id:"fastfood",    emoji:"🍔", name:"Fast food",   type:"plate", pnns:"bad",       good:false },
  { id:"legumesec",   emoji:"🫘", name:"Légum. secs", type:"plate", pnns:"legumes",   good:true  },
  { id:"fromage",     emoji:"🧀", name:"Fromage",     type:"plate", pnns:"laitiers",  good:true  },
  { id:"salade",      emoji:"🥗", name:"Salade",      type:"entree", pnns:"legumes",  good:true  },
  { id:"soupe",       emoji:"🍲", name:"Soupe",       type:"entree", pnns:"legumes",  good:true  },
  { id:"crudites",    emoji:"🥕", name:"Crudités",    type:"entree", pnns:"legumes",  good:true  },
  { id:"avocat",      emoji:"🥑", name:"Avocat",      type:"entree", pnns:"legumes",  good:true  },
  { id:"yaourt",      emoji:"🍦", name:"Yaourt",      type:"dessert", pnns:"laitiers", good:true  },
  { id:"compote",     emoji:"🫙", name:"Compote",     type:"dessert", pnns:"fruits",  good:true  },
  { id:"gateau",      emoji:"🍰", name:"Gâteau",      type:"dessert", pnns:"bad",     good:false },
  { id:"fraise",      emoji:"🍓", name:"Fruit rouge", type:"dessert", pnns:"fruits",  good:true  },
  { id:"eau",  emoji:"💧", name:"Eau",       type:"glass", pnns:"eau",  good:true,  color:"#85B7EB" },
  { id:"jus",  emoji:"🍊", name:"Jus fruit", type:"glass", pnns:"jus",  good:true,  color:"#EF9F27" },
  { id:"soda", emoji:"🥤", name:"Soda",      type:"glass", pnns:"bad",  good:false, color:"#E24B4A" },
  { id:"lait", emoji:"🥛", name:"Lait",      type:"glass", pnns:"lait", good:true,  color:"#B5D4F4" },
];

function MinijeuScreen({ onBack }) {
  const [plate, setPlate] = useState([]);
  const [entree, setEntree] = useState([]);
  const [dessert, setDessert] = useState([]);
  const [glass, setGlass] = useState(null);
  const [dragId, setDragId] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [feedbackColor, setFeedbackColor] = useState("#666");

  const usedIds = [...plate.map(f=>f.id), ...entree.map(f=>f.id), ...dessert.map(f=>f.id), ...(glass?[glass.id]:[])];

  const getBars = () => {
    const bars = { legumes:0, feculents:0, proteines:0, fruits:0, laitiers:0, eau:0 };
    [...plate, ...entree, ...dessert].forEach(f => {
      if(f.pnns && bars[f.pnns]!==undefined) bars[f.pnns] = Math.min(bars[f.pnns]+33, 100);
    });
    if(glass) { bars.eau = glass.good ? 100 : 20; }
    return bars;
  };

  const handleDrop = (zone) => {
    if(!dragId) return;
    const food = FOODS_LIST.find(f=>f.id===dragId);
    if(!food) return;
    if(zone==="plate" && food.type==="plate") {
      if(plate.length >= 5) return;
      setPlate(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]);
    } else if(zone==="entree" && food.type==="entree") {
      if(entree.length >= 2) return;
      setEntree(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]);
    } else if(zone==="dessert" && food.type==="dessert") {
      if(dessert.length >= 2) return;
      setDessert(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]);
    } else if(zone==="glass" && food.type==="glass") {
      setGlass(food);
    }
    setDragId(null);
  };

  const removeFromPlate = (id) => setPlate(prev=>prev.filter(f=>f.id!==id));
  const removeFromEntree = (id) => setEntree(prev=>prev.filter(f=>f.id!==id));
  const removeFromDessert = (id) => setDessert(prev=>prev.filter(f=>f.id!==id));
  const removeGlass = () => setGlass(null);

  const valider = () => {
    const allFoods = [...plate, ...entree, ...dessert];
    const bad = allFoods.filter(f=>!f.good);
    const good = allFoods.filter(f=>f.good);
    const badDrink = glass && !glass.good;
    saveGame({ type:"minijeu", data: {
      plate: plate.map(f => f.name),
      entree: entree.map(f => f.name),
      dessert: dessert.map(f => f.name),
      glass: glass ? glass.name : null,
      bons_aliments: good.map(f => f.name),
      mauvais_aliments: bad.map(f => f.name),
      score: good.length + bad.length > 0 ? Math.round((good.length/(good.length+bad.length))*100) : 0
    }});
    if(bad.length===0 && !badDrink && good.length>=2) {
      setFeedback("Bonne assiette ! " + good.length + " aliment" + (good.length>1?"s":"") + " sain" + (good.length>1?"s":"") + (glass?" + boisson adaptée":"") + ". Score PNNS : " + Math.round((good.length/(good.length+bad.length))*100) + "%");
      setFeedbackColor("#2e7d32");
      playSound("badge");
    } else {
      const issues = [];
      if(bad.length) issues.push(bad.map(f=>f.name).join(", ") + " déconseillé" + (bad.length>1?"s":""));
      if(badDrink) issues.push("le soda est déconseillé");
      if(!glass) issues.push("ajoute une boisson");
      setFeedback(issues.join(" · ") + ".");
      setFeedbackColor("#c4622d");
    }
  };

  const reset = () => { setPlate([]); setEntree([]); setDessert([]); setGlass(null); setFeedback(""); };
  const bars = getBars();

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.55)" }} />
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <span style={{ color:"white", fontWeight:900, fontSize:14 }}>Compose ton repas</span>
        <div style={{ display:"flex", gap:10 }}>
          <button onClick={reset} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"4px 12px", cursor:"pointer" }}>Réinitialiser</button>
          <button onClick={onBack} style={{ background:"#ffcc00", border:"2px solid #222", borderRadius:8, color:"#222", fontSize:12, fontWeight:800, padding:"4px 12px", cursor:"pointer", boxShadow:"2px 2px 0 #222" }}>← Menu</button>
        </div>
      </div>
      <div style={{ position:"relative", zIndex:1, display:"grid", gridTemplateColumns:"200px 1fr 80px", height:"100vh", paddingTop:50 }}>
        <div style={{ background:"rgba(255,255,255,0.92)", borderRight:"3px solid #222", overflowY:"auto", padding:12 }}>
          {[
            { label:"Entrée", type:"entree" },
            { label:"Plat", type:"plate" },
            { label:"Dessert", type:"dessert" },
            { label:"Boisson", type:"glass" },
          ].map(section => (
            <details key={section.type} open style={{ marginBottom:10 }}>
              <summary style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:2, color:"#c4622d", marginBottom:6, cursor:"pointer", listStyle:"none", display:"flex", justifyContent:"space-between", alignItems:"center", padding:"4px 0" }}>
                {section.label} <span>▾</span>
              </summary>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:6, marginTop:6 }}>
                {FOODS_LIST.filter(f=>f.type===section.type).map(food => {
                  const used = usedIds.includes(food.id);
                  return (
                    <div key={food.id} draggable={!used} onDragStart={() => !used && setDragId(food.id)} onDragEnd={() => setDragId(null)}
                      style={{ background:used?"#f0f0f0":"white", border:`2px solid ${used?"#ccc":food.good?"#9ACD32":"#E24B4A"}`, borderRadius:10, padding:"8px 4px", textAlign:"center", cursor:used?"not-allowed":"grab", opacity:used?0.4:1, transition:"opacity 0.2s" }}>
                      <div style={{ fontSize:24 }}>{food.emoji}</div>
                      <div style={{ fontSize:10, fontWeight:800, color:"#333", marginTop:2 }}>{food.name}</div>
                    </div>
                  );
                })}
              </div>
            </details>
          ))}
          <div style={{ marginTop:12, fontSize:10, color:"#888", lineHeight:1.5 }}>
            <span style={{ color:"#9ACD32", fontWeight:700 }}>Vert</span> = recommandé PNNS<br/>
            <span style={{ color:"#E24B4A", fontWeight:700 }}>Rouge</span> = déconseillé
          </div>
        </div>
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"space-between", padding:16, paddingTop:20, paddingBottom:16 }}>
          <div style={{ textAlign:"center" }}>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:52, fontWeight:900, color:"#FA8072", letterSpacing:2, textShadow:"3px 3px 0 #b2dfdb", margin:0, lineHeight:1.1 }}>
              Compose ton repas
            </h1>
            <div style={{ width:60, height:4, background:"#7FFFD4", borderRadius:99, border:"2px solid #222", margin:"8px auto" }} />
            <p style={{ color:"rgba(255,255,255,0.8)", fontSize:14, margin:0 }}>Glisse les aliments sur les assiettes · la boisson sur le verre</p>
          </div>
          <div style={{ display:"flex", alignItems:"center", gap:24 }}>
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:800, textTransform:"uppercase", letterSpacing:1 }}>Entrée</div>
              <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("entree")}
                style={{ width:200, height:200, borderRadius:"50%", border:"4px solid white", background:"rgba(255,255,255,0.12)", display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:12, position:"relative" }}>
                <img src="/assiette2.png" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"contain", opacity:0.35, pointerEvents:"none" }} alt="assiette" />
                {entree.length === 0 && <span style={{ fontSize:10, color:"rgba(255,255,255,0.5)", textAlign:"center", position:"relative", zIndex:1 }}>Dépose ici</span>}
                {entree.length >= 2 && <span style={{ fontSize:10, color:"#7CCC6C", textAlign:"center", position:"relative", zIndex:1, fontWeight:800 }}>Max !</span>}
                {entree.map(food => (
                  <span key={food.id} onClick={()=>removeFromEntree(food.id)} title="Clic pour retirer"
                    style={{ fontSize:28, cursor:"pointer", position:"relative", zIndex:1 }}>{food.emoji}</span>
                ))}
              </div>
            </div>
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:800, textTransform:"uppercase", letterSpacing:1 }}>Plat principal</div>
              <div style={{ display:"flex", alignItems:"center", gap:16 }}>
                <svg width="24" height="120" viewBox="0 0 24 120">
                  <line x1="5" y1="5" x2="5" y2="40" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.8"/>
                  <line x1="10" y1="5" x2="10" y2="40" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.8"/>
                  <line x1="15" y1="5" x2="15" y2="40" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.8"/>
                  <path d="M5 40 Q10 52 10 58 L10 115" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.8"/>
                </svg>
                <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("plate")}
                  style={{ width:260, height:260, borderRadius:"50%", border:"4px solid white", background:"rgba(255,255,255,0.12)", display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:14, position:"relative" }}>
                  <img src="/assiette2.png" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"contain", opacity:0.4, pointerEvents:"none" }} alt="assiette" />
                  {plate.length === 0 && <span style={{ fontSize:11, color:"rgba(255,255,255,0.5)", textAlign:"center", position:"relative", zIndex:1 }}>Dépose ici</span>}
                  {plate.length >= 5 && <span style={{ fontSize:11, color:"#FA8072", textAlign:"center", position:"relative", zIndex:1, fontWeight:800 }}>Maximum atteint !</span>}
                  {plate.map(food => (
                    <span key={food.id} onClick={()=>removeFromPlate(food.id)} title="Clic pour retirer"
                      style={{ fontSize:32, cursor:"pointer", position:"relative", zIndex:1 }}>{food.emoji}</span>
                  ))}
                </div>
                <svg width="24" height="120" viewBox="0 0 24 120">
                  <line x1="12" y1="5" x2="12" y2="115" stroke="white" strokeWidth="2" strokeLinecap="round" opacity="0.8"/>
                  <path d="M12 5 L20 25 L12 40" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.8"/>
                </svg>
              </div>
            </div>
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, color:"rgba(255,255,255,0.7)", fontWeight:800, textTransform:"uppercase", letterSpacing:1 }}>Dessert</div>
              <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("dessert")}
                style={{ width:200, height:200, borderRadius:"50%", border:"4px solid white", background:"rgba(255,255,255,0.12)", display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:12, position:"relative" }}>
                <img src="/assiette2.png" style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"contain", opacity:0.35, pointerEvents:"none" }} alt="assiette" />
                {dessert.length === 0 && <span style={{ fontSize:10, color:"rgba(255,255,255,0.5)", textAlign:"center", position:"relative", zIndex:1 }}>Dépose ici</span>}
                {dessert.length >= 2 && <span style={{ fontSize:10, color:"#F472B6", textAlign:"center", position:"relative", zIndex:1, fontWeight:800 }}>Max !</span>}
                {dessert.map(food => (
                  <span key={food.id} onClick={()=>removeFromDessert(food.id)} title="Clic pour retirer"
                    style={{ fontSize:28, cursor:"pointer", position:"relative", zIndex:1 }}>{food.emoji}</span>
                ))}
              </div>
            </div>
          </div>
          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6, width:"100%", marginTop:-20 }}>
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("glass")} onClick={removeGlass}
                style={{ width:50, height:80, borderRadius:"0 0 8px 8px", border:"3px solid white", background:glass?glass.color+"99":"rgba(255,255,255,0.1)", overflow:"hidden", cursor:glass?"pointer":"default", position:"relative" }}>
                {glass && <div style={{ position:"absolute", bottom:0, left:0, right:0, height:"80%", background:glass.color, opacity:0.7, borderRadius:"0 0 6px 6px" }} />}
                {glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:20 }}>{glass.emoji}</div>}
              </div>
              <div style={{ fontSize:10, color:"rgba(255,255,255,0.6)", letterSpacing:1, textTransform:"uppercase" }}>{glass ? glass.name : "Boisson"}</div>
            </div>
            <button onClick={valider} style={{ background:"#9ACD32", border:"3px solid #222", borderRadius:12, color:"#222", fontSize:15, fontWeight:800, padding:"11px 32px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              Valider mon repas
            </button>
            {feedback && (
              <div style={{ background:"white", border:"3px solid #222", borderRadius:12, padding:"12px 20px", maxWidth:420, fontSize:13, lineHeight:1.6, color:feedbackColor, fontWeight:700, boxShadow:"4px 4px 0 #222", textAlign:"center" }}>
                {feedback}
              </div>
            )}
          </div>
        </div>
        <div style={{ background:"rgba(255,255,255,0.92)", borderLeft:"3px solid #222", padding:"60px 10px 12px", display:"flex", flexDirection:"column", gap:6 }}>
          <div style={{ fontSize:9, fontWeight:900, textTransform:"uppercase", letterSpacing:1, color:"#c4622d", marginBottom:6 }}>Équilibre PNNS</div>
          {[
            { key:"legumes",   label:"Légumes",   color:"#639922" },
            { key:"feculents", label:"Féculents", color:"#EF9F27" },
            { key:"proteines", label:"Protéines", color:"#378ADD" },
            { key:"fruits",    label:"Fruits",    color:"#D4537E" },
            { key:"laitiers",  label:"Laitiers",  color:"#B5D4F4" },
            { key:"eau",       label:"Boisson",   color:"#85B7EB" },
          ].map(b => (
            <div key={b.key}>
              <div style={{ fontSize:9, color:"#555", marginBottom:2 }}>{b.label}</div>
              <div style={{ height:5, background:"#eee", borderRadius:99, overflow:"hidden" }}>
                <div style={{ height:"100%", width:bars[b.key]+"%", background:b.color, borderRadius:99, transition:"width 0.3s" }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ══ SÉLECTION QCM ══ */
function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu }) {
  const [hovered, setHovered] = useState(null);

  const MISSIONS = [
    { id:0, label:"Habitudes alimentaires", sub:"17 questions · QCM", color:"#FA8072", top:"30%", left:"9%", action:onStartQcm1 },
    { id:1, label:"Fabrique à Menus", sub:"5 questions · QCM", color:"#ffcc00", top:"12%", left:"50%", action:onStartQcm2 },
    { id:2, label:"Compose ton assiette", sub:"Mini-jeu interactif", color:"#9ACD32", top:"68%", left:"43%", action:onStartMinijeu },
  ];

  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, backgroundImage:"url('/frigo.png')", backgroundSize:"cover", backgroundPosition:"center", backgroundRepeat:"no-repeat" }} />

      <div style={{ position:"absolute", bottom:24, left:0, right:0, zIndex:20, textAlign:"center" }}>
        <span style={{ fontSize:15, color:"#222", fontWeight:800, background:"rgba(255,255,255,0.85)", borderRadius:20, padding:"8px 24px", boxShadow:"0 2px 10px rgba(0,0,0,0.15)" }}>
          Clique sur un point pour commencer ta mission !
        </span>
      </div>

      {MISSIONS.map((m) => (
        <div key={m.id} style={{ position:"absolute", top:m.top, left:m.left, zIndex:10 }}
          onMouseEnter={() => setHovered(m.id)}
          onMouseLeave={() => setHovered(null)}>

          <div style={{
            position:"absolute", bottom:"110%", left:"-70px", width:"180px",
            background:"white", border:`3px solid ${m.color}`, borderRadius:14,
            padding:"8px 12px", textAlign:"center",
            opacity: hovered === m.id ? 1 : 0,
            transition:"opacity 0.15s", pointerEvents:"none",
          }}>
            <div style={{ fontSize:12, fontWeight:900, color:m.color }}>{m.label}</div>
            <div style={{ fontSize:11, color:"#888", marginTop:2 }}>{m.sub}</div>
          </div>

          <div
            onClick={() => { playSound("click"); m.action && m.action(); }}
            style={{
              width:44, height:44, borderRadius:"50%",
              background: m.color, border:"3px solid white",
              cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center",
              fontSize:18, fontWeight:900, color:"white",
              boxShadow:`0 4px 16px ${m.color}88`,
              transform: hovered===m.id ? "scale(1.2)" : "scale(1)",
              transition:"transform 0.2s",
            }}>
            {m.id + 1}
          </div>
        </div>
      ))}
    </div>
  );
}

/* ══ DONNÉES QCM 1 ══ */
const QUESTIONS = [
  { id:'legumes', icon:'legume.png', title:'Légumes frais', subtitle:'À quelle fréquence en consommez-vous ?\n(hors pommes de terre — une portion = 80-100g)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus','Ne sait pas'], nutKey:'legumes', nutMax:7, reaction:v=>v>=5?{face:'',text:'Excellent ! Tu es dans les recommandations.'}:v>=3?{face:'',text:"Pas mal ! L'OMS recommande 5 portions/jour."}:{face:'',text:"C'est peu ! Les légumes apportent vitamines et fibres."} },
  { id:'legumineuses', icon:'legumesec.png', title:'Légumes secs', subtitle:'À quelle fréquence en consommez-vous ?\n(lentilles, pois chiches, haricots secs…)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'legumineuses', nutMax:6, reaction:v=>v===0?{face:'',text:"Jamais ? Essaie les lentilles corail !"}:v<=2?{face:'',text:"C'est un début ! Le PNNS recommande 2 fois/sem."}:v<=4?{face:'',text:"Très bien ! Riches en fibres et protéines végétales."}:{face:'🎉',text:"Champion des légumineuses !"} },
  { id:'feculents', icon:'feculent.png', title:'Féculents complets', subtitle:'À quelle fréquence en consommez-vous ?\n(pain complet, pâtes complètes, riz complet…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','Tous les jours','Ne sait pas'], nutKey:'feculents', nutMax:4, reaction:v=>v===0?{face:'',text:"Essaie le pain complet !"}:v<=3?{face:'',text:"Bien ! Riches en fibres."}:{face:'🎉',text:"Excellent ! Tes apports en fibres sont optimaux !"} },
  { id:'fruits', icon:'fraise.png', title:'Fruits', subtitle:'À quelle fréquence en consommez-vous ?\n(hors jus — compotes comprises)', labels:['Jamais','1 fruit/sem ou moins','2 à 3 fruits/sem','4 à 6 fruits/sem','1 fruit/jour','2 fruits/jour','3 fruits/jour','4 fruits et plus','Ne sait pas'], nutKey:'fruits', nutMax:7, reaction:v=>v===0?{face:'',text:"Aucun fruit ? Vitamines et antioxydants essentiels !"}:v<=2?{face:'',text:"L'OMS recommande au moins 2-3 fruits/jour."}:v<=5?{face:'',text:"Bien ! Excellente source de vitamines."}:{face:'🎉',text:"Parfait !"} },
  { id:'fruitsACoque', icon:'fruit_a_coque.png', title:'Fruits à coque', subtitle:'À quelle fréquence en mangez-vous ?\n(amandes, noix, noisettes…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','Au moins 1 portion/jour','Ne sait pas'], nutKey:'fruitsACoque', nutMax:4, reaction:v=>v===0?{face:'',text:"Riches en bons acides gras !"}:v<=2?{face:'',text:"Le PNNS recommande une petite poignée/jour."}:{face:'',text:"Excellent ! Protègent ton cœur."} },
  { id:'laitiers', icon:'lait.png', title:'Produits laitiers', subtitle:'À quelle fréquence en mangez-vous ?\n(lait, yaourt, fromage)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois/jour et plus','Ne sait pas'], nutKey:'laitiers', nutMax:7, reaction:v=>v===0?{face:'',text:"Pense aux autres sources de calcium."}:v<=3?{face:'',text:"Le PNNS recommande 2 produits laitiers/jour."}:v<=5?{face:'',text:"Bien ! Tes besoins en calcium sont couverts."}:{face:'🎉',text:"Parfait !"} },
  { id:'volaille', icon:'volaille.png', title:'Volaille', subtitle:'À quelle fréquence en mangez-vous ?\n(poulet, dinde…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','1 portion/jour','2 portions et plus/jour','Ne sait pas'], nutKey:'volaille', nutMax:5, reaction:v=>v===0?{face:'',text:"Bonne source de protéines maigres."}:v<=3?{face:'',text:"Bien ! Protéines pauvres en graisses saturées."}:{face:'',text:"Attention à ne pas dépasser 500g/semaine."} },
  { id:'viande', icon:'viande.png', title:'Viande (hors volaille)', subtitle:'À quelle fréquence en mangez-vous ?\n(bœuf, porc, agneau…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','1 portion/jour','2 portions et plus/jour','Ne sait pas'], nutKey:'viande', nutMax:5, reaction:v=>v===0?{face:'',text:"Excellent pour la santé cardiovasculaire !"}:v<=2?{face:'',text:"Bien ! Limite à 500g/semaine."}:v<=3?{face:'',text:"Attention : limite à 500g/semaine."}:{face:'',text:"Trop ! Risque accru de cancer colorectal."} },
  { id:'charcuterie', icon:'charcuterie.png', title:'Charcuterie', subtitle:'À quelle fréquence en mangez-vous ?\n(jambon, saucisson, saucisses…)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'charcuterie', nutMax:6, reaction:v=>v===0?{face:'🎉',text:"Cancérigène classé par l'OMS — bien d'éviter !"}:v<=2?{face:'',text:"Bien ! Limite à 150g/semaine."}:v<=3?{face:'',text:"Riche en sel et graisses saturées."}:{face:'',text:"Trop ! Classe 1 cancérigène OMS."} },
  { id:'poisson', icon:'poisson.png', title:'Poisson & produits de la pêche', subtitle:'À quelle fréquence en consommez-vous ?\n(incluant les conserves)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'poisson', nutMax:6, reaction:v=>v===0?{face:'',text:"Oméga-3 essentiels pour le cerveau et le cœur !"}:v<=2?{face:'',text:"2 portions/semaine dont un poisson gras."}:v<=4?{face:'',text:"Bien ! Oméga-3 et protéines de qualité."}:{face:'🎉',text:"Excellent !"} },
  { id:'oeufs', icon:'oeuf.png', title:'Œufs', subtitle:'À quelle fréquence en consommez-vous ?\n(une portion = 2 œufs)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois et plus/sem','Ne sait pas'], nutKey:'oeufs', nutMax:6, reaction:v=>v===0?{face:'',text:"Excellente source de protéines et vitamines B."}:v<=3?{face:'',text:"Bien ! Protéines de haute qualité."}:{face:'',text:"Diversifie aussi tes sources de protéines."} },
  { id:'snacks', icon:'snack.png', title:'Snacks salés', subtitle:'À quelle fréquence en mangez-vous ?\n(chips, biscuits apéritifs…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'snacks', nutMax:7, reaction:v=>v===0?{face:'🎉',text:"Zéro snack ! Sel et graisses saturées évités."}:v<=2?{face:'',text:"Raisonnable ! Des plaisirs occasionnels."}:v<=4?{face:'',text:"Riches en sel et graisses."}:{face:'',text:"Trop ! Risques d'hypertension."} },
  { id:'fastFood', icon:'fast_food.png', title:'Fast food', subtitle:'À quelle fréquence en mangez-vous ?\n(hamburgers, kebabs, pizzas…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'fastFood', nutMax:7, reaction:v=>v===0?{face:'🎉',text:"Zéro fast food ! Ultra-transformés évités."}:v<=2?{face:'',text:"Occasionnellement OK."}:v<=4?{face:'',text:"Très caloriques, riches en sel."}:{face:'',text:"Trop ! Liés à l'obésité."} },
  { id:'sucres', icon:'sucrerie.png', title:'Sucreries & desserts', subtitle:'À quelle fréquence en mangez-vous ?\n(gâteaux, viennoiseries, glaces…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'sucres', nutMax:7, reaction:v=>v===0?{face:'🎉',text:"Zéro sucrerie ! Sucres ajoutés évités."}:v<=2?{face:'',text:"Raisonnable !"}:v<=4?{face:'',text:"Riches en sucres ajoutés."}:{face:'',text:"Trop ! Diabète et caries."} },
];

const BOISSONS_LABELS = ['Jamais','1 verre/sem ou moins','2 à 3 verres/sem','4 à 6 verres/sem','1 verre/jour','2 verres/jour','3 verres/jour','4 verres/jour','5 verres et plus/jour','Ne sait pas'];
const BIO_LABELS = ['Tous les jours ou presque','Souvent','Rarement','Jamais'];
const VIANDE_OPTIONS = [
  {label:"Non, mais j'ai déjà envisagé de le faire sans finalement changer",score:20},
  {label:"Non, mais j'envisage de le faire prochainement sans savoir comment",score:40},
  {label:"Non, mais j'envisage de le faire prochainement et je sais comment",score:60},
  {label:"Non, je ne vois pas l'intérêt",score:0},
  {label:"Non, car je consommais déjà peu de viande ces dernières années",score:80},
  {label:"Non, car je ne consommais pas de viande ces dernières années",score:100},
  {label:"Non, c'est une autre raison",score:10},
];
const RAISONS_LABELS = [
  "Par préoccupation pour l'impact environnemental",
  "Pour des raisons éthiques ou spirituelles (bien-être animal…)",
  "Par goût",
  "Par souci de partage et/ou de plaisir (slow food…)",
  "C'est meilleur pour ma santé",
  "Pour éviter de prendre du poids",
  "C'est moins cher",
  "Suite à une prise de conscience par les médias",
];
const NUT_CONFIG = {
  legumes:{icon:'',label:'Légumes'},legumineuses:{icon:'',label:'Légumineuses'},feculents:{icon:'',label:'Féculents'},fruits:{icon:'',label:'Fruits'},fruitsACoque:{icon:'',label:'Fruits à coque'},laitiers:{icon:'',label:'Laitiers'},volaille:{icon:'',label:'Volaille'},viande:{icon:'',label:'Viande rouge'},charcuterie:{icon:'',label:'Charcuterie'},poisson:{icon:'',label:'Poisson'},oeufs:{icon:'',label:'Œufs'},snacks:{icon:'',label:'Snacks'},fastFood:{icon:'',label:'Fast food'},boissons:{icon:'',label:'Boissons sucrées'},sucres:{icon:'',label:'Sucreries'},bio:{icon:'',label:'Bio'},reductionViande:{icon:'',label:'Réduction viande'},
};

/* ══ QCM 1 ══ */
function Qcm1Screen({ onBack }) {
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [nutrition, setNutrition] = useState({});
  const [stars, setStars] = useState(0);
  const [card, setCard] = useState("slider");
  const [sliderVal, setSliderVal] = useState(4);
  const [selectedTile, setSelectedTile] = useState(-1);
  const [selectedRadio, setSelectedRadio] = useState(-1);
  const [selectedAccord, setSelectedAccord] = useState(null);
  const [checkedRaisons, setCheckedRaisons] = useState(new Set());

  const displayQ = card==="slider"?(currentQ===QUESTIONS.length-1?15:currentQ+1):card==="tiles"?14:card==="radio"?16:card==="accord"?17:18;
  const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:600, width:"100%", textAlign:"center", border:"3px solid #222", boxShadow:"5px 5px 0 #222" };

  const addAnswer = (id, val, label, nutKey, nutMax) => {
    const nut = nutKey ? Math.min(Math.round(val / nutMax * 100), 100) : 0;
    setNutrition(prev => ({ ...prev, [nutKey || id]: nut }));
    setAnswers(prev => [...prev, { id, value: val, label }]);
    setStars(s => s + 1);
  };

  const nextSlider = () => {
    playSound("good");
    const q = QUESTIONS[currentQ];
    addAnswer(q.id, sliderVal, q.labels[sliderVal], q.nutKey, q.nutMax);
    if (currentQ === QUESTIONS.length - 2) { setCard("tiles"); setSelectedTile(-1); }
    else if (currentQ === QUESTIONS.length - 1) { setCard("radio"); setSelectedRadio(-1); }
    else { setCurrentQ(c => c + 1); setSliderVal(Math.floor((QUESTIONS[currentQ + 1].labels.length - 1) / 2)); }
  };

  const nextTiles = () => {
    playSound("good");
    if (selectedTile === -1) return;
    addAnswer('boissons', selectedTile, BOISSONS_LABELS[selectedTile], 'boissons', BOISSONS_LABELS.length - 2);
    setCurrentQ(QUESTIONS.length - 1);
    setSliderVal(Math.floor((QUESTIONS[QUESTIONS.length - 1].labels.length - 1) / 2));
    setCard("slider");
  };

  const nextRadio = () => {
    playSound("good");
    if (selectedRadio === -1) return;
    addAnswer('bio', selectedRadio, BIO_LABELS[selectedRadio], 'bio', 3);
    setCard("accord"); setSelectedAccord(null);
  };

  const nextAccord = () => {
    playSound("good");
    if (selectedAccord === null) return;
    const label = selectedAccord === "oui" ? "Oui" : VIANDE_OPTIONS[selectedAccord]?.label || "";
    const score = selectedAccord === "oui" ? 100 : VIANDE_OPTIONS[selectedAccord]?.score || 0;
    addAnswer('reductionViande', selectedAccord, label, 'reductionViande', 100);
    setNutrition(prev => ({ ...prev, reductionViande: score }));
    if (selectedAccord === "oui") { setCard("check"); setCheckedRaisons(new Set()); }
    else { setCard("result"); }
  };

  const nextCheck = () => {
    playSound("badge");
    if (checkedRaisons.size === 0) return;
    addAnswer('raisonsViande', [...checkedRaisons], [...checkedRaisons].map(i => RAISONS_LABELS[i]).join(' | '), null, 0);
    setCard("result");
  };

  const q = QUESTIONS[currentQ] || QUESTIONS[0];
  const labels = q.labels;

  if (card === "result") {
    const vals = Object.values(nutrition);
    const avg = Math.round(vals.reduce((a, b) => a + b, 0) / vals.length);
    saveGame({ type:"qcm1", data: { answers, nutrition } });
    let emoji = '', title = 'Ton bilan', sub = '';
    if (avg >= 70) { emoji = '🌟'; title = 'Excellente alimentation !'; sub = 'Tes habitudes sont vraiment exemplaires !'; }
    else if (avg >= 40) { emoji = '🥗'; title = 'Pas mal du tout !'; sub = 'Quelques points à améliorer, mais tu es sur la bonne voie.'; }
    else { emoji = '🌱'; title = 'Des progrès à faire !'; sub = 'Chaque petit changement compte.'; }
    const weakKey = Object.entries(nutrition).sort((a,b)=>a[1]-b[1])[0]?.[0];
    const weakQ = QUESTIONS.find(x=>x.nutKey===weakKey);
    const conseil = weakQ ? weakQ.reaction(0).text : 'Continue comme ça !';
    return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", gap:14, overflowY:"auto", padding:"30px 16px", fontFamily:"Arial, sans-serif" }}>
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
        <div style={{ position:"relative", zIndex:1, textAlign:"center" }}>
          <div style={{ fontSize:56 }}>{emoji}</div>
          <div style={{ fontSize:"1.8em", fontWeight:"bold", marginTop:8, color:"white" }}>{title}</div>
          <div style={{ color:"rgba(255,255,255,0.65)", marginTop:4, fontSize:"0.92em" }}>{sub}</div>
        </div>
        <div style={{ position:"relative", zIndex:1, background:"white", color:"#333", borderRadius:20, padding:"18px 20px", maxWidth:540, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222" }}>
          <h2 style={{ fontSize:"1.3em", color:"#2e7d32", marginBottom:12, textAlign:"center" }}>Ton bilan</h2>
          {answers.slice(0, 17).map((a, i) => {
            const qq = QUESTIONS.find(x => x.id === a.id);
            const cfg = NUT_CONFIG[qq?.nutKey || a.id] || NUT_CONFIG[a.id];
            const p = nutrition[qq?.nutKey || a.id] || 0;
            const cls = p >= 60 ? '#e8f5e9' : p >= 30 ? '#fff8e1' : '#fbe9e7';
            const ico = p >= 60 ? '✅' : p >= 30 ? '⚠️' : '❌';
            const r = qq ? qq.reaction(a.value) : { face: '💬', text: a.label };
            return (
              <div key={i} style={{ display:"flex", alignItems:"flex-start", gap:10, padding:"8px 10px", borderRadius:10, marginBottom:6, fontSize:"0.83em", lineHeight:1.5, background:cls }}>
                <span style={{ fontSize:16 }}>{ico}</span>
                <div><strong style={{ display:"block", color:"#222", marginBottom:2 }}>{cfg?.icon} {qq?.title || cfg?.label || a.id}</strong>{r.face} {r.text}</div>
              </div>
            );
          })}
          <div style={{ marginTop:10, background:"#e8f5e9", borderLeft:"4px solid #4caf50", borderRadius:8, padding:"10px 12px", fontSize:"0.82em", color:"#2e7d32", lineHeight:1.6 }}>
            <strong style={{ display:"block", fontSize:"0.8em", textTransform:"uppercase", marginBottom:2 }}>💡 Conseil PNNS prioritaire</strong>
            {conseil}
          </div>
        </div>
        <div style={{ position:"relative", zIndex:1, display:"flex", gap:12, flexWrap:"wrap", justifyContent:"center" }}>
          <button onClick={onBack} style={{ ...btn, background:"white" }}>← Retour au menu</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"80px 16px 40px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white", textShadow:"1px 1px 0 #222" }}>Question {displayQ} / 17</div>
        <div style={{ fontSize:19, fontWeight:"bold", color:"#ffcc00", textShadow:"1px 1px 0 #222" }}>⭐ {stars}</div>
      </div>
      {card === "slider" && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src={`/${q.icon}`} alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>{q.title}</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em", lineHeight:1.5, whiteSpace:"pre-line" }}>{q.subtitle}</p>
          <input type="range" min={0} max={labels.length-1} value={sliderVal} onChange={e=>setSliderVal(+e.target.value)} style={{ width:"100%", accentColor:"#4caf50" }} />
          <div style={{ display:"flex", justifyContent:"space-between", padding:"0 10px", marginTop:-2 }}>
            {labels.map((_,i)=><div key={i} style={{ width:8, height:8, borderRadius:"50%", background:"#4caf50", border:"2px solid #2e7d32" }} />)}
          </div>
          <div style={{ marginTop:10, fontSize:"1.2em", fontWeight:"bold", color:"#2e7d32" }}>{labels[sliderVal]}</div>
          <div style={{ display:"flex", justifyContent:"center", marginTop:20 }}>
            <button onClick={nextSlider} style={btn}>Suivant →</button>
          </div>
        </div>
      )}
      {card === "tiles" && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/soda.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Boissons sucrées</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>Quelle est ta fréquence de consommation ?<br />(jus de fruits, sirop, sodas même light…)</p>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:8, margin:"16px 0" }}>
            {BOISSONS_LABELS.map((l,i)=>(
              <div key={i} onClick={()=>setSelectedTile(i)} style={{ background:selectedTile===i?"#ffcc00":"white", border:`2.5px solid ${selectedTile===i?"#f9a825":"#222"}`, borderRadius:10, padding:"10px 6px", fontSize:12, fontWeight:800, color:"#333", textAlign:"center", cursor:"pointer", boxShadow:"3px 3px 0 #222", lineHeight:1.3 }}>{l}</div>
            ))}
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={nextTiles} style={{ ...btn, opacity:selectedTile===-1?0.4:1, pointerEvents:selectedTile===-1?"none":"auto" }}>Suivant →</button>
          </div>
        </div>
      )}
      {card === "radio" && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/bio.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Aliments bio</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>À quelle fréquence consommez-vous des aliments issus de l'agriculture biologique ?</p>
          <div style={{ display:"flex", flexWrap:"wrap", gap:12, justifyContent:"center", margin:"20px 0" }}>
            {BIO_LABELS.map((l,i)=>(
              <div key={i} onClick={()=>setSelectedRadio(i)} style={{ display:"flex", alignItems:"center", gap:10, background:selectedRadio===i?"#4caf50":"white", border:"2.5px solid #222", borderRadius:99, padding:"10px 20px", fontSize:14, fontWeight:800, color:selectedRadio===i?"white":"#555", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>
                <div style={{ width:18, height:18, borderRadius:"50%", border:"2.5px solid", borderColor:selectedRadio===i?"white":"#ccc", background:"white", display:"flex", alignItems:"center", justifyContent:"center" }}>
                  {selectedRadio===i && <div style={{ width:8, height:8, borderRadius:"50%", background:"#4caf50" }} />}
                </div>
                {l}
              </div>
            ))}
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={nextRadio} style={{ ...btn, opacity:selectedRadio===-1?0.4:1, pointerEvents:selectedRadio===-1?"none":"auto" }}>Suivant →</button>
          </div>
        </div>
      )}
      {card === "accord" && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <div style={{ textAlign:"center", marginBottom:8 }}><img src="/viande.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900, textAlign:"center" }}>Consommation de viande</h2>
          <p style={{ color:"#666", marginBottom:12, fontSize:"0.85em", textAlign:"center" }}>Au cours des dernières années, avez-vous diminué votre consommation de viandes ?</p>
          <div style={{ display:"flex", flexDirection:"column", gap:8, margin:"12px 0" }}>
            <div onClick={()=>setSelectedAccord("oui")} style={{ display:"flex", alignItems:"center", gap:12, background:selectedAccord==="oui"?"#4caf50":"white", border:"3px solid #222", borderRadius:12, padding:"14px 18px", fontSize:15, fontWeight:800, color:selectedAccord==="oui"?"white":"#333", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>
              <span style={{ fontSize:20 }}>✅</span> Oui
            </div>
            <div style={{ border:"3px solid #222", borderRadius:12, overflow:"hidden" }}>
              <div style={{ background:"#e53935", padding:"12px 18px", fontSize:14, fontWeight:900, color:"white", display:"flex", alignItems:"center", gap:8 }}>
                <span style={{ fontSize:18 }}>❌</span> Non — Pourquoi ?
              </div>
              {VIANDE_OPTIONS.map((opt,i)=>(
                <div key={i} onClick={()=>setSelectedAccord(i)} style={{ background:selectedAccord===i?"#ffcc00":"white", borderBottom:"1px solid #ddd", padding:"11px 18px 11px 28px", fontSize:13, fontWeight:700, color:"#333", cursor:"pointer" }}>
                  <span style={{ display:"inline-block", width:10, height:10, borderRadius:"50%", border:"2px solid #aaa", marginRight:10, background:selectedAccord===i?"#c4622d":"transparent", borderColor:selectedAccord===i?"#c4622d":"#aaa", verticalAlign:"middle" }} />
                  {opt.label}
                </div>
              ))}
            </div>
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={nextAccord} style={{ ...btn, opacity:selectedAccord===null?0.4:1, pointerEvents:selectedAccord===null?"none":"auto" }}>Suivant →</button>
          </div>
        </div>
      )}
      {card === "check" && (
        <div style={{ ...qCard, position:"relative", zIndex:1, textAlign:"left" }}>
          <div style={{ textAlign:"center", marginBottom:8 }}><img src="/viande.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900, textAlign:"center" }}>Raisons de ce choix</h2>
          <p style={{ color:"#666", marginBottom:12, fontSize:"0.85em", textAlign:"center" }}>Veuillez préciser la ou les raisons :<br />(Plusieurs réponses possibles)</p>
          <div style={{ display:"flex", flexDirection:"column", gap:8, margin:"16px 0" }}>
            {RAISONS_LABELS.map((label,i)=>{
              const checked = checkedRaisons.has(i);
              return (
                <div key={i} onClick={()=>{ const s=new Set(checkedRaisons); checked?s.delete(i):s.add(i); setCheckedRaisons(s); }} style={{ display:"flex", alignItems:"flex-start", gap:12, background:checked?"#e8f5e9":"white", border:`2.5px solid ${checked?"#4caf50":"#222"}`, borderRadius:10, padding:"11px 14px", fontSize:13, fontWeight:700, color:"#333", cursor:"pointer", boxShadow:checked?"3px 3px 0 #388e3c":"3px 3px 0 #222", lineHeight:1.4 }}>
                  <div style={{ width:20, height:20, borderRadius:5, border:"2.5px solid", borderColor:checked?"#388e3c":"#ccc", background:checked?"#4caf50":"white", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:13, color:"white", marginTop:1 }}>{checked?"✓":""}</div>
                  {label}
                </div>
              );
            })}
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={nextCheck} style={{ ...btn, opacity:checkedRaisons.size===0?0.4:1, pointerEvents:checkedRaisons.size===0?"none":"auto" }}>Terminer →</button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══ QCM 2 ══ */
const VSLIDER_LABELS = ['Non, je mange de tout','Je mange sans porc','Je mange sans viande'];

function Qcm2Screen({ onBack }) {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState({});
  const [persons, setPersons] = useState(2);
  const [vslider, setVslider] = useState(0);
  const [compo, setCompo] = useState(null);
  const [cuisine, setCuisine] = useState(null);
  const [repas, setRepas] = useState(null);
  const [done, setDone] = useState(false);

  const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:600, width:"100%", textAlign:"center", border:"3px solid #222", boxShadow:"5px 5px 0 #222" };
  const bubbleStyle = (selected) => ({ display:"flex", alignItems:"center", gap:14, border:`2.5px solid ${selected?"#388e3c":"#74b87a"}`, borderRadius:99, padding:"12px 20px", fontSize:14, fontWeight:800, color:selected?"white":"#333", cursor:"pointer", background:selected?"#74b87a":"white", boxShadow:"3px 3px 0 #222", marginBottom:10 });

  const next = (s, a) => { playSound("good"); setAnswers(prev=>({...prev,...a})); setStep(s+1); };

  if (done) {
    saveGame({ type:"qcm2", data: { answers } });
    return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", gap:14, overflowY:"auto", padding:"30px 16px", fontFamily:"Arial, sans-serif" }}>
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
        <div style={{ position:"relative", zIndex:1, textAlign:"center" }}>
          <div style={{ fontSize:56 }}>🍽️</div>
          <div style={{ fontSize:"1.8em", fontWeight:"bold", marginTop:8, color:"white" }}>Profil créé !</div>
          <div style={{ color:"rgba(255,255,255,0.65)", marginTop:4, fontSize:"0.92em" }}>Récapitulatif de vos préférences</div>
        </div>
        <div style={{ position:"relative", zIndex:1, background:"white", color:"#333", borderRadius:20, padding:"18px 20px", maxWidth:540, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222" }}>
          <h2 style={{ fontSize:"1.3em", color:"#2e7d32", marginBottom:12, textAlign:"center" }}>Ma Fabrique à Menus</h2>
          {Object.entries(answers).map(([k,v])=>(
            <div key={k} style={{ display:"flex", alignItems:"flex-start", gap:10, padding:"8px 10px", borderRadius:10, marginBottom:6, fontSize:"0.83em", background:"#e8f5e9" }}>
              <span>✅</span>
              <div><strong style={{ display:"block", color:"#222" }}>{k}</strong>{v}</div>
            </div>
          ))}
          <p style={{ marginTop:12, color:"#2e7d32", fontStyle:"italic", fontSize:"0.85em" }}>💡 Le saviez-vous ? Tous les repas de la semaine comptent pour adopter une alimentation équilibrée.</p>
        </div>
        <div style={{ position:"relative", zIndex:1, display:"flex", gap:12, flexWrap:"wrap", justifyContent:"center" }}>
          <button onClick={()=>{setStep(1);setDone(false);setPersons(2);setVslider(0);setCompo(null);setCuisine(null);setRepas(null);setAnswers({});}} style={btn}>Recommencer 🔄</button>
          <button onClick={onBack} style={{ ...btn, background:"white" }}>← Retour au menu</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/i.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"80px 16px 40px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#74b87a", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white", textShadow:"1px 1px 0 #222" }}>Question {step} / 5</div>
        <div style={{ fontSize:14, fontWeight:900, color:"white" }}>🍽️ Fabrique à Menus</div>
      </div>
      {step === 1 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/assiette.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Nombre de personnes à table</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>Pour combien de personnes souhaitez-vous préparer vos repas ?</p>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"center", gap:28, margin:"20px 0" }}>
            <div onClick={()=>setPersons(p=>Math.max(1,p-1))} style={{ width:56, height:56, borderRadius:"50%", border:"3px solid #222", background:"#9ACD32", fontSize:30, fontWeight:900, color:"white", display:"flex", alignItems:"center", justifyContent:"center", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>−</div>
            <div style={{ textAlign:"center" }}>
              <div style={{ fontSize:"3em", fontWeight:900, color:"#2d6e33" }}>{persons}</div>
              <div style={{ fontSize:13, color:"#888" }}>{persons===1?"personne":"personnes"}</div>
            </div>
            <div onClick={()=>setPersons(p=>Math.min(16,p+1))} style={{ width:56, height:56, borderRadius:"50%", border:"3px solid #222", background:"#9ACD32", fontSize:30, fontWeight:900, color:"white", display:"flex", alignItems:"center", justifyContent:"center", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>+</div>
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={()=>next(1,{"👥 Nombre de personnes":`${persons} ${persons===1?"personne":"personnes"}`})} style={btn}>Suivant →</button>
          </div>
        </div>
      )}
      {step === 2 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/aliment.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Pratiques alimentaires</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>Évitez-vous certains aliments ?</p>
          <div style={{ display:"flex", justifyContent:"center", alignItems:"center", gap:36, margin:"16px 0" }}>
            <div style={{ display:"flex", flexDirection:"column", justifyContent:"space-between", height:150, textAlign:"right" }}>
              {[2,1,0].map(i=><span key={i} style={{ fontSize:13, fontWeight:vslider===i?900:700, color:vslider===i?"#2d6e33":"#bbb" }}>{VSLIDER_LABELS[i]}</span>)}
            </div>
            <input type="range" min={0} max={2} value={vslider} onChange={e=>setVslider(+e.target.value)} style={{ writingMode:"vertical-lr", direction:"rtl", width:34, height:150, accentColor:"#74b87a" }} />
          </div>
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={()=>next(2,{"🥗 Pratiques alimentaires":VSLIDER_LABELS[vslider]})} style={btn}>Suivant →</button>
          </div>
        </div>
      )}
      {step === 3 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/repas.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Composition de votre repas</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>Comment souhaitez-vous composer vos repas ?</p>
          {["Entrée + Plat","Entrée + Plat + Dessert","Plat + Dessert"].map(o=>(
            <div key={o} onClick={()=>setCompo(o)} style={bubbleStyle(compo===o)}>
              <div style={{ width:18, height:18, borderRadius:"50%", border:"2.5px solid", borderColor:compo===o?"white":"#74b87a", background:"white", display:"flex", alignItems:"center", justifyContent:"center" }}>
                {compo===o&&<div style={{ width:8, height:8, borderRadius:"50%", background:"#74b87a" }} />}
              </div>
              {o}
            </div>
          ))}
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={()=>compo&&next(3,{"🍽️ Composition du repas":compo})} style={{ ...btn, opacity:!compo?0.4:1, pointerEvents:!compo?"none":"auto" }}>Suivant →</button>
          </div>
        </div>
      )}
      {step === 4 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/marmitte.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>En cuisine</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>Avez-vous le temps de cuisiner ?</p>
          {["Je n'ai pas le temps","J'aime y passer du temps"].map(o=>(
            <div key={o} onClick={()=>setCuisine(o)} style={bubbleStyle(cuisine===o)}>
              <div style={{ width:18, height:18, borderRadius:"50%", border:"2.5px solid", borderColor:cuisine===o?"white":"#74b87a", background:"white", display:"flex", alignItems:"center", justifyContent:"center" }}>
                {cuisine===o&&<div style={{ width:8, height:8, borderRadius:"50%", background:"#74b87a" }} />}
              </div>
              {o}
            </div>
          ))}
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={()=>cuisine&&next(4,{"👨‍🍳 En cuisine":cuisine})} style={{ ...btn, opacity:!cuisine?0.4:1, pointerEvents:!cuisine?"none":"auto" }}>Suivant →</button>
          </div>
        </div>
      )}
      {step === 5 && (
        <div style={{ ...qCard, position:"relative", zIndex:1 }}>
          <div style={{ marginBottom:8 }}><img src="/oeuf.png" alt="" style={{ width:130, height:150, objectFit:"contain" }} /></div>
          <h2 style={{ fontSize:"1.4em", color:"#FA8072", marginBottom:8, fontWeight:900 }}>Nombre de repas</h2>
          <p style={{ color:"#666", marginBottom:16, fontSize:"0.85em" }}>En semaine, vous préparez à manger :</p>
          {["Midi uniquement","Midi et soir","Soir uniquement"].map(o=>(
            <div key={o} onClick={()=>setRepas(o)} style={bubbleStyle(repas===o)}>
              <div style={{ width:18, height:18, borderRadius:"50%", border:"2.5px solid", borderColor:repas===o?"white":"#74b87a", background:"white", display:"flex", alignItems:"center", justifyContent:"center" }}>
                {repas===o&&<div style={{ width:8, height:8, borderRadius:"50%", background:"#74b87a" }} />}
              </div>
              {o}
            </div>
          ))}
          <div style={{ display:"flex", justifyContent:"center" }}>
            <button onClick={()=>{ if(!repas) return; setAnswers(prev=>({...prev,"🕐 Nombre de repas":repas})); setDone(true); saveGame({ type:"qcm2", data: { answers: {...answers, "🕐 Nombre de repas": repas} } }); }} style={{ ...btn, opacity:!repas?0.4:1, pointerEvents:!repas?"none":"auto" }}>Terminer →</button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══ APP ══ */
export default function App() {
  const [phase, setPhase] = useState("splash");
  const [playerName, setPlayerName] = useState("");
  const [avatarChoice, setAvatarChoice] = useState("fille");
  const [sceneIdx, setSceneIdx] = useState(0);
  const [currentNode, setCurrentNode] = useState(0);
  const [completedNodes, setCompletedNodes] = useState([]);
  const [nodeScenes, setNodeScenes] = useState([]);

  const handleSelectNode = (nodeId) => {
    setCurrentNode(nodeId);
    setNodeScenes(SCENES_BY_NODE[nodeId] || []);
    setSceneIdx(0);
    setPhase("scene");
  };

  const handleSceneNext = () => {
    if (sceneIdx < nodeScenes.length - 1) {
      setSceneIdx(i => i + 1);
    } else {
      setCompletedNodes(prev => prev.includes(currentNode) ? prev : [...prev, currentNode]);
      if (currentNode === 3) { setPhase("select"); }
      else { setPhase("map"); }
    }
  };

  const screen = (() => {
    if (phase === "splash")  return <SplashScreen onStart={() => { playSound("click"); setPhase("intro"); }} />;
    if (phase === "intro")   return <IntroScreen onStart={() => { playSound("click"); setPhase("name"); }} />;
    if (phase === "name")    return <NameScreen onConfirm={name => { playSound("good"); setPlayerName(name); setCompletedNodes([]); setPhase("avatar"); }} />;
    if (phase === "avatar")  return <AvatarScreen playerName={playerName} onChoose={choice => { playSound("good"); setAvatarChoice(choice); setPhase("map"); }} />;
    if (phase === "scene")   return (
      <SceneScreen sceneIndex={sceneIdx} scenes={nodeScenes} playerName={playerName}
        avatarSrc={avatarChoice === "fille" ? "/fille.png" : "/garcon.png"}
        onNext={() => { playSound("next"); handleSceneNext(); }}
        onSkipAll={() => { playSound("click"); setCompletedNodes(prev => prev.includes(currentNode) ? prev : [...prev, currentNode]); setPhase("map"); }} />
    );
    if (phase === "map")     return <MapScreen onSelectNode={handleSelectNode} completedNodes={completedNodes} activeNode={currentNode} />;
    if (phase === "minijeu") return <MinijeuScreen onBack={() => setPhase("select")} />;
    if (phase === "qcm1")    return <Qcm1Screen onBack={() => { playSound("click"); setPhase("select"); }} />;
    if (phase === "qcm2")    return <Qcm2Screen onBack={() => { playSound("click"); setPhase("select"); }} />;
    return <QcmSelectScreen playerName={playerName}
      onStartQcm1={() => { playSound("click"); setPhase("qcm1"); }}
      onStartQcm2={() => { playSound("click"); setPhase("qcm2"); }}
      onStartMinijeu={() => { playSound("click"); setPhase("minijeu"); }} />;
  })();

  return (
    <>
      <GlobalStyles />
      {screen}
    </>
  );
}



