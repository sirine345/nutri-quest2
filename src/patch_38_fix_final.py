"""
PATCH 38 — Corrige les 2 apostrophes restantes (L339 et L2050)
Usage: python patch_38_fix_final.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

fixes = 0

# L339 - l\'activité → l&apos;activité
old339 = "l\\'activité physique régulière"
new339 = "l&apos;activité physique régulière"
if old339 in lines[338]:
    lines[338] = lines[338].replace(old339, new339)
    fixes += 1
    print("✅ L339 corrigée")
else:
    print(f"⚠️  L339: {repr(lines[338][:80])}")

# L2050 - {"t\'amuser"} → {"t'amuser"}  (backslash before apostrophe inside {})
old2050 = '{\"t\\\'amuser\"}'
new2050 = "{\"t'amuser\"}"
if old2050 in lines[2049]:
    lines[2049] = lines[2049].replace(old2050, new2050)
    fixes += 1
    print("✅ L2050 corrigée")
else:
    # Try alternative
    line = lines[2049]
    if "t\\'amuser" in line:
        lines[2049] = line.replace("t\\'amuser", "t'amuser")
        fixes += 1
        print("✅ L2050 corrigée (v2)")
    else:
        print(f"⚠️  L2050: {repr(line[:100])}")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n{fixes} correction(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
