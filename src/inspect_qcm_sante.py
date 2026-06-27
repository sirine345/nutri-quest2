#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

# Trouver QcmSanteScreen
idx = code.find("function QcmSanteScreen(")
print(f"QcmSanteScreen à: {idx}")
# Afficher les 300 premiers chars
print(repr(code[idx:idx+400]))

# Trouver le style du header du QCM1 pour réutiliser
idx2 = code.find("function Qcm1Screen(")
print(f"\nQcm1Screen à: {idx2}")
print(repr(code[idx2:idx2+300]))
