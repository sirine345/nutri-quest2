import React, { useState, useEffect, useRef } from "react";

/* ══ STYLES GLOBAUX ══ */
const CSS_CONTENT = `
  :root {
    --primary: #1A3A5C;
    --accent: #00BFA5;
    --accent-light: #E0F7F5;
    --warn: #FF6B35;
    --warn-light: #FFF0EB;
    --success: #00C853;
    --success-light: #E8FFF0;
    --purple: #7C3AED;
    --purple-light: #F3EEFF;
    --bg: #F8FAFC;
    --card: #FFFFFF;
    --border: #E8EDF2;
    --text: #1A1A1A;
    --muted: #6B7280;
    --shadow: 0 2px 16px rgba(26,58,92,0.08);
    --shadow-hover: 0 8px 32px rgba(26,58,92,0.15);
    --radius: 20px;
    --radius-sm: 12px;
  }

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
  @keyframes mapIn { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
  @keyframes nodePop { 0%{transform:scale(0)} 70%{transform:scale(1.15)} 100%{transform:scale(1)} }
  @keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.1)} }
  @keyframes pathGrow { from{stroke-dashoffset:300} to{stroke-dashoffset:0} }
  .map-in { animation: mapIn 0.5s ease both; }
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
`;
if (typeof document !== 'undefined') {
  const styleEl = document.createElement('style');
  styleEl.id = 'nutri-quest-styles';
  styleEl.textContent = CSS_CONTENT;
  if (!document.getElementById('nutri-quest-styles')) {
    document.head.appendChild(styleEl);
  }
}
const GlobalStyles = () => null;

/* ══ saveGame ══ */
const saveGame = async (data) => {
  try {
    const res = await fetch("https://nutri-quest2.onrender.com/save", {
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
function speak(text, role, avatarGender) {
  try {
    const synth = window.speechSynthesis;
    synth.cancel();
    if (!text) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "fr-FR";
    utter.volume = 0.9;
    const voices = synth.getVoices();
    const frVoices = voices.filter(v => v.lang.startsWith("fr"));
    if (role === "max") {
      utter.rate = 0.85;
      utter.pitch = 0.75;
      const v = frVoices.find(v => /male|man|homme|thomas|nicolas/i.test(v.name));
      if (v) utter.voice = v; else if (frVoices.length > 0) utter.voice = frVoices[frVoices.length - 1];
    } else if (role === "player") {
      utter.rate = 0.88;
      if (avatarGender === "garcon") {
        utter.pitch = 0.9;
        const v = frVoices.find(v => /male|man|homme|thomas|nicolas/i.test(v.name));
        if (v) utter.voice = v; else if (frVoices.length > 0) utter.voice = frVoices[frVoices.length - 1];
      } else {
        utter.pitch = 1.15;
        const v = frVoices.find(v => /female|woman|femme|amelie|marie/i.test(v.name));
        if (v) utter.voice = v; else if (frVoices.length > 0) utter.voice = frVoices[0];
      }
    } else {
      utter.rate = 0.88;
      utter.pitch = 1.0;
      if (frVoices.length > 0) utter.voice = frVoices[0];
    }
    synth.speak(utter);
  } catch(e) {}
}
function stopSpeech() {
  try { window.speechSynthesis.cancel(); } catch(e) {}
}

/* ══ SCÈNES ══ */
const SCENES_BY_NODE = {
  0: [
    { bg: "exterior", speaker: "narrator", text: "Une ville animée. Fast-foods et marchés se côtoient. L'alimentation de toute une génération est en jeu..." },
    { bg: "exterior", speaker: "narrator", text: "Un message sur ton téléphone : Rejoins-moi. Ta cuisine, 14h. — Max" },
  ],
  1: [
    { bg: "kitchen", speaker: "max", text: "Ah, tu es là ! Je m'appelle Max, coach nutrition. J'ai besoin de toi." },
    { bg: "kitchen", speaker: "max", text: "Cette cuisine cache des secrets. Chaque aliment a un impact sur ton corps." },
    { bg: "kitchen", speaker: "player", text: "..." },
    { bg: "kitchen", speaker: "max", text: "Ce n'est pas un cours. Ici, on joue. Et chaque choix compte." },
  ],
  2: [
    { bg: "market", speaker: "narrator", text: "Max t'emmène au marché. Légumes frais, fruits de saison, poissons scintillants." },
    { bg: "market", speaker: "max", text: "Légumineuses, céréales complètes, fruits à coque… C'est ton arsenal !" },
    { bg: "market", speaker: "max", text: "Attention aux ennemis : ultra-transformés, sucres cachés, charcuterie en excès." },
    { bg: "market", speaker: "player", text: "Comment je sais quoi choisir ?" },
    { bg: "market", speaker: "max", text: "C'est pour ça que je suis là ! On va construire ton profil nutritionnel." },
  ],
  3: [
    { bg: "lab", speaker: "narrator", text: "Le laboratoire de Max. Graphiques, données nutritionnelles, recettes partout." },
    { bg: "lab", speaker: "max", text: "Deux missions : évaluer tes habitudes alimentaires, puis construire ta Fabrique à Menus." },
    { bg: "lab", speaker: "max", text: "Prêt(e) {name} ? Ton alimentation n'attend plus !" },
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
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", backgroundPosition:"center", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.15)" }} />
      <div style={{ position:"relative", zIndex:1, display:"flex", flexDirection:"column", height:"100vh", padding:"20px 40px 16px", boxSizing:"border-box" }}>
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, marginBottom:16, flexShrink:0 }}>
          <img src="/e.png" style={{ width:80, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.3))", flexShrink:0 }} alt="Max" />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"12px 18px", boxShadow:"5px 5px 0 rgba(0,0,0,0.2)", fontSize:15, color:"#333", lineHeight:1.6, maxWidth:400 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:3 }}>Max — Coach Nutrition</div>
            Bonjour <strong>{playerName}</strong> ! Choisis ton personnage pour commencer l'aventure !
          </div>
        </div>
        <div style={{ textAlign:"center", marginBottom:16, flexShrink:0 }}>
          <h1 style={{ fontSize:56, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.2)", margin:0, lineHeight:1.1 }}>
            Choisis ton <span style={{ color:"#ffdd44" }}>personnage</span>
          </h1>
        </div>
        <div style={{ flex:1, display:"flex", gap:32, minHeight:0 }}>
          {avatars.map(av => (
            <div key={av.id}
              onClick={() => handleChoose(av.id)}
              onMouseEnter={() => setHovered(av.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                flex:1, background: selected===av.id ? av.color+"33" : hovered===av.id ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.15)",
                border: `4px solid ${selected===av.id ? av.color : hovered===av.id ? "white" : "rgba(255,255,255,0.4)"}`,
                borderRadius:24, cursor:"pointer", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"flex-end",
                padding:"16px 16px 24px", transition:"all 0.25s cubic-bezier(0.34,1.56,0.64,1)",
                transform: selected===av.id ? "scale(1.02)" : hovered===av.id ? "translateY(-6px) scale(1.01)" : "scale(1)",
                boxShadow: selected===av.id ? `0 20px 60px ${av.color}66` : hovered===av.id ? "0 16px 50px rgba(0,0,0,0.25)" : "0 4px 20px rgba(0,0,0,0.15)",
                overflow:"hidden", position:"relative", minHeight:0,
              }}>
              {selected===av.id && (
                <div style={{ position:"absolute", top:16, right:16, width:34, height:34, borderRadius:"50%", background:av.color, display:"flex", alignItems:"center", justifyContent:"center", fontSize:16, fontWeight:900, color:"white", boxShadow:"0 4px 12px rgba(0,0,0,0.3)" }}></div>
              )}
              <img src={av.src} alt={av.label} style={{ width:"auto", height:"80%", maxWidth:"70%", objectFit:"contain", filter:"drop-shadow(4px 8px 12px rgba(0,0,0,0.3))", marginBottom:12, flexShrink:1 }} />
              <div style={{ fontSize:20, fontWeight:900, letterSpacing:3, textTransform:"uppercase", flexShrink:0, color: selected===av.id ? av.color : "white", textShadow: selected===av.id ? `0 0 20px ${av.color}` : "2px 2px 0 rgba(0,0,0,0.3)" }}>
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
           Commencer
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
        <span style={{ fontSize:16 }}></span>
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

/* ══ SAISIE NOM / CONNEXION ══ */
function NameScreen({ onConfirm, onGuest }) {
  const [mode, setMode] = useState(null); // null | "login" | "register"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regPassword2, setRegPassword2] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const inputStyle = { border:"none", borderBottom:"2px solid #ccc", background:"transparent", padding:"10px 4px", fontSize:18, fontFamily:"inherit", color:"#1a1a1a", width:"100%", outline:"none", transition:"border-color 0.2s" };
  const labelStyle = { fontSize:12, fontWeight:700, color:"#222", letterSpacing:1, textTransform:"uppercase", marginBottom:4, display:"block", textAlign:"left" };

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) return;
    setLoading(true); setError("");
    try {
      const res = await fetch("https://nutri-quest2.onrender.com/login", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (data.status === "ok") {
        onConfirm(data.prenom || email, { email, ...data });
      } else {
        setError(data.message || "Email ou mot de passe incorrect");
      }
    } catch(e) { setError("Impossible de contacter le serveur"); }
    setLoading(false);
  };

  const handleRegister = async () => {
    if (!regEmail.trim() || !regPassword.trim()) return;
    if (regPassword !== regPassword2) { setError("Les mots de passe ne correspondent pas"); return; }
    setLoading(true); setError("");
    try {
      const res = await fetch("https://nutri-quest2.onrender.com/register", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ email: regEmail, password: regPassword })
      });
      const data = await res.json();
      if (data.status === "ok") {
        setMode("login"); setEmail(regEmail); setPassword(""); setError("Compte créé ! Connecte-toi.");
      } else {
        setError(data.message || "Erreur lors de la création");
      }
    } catch(e) { setError("Impossible de contacter le serveur"); }
    setLoading(false);
  };

  return (
    <div style={{ position:"fixed", inset:0, background:"#f4dcbf", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"20px" }}>
      <button onClick={() => window.open("https://nutri-quest2.onrender.com/dashboard?pwd=Sirine1234", "_blank")}
        style={{ position:"fixed", top:16, right:16, background:"#333", color:"white", border:"none", borderRadius:10, padding:"8px 18px", fontSize:13, fontWeight:800, cursor:"pointer", zIndex:100 }}>
         Gestionnaire
      </button>
      {mode === null && (
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:20, maxWidth:480, width:"100%", textAlign:"center" }}>
          <div style={{ display:"inline-flex", alignItems:"center", gap:10, background:"#EAF3DE", borderRadius:30, padding:"8px 20px" }}>
            <span style={{ fontSize:16 }}></span>
          </div>
          <h1 style={{ fontSize:52, fontWeight:900, color:"#1a1a1a", lineHeight:1.12, margin:0 }}>
            Bienvenue sur<br/><span style={{ color:"#FA8072" }}>Nutri-Quest !</span>
          </h1>
          <p style={{ fontSize:15, color:"#555", margin:0 }}>Comment souhaitez-vous accéder au jeu ?</p>
          <div style={{ display:"flex", flexDirection:"column", gap:12, width:"100%" }}>
            <button onClick={() => onGuest()}
              style={{ background:"white", border:"3px solid #ddd", borderRadius:16, padding:"16px 24px", fontSize:15, fontWeight:800, color:"#555", cursor:"pointer", textAlign:"left", transition:"all 0.2s" }}
              onMouseEnter={e=>e.currentTarget.style.borderColor="#FA8072"}
              onMouseLeave={e=>e.currentTarget.style.borderColor="#ddd"}>
               Accès simple
              <div style={{ fontSize:12, fontWeight:500, color:"#999", marginTop:3 }}>Jouer sans compte, données non sauvegardées</div>
            </button>
            <button onClick={() => { setMode("login"); setError(""); }}
              style={{ background:"#9ACD32", border:"3px solid #9ACD32", borderRadius:16, padding:"16px 24px", fontSize:15, fontWeight:800, color:"white", cursor:"pointer", textAlign:"left", transition:"all 0.2s" }}>
               Se connecter
              <div style={{ fontSize:12, fontWeight:500, color:"rgba(255,255,255,0.8)", marginTop:3 }}>Retrouve tes données précédentes</div>
            </button>
            <button onClick={() => { setMode("register"); setError(""); }}
              style={{ background:"#FA8072", border:"3px solid #FA8072", borderRadius:16, padding:"16px 24px", fontSize:15, fontWeight:800, color:"white", cursor:"pointer", textAlign:"left", transition:"all 0.2s" }}>
              Créer un compte
              <div style={{ fontSize:12, fontWeight:500, color:"rgba(255,255,255,0.8)", marginTop:3 }}>Sauvegarde ta progression</div>
            </button>
          </div>
        </div>
      )}
      {mode === "login" && (
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:18, maxWidth:420, width:"100%" }}>
          <button onClick={() => { setMode(null); setError(""); }} style={{ alignSelf:"flex-start", background:"none", border:"none", fontSize:14, color:"#888", cursor:"pointer", fontWeight:700 }}>← Retour</button>
          <h2 style={{ fontSize:36, fontWeight:900, color:"#1a1a1a", margin:0 }}>Connexion</h2>
          <div style={{ width:"100%" }}>
            <label style={labelStyle}>Email</label>
            <input type="email" placeholder="ton@email.com" value={email} onChange={e=>setEmail(e.target.value)} style={inputStyle} onFocus={e=>e.target.style.borderBottomColor="#FA8072"} onBlur={e=>e.target.style.borderBottomColor="#ccc"} />
          </div>
          <div style={{ width:"100%" }}>
            <label style={labelStyle}>Mot de passe</label>
            <input type="password" placeholder="••••••••" value={password} onChange={e=>setPassword(e.target.value)} style={inputStyle} onFocus={e=>e.target.style.borderBottomColor="#FA8072"} onBlur={e=>e.target.style.borderBottomColor="#ccc"} onKeyDown={e=>e.key==="Enter"&&handleLogin()} />
          </div>
          {error && <div style={{ color: error.includes("créé") ? "#2e7d32" : "#e53935", fontSize:13, fontWeight:700 }}>{error}</div>}
          <button onClick={handleLogin} disabled={loading || !email.trim() || !password.trim()}
            style={{ background:"#9ACD32", border:"none", borderRadius:14, padding:"14px 48px", fontSize:18, fontWeight:800, color:"white", cursor:"pointer", width:"100%", opacity:loading?0.6:1 }}>
            {loading ? "Connexion..." : "Se connecter →"}
          </button>
          <p style={{ fontSize:13, color:"#888", margin:0 }}>Pas de compte ? <span onClick={()=>{setMode("register");setError("");}} style={{ color:"#FA8072", cursor:"pointer", fontWeight:700 }}>Créer un compte</span></p>
        </div>
      )}
      {mode === "register" && (
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:18, maxWidth:420, width:"100%" }}>
          <button onClick={() => { setMode(null); setError(""); }} style={{ alignSelf:"flex-start", background:"none", border:"none", fontSize:14, color:"#888", cursor:"pointer", fontWeight:700 }}>← Retour</button>
          <h2 style={{ fontSize:36, fontWeight:900, color:"#1a1a1a", margin:0 }}>Créer un compte</h2>
          <div style={{ width:"100%" }}>
            <label style={labelStyle}>Email</label>
            <input type="email" placeholder="ton@email.com" value={regEmail} onChange={e=>setRegEmail(e.target.value)} style={inputStyle} onFocus={e=>e.target.style.borderBottomColor="#FA8072"} onBlur={e=>e.target.style.borderBottomColor="#ccc"} />
          </div>
          <div style={{ width:"100%" }}>
            <label style={labelStyle}>Mot de passe</label>
            <input type="password" placeholder="••••••••" value={regPassword} onChange={e=>setRegPassword(e.target.value)} style={inputStyle} onFocus={e=>e.target.style.borderBottomColor="#FA8072"} onBlur={e=>e.target.style.borderBottomColor="#ccc"} />
          </div>
          <div style={{ width:"100%" }}>
            <label style={labelStyle}>Confirmer le mot de passe</label>
            <input type="password" placeholder="••••••••" value={regPassword2} onChange={e=>setRegPassword2(e.target.value)} style={inputStyle} onFocus={e=>e.target.style.borderBottomColor="#FA8072"} onBlur={e=>e.target.style.borderBottomColor="#ccc"} onKeyDown={e=>e.key==="Enter"&&handleRegister()} />
          </div>
          {error && <div style={{ color:"#e53935", fontSize:13, fontWeight:700 }}>{error}</div>}
          <button onClick={handleRegister} disabled={loading || !regEmail.trim() || !regPassword.trim()}
            style={{ background:"#FA8072", border:"none", borderRadius:14, padding:"14px 48px", fontSize:18, fontWeight:800, color:"white", cursor:"pointer", width:"100%", opacity:loading?0.6:1 }}>
            {loading ? "Création..." : "Créer mon compte →"}
          </button>
          <p style={{ fontSize:13, color:"#888", margin:0 }}>Déjà un compte ? <span onClick={()=>{setMode("login");setError("");}} style={{ color:"#9ACD32", cursor:"pointer", fontWeight:700 }}>Se connecter</span></p>
        </div>
      )}
    </div>
  );
}

