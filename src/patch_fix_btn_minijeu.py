"""
Fix bouton Composer mon assiette → onMinijeu
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Composer mon assiette' in l:
        # Check line before (button onClick)
        for j in range(max(0, i-3), i):
            if 'onClick' in lines[j] and 'onBack' in lines[j]:
                lines[j] = lines[j].replace('onClick={() => onBack()}', 'onClick={() => onMinijeu && onMinijeu()}')
                lines[j] = lines[j].replace('onClick={onBack}', 'onClick={() => onMinijeu && onMinijeu()}')
                print(f"✅ L{j+1} corrigée: {lines[j].rstrip()[:80]}")
                break

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
