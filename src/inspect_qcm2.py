#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

# Lire le début de Qcm1Screen pour voir le style du header et des boutons
idx = 145218
print("=== DEBUT QCM1SCREEN ===")
print(code[idx:idx+3000])
