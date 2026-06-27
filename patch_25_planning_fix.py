"""
PATCH 25 — Planning : petit-déj varié + ajout recettes dessert dans RECETTES_DATA
Usage: python patch_25_planning_fix.py App.jsx
"""
import sys

with open(sys.argv[1], 'r', encoding='utf-8', errors='replace') as f:
    code = f.read()

fixes = 0

# FIX 1 — Ajouter recettes dessert dans RECETTES_DATA
OLD_END_RECETTES = '  { id:"lentilles_lardons"'
NEW_RECETTES_DESSERT = '''  { id:"compote_pomme", image:"/compote.png", categorie:"Desserts", tag:"Sans cuisson", temps:"5 min", type:"Dessert",
    profils:["rapide","sans_porc","vegetarien","mediterraneen"],
    titre:"Compote de pommes maison",
    benefice:"La pomme est riche en fibres et en antioxydants. Une compote maison sans sucre ajouté est idéale pour finir un repas légèrement.",
    source:"mangerbouger.fr", url:"https://www.mangerbouger.fr",
    ingredients:["4 pommes","1 cuillère à café de cannelle","2 cuillères à soupe d'eau"],
    etapes:["Éplucher et couper les pommes en dés.","Faire cuire à feu doux avec l'eau 15 min.","Mixer et ajouter la cannelle."],
    name:"Compote de pommes maison", description:"Compote légère sans sucre ajouté."
  },
  { id:"yaourt_fruit", image:"/yaourt.png", categorie:"Desserts", tag:"Sans cuisson", temps:"5 min", type:"Dessert",
    profils:["rapide","sans_porc","vegetarien"],
    titre:"Yaourt au fruit frais",
    benefice:"Le yaourt apporte du calcium et des protéines. Les fruits frais ajoutent des vitamines et des fibres.",
    source:"mangerbouger.fr", url:"https://www.mangerbouger.fr",
    ingredients:["1 yaourt nature","1 fruit de saison (fraise, pêche, kiwi)","1 cuillère à café de miel"],
    etapes:["Couper le fruit en morceaux.","Mélanger avec le yaourt.","Ajouter un filet de miel si souhaité."],
    name:"Yaourt au fruit frais", description:"Dessert simple, rapide et nutritif."
  },
  { id:"gateau_carotte", image:"/gateau.png", categorie:"Desserts", tag:"Four", temps:"40 min", type:"Dessert",
    profils:["vegetarien","sans_porc"],
    titre:"Gâteau aux carottes",
    benefice:"Les carottes apportent du bêta-carotène. Ce gâteau est moins sucré qu'un dessert classique.",
    source:"mangerbouger.fr", url:"https://www.mangerbouger.fr",
    ingredients:["200g de carottes râpées","2 oeufs","100g de farine complète","60g de sucre","1 sachet de levure","100ml d'huile"],
    etapes:["Mélanger les oeufs et le sucre.","Ajouter la farine, la levure et l'huile.","Incorporer les carottes.","Cuire 35 min à 180°C."],
    name:"Gâteau aux carottes", description:"Gâteau moelleux aux légumes, moins sucré."
  },
  { id:"salade_fruits", image:"/fraise.png", categorie:"Desserts", tag:"Sans cuisson", temps:"10 min", type:"Dessert",
    profils:["rapide","sans_porc","vegetarien","mediterraneen","legumes"],
    titre:"Salade de fruits de saison",
    benefice:"Les fruits apportent vitamines, minéraux et fibres. Une salade de fruits est le dessert idéal pour atteindre les 5 fruits et légumes par jour.",
    source:"mangerbouger.fr", url:"https://www.mangerbouger.fr",
    ingredients:["1 pomme","1 orange","1 banane","quelques fraises","jus d'un demi citron","quelques feuilles de menthe"],
    etapes:["Couper tous les fruits en morceaux.","Arroser de jus de citron.","Décorer de feuilles de menthe."],
    name:"Salade de fruits de saison", description:"Dessert frais et vitaminé."
  },
  { id:"lentilles_lardons"'''

if OLD_END_RECETTES in code:
    code = code.replace(OLD_END_RECETTES, NEW_RECETTES_DESSERT)
    fixes += 1
    print("✅ FIX 1 — 4 recettes dessert ajoutées dans RECETTES_DATA")
else:
    print("⚠️  FIX 1 — Marqueur lentilles_lardons non trouvé")

# FIX 2 — Varier le petit-déjeuner dans le planning
OLD_PETITDEJ = '''      const DEJEUNERS_DEFAUT = ["Salade composée", "Quiche légumes", "Soupe + pain complet", "Riz sauté légumes", "Omelette champignons", "Taboulé maison", "Wrap thon crudités"];
    const DINERS_DEFAUT    = ["Soupe + tartines", "Lentilles vapeur", "Oeufs cocotte", "Poêlée légumes", "Purée + poisson", "Velouté carottes", "Ratatouille + riz"];'''

