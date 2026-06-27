import json
import csv
import os
 
INPUT_FILE  = "donnees_collectees/reponses.json"
OUTPUT_FILE = "donnees_collectees/reponses_aplaties.csv"
 
rows = []
 
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        timestamp = entry.get("timestamp", "")
        type_     = entry.get("type", "")
        data      = entry.get("data", {})
 
        row = {"timestamp": timestamp, "type": type_}
 
        if type_ == "qcm1":
            answers   = data.get("answers", [])
            nutrition = data.get("nutrition", {})
            for ans in answers:
                col_name = ans.get("id", "?")
                row[col_name] = ans.get("label", "")
            for key, val in nutrition.items():
                row[f"score_{key}"] = val
 
        elif type_ == "qcm2":
            answers = data.get("answers", {})
            for key, val in answers.items():
                clean_key = key.encode("ascii", "ignore").decode().strip()
                if not clean_key:
                    clean_key = key
                row[clean_key] = val
 
        elif type_ == "minijeu":
            row["aliments_assiette"] = ", ".join(data.get("plate", []))
            row["boisson"]           = data.get("glass", "aucune")
            row["bons_aliments"]     = ", ".join(data.get("bons_aliments", []))
            row["mauvais_aliments"]  = ", ".join(data.get("mauvais_aliments", []))
            row["score_pnns"]        = data.get("score", 0)
 
        else:
            row["data_brute"] = json.dumps(data, ensure_ascii=False)
 
        rows.append(row)
 
if not rows:
    print("Aucune donnée trouvée dans reponses.json")
else:
    all_keys = []
    for row in rows:
        for k in row.keys():
            if k not in all_keys:
                all_keys.append(k)
 
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
 
    print(f"Fichier cree : {OUTPUT_FILE}")
    print(f"{len(rows)} lignes · {len(all_keys)} colonnes")
 
    par_type = {}
    for r in rows:
        t = r["type"]
        par_type[t] = par_type.get(t, 0) + 1
    for t, n in par_type.items():
        print(f"  - {t} : {n} ligne(s)")
 
 
 