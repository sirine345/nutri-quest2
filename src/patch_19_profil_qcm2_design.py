"""
PATCH 19 — ProfilQcm2Screen : grands personnages, dialogue en avant, tout sur une page
Usage: python patch_19_profil_qcm2_design.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find ProfilQcm2Screen
starts = [i for i, l in enumerate(lines) if 'function ProfilQcm2Screen' in l]
if not starts:
    print("⚠️  ProfilQcm2Screen non trouvé")
    sys.exit(1)

start_idx = starts[0]
# Find comment before
block_start = start_idx
for offset in range(1, 4):
    if start_idx - offset >= 0 and '/* ══' in lines[start_idx - offset]:
        block_start = start_idx - offset
        break

# Find end
def find_end(lines, start):
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth <= 0 and i > start:
            return i
    return len(lines) - 1

block_end = find_end(lines, start_idx)
print(f"ProfilQcm2Screen: lignes {block_start+1}–{block_end+1}")

NEW_BLOCK = '''/* ══ PAGE RÉCAP QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";
  const cuisine   = answers["‍ En cuisine"] || "—";
  const pratiques = answers[" Pratiques alimentaires"] || "—";
  const compo     = answers[" Composition du repas"] || "—";
  const nbPersons = answers[" Nombre de personnes"] || "—";
  const nbRepas   = answers[" Nombre de repas"] || "—";

  const LIGNES = [
    { label:"Personnes", value:nbPersons,  icon:"👥" },
    { label:"Pratiques", value:pratiques,  icon:"🥗" },
    { label:"Composition", value:compo,   icon:"🍽️" },
    { label:"Cuisine",   value:cuisine,   icon:"⏱️" },
    { label:"Repas/jour", value:nbRepas,  icon:"📅" },
  ];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column", overflow:"hidden" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"12px 20px", textAlign:"center", flexShrink:0, position:"relative" }}>
        <button onClick={onBack} style={{ position:"absolute", left:16, top:"50%", transform:"translateY(-50%)", background:"rgba(255,255,255,0.2)", border:"2px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"5px 12px" }}>← Retour</button>
        <div style={{ fontSize:18, fontWeight:900, color:"white", fontFamily:"Arial Black, Arial, sans-serif" }}>⭐ Profil créé ! ⭐</div>
        <div style={{ fontSize:11, color:"rgba(255,255,255,0.9)", marginTop:2 }}>Voici ton profil alimentaire personnalisé</div>
      </div>

      {/* Corps principal — tout sur une ligne */}
      <div style={{ flex:1, display:"flex", overflow:"hidden" }}>

        {/* MAX — grand à gauche */}
        <div style={{ width:220, flexShrink:0, background:"#fff8f0", borderRight:"2px solid #eee", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"flex-end", padding:"0 16px 16px", gap:8 }}>
          <img src="/e.png" alt="Max" style={{ width:180, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"#e8f5e9", border:"2px solid #9ACD32", borderRadius:"12px 12px 12px 4px", padding:"10px 12px", fontSize:12, color:"#2e7d32", lineHeight:1.6, textAlign:"center", width:"100%" }}>
            Wow ! 🌟 Tu viens de compléter ton profil alimentaire ! Regardons ensemble tes habitudes.
          </div>
          <div style={{ fontSize:11, fontWeight:900, color:"#FA8072", background:"#fff0ee", border:"1px solid #FA807244", borderRadius:20, padding:"3px 12px" }}>Max</div>
        </div>

        {/* RÉCAP — centre */}
        <div style={{ flex:1, padding:"16px 20px", overflowY:"auto" }}>
          <div style={{ fontSize:12, fontWeight:900, color:"#888", textTransform:"uppercase", letterSpacing:"1px", marginBottom:12 }}>Récapitulatif de tes habitudes</div>

          {/* Grille compacte 2 colonnes */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:12 }}>
            {LIGNES.map((l, i) => (
              <div key={i} style={{ background:"white", borderRadius:10, padding:"10px 12px", border:"1.5px solid #eee", display:"flex", alignItems:"center", gap:8 }}>
                <span style={{ fontSize:18, flexShrink:0 }}>{l.icon}</span>
                <div style={{ minWidth:0 }}>
                  <div style={{ fontSize:10, color:"#aaa", fontWeight:700, marginBottom:1 }}>{l.label}</div>
                  <div style={{ fontSize:12, fontWeight:800, color:"#1A1A1A", whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis" }}>{l.value}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Message étoile */}
          <div style={{ background:"#fff8e1", borderRadius:10, padding:"10px 14px", fontSize:12, color:"#f57c00", marginBottom:12 }}>
            ⭐ Ton profil est unique, chaque petit pas compte pour ta santé !
          </div>

          {/* Bouton suivant */}
          <button onClick={onSuivant}
            style={{ width:"100%", background:"#9ACD32", border:"3px solid #222", borderRadius:12, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:15, fontWeight:900, padding:"13px", cursor:"pointer", boxShadow:"4px 4px 0 #222" }}>
            Suivant →
          </button>
        </div>

        {/* AVATAR joueur — grand à droite */}
        <div style={{ width:200, flexShrink:0, background:"#f0f7ff", borderLeft:"2px solid #eee", display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"flex-end", padding:"0 16px 16px", gap:8 }}>
          <img src={avatarSrc} alt={playerName} style={{ width:160, filter:"drop-shadow(3px 3px 0 rgba(0,0,0,0.2))" }} />
          <div style={{ background:"white", border:"2px solid #1976d2", borderRadius:"12px 12px 4px 12px", padding:"10px 12px", fontSize:12, color:"#1976d2", lineHeight:1.6, textAlign:"center", width:"100%" }}>
            D'accord Max, je suis curieux(se) de voir ! 👀
          </div>
          <div style={{ fontSize:11, fontWeight:900, color:"#1976d2", background:"#e3f2fd", border:"1px solid #1976d244", borderRadius:20, padding:"3px 12px" }}>{playerName}</div>
        </div>

      </div>
    </div>
  );
}

'''

lines[block_start:block_end+1] = [NEW_BLOCK]
print("✅ FIX 1 — ProfilQcm2Screen redesigné")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
