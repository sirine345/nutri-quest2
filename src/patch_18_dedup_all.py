"""
PATCH 18 — Supprime TOUS les doublons en une seule passe
Garde toujours la DERNIÈRE occurrence de chaque fonction
Usage: python patch_18_dedup_all.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total avant: {len(lines)} lignes")

FUNCS_TO_DEDUP = [
    'ProfilQcm2Screen',
    'AuProgrammeScreen', 
    'IntroRecosQcm2Screen',
]

def find_func_end(lines, start_idx):
    depth = 0
    for i in range(start_idx, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth <= 0 and i > start_idx:
            return i
    return len(lines) - 1

# Collecte tous les blocs à supprimer
all_blocks_to_remove = []

for fn in FUNCS_TO_DEDUP:
    starts = [i for i, l in enumerate(lines) if f'function {fn}' in l]
    if len(starts) <= 1:
        print(f"✅ {fn}: pas de doublon")
        continue
    
    print(f"⚠️  {fn}: {len(starts)} déclarations → lignes {[s+1 for s in starts]}")
    
    for s in starts[:-1]:  # Garde le dernier
        # Cherche commentaire précédent
        block_start = s
        for offset in range(1, 4):
            if s - offset >= 0 and ('/* ══' in lines[s-offset] or lines[s-offset].strip() == ''):
                if '/* ══' in lines[s-offset]:
                    block_start = s - offset
                    break
        
        block_end = find_func_end(lines, s)
        all_blocks_to_remove.append((block_start, block_end))
        print(f"   Suppression lignes {block_start+1}–{block_end+1}")

# Trie et déduplique les blocs
all_blocks_to_remove = sorted(set(all_blocks_to_remove), reverse=True)

# Supprime de la fin vers le début
for start, end in all_blocks_to_remove:
    del lines[start:end+1]

print(f"\nTotal après: {len(lines)} lignes")
print(f"✅ {len(all_blocks_to_remove)} bloc(s) supprimé(s)")

# Vérification
for fn in FUNCS_TO_DEDUP:
    count = sum(1 for l in lines if f'function {fn}' in l)
    print(f"  {fn}: {count} déclaration(s)")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\nFichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
