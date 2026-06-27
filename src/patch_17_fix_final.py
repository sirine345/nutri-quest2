"""
PATCH 17 — Supprime proprement les 2 premiers doublons de ProfilQcm2Screen
Garde uniquement la 3ème (ligne 2515), supprime lignes 1751-1845 et 2309-2421
Usage: python patch_17_fix_final.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total avant: {len(lines)} lignes")

def find_func_end(lines, start_idx):
    depth = 0
    for i in range(start_idx, len(lines)):
        depth += lines[i].count('{') - lines[i].count('}')
        if depth <= 0 and i > start_idx:
            return i
    return len(lines) - 1

# Trouve les 3 occurrences
import re
starts = []
for i, l in enumerate(lines):
    if 'function ProfilQcm2Screen' in l:
        starts.append(i)
        print(f"  Déclaration ligne {i+1}")

if len(starts) <= 1:
    print("✅ Pas de doublon")
else:
    # Pour chaque doublon (sauf le dernier), trouve le bloc complet
    # incluant le commentaire /* ══ PAGE RÉCAP QCM2 ══ */ qui précède
    blocks_to_remove = []
    for s in starts[:-1]:  # Tous sauf le dernier
        # Cherche le commentaire qui précède (1-2 lignes avant)
        block_start = s
        if s > 0 and '/* ══ PAGE RÉCAP QCM2 ══ */' in lines[s-1]:
            block_start = s - 1
        elif s > 1 and '/* ══ PAGE RÉCAP QCM2 ══ */' in lines[s-2]:
            block_start = s - 2
        
        block_end = find_func_end(lines, s)
        blocks_to_remove.append((block_start, block_end))
        print(f"  → Suppression lignes {block_start+1} à {block_end+1}")
    
    # Supprime de la fin vers le début pour préserver les indices
    for start, end in reversed(blocks_to_remove):
        del lines[start:end+1]
    
    print(f"✅ {len(blocks_to_remove)} doublon(s) supprimé(s)")

print(f"Total après: {len(lines)} lignes")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
