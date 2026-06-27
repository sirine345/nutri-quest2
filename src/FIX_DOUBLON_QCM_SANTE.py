#!/usr/bin/env python3
"""Supprime le doublon de QcmSanteScreen"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

idx1 = code.find("function QcmSanteScreen(")
idx2 = code.find("function QcmSanteScreen(", idx1 + 1)
print(f"QcmSanteScreen 1: {idx1}")
print(f"QcmSanteScreen 2: {idx2}")

if idx2 == -1:
    print("Pas de doublon")
else:
    # Garder la 2eme (la nouvelle), supprimer la 1ere
    debut1 = code.rfind("\n/*", 0, idx1)
    if debut1 == -1:
        debut1 = code.rfind("\n\n", 0, idx1)
    
    # Fin du 1er bloc = debut du 2eme bloc
    debut2 = code.rfind("\n/*", 0, idx2)
    
    print(f"Suppression bloc 1: {debut1} -> {debut2}")
    print(f"Debut: {repr(code[debut1:debut1+60])}")
    print(f"Fin: {repr(code[debut2:debut2+60])}")
    
    code = code[:debut1] + code[debut2:]
    
    # Verifier
    c1 = code.find("function QcmSanteScreen(")
    c2 = code.find("function QcmSanteScreen(", c1+1)
    print(f"Apres - QcmSanteScreen: {c1}, doublon: {c2}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print(f"OK App.jsx ecrit ({len(code)} chars)!")
