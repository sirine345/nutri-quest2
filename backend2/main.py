from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import json
import csv
import io
import xml.etree.ElementTree as ET
from datetime import datetime

# ── Config DB ──────────────────────────────────────────
import psycopg2

def get_conn():
    return psycopg2.connect("postgresql://nutri_quest_db_user:Om1ZcZSRYn6MNa8KhXCW1tYk9A6HrACZ@dpg-d8u5fbeq1p3s73cb89ng-a/nutri_quest_db")

engine = create_engine("postgresql+psycopg2://", creator=get_conn)

app = FastAPI(title="nutri-quest2 API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    with engine.connect() as conn:
        yield conn


# ── Endpoints existants ────────────────────────────────

@app.get("/")
def home():
    return {"message": "nutri-quest2 API OK", "version": "1.0"}


@app.post("/save")
def save_game(payload: dict, db=Depends(get_db)):
    try:
        ptype = payload.get("type", "unknown")
        data = payload.get("data", {})
        prenom = data.get("patient", {}).get("prenom", "Invité")

        # Récupérer ou créer l'utilisateur
        row = db.execute(
            text("SELECT id FROM utilisateurs WHERE prenom = :p"),
            {"p": prenom}
        ).fetchone()

        if row:
            user_id = row[0]
        else:
            result = db.execute(
                text("INSERT INTO utilisateurs (prenom) VALUES (:p) RETURNING id"),
                {"p": prenom}
            )
            user_id = result.fetchone()[0]

        # Créer ou récupérer la session
        session_row = db.execute(
            text("SELECT id FROM session WHERE utilisateur_id = :uid ORDER BY date_debut DESC LIMIT 1"),
            {"uid": user_id}
        ).fetchone()

        if not session_row:
            sess = db.execute(
                text("INSERT INTO session (utilisateur_id) VALUES (:uid) RETURNING id"),
                {"uid": user_id}
            )
            session_id = sess.fetchone()[0]
        else:
            session_id = session_row[0]

        # Sauvegarder selon le type
        if ptype == "qcm1":
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
            )

        elif ptype == "qcm2_mna" or ptype == "mna":
            mna = data.get("mna", {})
            db.execute(
                text("""
                    INSERT INTO mna_result (session_id, score_depistage, score_globale, score_total, label)
                    VALUES (:sid, :dep, :glob, :tot, :lab)
                    ON CONFLICT DO NOTHING
                """),
                {
                    "sid": session_id,
                    "dep": mna.get("depistage", 0),
                    "glob": mna.get("globale", 0),
                    "tot": mna.get("total", 0),
                    "lab": mna.get("label", "")
                }
            )
            db.execute(
                text("UPDATE session SET score_mna = :s WHERE id = :id"),
                {"s": mna.get("total", 0), "id": session_id}
            )

        elif ptype == "qcm_sante":
            medas = data.get("medasResult")
            if medas:
                answers = medas.get("answers", {})
                db.execute(
                    text("""
                        INSERT INTO medas_result (
                            session_id, score_total,
                            huile_olive_principale, huile_olive_dose,
                            legumes, fruits, viande_rouge, beurre,
                            sodas, vin, legumineuses, poisson,
                            patisseries, fruits_coque, viande_blanche, sofrito
                        ) VALUES (
                            :sid, :total,
                            :ho_p, :ho_d,
                            :leg, :fru, :vr, :beu,
                            :sod, :vin, :legu, :poi,
                            :pat, :fc, :vb, :sof
                        )
                    """),
                    {
                        "sid": session_id, "total": medas.get("score", 0),
                        "ho_p": answers.get("huile_olive_principale", 0),
                        "ho_d": answers.get("huile_olive_dose", 0),
                        "leg": answers.get("legumes", 0),
                        "fru": answers.get("fruits", 0),
                        "vr": answers.get("viande_rouge", 0),
                        "beu": answers.get("beurre", 0),
                        "sod": answers.get("sodas", 0),
                        "vin": answers.get("vin", 0),
                        "legu": answers.get("legumineuses", 0),
                        "poi": answers.get("poisson", 0),
                        "pat": answers.get("patisseries", 0),
                        "fc": answers.get("fruits_coque", 0),
                        "vb": answers.get("viande_blanche", 0),
                        "sof": answers.get("sofrito", 0),
                    }
                )
                db.execute(
                    text("UPDATE session SET score_medas = :s WHERE id = :id"),
                    {"s": medas.get("score", 0), "id": session_id}
                )

        db.commit()
        return {"status": "ok", "session_id": session_id}

    except Exception as e:
        db.rollback()
        print(f"Erreur save: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/login")
