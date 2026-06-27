"""
PATCH 40 — Corrige le regex avec caractères accentués dans IngredientsBlock
Usage: python patch_40_fix_regex.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix the regex - replace accented chars with unicode escapes
old = 'const m = ing.match(/^([\\d]+(?:[.,][\\d]+)?)\\s*([a-zA-Zàâéèêëîïôùûüç]+(?:\\s?à\\s?[a-zA-Z]+)?)?\\s+(.+)$/);'
new = 'const m = ing.match(/^([\\d]+(?:[.,][\\d]+)?)\\s*([a-zA-Z\\u00e0\\u00e2\\u00e9\\u00e8\\u00ea\\u00eb\\u00ee\\u00ef\\u00f4\\u00f9\\u00fb\\u00fc\\u00e7]+(?:\\s?[a-z]+\\s?[a-zA-Z]+)?)?\\s+(.+)$/);'

if old in content:
    content = content.replace(old, new)
    print("✅ Regex corrigé (caractères accentués → unicode escapes)")
else:
    # Try finding it differently
    import re
    m = re.search(r'ing\.match\(/\^.*?àâé.*?\$/\)', content)
    if m:
        old_found = m.group(0)
        new_simple = "const m = ing.match(/^([\\d]+(?:[.,][\\d]+)?)\\s*([a-zA-Z]+(?:\\s?[a-z]+\\s?[a-zA-Z]+)?)?\\s+(.+)$/);"
        content = content.replace("const m = " + old_found + ";", new_simple)
        print("✅ Regex simplifié")
    else:
        # Direct line replacement
        lines = content.split('\n')
        for i, l in enumerate(lines):
            if 'ing.match' in l and 'àâé' in l:
                lines[i] = "    const m = ing.match(/^([\\d]+(?:[.,][\\d]+)?)\\s*([a-zA-Z]+(?:\\s?[a-z]+)?)?\\s+(.+)$/);"
                print(f"✅ Ligne {i+1} remplacée directement")
                break
        content = '\n'.join(lines)

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
