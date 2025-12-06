# 🔧 Configurer Git pour le compte Support-Senedoo

## Problème

Vous avez 2 comptes GitHub :
- `PatriceWeisz` (compte personnel)
- `Support-Senedoo` (compte professionnel - celui que vous voulez utiliser)

Git utilise actuellement les credentials de `PatriceWeisz`.

## Solution : Configuration locale + Token

### Étape 1 : Configurer le dépôt local pour Support-Senedoo

**Quelle est l'adresse email associée au compte GitHub `Support-Senedoo` ?**

Une fois que vous me donnez l'email, je configurerai :
```bash
git config --local user.name "Support-Senedoo"
git config --local user.email "VOTRE_EMAIL_SUPPORT_SENEDOO"
```

### Étape 2 : Créer un Personal Access Token pour Support-Senedoo

**IMPORTANT** : Vous devez créer le token en étant connecté au compte **Support-Senedoo** sur GitHub.

1. **Connectez-vous** sur GitHub avec le compte **Support-Senedoo**
   - Allez sur https://github.com
   - Déconnectez-vous si nécessaire
   - Connectez-vous avec le compte Support-Senedoo

2. **Créez le token** :
   - Allez sur : https://github.com/settings/tokens
   - Cliquez sur : **"Generate new token"** → **"Generate new token (classic)"**
   - **Note** : `TAL-migration`
   - **Expiration** : 90 jours (ou plus)
   - **Scopes** : **Cochez `repo`** (accès complet aux dépôts)
   - Cliquez sur : **"Generate token"**
   - **⚠️ COPIEZ LE TOKEN** (il commence par `ghp_...`)

### Étape 3 : Utiliser le token

Une fois le token créé, exécutez :
```bash
git push -u origin main
```

Quand Git demande :
- **Username** : `Support-Senedoo`
- **Password** : Collez le **TOKEN** du compte Support-Senedoo

### Étape 4 : Vérification

Après le push réussi, vérifiez sur :
- https://github.com/Support-Senedoo/TAL-migration

Les commits devraient apparaître avec l'auteur "Support-Senedoo".

## Alternative : Utiliser le token dans l'URL

Si vous préférez, vous pouvez mettre le token directement dans l'URL :

```bash
git remote set-url origin https://VOTRE_TOKEN@github.com/Support-Senedoo/TAL-migration.git
git push -u origin main
```

Remplacez `VOTRE_TOKEN` par le token que vous avez créé.

## Gestion de plusieurs comptes GitHub

Pour gérer plusieurs comptes GitHub sur la même machine, vous pouvez :

1. **Utiliser des configurations locales** (ce qu'on fait ici)
   - Chaque dépôt utilise son propre compte

2. **Utiliser Git Credential Manager avec plusieurs comptes**
   - Windows Credential Manager stockera les tokens séparément

3. **Utiliser SSH keys** (plus avancé)
   - Une clé SSH par compte GitHub


