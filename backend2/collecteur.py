from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import json, csv, os, io, hashlib, psycopg2
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SAVE_DIR = "donnees_collectees"
os.makedirs(SAVE_DIR, exist_ok=True)
USERS_FILE = os.path.join(SAVE_DIR, "users.json")
ADMIN_PASSWORD = "Sirine1234"

QUESTIONS_QCM1 = {
    "legumes":1,"legumineuses":2,"feculents":3,"fruits":4,"fruitsACoque":5,
    "laitiers":6,"volaille":7,"viande":8,"charcuterie":9,"poisson":10,
    "oeufs":11,"snacks":12,"fastFood":13,"boissons":14,"sucres":15,
    "bio":16,"reductionViande":17
}
QUESTIONS_QCM2 = {
    " Nombre de personnes":18," Pratiques alimentaires":19,
    " Composition du repas":20,"\u200d En cuisine":21," Nombre de repas":22,
}
QUESTIONS_SANTE = {
    "age":23,"sexe":24,"silhouette":25,"evolution":26,"seul":27,
    "autonomie":28,"maladieChroniqueOui":29,"pathologies":30,
    "traitement":31,"regimePrescrit":32,"modeVie":33,"freins":34,
}
QUESTIONS_MEDAS = {
    "huile_olive_principale":35,"huile_olive_dose":36,"legumes":37,"fruits":38,
    "viande_rouge":39,"beurre":40,"sodas":41,"vin":42,"legumineuses":43,
    "poisson":44,"patisseries":45,"fruits_coque":46,"viande_blanche":47,"sofrito":48,
}
QCM1_LABELS = {
    "legumes":"Légumes frais","legumineuses":"Légumes secs","feculents":"Féculents complets",
    "fruits":"Fruits","fruitsACoque":"Fruits à coque","laitiers":"Produits laitiers",
    "volaille":"Volaille","viande":"Viande (hors volaille)","charcuterie":"Charcuterie",
    "poisson":"Poisson","oeufs":"Oeufs","snacks":"Snacks salés","fastFood":"Fast food",
    "boissons":"Boissons sucrées","sucres":"Sucreries","bio":"Aliments bio",
    "reductionViande":"Réduction viande"
}
SANTE_LABELS = {
    "age":"Âge","sexe":"Sexe","silhouette":"Silhouette (Stunkard)","evolution":"Évolution silhouette",
    "seul":"Vit seul(e)","autonomie":"Autonomie courses/repas","maladieChroniqueOui":"Maladie chronique",
    "pathologies":"Pathologies","traitement":"Traitement régulier","regimePrescrit":"Régime prescrit",
    "modeVie":"Mode de vie","freins":"Freins activité physique",
}
MEDAS_LABELS = {
    "huile_olive_principale":"Huile olive principale","huile_olive_dose":"Huile olive ≥4cs/j",
    "legumes":"Légumes MEDAS ≥2/j","fruits":"Fruits MEDAS ≥3/j","viande_rouge":"Viande rouge <1/j",
    "beurre":"Beurre <1/j","sodas":"Sodas <1/j","vin":"Vin ≥7/sem","legumineuses":"Légumineuses ≥3/sem",
    "poisson":"Poisson MEDAS ≥3/sem","patisseries":"Pâtisseries <3/sem","fruits_coque":"Fruits à coque ≥3/sem",
    "viande_blanche":"Viande blanche préférée","sofrito":"Sofrito ≥2/sem",
}

def get_db():
    conn = psycopg2.connect(host="localhost",database="nutri_quest",user="postgres",password="F.zhi5",port="5432")
    conn.set_client_encoding('UTF8')
    return conn

def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def load_users():
    if not os.path.exists(USERS_FILE): return {}
    with open(USERS_FILE,"r",encoding="utf-8") as f: return json.load(f)
def save_users(u):
    with open(USERS_FILE,"w",encoding="utf-8") as f: json.dump(u,f,ensure_ascii=False,indent=2)

class GameData(BaseModel):
    type: str
    data: Dict[str,Any] = {}
class RegisterData(BaseModel):
    email:str; password:str; prenom:str=""; sexe:str=""; age:str=""; taille:str=""; poids:str=""; restriction:List[str]=[]
class LoginData(BaseModel):
    email:str; password:str

@app.post("/register")
async def register(data: RegisterData):
    users=load_users(); email=data.email.lower().strip()
    if email in users: return {"status":"error","message":"Email déjà utilisé"}
    users[email]={"password":hash_password(data.password),"prenom":data.prenom,"sexe":data.sexe,
                  "age":data.age,"taille":data.taille,"poids":data.poids,"restriction":data.restriction,
                  "created_at":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"sessions":[]}
    save_users(users); return {"status":"ok","message":"Compte créé"}

