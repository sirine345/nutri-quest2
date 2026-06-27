#!/usr/bin/env python3
"""Supprime le doublon de MnaScreen"""
import os

src = os.path.join(os.path.dirname(__file__), "App.jsx")
with open(src, "r", encoding="utf-8") as f:
    code = f.read()
print(f"Lu {len(code)} chars")

# Trouver les deux occurrences de MnaScreen
idx1 = code.find("function MnaScreen(")
idx2 = code.find("function MnaScreen(", idx1 + 1)
print(f"MnaScreen 1: {idx1}")
print(f"MnaScreen 2: {idx2}")

if idx2 == -1:
    print("Pas de doublon trouve — autre probleme")
else:
    # Garder la premiere, supprimer la seconde
    # Trouver le debut du bloc (commentaire avant)
    debut = code.rfind("\n/*", 0, idx2)
    if debut == -1:
        debut = code.rfind("\nfunction", 0, idx2)
    
    # Trouver la fin du bloc (prochain /* ou function au meme niveau)
    # Chercher la fonction suivante apres idx2
    next_fn = code.find("\n/*", idx2 + 1)
    if next_fn == -1:
        next_fn = code.find("\nfunction ", idx2 + 1)
    
    print(f"Suppression: {debut} -> {next_fn}")
    print(f"Debut: {repr(code[debut:debut+60])}")
    print(f"Fin: {repr(code[next_fn:next_fn+60])}")
    
    code = code[:debut] + code[next_fn:]
    print(f"Nouvelle taille: {len(code)}")

    # Verifier qu'il n'y a plus de doublon
    c1 = code.find("function MnaScreen(")
    c2 = code.find("function MnaScreen(", c1+1)
    print(f"Apres correction - MnaScreen: {c1}, doublon: {c2}")

with open(src, "w", encoding="utf-8") as f:
    f.write(code)
print("OK App.jsx ecrit!")
