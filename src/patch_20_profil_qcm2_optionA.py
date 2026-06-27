"""
PATCH 20 — ProfilQcm2Screen : Option A (personnages en haut, récap en bas, bouton petit)
Usage: python patch_20_profil_qcm2_optionA.py App.jsx
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
print(f"Remplacement lignes {block_start+1}–{block_end+1}")

NEW_BLOCK = '''/* ══ PAGE RÉCAP QCM2 ══ */
function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {
  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";
  const cuisine   = answers["‍ En cuisine"] || "—";
  const pratiques = answers[" Pratiques alimentaires"] || "—";
  const compo     = answers[" Composition du repas"] || "—";
  const nbPersons = answers[" Nombre de personnes"] || "—";
  const nbRepas   = answers[" Nombre de repas"] || "—";

  const LIGNES = [
    { icon:"ti-users",           label:"Nombre de personnes",   val:nbPersons },
    { icon:"ti-leaf",            label:"Pratiques alimentaires", val:pratiques },
    { icon:"ti-bowl-chopsticks", label:"Composition du repas",  val:compo     },
    { icon:"ti-clock",           label:"Temps en cuisine",       val:cuisine   },
    { icon:"ti-calendar",        label:"Repas par jour",         val:nbRepas   },
  ];

  return (
    <div style={{ position:"fixed", inset:0, background:"#FFF5EE", fontFamily:"Arial, sans-serif", display:"flex", flexDirection:"column" }}>

      {/* Header */}
      <div style={{ background:"#FA8072", padding:"12px 20px", textAlign:"center", flexShrink:0, position:"relative" }}>
        <button onClick={onBack} style={{ position:"absolute", left:12, top:"50%", transform:"translateY(-50%)", background:"rgba(255,255,255,0.2)", border:"1px solid rgba(255,255,255,0.4)", borderRadius:8, color:"white", fontSize:12, fontWeight:700, cursor:"pointer", padding:"4px 10px" }}>← Retour</button>
        <div style={{ fontSize:16, fontWeight:900, color:"white", fontFamily:"Arial Black, Arial, sans-serif" }}>⭐ Profil créé ! ⭐</div>
        <div style={{ fontSize:11, color:"rgba(255,255,255,0.85)", marginTop:2 }}>Voici ton profil alimentaire personnalisé</div>
      </div>

      {/* Personnages en haut */}
      <div style={{ background:"#fff8f0", borderBottom:"2px solid #eee", padding:"16px 30px 0", display:"flex", justifyContent:"space-around", alignItems:"flex-end", flexShrink:0 }}>

        {/* Max */}
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
          <img src="/e.png" alt="Max" style={{ height:160, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.15))" }} />
          <div style={{ background:"#e8f5e9", border:"1.5px solid #9ACD32", borderRadius:"10px 10px 10px 3px", padding:"8px 12px", fontSize:11, color:"#27500A", lineHeight:1.5, textAlign:"center", maxWidth:160 }}>
            Wow ! Tu viens de compléter ton profil alimentaire ! Regardons ensemble tes habitudes.
          </div>
          <span style={{ fontSize:11, fontWeight:700, color:"#FA8072", background:"#fff0ee", padding:"2px 10px", borderRadius:20, border:"1px solid #FA807244", marginBottom:4 }}>Max</span>
        </div>

        {/* Avatar */}
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
          <img src={avatarSrc} alt={playerName} style={{ height:130, objectFit:"contain", filter:"drop-shadow(2px 2px 0 rgba(0,0,0,0.15))" }} />
          <div style={{ background:"white", border:"1.5px solid #1976d2", borderRadius:"10px 10px 3px 10px", padding:"8px 12px", fontSize:11, color:"#0C447C", lineHeight:1.5, textAlign:"center", maxWidth:150 }}>
            D'accord Max, je suis curieux(se) de voir ! 👀
          </div>
          <span style={{ fontSize:11, fontWeight:700, color:"#1976d2", background:"#e3f2fd", padding:"2px 10px", borderRadius:20, border:"1px solid #1976d244", marginBottom:4 }}>{playerName}</span>
        </div>

      </div>

      {/* Récap compact */}
      <div style={{ flex:1, padding:"14px 20px", overflowY:"auto" }}>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:8, marginBottom:10 }}>
          {LIGNES.map((l, i) => (
            <div key={i} style={{ background:"white", borderRadius:10, padding:"8px 10px", border:"1px solid #eee", display:"flex", alignItems:"center", gap:7 }}>
              <i className={"ti " + l.icon} style={{ fontSize:16, color:"#FA8072", flexShrink:0 }} />
              <div style={{ minWidth:0 }}>
                <div style={{ fontSize:9, color:"#aaa", fontWeight:600, marginBottom:1 }}>{l.label}</div>
                <div style={{ fontSize:11, fontWeight:800, color:"#1A1A1A", whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis" }}>{l.val}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ background:"#fff8e1", borderRadius:8, padding:"8px 12px", fontSize:11, color:"#854F0B", marginBottom:12 }}>
          ⭐ Ton profil est unique, chaque petit pas compte pour ta santé !
        </div>

        <div style={{ display:"flex", justifyContent:"flex-end" }}>
          <button onClick={onSuivant}
            style={{ background:"#9ACD32", border:"2px solid #222", borderRadius:10, color:"#222", fontFamily:"Arial Black, Arial, sans-serif", fontSize:13, fontWeight:900, padding:"9px 22px", cursor:"pointer", boxShadow:"3px 3px 0 #222" }}>
            Suivant →
          </button>
        </div>
      </div>

    </div>
  );
}

'''

lines[block_start:block_end+1] = [NEW_BLOCK]
print("✅ FIX 1 — ProfilQcm2Screen option A appliqué")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
