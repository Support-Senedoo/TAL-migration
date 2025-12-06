# 🔄 Synchronisation GitHub - Guide Complet

## 📋 Vue d'ensemble

Ce projet est maintenant configuré pour être synchronisé avec GitHub et exécutable depuis PythonAnywhere.

## 🔐 Sécurité

✅ **Fichiers protégés** (dans `.gitignore`, ne seront PAS commités) :
- `config.py` - Contient vos mots de passe Odoo
- `progression_transfert.json` - Données locales de progression
- `Factures_pdf_TAL/` - PDFs sauvegardés localement
- `*.pdf` - Tous les fichiers PDF

✅ **Fichiers commités** :
- Tous les scripts Python
- `config.py.template` - Template sans mots de passe
- Documentation
- Scripts de déploiement

## 🚀 Première synchronisation

### 1. Initialiser Git (si pas déjà fait)

```bash
cd TAL-migration
git init
git remote add origin https://github.com/VOTRE_USERNAME/TAL-migration.git
```

### 2. Vérifier que config.py est ignoré

```bash
git status
# config.py ne doit PAS apparaître dans la liste
```

### 3. Premier commit

```bash
git add -A
git commit -m "Initial commit: Scripts de transfert factures TAL"
git push -u origin main
```

## 📤 Synchronisation régulière

### Sur votre machine locale

**Méthode 1 : Script Windows**
- Double-cliquez sur `COMMIT_ET_PUSH.bat`
- Le script utilise `COMMIT_MESSAGE.txt` pour le message

**Méthode 2 : Ligne de commande**
```bash
git add -A
git commit -F COMMIT_MESSAGE.txt
git push origin main
```

## 📥 Sur PythonAnywhere

### Installation initiale

```bash
cd ~
git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
cd TAL-migration

# Installer dépendances
pip3.10 install --user -r requirements.txt

# Créer config.py depuis le template
cp config.py.template config.py
nano config.py  # Modifiez avec vos identifiants

# Créer dossier PDFs
mkdir -p Factures_pdf_TAL
```

### Mise à jour depuis GitHub

```bash
cd ~/TAL-migration
bash update_from_github.sh
```

Ou manuellement :
```bash
cd ~/TAL-migration
git pull origin main
pip3.10 install --user -r requirements.txt
```

## 📝 Workflow recommandé

### Développement local

1. Modifier les scripts
2. Tester localement
3. Modifier `COMMIT_MESSAGE.txt` avec votre message
4. Exécuter `COMMIT_ET_PUSH.bat`
5. Scripts synchronisés sur GitHub

### Exécution sur PythonAnywhere

1. Se connecter en SSH
2. `cd ~/TAL-migration`
3. `bash update_from_github.sh` (mise à jour)
4. `python3.10 transferer_factures_documents_v2.py --all`

## 🛠️ Scripts disponibles

| Script | Description |
|--------|-------------|
| `COMMIT_ET_PUSH.bat` | Sauvegarde sur GitHub (Windows) |
| `update_from_github.sh` | Mise à jour depuis GitHub (Linux/PythonAnywhere) |
| `INSTALL_PYTHONANYWHERE.sh` | Installation complète sur PythonAnywhere |
| `transferer_factures_documents_v2.py` | Script principal optimisé |
| `gestion_progression.py` | Gestion de la progression |

## ✅ Checklist avant commit

- [ ] `config.py` n'est PAS dans la liste des fichiers à commiter
- [ ] `progression_transfert.json` n'est PAS dans la liste
- [ ] Aucun fichier PDF dans la liste
- [ ] Message de commit préparé dans `COMMIT_MESSAGE.txt`
- [ ] Tests locaux réussis

## 🔍 Vérification

Pour vérifier ce qui sera commité :
```bash
git status
```

Pour voir les fichiers ignorés :
```bash
git status --ignored
```

## 📚 Documentation

- `README.md` - Documentation principale
- `DEPLOIEMENT_PYTHONANYWHERE.md` - Guide déploiement détaillé
- `DEMARRAGE_RAPIDE.md` - Guide de démarrage rapide