def login(payload: dict, db=Depends(get_db)):
    email = payload.get("email", "")
    row = db.execute(
        text("SELECT id, prenom FROM utilisateurs WHERE prenom = :e"),
        {"e": email}
    ).fetchone()
    if row:
        return {"status": "ok", "prenom": row[1], "id": row[0]}
    return {"status": "error", "message": "Utilisateur non trouvé"}


@app.post("/register")
def register(payload: dict, db=Depends(get_db)):
    email = payload.get("email", "")
    try:
        result = db.execute(
            text("INSERT INTO utilisateurs (prenom) VALUES (:p) RETURNING id"),
            {"p": email}
        )
        db.commit()
        return {"status": "ok", "id": result.fetchone()[0]}
    except:
        return {"status": "error", "message": "Erreur création compte"}


# ── Dashboard endpoints ────────────────────────────────

@app.get("/dashboard/stats")
def dashboard_stats(db=Depends(get_db)):
    """Toutes les stats pour le dashboard"""
    try:
        # Total participants
        total_p = db.execute(text("SELECT COUNT(*) FROM utilisateurs")).scalar()
        total_s = db.execute(text("SELECT COUNT(*) FROM session")).scalar()

        # Score MEDAS moyen
        medas_avg = db.execute(text("SELECT ROUND(AVG(score_total)::numeric, 1) FROM medas_result")).scalar()

        # Risque dénutrition (score MNA < 24)
        mna_risk = db.execute(text("SELECT COUNT(*) FROM mna_result WHERE score_total < 24")).scalar()
        pct_mna = round(mna_risk / max(total_p, 1) * 100, 1) if mna_risk else 0

        # Scores PNNS moyens depuis vue_participants
        scores_rows = db.execute(text("""
            SELECT
                ROUND(AVG(score_legumes)::numeric, 1) as legumes,
                ROUND(AVG(score_fruits)::numeric, 1) as fruits,
                ROUND(AVG(score_poisson)::numeric, 1) as poisson,
                ROUND(AVG(score_charcuterie)::numeric, 1) as charcuterie,
                ROUND(AVG(score_fastfood)::numeric, 1) as fastfood
            FROM vue_participants
        """)).fetchone()

        scores_pnns = {}
        if scores_rows:
            keys = ["Légumes", "Fruits", "Poisson", "Charcuterie", "Fast-food"]
            for k, v in zip(keys, scores_rows):
                scores_pnns[k] = float(v or 0)

        # Pathologies
        path_rows = db.execute(text("""
            SELECT pathologies, COUNT(*) as n
            FROM vue_participants
            WHERE pathologies IS NOT NULL AND pathologies != ''
            GROUP BY pathologies
            ORDER BY n DESC
            LIMIT 10
        """)).fetchall()
        pathologies = {r[0]: r[1] for r in path_rows}

        # Modes de vie
        mode_rows = db.execute(text("""
            SELECT mode_vie, COUNT(*) as n
            FROM vue_participants
            WHERE mode_vie IS NOT NULL
            GROUP BY mode_vie
            ORDER BY n DESC
        """)).fetchall()
        modes_vie = {r[0]: r[1] for r in mode_rows}

        # Participants liste
        part_rows = db.execute(text("""
            SELECT utilisateur_id, prenom, created_at, age, sexe,
                   pathologies, score_qcm1, score_medas, score_mna
            FROM vue_participants
            ORDER BY created_at DESC
            LIMIT 100
        """)).fetchall()

        participants = []
        for r in part_rows:
            participants.append({
                "utilisateur_id": r[0],
                "prenom": r[1],
                "created_at": r[2].isoformat() if r[2] else None,
                "age": r[3],
                "sexe": r[4],
                "pathologies": r[5],
                "score_qcm1": r[6],
                "score_medas": r[7],
                "score_mna": float(r[8]) if r[8] else None,
            })

        # Stats MEDAS depuis vue
        medas_row = db.execute(text("""
            SELECT total_participants, score_moyen,
                   adherence_faible, adherence_moderee, adherence_forte,
                   pct_huile_olive, pct_legumes_ok, pct_poisson_ok
            FROM vue_medas_stats
        """)).fetchone()

        medas_stats = {}
        if medas_row:
            medas_stats = {
                "total_participants": medas_row[0],
                "score_moyen": float(medas_row[1] or 0),
                "adherence_faible": medas_row[2],
                "adherence_moderee": medas_row[3],
                "adherence_forte": medas_row[4],
                "pct_huile_olive": float(medas_row[5] or 0),
                "pct_legumes_ok": float(medas_row[6] or 0),
                "pct_poisson_ok": float(medas_row[7] or 0),
            }

        return {
            "total_participants": total_p,
            "total_sessions": total_s,
            "score_medas_moyen": float(medas_avg or 0),
            "pct_risque_denutrition": pct_mna,
            "scores_pnns": scores_pnns,
            "pathologies": pathologies,
            "modes_vie": modes_vie,
            "participants": participants,
            "medas": medas_stats,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export/csv")
def export_csv(db=Depends(get_db)):
    """Export CSV de tous les participants"""
    rows = db.execute(text("""
        SELECT utilisateur_id, prenom, created_at, age, sexe,
               pathologies, mode_vie, pratiques_alimentaires,
               composition_repas, score_qcm1, score_medas, score_mna,
               score_legumes, score_fruits, score_poisson,
               score_charcuterie, score_fastfood
        FROM vue_participants
        ORDER BY created_at DESC
    """)).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Prénom", "Date", "Âge", "Sexe",
        "Pathologies", "Mode de vie", "Pratiques alimentaires",
        "Composition repas", "Score QCM1", "Score MEDAS", "Score MNA",
        "Score légumes", "Score fruits", "Score poisson",
        "Score charcuterie", "Score fast-food"
    ])
    for r in rows:
        writer.writerow([str(v) if v is not None else "" for v in r])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=nutri_quest_{datetime.now().strftime('%Y%m%d')}.csv"}
    )


