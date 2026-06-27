"""
PATCH 14 — Supprimer les doublons de ProfilQcm2Screen
Usage: python patch_14_dedup.py App.jsx
"""
import sys, re

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

def find_function_end(code, start):
    """Find the end of a function starting at position start"""
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
                return i + 1
        i += 1
    return len(code)

# Find all ProfilQcm2Screen declarations
matches = list(re.finditer(r'/\* ══ PAGE RÉCAP QCM2 ══ \*/\nfunction ProfilQcm2Screen', code))
print(f"Trouvé {len(matches)} blocs ProfilQcm2Screen avec marqueur")

# Also find without marker
all_matches = list(re.finditer(r'function ProfilQcm2Screen', code))
print(f"Total déclarations: {len(all_matches)}")

if len(all_matches) > 1:
    # Keep only the LAST one (most recent patch), remove the others
    # Find the full block for each (including the preceding comment if any)
    blocks_to_remove = []
    
    for m in all_matches[:-1]:  # All except the last
        start = m.start()
        # Check if there's a comment before
        comment_start = code.rfind('/* ══', 0, start)
        if comment_start != -1 and comment_start > start - 100:
            start = comment_start
        end = find_function_end(code, m.start())
        # Skip trailing newlines
        while end < len(code) and code[end] in '\n\r':
            end += 1
        blocks_to_remove.append((start, end))
        line = code[:m.start()].count('\n') + 1
        print(f"  → Suppression du bloc ligne {line} (positions {start}-{end})")
    
    # Remove from end to start to preserve positions
    for start, end in reversed(blocks_to_remove):
        code = code[:start] + code[end:]
    
    print(f"✅ {len(blocks_to_remove)} doublon(s) supprimé(s)")
else:
    print("✅ Aucun doublon trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
