# 🚀 Démarrage Rapide - TAL-migration

## Sur votre machine locale

### 1. Initialiser Git (première fois)

```bash
cd TAL-migration
git init
git remote add origin https://github.com/VOTRE_USERNAME/TAL-migration.git
```

### 2. Sauvegarder sur GitHub

**Windows :** Double-cliquez sur `COMMIT_ET_PUSH.bat`

**Linux/Mac :**
```bash
git add -A
git commit -F COMMIT_MESSAGE.txt
git push origin main
```

## Sur PythonAnywhere

### Option 1 : Installation automatique

```bash
cd ~
bash <(curl -s https://raw.githubusercontent.com/VOTRE_USERNAME/TAL-migration/main/INSTALL_PYTHONANYWHERE.sh)
```

### Option 2 : Installation manuelle

```bash
# 1. Cloner le dépôt
cd ~
git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
cd TAL-migration

# 2. Installer les dépendances
pip3.10 install --user -r requirements.txt

# 3. Créer config.py depuis le template
cp config.py.template config.py
nano config.py  # Modifiez avec vos identifiants

# 4. Créer le dossier pour les PDFs
mkdir -p Factures_pdf_TAL

# 5. Tester la connexion
python3.10 connexion_odoo.py

# 6. Lancer un test (10 factures)
python3.10 transferer_factures_documents_v2.py
```

## Mise à jour depuis GitHub

Sur PythonAnywhere :
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

## Commandes utiles

### Test de connexion
```bash
python3.10 connexion_odoo.py
```

### Test sur 100 factures
```bash
python3.10 transferer_factures_documents_v2.py
```

### Transfert complet de toutes les factures
```bash
python3.10 transferer_factures_documents_v2.py --all
```

### Gérer la progression
```bash
python3.10 gestion_progression.py afficher
python3.10 gestion_progression.py reinitialiser
python3.10 gestion_progression.py nettoyer
```

## ⚠️ Important

- Le fichier `config.py` avec vos mots de passe **n'est PAS commité** (dans .gitignore)
- Créez-le manuellement sur chaque machine (local et PythonAnywhere)
- Utilisez `config.py.template` comme modèle

