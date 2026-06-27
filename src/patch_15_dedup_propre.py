"""
PATCH 15 — Suppression propre des doublons ProfilQcm2Screen
Garde seulement la DERNIÈRE occurrence (ligne 2515 dans l'original)
Usage: python patch_15_dedup_propre.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

def find_function_block(code, func_match):
    """Trouve le début du bloc (avec commentaire) et la fin de la fonction"""
    start = func_match.start()
    # Cherche le commentaire qui précède
    comment_search = code.rfind('\n/* ══', 0, start)
    if comment_search != -1 and comment_search > start - 150:
        block_start = comment_search + 1  # +1 pour sauter le \n
    else:
        block_start = start
    
    # Trouve la fin de la fonction en comptant les accolades
    depth = 0
    i = start
    started = False
    while i < len(code):
        if code[i] == '{':
            depth += 1
            started = True
        elif code[i] == '}':
            depth -= 1
            if started and depth == 0:
                # Skip trailing newlines
                end = i + 1
                while end < len(code) and code[end] == '\n':
                    end += 1
                return block_start, end
        i += 1
    return block_start, len(code)

all_matches = list(re.finditer(r'function ProfilQcm2Screen', code))
print(f"Trouvé {len(all_matches)} déclarations ProfilQcm2Screen")

if len(all_matches) <= 1:
    print("✅ Pas de doublon")
else:
    # Garde la dernière, supprime les autres
    to_remove = []
    for m in all_matches[:-1]:
        line = code[:m.start()].count('\n') + 1
        start, end = find_function_block(code, m)
        to_remove.append((start, end))
        print(f"  Suppression ligne {line} (pos {start}-{end})")
    
    # Supprime de la fin vers le début
    for start, end in reversed(to_remove):
        code = code[:start] + code[end:]
    
    print(f"✅ {len(to_remove)} doublon(s) supprimé(s)")

# Vérification finale
remaining = list(re.finditer(r'function ProfilQcm2Screen', code))
print(f"Après nettoyage: {len(remaining)} déclaration(s)")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
