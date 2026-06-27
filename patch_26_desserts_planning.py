"""
PATCH 26 — Fix desserts (exclure de "recettes pour vous") + fix planning (PETITSDEJ manquant)
Usage: python patch_26_desserts_planning.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# FIX 1 — Exclure les desserts de "pourVous" (ils ont profils.includes("dessert") ou type Dessert)
OLD_FILTREES = '''  const filtrees = toutes.filter(r => {
    if (sansPorc    && r.profils && r.profils.includes("porc")) return false;
    if (sansViande  && r.profils && r.profils.includes("viande")) return false;
    if (pasTemps    && r.temps > 20) return false;
    return true;
  });

  const pourVous = filtrees.length > 0 ? filtrees : toutes;'''

NEW_FILTREES = '''  const filtrees = toutes.filter(r => {
    if (r.type === "Dessert" || r.type === "Dessert simple" || r.type === "Dessert gourmands") return false;
    if (r.profils && r.profils.includes("dessert") && !r.profils.includes("plat")) return false;
    if (sansPorc    && r.profils && r.profils.includes("porc")) return false;
    if (sansViande  && r.profils && r.profils.includes("viande")) return false;
    if (pasTemps    && r.temps > 20) return false;
    return true;
  });

  const desserts = toutes.filter(r =>
    r.type === "Dessert" || r.type === "Dessert simple" || r.type === "Dessert gourmands" ||
    (r.profils && r.profils.includes("dessert"))
  );

  const pourVous = filtrees.length > 0 ? filtrees : toutes.filter(r => r.type !== "Dessert" && r.type !== "Dessert simple" && r.type !== "Dessert gourmands");'''

if OLD_FILTREES in code:
    code = code.replace(OLD_FILTREES, NEW_FILTREES)
    fixes += 1
    print("✅ FIX 1 — Desserts exclus de 'Recettes pour vous'")
else:
    print("⚠️  FIX 1 — filtre non trouvé")

# FIX 2 — Définir PETITSDEJ et DESSERTS_DEFAUT AVANT genererPlanning (dans le scope de la fonction)
OLD_GENERER = '''  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;'''

NEW_GENERER = '''  const PETITSDEJ = [
    "Yaourt + fruit frais + pain complet",
    "Flocons d'avoine + lait + banane",
    "Pain complet + fromage blanc + fruit",
    "Smoothie fruits + pain complet",
    "Oeuf à la coque + tartine complète + jus d'orange",
    "Müesli + lait végétal + fraises",
    "Pancakes complets + compote de pommes",
  ];
  const DESSERTS_DEFAUT = [
    "Compote de pommes", "Yaourt au fruit", "Salade de fruits",
    "Carré de chocolat noir + noix", "Fromage blanc + miel",
    "Fruit de saison", "Crème dessert maison",
  ];

  const genererPlanning = () => {
    if (!dateDebut || !dateFin) return;'''

if OLD_GENERER in code:
    code = code.replace(OLD_GENERER, NEW_GENERER)
    fixes += 1
    print("✅ FIX 2 — PETITSDEJ et DESSERTS_DEFAUT définis dans le bon scope")
else:
    print("⚠️  FIX 2 — genererPlanning non trouvé")

# FIX 3 — Utiliser les vrais desserts dans le planning
OLD_DESSERT_REC = '''      const dessertRec = recsMelangees.find(r => r.type === "Dessert" || (r.profils && r.profils.includes("dessert")));
      const dessertNom = dessertRec?.name || DESSERTS_DEFAUT[idx % DESSERTS_DEFAUT.length];'''

NEW_DESSERT_REC = '''      const dessertRec = desserts[idx % (desserts.length || 1)];
      const dessertNom = dessertRec?.titre || dessertRec?.name || DESSERTS_DEFAUT[idx % DESSERTS_DEFAUT.length];'''

if OLD_DESSERT_REC in code:
    code = code.replace(OLD_DESSERT_REC, NEW_DESSERT_REC)
    fixes += 1
    print("✅ FIX 3 — Vrais desserts utilisés dans le planning")
else:
    print("⚠️  FIX 3 — dessertRec non trouvé")

# FIX 4 — Utiliser titre au lieu de name pour les recettes dans le planning
OLD_DEJ_NOM = '''      const recDej = recsMelangees[idx % recsMelangees.length];
      const recDin = recsMelangees[(idx + Math.ceil(recsMelangees.length / 2)) % recsMelangees.length];
      const dejNom = recDej?.name !== recDin?.name ? recDej?.name : DEJEUNERS_DEFAUT[idx % DEJEUNERS_DEFAUT.length];
      const dinNom = recDin?.name || DINERS_DEFAUT[idx % DINERS_DEFAUT.length];'''

NEW_DEJ_NOM = '''      const recDej = recsMelangees[idx % recsMelangees.length];
      const recDin = recsMelangees[(idx + Math.ceil(recsMelangees.length / 2)) % recsMelangees.length];
      const dejLabel = recDej?.titre || recDej?.name;
      const dinLabel = recDin?.titre || recDin?.name;
      const dejNom = dejLabel !== dinLabel ? dejLabel : DEJEUNERS_DEFAUT[idx % DEJEUNERS_DEFAUT.length];
      const dinNom = dinLabel || DINERS_DEFAUT[idx % DINERS_DEFAUT.length];'''

if OLD_DEJ_NOM in code:
    code = code.replace(OLD_DEJ_NOM, NEW_DEJ_NOM)
    fixes += 1
    print("✅ FIX 4 — Titres des recettes utilisés (titre au lieu de name)")
else:
    print("⚠️  FIX 4 — recDej non trouvé")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/4 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
