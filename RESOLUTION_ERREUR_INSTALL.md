# 🔧 Résolution : Erreur "destination path already exists"

## Problème

Lors de l'installation sur PythonAnywhere, vous obtenez :
```
fatal: destination path '.' already exists and is not an empty directory.
```

## ✅ Solutions

### Solution 1 : Mettre à jour (si déjà installé)

Si vous avez déjà installé le projet et voulez juste récupérer les dernières modifications :

```bash
cd ~/TAL-migration
git pull origin main
pip3.10 install --user -r requirements.txt
```

### Solution 2 : Supprimer et réinstaller

Si vous voulez tout recommencer :

```bash
cd ~
rm -rf TAL-migration
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration
bash INSTALL_PYTHONANYWHERE.sh
```

### Solution 3 : Utiliser le script mis à jour

Le script `INSTALL_PYTHONANYWHERE.sh` a été mis à jour pour gérer ce cas automatiquement.

**Mettez d'abord à jour le script** :
```bash
cd ~/TAL-migration
git pull origin main
```

**Puis relancez** :
```bash
bash INSTALL_PYTHONANYWHERE.sh
```

Le script vous proposera :
1. Mettre à jour depuis GitHub (recommandé)
2. Supprimer et réinstaller
3. Annuler

## 🚀 Installation rapide (si dossier existe déjà)

```bash
cd ~/TAL-migration
git pull origin main
pip3.10 install --user -r requirements.txt
```

Puis continuez avec la configuration :
```bash
nano config.py
python3.10 connexion_odoo.py
```

