# 🎯 Étapes Finales : GitHub + PythonAnywhere

## ✅ État Actuel

✅ Git initialisé localement  
✅ Tous les fichiers commités (sauf config.py qui est protégé)  
✅ 2 commits créés

## 📤 ÉTAPE 1 : Créer le dépôt sur GitHub

1. **Allez sur** https://github.com et connectez-vous

2. **Cliquez sur** le bouton **"+"** (en haut à droite) → **"New repository"**

3. **Remplissez le formulaire** :
   - **Repository name** : `TAL-migration`
   - **Description** : `Scripts de transfert des factures TAL vers le module Document Odoo`
   - **Visibility** : 
     - ✅ **Private** (recommandé - plus sûr pour vos mots de passe)
     - Ou Public si vous voulez partager
   - **❌ NE COCHEZ PAS** "Add a README file" (on a déjà le nôtre)
   - **❌ NE COCHEZ PAS** "Add .gitignore" (on a déjà le nôtre)
   - **❌ NE COCHEZ PAS** "Choose a license"

4. **Cliquez sur** **"Create repository"**

## 📡 ÉTAPE 2 : Connecter votre dépôt local à GitHub

Après avoir créé le dépôt, GitHub vous montre une page avec des instructions.

**Copiez l'URL HTTPS** de votre dépôt (elle ressemble à) :
```
https://github.com/VOTRE_USERNAME/TAL-migration.git
```

**Puis exécutez ces commandes** dans votre terminal (dans le dossier TAL-migration) :

```bash
git remote add origin https://github.com/VOTRE_USERNAME/TAL-migration.git
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANT :** Remplacez `VOTRE_USERNAME` par votre vrai nom d'utilisateur GitHub !

## 🔐 ÉTAPE 3 : Authentification GitHub

Si GitHub vous demande des identifiants lors du `git push` :

### Option A : Personal Access Token (recommandé)

1. **Créez un token** :
   - Allez sur GitHub → **Settings** (votre profil en haut à droite)
   - Dans le menu de gauche : **Developer settings**
   - Cliquez sur **Personal access tokens** → **Tokens (classic)**
   - Cliquez sur **Generate new token** → **Generate new token (classic)**
   - Donnez un nom : `TAL-migration`
   - Sélectionnez l'expiration (90 jours recommandé)
   - **Cochez la case `repo`** (accès complet aux dépôts)
   - Cliquez sur **Generate token**
   - **⚠️ COPIEZ LE TOKEN** (vous ne le reverrez plus !)

2. **Lors du git push** :
   - **Username** : Votre nom d'utilisateur GitHub
   - **Password** : Collez le token (pas votre mot de passe GitHub)

### Option B : GitHub CLI (alternative)

```bash
gh auth login
git push -u origin main
```

## ✅ ÉTAPE 4 : Vérification sur GitHub

Allez sur votre dépôt GitHub. Vous devriez voir :
- ✅ Tous les fichiers Python
- ✅ Tous les fichiers de documentation
- ✅ `.gitignore`
- ✅ `config.py.template`
- ❌ `config.py` (N'apparaît PAS - bien protégé ✅)
- ❌ `progression_transfert.json` (N'apparaît PAS - bien protégé ✅)

## 🐍 ÉTAPE 5 : Installation sur PythonAnywhere

### 5.1 Se connecter en SSH

```bash
ssh votre_username@ssh.pythonanywhere.com
```

Remplacez `votre_username` par votre nom d'utilisateur PythonAnywhere.

### 5.2 Installation automatique

```bash
cd ~
git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
cd TAL-migration
bash INSTALL_PYTHONANYWHERE.sh
```

Quand le script demande votre nom d'utilisateur GitHub, entrez-le.

### 5.3 Configuration

Après l'installation, configurez `config.py` :

```bash
nano config.py
```

Modifiez avec vos identifiants Odoo :
- `URL` : `https://tal-senegal.odoo.com/`
- `DB` : `tal-senegal`
- `USER` : `support@senedoo.com`
- `PASS` : `senedoo@2025`

Sauvegardez : `Ctrl+X` puis `Y` puis `Enter`

### 5.4 Test de connexion

```bash
python3.10 connexion_odoo.py
```

Si ça fonctionne, vous verrez :
```
✅ Connexion réussie!
```

### 5.5 Lancer le transfert

**Test sur 100 factures :**
```bash
python3.10 transferer_factures_documents_v2.py
```

**Transfert complet :**
```bash
python3.10 transferer_factures_documents_v2.py --all
```

## 🔄 ÉTAPE 6 : Mise à jour future

### Sur votre machine locale (après modifications)

```bash
cd TAL-migration
git add -A
git commit -F COMMIT_MESSAGE.txt
git push origin main
```

Ou double-cliquez sur `COMMIT_ET_PUSH.bat`

### Sur PythonAnywhere (pour récupérer les modifications)

```bash
cd ~/TAL-migration
bash update_from_github.sh
```

## 📋 Checklist Complète

### GitHub
- [ ] Dépôt créé sur GitHub
- [ ] URL du dépôt copiée
- [ ] Dépôt local connecté (`git remote add origin ...`)
- [ ] Premier push réussi
- [ ] Vérification : fichiers visibles sur GitHub
- [ ] Vérification : `config.py` n'apparaît PAS ✅

### PythonAnywhere
- [ ] Connexion SSH réussie
- [ ] Dépôt cloné depuis GitHub
- [ ] Script d'installation exécuté
- [ ] `config.py` créé et configuré
- [ ] Test de connexion Odoo réussi
- [ ] Dossier `Factures_pdf_TAL/` créé
- [ ] Test sur 100 factures réussi

## 🆘 Aide

Si vous avez des problèmes, consultez :
- `GUIDE_GITHUB_PYTHONANYWHERE.md` - Guide détaillé
- `DEPLOIEMENT_PYTHONANYWHERE.md` - Guide déploiement
- `DEMARRAGE_RAPIDE.md` - Guide rapide