NEW_PETITDEJ = '''      const PETITSDEJ = [
        "Yaourt + fruit frais + pain complet",
        "Flocons d'avoine + lait + banane",
        "Pain complet + fromage blanc + fruit",
        "Smoothie fruits + pain complet",
        "Oeuf à la coque + tartine complète + jus d'orange",
        "Müesli + lait végétal + fraises",
        "Pancakes complets + compote de pommes",
      ];
    const DEJEUNERS_DEFAUT = ["Salade composée", "Quiche légumes", "Soupe + pain complet", "Riz sauté légumes", "Omelette champignons", "Taboulé maison", "Wrap thon crudités"];
    const DINERS_DEFAUT    = ["Soupe + tartines", "Lentilles vapeur", "Oeufs cocotte", "Poêlée légumes", "Purée + poisson", "Velouté carottes", "Ratatouille + riz"];
    const DESSERTS_DEFAUT  = ["Compote de pommes", "Yaourt au fruit", "Salade de fruits", "Carré de chocolat noir + noix", "Fromage blanc + miel", "Fruit de saison", "Gâteau aux carottes"];'''

if OLD_PETITDEJ in code:
    code = code.replace(OLD_PETITDEJ, NEW_PETITDEJ)
    fixes += 1
    print("✅ FIX 2 — Petit-déjeuners variés ajoutés")
else:
    print("⚠️  FIX 2 — DEJEUNERS_DEFAUT non trouvé")

# FIX 3 — Utiliser les petits-déj variés et ajouter dessert dans le planning
OLD_JOUR = '''      jours.push({
        nom:  noms[cur.getDay()],
        date: `${cur.getDate()} ${mois[cur.getMonth()]}`,
        dej:  dejNom,
        din:  dinNom !== dejNom ? dinNom : DINERS_DEFAUT[idx % DINERS_DEFAUT.length],
      });'''

NEW_JOUR = '''      const dessertRec = recsMelangees.find(r => r.type === "Dessert" || (r.profils && r.profils.includes("dessert")));
      const dessertNom = dessertRec?.name || DESSERTS_DEFAUT[idx % DESSERTS_DEFAUT.length];
      jours.push({
        nom:     noms[cur.getDay()],
        date:    `${cur.getDate()} ${mois[cur.getMonth()]}`,
        petitdej: PETITSDEJ[idx % PETITSDEJ.length],
        dej:     dejNom,
        din:     dinNom !== dejNom ? dinNom : DINERS_DEFAUT[idx % DINERS_DEFAUT.length],
        dessert: dessertNom,
      });'''

if OLD_JOUR in code:
    code = code.replace(OLD_JOUR, NEW_JOUR)
    fixes += 1
    print("✅ FIX 3 — Dessert et petit-déj ajoutés dans chaque jour")
else:
    print("⚠️  FIX 3 — jours.push non trouvé")

# FIX 4 — Afficher petit-déj et dessert dans le rendu du planning
OLD_REPAS = '''      {[
                      { emoji:"🌅", repas:"Petit-déjeuner", plat:"Yaourt + fruit + pain complet" },
                      { emoji:"☀️", repas:"Déjeuner",       plat:j.dej },
                      { emoji:"🌙", repas:"Dîner",          plat:j.din },
                    ].map((r, ri) => ('''

NEW_REPAS = '''      {[
                      { emoji:"🌅", repas:"Petit-déjeuner", plat:j.petitdej || "Yaourt + fruit + pain complet" },
                      { emoji:"☀️", repas:"Déjeuner",       plat:j.dej },
                      { emoji:"🌙", repas:"Dîner",          plat:j.din },
                      { emoji:"🍮", repas:"Dessert",         plat:j.dessert },
                    ].map((r, ri) => ('''

if OLD_REPAS in code:
    code = code.replace(OLD_REPAS, NEW_REPAS)
    fixes += 1
    print("✅ FIX 4 — Petit-déj varié et dessert affichés dans le planning")
else:
    print("⚠️  FIX 4 — Rendu planning non trouvé")

# FIX 5 — Mettre grid 4 colonnes au lieu de 3 pour afficher les 4 repas
OLD_GRID3 = 'gridTemplateColumns:"1fr 1fr 1fr"'
NEW_GRID4 = 'gridTemplateColumns:"1fr 1fr 1fr 1fr"'
# Only replace the one in the planning section
if OLD_GRID3 in code:
    code = code.replace(OLD_GRID3, NEW_GRID4, 1)
    fixes += 1
    print("✅ FIX 5 — Grille planning passée en 4 colonnes")

out = sys.argv[1].replace('.jsx', '_patched.jsx')
with open(out, 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/5 fix(es) appliqué(s)")
print(f"Fichier : {out}")
print("→ Copy-Item App_patched.jsx App.jsx -Force")
