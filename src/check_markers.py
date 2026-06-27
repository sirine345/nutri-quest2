#!/usr/bin/env python3
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()

START = "/* ══ ÉCRAN RECOMMANDATIONS QCM1 ══ */"
END   = "/* ══ ÉCRAN RECOMMANDATIONS QCM2 ══ */"

print(f"Taille: {len(code)} chars")
print(f"START trouvé: {code.find(START)}")
print(f"END trouvé: {code.find(END)}")

# Show what's around START
idx = code.find(START)
if idx >= 0:
    print(f"\nContenu après START (100 chars):")
    print(repr(code[idx:idx+100]))
else:
    # Try to find similar
    print("\nRecherche alternative...")
    for variant in ["RECOMMANDATIONS QCM1", "RecommandationsQcm1", "ÉCRAN RECOMMANDATIONS"]:
        i = code.find(variant)
        print(f"  '{variant}': {i}")
        if i >= 0:
            print(f"  Contexte: {repr(code[i-5:i+50])}")
