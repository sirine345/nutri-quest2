"""
PATCH 24 — Planning semaine : menu différent chaque jour (shuffle)
Usage: python patch_24_planning_varié.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

OLD = '''  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;
    const start = new Date(dateDebut);
    const end   = new Date(dateFin);
    const jours = [];
    const noms  = ["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"];
    const mois  = ["jan","fév","mar","avr","mai","juin","juil","aoû","sep","oct","nov","déc"];
    let cur = new Date(start);
    let idx = 0;
    while (cur <= end && jours.length < 14) {
      const recDej  = pourVous[idx % pourVous.length];
      const recDin  = pourVous[(idx + 1) % pourVous.length];
      jours.push({
        nom: noms[cur.getDay()],
        date: `${cur.getDate()} ${mois[cur.getMonth()]}`,
        dej:  recDej?.name  || "Salade composée",
        din:  recDin?.name  || "Soupe + pain",
      });
      cur.setDate(cur.getDate() + 1);
      idx += 2;
    }
    setPlanning(jours);
  };'''

NEW = '''  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;
    const start = new Date(dateDebut);
    const end   = new Date(dateFin);
    const jours = [];
    const noms  = ["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"];
    const mois  = ["jan","fév","mar","avr","mai","juin","juil","aoû","sep","oct","nov","déc"];

    // Mélange aléatoire des recettes pour varier chaque jour
    const shuffle = (arr) => {
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    };

    // Plats de secours si pas assez de recettes
    const DEJEUNERS_DEFAUT = ["Salade composée", "Quiche légumes", "Soupe + pain complet", "Riz sauté légumes", "Omelette champignons", "Taboulé maison", "Wrap thon crudités"];
    const DINERS_DEFAUT    = ["Soupe + tartines", "Lentilles vapeur", "Oeufs cocotte", "Poêlée légumes", "Purée + poisson", "Velouté carottes", "Ratatouille + riz"];

    const recsMelangees = shuffle(pourVous);
    let cur = new Date(start);
    let idx = 0;

    while (cur <= end && jours.length < 14) {
      const recDej = recsMelangees[idx % recsMelangees.length];
      const recDin = recsMelangees[(idx + Math.ceil(recsMelangees.length / 2)) % recsMelangees.length];
      const dejNom = recDej?.name !== recDin?.name ? recDej?.name : DEJEUNERS_DEFAUT[idx % DEJEUNERS_DEFAUT.length];
      const dinNom = recDin?.name || DINERS_DEFAUT[idx % DINERS_DEFAUT.length];
      jours.push({
        nom:  noms[cur.getDay()],
        date: `${cur.getDate()} ${mois[cur.getMonth()]}`,
        dej:  dejNom,
        din:  dinNom !== dejNom ? dinNom : DINERS_DEFAUT[idx % DINERS_DEFAUT.length],
      });
      cur.setDate(cur.getDate() + 1);
      idx++;
    }
    setPlanning(jours);
  };'''

if OLD in code:
    code = code.replace(OLD, NEW)
    print("✅ FIX 1 — Planning : menu différent chaque jour avec shuffle")
else:
    print("⚠️  Fonction genererPlanning non trouvée")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