@app.get("/export/json")
def export_json(db=Depends(get_db)):
    """Export JSON de tous les participants"""
    rows = db.execute(text("""
        SELECT utilisateur_id, prenom, created_at, age, sexe,
               pathologies, mode_vie, pratiques_alimentaires,
               composition_repas, score_qcm1, score_medas, score_mna,
               score_legumes, score_fruits, score_poisson,
               score_charcuterie, score_fastfood
        FROM vue_participants
        ORDER BY created_at DESC
    """)).fetchall()

    cols = ["id", "prenom", "date", "age", "sexe", "pathologies",
            "mode_vie", "pratiques_alimentaires", "composition_repas",
            "score_qcm1", "score_medas", "score_mna",
            "score_legumes", "score_fruits", "score_poisson",
            "score_charcuterie", "score_fastfood"]

    data = []
    for r in rows:
        d = {}
        for col, val in zip(cols, r):
            d[col] = val.isoformat() if hasattr(val, 'isoformat') else val
        data.append(d)

    content = json.dumps({"participants": data, "total": len(data),
                          "export_date": datetime.now().isoformat()},
                         ensure_ascii=False, indent=2)
    return Response(
        content=content.encode("utf-8"),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=nutri_quest_{datetime.now().strftime('%Y%m%d')}.json"}
    )


@app.get("/export/xml")
def export_xml(db=Depends(get_db)):
    """Export XML de tous les participants"""
    rows = db.execute(text("""
        SELECT utilisateur_id, prenom, created_at, age, sexe,
               pathologies, mode_vie, score_qcm1, score_medas, score_mna
        FROM vue_participants
        ORDER BY created_at DESC
    """)).fetchall()

    root = ET.Element("nutri_quest_export")
    root.set("date", datetime.now().isoformat())
    root.set("total", str(len(rows)))

    participants = ET.SubElement(root, "participants")
    for r in rows:
        p = ET.SubElement(participants, "participant")
        fields = ["id", "prenom", "date", "age", "sexe",
                  "pathologies", "mode_vie", "score_qcm1", "score_medas", "score_mna"]
        for field, val in zip(fields, r):
            el = ET.SubElement(p, field)
            el.text = val.isoformat() if hasattr(val, 'isoformat') else (str(val) if val is not None else "")

    xml_str = ET.tostring(root, encoding="unicode", xml_declaration=False)
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'

    return Response(
        content=xml_content.encode("utf-8"),
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename=nutri_quest_{datetime.now().strftime('%Y%m%d')}.xml"}
    )


@app.get("/dashboard")
def dashboard_html(pwd: str = ""):
    """Page dashboard protégée (accès direct URL)"""
    if pwd != "F.zhi5":
        return Response(content="<h1>Accès refusé</h1>", media_type="text/html")
    return {"message": "Utilisez le dashboard intégré dans l'application React"}