/* ══ MENU HAMBURGER PROFIL ══ */
function HamburgerMenu({ playerName, playerInfos, onSaveProfile, isGuest }) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState(playerName || "");
  const [sexe, setSexe] = useState(playerInfos?.sexe || "");
  const [age, setAge] = useState(playerInfos?.age || "");
  const [taille, setTaille] = useState(playerInfos?.taille || "");
  const [poids, setPoids] = useState(playerInfos?.poids || "");
  const [restriction, setRestriction] = useState(playerInfos?.restriction || []);
  const [saved, setSaved] = useState(false);

  const inputStyle = { border:"none", borderBottom:"2px solid #ddd", background:"transparent", padding:"8px 4px", fontSize:16, fontFamily:"inherit", color:"#1a1a1a", width:"100%", outline:"none" };
  const labelStyle = { fontSize:11, fontWeight:700, color:"#888", letterSpacing:1, textTransform:"uppercase", marginBottom:2, display:"block" };

  const handleSave = async () => {
    const infos = { sexe, age, taille, poids, restriction, email: playerInfos?.email };
    if (playerInfos?.email) {
      try {
        await fetch("https://nutri-quest2.onrender.com/update_profile", {
          method:"POST", headers:{"Content-Type":"application/json"},
          body: JSON.stringify({ email: playerInfos.email, prenom: name, sexe, age, taille, poids, restriction })
        });
      } catch(e) {}
    }
    onSaveProfile(name, infos);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <>
      <div style={{ position:"fixed", top:60, right:16, zIndex:200, display:"flex", alignItems:"center", gap:8 }}>
        {!open && <div style={{ background:"#FA8072", color:"white", borderRadius:20, padding:"4px 12px", fontSize:12, fontWeight:800, whiteSpace:"nowrap", boxShadow:"2px 2px 0 #222" }}>Mon profil </div>}
        <button onClick={() => setOpen(o => !o)}
          style={{ background:"white", border:"2px solid #222", borderRadius:10, width:44, height:44, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", gap:5, cursor:"pointer", boxShadow:"2px 2px 0 #222" }}>
          <div style={{ width:20, height:2, background:"#222", borderRadius:2 }} />
          <div style={{ width:20, height:2, background:"#222", borderRadius:2 }} />
          <div style={{ width:20, height:2, background:"#222", borderRadius:2 }} />
        </button>
      </div>
      {open && <div onClick={() => setOpen(false)} style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.4)", zIndex:198 }} />}
      <div style={{ position:"fixed", top:0, left:0, bottom:0, width:320, background:"white", zIndex:199, transform:open?"translateX(0)":"translateX(-100%)", transition:"transform 0.3s ease", boxShadow:"4px 0 20px rgba(0,0,0,0.2)", display:"flex", flexDirection:"column", overflowY:"auto" }}>
        <div style={{ background:"#FA8072", padding:"20px 20px 16px", color:"white" }}>
          <div style={{ fontSize:22, fontWeight:900 }}> Mon Profil</div>
          <div style={{ fontSize:13, opacity:0.8, marginTop:4 }}>{isGuest ? "Mode invité" : playerInfos?.email || ""}</div>
        </div>
        <div style={{ padding:"20px", display:"flex", flexDirection:"column", gap:16, flex:1 }}>
          {isGuest && (
            <div style={{ background:"#fff8e1", border:"2px solid #ffcc00", borderRadius:10, padding:"12px", fontSize:13, color:"#666" }}>
              ⚠️ En mode invité, tes données ne sont pas sauvegardées.
            </div>
          )}
          <div>
            <label style={labelStyle}>Prénom</label>
            <input type="text" value={name} onChange={e=>setName(e.target.value)} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>Sexe</label>
            <div style={{ display:"flex", gap:8, marginTop:4 }}>
              {["Fille","Garçon","Autre"].map(s => (
                <div key={s} onClick={() => setSexe(s)} style={{ flex:1, padding:"8px", borderRadius:8, border:`2px solid ${sexe===s?"#FA8072":"#ddd"}`, background:sexe===s?"#FFF0EE":"white", cursor:"pointer", fontWeight:700, fontSize:12, color:sexe===s?"#FA8072":"#888", textAlign:"center" }}>{s}</div>
              ))}
            </div>
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr 1fr", gap:12 }}>
            <div>
              <label style={labelStyle}>Âge</label>
              <input type="number" value={age} onChange={e=>setAge(e.target.value)} style={inputStyle} placeholder="ans" />
            </div>
            <div>
              <label style={labelStyle}>Taille</label>
              <input type="number" value={taille} onChange={e=>setTaille(e.target.value)} style={inputStyle} placeholder="cm" />
            </div>
            <div>
              <label style={labelStyle}>Poids</label>
              <input type="number" value={poids} onChange={e=>setPoids(e.target.value)} style={inputStyle} placeholder="kg" />
            </div>
          </div>
          <div>
            <label style={labelStyle}>Restrictions alimentaires</label>
            <div style={{ display:"flex", flexWrap:"wrap", gap:6, marginTop:6 }}>
              {["Aucune","Végétarien","Végétalien","Sans gluten","Sans lactose","Allergie fruits à coque"].map(r => (
                <div key={r} onClick={() => { if(r==="Aucune"){setRestriction(["Aucune"]);return;} setRestriction(prev=>{const f=prev.filter(x=>x!=="Aucune");return f.includes(r)?f.filter(x=>x!==r):[...f,r];}); }}
                  style={{ padding:"5px 12px", borderRadius:20, border:`2px solid ${restriction.includes(r)?"#9ACD32":"#ddd"}`, background:restriction.includes(r)?"#F0F9E0":"white", cursor:"pointer", fontWeight:700, fontSize:11, color:restriction.includes(r)?"#639922":"#888" }}>
                  {r}
                </div>
              ))}
            </div>
          </div>
        </div>
        <div style={{ padding:"16px 20px", borderTop:"2px solid #eee" }}>
          <button onClick={handleSave}
            style={{ background:"#FA8072", border:"none", borderRadius:12, padding:"12px", fontSize:15, fontWeight:800, color:"white", cursor:"pointer", width:"100%" }}>
            {saved ? " Sauvegardé !" : "Sauvegarder"}
          </button>
        </div>
      </div>
    </>
  );
}

/* ══ SCÈNE ══ */
function SceneScreen({ sceneIndex, scenes, playerName, avatarSrc, avatarGender, onNext, onSkipAll }) {
  const sceneList = scenes || SCENES;
  const scene = sceneList[sceneIndex] || sceneList[0];
  const rawText = (scene.text || "").replace("{name}", playerName);
  const [fading, setFading] = useState(false);
  const [visible, setVisible] = useState(true);
  const [muted, setMuted] = useState(false);

  useEffect(() => {
    setVisible(false);
    const t = setTimeout(() => { setVisible(true); if (!muted) speak(rawText, scene.speaker, avatarGender); }, 80);
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
          <button onClick={e=>{ e.stopPropagation(); muted ? (setMuted(false), speak(rawText, scene.speaker, avatarGender)) : (setMuted(true), stopSpeech()); }} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid #222", borderRadius:8, color:"white", fontSize:14, fontWeight:800, padding:"4px 10px", cursor:"pointer" }}>
            {muted ? "" : ""}
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
            {isMax && (
              <div style={{ position:"absolute", bottom:"58%", right:"4%", width:320, zIndex:30, animation:"dialogueSlideUp 0.3s ease both" }}>
                <div style={{ position:"relative", backgroundImage:"url('/bulle2.png')", backgroundSize:"100% 100%", backgroundRepeat:"no-repeat", width:"100%", minHeight:140, marginLeft:"-400px", display:"flex", alignItems:"center", justifyContent:"center", padding:"28px 36px 44px", boxSizing:"border-box" }}>
                  <p style={{ margin:0, fontSize:15, color:"#222", lineHeight:1.65, textAlign:"center", fontWeight:600 }}>{rawText}</p>
                </div>
                <div style={{ textAlign:"right", marginTop:4 }}>
                  <span style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222" }}>{isLast?" Jouer !":"Suivant "}</span>
                </div>
              </div>
            )}
            {isPlayer && (
              <div style={{ position:"absolute", bottom:"58%", left:"4%", width:320, zIndex:30, marginLeft:"500px", animation:"dialogueSlideUp 0.3s ease both" }}>
                <div style={{ position:"relative", backgroundImage:"url('/bulle.png')", backgroundSize:"100% 100%", backgroundRepeat:"no-repeat", width:"100%", minHeight:140, display:"flex", alignItems:"center", justifyContent:"center", padding:"28px 36px 44px", boxSizing:"border-box" }}>
                  <p style={{ margin:0, fontSize:15, color:"#222", lineHeight:1.65, textAlign:"center", fontWeight:600 }}>{rawText}</p>
                </div>
                <div style={{ textAlign:"left", marginTop:4 }}>
                  <span style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:20, padding:"4px 14px", fontSize:12, fontWeight:900, color:"white", boxShadow:"2px 2px 0 #222" }}>{isLast?" Jouer !":"Suivant "}</span>
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
          <p style={{ color:"#c4622d", fontSize:16, lineHeight:1.7, margin:0, fontStyle:"italic", minHeight:54, fontWeight:700 }}>{rawText}</p>
          <div style={{ position:"absolute", right:20, bottom:16, color:"#9ACD32", fontSize:13, fontWeight:800, border:"2px solid #9ACD32", borderRadius:8, padding:"3px 12px", background:"white" }}>{isLast?" Jouer !":"Suivant "}</div>
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
    { id:0, icon:"", label:"Chez toi",   desc:"Le point de départ de l'aventure",         color:"#FA8072",  bg:"#FFF0EB" },
    { id:1, icon:"", label:"La Cuisine", desc:"Là où les habitudes alimentaires naissent", color:"#ffcc00",  bg:"#FFFBE6" },
    { id:2, icon:"", label:"Le Marché",  desc:"Légumes, fruits, protéines… ton arsenal",   color:"#74b87a",  bg:"#EAF5EB" },
    { id:3, icon:"", label:"Le Labo",    desc:"Analyse ton profil et lance les QCM",        color:"#9ACD32",  bg:"#F0F9E0" },
  ];
  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_jaune.png')", backgroundSize:"cover", backgroundPosition:"center", backgroundRepeat:"no-repeat", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.35)" }} />
      <div className="map-in" style={{ position:"relative", zIndex:1, textAlign:"center", marginBottom:32 }}>
        <div style={{ fontSize:52, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.2em", color:"#7FFFD4", marginBottom:8 }}>Carte de l'aventure</div>
        <h2 style={{ fontSize:88, fontWeight:900, color:"white", textShadow:"3px 3px 0 rgba(0,0,0,0.3)", margin:0, lineHeight:1.1 }}>
          Choisis ton prochain <span style={{ color:"#ffdd44" }}>lieu</span>
        </h2>
      </div>
      <div className="map-in" style={{ position:"relative", zIndex:1, display:"flex", gap:24, width:"90vw", maxWidth:1000, animationDelay:"0.1s" }}>
        {NODES.map((node, i) => {
          const done = completedNodes.includes(node.id);
          const isActive = activeNode === node.id;
          const locked = node.id > 0 && !completedNodes.includes(node.id - 1);
          const isHov = hovered === node.id;
          return (
            <div key={node.id} className="node-pop"
              onClick={() => !locked && onSelectNode(node.id)}
              onMouseEnter={() => setHovered(node.id)}
              onMouseLeave={() => setHovered(null)}
              style={{ flex:1, background: locked ? "rgba(255,255,255,0.08)" : done ? node.bg : isHov ? "rgba(255,255,255,0.95)" : "rgba(255,255,255,0.88)", border: `3px solid ${locked ? "rgba(255,255,255,0.2)" : done ? node.color : isActive ? node.color : isHov ? node.color : "rgba(255,255,255,0.5)"}`, borderRadius:20, padding:"28px 20px 24px", cursor: locked ? "not-allowed" : "pointer", opacity: locked ? 0.5 : 1, transform: isHov && !locked ? "translateY(-8px) scale(1.03)" : isActive ? "scale(1.02)" : "scale(1)", transition:"all 0.25s cubic-bezier(0.34,1.56,0.64,1)", boxShadow: done ? `0 8px 30px ${node.color}55` : isHov && !locked ? "0 16px 40px rgba(0,0,0,0.3)" : "0 4px 16px rgba(0,0,0,0.2)", display:"flex", flexDirection:"column", alignItems:"center", gap:12, textAlign:"center", animationDelay:`${i*0.1}s`, position:"relative" }}>
              {isActive && !done && (<div style={{ position:"absolute", top:-12, left:"50%", transform:"translateX(-50%)", background:node.color, border:"2px solid white", borderRadius:20, padding:"3px 14px", fontSize:10, fontWeight:900, color:"white", whiteSpace:"nowrap", boxShadow:"0 2px 8px rgba(0,0,0,0.2)" }}>ACTIF</div>)}
              {done && (<div style={{ position:"absolute", top:-12, right:14, background:"#ffcc00", border:"2px solid white", borderRadius:"50%", width:28, height:28, display:"flex", alignItems:"center", justifyContent:"center", fontSize:14, fontWeight:900, boxShadow:"0 2px 8px rgba(0,0,0,0.2)" }}></div>)}
              <div style={{ width:70, height:70, borderRadius:"50%", background: locked ? "#888" : done ? node.color : isHov ? node.color : node.bg, border: `3px solid ${locked ? "#666" : node.color}`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:32, boxShadow: !locked ? `0 4px 16px ${node.color}55` : "none", transition:"all 0.2s" }}>
                {locked ? "" : node.icon}
              </div>
              <div style={{ fontSize:16, fontWeight:900, color: locked ? "#aaa" : done ? node.color : "#222", letterSpacing:1 }}>{node.label}</div>
              <div style={{ fontSize:12, color: locked ? "#888" : "#666", lineHeight:1.5, maxWidth:140 }}>{node.desc}</div>
              {!locked && (<div style={{ marginTop:4, padding:"8px 20px", background: done ? node.color : isActive ? node.color : "rgba(0,0,0,0.08)", borderRadius:20, fontSize:12, fontWeight:900, color: done || isActive ? "white" : "#555", border: `2px solid ${done || isActive ? node.color : "rgba(0,0,0,0.1)"}`, transition:"all 0.2s" }}>{done ? "Rejouer →" : isActive ? "Continuer →" : "Découvrir →"}</div>)}
            </div>
          );
        })}
      </div>
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
];

function MinijeuScreen({ onBack, playerName, playerInfos, compoChoice }) {
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
    [...plate, ...entree, ...dessert].forEach(f => { if(f.pnns && bars[f.pnns]!==undefined) bars[f.pnns] = Math.min(bars[f.pnns]+33, 100); });
    if(glass) { bars.eau = glass.good ? 100 : 20; }
    return bars;
  };
  const handleDrop = (zone) => {
    if(!dragId) return;
    const food = FOODS_LIST.find(f=>f.id===dragId);
    if(!food) return;
    if(zone==="plate" && food.type==="plate") { if(plate.length >= 5) return; setPlate(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]); }
    else if(zone==="entree" && food.type==="entree") { if(entree.length >= 2) return; setEntree(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]); }
    else if(zone==="dessert" && food.type==="dessert") { if(dessert.length >= 2) return; setDessert(prev => prev.find(f=>f.id===dragId) ? prev : [...prev, food]); }
    else if(zone==="glass" && food.type==="glass") { setGlass(food); }
    setDragId(null);
  };
  const showEntree = compoChoice !== "Plat + Dessert";
  const showDessert = compoChoice !== "Entrée + Plat";
  const removeFromPlate = (id) => setPlate(prev=>prev.filter(f=>f.id!==id));
  const removeFromEntree = (id) => setEntree(prev=>prev.filter(f=>f.id!==id));
  const removeFromDessert = (id) => setDessert(prev=>prev.filter(f=>f.id!==id));
  const removeGlass = () => setGlass(null);
  const valider = () => {
    const allFoods = [...plate, ...entree, ...dessert];
    const bad = allFoods.filter(f=>!f.good);
    const good = allFoods.filter(f=>f.good);
    const badDrink = glass && !glass.good;
    saveGame({
      type: "minijeu",
      data: {
        plate: plate.map(f => f.name),
        entree: entree.map(f => f.name),
        dessert: dessert.map(f => f.name),
        glass: glass ? glass.name : null,
        bons_aliments: good.map(f => f.name),
        mauvais_aliments: bad.map(f => f.name),
        score: good.length + bad.length > 0 ? Math.round((good.length/(good.length+bad.length))*100) : 0,
        patient: { prenom: playerName, ...(playerInfos||{}) }
      }
    });
    if(bad.length===0 && !badDrink && good.length>=2) { setFeedback("Bonne assiette ! " + good.length + " aliment" + (good.length>1?"s":"") + " sain" + (good.length>1?"s":"") + (glass?" + boisson adaptée":"") + ". Score PNNS : " + Math.round((good.length/(good.length+bad.length))*100) + "%"); setFeedbackColor("#2e7d32"); playSound("badge"); }
    else { const issues = []; if(bad.length) issues.push(bad.map(f=>f.name).join(", ") + " déconseillé" + (bad.length>1?"s":"")); if(badDrink) issues.push("le soda est déconseillé"); if(!glass) issues.push("ajoute une boisson"); setFeedback(issues.join(" · ") + "."); setFeedbackColor("#c4622d"); }
  };
  const reset = () => { setPlate([]); setEntree([]); setDessert([]); setGlass(null); setFeedback(""); };
  const bars = getBars();

  const AssietteDrop = ({ zone, items, onRemove, size, maxItems }) => (
    <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop(zone)}
      style={{ width:size, height:size, position:"relative", flexShrink:0, borderRadius:"50%", background:"white", border:"4px solid #FA8072", boxShadow:"0 4px 16px rgba(250,128,114,0.25)", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, display:"flex", flexWrap:"wrap", alignItems:"center", justifyContent:"center", gap:4, padding:size*0.1 }}>
        {items.length === 0 && <span style={{ fontSize:11, color:"#FA8072", textAlign:"center", fontWeight:700 }}>Dépose ici</span>}
        {items.length >= maxItems && <span style={{ fontSize:10, color:"#FA8072", textAlign:"center", fontWeight:800 }}>Max !</span>}
        {items.map(food => (
          <span key={food.id} onClick={()=>onRemove(food.id)} title="Clic pour retirer" style={{ cursor:"pointer", position:"relative", zIndex:1 }}>
            <img src={food.emoji} style={{ width:size*0.2, height:size*0.2, objectFit:"contain" }} />
          </span>
        ))}
      </div>
    </div>
  );

  return (
    <div style={{ position:"fixed", inset:0, background:"white", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>
      {/* Header */}
      <div style={{ background:"#FA8072", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", flexShrink:0 }}>
        <span style={{ color:"white", fontWeight:900, fontSize:15 }}>🍽️ Compose ton repas</span>
        <div style={{ display:"flex", gap:10 }}>
          <button onClick={reset} style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>Réinitialiser</button>
          <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:8, color:"white", fontSize:12, fontWeight:800, padding:"6px 14px", cursor:"pointer" }}>← Retour au menu</button>
        </div>
      </div>

      {/* Corps : 50% aliments | 50% assiettes */}
      <div style={{ flex:1, display:"grid", gridTemplateColumns:"1fr 1fr", overflow:"hidden" }}>

        {/* GAUCHE — Aliments par catégorie */}
        <div style={{ borderRight:"2px solid #e0e0e0", overflowY:"auto", padding:"16px" }}>
          <div style={{ fontSize:13, fontWeight:900, color:"#FA8072", marginBottom:12, textTransform:"uppercase", letterSpacing:1 }}>Glisse les aliments sur ton assiette</div>
          {CATEGORIES_PNNS.map(cat => {
            const foods = FOODS_LIST.filter(f => f.categorie === cat);
            if (foods.length === 0) return null;
            return (
              <div key={cat} style={{ marginBottom:18 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#9ACD32", textTransform:"uppercase", letterSpacing:1, marginBottom:8, paddingBottom:4, borderBottom:"2px solid #f0f9e0" }}>{cat}</div>
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
          <div style={{ fontSize:13, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Mon plateau</div>

          {/* Assiettes en grille : 2 en haut + boisson, puis dessert en bas */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16 }}>
            {showEntree && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Entrée</div>
                <AssietteDrop zone="entree" items={entree} onRemove={removeFromEntree} size={180} maxItems={2} />
              </div>
            )}
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Plat principal</div>
              <AssietteDrop zone="plate" items={plate} onRemove={removeFromPlate} size={180} maxItems={5} />
            </div>
            {showDessert && (
              <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1 }}>Dessert</div>
                <AssietteDrop zone="dessert" items={dessert} onRemove={removeFromDessert} size={180} maxItems={2} />
              </div>
            )}
            {/* Boisson */}
            <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:6 }}>
              <div style={{ fontSize:11, fontWeight:900, color:"#9ACD32", textTransform:"uppercase", letterSpacing:1 }}>Boisson</div>
              <div onDragOver={e=>e.preventDefault()} onDrop={()=>handleDrop("glass")} onClick={removeGlass}
                style={{ width:80, height:120, borderRadius:"0 0 16px 16px", border:"3px solid #9ACD32", background:glass?glass.color+"22":"#f5f9ee", overflow:"hidden", cursor:glass?"pointer":"default", position:"relative", boxShadow:"0 2px 8px rgba(135,206,235,0.3)" }}>
                {glass && <div style={{ position:"absolute", bottom:0, left:0, right:0, height:"70%", background:glass.color, opacity:0.5, borderRadius:"0 0 14px 14px" }} />}
                {glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center" }}><img src={glass.emoji} style={{ width:40, height:40, objectFit:"contain" }} /></div>}
                {!glass && <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:11, color:"#87CEEB", fontWeight:700, textAlign:"center", padding:4 }}>Dépose ici</div>}
              </div>
              <div style={{ fontSize:11, color:"#666", fontWeight:700 }}>{glass ? glass.name : "—"}</div>
            </div>
          </div>



          {/* Bouton valider */}
          <button onClick={valider} style={{ background:"#FA8072", border:"3px solid #222", borderRadius:12, color:"white", fontSize:15, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            ✅ Valider mon repas
          </button>
          {feedback && (
            <div style={{ background:feedbackColor==="#2e7d32"?"#e8f5e9":"#fbe9e7", border:`2px solid ${feedbackColor}`, borderRadius:12, padding:"12px 16px", fontSize:13, color:feedbackColor, fontWeight:700, textAlign:"center" }}>
              {feedback}
            </div>
          )}
          <button onClick={onBack}
            style={{ background:"white", border:"2px solid #FA8072", borderRadius:12, color:"#FA8072", fontSize:14, fontWeight:800, padding:"12px", cursor:"pointer", marginTop:4 }}>
            ← Retour au menu des missions
          </button>
        </div>
      </div>
    </div>
  );
}

/* ══ RECETTES RAPIDES PNNS ══ */
const RECETTES_DATA = [
  {
    id:"sardines", image:"/sardine.png", categorie:"Tartines", tag:"Sans cuisson", temps:"15 min", type:"Plat complet",
    profils:["rapide","poisson","sans_porc","mediterraneen"],
    titre:"Tartines de sardines et tomates",
    benefice:"Pain complet riche en fibres et sardines riches en oméga-3.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2731-tartines-de-sardines-et-tomates",
    ingredients:["1 gousse d'ail","1 poignée de roquette","10 cl d'huile d'olive","2 petites boîtes de sardines à l'huile (conserve)","300 g de tomates","4 tranches de pain de campagne","1 cuillère à café d'herbes de Provence","1 pincée de poivre","1 pincée de sel"],
    etapes:["Égoutter les sardines. Enlever les arêtes. Réserver.","Laver les tomates, les épépiner puis les couper en petits dés.","Émincer grossièrement la roquette.","Dans un saladier, mélanger la roquette, les dés de tomates, l'huile et les herbes de Provence. Saler, poivrer. Réserver.","Griller les tranches de pain puis les frotter légèrement à l'ail.","Disposer les sardines en les partageant entre les 4 tartines. Ajouter la salade de tomates et la roquette marinées.","Bonne dégustation."],
  },
  {
    id:"grecque", image:"/salade_grecque.png", categorie:"Salades", tag:"Sans cuisson", temps:"10 min", type:"Entrée",
    profils:["rapide","vegetarien","sans_porc","mediterraneen","legumes"],
    titre:"Salade à la grecque",
    benefice:"Riche en légumes et fibres — aide à atteindre les 5 fruits et légumes recommandés par jour.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2516-salade-a-la-grecque",
    ingredients:["5 tomates","350 g de feta","1 concombre","1 poivron rouge","1 oignon rouge","1 filet d'huile d'olive","60 g d'olives noires","1 citron (pour le jus)","1 bouquet d'origan","1 pincée de poivre","1 pincée de sel"],
    etapes:["Couper la feta en cubes.","Laver les tomates et les trancher. Peler et couper le concombre en rondelles.","Épépiner le poivron rouge, le trancher en fines lanières. Peler et émincer finement l'oignon rouge.","Ciseler le bouquet d'origan. Placer tous les ingrédients dans un saladier, ajouter les olives noires.","Verser dessus le jus d'un citron, un filet d'huile d'olive, du sel et du poivre. Bien mélanger. Servir."],
  },
  {
    id:"concombre-yaourt", image:"/recettes/concombre-yaourt.jpg", categorie:"Salades", tag:"Sans cuisson", temps:"10 min", type:"Entrée",
    profils:["rapide","vegetarien","sans_porc","legumes"],
    titre:"Salade de concombre au yaourt",
    benefice:"Plus de légumes riches en fibres — bon moyen d'atteindre les 5 portions de fruits et légumes par jour.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2544-salade-de-concombre-au-yaourt",
    ingredients:["1 cuillère à soupe d'huile d'olive","1 cuillère à soupe de menthe fraîche","1 concombre","1 gousse d'ail","1 pot de yaourt au lait de brebis","2 pincées de paprika en poudre","1 pincée de poivre","1 pincée de sel"],
    etapes:["Épluchez le concombre, coupez-le en deux dans la longueur et retirez les graines. Détaillez-les ensuite en petits dés.","Pelez la gousse d'ail. Écrasez-la au pilon dans un saladier avec un peu de sel puis versez le yaourt et l'huile d'olive. Mélangez.","Ajoutez les dés de concombre, salez et poivrez. Parsemez de menthe et remuez délicatement. Mettez au réfrigérateur jusqu'au moment de servir.","Au dernier moment, saupoudrez un peu de paprika en surface et décorez de quelques feuilles de menthe fraîche."],
  },
  {
    id:"shakshuka", image:"/Shakshuka.png", categorie:"Plats rapides", tag:"Cuisson rapide", temps:"7 min", type:"Plat complet",
    profils:["rapide","vegetarien","sans_porc","legumes"],
    titre:"Shakshuka",
    benefice:"Légumes, œufs et pain complet — rapide, équilibré et rassasiant.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2831-shakshuka",
    ingredients:["2 tranches de pain complet","1 bocal de tomates pelées (conserve)","2 œufs","1 oignon","1 goutte d'huile de colza","1 brin de coriandre fraîche","1 pincée de cumin","1 pincée de poivre","1 pincée de sel"],
    etapes:["Trancher le pain en gros morceaux.","Émincer l'oignon. Couper les tomates en morceaux si elles sont entières.","Faire revenir l'oignon dans une poêle.","Verser dans la poêle les tomates, le sel, le poivre, le cumin et la coriandre.","Mélanger les ingrédients. Attendre que les tomates fondent.","Casser les œufs sur le mélange. Laisser cuire jusqu'à ce que le blanc ne soit plus translucide.","Ajouter le pain et déguster."],
  },
  {
    id:"poulet-curry", image:"/poulet_curry.png", categorie:"Plats rapides", tag:"Cuisson rapide", temps:"25 min", type:"Plat simple",
    profils:["rapide","sans_porc"],
    titre:"Poulet au curry express",
    benefice:"Volaille privilégiée comme recommandé — saveurs variées grâce aux épices. À accompagner de riz complet.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2242-poulet-au-curry-express",
    ingredients:["400 ml de lait de coco (conserve)","1 cuillère à soupe de curry","400 g de blanc de poulet","4 brins de coriandre fraîche","1 pincée de sel"],
    etapes:["Versez le lait de coco dans une poêle. Ajoutez le curry.","Faites chauffer à découvert à feu doux 15 min environ.","Découpez les escalopes de poulet en morceaux. Déposez-les dans la poêle.","Faites cuire à feu doux 6 à 8 min.","Le lait de coco ne doit pas bouillir.","Sortez les morceaux de poulet de la poêle.","Déposez-les sur un plat."],
  },
  {
    id:"curry-lentilles", image:"/curry_lentille.png", categorie:"Plats rapides", tag:"Cuisson rapide", temps:"23 min", type:"Plat complet",
    profils:["rapide","vegetarien","sans_porc","legumineuses","mediterraneen"],
    titre:"Le curry aux lentilles",
    benefice:"Plus de légumes secs sans passer des heures en cuisine — lentilles corail rapides, gourmandes et riches en fibres.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2829-le-curry-aux-lentilles",
    ingredients:["1 cuillère à soupe de curry","1 gousse d'ail","1 pincée de poivre","1 pincée de sel","10 cl d'eau","2 escalopes de volaille (optionnel)","70 g de lentilles corail","1 cuillère à soupe d'huile de colza","1 brique de lait de coco (conserve)"],
    etapes:["Couper l'ail en petits morceaux.","Chauffer l'huile dans une casserole à feu moyen. Faire revenir l'ail.","Rincer les lentilles. Les verser dans la casserole avec le lait de coco, l'eau et le curry. Mélanger. En option : ajouter deux escalopes de volaille coupées en morceaux.","Couvrir la casserole et laisser cuire à feu doux pendant 20 minutes, en mélangeant de temps en temps.","Ajouter une pincée de sel et du poivre à la préparation. En option : ajouter de la coriandre ou du persil frais.","Servir chaud."],
  },  {
    id:"ragout-haricots", image:"/ragout.png", categorie:"Plats mijotés", tag:"Cuisson rapide", temps:"30 min", type:"Plat complet",
    profils:["vegetarien","sans_porc","legumineuses","legumes"],
    titre:"Ragoût de haricots blancs, épinards et tomates séchées",
    benefice:"Riche en légumes secs et légumes — fibres et protéines végétales.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/200000266-ragout-de-haricots-blancs-epinards-et-tomates-sechees",
    ingredients:["500 g de haricots blancs (conserve)","100 g d'épinards surgelés","100 g de tomates séchées","3 gousses d'ail","2 oignons","50 ml de crème fraîche liquide","400 ml d'eau","4 tranches de pain","5 feuilles de basilic frais","1 pincée de sel","1 pincée de poivre","1 pincée de paprika en poudre","1 cuillère à café de curry","1 pincée d'origan"],
    etapes:["Éplucher et couper l'oignon et l'ail en petits morceaux. Tailler les tomates séchées en petits cubes.","Récupérer un filet de l'huile des tomates séchées. La faire chauffer dans une marmite et y faire revenir l'oignon et l'ail quelques minutes.","Ajouter les tomates séchées, l'origan, le paprika et le curry et laisser cuire quelques minutes de plus.","Verser les haricots blancs égouttés, les épinards, le basilic, le sel et le poivre. Bien mélanger.","Verser l'eau et la crème fraîche. Laisser mijoter 20 min.","Servir avec les tranches de pain."],
  },
  {
    id:"quiche-poireaux", image:"/quiche.png", categorie:"Plats mijotés", tag:"Cuisson rapide", temps:"45 min", type:"Plat complet",
    profils:["vegetarien","sans_porc","legumes"],
    titre:"Quiche poireaux-roquefort",
    benefice:"Plus de légumes — bon moyen d'atteindre les 5 portions recommandées par jour.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2619-quiche-poireaux-roquefort",
    ingredients:["2 poireaux","1 pâte feuilletée","100 ml de crème fraîche fluide 15% MG","125 g de roquefort","300 ml de lait demi-écrémé","4 œufs","1 pincée de noix de muscade","1 pincée de poivre","1 pincée de sel"],
    etapes:["Enlever le vert du poireau. Laver le blanc. L'émincer en petits tronçons. Les déposer dans une poêle.","Ajouter 1 grand verre d'eau. Saler. Couvrir et faire cuire à feu moyen 20 min environ jusqu'à obtenir une fondue de poireaux.","Les égoutter. Ajouter 2 pincées de muscade. Rectifier l'assaisonnement.","Préchauffer le four à 180°C. Étaler la pâte dans un moule. Piquer le fond. Enfourner 10 min.","Disposer la fondue de poireaux sur le fond de tarte.","Battre ensemble les œufs, la crème fraîche et le lait. Écraser le roquefort et le joindre à la préparation. Verser sur la tarte.","Enfourner 20 à 30 min. Servir chaud ou tiède avec une salade."],
  },
  {
    id:"flan-courgettes", image:"/flan.png", categorie:"Plats mijotés", tag:"Cuisson rapide", temps:"45 min", type:"Plat complet",
    profils:["vegetarien","sans_porc","legumes"],
    titre:"Flan aux courgettes",
    benefice:"Légumes et œufs — source de protéines et de vitamines.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2116-flan-aux-courgettes",
    ingredients:["10 cl de crème fraîche liquide","3 œufs","3 courgettes","1 pincée de noix de muscade","1 pincée de poivre","1 pincée de sel"],
    etapes:["Laver et couper les courgettes en rondelles. Les faire cuire à l'eau pendant 15 min environ.","Préchauffer votre four à 180°C.","Répartir les courgettes cuites au fond d'un plat à gratin ou d'un moule à tarte.","Battre les œufs en omelette, ajouter la muscade, la crème fraîche, saler, poivrer et verser le mélange sur les courgettes.","Faire cuire 25 min jusqu'à ce que le dessus soit légèrement doré."],
  },
  {
    id:"lentilles-lardons", image:"/lentille_lardon.png", categorie:"Plats mijotés", tag:"Cuisson rapide", temps:"30 min", type:"Plat complet",
    profils:["legumineuses"],
    titre:"Lentilles aux lardons",
    benefice:"Légumes secs riches en fibres et protéines — un plat complet et nourrissant.",
    source:"mangerbouger.fr",
    url:"https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/200000159-lentilles-aux-lardons",
    ingredients:["1 grande boîte de lentilles (conserve)","200 g de lardons (ou lardons de volaille)","2 carottes","1 oignon","3 cuillères à soupe de moutarde"],
    etapes:["Éplucher et émincer l'oignon. Le faire revenir dans une poêle avec un peu d'huile d'olive.","Éplucher et couper les carottes en dés. Les ajouter aux oignons.","Ajouter les lardons et la moutarde à la préparation.","Égoutter les lentilles et les ajouter à l'ensemble. Laisser cuire 20 minutes en remuant de temps en temps.","Saler et poivrer, déguster chaud !"],
  },
  {
    id: "omelette-champignons",
    image: "/omelette.png",
    categorie: "Plats rapides",
    tag: "Cuisson rapide",
    temps: "20 min",
    type: "Plat complet",
    profils: ["rapide", "vegetarien", "sans_porc"],
    titre: "Omelette aux champignons et salade",
    benefice: "Les œufs apportent des protéines complètes et les champignons des fibres — un repas léger et rassasiant.",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/11290",
    ingredients: [
      "4 œufs", "1/2 cuillère à café de moutarde", "1/2 grande boîte de champignons de Paris (conserve)",
      "2 pincées de sel", "1 cuillère à soupe d'huile d'olive", "1/2 cuillère à soupe de vinaigre de vin",
      "1 cuillère à soupe de crème fraîche épaisse 15% MG", "1 pincée de poivre",
      "1/2 salade", "1,5 cuillère à soupe d'huile de colza"
    ],
    etapes: [
      "Casser les œufs dans un saladier et les battre à l'aide d'une fourchette. Saler, poivrer et ajouter la crème fraîche.",
      "Battre à nouveau et ajouter les champignons égouttés. Battre l'ensemble.",
      "Faire chauffer l'huile de colza dans une poêle et faire cuire l'omelette à feu doux.",
      "Laver la salade. Préparer la vinaigrette en délayant la moutarde avec le vinaigre, sel et poivre, puis émulsionner avec les deux huiles.",
      "Servir l'omelette avec la salade assaisonnée."
    ]
  },
  {
    id: "oeuf-mollet-lentilles",
    image: "/oeuf_mollet.png",
    categorie: "Plats mijotés",
    tag: "Cuisson rapide",
    temps: "30 min",
    type: "Plat complet",
    profils: ["vegetarien", "sans_porc", "legumineuses", "legumes", "mediterraneen"],
    titre: "Œuf mollet aux lentilles corail et épices",
    benefice: "Lentilles corail riches en fibres et protéines végétales, épinards pour le fer — un plat complet très équilibré.",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/oeuf-mollet-lentilles-corail",
    ingredients: [
      "4 œufs", "200 g de lentilles corail", "500 g d'épinards frais", "4 champignons de Paris",
      "1 oignon", "1 gousse d'ail", "1 brin de coriandre fraîche",
      "1 cuillère à soupe de cumin", "1 cuillère à café de curry",
      "2 cuillères à soupe d'huile d'olive", "2 pincées de sel", "2 pincées de poivre"
    ],
    etapes: [
      "Porter à ébullition un grand volume d'eau salée. Plonger les lentilles corail et les faire cuire 7 minutes.",
      "Dans une poêle, faire cuire l'oignon et l'ail dans un filet d'huile d'olive. Ajouter les champignons et les épinards, remuer pendant 10 minutes.",
      "Égoutter les lentilles, les verser dans un bol et ajouter les épices (cumin, curry). Mélanger.",
      "Plonger les œufs dans une casserole d'eau bouillante et les cuire 6 minutes. Rincer sous l'eau froide et écaler.",
      "Servir les lentilles dans une assiette, ajouter les légumes par-dessus, puis l'œuf mollet et la coriandre ciselée."
    ]
  },
  {
    id: "burger-pois-chiches",
    image: "/burger.png",
    categorie: "Plats rapides",
    tag: "Cuisson rapide",
    temps: "30 min",
    type: "Plat complet",
    profils: ["vegetarien", "sans_porc", "legumineuses", "legumes"],
    titre: "Burger de pois chiches aux légumes",
    benefice: "Les pois chiches remplacent la viande avec des protéines végétales et des fibres — idéal pour manger moins de viande.",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/burger-pois-chiches",
    ingredients: [
      "4 pains hamburger", "4 noix de beurre", "3 cuillères à soupe de coriandre fraîche",
      "1 pincée de poivre", "1 carotte", "3 cuillères à soupe de chapelure",
      "3 cuillères à soupe d'huile d'olive", "1 oignon", "2 tomates",
      "1 pincée de sel", "400 g de pois chiches (conserve)", "1 œuf",
      "1 cuillère à café de moutarde", "2 courgettes", "1 gousse d'ail",
      "1 salade", "1 cuillère à soupe de vinaigre de vin", "50 g de fromage blanc 0%"
    ],
    etapes: [
      "Faire revenir l'oignon 5 min dans 1 c. à s. d'huile d'olive. Ajouter l'ail, les courgettes et carottes émincés, cuire 2-3 min. Égoutter.",
      "Mixer la chapelure et les pois chiches. Ajouter les légumes, le beurre, le jaune d'œuf et la coriandre. Mixer jusqu'à homogénéité.",
      "Former 6 galettes et réfrigérer 10 min.",
      "Faire cuire les galettes 1 à 2 min de chaque côté dans une poêle huilée.",
      "Faire chauffer les pains, les couper en deux. Poser les galettes et une rondelle de tomate.",
      "Préparer la vinaigrette avec moutarde, vinaigre, fromage blanc et huile. Servir avec la salade assaisonnée."
    ]
  },
  {
    id: "veloute-pois-casses",
    image: "/veloute.png",
    categorie: "Plats mijotés",
    tag: "Cuisson rapide",
    temps: "40 min",
    type: "Plat complet",
    profils: ["vegetarien", "sans_porc", "legumineuses"],
    titre: "Velouté de pois cassés",
    benefice: "Les pois cassés sont riches en fibres et protéines végétales — un velouté nourrissant qui booste les apports en légumineuses.",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/veloute-pois-casses",
    ingredients: [
      "150 g de pois cassés", "200 g de carottes", "4 œufs", "4 feuilles de laurier",
      "1 oignon", "1 cuillère à soupe de thym", "2 cuillères à soupe d'huile d'olive",
      "2 pincées de sel", "2 pincées de poivre"
    ],
    etapes: [
      "Faire cuire les pois cassés selon les indications de l'emballage dans un grand volume d'eau bouillante.",
      "Éplucher et couper la carotte en dés, ciseler l'oignon. Faire revenir 5 min dans une cocotte avec l'huile d'olive.",
      "Égoutter les pois cassés, les ajouter dans la cocotte. Recouvrir d'eau, ajouter le laurier et le sel. Cuire 30 min à feu moyen.",
      "Faire cuire les œufs 6 min dans l'eau bouillante. Les éplucher sous l'eau froide.",
      "Mixer les légumes dans la cocotte. Ajuster l'assaisonnement.",
      "Verser le velouté dans un bol et disposer l'œuf mollet par-dessus."
    ]
  },
  {
    id: "tarte-ratatouille",
    image: "/ratatouille.png",
    categorie: "Plats mijotés",
    tag: "Cuisson rapide",
    temps: "25 min",
    type: "Plat complet",
    profils: ["vegetarien", "sans_porc", "legumes"],
    titre: "Tarte à la ratatouille",
    benefice: "Plus de légumes — un bon moyen d'atteindre les 5 portions de fruits et légumes recommandées par jour.",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/tarte-ratatouille",
    ingredients: [
      "1 pot de ratatouille surgelée", "1 pâte feuilletée", "3 œufs",
      "50 g de gruyère râpé", "1 pincée de poivre", "1 pincée de sel"
    ],
    etapes: [
      "Préchauffer le four à 200°C.",
      "Déposer la pâte dans un moule à tarte avec le papier sulfurisé. Piquer le fond et enfourner 10 min.",
      "Faire revenir la ratatouille dans une poêle légèrement huilée quelques minutes.",
      "Battre les œufs en omelette. Ajouter la ratatouille égouttée et le gruyère. Saler, poivrer.",
      "Verser le mélange sur le fond de tarte précuit. Enfourner 20 min."
    ]
  },

    {
    id: "poisson_oseille",
    image: "/poisson_oseille.png",
    categorie: "Plats mijoté",
    tag: "Cuisson rapide",
    temps: "20 min",
    type: "Plat simple",
    profils: [ "sans_porc", "legumes"],
    titre: "Poisson sauce à l'oseille",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/1225-poisson-sauce-a-loseille",
     ingredients: [
      "Oseille 30g", "1 noisette de beurre", " 1 pincée de poivre ",
      "400g de cabillaud", "100g de crème fraiche paisse 15% MG", "1 cuillère à soupe de farine", "1 oignon", "1 pincée de sel",
    ],
    etapes: [
      "Préchauffer le four à 200°C.",
      "Eplucher l'oignon et le couper en rondelles. Disposer le dans un plat allant au four avec le poisson puis enfourner pendant 15 minutes.",
      "Laver l'oseille et couper la finement. Fondre le beurre dans une casserole puis ajouter l'oseille tout en remuant. Verser la farine dans la casserole quand l'oseille change de couleur. Ajouter ensuite la crème et continuer de mélanger.",
      "Saler et poivrer la sauce.",
      "Recouvrir le poisson de la sauce 5 minutes avant la fin de cuisson.",
      "Servir."
    ]
  },

 {
    id: "poisson_bordelaise",
    image: "/poisson_bordelaise.png",
    categorie: "Plats mijoté",
    tag: "Cuisson rapide",
    temps: "25 min",
    type: "Plat simple",
    profils: [ "sans_porc", "legumes"],
    titre: "Poisson sauce à la bordelaise",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/1223-poisson-a-la-bordelaise",
     ingredients: [
      "40g de chapelure", "1 filet d'huile d'olive", " 1 cuillère à soupe de Persil",
      "10cl de vin blanc sec", "4 filets de Colin", "2 Echalote", "1 cuillère à soupe de jus de Citron", 
    ],
    etapes: [
      "Préchauffer le four à 1800°C.",
      "Eplucher et hâcher les échalotes. Verser les dans une poêle avec l'huile puis les faire revenir.",
      "Ajouter le jus de citron avec le vin blanc. Cuire pendant quelques minutes puis ajouter la chapelure mélangée au persil.",
      "Placer les filets de colin dans un plat allant au four puis verser-y la préparation.",
      "Cuire 20 minutes.",
    ]
  },

 {
    id: "Brochette_thon_fenouil",
    image: "/brochette_thon.png",
    categorie: "Plats complet",
    tag: "Cuisson rapide",
    temps: "15 min",
    type: "Plat simple",
    profils: [ "sans_porc", "legumes", "poisson"],
    titre: "Brochettes de thon au fenouil et citron",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/128-brochettes-de-thon-au-fenouil-et-citron",
     ingredients: [
      "4 cuillère à soupe Huile d'olive", "4 citron", "4 Oignons ",
      "1 pièce Fenouil", "500g  thon frais", 
    ],
    etapes: [
      "Préchauffer le four à 210 °C (th. 7).",
      "Faire tremper dans l'eau les piques des brochettes en bois (pour éviter qu’elles ne brûlent à la cuisson).",
      "Couper le thon en gros cubes et les arroser du jus d’un citron et d’huile d’olive.",
      "Peler et couper les oignons en quartiers.",
      "Nettoyer les fenouils et les couper en larges morceaux.",
      "Laver et couper en quartiers les trois citrons restants et les tomates.",
      "Piquer en alternance sur les brochettes : cubes de thon, quartiers d'oignons, quartiers de tomate, morceaux de fenouil et quartiers de citron.",
      "Placer les brochettes dans un plat à four et les faire griller 15 min. À mi-cuisson, les retourner et les arroser d’un peu de jus de citron et d’huile d’olive.",   
      "Saler et poivrer.",
]
  },

 {
    id: "Dessert_gourmands",
    image: "/dessert_gourmand.png",
    categorie: "Dessert",
    tag: "préparation rapide",
    temps: "30 min",
    type: "Dessert simple",
    profils: [ "sans_porc", "legumes", "poisson","dessert"],
    titre: "Desserts gourmands",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/2589-creme-dessert-au-chocolat",
     ingredients: [
      "25g Fécule de mais(maizena", "40cl Lait demi-écrémé", "40g Cacao en poudre ",
      "40g Sucre roux", 
    ],
    etapes: [
      "Mélanger la maizena avec le cacao et le sucre dans un saladier. Porter à ébullition le lait.",
      "Ajouter le lait chaud dans le saladier tout en remuant avec un fouet. Verser le mélange dans la casserole et faire cuire à feu moyen jusqu'à épaississement sans cesser de mélanger avec un fouet.",
      "Repartir la crème dans des moules. Laisser refroidir. Déguster la crème tiède ou froide.",
]
  },

 {
    id: "Petits_gateaux",
    image: "/petit_gateaux.png",
    categorie: "Dessert",
    tag: "préparation rapide",
    temps: "30 min",
    type: "Dessert gourmands",
    profils: [ "sans_porc", "legumes", "poisson","dessert"],
    titre: "Petits gâteaux moelleux à la noix de coco",
    source: "mangerbouger.fr",
    url: "https://www.mangerbouger.fr/manger-mieux/la-fabrique-a-menus/recettes/1159-petits-gateaux-moelleux-a-la-noix-de-coco",
     ingredients: [
      "60g Sucre en poudre", "150g Farine", "60g Noix de coco râpée", "2 Oeufs", "1 pot Yaourt nature", "70g Margarine", "1 sachet Levure", 
      
    ],
    etapes: [
     "réchauffer le four à 180 °C (th. 6).",
     "Incorporer la levure chimique à la farine.",
     "Dans un saladier, mélanger la margarine et le sucre à l’aide d’une spatule en bois jusqu’à ce que le mélange blanchisse.",
     "Ajouter un œuf tout en continuant de mélanger, puis une partie de la farine, puis l’autre œuf et le reste de la farine.",
     "Verser le yaourt et la noix de coco, mélanger à nouveau.",
     "Répartir la préparation dans un moule en silicone à 8 alvéoles et déposer une pincée de noix de coco sur chaque gâteau pour décorer. Mettre au four pour 20 min.",
     "Lorsque les gâteaux sont cuits, les laisser reposer 5 min avant de les démouler.",
    "Servir tiède ou froid.",
    ]
  },
];
const CATEGORIES = ["Tout", "Tartines", "Salades", "Plats rapides", "Plats mijotés"];
const TAGS = ["Tout", "Sans cuisson", "Cuisson rapide"];

// Profils de recommandation
const PROFILS = {
  rapide: "rapide",
  vegetarien: "vegetarien",
  sans_porc: "sans_porc",
  poisson: "poisson",
  mediterraneen: "mediterraneen",
  senior: "senior",
  legumes: "legumes",
  legumineuses: "legumineuses",
};

/* ══ DONNÉES PETIT DÉJEUNER ══ */
const PETIT_DEJ_DATA = [
  { jour:"Lundi", items:["Tartines de pain complet avec confiture de framboises","Un morceau de comté (30 g)","Une compote pomme/poire sans sucre ajouté"] },
  { jour:"Mardi", items:["Tartines de pain complet avec un peu de beurre","Fromage blanc (125g) avec morceaux de banane et poire, quelques amandes et un filet de miel"] },
  { jour:"Mercredi", items:["Tartines de pain complet avec fromage frais","Une banane"] },
  { jour:"Jeudi", items:["Tartines de pain aux céréales avec confiture d'abricots","Un morceau d'emmental (30 g)","Un bol de fruits de saison (kiwi l'hiver, fraises l'été)"] },
  { jour:"Vendredi", items:["Tartines de pain complet au miel","Un yaourt nature avec confiture de fraises","Une mandarine (hiver) ou cerises (été)"] },
  { jour:"Samedi", items:["Tranches de pain complet grillées à tremper dans un œuf à la coque","Un bol de fruits découpés en morceaux"] },
  { jour:"Dimanche", items:["Une ou deux tranches de quatre-quarts maison","Une coupelle de compote maison"] },
];

/* ══ RECOMMANDATIONS PAR PROFIL ══ */
const RECOMMANDATIONS = {
  legumes: {
    titre:" Augmentez vos fruits et légumes",
    couleur:"#4caf50",
    bg:"#e8f5e9",
    texte:"Le PNNS recommande au moins 5 portions (400g) par jour. Variez les couleurs pour maximiser les apports en vitamines et antioxydants.",
    conseils:["Ajoutez des légumes dans chaque repas","Préférez les légumes frais ou surgelés nature","Mangez au moins un fruit entier par jour","Les jus de fruits ne remplacent pas les fruits entiers"],
    profil:"legumes"
  },
  legumineuses: {
    titre:"🫘 Mangez plus de légumes secs",
    couleur:"#795548",
    bg:"#efebe9",
    texte:"Le PNNS recommande au moins 2 portions par semaine. Lentilles, pois chiches, haricots secs sont riches en fibres et protéines végétales.",
    conseils:["Remplacez la viande par des légumineuses 2x/semaine","Ajoutez des lentilles dans vos soupes","Utilisez les pois chiches en conserve pour aller vite","Pensez au houmous comme en-cas"],
    profil:"legumineuses"
  },
  poisson: {
    titre:" Mangez plus de poisson",
    couleur:"#0288d1",
    bg:"#e1f5fe",
    texte:"Le PNNS recommande 2 portions par semaine, en alternant poissons gras (saumon, sardine, maquereau) et maigres (cabillaud, merlu).",
    conseils:["Privilégiez les poissons gras riches en oméga-3","Les conserves (sardines, thon) comptent aussi","Remplacez la viande rouge par du poisson 2x/sem","Évitez les poissons panés industriels"],
    profil:"poisson"
  },
  charcuterie: {
    titre:"⚠️ Réduisez la charcuterie",
    couleur:"#e53935",
    bg:"#fbe9e7",
    texte:"La charcuterie est classée cancérigène groupe 1 par l'OMS. Le PNNS recommande de la limiter à 150g/semaine maximum.",
    conseils:["Remplacez la charcuterie par des œufs ou du poulet","Lisez les étiquettes (sel, graisses cachés)","Choisissez du jambon blanc plutôt que saucisson","Réduisez progressivement pour ne pas vous frustrer"],
    profil:"charcuterie"
  },
  fastFood: {
    titre:" Réduisez le fast food",
    couleur:"#e53935",
    bg:"#fbe9e7",
    texte:"Les aliments ultra-transformés sont liés à l'obésité, au diabète et aux maladies cardiovasculaires. Privilégiez le fait maison.",
    conseils:["Cuisinez en grande quantité et congelez","Préparez des repas simples en 20 min (œufs, légumes)","Si fast food : préférez les salades et eau","Planifiez vos repas en début de semaine"],
    profil:"fastFood"
  },
  sucres: {
    titre:" Réduisez les sucreries",
    couleur:"#f57c00",
    bg:"#fff8e1",
    texte:"Les sucres ajoutés favorisent les caries, le surpoids et le diabète de type 2. Le PNNS recommande de les limiter.",
    conseils:["Remplacez les sucreries par des fruits frais","Lisez les étiquettes : sucre ajouté se cache partout","Cuisinez vous-même vos desserts (moins de sucre)","Limitez les boissons sucrées : eau à la place"],
    profil:"sucres"
  },
  mediterraneen: {
    titre:"🫒 Le régime méditerranéen",
    couleur:"#2e7d32",
    bg:"#e8f5e9",
    texte:"Reconnu pour favoriser l'équilibre alimentaire. Riche en fruits, légumes, légumineuses, poisson et huile d'olive. Limite la viande rouge et les produits transformés.",
    conseils:["Utilisez l'huile d'olive comme matière grasse principale","Mangez du poisson au moins 2x/semaine","Privilégiez les céréales complètes","Consommez des légumineuses 2-3x/semaine","Limitez la viande rouge à 1-2x/semaine"],
    profil:"mediterraneen"
  },
  senior: {
    titre:" Conseils pour bien manger après 75 ans",
    couleur:"#6a1b9a",
    bg:"#f3e5f5",
    texte:"Après 75 ans, les besoins nutritionnels changent. Il est important de maintenir ses apports en protéines et de ne pas sauter de repas.",
    conseils:[
      "Gardez un œil sur le contenu de votre réfrigérateur",
      "Continuez de prendre 3 repas par jour, même légers",
      "Enrichissez votre alimentation : fromage râpé dans les pâtes, œuf battu dans les gratins",
      "Bannissez les produits allégés",
      "Privilégiez les protéines : viande, œufs ou poisson 1-2x/jour",
      "Optez pour 3 à 4 produits laitiers par jour",
      "Stimulez votre appétit avec des épices et herbes aromatiques",
      "Ne supprimez pas le sel sauf prescription médicale",
      "Variez les modes de cuisson et les textures",
      "Prenez le temps de mettre la table joliment"
    ],
    profil:"senior"
  },
};

/* ══ COMPOSANT RECOMMANDATION ══ */
function RecoCard({ reco, recettes, onVoirRecettes }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ background:"#fff", borderRadius:20, marginBottom:12, boxShadow: open ? "0 8px 32px rgba(26,58,92,0.12)" : "0 2px 12px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2", overflow:"hidden", transition:"box-shadow 0.2s" }}>
      <div onClick={() => setOpen(o => !o)} style={{ padding:"18px 20px", cursor:"pointer", display:"flex", alignItems:"center", gap:14 }}>
        <div style={{ width:44, height:44, borderRadius:14, background:reco.bg, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
          <div style={{ width:20, height:20, borderRadius:"50%", background:reco.couleur }} />
        </div>
        <div style={{ flex:1, minWidth:0 }}>
          <div style={{ fontSize:15, fontWeight:800, color:"#1A1A1A", lineHeight:1.3 }}>{reco.titre}</div>
          <div style={{ fontSize:12, color:"#6B7280", marginTop:2 }}>{reco.texte.slice(0,55)}…</div>
        </div>
        <div style={{ fontSize:12, color:"#6B7280", fontWeight:700, transform: open ? "rotate(180deg)" : "none", transition:"transform 0.2s", flexShrink:0 }}>▼</div>
      </div>
      {open && (
        <div style={{ borderTop:"1px solid #F1F5F9", padding:"20px" }}>
          <p style={{ fontSize:14, color:"#374151", lineHeight:1.7, margin:"0 0 16px" }}>{reco.texte}</p>
          <div style={{ display:"flex", flexDirection:"column", gap:10, marginBottom: recettes.length > 0 ? 16 : 0 }}>
            {reco.conseils.map((c, i) => (
              <div key={i} style={{ display:"flex", gap:12, alignItems:"flex-start" }}>
                <div style={{ width:24, height:24, borderRadius:8, background:reco.bg, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:11, fontWeight:800, color:reco.couleur }}>{i+1}</div>
                <span style={{ fontSize:13, color:"#374151", lineHeight:1.6, paddingTop:3 }}>{c}</span>
              </div>
            ))}
          </div>
          {recettes.length > 0 && (
            <button onClick={() => onVoirRecettes(reco.profil)}
              style={{ background:reco.couleur, color:"white", border:"none", borderRadius:12, padding:"13px 20px", fontSize:13, fontWeight:800, cursor:"pointer", width:"100%", transition:"opacity 0.15s" }}
              onMouseEnter={e => e.currentTarget.style.opacity="0.85"}
              onMouseLeave={e => e.currentTarget.style.opacity="1"}>
              Voir les {recettes.length} recettes →
            </button>
          )}
        </div>
      )}
    </div>
  );
}


/* ══ PAGE PROFIL QCM1 ══ */
function ProfilQcm1Screen({ nutrition, playerName, onVoirRecos, onVoirRecettes, onBack }) {

  const CATEGORIES = [
    { label:"Fruits & légumes", img:"/legume2.png", couleur:"#4caf50", bg:"#e8f5e9",
      score: Math.round(((nutrition.legumes||0)+(nutrition.fruits||0))/2),
      attendu:70, inverted:false,
      desc:(s)=> s>=70?"Tu atteins les 5 portions/jour recommandées ✓":s>=40?"Consommation modérée — objectif : 5 portions/jour":"Tu en manges rarement — objectif : 5 portions/jour" },
    { label:"Poisson", img:"/poisson.png", couleur:"#0288d1", bg:"#e1f5fe",
      score: nutrition.poisson||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Tu atteins les 2 fois/semaine recommandées ✓":"Rarement consommé — objectif : 2 fois/semaine" },
    { label:"Légumineuses", img:"/legumesec.png", couleur:"#795548", bg:"#efebe9",
      score: nutrition.legumineuses||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Tu atteins les 2 fois/semaine recommandées ✓":"Peu consommé — objectif : 2 fois/semaine" },
    { label:"Féculents complets", img:"/feculent.png", couleur:"#f57c00", bg:"#fff3e0",
      score: nutrition.feculents||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"Bonne consommation à chaque repas ✓":"Objectif : féculents complets à chaque repas" },
    { label:"Produits laitiers", img:"/lait2.png", couleur:"#1976d2", bg:"#e3f2fd",
      score: nutrition.laitiers||0,
      attendu:60, inverted:false,
      desc:(s)=> s>=60?"2 portions/jour atteintes ✓":"Objectif : 2 produits laitiers par jour" },
    { label:"Charcuterie & fast food", img:"/charcuterie.png", couleur:"#e53935", bg:"#fbe9e7",
      score: Math.round(((nutrition.charcuterie||0)+(nutrition.fastFood||0))/2),
      attendu:20, inverted:true,
      desc:(s)=> s<=20?"Très bien — tu limites ces aliments ✓":s<=50?"Consommation modérée — essaie de réduire":"Trop fréquent — max 150g charcuterie/sem (OMS)" },
  ];

  const augmenter = CATEGORIES.filter(c => !c.inverted && c.score < c.attendu);
  const atteint   = CATEGORIES.filter(c => c.inverted ? c.score <= c.attendu : c.score >= c.attendu);
  const reduire   = CATEGORIES.filter(c => c.inverted && c.score > c.attendu);
  const nbOK = atteint.length;
  const total = CATEGORIES.length;

  const MiniCard = ({ cat }) => {
    const pct    = cat.inverted ? Math.max(0, 100-cat.score) : Math.min(cat.score, 100);
    const attPct = cat.inverted ? 100-cat.attendu : cat.attendu;
    return (
      <div style={{ background:cat.bg, borderRadius:12, padding:"12px 14px", border:`2px solid ${cat.couleur}44`, marginBottom:8 }}>
        <div style={{ display:"flex", alignItems:"center", gap:10, marginBottom:8 }}>
          <img src={cat.img} alt={cat.label} style={{ width:36, height:36, objectFit:"contain", flexShrink:0 }} />
          <div>
            <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A" }}>{cat.label}</div>
            <div style={{ fontSize:11, color:"#555", marginTop:2, lineHeight:1.4 }}>{cat.desc(cat.score)}</div>
          </div>
        </div>
        <div style={{ position:"relative", height:8, background:"rgba(0,0,0,0.1)", borderRadius:99 }}>
          <div style={{ position:"absolute", left:0, top:0, height:"100%", width:`${pct}%`, background:cat.couleur, borderRadius:99 }} />
          <div style={{ position:"absolute", top:-4, left:`${attPct}%`, transform:"translateX(-50%)", width:3, height:16, background:"#222", borderRadius:2, zIndex:2 }} />
        </div>
        <div style={{ display:"flex", justifyContent:"space-between", fontSize:10, marginTop:4 }}>
          <span style={{ color:cat.couleur, fontWeight:800 }}>Ta consommation</span>
          <span style={{ color:"#555", fontWeight:700 }}>│ Objectif PNNS</span>
        </div>
      </div>
    );
  };

  const ColTitle = ({ emoji, label, color }) => (
    <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:14, paddingBottom:10, borderBottom:`2px solid ${color}44` }}>
      <span style={{ fontSize:18 }}>{emoji}</span>
      <span style={{ fontSize:12, fontWeight:900, color:color, textTransform:"uppercase", letterSpacing:"0.5px" }}>{label}</span>
    </div>
  );

  return (
    <div style={{ position:"fixed", inset:0, background:"#f5f5f5", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header saumon pleine largeur */}
      <div style={{ background:"#FA8072", padding:"20px 32px 22px" }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.25)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:10, color:"white", fontSize:13, fontWeight:800, cursor:"pointer", padding:"6px 14px", marginBottom:14 }}>← Retour</button>
        <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>Bilan alimentaire · QCM Habitudes</div>
        <div style={{ fontSize:26, fontWeight:900, color:"white", marginBottom:4 }}>Bonjour {playerName} 👋</div>
        <div style={{ fontSize:14, color:"rgba(255,255,255,0.9)" }}>Voici tes résultats personnalisés basés sur tes réponses</div>
      </div>

      {/* Bandeau score global */}
      <div style={{ background:"white", borderBottom:"2px solid #eee", padding:"16px 32px", display:"flex", alignItems:"center", gap:20 }}>
        <div style={{ textAlign:"center", flexShrink:0 }}>
          <div style={{ fontSize:36, fontWeight:900, lineHeight:1, color: nbOK>=total*0.8?"#2e7d32":nbOK>=total*0.5?"#f57c00":"#e53935" }}>
            {nbOK}<span style={{ fontSize:18, color:"#999" }}>/{total}</span>
          </div>
          <div style={{ fontSize:11, color:"#888", fontWeight:700, marginTop:2 }}>groupes atteints</div>
        </div>
        <div style={{ width:2, height:52, background:"#eee", flexShrink:0 }} />
        <div>
          <div style={{ fontSize:15, fontWeight:900, color:"#1A1A1A", marginBottom:4 }}>
            {nbOK} groupe{nbOK>1?"s":""} sur {total} atteignent l'objectif PNNS
          </div>
          <div style={{ fontSize:12, color:"#666", lineHeight:1.6 }}>
            Le PNNS fixe des objectifs de consommation pour chaque groupe alimentaire. Le trait noir sur chaque barre indique l'objectif à atteindre.
          </div>
        </div>
      </div>

      {/* 3 colonnes pleine largeur */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:0, background:"white", borderBottom:"2px solid #eee" }}>

        <div style={{ padding:"20px 24px", borderRight:"2px solid #eee" }}>
          <ColTitle emoji="📈" label="À augmenter" color="#2e7d32" />
          {augmenter.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Aucun groupe à augmenter — bravo !</div>
            : augmenter.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

        <div style={{ padding:"20px 24px", borderRight:"2px solid #eee" }}>
          <ColTitle emoji="✅" label="Objectif atteint" color="#0288d1" />
          {atteint.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Continue tes efforts !</div>
            : atteint.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

        <div style={{ padding:"20px 24px" }}>
          <ColTitle emoji="⬇️" label="À réduire" color="#e53935" />
          {reduire.length===0
            ? <div style={{ fontSize:12, color:"#888", fontStyle:"italic", padding:"10px 0" }}>Rien à réduire — excellent !</div>
            : reduire.map(c => <MiniCard key={c.label} cat={c} />)
          }
        </div>

      </div>

      {/* Encart PNNS */}
      <div style={{ background:"#fff8f0", padding:"16px 32px", borderBottom:"2px solid #eee" }}>
        <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"1px", marginBottom:6 }}>Ce que dit le PNNS</div>
        <div style={{ fontSize:13, color:"#444", lineHeight:1.7 }}>
          Le Programme National Nutrition Santé recommande <strong>5 portions de fruits et légumes par jour</strong>, <strong>2 portions de poisson par semaine</strong> dont 1 poisson gras, et de <strong>limiter la charcuterie à 150g/semaine</strong> maximum (classée cancérigène groupe 1 par l'OMS).
        </div>
      </div>

      {/* Boutons */}
      <div style={{ padding:"20px 32px 32px", background:"white", display:"flex", gap:14 }}>
        <button onClick={onVoirRecos}
          style={{ flex:1, background:"#FA8072", border:"none", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"16px", cursor:"pointer", boxShadow:"0 4px 16px rgba(250,128,114,0.4)" }}>
          Voir mes recommandations PNNS →
        </button>

      </div>

    </div>
  );
}

/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */
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

/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */
function RecommandationsQcm2Screen({ answers, playerName, avatarChoice, onBack, onMinijeu }) {
  const [onglet, setOnglet] = useState("pour_vous");
  const [dateDebut, setDateDebut] = useState("");
  const [dateFin, setDateFin] = useState("");
  const [planning, setPlanning] = useState(null);

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
    if (r.type === "Dessert" || r.type === "Dessert simple" || r.type === "Dessert gourmands") return false;
    if (r.profils && r.profils.includes("dessert") && !r.profils.includes("plat")) return false;
    if (sansPorc    && r.profils && r.profils.includes("porc")) return false;
    if (sansViande  && r.profils && r.profils.includes("viande")) return false;
    if (pasTemps    && r.temps > 20) return false;
    return true;
  });

  const desserts = toutes.filter(r =>
    r.type === "Dessert" || r.type === "Dessert simple" || r.type === "Dessert gourmands" ||
    (r.profils && r.profils.includes("dessert"))
  );

  const pourVous = filtrees.length > 0 ? filtrees : toutes.filter(r => r.type !== "Dessert" && r.type !== "Dessert simple" && r.type !== "Dessert gourmands");

  const PETITSDEJ = [
    "Yaourt + fruit frais + pain complet",
    "Flocons d'avoine + lait + banane",
    "Pain complet + fromage blanc + fruit",
    "Smoothie fruits + pain complet",
    "Oeuf à la coque + tartine complète + jus d'orange",
    "Müesli + lait végétal + fraises",
    "Pancakes complets + compote de pommes",
  ];
  const DESSERTS_DEFAUT = [
    "Compote de pommes", "Yaourt au fruit", "Salade de fruits",
    "Carré de chocolat noir + noix", "Fromage blanc + miel",
    "Fruit de saison", "Crème dessert maison",
  ];

  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;
    const start = new Date(dateDebut);
    const end   = new Date(dateFin);
    const jours = [];
    const noms  = ["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"];
    const mois  = ["jan","fév","mar","avr","mai","juin","juil","aoû","sep","oct","nov","déc"];

    // Mélange aléatoire des recettes pour varier chaque jour
    const shuffle = (arr) => {
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    };

    // Plats de secours si pas assez de recettes
    const DEJEUNERS_DEFAUT = ["Salade composée", "Quiche légumes", "Soupe + pain complet", "Riz sauté légumes", "Omelette champignons", "Taboulé maison", "Wrap thon crudités"];
    const DINERS_DEFAUT    = ["Soupe + tartines", "Lentilles vapeur", "Oeufs cocotte", "Poêlée légumes", "Purée + poisson", "Velouté carottes", "Ratatouille + riz"];

    const recsMelangees = shuffle(pourVous);
    let cur = new Date(start);
    let idx = 0;

    while (cur <= end && jours.length < 14) {
      const recDej = recsMelangees[idx % recsMelangees.length];
      const recDin = recsMelangees[(idx + Math.ceil(recsMelangees.length / 2)) % recsMelangees.length];
      const dejLabel = recDej?.titre || recDej?.name;
      const dinLabel = recDin?.titre || recDin?.name;
      const dejNom = dejLabel !== dinLabel ? dejLabel : DEJEUNERS_DEFAUT[idx % DEJEUNERS_DEFAUT.length];
      const dinNom = dinLabel || DINERS_DEFAUT[idx % DINERS_DEFAUT.length];
      const dessertRec = desserts[idx % (desserts.length || 1)];
      const dessertNom = dessertRec?.titre || dessertRec?.name || DESSERTS_DEFAUT[idx % DESSERTS_DEFAUT.length];
      jours.push({
        nom:     noms[cur.getDay()],
        date:    `${cur.getDate()} ${mois[cur.getMonth()]}`,
        petitdej: PETITSDEJ[idx % PETITSDEJ.length],
        dej:     dejNom,
        din:     dinNom !== dejNom ? dinNom : DINERS_DEFAUT[idx % DINERS_DEFAUT.length],
        dessert: dessertNom,
      });
      cur.setDate(cur.getDate() + 1);
      idx++;
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
                      { emoji:"🌅", repas:"Petit-déjeuner", plat:j.petitdej || "Yaourt + fruit + pain complet" },
                      { emoji:"☀️", repas:"Déjeuner",       plat:j.dej },
                      { emoji:"🌙", repas:"Dîner",          plat:j.din },
                      { emoji:"🍮", repas:"Dessert",         plat:j.dessert },
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

          {/* Bouton Max → mini-jeu */}
          <div style={{ marginTop:32, background:"white", borderRadius:20, padding:"24px 28px", border:"3px solid #222", boxShadow:"5px 5px 0 #222" }}>
            <div style={{ display:"flex", alignItems:"center", gap:16, marginBottom:16 }}>
              <img src="/e.png" alt="Max" style={{ height:100, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
              <div style={{ background:"#fff8f0", border:"2px solid #FA8072", borderRadius:"14px 14px 14px 4px", padding:"14px 16px", flex:1 }}>
                <div style={{ fontSize:11, fontWeight:900, color:"#c4622d", textTransform:"uppercase", letterSpacing:"0.1em", marginBottom:6 }}>Max</div>
                <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
                  {"Tu as tout ce qu'il faut ! Viens maintenant composer ton assiette idéale dans le mini-jeu 🎮"}
                </div>
              </div>
            </div>
            <button onClick={() => onMinijeu && onMinijeu()}
              style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:14, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"14px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
              🥗 Composer mon assiette →
            </button>
          </div>

        </div>
      )}

    </div>
  );
}



/* ══ COMPOSANT INGRÉDIENTS AVEC PORTIONS ══ */
/* ══ COMPOSANT INGRÉDIENTS AVEC PORTIONS ══ */
function IngredientsBlock({ ingredients }) {
  const [portions, setPortions] = useState(4);
  const base = 4;

  const parseIng = (ing) => {
    const m = ing.match(/^([\d]+(?:[.,][\d]+)?)\s*([a-zA-Zàâéèêëîïôùûüç]+(?:\s?à\s?[a-zA-Z]+)?)?\s+(.+)$/);
    if (m) return { qty: parseFloat(m[1].replace(',','.')), unit: m[2]||'', name: m[3] };
    return { qty: null, unit: '', name: ing };
  };

  const fmt = (qty) => {
    const v = qty * (portions / base);
    return v === Math.round(v) ? String(Math.round(v)) : v.toFixed(1);
  };

  return (
    <div style={{ margin:"24px 0 0", background:"white", borderRadius:20, padding:"28px 24px", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>
      <h2 style={{ fontSize:22, fontWeight:900, color:"#1A1A1A", textAlign:"center", margin:"0 0 24px" }}>
        <span style={{ background:"#FFD6D0", borderRadius:8, padding:"2px 16px" }}>Ingrédients</span>
      </h2>
      <div style={{ display:"flex", alignItems:"center", justifyContent:"center", gap:20, marginBottom:28 }}>
        <button onClick={() => setPortions(p => Math.max(1, p-1))}
          style={{ width:42, height:42, borderRadius:"50%", background:"#E8534A", border:"none", color:"white", fontSize:24, fontWeight:900, cursor:"pointer", boxShadow:"0 2px 8px rgba(232,83,74,0.35)", display:"flex", alignItems:"center", justifyContent:"center" }}>−</button>
        <span style={{ fontSize:17, fontWeight:800, color:"#1A1A1A", minWidth:130, textAlign:"center" }}>{portions} personne{portions > 1 ? "s" : ""}</span>
        <button onClick={() => setPortions(p => p+1)}
          style={{ width:42, height:42, borderRadius:"50%", background:"#E8534A", border:"none", color:"white", fontSize:24, fontWeight:900, cursor:"pointer", boxShadow:"0 2px 8px rgba(232,83,74,0.35)", display:"flex", alignItems:"center", justifyContent:"center" }}>+</button>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"0 28px" }}>
        {ingredients.map((ing, i) => {
          const p = parseIng(ing);
          return (
            <div key={i} style={{ display:"flex", justifyContent:"space-between", alignItems:"baseline", padding:"12px 0", borderBottom:"1px solid #F0F0F0" }}>
              <span style={{ fontSize:14, fontWeight:800, color:"#1A1A1A" }}>{p.qty ? p.name : ing}</span>
              <span style={{ fontSize:13, color:"#6B7280", textAlign:"right", paddingLeft:8, flexShrink:0 }}>
                {p.qty ? `${fmt(p.qty)}${p.unit ? " "+p.unit : ""}` : ""}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ══ ÉCRAN RECETTES ══ */
function RecettesScreen({ onBack, cuisineChoice, filtreProfilInitial }) {
  const [selectedCat, setSelectedCat] = useState("Tout");
  const [selectedTag, setSelectedTag] = useState("Tout");
  const [openRecette, setOpenRecette] = useState(null);
  const [filtreProfil, setFiltreProfil] = useState(filtreProfilInitial || null);
  const [search, setSearch] = useState("");

  const catColors = {
    "Tartines":"#ffb892", "Salades":"#82b985",
    "Plats rapides":"#91bff4", "Plats mijotés":"#cc8ef2", "Dessert" : "#e2849a"
  };
  const catIcons = {
    "Tartines":"", "Salades":"",
    "Plats rapides":"", "Plats mijotés":"", "Dessert" :"",
  };

  const filtered = RECETTES_DATA.filter(r => {
    if (selectedCat !== "Tout" && r.categorie !== selectedCat) return false;
    if (selectedTag !== "Tout" && r.tag !== selectedTag) return false;
    if (filtreProfil && !(r.profils && r.profils.includes(filtreProfil))) return false;
    if (search && !r.titre.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  /* ─── VUE DÉTAIL ─── */
  if (openRecette) {
    const r = openRecette;
    const col = catColors[r.categorie] || "#1A3A5C";
    return (
      <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"'Segoe UI', Arial, sans-serif", overflowY:"auto" }}>
        {/* Barre navigation */}
        <div style={{ position:"sticky", top:0, zIndex:10, background:"white", borderBottom:"1px solid #E8EDF2", padding:"12px 20px", display:"flex", alignItems:"center", gap:12 }}>
          <button onClick={() => setOpenRecette(null)}
            style={{ display:"flex", alignItems:"center", gap:6, background:"none", border:"1px solid #E8EDF2", borderRadius:10, color:"#1A3A5C", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>
            ← Toutes les recettes
          </button>
          <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:8 }}>
            <span style={{ background:col+"18", color:col, borderRadius:20, padding:"4px 12px", fontSize:11, fontWeight:800, textTransform:"uppercase", letterSpacing:0.5 }}>{r.categorie}</span>
            <span style={{ background: r.tag==="Sans cuisson"?"#E0F7F5":"#FFF0EB", color: r.tag==="Sans cuisson"?"#00897B":"#E65100", borderRadius:20, padding:"4px 12px", fontSize:11, fontWeight:800 }}>{r.tag}</span>
          </div>
        </div>

        {/* Image hero */}
        {r.image ? (
          <div style={{ position:"relative", height:280, overflow:"hidden" }}>
            <img src={r.image} alt={r.titre}
              style={{ width:"100%", height:"100%", objectFit:"cover", display:"block" }} />
            <div style={{ position:"absolute", inset:0, background:"linear-gradient(to top, rgba(0,0,0,0.55) 0%, transparent 60%)" }} />
            <div style={{ position:"absolute", bottom:0, left:0, right:0, padding:"24px 24px 20px" }}>
              <h1 style={{ fontSize:26, fontWeight:900, color:"white", margin:0, lineHeight:1.3, textShadow:"0 1px 4px rgba(0,0,0,0.3)" }}>{r.titre}</h1>
            </div>
          </div>
        ) : (
          <div style={{ background:col, padding:"32px 24px 24px" }}>
            <h1 style={{ fontSize:26, fontWeight:900, color:"white", margin:0, lineHeight:1.3 }}>{r.titre}</h1>
          </div>
        )}

        <div style={{ maxWidth:680, margin:"0 auto", padding:"0 20px 40px" }}>
          {/* Stats strip */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:12, margin:"20px 0" }}>
            {[["⏱ Durée", r.temps, "#E0F7F5","#00897B"],["🛒 Ingrédients", r.ingredients.length+" items","#F3EEFF","#7C3AED"],["👨‍🍳 Étapes", r.etapes.length+" étapes","#FFF0EB","#E65100"]].map(([label,val,bg,col2])=>(
              <div key={label} style={{ background:bg, borderRadius:14, padding:"14px 16px", textAlign:"center" }}>
                <div style={{ fontSize:11, color:col2, fontWeight:800, textTransform:"uppercase", letterSpacing:0.5, marginBottom:4 }}>{label}</div>
                <div style={{ fontSize:16, fontWeight:900, color:col2 }}>{val}</div>
              </div>
            ))}
          </div>

          {/* Bénéfice */}
          <div style={{ background:"#E0F7F5", borderLeft:"4px solid #00BFA5", borderRadius:"0 12px 12px 0", padding:"14px 16px", marginBottom:20 }}>
            <div style={{ fontSize:11, fontWeight:800, color:"#00897B", textTransform:"uppercase", letterSpacing:1, marginBottom:4 }}>💡 Bénéfice nutritionnel</div>
            <p style={{ margin:0, fontSize:14, color:"#004D40", lineHeight:1.6 }}>{r.benefice}</p>
          </div>

          {/* Ingrédients */}
          <IngredientsBlock ingredients={r.ingredients} />

          {/* Étapes */}
          <div style={{ margin:"24px 0 0", background:"white", borderRadius:20, padding:"28px 24px", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", border:"1px solid #E8EDF2" }}>
            <h2 style={{ fontSize:22, fontWeight:900, color:"#1A1A1A", textAlign:"center", margin:"0 0 28px" }}>
              <span style={{ background:"#FFD6D0", borderRadius:8, padding:"2px 16px" }}>Étapes</span>
            </h2>
            {r.etapes.map((etape, i) => (
              <div key={i} style={{ display:"flex", gap:20, marginBottom: i < r.etapes.length-1 ? 24 : 0, alignItems:"flex-start" }}>
                <span style={{ fontSize:42, fontWeight:900, color:"#E8534A", lineHeight:1, minWidth:32, flexShrink:0 }}>{i+1}</span>
                <div style={{ width:3, borderRadius:4, background:"#FFD6D0", alignSelf:"stretch", flexShrink:0, marginTop:6 }} />
                <p style={{ margin:0, fontSize:15, color:"#1A1A1A", lineHeight:1.7, paddingTop:6 }}>{etape}</p>
              </div>
            ))}
          </div>

          {/* Lien source */}
          <div style={{ textAlign:"center", marginTop:24 }}>
            <a href={r.url} target="_blank" rel="noopener noreferrer"
              style={{ display:"inline-flex", alignItems:"center", gap:6, background:col, color:"white", borderRadius:12, padding:"12px 24px", fontSize:13, fontWeight:800, textDecoration:"none" }}>
              Voir sur {r.source} →
            </a>
          </div>
        </div>
      </div>
    );
  }

  /* ─── VUE LISTE ─── */
  return (
    <div style={{ position:"fixed", inset:0, background:"#F8FAFC", fontFamily:"'Segoe UI', Arial, sans-serif", overflowY:"auto" }}>

      {/* Header hero */}
      <div style={{ background:"#1A3A5C", padding:"0" }}>
        <div style={{ padding:"14px 20px", display:"flex", alignItems:"center", justifyContent:"space-between" }}>
          <button onClick={onBack}
            style={{ display:"flex", alignItems:"center", gap:6, background:"rgba(255,255,255,0.12)", border:"1px solid rgba(255,255,255,0.25)", borderRadius:10, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>
            ← Retour
          </button>
          <span style={{ fontSize:11, color:"rgba(255,255,255,0.5)", fontWeight:600, textTransform:"uppercase", letterSpacing:1 }}>mangerbouger.fr</span>
        </div>

        <div style={{ padding:"4px 20px 28px" }}>
          <div style={{ fontSize:11, fontWeight:800, color:"rgba(255,255,255,0.5)", textTransform:"uppercase", letterSpacing:2, marginBottom:8 }}>La Fabrique à Menus — PNNS</div>
          <h1 style={{ fontSize:30, fontWeight:900, color:"white", margin:"0 0 20px", lineHeight:1.15 }}>
            Recettes<br/>
            <span style={{ color:"#5DCAA5" }}>équilibrées</span>
          </h1>

          {/* Barre de recherche */}
          <div style={{ position:"relative" }}>
            <span style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", fontSize:16, opacity:0.5 }}>🔍</span>
            <input value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Rechercher une recette..."
              style={{ width:"100%", boxSizing:"border-box", background:"rgba(255,255,255,0.12)", border:"1px solid rgba(255,255,255,0.2)", borderRadius:12, padding:"12px 16px 12px 42px", fontSize:14, color:"white", outline:"none" }} />
          </div>

          {/* Stats */}
          {filtreProfil && (
            <div style={{ display:"inline-flex", alignItems:"center", gap:8, background:"rgba(255,255,255,0.15)", borderRadius:20, padding:"5px 14px", marginTop:14 }}>
              <span style={{ fontSize:12, color:"white", fontWeight:700 }}>Filtre : {filtreProfil}</span>
              <button onClick={() => setFiltreProfil(null)} style={{ background:"none", border:"none", color:"rgba(255,255,255,0.7)", cursor:"pointer", fontSize:14, fontWeight:900, padding:0 }}>✕</button>
            </div>
          )}
        </div>

        {/* Catégories scrollables */}
        <div style={{ display:"flex", gap:8, padding:"0 20px 0", overflowX:"auto", scrollbarWidth:"none", paddingBottom:0 }}>
          {["Tout", ...Object.keys(catIcons)].map(cat => (
            <button key={cat} onClick={() => setSelectedCat(cat)}
              style={{
                flexShrink:0, display:"flex", alignItems:"center", gap:6,
                background: selectedCat===cat ? "white" : "rgba(255,255,255,0.1)",
                color: selectedCat===cat ? (catColors[cat]||"#1A3A5C") : "rgba(255,255,255,0.8)",
                border: selectedCat===cat ? "none" : "1px solid rgba(255,255,255,0.2)",
                borderRadius:"20px 20px 0 0", padding:"9px 18px", fontSize:13, fontWeight:800, cursor:"pointer",
                transition:"all 0.15s"
              }}>
              {catIcons[cat] && <span style={{fontSize:14}}>{catIcons[cat]}</span>}
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Sous-filtres tags */}
      <div style={{ background:"white", borderBottom:"1px solid #E8EDF2", padding:"10px 20px", display:"flex", gap:8, alignItems:"center" }}>
        {["Tout","Sans cuisson","Cuisson rapide"].map(tag => (
          <button key={tag} onClick={() => setSelectedTag(tag)}
            style={{
              background: selectedTag===tag ? (tag==="Sans cuisson"?"#00BFA5":tag==="Cuisson rapide"?"#FF6B35":"#1A3A5C") : "transparent",
              color: selectedTag===tag ? "white" : "#6B7280",
              border: `1px solid ${selectedTag===tag ? "transparent" : "#E8EDF2"}`,
              borderRadius:20, padding:"5px 14px", fontSize:12, fontWeight:700, cursor:"pointer"
            }}>{tag}</button>
        ))}
        <span style={{ marginLeft:"auto", fontSize:12, color:"#9CA3AF", fontWeight:600 }}>{filtered.length} recette{filtered.length>1?"s":""}</span>
      </div>

      {/* Grille */}
      <div style={{ padding:"20px", display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(280px, 1fr))", gap:16, maxWidth:1200, margin:"0 auto" }}>
        {filtered.map(r => {
          const col = catColors[r.categorie] || "#1A3A5C";
          const icon = catIcons[r.categorie] || "🍽";
          const tagBg = r.tag==="Sans cuisson" ? "#E0F7F5" : "#FFF0EB";
          const tagCol = r.tag==="Sans cuisson" ? "#00897B" : "#E65100";
          return (
            <div key={r.id} onClick={() => setOpenRecette(r)}
              style={{ background:"white", borderRadius:20, overflow:"hidden", cursor:"pointer", border:"1px solid #E8EDF2", transition:"transform 0.18s, box-shadow 0.18s", boxShadow:"0 2px 10px rgba(26,58,92,0.05)" }}
              onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-5px)";e.currentTarget.style.boxShadow="0 12px 32px rgba(26,58,92,0.14)";}}
              onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="0 2px 10px rgba(26,58,92,0.05)";}}>

              {/* Image ou placeholder coloré */}
              {r.image ? (
                <div style={{ height:180, overflow:"hidden", position:"relative" }}>
                  <img src={r.image} alt={r.titre} style={{ width:"100%", height:"100%", objectFit:"cover", display:"block" }} />
                  <div style={{ position:"absolute", top:10, right:10, background:tagBg, color:tagCol, borderRadius:20, padding:"3px 10px", fontSize:10, fontWeight:800, textTransform:"uppercase", letterSpacing:0.5 }}>{r.tag}</div>
                </div>
              ) : (
                <div style={{ height:100, background:col, display:"flex", alignItems:"center", justifyContent:"center", position:"relative" }}>
                  <span style={{ fontSize:40, opacity:0.8 }}>{icon}</span>
                  <div style={{ position:"absolute", top:10, right:10, background:"rgba(255,255,255,0.25)", color:"white", borderRadius:20, padding:"3px 10px", fontSize:10, fontWeight:800, textTransform:"uppercase", letterSpacing:0.5 }}>{r.tag}</div>
                </div>
              )}

              {/* Contenu */}
              <div style={{ padding:"16px" }}>
                <div style={{ fontSize:15, fontWeight:800, color:"#1A1A1A", lineHeight:1.4, marginBottom:8 }}>{r.titre}</div>
                <div style={{ display:"flex", gap:6, marginBottom:10, flexWrap:"wrap" }}>
                  <span style={{ background:"#F1F5F9", borderRadius:8, padding:"4px 10px", fontSize:11, fontWeight:700, color:"#374151" }}>⏱ {r.temps}</span>
                  <span style={{ background:"#F1F5F9", borderRadius:8, padding:"4px 10px", fontSize:11, fontWeight:700, color:"#374151" }}>{r.type}</span>
                </div>
                <p style={{ margin:"0 0 14px", fontSize:13, color:"#6B7280", lineHeight:1.5 }}>{r.benefice}</p>
                <div style={{ background:col, borderRadius:10, padding:"10px 14px", textAlign:"center", color:"white", fontSize:13, fontWeight:800 }}>
                  Voir la recette →
                </div>
              </div>
            </div>
          );
        })}
        {filtered.length === 0 && (
          <div style={{ gridColumn:"1/-1", textAlign:"center", padding:"60px 20px", color:"#9CA3AF" }}>
            <div style={{ fontSize:48, marginBottom:12 }}>🔍</div>
            <div style={{ fontSize:16, fontWeight:700 }}>Aucune recette trouvée</div>
            <div style={{ fontSize:13, marginTop:6 }}>Essayez d'autres filtres</div>
          </div>
        )}
      </div>
    </div>
  );
}


/* ══ PAGE RÉCAP QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";
  const cuisine   = answers["‍ En cuisine"] || "—";
  const pratiques = answers[" Pratiques alimentaires"] || "—";
  const compo     = answers[" Composition du repas"] || "—";
  const nbPersons = answers[" Nombre de personnes"] || "—";
  const nbRepas   = answers[" Nombre de repas"] || "—";

  const LIGNES = [
    { icon:"👥", label:"Nombre de personnes",   val:nbPersons },
    { icon:"🥗", label:"Pratiques alimentaires", val:pratiques },
    { icon:"🍽️", label:"Composition du repas",  val:compo     },
    { icon:"⏱️", label:"Temps en cuisine",       val:cuisine   },
    { icon:"📅", label:"Repas par jour",          val:nbRepas   },
  ];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"16px 24px", textAlign:"center", flexShrink:0, position:"relative" }}>
        <button onClick={onBack} style={{ position:"absolute", left:16, top:"50%", transform:"translateY(-50%)", background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:13, fontWeight:700, cursor:"pointer", padding:"6px 14px" }}>← Retour</button>
        <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"white" }}>⭐ Profil créé ! ⭐</div>
        <div style={{ fontSize:13, color:"rgba(255,255,255,0.85)", marginTop:3 }}>Voici ton profil alimentaire personnalisé</div>
      </div>

      {/* Personnages en haut — GRANDS */}
      <div style={{ background:"#fff8f0", borderBottom:"2px solid #eee", padding:"20px 60px 0", display:"flex", justifyContent:"space-around", alignItems:"flex-end", flexShrink:0 }}>

        {/* Max */}
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:10 }}>
          <img src="/e.png" alt="Max" style={{ height:220, objectFit:"contain", filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"#e8f5e9", border:"2px solid #9ACD32", borderRadius:"14px 14px 14px 4px", padding:"12px 16px", fontSize:13, color:"#27500A", lineHeight:1.6, textAlign:"center", maxWidth:200 }}>
            Wow ! Tu viens de compléter ton profil alimentaire ! Regardons ensemble tes habitudes. 🌟
          </div>
          <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#FA8072", background:"#fff0ee", padding:"4px 14px", borderRadius:20, border:"1.5px solid #FA807244", marginBottom:6 }}>Max</span>
        </div>

        {/* Avatar */}
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:10 }}>
          <img src={avatarSrc} alt={playerName} style={{ height:190, objectFit:"contain", filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"white", border:"2px solid #1976d2", borderRadius:"14px 14px 4px 14px", padding:"12px 16px", fontSize:13, color:"#0C447C", lineHeight:1.6, textAlign:"center", maxWidth:190 }}>
            D'accord Max, j'ai hâte de voir ! 👀
          </div>
          <span style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, color:"#1976d2", background:"#e3f2fd", padding:"4px 14px", borderRadius:20, border:"1.5px solid #1976d244", marginBottom:6 }}>{playerName}</span>
        </div>

      </div>

      {/* Récap */}
      <div style={{ flex:1, padding:"18px 24px", overflowY:"auto" }}>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12, marginBottom:14 }}>
          {LIGNES.map((l, i) => (
            <div key={i} style={{ background:"white", borderRadius:14, padding:"14px 16px", border:"1.5px solid #eee", display:"flex", alignItems:"center", gap:12 }}>
              <span style={{ fontSize:28, flexShrink:0 }}>{l.icon}</span>
              <div style={{ minWidth:0 }}>
                <div style={{ fontSize:11, color:"#aaa", fontWeight:700, marginBottom:3, textTransform:"uppercase", letterSpacing:"0.5px" }}>{l.label}</div>
                <div style={{ fontSize:14, fontWeight:900, color:"#1A1A1A", fontFamily:"Arial Black, Arial, sans-serif" }}>{l.val}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ background:"#fff8e1", borderRadius:12, padding:"12px 16px", fontSize:13, color:"#854F0B", marginBottom:16 }}>
          ⭐ Ton profil est unique, chaque petit pas compte pour ta santé !
        </div>

        <div style={{ display:"flex", justifyContent:"flex-end" }}>
          <button onClick={onSuivant}
            style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:10, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, padding:"10px 24px", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>
            Suivant →
          </button>
        </div>
      </div>

    </div>
  );
}


/* ══ PAGE AU PROGRAMME (post-QCM2) ══ */
function AuProgrammeScreen({ playerName, avatarChoice, onRecos, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";

  const STEPS = ["QCM 1", "QCM 2", "Profil", "Recos", "Recettes"];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"16px 24px", display:"flex", alignItems:"center", gap:16 }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px", flexShrink:0 }}>← Retour</button>
        <div style={{ flex:1 }}>
          <div style={{ fontSize:11, color:"rgba(255,255,255,0.8)", marginBottom:2 }}>Super travail ! 🎉</div>
          <div style={{ fontSize:14, fontWeight:700, color:"white", lineHeight:1.5 }}>
            Grâce à tes réponses, je peux te proposer des recommandations et des recettes 100% adaptées à toi !
          </div>
        </div>
        <img src={avatarSrc} alt="Avatar" style={{ width:60, filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
      </div>

      {/* Contenu */}
      <div style={{ padding:"24px 32px" }}>

        {/* Max + bulle */}
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, marginBottom:28 }}>
          <img src="/e.png" alt="Max" style={{ width:130, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
          <div style={{ background:"white", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.15)", flex:1 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:14, fontWeight:700, color:"#222", lineHeight:1.7 }}>
              Prêt(e) à découvrir tout ça ? 🌟<br/>
              <span style={{ fontSize:13, fontWeight:600, color:"#555" }}>Tes recommandations et recettes sont personnalisées en fonction de tes habitudes alimentaires, tes préférences et ton profil.</span>
            </div>
          </div>
        </div>

        {/* Titre */}
        <div style={{ textAlign:"center", marginBottom:20 }}>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 rgba(0,0,0,0.08)" }}>Au programme :</div>
        </div>

        {/* 2 cartes */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:20 }}>
          <div style={{ background:"white", border:"2px solid #9ACD3266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#e8f5e9", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center" }}>
              <i className="ti ti-clipboard-list" style={{ fontSize:28, color:"#9ACD32" }} />
            </div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#639922", marginBottom:6 }}>Recommandations personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil alimentaire</div>
          </div>
          <div style={{ background:"white", border:"2px solid #FA807266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#fff0ee", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center" }}>
              <i className="ti ti-salad" style={{ fontSize:28, color:"#FA8072" }} />
            </div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#c4622d", marginBottom:6 }}>Recettes personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
          </div>
        </div>

        {/* Bouton principal */}
        <button onClick={onRecos}
          style={{ width:"100%", background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"4px 4px 0 #222", marginBottom:24 }}>
          Clique ici pour découvrir tes recommandations et recettes ! 🍽️
        </button>

        {/* Barre progression mission */}
        <div style={{ background:"white", borderRadius:14, padding:"12px 20px", border:"1.5px solid #eee", display:"flex", alignItems:"center", gap:12 }}>
          <span style={{ fontSize:20 }}>🏆</span>
          <div>
            <div style={{ fontSize:11, fontWeight:900, color:"#c4622d" }}>Mission accomplie</div>
            <div style={{ fontSize:10, color:"#888" }}>Ton aventure continue...</div>
          </div>
          <div style={{ flex:1, display:"flex", alignItems:"center", justifyContent:"flex-end", gap:4 }}>
            {STEPS.map((s, i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:3 }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:2 }}>
                  <div style={{ width:22, height:22, borderRadius:"50%", background:i<3?"#9ACD32":i===3?"#FA8072":"#eee", border:"2px solid " + (i<3?"#639922":i===3?"#c4622d":"#ddd"), display:"flex", alignItems:"center", justifyContent:"center" }}>
                    {i < 2 ? <i className="ti ti-check" style={{ fontSize:11, color:"white" }} /> : <div style={{ width:6, height:6, borderRadius:"50%", background:i===2?"white":i===3?"white":"#ccc" }} />}
                  </div>
                  <div style={{ fontSize:8, color:"#888", whiteSpace:"nowrap" }}>{s}</div>
                </div>
                {i < STEPS.length - 1 && <div style={{ width:12, height:1.5, background:"#ddd", marginBottom:10 }} />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══ PAGE AU PROGRAMME QCM2 ══ */
function IntroRecosQcm2Screen({ answers, playerName, avatarChoice, onBack, onVoirRecos, onVoirRecettes }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";
  const STEPS = ["QCM 1", "QCM 2", "Profil", "Recos", "Recettes"];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"16px 24px", display:"flex", alignItems:"center", gap:16 }}>
        <button onClick={onBack} style={{ background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px", flexShrink:0 }}>← Retour</button>
        <div style={{ flex:1 }}>
          <div style={{ fontSize:11, color:"rgba(255,255,255,0.8)", marginBottom:2 }}>Super travail ! 🎉</div>
          <div style={{ fontSize:14, fontWeight:700, color:"white", lineHeight:1.5 }}>
            Grâce à tes réponses, je peux te proposer des recommandations et des recettes 100% adaptées à toi !
          </div>
        </div>
        <img src={avatarSrc} alt="Avatar" style={{ width:60, filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
      </div>

      {/* Contenu */}
      <div style={{ padding:"24px 32px" }}>

        {/* Max + bulle */}
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, marginBottom:28 }}>
          <img src="/e.png" alt="Max" style={{ width:130, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))", flexShrink:0 }} />
          <div style={{ background:"white", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.15)", flex:1 }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:14, fontWeight:700, color:"#222", lineHeight:1.7 }}>
              Prêt(e) à découvrir tout ça ? 🌟<br/>
              <span style={{ fontSize:13, fontWeight:600, color:"#555" }}>Tes recommandations et recettes sont personnalisées en fonction de tes habitudes alimentaires et tes préférences.</span>
            </div>
          </div>
        </div>

        {/* Titre */}
        <div style={{ textAlign:"center", marginBottom:20 }}>
          <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:22, fontWeight:900, color:"#FA8072", textShadow:"2px 2px 0 rgba(0,0,0,0.08)" }}>Au programme :</div>
        </div>

        {/* 2 cartes */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:20 }}>
          <div style={{ background:"white", border:"2px solid #9ACD3266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#e8f5e9", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center", fontSize:28 }}>📋</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#639922", marginBottom:6 }}>Recommandations personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des conseils nutritionnels adaptés à ton profil alimentaire</div>
          </div>
          <div style={{ background:"white", border:"2px solid #FA807266", borderRadius:18, padding:"20px", textAlign:"center" }}>
            <div style={{ width:56, height:56, borderRadius:"50%", background:"#fff0ee", margin:"0 auto 12px", display:"flex", alignItems:"center", justifyContent:"center", fontSize:28 }}>🍽️</div>
            <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:14, fontWeight:900, color:"#c4622d", marginBottom:6 }}>Recettes personnalisées</div>
            <div style={{ fontSize:12, color:"#888", lineHeight:1.5 }}>Des idées de recettes équilibrées rien que pour toi</div>
          </div>
        </div>

        {/* Bouton principal */}
        <button onClick={onVoirRecos}
          style={{ width:"100%", background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"18px", cursor:"pointer", boxShadow:"4px 4px 0 #222", marginBottom:24 }}>
          Clique ici pour découvrir tes recommandations et recettes ! 🍽️
        </button>

        {/* Barre progression mission */}
        <div style={{ background:"white", borderRadius:14, padding:"12px 20px", border:"1.5px solid #eee", display:"flex", alignItems:"center", gap:12 }}>
          <span style={{ fontSize:20 }}>🏆</span>
          <div>
            <div style={{ fontSize:11, fontWeight:900, color:"#c4622d" }}>Mission accomplie</div>
            <div style={{ fontSize:10, color:"#888" }}>Ton aventure continue...</div>
          </div>
          <div style={{ flex:1, display:"flex", alignItems:"center", justifyContent:"flex-end", gap:2 }}>
            {STEPS.map((s, i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:2 }}>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:2 }}>
                  <div style={{ width:22, height:22, borderRadius:"50%", background:i<3?"#9ACD32":i===3?"#FA8072":"#eee", border:"2px solid "+(i<3?"#639922":i===3?"#c4622d":"#ddd"), display:"flex", alignItems:"center", justifyContent:"center" }}>
                    {i < 2 ? <span style={{ fontSize:10, color:"white" }}>✓</span> : <div style={{ width:6, height:6, borderRadius:"50%", background:i===2?"white":i===3?"white":"#ccc" }} />}
                  </div>
                  <div style={{ fontSize:8, color:"#888", whiteSpace:"nowrap" }}>{s}</div>
                </div>
                {i < STEPS.length-1 && <div style={{ width:10, height:1.5, background:"#ddd", marginBottom:10 }} />}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══ SÉLECTION QCM ══ */
function QcmSelectScreen({ playerName, onStartQcm1, onStartQcm2, onStartMinijeu, onStartSante, mission4Unlocked, completedMissions = [], onDashboard }) {
  const [hovered, setHovered] = useState(null);
  const MISSIONS = [
    { id:0, label:"Habitudes alimentaires", sub:"17 questions · QCM", color:"#FA8072", top:"30%", left:"9%", action:onStartQcm1 },
    { id:1, label:"Fabrique à Menus", sub:"5 questions · QCM", color:"#ffcc00", top:"47%", left:"22%", action:onStartQcm2 },
    { id:2, label:"Compose ton assiette", sub:"Mini-jeu interactif", color:"#9ACD32", top:"68%", left:"53%", action:onStartMinijeu },
    { id:3, label:"Mon profil santé", sub:"QCM · Profil & pathologies", color:"#7C3AED", top:"25%", left:"65%", action:onStartSante },
  ];
  return (
    <div style={{ position:"fixed", inset:0, fontFamily:"Arial, sans-serif", overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0, backgroundImage:"url('/frigo.png')", backgroundSize:"cover", backgroundPosition:"center", backgroundRepeat:"no-repeat" }} />
      <div style={{ position:"absolute", bottom:24, left:0, right:0, zIndex:20, textAlign:"center" }}>
        {completedMissions.includes(3) ? (
          <button onClick={onDashboard}
            style={{ fontSize:18, fontWeight:900, fontFamily:"Arial Black, Arial, sans-serif", background:"#ffdd44", border:"3px solid #222", borderRadius:20, padding:"12px 32px", boxShadow:"5px 5px 0 #222", cursor:"pointer", color:"#222" }}>
            📊 Consulter le dashboard →
          </button>
        ) : (
          <span style={{ fontSize:25, color:"#e72222", fontWeight:800, background:"rgba(255,255,255,0.85)", borderRadius:20, padding:"8px 24px", boxShadow:"0 2px 10px rgba(0,0,0,0.15)" }}>
            Clique sur un point pour commencer ta mission !
          </span>
        )}
      </div>
      {MISSIONS.map((m) => {
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
              style={{ width:90, height:90, borderRadius:"50%", background: isLocked?"#bbb":m.color, border:"3px solid white", cursor:isLocked?"not-allowed":"pointer", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", fontSize:completedMissions.includes(m.id)?11:18, fontWeight:900, color:"white", boxShadow:`0 4px 16px ${isLocked?"#bbb":m.color}88`, transform: hovered===m.id && !isLocked ? "scale(1.2)" : "scale(1)", transition:"transform 0.2s", opacity:isLocked?0.5:1 }}>
              {isLocked ? "🔒" : completedMissions.includes(m.id) ? (
                <><div style={{ fontSize:20 }}>✓</div><div style={{ fontSize:10, letterSpacing:1 }}>★★★★★</div></>
              ) : m.id + 1}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ══ DONNÉES QCM 1 ══ */
const QUESTIONS = [
  { id:'legumes', icon:'legume.png', title:'Légumes frais', subtitle:'À quelle fréquence en consommez-vous ?\n(hors pommes de terre — une portion = 80-100g)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus','Ne sait pas'], nutKey:'legumes', nutMax:7, reaction:v=>v>=5?{face:'',text:'Excellent ! Tu es dans les recommandations.'}:v>=3?{face:'',text:"Pas mal ! L'OMS recommande 5 portions/jour."}:{face:'',text:"C'est peu ! Les légumes apportent vitamines et fibres."} },
  { id:'legumineuses', icon:'legumesec.png', title:'Légumes secs', subtitle:'À quelle fréquence en consommez-vous ?\n(lentilles, pois chiches, haricots secs…)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'legumineuses', nutMax:6, reaction:v=>v===0?{face:'',text:"Jamais ? Essaie les lentilles corail !"}:v<=2?{face:'',text:"C'est un début ! Le PNNS recommande 2 fois/sem."}:v<=4?{face:'',text:"Très bien ! Riches en fibres et protéines végétales."}:{face:'',text:"Champion des légumineuses !"} },
  { id:'feculents', icon:'feculent.png', title:'Féculents complets', subtitle:'À quelle fréquence en consommez-vous ?\n(pain complet, pâtes complètes, riz complet…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','Tous les jours','Ne sait pas'], nutKey:'feculents', nutMax:4, reaction:v=>v===0?{face:'',text:"Essaie le pain complet !"}:v<=3?{face:'',text:"Bien ! Riches en fibres."}:{face:'',text:"Excellent ! Tes apports en fibres sont optimaux !"} },
  { id:'fruits', icon:'fraise.png', title:'Fruits', subtitle:'À quelle fréquence en consommez-vous ?\n(hors jus — compotes comprises)', labels:['Jamais','1 fruit/sem ou moins','2 à 3 fruits/sem','4 à 6 fruits/sem','1 fruit/jour','2 fruits/jour','3 fruits/jour','4 fruits et plus','Ne sait pas'], nutKey:'fruits', nutMax:7, reaction:v=>v===0?{face:'',text:"Aucun fruit ? Vitamines et antioxydants essentiels !"}:v<=2?{face:'',text:"L'OMS recommande au moins 2-3 fruits/jour."}:v<=5?{face:'',text:"Bien ! Excellente source de vitamines."}:{face:'',text:"Parfait !"} },
  { id:'fruitsACoque', icon:'fruit_a_coque.png', title:'Fruits à coque', subtitle:'À quelle fréquence en mangez-vous ?\n(amandes, noix, noisettes…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','Au moins 1 portion/jour','Ne sait pas'], nutKey:'fruitsACoque', nutMax:4, reaction:v=>v===0?{face:'',text:"Riches en bons acides gras !"}:v<=2?{face:'',text:"Le PNNS recommande une petite poignée/jour."}:{face:'',text:"Excellent ! Protègent ton cœur."} },
  { id:'laitiers', icon:'lait.png', title:'Produits laitiers', subtitle:'À quelle fréquence en mangez-vous ?\n(lait, yaourt, fromage)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois/jour et plus','Ne sait pas'], nutKey:'laitiers', nutMax:7, reaction:v=>v===0?{face:'',text:"Pense aux autres sources de calcium."}:v<=3?{face:'',text:"Le PNNS recommande 2 produits laitiers/jour."}:v<=5?{face:'',text:"Bien ! Tes besoins en calcium sont couverts."}:{face:'',text:"Parfait !"} },
  { id:'volaille', icon:'volaille.png', title:'Volaille', subtitle:'À quelle fréquence en mangez-vous ?\n(poulet, dinde…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','1 portion/jour','2 portions et plus/jour','Ne sait pas'], nutKey:'volaille', nutMax:5, reaction:v=>v===0?{face:'',text:"Bonne source de protéines maigres."}:v<=3?{face:'',text:"Bien ! Protéines pauvres en graisses saturées."}:{face:'',text:"Attention à ne pas dépasser 500g/semaine."} },
  { id:'viande', icon:'viande.png', title:'Viande (hors volaille)', subtitle:'À quelle fréquence en mangez-vous ?\n(bœuf, porc, agneau…)', labels:['Jamais','1 portion/sem ou moins','2 à 3 portions/sem','4 à 6 portions/sem','1 portion/jour','2 portions et plus/jour','Ne sait pas'], nutKey:'viande', nutMax:5, reaction:v=>v===0?{face:'',text:"Excellent pour la santé cardiovasculaire !"}:v<=2?{face:'',text:"Bien ! Limite à 500g/semaine."}:v<=3?{face:'',text:"Attention : limite à 500g/semaine."}:{face:'',text:"Trop ! Risque accru de cancer colorectal."} },
  { id:'charcuterie', icon:'charcuterie.png', title:'Charcuterie', subtitle:'À quelle fréquence en mangez-vous ?\n(jambon, saucisson, saucisses…)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'charcuterie', nutMax:6, reaction:v=>v===0?{face:'',text:"Cancérigène classé par l'OMS — bien d'éviter !"}:v<=2?{face:'',text:"Bien ! Limite à 150g/semaine."}:v<=3?{face:'',text:"Riche en sel et graisses saturées."}:{face:'',text:"Trop ! Classe 1 cancérigène OMS."} },
  { id:'poisson', icon:'poisson.png', title:'Poisson & produits de la pêche', subtitle:'À quelle fréquence en consommez-vous ?\n(incluant les conserves)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois/sem et plus','Ne sait pas'], nutKey:'poisson', nutMax:6, reaction:v=>v===0?{face:'',text:"Oméga-3 essentiels pour le cerveau et le cœur !"}:v<=2?{face:'',text:"2 portions/semaine dont un poisson gras."}:v<=4?{face:'',text:"Bien ! Oméga-3 et protéines de qualité."}:{face:'',text:"Excellent !"} },
  { id:'oeufs', icon:'oeuf.png', title:'Œufs', subtitle:'À quelle fréquence en consommez-vous ?\n(une portion = 2 œufs)', labels:['Jamais','1 fois/mois ou moins','2 à 3 fois/mois','1 fois/sem','2 fois/sem','3 fois/sem','4 fois et plus/sem','Ne sait pas'], nutKey:'oeufs', nutMax:6, reaction:v=>v===0?{face:'',text:"Excellente source de protéines et vitamines B."}:v<=3?{face:'',text:"Bien ! Protéines de haute qualité."}:{face:'',text:"Diversifie aussi tes sources de protéines."} },
  { id:'snacks', icon:'snack.png', title:'Snacks salés', subtitle:'À quelle fréquence en mangez-vous ?\n(chips, biscuits apéritifs…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'snacks', nutMax:7, reaction:v=>v===0?{face:'',text:"Zéro snack ! Sel et graisses saturées évités."}:v<=2?{face:'',text:"Raisonnable ! Des plaisirs occasionnels."}:v<=4?{face:'',text:"Riches en sel et graisses."}:{face:'',text:"Trop ! Risques d'hypertension."} },
  { id:'fastFood', icon:'fast_food.png', title:'Fast food', subtitle:'À quelle fréquence en mangez-vous ?\n(hamburgers, kebabs, pizzas…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'fastFood', nutMax:7, reaction:v=>v===0?{face:'',text:"Zéro fast food ! Ultra-transformés évités."}:v<=2?{face:'',text:"Occasionnellement OK."}:v<=4?{face:'',text:"Très caloriques, riches en sel."}:{face:'',text:"Trop ! Liés à l'obésité."} },
  { id:'sucres', icon:'sucrerie.png', title:'Sucreries & desserts', subtitle:'À quelle fréquence en mangez-vous ?\n(gâteaux, viennoiseries, glaces…)', labels:['Jamais','1 fois/sem ou moins','2 à 3 fois/sem','4 à 6 fois/sem','1 fois/jour','2 fois/jour','3 fois/jour','4 fois et plus/jour','Ne sait pas'], nutKey:'sucres', nutMax:7, reaction:v=>v===0?{face:'',text:"Zéro sucrerie ! Sucres ajoutés évités."}:v<=2?{face:'',text:"Raisonnable !"}:v<=4?{face:'',text:"Riches en sucres ajoutés."}:{face:'',text:"Trop ! Diabète et caries."} },
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
function Qcm1Screen({ onBack, playerName, playerInfos, onDone, onShowRecos }) {
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [nutrition, setNutrition] = useState({});
  const [stars, setStars] = useState(0);
  const [card, setCard] = useState("slider");
  const [sliderVal, setSliderVal] = useState(4);
  const [selectedTile, setSelectedTile] = useState(-1);
  const [selectedRadio, setSelectedRadio] = useState(-1);
  const [selectedAccord, setSelectedAccord] = useState(null);
  const [checkedRaisons, setCheckedRaisons] = useState([]);

  const displayQ = card==="slider"?(currentQ===QUESTIONS.length-1?15:currentQ+1):card==="tiles"?14:card==="radio"?16:card==="accord"?17:18;
  const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const [history, setHistory] = useState([]);

  const goBack = () => {
    if (history.length === 0) return;
    const prev = history[history.length - 1];
    setHistory(h => h.slice(0, -1));
    setCard(prev.card);
    setCurrentQ(prev.currentQ);
    setSliderVal(prev.sliderVal);
    setAnswers(prev.answers);
    setNutrition(prev.nutrition);
    setStars(prev.stars);
    setSelectedTile(prev.selectedTile ?? -1);
    setSelectedRadio(prev.selectedRadio ?? -1);
    setSelectedAccord(prev.selectedAccord ?? null);
    setCheckedRaisons(prev.checkedRaisons ?? []);
  };

  const saveHistory = () => {
    setHistory(h => [...h, { card, currentQ, sliderVal, answers: [...answers], nutrition: {...nutrition}, stars, selectedTile, selectedRadio, selectedAccord, checkedRaisons: [...checkedRaisons] }]);
  };
  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:1500, width:"100%", textAlign:"center", border:"3px solid #222", boxShadow:"5px 5px 0 #222" };

  const addAnswer = (id, val, label, nutKey, nutMax) => {
    const nut = nutKey ? Math.min(Math.round(val / nutMax * 100), 100) : 0;
    setNutrition(prev => ({ ...prev, [nutKey || id]: nut }));
    setAnswers(prev => [...prev, { id, value: val, label }]);
    setStars(s => s + 1);
  };

  const nextSlider = () => {
    saveHistory();
    playSound("good");
    const q = QUESTIONS[currentQ];
    addAnswer(q.id, sliderVal, q.labels[sliderVal], q.nutKey, q.nutMax);
    if (currentQ === QUESTIONS.length - 2) { setCard("tiles"); setSelectedTile(-1); }
    else if (currentQ === QUESTIONS.length - 1) { setCard("radio"); setSelectedRadio(-1); }
    else { setCurrentQ(c => c + 1); setSliderVal(Math.floor((QUESTIONS[currentQ + 1].labels.length - 1) / 2)); }
  };

  const nextTiles = () => {
    saveHistory();
    playSound("good");
    if (selectedTile === -1) return;
    addAnswer('boissons', selectedTile, BOISSONS_LABELS[selectedTile], 'boissons', BOISSONS_LABELS.length - 2);
    setCurrentQ(QUESTIONS.length - 1);
    setSliderVal(Math.floor((QUESTIONS[QUESTIONS.length - 1].labels.length - 1) / 2));
    setCard("slider");
  };

  const nextRadio = () => {
    saveHistory();
    playSound("good");
    if (selectedRadio === -1) return;
    addAnswer('bio', selectedRadio, BIO_LABELS[selectedRadio], 'bio', 3);
    setCard("accord"); setSelectedAccord(null);
  };

  const nextAccord = () => {
    saveHistory();
    playSound("good");
    if (selectedAccord === null) return;
    const label = selectedAccord === "oui" ? "Oui" : VIANDE_OPTIONS[selectedAccord]?.label || "";
    const score = selectedAccord === "oui" ? 100 : VIANDE_OPTIONS[selectedAccord]?.score || 0;
    addAnswer('reductionViande', selectedAccord, label, 'reductionViande', 100);
    setNutrition(prev => ({ ...prev, reductionViande: score }));
    if (selectedAccord === "oui") { setCard("check"); setCheckedRaisons([]); }
    else { setCard("result"); }
  };

  const nextCheck = () => {
    saveHistory();
    playSound("badge");
    if (checkedRaisons.length === 0) return;
    addAnswer('raisonsViande', checkedRaisons, checkedRaisons.map(i => RAISONS_LABELS[i]).join(' | '), null, 0);
    setCard("result");
  };

  const q = QUESTIONS[currentQ] || QUESTIONS[0];
  const labels = q.labels;

  if (card === "result") {
    const vals = Object.values(nutrition);
    const avg = vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
    let emoji = '', title = 'Ton bilan', sub = '';
    if (avg >= 70) { emoji = ''; title = 'Excellente alimentation !'; sub = 'Tes habitudes sont vraiment exemplaires !'; }
    else if (avg >= 40) { emoji = ''; title = 'Pas mal du tout !'; sub = 'Quelques points à améliorer, mais tu es sur la bonne voie.'; }
    else { emoji = ''; title = 'Des progrès à faire !'; sub = 'Chaque petit changement compte.'; }
    const weakKey = Object.entries(nutrition).sort((a,b)=>a[1]-b[1])[0]?.[0];
    const weakQ = QUESTIONS.find(x=>x.nutKey===weakKey);
    const conseil = weakQ ? weakQ.reaction(0).text : 'Continue comme ça !';
    saveGame({ type:"qcm1", data: { answers, nutrition, patient: { prenom: playerName, ...(playerInfos||{}) } } });
    if (onDone) onDone(nutrition);
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
            const ico = p >= 60 ? '' : p >= 30 ? '⚠️' : '';
            const r = qq ? qq.reaction(a.value) : { face: '', text: a.label };
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
          <button onClick={() => { if(onShowRecos) onShowRecos(nutrition); }} style={{ ...btn, background:"#2e7d32", color:"white", border:"3px solid #1b5e20" }}> Mes recommandations PNNS →</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('fond_orange.png')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"80px 16px 40px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgb(255, 255, 255)" }} />
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white", textShadow:"1px 1px 0 #222" }}>Question {displayQ} / 17</div>
        <div style={{ fontSize:19, fontWeight:"bold", color:"#ffcc00", textShadow:"1px 1px 0 #222" }}> {stars}</div>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginTop:20 }}>
            {history.length > 0 ? <button onClick={goBack} style={{ ...btn, background:"white" }}>← Retour</button> : <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>}
            <button onClick={nextSlider} style={btn}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
           <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            {history.length > 0 ? <button onClick={goBack} style={{ ...btn, background:"white" }}>← Retour</button> : <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>}
            <button onClick={nextTiles} style={{ ...btn, opacity:selectedTile===-1?0.4:1, pointerEvents:selectedTile===-1?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
<button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            {history.length > 0 ? <button onClick={goBack} style={{ ...btn, background:"white" }}>← Retour</button> : <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>}
            <button onClick={nextRadio} style={{ ...btn, opacity:selectedRadio===-1?0.4:1, pointerEvents:selectedRadio===-1?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
              <span style={{ fontSize:20 }}></span> Oui
            </div>
            <div style={{ border:"3px solid #222", borderRadius:12, overflow:"hidden" }}>
              <div style={{ background:"#e53935", padding:"12px 18px", fontSize:14, fontWeight:900, color:"white", display:"flex", alignItems:"center", gap:8 }}>
                <span style={{ fontSize:18 }}></span> Non — Pourquoi ?
              </div>
              {VIANDE_OPTIONS.map((opt,i)=>(
                <div key={i} onClick={()=>setSelectedAccord(i)} style={{ background:selectedAccord===i?"#ffcc00":"white", borderBottom:"1px solid #ddd", padding:"11px 18px 11px 28px", fontSize:13, fontWeight:700, color:"#333", cursor:"pointer" }}>
                  <span style={{ display:"inline-block", width:10, height:10, borderRadius:"50%", border:"2px solid #aaa", marginRight:10, background:selectedAccord===i?"#c4622d":"transparent", borderColor:selectedAccord===i?"#c4622d":"#aaa", verticalAlign:"middle" }} />
                  {opt.label}
                </div>
              ))}
            </div>
          </div>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            {history.length > 0 ? <button onClick={goBack} style={{ ...btn, background:"white" }}>← Retour</button> : <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>}
            <button onClick={nextAccord} style={{ ...btn, opacity:selectedAccord===null?0.4:1, pointerEvents:selectedAccord===null?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
              const checked = checkedRaisons.includes(i);
              return (
                <div key={i} onClick={()=>{ setCheckedRaisons(prev => prev.includes(i) ? prev.filter(x=>x!==i) : [...prev, i]); }} style={{ display:"flex", alignItems:"flex-start", gap:12, background:checked?"#e8f5e9":"white", border:`2.5px solid ${checked?"#4caf50":"#222"}`, borderRadius:10, padding:"11px 14px", fontSize:13, fontWeight:700, color:"#333", cursor:"pointer", boxShadow:checked?"3px 3px 0 #388e3c":"3px 3px 0 #222", lineHeight:1.4 }}>
                  <div style={{ width:20, height:20, borderRadius:5, border:"2.5px solid", borderColor:checked?"#388e3c":"#ccc", background:checked?"#4caf50":"white", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:13, color:"white", marginTop:1 }}>{checked?"":""}</div>
                  {label}
                </div>
              );
            })}
          </div>
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            {history.length > 0 ? <button onClick={goBack} style={{ ...btn, background:"white" }}>← Retour</button> : <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>}
            <button onClick={nextCheck} style={{ ...btn, opacity:checkedRaisons.length===0?0.4:1, pointerEvents:checkedRaisons.length===0?"none":"auto" }}>Terminer →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══ QCM 2 ══ */
const VSLIDER_LABELS = ['Non, je mange de tout','Je mange sans porc','Je mange sans viande'];

function Qcm2Screen({ onBack, playerName, playerInfos, onDone }) {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState({});
  const [persons, setPersons] = useState(2);
  const [vslider, setVslider] = useState(0);
  const [compo, setCompo] = useState(null);
  const [cuisine, setCuisine] = useState(null);
  const [repas, setRepas] = useState(null);
  const [done, setDone] = useState(false);
  // MNA déplacé vers QCM Santé

  const btn = { marginTop:16, padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"22px 20px", borderRadius:22, maxWidth:600, width:"100%", textAlign:"center", border:"3px solid #222", boxShadow:"5px 5px 0 #222" };
  const bubbleStyle = (selected) => ({ display:"flex", alignItems:"center", gap:14, border:`2.5px solid ${selected?"#388e3c":"#74b87a"}`, borderRadius:99, padding:"12px 20px", fontSize:14, fontWeight:800, color:selected?"white":"#333", cursor:"pointer", background:selected?"#74b87a":"white", boxShadow:"3px 3px 0 #222", marginBottom:10 });

  const next = (s, a) => { playSound("good"); setAnswers(prev=>({...prev,...a})); setStep(s+1); };

  // Notify parent when done (in effect to avoid setState-during-render)
  useEffect(() => {
    if (done) {
      saveGame({ type:"qcm2", data: { answers, patient: { prenom: playerName, ...(playerInfos||{}) } } });
      const cuisineVal = answers["‍ En cuisine"];
      const compoVal = answers[" Composition du repas"];
      if (onDone) onDone(compoVal, cuisineVal, answers);
    }
  }, [done]); // eslint-disable-line

  if (done) {
    const cuisineVal = answers["‍ En cuisine"];
    const compoVal = answers[" Composition du repas"];
    return (
      <div style={{ position:"fixed", inset:0, background:"#F2F7F2", fontFamily:"Arial, sans-serif", overflowY:"auto" }}>
        {/* Header Medaviz */}
        <div style={{ background:"#F8FAFC", borderBottom:"1px solid #E8EDF2" }}>
          <div style={{ padding:"14px 20px" }}>
            <button onClick={onBack} style={{ background:"none", border:"1px solid #E8EDF2", borderRadius:10, color:"#1A3A5C", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour</button>
          </div>
          <div style={{ padding:"8px 20px 24px" }}>
            <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#FFF0EB", borderRadius:20, padding:"4px 12px", marginBottom:12 }}>
              <div style={{ width:6, height:6, borderRadius:"50%", background:"#FF6B35" }} />
              <span style={{ fontSize:11, fontWeight:800, color:"#E65100", textTransform:"uppercase", letterSpacing:1 }}>Fabrique à Menus</span>
            </div>
            <h1 style={{ fontSize:28, fontWeight:900, color:"#1A1A1A", margin:"0 0 4px" }}>Profil créé !</h1>
            <p style={{ color:"#6B7280", fontSize:14, margin:0 }}>Récapitulatif de vos préférences alimentaires</p>
          </div>
        </div>

        <div style={{ padding:"20px", display:"flex", flexDirection:"column", gap:14 }}>
          {/* Recap réponses */}
          <div style={{ background:"white", borderRadius:16, overflow:"hidden", boxShadow:"0 2px 10px rgba(0,0,0,0.07)" }}>
            <div style={{ background:"#E65100", padding:"14px 18px" }}>
              <div style={{ fontSize:14, fontWeight:900, color:"white" }}>Vos réponses</div>
            </div>
            <div style={{ padding:"16px 18px" }}>
              {Object.entries(answers).map(([k,v])=>(
                <div key={k} style={{ display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 0", borderBottom:"1px solid #F5F5F5" }}>
                  <span style={{ fontSize:13, color:"#888", fontWeight:600 }}>{k}</span>
                  <span style={{ fontSize:13, color:"#333", fontWeight:800, textAlign:"right", maxWidth:"55%" }}>{String(v)}</span>
                </div>
              ))}
              <div style={{ marginTop:14, background:"#FFF8E1", borderRadius:10, padding:"12px 14px", fontSize:13, color:"#E65100", fontWeight:600, lineHeight:1.5 }}>
                💡 Tous les repas de la semaine comptent pour adopter une alimentation équilibrée.
              </div>
            </div>
          </div>

          {/* Actions cards - Medaviz style */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
            <div onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "recos", answers); }}
              style={{ background:"white", borderRadius:20, padding:"20px", border:"1px solid #E8EDF2", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", cursor:"pointer", transition:"box-shadow 0.2s, transform 0.2s" }}
              onMouseEnter={e=>{e.currentTarget.style.boxShadow="0 8px 32px rgba(26,58,92,0.12)";e.currentTarget.style.transform="translateY(-2px)";}}
              onMouseLeave={e=>{e.currentTarget.style.boxShadow="0 2px 16px rgba(26,58,92,0.06)";e.currentTarget.style.transform="translateY(0)";}}>
              <div style={{ width:40, height:40, borderRadius:12, background:"#E0F7F5", marginBottom:12, display:"flex", alignItems:"center", justifyContent:"center" }}>
                <div style={{ width:16, height:16, borderRadius:"50%", background:"#00BFA5" }} />
              </div>
              <div style={{ fontSize:14, fontWeight:800, color:"#1A1A1A", marginBottom:4 }}>Recommandations</div>
              <div style={{ fontSize:12, color:"#6B7280", lineHeight:1.5, marginBottom:12 }}>Conseils nutritionnels personnalisés selon vos réponses.</div>
              <div style={{ fontSize:12, fontWeight:800, color:"#00BFA5" }}>Découvrir →</div>
            </div>
            <div onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "recettes", answers); }}
              style={{ background:"white", borderRadius:20, padding:"20px", border:"1px solid #E8EDF2", boxShadow:"0 2px 16px rgba(26,58,92,0.06)", cursor:"pointer", transition:"box-shadow 0.2s, transform 0.2s" }}
              onMouseEnter={e=>{e.currentTarget.style.boxShadow="0 8px 32px rgba(26,58,92,0.12)";e.currentTarget.style.transform="translateY(-2px)";}}
              onMouseLeave={e=>{e.currentTarget.style.boxShadow="0 2px 16px rgba(26,58,92,0.06)";e.currentTarget.style.transform="translateY(0)";}}>
              <div style={{ width:40, height:40, borderRadius:12, background:"#FFF0EB", marginBottom:12, display:"flex", alignItems:"center", justifyContent:"center" }}>
                <div style={{ width:16, height:16, borderRadius:5, background:"#FF6B35" }} />
              </div>
              <div style={{ fontSize:14, fontWeight:800, color:"#1A1A1A", marginBottom:4 }}>
                {answers[" En cuisine"] === "Je n'ai pas le temps" ? "Recettes rapides" : "Idées de recettes"}
              </div>
              <div style={{ fontSize:12, color:"#6B7280", lineHeight:1.5, marginBottom:12 }}>
                {answers[" En cuisine"] === "Je n'ai pas le temps" ? "Recettes équilibrées en moins de 30 min." : "Recettes selon vos préférences."}
              </div>
              <div style={{ fontSize:12, fontWeight:800, color:"#FF6B35" }}>Découvrir →</div>
            </div>
          </div>
          <div style={{ display:"flex", gap:10 }}>
            <button onClick={()=>{setStep(1);setDone(false);setPersons(2);setVslider(0);setCompo(null);setCuisine(null);setRepas(null);setAnswers({});}}
              style={{ flex:1, background:"white", border:"1px solid #E8EDF2", borderRadius:12, padding:"12px", fontSize:13, fontWeight:700, color:"#374151", cursor:"pointer" }}>Recommencer</button>
            <button onClick={onBack}
              style={{ flex:1, background:"white", border:"1px solid #E8EDF2", borderRadius:12, padding:"12px", fontSize:13, fontWeight:700, color:"#374151", cursor:"pointer" }}>← Menu</button>
          </div>

          {/* Continuer */}
          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "sante", answers); }}
            style={{ background:"#1A3A5C", border:"none", borderRadius:14, color:"white", fontSize:15, fontWeight:900, padding:"18px", cursor:"pointer", width:"100%", boxShadow:"0 4px 20px rgba(26,58,92,0.25)" }}
            onMouseEnter={e => e.currentTarget.style.opacity = "0.9"}
            onMouseLeave={e => e.currentTarget.style.opacity = "1"}>
            Continuer vers mon profil santé →
          </button>
          <button onClick={()=>{ if(onDone) onDone(answers[" Composition du repas"], "profil_qcm2", answers); }}
            style={{ background:"white", border:"2px solid #9ACD32", borderRadius:14, color:"#639922", fontSize:14, fontWeight:900, padding:"14px", cursor:"pointer", width:"100%" }}>
            Voir mon profil alimentaire →
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_blanc.jpg')", backgroundSize:"cover", backgroundPosition:"center", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"80px 16px 40px", fontFamily:"Arial, sans-serif" }}>
      
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#74b87a", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"0 3px 0 #222", zIndex:100 }}>
        <div style={{ display:"flex", alignItems:"center", gap:12 }}>
          <div style={{ fontSize:15, fontWeight:900, color:"white", textShadow:"1px 1px 0 #222" }}>{step <= 5 ? `Question ${step} / 5` : step === 20 || step === 25 ? "Résultat MNA" : step <= 11 ? `Dépistage ${step-5} / 6` : `Évaluation ${step >= 12 && step <= 24 ? [12,13,14,15,16,17,18,19,21,22,23,24].indexOf(step)+1 : '?'} / 12`}</div>
        </div>
        <div style={{ fontSize:14, fontWeight:900, color:"white" }}> Fabrique à Menus</div>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={onBack} style={{ ...btn, background:"white", opacity:0.4 }}>← Retour</button>
            <button onClick={()=>next(1,{" Nombre de personnes":`${persons} ${persons===1?"personne":"personnes"}`})} style={btn}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={()=>setStep(1)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={()=>next(2,{" Pratiques alimentaires":VSLIDER_LABELS[vslider]})} style={btn}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={()=>setStep(2)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={()=>compo&&next(3,{" Composition du repas":compo})} style={{ ...btn, opacity:!compo?0.4:1, pointerEvents:!compo?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={()=>setStep(3)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={()=>cuisine&&next(4,{"‍ En cuisine":cuisine})} style={{ ...btn, opacity:!cuisine?0.4:1, pointerEvents:!cuisine?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button
  onClick={onBack}
  style={{
    position: "absolute",
    top: 10,
    right: 10,
    width: 35,
    height: 35,
    borderRadius: "50%",
    border: "none",
    background: "#e53935",
    color: "white",
    fontSize: 20,
    fontWeight: "bold",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }}
>
  ✕
</button>
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
          <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
            <button onClick={()=>setStep(4)} style={{ ...btn, background:"white" }}>← Retour</button>
            <button onClick={()=>{ if(!repas) return; setAnswers(prev=>({...prev," Nombre de repas":repas})); setDone(true); }} style={{ ...btn, opacity:!repas?0.4:1, pointerEvents:!repas?"none":"auto" }}>Suivant →</button>
          </div>
          <div style={{ textAlign:"center", marginTop:8 }}>
            <button onClick={onBack} style={{ position:"absolute", top:10, right:10, width:35, height:35, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:20, fontWeight:"bold", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
          </div>
        </div>
      )}

    </div>
  );
}


/* ══ TRANSITION LLC → MEDAS ══ */

const MEDAS_QUESTIONS = [
  { id:"huile_olive_principale", q:"Utilisez-vous l'huile d'olive comme principale matière grasse pour cuisiner ?", bon:"Oui", mauvais:"Non" },
  { id:"huile_olive_dose", q:"Combien de cuillères à soupe d'huile d'olive consommez-vous par jour ?", note:"(y compris cuisson, assaisonnement, pain…)", bon:"≥ 4 cuillères à soupe/jour", mauvais:"< 4 cuillères à soupe/jour" },
  { id:"legumes", q:"Combien de portions de légumes consommez-vous par jour ?", note:"Une portion ≈ 200 g ; les accompagnements et salades sont inclus", bon:"≥ 2 portions/jour", mauvais:"< 2 portions/jour" },
  { id:"fruits", q:"Combien de portions de fruits consommez-vous par jour ?", note:"Une portion ≈ 80–100 g", bon:"≥ 3 portions/jour", mauvais:"< 3 portions/jour" },
  { id:"viande_rouge", q:"Combien de portions de viande rouge, hamburger, saucisses ou charcuteries consommez-vous par jour ?", bon:"< 1 portion/jour", mauvais:"≥ 1 portion/jour" },
  { id:"beurre", q:"Combien de portions de beurre, margarine ou crème consommez-vous par jour ?", note:"1 portion ≈ 12 g", bon:"< 1 portion/jour", mauvais:"≥ 1 portion/jour" },
  { id:"sodas", q:"Combien de boissons sucrées ou sodas consommez-vous par jour ?", bon:"< 1 boisson/jour", mauvais:"≥ 1 boisson/jour" },
  { id:"vin", q:"Combien de verres de vin consommez-vous par semaine ?", bon:"≥ 7 verres/semaine", mauvais:"< 7 verres/semaine" },
  { id:"legumineuses", q:"Combien de portions de légumineuses consommez-vous par semaine ?", note:"haricots, lentilles, pois chiches, etc.", bon:"≥ 3 portions/semaine", mauvais:"< 3 portions/semaine" },
  { id:"poisson", q:"Combien de portions de poisson ou fruits de mer consommez-vous par semaine ?", bon:"≥ 3 portions/semaine", mauvais:"< 3 portions/semaine" },
  { id:"patisseries", q:"Combien de fois par semaine consommez-vous des pâtisseries industrielles, biscuits, gâteaux ou viennoiseries ?", bon:"< 3 fois/semaine", mauvais:"≥ 3 fois/semaine" },
  { id:"fruits_coque", q:"Combien de portions de fruits à coque consommez-vous par semaine ?", note:"amandes, noix, noisettes, pistaches…", bon:"≥ 3 portions/semaine", mauvais:"< 3 portions/semaine" },
  { id:"viande_blanche", q:"Préférez-vous la viande blanche (poulet, dinde, lapin) à la viande rouge ou aux viandes transformées ?", bon:"Oui", mauvais:"Non" },
  { id:"sofrito", q:"Combien de fois par semaine consommez-vous des plats contenant du « sofrito » ?", note:"Sauce méditerranéenne à base de tomate, ail, oignon ou poireau cuits dans l'huile d'olive", bon:"≥ 2 fois/semaine", mauvais:"< 2 fois/semaine" },
];


const SILHOUETTES_H = [
  // SVG silhouettes masculines 1-9 (mince à corpulent)
  // Simplified SVG outlines
  { score:1, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="8" ry="9" fill="currentColor"/><rect x="24" y="24" width="12" height="45" rx="4" fill="currentColor"/><rect x="22" y="26" width="7" height="35" rx="3" fill="currentColor" transform="rotate(-5 22 26)"/><rect x="31" y="26" width="7" height="35" rx="3" fill="currentColor" transform="rotate(5 31 26)"/><rect x="23" y="68" width="7" height="40" rx="3" fill="currentColor" transform="rotate(3 23 68)"/><rect x="30" y="68" width="7" height="40" rx="3" fill="currentColor" transform="rotate(-3 30 68)"/></svg>` },
  { score:2, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="9" ry="10" fill="currentColor"/><rect x="23" y="25" width="14" height="46" rx="4" fill="currentColor"/><rect x="21" y="27" width="8" height="35" rx="3" fill="currentColor" transform="rotate(-5 21 27)"/><rect x="31" y="27" width="8" height="35" rx="3" fill="currentColor" transform="rotate(5 31 27)"/><rect x="22" y="69" width="8" height="40" rx="3" fill="currentColor" transform="rotate(3 22 69)"/><rect x="30" y="69" width="8" height="40" rx="3" fill="currentColor" transform="rotate(-3 30 69)"/></svg>` },
  { score:3, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="10" ry="10" fill="currentColor"/><rect x="22" y="25" width="16" height="46" rx="5" fill="currentColor"/><rect x="20" y="27" width="8" height="35" rx="3" fill="currentColor" transform="rotate(-6 20 27)"/><rect x="32" y="27" width="8" height="35" rx="3" fill="currentColor" transform="rotate(6 32 27)"/><rect x="21" y="69" width="9" height="40" rx="3" fill="currentColor" transform="rotate(3 21 69)"/><rect x="30" y="69" width="9" height="40" rx="3" fill="currentColor" transform="rotate(-3 30 69)"/></svg>` },
  { score:4, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="10" ry="11" fill="currentColor"/><rect x="21" y="25" width="18" height="47" rx="5" fill="currentColor"/><rect x="19" y="27" width="9" height="35" rx="3" fill="currentColor" transform="rotate(-6 19 27)"/><rect x="32" y="27" width="9" height="35" rx="3" fill="currentColor" transform="rotate(6 32 27)"/><rect x="20" y="70" width="9" height="40" rx="3" fill="currentColor" transform="rotate(3 20 70)"/><rect x="30" y="70" width="9" height="40" rx="3" fill="currentColor" transform="rotate(-3 30 70)"/></svg>` },
  { score:5, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="11" ry="11" fill="currentColor"/><ellipse cx="30" cy="48" rx="12" ry="14" fill="currentColor"/><rect x="18" y="28" width="10" height="33" rx="3" fill="currentColor" transform="rotate(-8 18 28)"/><rect x="32" y="28" width="10" height="33" rx="3" fill="currentColor" transform="rotate(8 32 28)"/><rect x="19" y="70" width="10" height="40" rx="3" fill="currentColor" transform="rotate(4 19 70)"/><rect x="30" y="70" width="10" height="40" rx="3" fill="currentColor" transform="rotate(-4 30 70)"/></svg>` },
  { score:6, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="11" ry="12" fill="currentColor"/><ellipse cx="30" cy="50" rx="14" ry="15" fill="currentColor"/><rect x="16" y="28" width="11" height="33" rx="3" fill="currentColor" transform="rotate(-9 16 28)"/><rect x="33" y="28" width="11" height="33" rx="3" fill="currentColor" transform="rotate(9 33 28)"/><rect x="18" y="72" width="11" height="38" rx="3" fill="currentColor" transform="rotate(5 18 72)"/><rect x="30" y="72" width="11" height="38" rx="3" fill="currentColor" transform="rotate(-5 30 72)"/></svg>` },
  { score:7, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="12" ry="12" fill="currentColor"/><ellipse cx="30" cy="52" rx="16" ry="17" fill="currentColor"/><rect x="14" y="29" width="12" height="33" rx="3" fill="currentColor" transform="rotate(-10 14 29)"/><rect x="34" y="29" width="12" height="33" rx="3" fill="currentColor" transform="rotate(10 34 29)"/><rect x="17" y="74" width="12" height="37" rx="3" fill="currentColor" transform="rotate(6 17 74)"/><rect x="30" y="74" width="12" height="37" rx="3" fill="currentColor" transform="rotate(-6 30 74)"/></svg>` },
  { score:8, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="12" ry="13" fill="currentColor"/><ellipse cx="30" cy="54" rx="18" ry="19" fill="currentColor"/><rect x="12" y="30" width="12" height="32" rx="3" fill="currentColor" transform="rotate(-11 12 30)"/><rect x="36" y="30" width="12" height="32" rx="3" fill="currentColor" transform="rotate(11 36 30)"/><rect x="16" y="76" width="13" height="36" rx="3" fill="currentColor" transform="rotate(7 16 76)"/><rect x="30" y="76" width="13" height="36" rx="3" fill="currentColor" transform="rotate(-7 30 76)"/></svg>` },
  { score:9, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="15" rx="13" ry="13" fill="currentColor"/><ellipse cx="30" cy="56" rx="20" ry="21" fill="currentColor"/><rect x="10" y="30" width="13" height="32" rx="3" fill="currentColor" transform="rotate(-12 10 30)"/><rect x="37" y="30" width="13" height="32" rx="3" fill="currentColor" transform="rotate(12 37 30)"/><rect x="15" y="78" width="14" height="35" rx="3" fill="currentColor" transform="rotate(8 15 78)"/><rect x="30" y="78" width="14" height="35" rx="3" fill="currentColor" transform="rotate(-8 30 78)"/></svg>` },
];


const SILHOUETTES_F = [
  { score:1, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="8" ry="9" fill="currentColor"/><path d="M26 23 Q22 42 24 55 Q30 58 36 55 Q38 42 34 23 Z" fill="currentColor"/><ellipse cx="30" cy="38" rx="7" ry="5" fill="currentColor" opacity="0.3"/><rect x="21" y="27" width="6" height="32" rx="3" fill="currentColor" transform="rotate(-5 21 27)"/><rect x="33" y="27" width="6" height="32" rx="3" fill="currentColor" transform="rotate(5 33 27)"/><rect x="23" y="68" width="7" height="40" rx="3" fill="currentColor" transform="rotate(2 23 68)"/><rect x="30" y="68" width="7" height="40" rx="3" fill="currentColor" transform="rotate(-2 30 68)"/></svg>` },
  { score:2, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="9" ry="9" fill="currentColor"/><path d="M25 23 Q20 43 23 56 Q30 60 37 56 Q40 43 35 23 Z" fill="currentColor"/><ellipse cx="30" cy="39" rx="8" ry="6" fill="currentColor" opacity="0.3"/><rect x="20" y="27" width="7" height="32" rx="3" fill="currentColor" transform="rotate(-5 20 27)"/><rect x="33" y="27" width="7" height="32" rx="3" fill="currentColor" transform="rotate(5 33 27)"/><rect x="22" y="68" width="8" height="40" rx="3" fill="currentColor" transform="rotate(2 22 68)"/><rect x="30" y="68" width="8" height="40" rx="3" fill="currentColor" transform="rotate(-2 30 68)"/></svg>` },
  { score:3, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="10" ry="10" fill="currentColor"/><path d="M24 24 Q18 44 22 57 Q30 62 38 57 Q42 44 36 24 Z" fill="currentColor"/><ellipse cx="30" cy="40" rx="9" ry="7" fill="currentColor" opacity="0.3"/><rect x="19" y="28" width="7" height="32" rx="3" fill="currentColor" transform="rotate(-6 19 28)"/><rect x="34" y="28" width="7" height="32" rx="3" fill="currentColor" transform="rotate(6 34 28)"/><rect x="21" y="69" width="9" height="39" rx="3" fill="currentColor" transform="rotate(2 21 69)"/><rect x="30" y="69" width="9" height="39" rx="3" fill="currentColor" transform="rotate(-2 30 69)"/></svg>` },
  { score:4, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="10" ry="10" fill="currentColor"/><path d="M23 24 Q16 45 21 58 Q30 64 39 58 Q44 45 37 24 Z" fill="currentColor"/><ellipse cx="30" cy="41" rx="10" ry="8" fill="currentColor" opacity="0.3"/><rect x="18" y="28" width="8" height="32" rx="3" fill="currentColor" transform="rotate(-7 18 28)"/><rect x="34" y="28" width="8" height="32" rx="3" fill="currentColor" transform="rotate(7 34 28)"/><rect x="20" y="70" width="9" height="38" rx="3" fill="currentColor" transform="rotate(3 20 70)"/><rect x="30" y="70" width="9" height="38" rx="3" fill="currentColor" transform="rotate(-3 30 70)"/></svg>` },
  { score:5, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="11" ry="11" fill="currentColor"/><path d="M22 25 Q14 46 20 60 Q30 67 40 60 Q46 46 38 25 Z" fill="currentColor"/><ellipse cx="30" cy="43" rx="12" ry="10" fill="currentColor" opacity="0.3"/><rect x="16" y="29" width="9" height="32" rx="3" fill="currentColor" transform="rotate(-8 16 29)"/><rect x="35" y="29" width="9" height="32" rx="3" fill="currentColor" transform="rotate(8 35 29)"/><rect x="19" y="72" width="10" height="37" rx="3" fill="currentColor" transform="rotate(4 19 72)"/><rect x="30" y="72" width="10" height="37" rx="3" fill="currentColor" transform="rotate(-4 30 72)"/></svg>` },
  { score:6, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="11" ry="12" fill="currentColor"/><path d="M21 25 Q12 47 19 62 Q30 70 41 62 Q48 47 39 25 Z" fill="currentColor"/><ellipse cx="30" cy="45" rx="14" ry="11" fill="currentColor" opacity="0.3"/><rect x="14" y="29" width="10" height="32" rx="3" fill="currentColor" transform="rotate(-9 14 29)"/><rect x="36" y="29" width="10" height="32" rx="3" fill="currentColor" transform="rotate(9 36 29)"/><rect x="18" y="74" width="11" height="36" rx="3" fill="currentColor" transform="rotate(5 18 74)"/><rect x="30" y="74" width="11" height="36" rx="3" fill="currentColor" transform="rotate(-5 30 74)"/></svg>` },
  { score:7, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="12" ry="12" fill="currentColor"/><path d="M20 25 Q10 48 18 64 Q30 73 42 64 Q50 48 40 25 Z" fill="currentColor"/><ellipse cx="30" cy="47" rx="16" ry="13" fill="currentColor" opacity="0.3"/><rect x="12" y="30" width="11" height="32" rx="3" fill="currentColor" transform="rotate(-10 12 30)"/><rect x="37" y="30" width="11" height="32" rx="3" fill="currentColor" transform="rotate(10 37 30)"/><rect x="17" y="76" width="12" height="35" rx="3" fill="currentColor" transform="rotate(6 17 76)"/><rect x="30" y="76" width="12" height="35" rx="3" fill="currentColor" transform="rotate(-6 30 76)"/></svg>` },
  { score:8, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="13" rx="12" ry="13" fill="currentColor"/><path d="M19 25 Q8 49 17 66 Q30 76 43 66 Q52 49 41 25 Z" fill="currentColor"/><ellipse cx="30" cy="49" rx="18" ry="15" fill="currentColor" opacity="0.3"/><rect x="10" y="30" width="12" height="32" rx="3" fill="currentColor" transform="rotate(-11 10 30)"/><rect x="38" y="30" width="12" height="32" rx="3" fill="currentColor" transform="rotate(11 38 30)"/><rect x="16" y="78" width="13" height="34" rx="3" fill="currentColor" transform="rotate(7 16 78)"/><rect x="30" y="78" width="13" height="34" rx="3" fill="currentColor" transform="rotate(-7 30 78)"/></svg>` },
  { score:9, svg:`<svg viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg"><ellipse cx="30" cy="14" rx="13" ry="13" fill="currentColor"/><path d="M18 26 Q6 50 16 68 Q30 79 44 68 Q54 50 42 26 Z" fill="currentColor"/><ellipse cx="30" cy="51" rx="20" ry="17" fill="currentColor" opacity="0.3"/><rect x="8" y="31" width="13" height="31" rx="3" fill="currentColor" transform="rotate(-12 8 31)"/><rect x="39" y="31" width="13" height="31" rx="3" fill="currentColor" transform="rotate(12 39 31)"/><rect x="15" y="80" width="14" height="33" rx="3" fill="currentColor" transform="rotate(8 15 80)"/><rect x="30" y="80" width="14" height="33" rx="3" fill="currentColor" transform="rotate(-8 30 80)"/></svg>` },
];


function getSilhouetteLabel(score) {
  if (score <= 2) return { label:"Maigreur", color:"#1565c0", bg:"#e3f2fd" };
  if (score <= 4) return { label:"Corpulence normale", color:"#2e7d32", bg:"#e8f5e9" };
  if (score <= 6) return { label:"Surpoids modéré", color:"#f57c00", bg:"#fff3e0" };
  return { label:"Obésité probable", color:"#c62828", bg:"#fbe9e7" };
}

function TransitionLLCScreen({ onStart }) {
  const [phase, setPhase] = useState(0);
  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 300);
    const t2 = setTimeout(() => setPhase(2), 1000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);
  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"40px 24px" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
      <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:24, maxWidth:520, width:"100%",
        opacity:phase>=1?1:0, transform:phase>=1?"translateY(0)":"translateY(30px)", transition:"all 0.7s cubic-bezier(0.34,1.56,0.64,1)" }}>
        <div style={{ display:"flex", alignItems:"flex-end", gap:16, width:"100%" }}>
          <img src="/e.png" alt="Max" style={{ width:110, filter:"drop-shadow(4px 4px 0 rgba(0,0,0,0.4))", flexShrink:0 }} />
          <div style={{ background:"#fff8f0", border:"3px solid #222", borderRadius:"20px 20px 20px 4px", padding:"16px 20px", boxShadow:"5px 5px 0 rgba(0,0,0,0.3)", flex:1,
            opacity:phase>=2?1:0, transform:phase>=2?"translateY(0)":"translateY(16px)", transition:"all 0.5s ease 0.2s" }}>
            <div style={{ fontSize:10, fontWeight:900, textTransform:"uppercase", letterSpacing:"0.15em", color:"#d4622d", marginBottom:6 }}>Max — Coach Nutrition</div>
            <div style={{ fontSize:15, fontWeight:700, color:"#222", lineHeight:1.7 }}>
              Tu as mentionné la <strong style={{ color:"#7C3AED" }}>LLC</strong>. 🫒<br/>
              <span style={{ fontSize:14, fontWeight:600, color:"#555" }}>Des études montrent que le <strong>régime méditerranéen</strong> est particulièrement bénéfique. 14 questions rapides !</span>
            </div>
          </div>
        </div>
        <button onClick={onStart} style={{ background:"#FA8072", border:"3px solid #222", borderRadius:14, color:"white", fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, padding:"16px 48px", cursor:"pointer", boxShadow:"5px 5px 0 #222", width:"100%",
          opacity:phase>=2?1:0, transition:"opacity 0.5s ease 0.4s" }}>
          Commencer le questionnaire méditerranéen →
        </button>
      </div>
    </div>
  );
}

function QcmMedasScreen({ onBack, onDone, playerName }) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selected, setSelected] = useState(null);
  const q = MEDAS_QUESTIONS[step];
  const TOTAL = MEDAS_QUESTIONS.length;
  const qCard = { background:"white", padding:"28px 24px 24px", borderRadius:22, maxWidth:620, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };

  const handleAnswer = (isBon) => {
    setSelected(isBon);
    setTimeout(() => {
      setSelected(null);
      const newAnswers = { ...answers, [q.id]: isBon ? 1 : 0 };
      setAnswers(newAnswers);
      if (step < TOTAL - 1) { setStep(s => s + 1); }
      else { const score = Object.values(newAnswers).reduce((a, b) => a + b, 0); onDone({ answers: newAnswers, score }); }
    }, 300);
  };

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"70px 16px 20px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.92)" }} />
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#9ACD32", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", zIndex:100, boxShadow:"0 3px 0 #222" }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white" }}>🫒 Régime méditerranéen — {step+1} / {TOTAL}</div>
        <div style={{ display:"flex", gap:4 }}>
          {Array.from({length:TOTAL}).map((_,i) => (
            <div key={i} style={{ width:16, height:5, borderRadius:3, background:step>i?"#ffcc00":"rgba(255,255,255,0.4)", transition:"background 0.3s" }} />
          ))}
        </div>
      </div>
      <div style={{ ...qCard, zIndex:1 }}>
        <button onClick={onBack} style={{ position:"absolute", top:12, right:12, width:34, height:34, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:18, fontWeight:900, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
        <div style={{ textAlign:"center", marginBottom:16 }}>
          <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#f0f9e0", border:"2px solid #9ACD32", borderRadius:20, padding:"4px 14px", marginBottom:10 }}>
            <span style={{ fontSize:11, fontWeight:900, color:"#639922", textTransform:"uppercase", letterSpacing:1 }}>Question {step+1}/{TOTAL}</span>
          </div>
          <h2 style={{ fontSize:"1.2em", color:"#FA8072", fontWeight:900, margin:"0 0 6px", lineHeight:1.4 }}>{q.q}</h2>
          {q.note && <p style={{ fontSize:12, color:"#888", fontStyle:"italic", margin:"0 0 12px" }}>{q.note}</p>}
        </div>
        <div style={{ display:"flex", flexDirection:"column", gap:12 }}>
          <div onClick={() => handleAnswer(true)}
            style={{ background:selected===true?"#f0f9e0":"white", border:`2.5px solid ${selected===true?"#9ACD32":"#ddd"}`, borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222", transition:"all 0.2s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:selected===true?"#2E7D32":"#333" }}>{q.bon}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:selected===true?"#9ACD32":"#eee", display:"flex", alignItems:"center", justifyContent:"center", color:selected===true?"white":"#aaa", fontWeight:900, fontSize:12, transition:"all 0.2s" }}>+1</div>
          </div>
          <div onClick={() => handleAnswer(false)}
            style={{ background:selected===false?"#fbe9e7":"white", border:`2.5px solid ${selected===false?"#e53935":"#ddd"}`, borderRadius:14, padding:"16px 20px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #ddd", transition:"all 0.2s" }}>
            <span style={{ fontSize:14, fontWeight:800, color:selected===false?"#e53935":"#555" }}>{q.mauvais}</span>
            <div style={{ width:28, height:28, borderRadius:"50%", background:selected===false?"#e53935":"#f0f0f0", display:"flex", alignItems:"center", justifyContent:"center", color:selected===false?"white":"#aaa", fontWeight:900, fontSize:12, transition:"all 0.2s" }}>0</div>
          </div>
        </div>
        {step > 0 && <button onClick={() => setStep(s => s-1)} style={{ marginTop:14, background:"none", border:"none", color:"#888", fontSize:13, fontWeight:700, cursor:"pointer" }}>← Question précédente</button>}
      </div>
    </div>
  );
}

function QcmSanteScreen({ onBack, onDone, playerName, playerInfos }) {
  const [step, setStep] = useState(1);
  const [age, setAge] = useState(null);
  const [sexe, setSexe] = useState(null);
  const [silhouette, setSilhouette] = useState(null);
  const [evolution, setEvolution] = useState(null);
  const [seul, setSeul] = useState(null);
  const [autonomie, setAutonomie] = useState(null);
  const [maladie, setMaladie] = useState(null);
  const [pathologies, setPathologies] = useState([]);
  const [traitement, setTraitement] = useState(null);
  const [regime, setRegime] = useState(null);
  const [modeVie, setModeVie] = useState(null);
  const [showMedas, setShowMedas] = useState(false);
  const [showTransitionLLC, setShowTransitionLLC] = useState(false);
  const [medasDone, setMedasDone] = useState(false);
  const [medasResult, setMedasResult] = useState(null);

  const [openRec, setOpenRec] = useState(null);
  const [mnaStep, setMnaStep] = useState(0);
  const [mnaAnswers, setMnaAnswers] = useState({});
  const hasLLC = pathologies.some(p => p.includes("LLC"));
  const hasPoids = evolution === "Beaucoup plus mince" || evolution === "Un peu plus mince";
  const silhouettes = sexe === "Homme" ? SILHOUETTES_H : SILHOUETTES_F;
  const sil = silhouette ? getSilhouetteLabel(silhouette) : null;
  const TOTAL = 10;

  const btn = { padding:"13px 30px", fontSize:16, fontWeight:800, border:"3px solid #222", cursor:"pointer", background:"#9ACD32", borderRadius:12, boxShadow:"4px 4px 0 #222", color:"#222" };
  const qCard = { background:"white", color:"#333", padding:"28px 24px 24px", borderRadius:22, maxWidth:660, width:"100%", border:"3px solid #222", boxShadow:"5px 5px 0 #222", position:"relative" };
  const bubble = (selected) => ({
    display:"flex", alignItems:"center", gap:14,
    border:`2.5px solid ${selected?"#7C3AED":"#ddd"}`,
    borderRadius:99, padding:"12px 20px", fontSize:14, fontWeight:800,
    color:selected?"white":"#333", cursor:"pointer",
    background:selected?"#7C3AED":"white",
    boxShadow:"3px 3px 0 #222", marginBottom:10
  });
  const radio = (selected) => (
    <div style={{ width:18, height:18, borderRadius:"50%", border:`2.5px solid ${selected?"white":"#ccc"}`, flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
      {selected && <div style={{ width:8, height:8, borderRadius:"50%", background:"white" }} />}
    </div>
  );
  const CloseBtn = () => (
    <button onClick={onBack} style={{ position:"absolute", top:12, right:12, width:34, height:34, borderRadius:"50%", border:"none", background:"#e53935", color:"white", fontSize:18, fontWeight:900, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center" }}>✕</button>
  );
  const Nav = ({ onPrev, onNext, canNext }) => (
    <div style={{ display:"flex", justifyContent:"space-between", marginTop:20 }}>
      <button onClick={onPrev} style={{ ...btn, background:"white" }}>← Retour</button>
      <button onClick={onNext} style={{ ...btn, opacity:canNext?1:0.4, pointerEvents:canNext?"auto":"none" }}>Suivant →</button>
    </div>
  );

  if (showTransitionLLC && !showMedas) return <TransitionLLCScreen onStart={() => { setShowTransitionLLC(false); setShowMedas(true); }} />;
  if (showMedas && !medasDone) return <QcmMedasScreen onBack={() => setShowMedas(false)} playerName={playerName} onDone={(r) => { setMedasResult(r); setMedasDone(true); setShowMedas(false); setStep(99); }} />;

  const handleFinish = () => {
    const data = { age, sexe, silhouette, evolution, seul, autonomie, maladie, pathologies, traitement, regime, modeVie, medasResult, hasLLC, hasPoids };
    saveGame({ type:"qcm_sante", data: { ...data, patient: { prenom:playerName, email:playerInfos?.email||"" } } });
    onDone(data);
  };

  return (
    <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_orange.png')", backgroundSize:"cover", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"70px 16px 20px", fontFamily:"Arial, sans-serif" }}>
      <div style={{ position:"absolute", inset:0, background:"rgba(255,255,255,0.92)" }} />

      {/* Header */}
      <div style={{ position:"fixed", top:0, left:0, right:0, background:"#c4622d", borderBottom:"3px solid #222", padding:"10px 20px", display:"flex", alignItems:"center", justifyContent:"space-between", zIndex:100, boxShadow:"0 3px 0 #222" }}>
        <div style={{ fontSize:15, fontWeight:900, color:"white" }}>🏥 Mon profil santé — {Math.min(step,TOTAL)} / {TOTAL}</div>
        <div style={{ display:"flex", gap:5 }}>
          {Array.from({length:TOTAL}).map((_,i) => (
            <div key={i} style={{ width:22, height:5, borderRadius:3, background:step>i?"#ffcc00":"rgba(255,255,255,0.3)", transition:"background 0.3s" }} />
          ))}
        </div>
      </div>

      {/* Q1 — Âge */}
      {step===1 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🎂</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Quelle est votre catégorie d&apos;âge ?</h2>
          {["Moins de 40 ans","40 à 60 ans","60 à 74 ans","75 à 84 ans","85 ans et plus"].map(a => (
            <div key={a} onClick={()=>setAge(a)} style={bubble(age===a)}>{radio(age===a)}{a}</div>
          ))}
          <Nav onPrev={onBack} onNext={()=>setStep(2)} canNext={!!age} />
        </div>
      )}

      {/* Q2 — Sexe */}
      {step===2 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>👤</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Sexe</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Homme","Femme"].map(s => (
              <div key={s} onClick={()=>setSexe(s)} style={{ ...bubble(sexe===s), flex:1, justifyContent:"center" }}>{s}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(1)} onNext={()=>setStep(3)} canNext={!!sexe} />
        </div>
      )}

      {/* Q3 — Silhouette */}
      {step===3 && (
        <div style={qCard}>
          <CloseBtn />
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:4 }}>Quelle silhouette vous ressemble le plus ?</h2>
          <p style={{ color:"#aaa", fontSize:11, fontStyle:"italic", textAlign:"center", marginBottom:16 }}>Échelle de Stunkard — auto-perception, données non stockées</p>
          <div style={{ display:"flex", gap:6, overflowX:"auto", paddingBottom:8, justifyContent:"center" }}>
            {(sexe==="Homme"?SILHOUETTES_H:SILHOUETTES_F).map(s => (
              <div key={s.score} onClick={()=>setSilhouette(s.score)} style={{ flexShrink:0, display:"flex", flexDirection:"column", alignItems:"center", gap:4, cursor:"pointer" }}>
                <div style={{ width:52, height:95, border:`2.5px solid ${silhouette===s.score?"#7C3AED":"#eee"}`, borderRadius:10, background:silhouette===s.score?"#f3eeff":"#fafafa", display:"flex", alignItems:"center", justifyContent:"center", padding:3 }}
                  dangerouslySetInnerHTML={{ __html: s.svg.replace(/fill="currentColor"/g,`fill="${silhouette===s.score?"#7C3AED":"#bbb"}"`) }} />
                <div style={{ fontSize:11, fontWeight:900, color:silhouette===s.score?"#7C3AED":"#aaa" }}>{s.score}</div>
              </div>
            ))}
          </div>
          {sil && <div style={{ margin:"12px 0", background:sil.bg, border:`2px solid ${sil.color}`, borderRadius:10, padding:"8px 14px", fontSize:13, fontWeight:700, color:sil.color, textAlign:"center" }}>Silhouette {silhouette} — {sil.label}</div>}
          <Nav onPrev={()=>setStep(2)} onNext={()=>setStep(4)} canNext={!!silhouette} />
        </div>
      )}

      {/* Q4 — Évolution */}
      {step===4 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>⚖️</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Cette silhouette est-elle différente de celle d&apos;il y a 6 mois ?</h2>
          {["Beaucoup plus mince","Un peu plus mince","Identique","Un peu plus corpulent(e)","Beaucoup plus corpulent(e)"].map(e => (
            <div key={e} onClick={()=>setEvolution(e)} style={bubble(evolution===e)}>{radio(evolution===e)}{e}</div>
          ))}
          <Nav onPrev={()=>setStep(3)} onNext={()=>setStep(5)} canNext={!!evolution} />
        </div>
      )}

      {/* Q5 — Seul */}
      {step===5 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🏠</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Vivez-vous seul(e) ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setSeul(v)} style={{ ...bubble(seul===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(4)} onNext={()=>setStep(6)} canNext={!!seul} />
        </div>
      )}

      {/* Q6 — Autonomie */}
      {step===6 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🛒</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Faites-vous vos courses et vos repas vous-même ?</h2>
          {["Courses et repas","Courses seulement","Repas seulement","Ni l'un ni l'autre"].map(a => (
            <div key={a} onClick={()=>setAutonomie(a)} style={bubble(autonomie===a)}>{radio(autonomie===a)}{a}</div>
          ))}
          <Nav onPrev={()=>setStep(5)} onNext={()=>setStep(7)} canNext={!!autonomie} />
        </div>
      )}

      {/* Q7 — Maladie chronique */}
      {step===7 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🏥</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Avez-vous une maladie chronique connue ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setMaladie(v)} style={{ ...bubble(maladie===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(6)} onNext={()=>setStep(8)} canNext={!!maladie} />
        </div>
      )}

      {/* Q8 — Pathologies */}
      {step===8 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>📋</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:4 }}>Avez-vous l&apos;une de ces pathologies ?</h2>
          <p style={{ color:"#aaa", fontSize:12, textAlign:"center", marginBottom:14 }}>Plusieurs réponses possibles</p>
          {["LLC (Leucémie Lymphoïde Chronique)","Diabète","Hypertension","Maladie cardiovasculaire","Insuffisance rénale","Cancer (autre)","Aucune"].map(p => {
            const checked = pathologies.includes(p);
            return (
              <div key={p} onClick={()=>{ if(p==="Aucune"){setPathologies(["Aucune"]);return;} setPathologies(prev=>{const f=prev.filter(x=>x!=="Aucune");return f.includes(p)?f.filter(x=>x!==p):[...f,p];}); }}
                style={{ display:"flex", alignItems:"center", gap:12, border:`2.5px solid ${checked?"#7C3AED":"#ddd"}`, borderRadius:12, padding:"11px 16px", cursor:"pointer", background:checked?"#f3eeff":"white", marginBottom:8, fontSize:13, fontWeight:700 }}>
                <div style={{ width:20, height:20, borderRadius:5, border:`2.5px solid ${checked?"#7C3AED":"#ccc"}`, background:checked?"#7C3AED":"white", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", fontSize:12, color:"white" }}>{checked?"✓":""}</div>
                {p}
                {p.includes("LLC") && <span style={{ marginLeft:"auto", fontSize:10, background:"#f3eeff", border:"1px solid #7C3AED", borderRadius:20, padding:"2px 8px", color:"#7C3AED", fontWeight:900 }}>QCM spécifique</span>}
              </div>
            );
          })}
          <Nav onPrev={()=>setStep(7)} onNext={()=>setStep(9)} canNext={pathologies.length>0} />
        </div>
      )}

      {/* Q9 — Traitement */}
      {step===9 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>💊</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Suivez-vous un traitement régulier ?</h2>
          <div style={{ display:"flex", gap:16 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setTraitement(v)} style={{ ...bubble(traitement===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <Nav onPrev={()=>setStep(8)} onNext={()=>setStep(10)} canNext={!!traitement} />
        </div>
      )}

      {/* Q10 — Régime + Mode de vie */}
      {step===10 && (
        <div style={qCard}>
          <CloseBtn />
          <div style={{ textAlign:"center", marginBottom:16 }}><div style={{ fontSize:40 }}>🥗</div></div>
          <h2 style={{ fontSize:"1.3em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:16 }}>Votre médecin vous a-t-il conseillé un régime particulier ?</h2>
          <div style={{ display:"flex", gap:16, marginBottom:20 }}>
            {["Oui","Non"].map(v => (
              <div key={v} onClick={()=>setRegime(v)} style={{ ...bubble(regime===v), flex:1, justifyContent:"center" }}>{v}</div>
            ))}
          </div>
          <h2 style={{ fontSize:"1.2em", color:"#FA8072", fontWeight:900, textAlign:"center", marginBottom:12 }}>Quel est votre mode de vie ?</h2>
          {["Très actif","Actif","Sédentaire"].map(m => (
            <div key={m} onClick={()=>setModeVie(m)} style={bubble(modeVie===m)}>{radio(modeVie===m)}{m}</div>
          ))}
          {hasLLC && <div style={{ background:"#f3eeff", border:"2px solid #7C3AED", borderRadius:10, padding:"10px 14px", fontSize:13, fontWeight:700, color:"#7C3AED", marginTop:8 }}>⚠️ LLC détectée — un QCM sur le régime méditerranéen va suivre.</div>}
          <Nav onPrev={()=>setStep(9)} onNext={()=>{
  const is75plus = age==="75 à 84 ans" || age==="85 ans et plus";
  const needsMNA = is75plus && hasPoids;
  if(hasLLC){ setShowTransitionLLC(true); }
  else if(needsMNA){ setStep(11); }
  else{ setStep(99); }
}} canNext={!!regime && !!modeVie} />
        </div>
      )}

      {/* Step 11 — MNA Dénutrition */}
      {step===11 && (() => {
        const MNA_QS = [
          { q:"Le patient présente-t-il une perte d'appétit ces 3 derniers mois ?", opts:[[0,"Baisse sévère"],[1,"Légère baisse"],[2,"Pas de baisse"]], key:"appetit" },
          { q:"Perte de poids récente (< 3 mois) ?", opts:[[0,"Perte > 3 kg"],[1,"Ne sait pas"],[2,"Perte 1-3 kg"],[3,"Pas de perte"]], key:"poids" },
          { q:"Motricité ?", opts:[[0,"Au lit ou fauteuil"],[1,"Autonome à l'intérieur"],[2,"Sort du domicile"]], key:"motricite" },
          { q:"Maladie aiguë ou stress psychologique ces 3 derniers mois ?", opts:[[0,"Oui"],[2,"Non"]], key:"stress" },
          { q:"Problèmes neuropsychologiques ?", opts:[[0,"Démence ou dépression sévère"],[1,"Démence légère"],[2,"Pas de problème"]], key:"neuro" },
          { q:"IMC (Indice de Masse Corporelle) ?", opts:[[0,"< 19"],[1,"19-21"],[2,"21-23"],[3,"≥ 23"]], key:"imc" },
        ];
        const mnaQ = MNA_QS[mnaStep];
        const mnaScore = Object.values(mnaAnswers).reduce((a,b)=>a+b,0);
        const handleMna = (val) => {
          const newA = { ...mnaAnswers, [mnaQ.key]: val };
          setMnaAnswers(newA);
          if (mnaStep < MNA_QS.length-1) { setMnaStep(s=>s+1); }
          else { setStep(99); }
        };
        return (
          <div style={{ ...qCard, zIndex:1 }}>
            <CloseBtn />
            <div style={{ textAlign:"center", marginBottom:14 }}>
              <div style={{ display:"inline-flex", alignItems:"center", gap:6, background:"#fbe9e7", border:"2px solid #e53935", borderRadius:20, padding:"4px 14px", marginBottom:10 }}>
                <span style={{ fontSize:11, fontWeight:900, color:"#e53935", textTransform:"uppercase", letterSpacing:1 }}>Dépistage dénutrition MNA — {mnaStep+1}/6</span>
              </div>
              <h2 style={{ fontSize:"1.2em", color:"#FA8072", fontWeight:900, margin:0, lineHeight:1.4 }}>{mnaQ.q}</h2>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
              {mnaQ.opts.map(([val, label]) => (
                <div key={val} onClick={() => handleMna(val)}
                  style={{ background:"white", border:"2.5px solid #ddd", borderRadius:14, padding:"14px 18px", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"space-between", boxShadow:"3px 3px 0 #222" }}>
                  <span style={{ fontSize:13, fontWeight:800, color:"#333" }}>{label}</span>
                  <span style={{ fontSize:12, background:"#f5f5f5", borderRadius:20, padding:"3px 10px", color:"#888", fontWeight:700 }}>{val} pt{val>1?"s":""}</span>
                </div>
              ))}
            </div>
            <div style={{ display:"flex", justifyContent:"space-between", marginTop:16 }}>
              <button onClick={() => mnaStep>0?setMnaStep(s=>s-1):setStep(10)} style={{ ...btn, background:"white" }}>← Retour</button>
              <button onClick={() => setStep(99)} style={{ fontSize:12, fontWeight:700, color:"#aaa", background:"none", border:"none", cursor:"pointer" }}>Passer →</button>
            </div>
          </div>
        );
      })()}

      {/* Bilan */}
      {step===99 && (() => {
        const medsRecs = RECETTES_DATA.filter(r => r.profils && r.profils.includes("mediterraneen"));

        if (openRec) return (
          <div style={{ position:"fixed", inset:0, background:"#F8FAFC", overflowY:"auto", zIndex:200 }}>
            <div style={{ position:"sticky", top:0, zIndex:10, background:"white", borderBottom:"1px solid #eee", padding:"12px 20px", display:"flex", alignItems:"center", gap:12 }}>
              <button onClick={() => setOpenRec(null)} style={{ background:"none", border:"1px solid #eee", borderRadius:10, color:"#333", fontSize:13, fontWeight:700, cursor:"pointer", padding:"7px 14px" }}>← Retour au bilan</button>
              <span style={{ fontSize:14, fontWeight:900, color:"#9ACD32" }}>🫒 {openRec.titre}</span>
            </div>
            {openRec.image && <div style={{ height:220, overflow:"hidden" }}><img src={openRec.image} style={{ width:"100%", height:"100%", objectFit:"cover" }} /></div>}
            <div style={{ padding:"20px", maxWidth:680, margin:"0 auto" }}>
              <div style={{ background:"#E0F7F5", borderLeft:"4px solid #00BFA5", borderRadius:"0 12px 12px 0", padding:"12px 16px", marginBottom:20 }}>
                <div style={{ fontSize:11, fontWeight:800, color:"#00897B", textTransform:"uppercase", marginBottom:4 }}>💡 Bénéfice</div>
                <p style={{ margin:0, fontSize:13, color:"#004D40", lineHeight:1.6 }}>{openRec.benefice}</p>
              </div>
              <div style={{ background:"white", borderRadius:16, padding:"20px", marginBottom:16, border:"1px solid #eee" }}>
                <h3 style={{ fontSize:16, fontWeight:900, color:"#1A1A1A", marginBottom:14 }}>Ingrédients</h3>
                <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8 }}>
                  {openRec.ingredients.map((ing,i) => (
                    <div key={i} style={{ fontSize:13, color:"#444", padding:"6px 0", borderBottom:"1px solid #f5f5f5" }}>• {ing}</div>
                  ))}
                </div>
              </div>
              <div style={{ background:"white", borderRadius:16, padding:"20px", border:"1px solid #eee" }}>
                <h3 style={{ fontSize:16, fontWeight:900, color:"#1A1A1A", marginBottom:14 }}>Étapes</h3>
                {openRec.etapes.map((e,i) => (
                  <div key={i} style={{ display:"flex", gap:16, marginBottom:16, alignItems:"flex-start" }}>
                    <span style={{ fontSize:32, fontWeight:900, color:"#9ACD32", lineHeight:1, minWidth:28, flexShrink:0 }}>{i+1}</span>
                    <p style={{ margin:0, fontSize:14, color:"#333", lineHeight:1.7 }}>{e}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

        return (
          <div style={{ position:"fixed", inset:0, background:"#F8FAFC", overflowY:"auto", fontFamily:"Arial, sans-serif" }}>
            {/* Header */}
            <div style={{ background:"#7C3AED", padding:"20px 24px" }}>
              <div style={{ fontSize:11, fontWeight:700, color:"rgba(255,255,255,0.75)", textTransform:"uppercase", letterSpacing:"1.5px", marginBottom:6 }}>QCM Santé — Résultats</div>
              <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:26, fontWeight:900, color:"white", margin:0 }}>✅ Mon profil santé</h1>
            </div>

            <div style={{ padding:"20px 24px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, maxWidth:900, margin:"0 auto" }}>

              {/* Alertes */}
              <div style={{ gridColumn:"1/-1", display:"flex", flexDirection:"column", gap:10 }}>
                {hasPoids && <div style={{ background:"#fbe9e7", border:"2px solid #e53935", borderRadius:12, padding:"14px 16px", fontSize:13, fontWeight:700, color:"#e53935" }}>⚠️ Perte de poids détectée — consultez votre médecin pour un bilan nutritionnel.</div>}
                {medasResult && <div style={{ background:medasResult.score>=10?"#e8f5e9":"#fff8e1", border:`2px solid ${medasResult.score>=10?"#2e7d32":"#f57c00"}`, borderRadius:12, padding:"14px 16px", fontSize:13, fontWeight:700, color:medasResult.score>=10?"#2e7d32":"#f57c00" }}>🫒 Score MEDAS : {medasResult.score}/14 — {medasResult.score>=10?"Forte adhésion au régime méditerranéen":medasResult.score>=6?"Adhésion modérée":"Faible adhésion — améliorez votre alimentation méditerranéenne"}</div>}
              </div>

              {/* Profil général */}
              <div style={{ background:"white", borderRadius:16, padding:"18px", border:"1px solid #eee", boxShadow:"0 2px 8px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#7C3AED", textTransform:"uppercase", letterSpacing:1, marginBottom:12 }}>👤 Profil général</div>
                {[["Âge",age],["Sexe",sexe],["Évolution",evolution],["Vit seul(e)",seul],["Mode de vie",modeVie],["Traitement",traitement]].filter(([,v])=>v).map(([k,v])=>(
                  <div key={k} style={{ display:"flex", justifyContent:"space-between", padding:"7px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                    <span style={{ color:"#888" }}>{k}</span><span style={{ fontWeight:800, color:"#333" }}>{v}</span>
                  </div>
                ))}
              </div>

              {/* Santé */}
              <div style={{ background:"white", borderRadius:16, padding:"18px", border:"1px solid #eee", boxShadow:"0 2px 8px rgba(0,0,0,0.06)" }}>
                <div style={{ fontSize:13, fontWeight:900, color:"#FA8072", textTransform:"uppercase", letterSpacing:1, marginBottom:12 }}>🏥 Santé</div>
                <div style={{ padding:"7px 0", borderBottom:"1px solid #f5f5f5", fontSize:13 }}>
                  <span style={{ color:"#888" }}>Maladie chronique</span><br/>
                  <span style={{ fontWeight:800, color:"#333" }}>{maladie}</span>
                </div>
                {pathologies.length>0 && !pathologies.includes("Aucune") && (
                  <div style={{ padding:"7px 0", fontSize:13 }}>
                    <span style={{ color:"#888" }}>Pathologies</span><br/>
                    <span style={{ fontWeight:800, color:"#7C3AED" }}>{pathologies.join(", ")}</span>
                  </div>
                )}
              </div>

              {/* Recettes méditerranéennes */}
              {hasLLC && medasResult && (
                <div style={{ gridColumn:"1/-1" }}>
                  <div style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:16, fontWeight:900, color:"#9ACD32", marginBottom:14 }}>🫒 Recettes méditerranéennes recommandées</div>
                  <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(200px, 1fr))", gap:14 }}>
                    {medsRecs.map((r,i) => (
                      <div key={i} onClick={() => setOpenRec(r)} style={{ background:"white", borderRadius:16, overflow:"hidden", border:"2px solid #9ACD3244", boxShadow:"0 2px 10px rgba(0,0,0,0.08)", cursor:"pointer", transition:"transform 0.15s, box-shadow 0.15s" }}
                        onMouseEnter={e=>{e.currentTarget.style.transform="translateY(-4px)";e.currentTarget.style.boxShadow="0 8px 24px rgba(154,205,50,0.25)";}}
                        onMouseLeave={e=>{e.currentTarget.style.transform="translateY(0)";e.currentTarget.style.boxShadow="0 2px 10px rgba(0,0,0,0.08)";}}>
                        <div style={{ height:110, overflow:"hidden", background:"#f0f9e0" }}>
                          <img src={r.image} alt={r.titre} style={{ width:"100%", height:"100%", objectFit:"cover" }} onError={e=>{e.target.style.display="none";}} />
                        </div>
                        <div style={{ padding:"12px 14px" }}>
                          <div style={{ fontSize:13, fontWeight:800, color:"#1A1A1A", lineHeight:1.3, marginBottom:6 }}>{r.titre}</div>
                          <div style={{ display:"flex", gap:6, flexWrap:"wrap" }}>
                            <span style={{ background:"#f0f9e0", borderRadius:8, padding:"3px 8px", fontSize:11, fontWeight:700, color:"#639922" }}>⏱ {r.temps}</span>
                            <span style={{ background:"#f0f9e0", borderRadius:8, padding:"3px 8px", fontSize:11, fontWeight:700, color:"#639922" }}>{r.type}</span>
                          </div>
                          <div style={{ marginTop:10, background:"#9ACD32", borderRadius:8, padding:"7px 10px", textAlign:"center", color:"white", fontSize:12, fontWeight:800 }}>Voir la recette →</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Bouton terminer */}
              <div style={{ gridColumn:"1/-1" }}>
                <button onClick={handleFinish} style={{ ...btn, background:"#7C3AED", color:"white", border:"3px solid #5b21b6", width:"100%", fontSize:16 }}>
                  Terminer mon profil santé →
                </button>
              </div>
            </div>
          </div>
        );
      })()}
    </div>
  );
}


/* ══ DASHBOARD ══ */
function DashboardScreen({ onBack, playerName }) {
  const [tab, setTab] = useState("apercu");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartsRef = useRef({});

  useEffect(() => {
    fetch("https://nutri-quest2.onrender.com/dashboard/stats")
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => { setError("Impossible de charger les donnees."); setLoading(false); });
  }, []);

  useEffect(() => {
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

  const exportData = (fmt) => window.open("https://nutri-quest2.onrender.com/export/"+fmt, "_blank");
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
                <Card title="Distribution MEDAS">
  <Leg items={[
    ["#e53935","0-2 : tres faible adhesion"],
    ["#f57c00","3-5 : faible"],
    ["#ffcc00","6-8 : moderee"],
    ["#9ACD32","9-11 : bonne"],
    ["#2e7d32","12-14 : excellente"]
  ]} />
  <div style={{ position:"relative", height:190 }}><canvas id="barMedas" role="img" aria-label="MEDAS dist">MEDAS dist</canvas></div>
</Card>
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
}

export default function App() {
  const [phase, setPhase] = useState("splash");
  const [playerName, setPlayerName] = useState("");
  const [playerInfos, setPlayerInfos] = useState({});
  const [isGuest, setIsGuest] = useState(false);
  const [avatarChoice, setAvatarChoice] = useState("fille");
  const [sceneIdx, setSceneIdx] = useState(0);
  const [currentNode, setCurrentNode] = useState(0);
  const [completedNodes, setCompletedNodes] = useState([]);
  const [mission4Unlocked, setMission4Unlocked] = useState(false);
  const [completedMissions, setCompletedMissions] = useState([]);
  const [santeCompleted, setSanteCompleted] = useState(false);
  const [nodeScenes, setNodeScenes] = useState([]);
  const [phaseHistory, setPhaseHistory] = useState([]);
  const [qcm2Compo, setQcm2Compo] = useState(null);
  const [qcm2Cuisine, setQcm2Cuisine] = useState(null);
  const [qcm1Nutrition, setQcm1Nutrition] = useState({});
  const [qcm2Answers, setQcm2Answers] = useState({});
  const [filtreRecetteProfil, setFiltreRecetteProfil] = useState(null);
  const [playerAge, setPlayerAge] = useState(null);
  const [santeData, setSanteData] = useState({});

  const goTo = (newPhase) => {
    setPhaseHistory(h => [...h, phase]);
    setPhase(newPhase);
  };
  const goBack = () => {
    if (phaseHistory.length > 0) {
      const prev = phaseHistory[phaseHistory.length - 1];
      setPhaseHistory(h => h.slice(0, -1));
      setPhase(prev);
    } else {
      setPhase("select");
    }
  };

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
    if (phase === "name")    return <NameScreen
      onConfirm={(name, infos) => { playSound("good"); setPlayerName(name); setPlayerInfos(infos||{}); setIsGuest(false); setCompletedNodes([]); setPhase("avatar"); }}
      onGuest={() => { playSound("good"); setPlayerName("Invité"); setPlayerInfos({}); setIsGuest(true); setCompletedNodes([]); setPhase("avatar"); }}
    />;
    if (phase === "avatar")  return <AvatarScreen playerName={playerName} onChoose={choice => { playSound("good"); setAvatarChoice(choice); setPhase("map"); }} />;
    if (phase === "scene")   return (
      <SceneScreen sceneIndex={sceneIdx} scenes={nodeScenes} playerName={playerName}
        avatarSrc={avatarChoice === "fille" ? "/fille.png" : "/garcon.png"}
        avatarGender={avatarChoice}
        onNext={() => { playSound("next"); handleSceneNext(); }}
        onSkipAll={() => { playSound("click"); setCompletedNodes(prev => prev.includes(currentNode) ? prev : [...prev, currentNode]); setPhase("map"); }} />
    );
    if (phase === "map")     return <MapScreen onSelectNode={handleSelectNode} completedNodes={completedNodes} activeNode={currentNode} />;
    if (phase === "minijeu") return <MinijeuScreen playerName={playerName} playerInfos={playerInfos} compoChoice={qcm2Compo} onBack={() => { setMission4Unlocked(true); setCompletedMissions(prev => prev.includes(2)?prev:[...prev,2]); setPhase("select_mission4"); setPhaseHistory([]); }} />;
    if (phase === "recettes") return <RecettesScreen cuisineChoice={qcm2Cuisine} filtreProfilInitial={filtreRecetteProfil} onBack={() => { setFiltreRecetteProfil(null); goBack(); }} />;
    if (phase === "profil_qcm1") return <ProfilQcm1Screen nutrition={qcm1Nutrition} playerName={playerName} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm1")} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;
    if (phase === "recos_qcm1") return <RecommandationsQcm1Screen nutrition={qcm1Nutrition} onBack={() => goBack()} onVoirRecettes={(profil) => { setFiltreRecetteProfil(profil); goTo("recettes"); }} />;
        if (phase === "select_mission4") return (
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
    if (phase === "dashboard") return <DashboardScreen onBack={() => { setPhase("select"); setPhaseHistory([]); }} playerName={playerName} />;
    if (phase === "felicitations") return (
      <div style={{ position:"fixed", inset:0, backgroundImage:"url('/fond_vert3.png')", backgroundSize:"cover", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", padding:"40px 24px" }}>
        <div style={{ position:"absolute", inset:0, background:"rgba(0,0,0,0.5)" }} />
        <div style={{ position:"relative", zIndex:2, display:"flex", flexDirection:"column", alignItems:"center", gap:32, maxWidth:780, width:"100%", textAlign:"center" }}>

          {/* Badge étoiles */}
          <div style={{ background:"linear-gradient(135deg, #ffdd44, #FA8072)", borderRadius:"50%", width:200, height:200, display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", boxShadow:"0 0 60px rgba(255,220,50,0.7), 0 12px 40px rgba(0,0,0,0.5)", border:"5px solid #fff" }}>
            <div style={{ fontSize:70 }}>🏆</div>
            <div style={{ fontSize:28, color:"white", letterSpacing:4 }}>★★★★★</div>
          </div>

          {/* Titre */}
          <div>
            <h1 style={{ fontFamily:"Arial Black, Arial, sans-serif", fontSize:52, fontWeight:900, color:"white", textShadow:"4px 4px 0 rgba(0,0,0,0.3)", margin:"0 0 12px", lineHeight:1.1 }}>
              Félicitations {playerName} ! 🎉
            </h1>
            <p style={{ color:"rgba(255,255,255,0.9)", fontSize:20, margin:0, lineHeight:1.6 }}>
              Tu as complété toutes les missions nutritionnelles !<br/>
              Ton profil complet a été enregistré.
            </p>
          </div>

          {/* Récap badges */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, width:"100%" }}>
            {[
              { icon:"🥗", label:"Habitudes alimentaires", color:"#FA8072" },
              { icon:"👨‍🍳", label:"Fabrique à Menus", color:"#ffcc00" },
              { icon:"🍽️", label:"Compose ton assiette", color:"#9ACD32" },
              { icon:"🏥", label:"Profil santé", color:"#7C3AED" },
            ].map((b,i) => (
              <div key={i} style={{ background:"rgba(255,255,255,0.18)", border:`3px solid ${b.color}`, borderRadius:20, padding:"20px 24px", display:"flex", alignItems:"center", gap:16, boxShadow:`0 4px 20px ${b.color}44` }}>
                <span style={{ fontSize:40 }}>{b.icon}</span>
                <div style={{ textAlign:"left" }}>
                  <div style={{ fontSize:16, fontWeight:900, color:"white", marginBottom:4 }}>{b.label}</div>
                  <div style={{ fontSize:14, color:"#ffdd44", fontWeight:800, letterSpacing:2 }}>★★★★★ Complété</div>
                </div>
              </div>
            ))}
          </div>

          {/* Boutons */}
          <div style={{ display:"flex", flexDirection:"column", gap:14, width:"100%" }}>
            <button onClick={() => { setPhase("dashboard"); setPhaseHistory([]); }}
              style={{ background:"#ffdd44", border:"4px solid #222", borderRadius:16, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:20, fontWeight:900, padding:"20px", cursor:"pointer", boxShadow:"6px 6px 0 #222" }}>
              📊 Accéder à mon dashboard →
            </button>
            <button onClick={() => { setPhase("select"); setPhaseHistory([]); }}
              style={{ background:"rgba(255,255,255,0.15)", border:"2px solid rgba(255,255,255,0.5)", borderRadius:14, color:"white", fontSize:16, fontWeight:700, padding:"14px", cursor:"pointer" }}>
              ← Retour au menu
            </button>
          </div>

        </div>
      </div>
    );
    if (phase === "qcm_sante") return <QcmSanteScreen onBack={() => goBack()} onDone={(data) => { setSanteData(data); setSanteCompleted(true); setCompletedMissions(prev => prev.includes(3)?prev:[...prev,3]); setPhase("felicitations"); setPhaseHistory([]); }} playerName={playerName} playerInfos={playerInfos} />;
    if (phase === "qcm1")    return <Qcm1Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(nut) => { setQcm1Nutrition(nut); }} onDone={(nut) => { setQcm1Nutrition(nut); setCompletedMissions(prev => prev.includes(0)?prev:[...prev,0]); }} onShowRecos={(nut) => { setQcm1Nutrition(nut); goTo("profil_qcm1"); }} />;
    if (phase === "qcm2")    return <Qcm2Screen playerName={playerName} playerInfos={playerInfos} onBack={() => { playSound("click"); goBack(); }} onDone={(compo, cuisine, ans) => { setQcm2Compo(compo); setQcm2Cuisine(cuisine); if(ans) setQcm2Answers(ans); if(cuisine==="recettes") goTo("recettes"); else if(cuisine==="recos") goTo("recos_qcm2"); else if(cuisine==="sante") goTo("qcm_sante"); else goTo("profil_qcm2"); }} />;
    if (phase === "au_programme") return <AuProgrammeScreen playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onRecos={() => goTo("recos_qcm2")} />;
    if (phase === "profil_qcm2") return <ProfilQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onSuivant={() => goTo("intro_recos_qcm2")} />;
    if (phase === "intro_recos_qcm2") return <IntroRecosQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onVoirRecos={() => goTo("recos_qcm2")} onVoirRecettes={() => { setFiltreRecetteProfil(null); goTo("recettes"); }} />;
    if (phase === "recos_qcm2") return <RecommandationsQcm2Screen answers={qcm2Answers} playerName={playerName} avatarChoice={avatarChoice} onBack={() => goBack()} onMinijeu={() => { setPhase("minijeu"); setPhaseHistory([]); }} />;
    return <QcmSelectScreen playerName={playerName}
      onStartQcm1={() => { playSound("click"); goTo("qcm1"); }}
      onStartQcm2={() => { playSound("click"); goTo("qcm2"); }}
      onStartMinijeu={() => { playSound("click"); goTo("minijeu"); }}
      onStartSante={() => { playSound("click"); goTo("qcm_sante"); }}
      mission4Unlocked={mission4Unlocked}
      completedMissions={completedMissions}
      onDashboard={() => { setPhase("dashboard"); setPhaseHistory([]); }} />;
  })();

  return (
    <>
      <GlobalStyles />
      <div style={{ visibility: ["splash","intro","name","scene"].includes(phase) ? "hidden" : "visible" }}>
        <HamburgerMenu
          playerName={playerName}
          playerInfos={playerInfos}
          isGuest={isGuest}
          onSaveProfile={(name, infos) => { setPlayerName(name); setPlayerInfos(infos); }}
        />
      </div>
      {screen}
    </>
  );
}