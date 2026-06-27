"""
PATCH 16 — Répare la ligne 1751 cassée : ajoute la signature manquante
Usage: python patch_16_fix_line1751.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

# Le problème: le patch 14 a supprimé "function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }"
# mais a laissé ") {" orphelin à la ligne 1751

OLD = '\n) {\n  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";'
NEW = '\n/* ══ PAGE RÉCAP QCM2 ══ */\nfunction ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {\n  const avatarSrc = avatarChoice === "fille" ? "/fille.png" : "/garcon.png";'

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ FIX 1 — Signature ProfilQcm2Screen restaurée ligne 1751")
else:
    # Try with \r\n
    OLD2 = '\r\n) {\r\n  const avatarSrc'
    NEW2 = '\r\n/* ══ PAGE RÉCAP QCM2 ══ */\r\nfunction ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {\r\n  const avatarSrc'
    if OLD2 in code:
        code = code.replace(OLD2, NEW2)
        print("✅ FIX 1 — Signature restaurée (CRLF)")
    else:
        print("⚠️  Tentative directe par numéro de ligne...")
        lines = code.split('\n')
        # Find the orphan ) {
        for i, line in enumerate(lines):
            if line.strip() == ') {' and i > 1748 and i < 1755:
                lines[i] = 'function ProfilQcm2Screen({ answers, playerName, avatarChoice, onSuivant, onBack }) {'
                # Add comment before
                lines.insert(i, '/* ══ PAGE RÉCAP QCM2 ══ */')
                print(f"✅ FIX 1 — Ligne {i+1} corrigée directement")
                break
        code = '\n'.join(lines)

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
