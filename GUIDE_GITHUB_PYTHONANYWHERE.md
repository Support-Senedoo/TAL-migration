# 🚀 Guide Complet : GitHub + PythonAnywhere

## Étape 1 : Créer le dépôt GitHub

1. **Allez sur GitHub.com** et connectez-vous
2. Cliquez sur **"New repository"** (ou le bouton "+" en haut à droite)
3. Remplissez :
   - **Repository name** : `TAL-migration`
   - **Description** : `Scripts de transfert des factures TAL vers le module Document Odoo`
   - **Visibility** : Private (recommandé) ou Public
   - **NE COCHEZ PAS** "Initialize with README" (on a déjà nos fichiers)
4. Cliquez sur **"Create repository"**

## Étape 2 : Connecter votre dépôt local à GitHub

**Copiez l'URL de votre dépôt GitHub** (elle ressemble à : `https://github.com/VOTRE_USERNAME/TAL-migration.git`)

Ensuite, exécutez ces commandes dans le terminal :

```bash
cd TAL-migration
git remote add origin https://github.com/VOTRE_USERNAME/TAL-migration.git
git branch -M main
```

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub.

## Étape 3 : Premier commit et push

Les fichiers sont déjà préparés. Exécutez :

```bash
git commit -m "Initial commit: Scripts transfert factures TAL optimisés"
git push -u origin main
```

Si GitHub vous demande des identifiants :
- **Username** : Votre nom d'utilisateur GitHub
- **Password** : Utilisez un **Personal Access Token** (pas votre mot de passe)

### Créer un Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Donnez-lui un nom (ex: "TAL-migration")
4. Cochez `repo` (accès complet aux dépôts)
5. Generate token
6. **COPIEZ LE TOKEN** (vous ne le reverrez plus !)
7. Utilisez ce token comme mot de passe lors du `git push`

## Étape 4 : Vérification sur GitHub

Allez sur votre dépôt GitHub. Vous devriez voir tous les fichiers, **SAUF** :
- ❌ `config.py` (bien protégé)
- ❌ `progression_transfert.json` (données locales)
- ❌ `Factures_pdf_TAL/` (PDFs locaux)

## Étape 5 : Installation sur PythonAnywhere

### Option A : Installation automatique (recommandé)

1. **Connectez-vous en SSH** à PythonAnywhere :
   ```bash
   ssh votre_username@ssh.pythonanywhere.com
   ```

2. **Exécutez le script d'installation** :
   ```bash
   cd ~
   git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
   cd TAL-migration
   bash INSTALL_PYTHONANYWHERE.sh
   ```

3. **Quand le script demande votre nom d'utilisateur GitHub**, entrez-le

4. **Configurez config.py** :
   ```bash
   nano config.py
   ```
   Modifiez avec vos identifiants Odoo (URL, DB, USER, PASS)

### Option B : Installation manuelle

```bash
# 1. Se connecter en SSH
ssh votre_username@ssh.pythonanywhere.com

# 2. Cloner le dépôt
cd ~
git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
cd TAL-migration

# 3. Installer les dépendances
pip3.10 install --user -r requirements.txt

# 4. Créer config.py depuis le template
cp config.py.template config.py
nano config.py  # Modifiez avec vos identifiants

# 5. Créer le dossier pour les PDFs
mkdir -p Factures_pdf_TAL

# 6. Tester la connexion
python3.10 connexion_odoo.py
```

## Étape 6 : Lancer le script sur PythonAnywhere

### Test (100 factures)
```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

### Transfert complet
```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py --all
```

### Via Scheduled Task (tâche planifiée)

1. Allez sur **PythonAnywhere Dashboard** → **Tasks**
2. Cliquez sur **"Create a task"**
3. Configurez :
   - **Command** : `cd ~/TAL-migration && python3.10 transferer_factures_documents_v2.py --all`
   - **Hour** : Choisissez l'heure
   - **Minute** : Choisissez la minute
4. Cliquez sur **"Create"**

## Étape 7 : Mise à jour depuis GitHub

Quand vous modifiez des fichiers localement et les poussez sur GitHub :

### Sur votre machine locale
```bash
cd TAL-migration
git add -A
git commit -F COMMIT_MESSAGE.txt
git push origin main
```

### Sur PythonAnywhere
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

## 🔄 Workflow quotidien recommandé

### Développement local
1. Modifiez les scripts
2. Testez localement
3. Modifiez `COMMIT_MESSAGE.txt`
4. Exécutez `COMMIT_ET_PUSH.bat` (ou commandes Git)
5. Scripts synchronisés sur GitHub ✅

### Exécution sur PythonAnywhere
1. SSH vers PythonAnywhere
2. `cd ~/TAL-migration`
3. `bash update_from_github.sh` (mise à jour)
4. `python3.10 transferer_factures_documents_v2.py --all`

## ✅ Checklist de vérification

### GitHub
- [ ] Dépôt créé sur GitHub
- [ ] Dépôt local connecté (`git remote -v`)
- [ ] Premier push réussi
- [ ] `config.py` n'apparaît PAS sur GitHub (bien protégé)

### PythonAnywhere
- [ ] Dépôt cloné
- [ ] Dépendances installées
- [ ] `config.py` créé avec les bons identifiants
- [ ] Test de connexion réussi
- [ ] Dossier `Factures_pdf_TAL/` créé

## 🆘 Problèmes courants

### Erreur "repository not found"
- Vérifiez l'URL du dépôt GitHub
- Vérifiez que vous utilisez un Personal Access Token, pas votre mot de passe

### Erreur "config.py not found" sur PythonAnywhere
- Vous devez créer `config.py` manuellement depuis `config.py.template`
- `cp config.py.template config.py` puis `nano config.py`

### Erreur "Module not found" sur PythonAnywhere
```bash
pip3.10 install --user --upgrade -r requirements.txt
```

### Le script est lent sur PythonAnywhere
- Normal, les serveurs PythonAnywhere sont partagés
- Le temps estimé est indicatif, peut varier selon la charge

## 📞 Commandes utiles

### Vérifier l'état Git
```bash
git status
```

### Voir les remotes
```bash
git remote -v
```

### Forcer la mise à jour (si nécessaire)
```bash
git pull origin main --force
```

### Voir les logs
```bash
git log --oneline
```

