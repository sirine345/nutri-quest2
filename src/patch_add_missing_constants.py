"""
PATCH — Réinsère MEDAS_QUESTIONS, SILHOUETTES_H, SILHOUETTES_F avant TransitionLLCScreen
Usage: python patch_add_missing_constants.py App.jsx App.jsx.backup_avant_qcm2_gameplay_v6
"""
import sys

# Read current App.jsx
with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    current = f.read()

# Read backup to extract constants
backup_path = sys.argv[2] if len(sys.argv) > 2 else 'App.jsx.backup_avant_qcm2_gameplay_v6'
with open(backup_path, 'r', encoding='utf-8', errors='replace') as f:
    backup_lines = f.readlines()

# Extract MEDAS_QUESTIONS block
def extract_const(lines, const_name):
    start = next((i for i, l in enumerate(lines) if f'const {const_name}' in l), None)
    if start is None:
        return None
    # Find end: next const or function
    for i in range(start+1, len(lines)):
        l = lines[i].strip()
        if (l.startswith('const ') or l.startswith('function ') or l.startswith('export default')) and i > start+2:
            return ''.join(lines[start:i]) + '\n'
    return None

medas = extract_const(backup_lines, 'MEDAS_QUESTIONS')
sil_h = extract_const(backup_lines, 'SILHOUETTES_H')
sil_f = extract_const(backup_lines, 'SILHOUETTES_F')
get_sil = extract_const(backup_lines, 'getSilhouetteLabel')

print(f"MEDAS_QUESTIONS: {'✅' if medas else '⚠️'} ({len(medas) if medas else 0} chars)")
print(f"SILHOUETTES_H: {'✅' if sil_h else '⚠️'} ({len(sil_h) if sil_h else 0} chars)")
print(f"SILHOUETTES_F: {'✅' if sil_f else '⚠️'} ({len(sil_f) if sil_f else 0} chars)")
print(f"getSilhouetteLabel: {'✅' if get_sil else '⚠️'}")

# Insert before TransitionLLCScreen
marker = 'function TransitionLLCScreen('
idx = current.find(marker)
if idx == -1:
    print("⚠️ TransitionLLCScreen non trouvée"); sys.exit(1)

insert = '\n'
if medas: insert += medas
if sil_h: insert += sil_h  
if sil_f: insert += sil_f
if get_sil and 'getSilhouetteLabel' not in current: insert += get_sil

current = current[:idx] + insert + current[idx:]
print("✅ Constantes réinsérées avant TransitionLLCScreen")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(current)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
