#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lignes: {len(lines)}")

# Afficher les lignes autour de 2394
start = max(0, 2394-10)
end = min(len(lines), 2394+20)
print(f"\n=== Lignes {start}-{end} ===")
for i, l in enumerate(lines[start:end], start=start+1):
    print(f"{i:4}: {l}", end="")

# Chercher tous les useEffect dans Qcm2Screen
print("\n\n=== Tous les useEffect dans le fichier ===")
for i, l in enumerate(lines, 1):
    if 'useEffect' in l:
        print(f"L{i:4}: {l.rstrip()}")

# Chercher le bloc if(done) avec useEffect
print("\n\n=== Blocs if(done) ===")
code = ''.join(lines)
idx = 0
while True:
    idx = code.find('if (done)', idx)
    if idx == -1:
        break
    line_no = code[:idx].count('\n') + 1
    print(f"\nL{line_no}: {repr(code[idx:idx+200])}")
    idx += 1
