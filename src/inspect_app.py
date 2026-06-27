#!/usr/bin/env python3
"""Inspect App.jsx pour trouver les bonnes strings"""
import os, re

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

print(f"Taille: {len(code)} chars\n")

# 1. Chercher le bloc "if (done)" dans Qcm2Screen
idx = code.find('if (done) {')
while idx != -1:
    print(f"=== 'if (done)' à {idx} ===")
    print(repr(code[idx:idx+400]))
    print()
    idx = code.find('if (done) {', idx+1)

# 2. Chercher useEffect dans Qcm2Screen
idx2 = code.find('Notify parent when done')
if idx2 > 0:
    print(f"=== useEffect original à {idx2} ===")
    print(repr(code[idx2:idx2+300]))
    print()

# 3. Chercher bouton retour step1
idx3 = code.find('onBack} style={{ ...btn, background:"#f5f5f5"')
if idx3 > 0:
    print(f"=== Bouton retour step1 à {idx3} ===")
    print(repr(code[idx3:idx3+200]))
else:
    # Chercher la zone du step 1
    idx3 = code.find('"Nombre de personnes à table"')
    if idx3 > 0:
        print(f"=== Zone step1 QCM2 à {idx3} ===")
        # Chercher bouton retour dans les 500 chars avant
        zone = code[max(0,idx3-800):idx3+200]
        print(repr(zone[-600:]))

