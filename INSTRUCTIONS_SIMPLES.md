# 🚀 Instructions Simples - Push vers GitHub

## ✅ Étape 1 : Créer le Token (5 minutes)

1. **Connectez-vous** sur GitHub avec le compte **Support-Senedoo**
   - https://github.com

2. **Allez sur** : https://github.com/settings/tokens

3. **Cliquez sur** : "Generate new token" → "Generate new token (classic)"

4. **Remplissez** :
   - Note : `TAL-migration`
   - Expiration : 90 jours
   - **Cochez `repo`** ✅
   - Cliquez "Generate token"

5. **COPIEZ LE TOKEN** (il commence par `ghp_...`)
   - ⚠️ Vous ne le reverrez plus !
   - Sauvegardez-le quelque part

## ✅ Étape 2 : Pousser vers GitHub

### Option A : Utiliser le script automatique (Recommandé)

**Double-cliquez sur** : `PUSH_VERS_GITHUB.bat`

Le script va :
- Configurer le dépôt pour Support-Senedoo
- Lancer le push
- Vous demander le token quand nécessaire

### Option B : Commandes manuelles

Ouvrez PowerShell dans le dossier `TAL-migration` et exécutez :

```powershell
# Configurer pour Support-Senedoo
git config --local user.name "Support-Senedoo"

# Pousser vers GitHub
git push -u origin main
```

**Quand Git demande** :
- **Username** : `Support-Senedoo`
- **Password** : Collez votre **TOKEN** (pas votre mot de passe)

## ✅ Étape 3 : Vérifier

Allez sur : https://github.com/Support-Senedoo/TAL-migration

Vous devriez voir tous vos fichiers ! ✅

## ❌ Si ça ne marche pas

1. **Vérifiez que vous êtes connecté au bon compte GitHub**
   - Le token doit être créé avec le compte Support-Senedoo

2. **Vérifiez que le token a la permission `repo`**
   - Recréez un token si nécessaire

3. **Vérifiez l'URL du remote** :
   ```bash
   git remote -v
   ```
   Doit afficher : `https://github.com/Support-Senedoo/TAL-migration.git`

4. **Essayez de mettre le token dans l'URL** :
   ```bash
   git remote set-url origin https://VOTRE_TOKEN@github.com/Support-Senedoo/TAL-migration.git
   git push -u origin main
   ```


