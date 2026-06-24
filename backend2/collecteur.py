from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import json
import csv
import os
import psycopg2
from datetime import datetime
 
app = FastAPI()
 
# ══ CORS ══
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ══ Dossier de sauvegarde ══
SAVE_DIR = "donnees_collectees"
os.makedirs(SAVE_DIR, exist_ok=True)
 
# ══ Mapping questions → id en base ══
QUESTIONS_QCM1 = {
    "legumes": 1, "legumineuses": 2, "feculents": 3, "fruits": 4,
    "fruitsACoque": 5, "laitiers": 6, "volaille": 7, "viande": 8,
    "charcuterie": 9, "poisson": 10, "oeufs": 11, "snacks": 12,
    "fastFood": 13, "boissons": 14, "sucres": 15, "bio": 16,
    "reductionViande": 17
}
 
QUESTIONS_QCM2 = {
    "👥 Nombre de personnes": 18,
    "🥗 Pratiques alimentaires": 19,
    "🍽️ Composition du repas": 20,
    "👨‍🍳 En cuisine": 21,
    "🕐 Nombre de repas": 22
}
 
# ══ Connexion PostgreSQL ══
import os

def get_db():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    conn.set_client_encoding('UTF8')
    return conn
    conn.set_client_encoding('UTF8')
    return conn
 
# ══ Modèle de données ══
class GameData(BaseModel):
    type: str
    data: Dict[str, Any] = {}
 
# ══ ENDPOINT PRINCIPAL ══
@app.post("/save")
async def save_data(payload: GameData):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 
    # 1. Sauvegarde JSON
    json_file = os.path.join(SAVE_DIR, "reponses.json")
    entry = {
        "timestamp": timestamp,
        "type": payload.type,
        "data": payload.data
    }
    with open(json_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
 
    # 2. Sauvegarde CSV
    csv_file = os.path.join(SAVE_DIR, "reponses.csv")
    file_exists = os.path.exists(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "type", "data"])
        writer.writerow([timestamp, payload.type, json.dumps(payload.data, ensure_ascii=False)])
 
    # 3. Sauvegarde PostgreSQL
    try:
        conn = get_db()
        cur = conn.cursor()
 
        # Prénom du joueur
        prenom = payload.data.get("prenom", "Anonyme")
 
        # Crée l'utilisateur
        cur.execute(
            "INSERT INTO utilisateurs (prenom) VALUES (%s) RETURNING id",
            (prenom,)
        )
        utilisateur_id = cur.fetchone()[0]
 
        # Calcule le score total si QCM1
        score_total = 0
        if payload.type == "qcm1":
            nutrition = payload.data.get("nutrition", {})
            if nutrition:
                score_total = round(sum(nutrition.values()) / len(nutrition))
 
        # Crée la session
        cur.execute(
            "INSERT INTO session (utilisateur_id, score_total) VALUES (%s, %s) RETURNING id",
            (utilisateur_id, score_total)
        )
        session_id = cur.fetchone()[0]
 
        # Sauvegarde les réponses avec question_id
        if payload.type == "qcm1":
            answers = payload.data.get("answers", [])
            for ans in answers:
                question_id = QUESTIONS_QCM1.get(ans.get("id"), None)
                cur.execute(
                    "INSERT INTO reponse (session_id, question_id, valeur) VALUES (%s, %s, %s)",
                    (session_id, question_id, ans.get("label", ""))
                )
 
        elif payload.type == "qcm2":
            answers = payload.data.get("answers", {})
            for question, valeur in answers.items():
                question_id = QUESTIONS_QCM2.get(question, None)
                cur.execute(
                    "INSERT INTO reponse (session_id, question_id, valeur) VALUES (%s, %s, %s)",
                    (session_id, question_id, str(valeur))
                )
 
        elif payload.type == "minijeu":
            data = payload.data
            valeur = f"Plat: {data.get('plate', [])} | Entree: {data.get('entree', [])} | Dessert: {data.get('dessert', [])} | Boisson: {data.get('glass', '')} | Score: {data.get('score', 0)}%"
            cur.execute(
                "INSERT INTO reponse (session_id, question_id, valeur) VALUES (%s, %s, %s)",
                (session_id, None, valeur)
            )
 
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ PostgreSQL : session {session_id} sauvegardée")
 
    except Exception as e:
        print(f"❌ Erreur PostgreSQL : {e}")
 
    print(f"✅ Données reçues : {payload.type} à {timestamp}")
    return {"status": "ok", "message": f"Données {payload.type} sauvegardées"}
 
 
# ══ ENDPOINT EXPORT JSON ══
@app.get("/export/json")
async def export_json():
    json_file = os.path.join(SAVE_DIR, "reponses.json")
    if not os.path.exists(json_file):
        return {"data": [], "message": "Aucune donnée collectée"}
    entries = []
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return {"total": len(entries), "data": entries}
 
 
# ══ ENDPOINT STATS ══
@app.get("/stats")
async def stats():
    json_file = os.path.join(SAVE_DIR, "reponses.json")
    if not os.path.exists(json_file):
        return {"total": 0, "par_type": {}}
    entries = []
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    par_type = {}
    for e in entries:
        t = e.get("type", "inconnu")
        par_type[t] = par_type.get(t, 0) + 1
    return {"total": len(entries), "par_type": par_type}
 
 
# ══ ENDPOINT STATS POSTGRESQL ══
@app.get("/stats/db")
async def stats_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM session")
        total_sessions = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM utilisateurs")
        total_utilisateurs = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM reponse")
        total_reponses = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {
            "total_sessions": total_sessions,
            "total_utilisateurs": total_utilisateurs,
            "total_reponses": total_reponses
        }
    except Exception as e:
        return {"erreur": str(e)}
