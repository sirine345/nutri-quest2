import re

path = r"C:\Users\fzahi\Desktop\nutri-quest2\backend\main.py"

with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

old_qcm1 = '''        if ptype == "qcm1":
            nutrition = data.get("nutrition", {})
            for key, val in nutrition.items():
                db.execute(
                    text("""
                        INSERT INTO reponse (session_id, question_id, valeur, score_nutrition)
                        SELECT :sid, id, :val, :score FROM question WHERE intitule = :key
                        ON CONFLICT DO NOTHING
                    """),
                    {"sid": session_id, "val": str(val), "score": int(val), "key": key}
                )
            db.execute(
                text("UPDATE session SET score_total = :s WHERE id = :id"),
                {"s": sum(nutrition.values()) // max(len(nutrition), 1), "id": session_id}
            )'''

new_qcm1 = '''        if ptype == "qcm1":
            nutrition = data.get("nutrition", {})
            score_total = sum(nutrition.values()) // max(len(nutrition), 1) if nutrition else 0
            db.execute(
                text("""
                    UPDATE session SET
                        score_total = :total,
                        score_legumes = :leg,
                        score_fruits = :fru,
                        score_poisson = :poi,
                        score_charcuterie = :char,
                        score_fastfood = :fast
                    WHERE id = :sid
                """),
                {
                    "total": score_total,
                    "leg": int(nutrition.get("legumes", 0)),
                    "fru": int(nutrition.get("fruits", 0)),
                    "poi": int(nutrition.get("poisson", 0)),
                    "char": int(nutrition.get("charcuterie", 0)),
                    "fast": int(nutrition.get("fastFood", 0)),
                    "sid": session_id
                }
            )'''

if old_qcm1 in content:
    content = content.replace(old_qcm1, new_qcm1)
    print("OK bloc QCM1 remplace")
else:
    print("ERREUR bloc non trouve")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("main.py mis a jour !")