@app.post("/login")
async def login(data: LoginData):
    users=load_users(); email=data.email.lower().strip()
    if email not in users: return {"status":"error","message":"Email introuvable"}
    if users[email]["password"]!=hash_password(data.password): return {"status":"error","message":"Mot de passe incorrect"}
    u=users[email]
    return {"status":"ok","prenom":u.get("prenom",""),"sexe":u.get("sexe",""),"age":u.get("age",""),"taille":u.get("taille",""),"poids":u.get("poids",""),"restriction":u.get("restriction",[])}

@app.post("/update_profile")
async def update_profile(data: dict):
    users=load_users(); email=data.get("email","").lower().strip()
    if email not in users: return {"status":"error","message":"Compte introuvable"}
    for k in ["prenom","sexe","age","taille","poids","restriction"]:
        if k in data: users[email][k]=data[k]
    save_users(users); return {"status":"ok"}

@app.post("/save")
async def save_data(payload: GameData):
    timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    json_file=os.path.join(SAVE_DIR,"reponses.json")
    entry={"timestamp":timestamp,"type":payload.type,"data":payload.data}
    with open(json_file,"a",encoding="utf-8") as f: f.write(json.dumps(entry,ensure_ascii=False)+"\n")
    csv_file=os.path.join(SAVE_DIR,"reponses.csv")
    fe=os.path.exists(csv_file)
    with open(csv_file,"a",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        if not fe: w.writerow(["timestamp","type","data"])
        w.writerow([timestamp,payload.type,json.dumps(payload.data,ensure_ascii=False)])
    patient=payload.data.get("patient",{})
    email=patient.get("email","").lower().strip()
    if email:
        users=load_users()
        if email in users: users[email]["sessions"].append(entry); save_users(users)
    try:
        conn=get_db(); cur=conn.cursor()
        prenom=patient.get("prenom","Anonyme")
        cur.execute("INSERT INTO utilisateurs (prenom) VALUES (%s) RETURNING id",(prenom,))
        uid=cur.fetchone()[0]
        score_total=0; score_medas=None; score_mna=None
        if payload.type=="qcm1":
            n=payload.data.get("nutrition",{}); score_total=round(sum(n.values())/len(n)) if n else 0
        cur.execute("INSERT INTO session (utilisateur_id,score_total,score_medas,score_mna) VALUES (%s,%s,%s,%s) RETURNING id",
                    (uid,score_total,score_medas,score_mna))
        sid=cur.fetchone()[0]
        if payload.type=="qcm1":
            nut=payload.data.get("nutrition",{})
            for a in payload.data.get("answers",[]):
                qid=QUESTIONS_QCM1.get(a.get("id")); sn=nut.get(a.get("id"))
                cur.execute("INSERT INTO reponse (session_id,question_id,valeur,score_nutrition) VALUES (%s,%s,%s,%s)",
                            (sid,qid,a.get("label",""),sn))
        elif payload.type in ("qcm2","qcm2_mna"):
            for q,v in payload.data.get("answers",{}).items():
                qid=QUESTIONS_QCM2.get(q)
                cur.execute("INSERT INTO reponse (session_id,question_id,valeur) VALUES (%s,%s,%s)",(sid,qid,str(v)))
            mna=payload.data.get("mna",{})
            if mna:
                cur.execute("INSERT INTO mna_result (session_id,score_depistage,score_globale,score_total,label) VALUES (%s,%s,%s,%s,%s)",
                            (sid,mna.get("depistage"),mna.get("globale"),mna.get("total"),mna.get("label","")))
        elif payload.type=="qcm_sante":
            d=payload.data
            fields={"age":d.get("age"),"sexe":d.get("sexe"),"silhouette":d.get("silhouette"),
                    "evolution":d.get("evolution"),"seul":d.get("seul"),"autonomie":d.get("autonomie"),
                    "maladieChroniqueOui":d.get("maladieChroniqueOui"),
                    "pathologies":json.dumps(d.get("pathologies",[]),ensure_ascii=False),
                    "traitement":d.get("traitement"),"regimePrescrit":d.get("regimePrescrit"),
                    "modeVie":d.get("modeVie"),"freins":json.dumps(d.get("freins",[]),ensure_ascii=False)}
            for k,v in fields.items():
                if v is not None:
                    cur.execute("INSERT INTO reponse (session_id,question_id,valeur) VALUES (%s,%s,%s)",
                                (sid,QUESTIONS_SANTE.get(k),str(v)))
            med=d.get("medasResult",{})
            if med:
                ma=med.get("answers",{})
                cur.execute("""INSERT INTO medas_result
                    (session_id,score_total,huile_olive_principale,huile_olive_dose,legumes,fruits,viande_rouge,
                     beurre,sodas,vin,legumineuses,poisson,patisseries,fruits_coque,viande_blanche,sofrito)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (sid,med.get("score",0),ma.get("huile_olive_principale",0),ma.get("huile_olive_dose",0),
                     ma.get("legumes",0),ma.get("fruits",0),ma.get("viande_rouge",0),ma.get("beurre",0),
                     ma.get("sodas",0),ma.get("vin",0),ma.get("legumineuses",0),ma.get("poisson",0),
                     ma.get("patisseries",0),ma.get("fruits_coque",0),ma.get("viande_blanche",0),ma.get("sofrito",0)))
                for k,v in ma.items():
                    cur.execute("INSERT INTO reponse (session_id,question_id,valeur,score_nutrition) VALUES (%s,%s,%s,%s)",
                                (sid,QUESTIONS_MEDAS.get(k),str(v),v))
        elif payload.type=="minijeu":
            d=payload.data
            v=f"Plat:{d.get('plate',[])}|Entree:{d.get('entree',[])}|Dessert:{d.get('dessert',[])}|Boisson:{d.get('glass','')}|Score:{d.get('score',0)}%"
            cur.execute("INSERT INTO reponse (session_id,question_id,valeur) VALUES (%s,%s,%s)",(sid,None,v))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print(f"Erreur PostgreSQL: {e}")
    return {"status":"ok","message":f"Données {payload.type} sauvegardées"}

@app.get("/dashboard")
async def dashboard(pwd: str=""):
    if pwd!=ADMIN_PASSWORD:
        return HTMLResponse("""<html><body style="font-family:Arial;padding:40px;background:#f4dcbf">
        <h2>🔧 Espace Gestionnaire</h2><form method="get">
        <input name="pwd" type="password" placeholder="Mot de passe" style="padding:10px;font-size:16px;border-radius:8px;border:2px solid #ccc;margin-right:10px"/>
        <button type="submit" style="padding:10px 20px;background:#FA8072;color:white;border:none;border-radius:8px;font-size:16px;cursor:pointer">Accéder</button>
        </form></body></html>""")
    users=load_users()
    json_file=os.path.join(SAVE_DIR,"reponses.json")
    total_sessions=sum(1 for l in open(json_file,encoding="utf-8") if l.strip()) if os.path.exists(json_file) else 0
    db={"s":"N/A","u":"N/A","r":"N/A","m":"N/A","mna":"N/A"}
    last_rows=""; patho_rows=""; medas_html=""
    try:
        conn=get_db(); cur=conn.cursor()
        for k,q in [("s","SELECT COUNT(*) FROM session"),("u","SELECT COUNT(*) FROM utilisateurs"),
                    ("r","SELECT COUNT(*) FROM reponse"),("m","SELECT COUNT(*) FROM medas_result"),
                    ("mna","SELECT COUNT(*) FROM mna_result")]:
            cur.execute(q); db[k]=cur.fetchone()[0]
        cur.execute("SELECT u.prenom,s.created_at,s.score_total,s.score_medas,s.score_mna FROM session s JOIN utilisateurs u ON u.id=s.utilisateur_id ORDER BY s.created_at DESC LIMIT 20")
        for r in cur.fetchall():
            last_rows+=f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}%</td><td>{str(r[3])+'/14' if r[3] is not None else '—'}</td><td>{str(r[4])+'/30' if r[4] is not None else '—'}</td></tr>"
        cur.execute("SELECT valeur,COUNT(*) FROM reponse WHERE question_id=30 GROUP BY valeur ORDER BY COUNT(*) DESC LIMIT 10")
        for r in cur.fetchall(): patho_rows+=f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
        cur.execute("SELECT COUNT(*) FILTER(WHERE score_total<=5),COUNT(*) FILTER(WHERE score_total BETWEEN 6 AND 9),COUNT(*) FILTER(WHERE score_total>=10) FROM medas_result")
        r=cur.fetchone()
        if r: medas_html=f'<div class="stat"><div class="stat-n" style="color:#e53935">{r[0]}</div><div class="stat-l">MEDAS faible (≤5)</div></div><div class="stat"><div class="stat-n" style="color:#f57c00">{r[1]}</div><div class="stat-l">MEDAS modéré (6-9)</div></div><div class="stat"><div class="stat-n" style="color:#2e7d32">{r[2]}</div><div class="stat-l">MEDAS fort (≥10)</div></div>'
        cur.close(); conn.close()
    except Exception as e:
        last_rows=f"<tr><td colspan='5' style='color:red'>Erreur BDD: {e}</td></tr>"
    rows=""
    for email,u in users.items():
        rows+=f"<tr><td>{u.get('prenom','')}</td><td>{email}</td><td>{u.get('sexe','')}</td><td>{u.get('age','')}</td><td>{u.get('created_at','')}</td><td>{len(u.get('sessions',[]))}</td></tr>"
    return HTMLResponse(f"""<html><head><meta charset="utf-8"><style>
      body{{font-family:Arial;padding:30px;background:#f4dcbf}}h1{{color:#FA8072}}h2{{color:#c4622d;margin-top:30px}}
      table{{border-collapse:collapse;width:100%;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,.1);margin-bottom:20px}}
      th{{background:#FA8072;color:white;padding:12px;text-align:left;font-size:13px}}
      td{{padding:10px 12px;border-bottom:1px solid #eee;font-size:13px}}
      .stat{{background:white;border-radius:12px;padding:20px;margin:10px;display:inline-block;min-width:140px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.1)}}
      .stat-n{{font-size:32px;font-weight:900;color:#FA8072}}.stat-l{{font-size:12px;color:#888;margin-top:4px}}
      a{{color:#FA8072;text-decoration:none;font-weight:700}}
    </style></head><body>
    <h1>🔧 Espace Gestionnaire — Nutri-Quest</h1>
    <h2>📊 Vue d'ensemble</h2>
    <div>
      <div class="stat"><div class="stat-n">{len(users)}</div><div class="stat-l">Comptes</div></div>
      <div class="stat"><div class="stat-n">{total_sessions}</div><div class="stat-l">Sessions (fichier)</div></div>
      <div class="stat"><div class="stat-n">{db['s']}</div><div class="stat-l">Sessions (BDD)</div></div>
      <div class="stat"><div class="stat-n">{db['r']}</div><div class="stat-l">Réponses</div></div>
      <div class="stat"><div class="stat-n">{db['m']}</div><div class="stat-l">QCM MEDAS</div></div>
      <div class="stat"><div class="stat-n">{db['mna']}</div><div class="stat-l">MNA Dénutrition</div></div>
    </div>
    <h2>🫒 Score MEDAS (adhésion méditerranéen)</h2><div>{medas_html}</div>
    <p><a href="/export/csv?pwd={ADMIN_PASSWORD}">📥 CSV</a> &nbsp;|&nbsp; <a href="/export/json">📋 JSON</a> &nbsp;|&nbsp; <a href="/stats/db">🗄️ Stats BDD</a></p>
    <h2>🕒 20 dernières sessions</h2>
    <table><tr><th>Prénom</th><th>Date</th><th>Score QCM1</th><th>Score MEDAS</th><th>Score MNA</th></tr>
    {last_rows or '<tr><td colspan="5" style="text-align:center;color:#888">Aucune session</td></tr>'}</table>
    <h2>🏥 Pathologies déclarées</h2>
    <table style="max-width:500px"><tr><th>Pathologie</th><th>Occurrences</th></tr>
    {patho_rows or '<tr><td colspan="2">—</td></tr>'}</table>
    <h2>👥 Joueurs inscrits</h2>
    <table><tr><th>Prénom</th><th>Email</th><th>Sexe</th><th>Âge</th><th>Inscrit le</th><th>Sessions</th></tr>
    {rows or '<tr><td colspan="6" style="text-align:center;color:#888">Aucun joueur</td></tr>'}</table>
    </body></html>""")

@app.get("/export/csv")
async def export_csv():
    json_file=os.path.join(SAVE_DIR,"reponses.json")
    if not os.path.exists(json_file): return {"message":"Aucune donnée"}
    entries=[]
    with open(json_file,"r",encoding="utf-8") as f:
        for l in f:
            if l.strip(): entries.append(json.loads(l))
    output=io.StringIO()
    q1c=list(QCM1_LABELS.values()); q1s=[f"{v} (score)" for v in q1c]
    q2c=["Nb personnes","Pratiques alim.","Compo repas","Cuisine","Nb repas"]
    sc=list(SANTE_LABELS.values()); mc=list(MEDAS_LABELS.values())+["Score MEDAS /14"]
    mnac=["MNA dépistage /14","MNA évaluation /16","MNA total /30","MNA label"]
    minjc=["Entrée","Plat","Dessert","Boisson","Score assiette (%)"]
    patc=["Prénom","Email","Sexe","Âge","Taille","Poids","Restrictions"]
    headers=["Timestamp","Type"]+patc+q1c+q1s+q2c+sc+mc+mnac+minjc
    w=csv.writer(output); w.writerow(headers)
    for entry in entries:
        t=entry.get("type",""); d=entry.get("data",{}); pat=d.get("patient",{})
        row=[entry.get("timestamp",""),t,pat.get("prenom",""),pat.get("email",""),
             pat.get("sexe",""),pat.get("age",""),pat.get("taille",""),pat.get("poids",""),
             ", ".join(pat.get("restriction",[]) if isinstance(pat.get("restriction",[]),list) else [])]
        empty_q1=[""]*(len(q1c)+len(q1s)); empty_q2=[""]*(len(q2c))
        empty_s=[""]*(len(sc)); empty_m=[""]*(len(mc)); empty_mna=[""]*(len(mnac)); empty_min=[""]*(len(minjc))
        if t=="qcm1":
            ans={a["id"]:a["label"] for a in d.get("answers",[])}; nut=d.get("nutrition",{})
            row+=[ans.get(k,"") for k in QCM1_LABELS]+[nut.get(k,"") for k in QCM1_LABELS]
            row+=empty_q2+empty_s+empty_m+empty_mna+empty_min
        elif t in ("qcm2","qcm2_mna"):
            row+=empty_q1
            a=d.get("answers",{})
            row+=[a.get(" Nombre de personnes",""),a.get(" Pratiques alimentaires",""),
                  a.get(" Composition du repas",""),a.get("\u200d En cuisine",""),a.get(" Nombre de repas","")]
            row+=empty_s+empty_m
            mna=d.get("mna",{})
            row+=[mna.get("depistage",""),mna.get("globale",""),mna.get("total",""),mna.get("label","")]
            row+=empty_min
        elif t=="qcm_sante":
            row+=empty_q1+empty_q2
            for k in SANTE_LABELS:
                v=d.get(k,""); row.append(", ".join(v) if isinstance(v,list) else str(v) if v else "")
            med=d.get("medasResult",{}); ma=med.get("answers",{})
            row+=[ma.get(k,"") for k in MEDAS_LABELS]+[med.get("score","")]
            row+=empty_mna+empty_min
        elif t=="minijeu":
            row+=empty_q1+empty_q2+empty_s+empty_m+empty_mna
            row+=[", ".join(d.get("entree",[])),", ".join(d.get("plate",[])),", ".join(d.get("dessert",[])),
                  d.get("glass",""),d.get("score","")]
        else:
            row+=empty_q1+empty_q2+empty_s+empty_m+empty_mna+empty_min
        w.writerow(row)
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]),media_type="text/csv",
                             headers={"Content-Disposition":"attachment; filename=nutri_quest_export.csv"})

@app.get("/export/json")
async def export_json():
    json_file=os.path.join(SAVE_DIR,"reponses.json")
    if not os.path.exists(json_file): return {"data":[],"message":"Aucune donnée"}
    entries=[]
    with open(json_file,"r",encoding="utf-8") as f:
        for l in f:
            if l.strip(): entries.append(json.loads(l))
    return {"total":len(entries),"data":entries}

@app.get("/stats")
async def stats():
    json_file=os.path.join(SAVE_DIR,"reponses.json")
    if not os.path.exists(json_file): return {"total":0,"par_type":{}}
    entries=[]
    with open(json_file,"r",encoding="utf-8") as f:
        for l in f:
            if l.strip(): entries.append(json.loads(l))
    par_type={}
    for e in entries: t=e.get("type","inconnu"); par_type[t]=par_type.get(t,0)+1
    return {"total":len(entries),"par_type":par_type}

@app.get("/stats/db")
async def stats_db():
    try:
        conn=get_db(); cur=conn.cursor(); res={}
        for k,q in [("sessions","SELECT COUNT(*) FROM session"),("utilisateurs","SELECT COUNT(*) FROM utilisateurs"),
                    ("reponses","SELECT COUNT(*) FROM reponse"),("medas","SELECT COUNT(*) FROM medas_result"),
                    ("mna","SELECT COUNT(*) FROM mna_result"),
                    ("score_qcm1_moyen","SELECT ROUND(AVG(score_total)) FROM session WHERE score_total>0"),
                    ("score_medas_moyen","SELECT ROUND(AVG(score_total)::numeric,1) FROM medas_result"),
                    ("score_mna_moyen","SELECT ROUND(AVG(score_mna)::numeric,1) FROM session WHERE score_mna IS NOT NULL")]:
            cur.execute(q); res[k]=cur.fetchone()[0]
        cur.close(); conn.close(); return res
    except Exception as e: return {"erreur":str(e)}