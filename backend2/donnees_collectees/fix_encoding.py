import os

fichiers = ['reponses.json', 'reponses.csv']

for fichier in fichiers:
    if os.path.exists(fichier):
        try:
            with open(fichier, 'r', encoding='latin-1') as f:
                contenu = f.read()
            with open(fichier, 'w', encoding='utf-8') as f:
                f.write(contenu)
            print(f"✅ {fichier} corrigé !")
        except Exception as e:
            print(f"❌ Erreur sur {fichier} : {e}")
    else:
        print(f"⚠️ {fichier} non trouvé")
