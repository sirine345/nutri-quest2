#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

print(f"Taille: {len(code)} chars")

idx = code.find("function QcmSanteScreen(")
print(f"QcmSanteScreen a: {idx}")
print(f"\n--- Lignes 1-50 de QcmSanteScreen ---")
extrait = code[idx:idx+2000]
for i, ligne in enumerate(extrait.split('\n')[:50], 1):
    print(f"{i:3}: {ligne}")
