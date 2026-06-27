"""
PATCH 21 — ProfilQcm2Screen : TOUT plus grand (personnages, cartes, police)
Usage: python patch_21_profil_qcm2_grand.py App.jsx
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

starts = [i for i, l in enumerate(lines) if 'function ProfilQcm2Screen' in l]
if not starts:
    print("⚠️  ProfilQcm2Screen non trouvé")
    sys.exit(1)

start_idx = starts[0]
block_start = start_idx
for offset in range(1, 4):
    if start_idx - offset >= 0 and '/* ══' in lines[start_idx - offset]:
        block_start = start_idx - offset
        break

block_end = find_func_end(lines, start_idx)

NEW_BLOCK = '''/* ══ PAGE RÉCAP QCM2 ══ */
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

'''

lines[block_start:block_end+1] = [NEW_BLOCK]
print("✅ FIX 1 — ProfilQcm2Screen : tout agrandi")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
