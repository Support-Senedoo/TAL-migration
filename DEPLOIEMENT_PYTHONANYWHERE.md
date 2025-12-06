# 🚀 Déploiement sur PythonAnywhere

Ce guide explique comment synchroniser et exécuter les scripts TAL-migration depuis PythonAnywhere.

## 📋 Prérequis

1. Compte GitHub avec le dépôt TAL-migration
2. Compte PythonAnywhere (gratuit ou payant)
3. Accès SSH à PythonAnywhere

## 🔄 Étape 1: Synchronisation avec GitHub

### Sur votre machine locale

1. **Initialiser Git (si pas déjà fait)**
   ```bash
   cd TAL-migration
   git init
   git remote add origin https://github.com/VOTRE_USERNAME/TAL-migration.git
   ```

2. **Créer le fichier COMMIT_MESSAGE.txt** (déjà créé)
   - Modifiez-le avec votre message de commit

3. **Sauvegarder sur GitHub**
   - Double-cliquez sur `COMMIT_ET_PUSH.bat`
   - Ou en ligne de commande :
     ```bash
     git add -A
     git commit -F COMMIT_MESSAGE.txt
     git push origin main
     ```

## 📥 Étape 2: Télécharger sur PythonAnywhere

### Via SSH

1. **Se connecter à PythonAnywhere**
   ```bash
   ssh votre_username@ssh.pythonanywhere.com
   ```

2. **Créer le dossier du projet**
   ```bash
   mkdir -p ~/TAL-migration
   cd ~/TAL-migration
   ```

3. **Cloner le dépôt GitHub**
   ```bash
   git clone https://github.com/VOTRE_USERNAME/TAL-migration.git .
   ```

   Ou si le dossier existe déjà :
   ```bash
   git pull origin main
   ```

## ⚙️ Étape 3: Configuration sur PythonAnywhere

1. **Installer les dépendances**
   ```bash
   cd ~/TAL-migration
   pip3.10 install --user -r requirements.txt
   ```

2. **Créer le fichier de configuration**
   ```bash
   nano config.py
   ```
   
   Modifiez avec vos identifiants Odoo (le fichier config.py ne sera PAS commité si vous l'ajoutez au .gitignore)

3. **Créer le dossier pour les PDFs**
   ```bash
   mkdir -p Factures_pdf_TAL
   ```

## 🎯 Étape 4: Exécution depuis PythonAnywhere

### Via Console Bash

```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

### Via Scheduled Task (tâche planifiée)

1. Allez sur **Tasks** dans le dashboard PythonAnywhere
2. Créez une nouvelle tâche :
   - **Command**: `cd ~/TAL-migration && python3.10 transferer_factures_documents_v2.py --all`
   - **Hour**: Choisissez l'heure
   - **Minute**: Choisissez la minute

### Via Web App (optionnel)

Créez un fichier `webapp.py` dans votre web app PythonAnywhere :

```python
import sys
sys.path.insert(0, '/home/votre_username/TAL-migration')

from transferer_factures_documents_v2 import transferer_factures_vers_documents

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    result = transferer_factures_vers_documents(limit=10, reprendre=True, test_mode=True)
    
    return [f"<h1>Transfert terminé: {result}</h1>".encode('utf-8')]
```

## 🔄 Synchronisation continue

### Mettre à jour depuis GitHub

Sur PythonAnywhere :
```bash
cd ~/TAL-migration
git pull origin main
```

### Pousser les changements depuis PythonAnywhere

Si vous modifiez des fichiers sur PythonAnywhere :
```bash
cd ~/TAL-migration
git add -A
git commit -m "Modifications depuis PythonAnywhere"
git push origin main
```

## 📝 Notes importantes

1. **Fichiers sensibles** : `config.py` avec les mots de passe ne doit PAS être commité
2. **Fichiers volumineux** : Les PDFs dans `Factures_pdf_TAL/` ne sont pas commités
3. **Progression** : Le fichier `progression_transfert.json` n'est pas commité (local uniquement)

## 🛠️ Scripts utiles

### Script de mise à jour rapide

Créez `update_from_github.sh` sur PythonAnywhere :

```bash
#!/bin/bash
cd ~/TAL-migration
git pull origin main
echo "Mise à jour terminée!"
```

Rendez-le exécutable :
```bash
chmod +x update_from_github.sh
```

### Script de sauvegarde locale

Créez `backup_progression.sh` :

```bash
#!/bin/bash
cd ~/TAL-migration
cp progression_transfert.json progression_transfert_backup_$(date +%Y%m%d_%H%M%S).json
echo "Sauvegarde créée!"
```

## ✅ Checklist de déploiement

- [ ] Dépôt GitHub créé et synchronisé
- [ ] Projet cloné sur PythonAnywhere
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] `config.py` configuré avec les bons identifiants
- [ ] Dossier `Factures_pdf_TAL/` créé
- [ ] Test de connexion réussi (`python3.10 connexion_odoo.py`)
- [ ] Test sur 10 factures réussi
- [ ] Tâche planifiée configurée (optionnel)

## 🆘 Dépannage

### Erreur "Module not found"
```bash
pip3.10 install --user --upgrade requests pandas openpyxl
```

### Erreur de connexion Odoo
- Vérifiez `config.py` sur PythonAnywhere
- Vérifiez que l'URL est accessible depuis PythonAnywhere

### Erreur de permissions
```bash
chmod +x *.py
chmod 755 Factures_pdf_TAL
```

## 📞 Support

En cas de problème, vérifiez :
1. Les logs dans la console PythonAnywhere
2. Le fichier `progression_transfert.json` pour voir où le script s'est arrêté
3. Les permissions des fichiers et dossiers

