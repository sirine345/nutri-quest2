"""
PATCH 23 — Remplace React.useState par useState dans RecommandationsQcm2Screen
Usage: python patch_23_fix_react.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

replacements = [
    ('const [onglet, setOnglet] = React.useState("pour_vous");', 'const [onglet, setOnglet] = useState("pour_vous");'),
    ('const [dateDebut, setDateDebut] = React.useState("");', 'const [dateDebut, setDateDebut] = useState("");'),
    ('const [dateFin, setDateFin] = React.useState("");', 'const [dateFin, setDateFin] = useState("");'),
    ('const [planning, setPlanning] = React.useState(null);', 'const [planning, setPlanning] = useState(null);'),
]

fixes = 0
for old, new in replacements:
    if old in code:
        code = code.replace(old, new)
        fixes += 1
        print(f"✅ {new[:50]}...")

print(f"\n{fixes}/4 fix(es) appliqué(s)")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
