# 📋 Comment capturer et partager les erreurs

## Méthode 1 : Script automatique

Sur PythonAnywhere, exécutez :

```bash
cd ~/TAL-migration
bash CAPTURE_ERREURS.sh
```

Puis affichez le fichier créé :

```bash
cat erreurs_*.log
```

Copiez-collez tout le contenu du fichier.

## Méthode 2 : Redirection simple

Exécutez votre commande et redirigez vers un fichier :

```bash
cd ~/TAL-migration
bash update_from_github.sh > erreur.txt 2>&1
cat erreur.txt
```

Puis copiez-collez le contenu de `erreur.txt`.

## Méthode 3 : Commande avec capture

Pour toute commande, ajoutez `2>&1 | tee erreur.txt` :

```bash
cd ~/TAL-migration
git pull origin main 2>&1 | tee erreur.txt
cat erreur.txt
```

