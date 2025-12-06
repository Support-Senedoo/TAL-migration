# 🔑 Créer un Personal Access Token GitHub

## Étapes détaillées

### 1. Créer le token

1. **Allez sur** : https://github.com/settings/tokens
   - Ou : GitHub → Votre profil (en haut à droite) → **Settings** → **Developer settings** (menu de gauche) → **Personal access tokens** → **Tokens (classic)**

2. **Cliquez sur** : **"Generate new token"** → **"Generate new token (classic)"**

3. **Remplissez** :
   - **Note** : `TAL-migration`
   - **Expiration** : Choisissez (90 jours recommandé)
   - **Scopes** : **Cochez `repo`** (accès complet aux dépôts privés)
   - Les autres cases peuvent rester décochées

4. **Cliquez sur** : **"Generate token"** (en bas de la page)

5. **⚠️ IMPORTANT** : **COPIEZ LE TOKEN** immédiatement (il ressemble à `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - Vous ne pourrez plus le voir après !
   - Sauvegardez-le dans un endroit sûr

### 2. Utiliser le token

**Option A : Lors du push (recommandé)**

Quand vous exécutez `git push`, Git vous demandera :
- **Username** : `Support-Senedoo` (ou votre username GitHub)
- **Password** : Collez le **TOKEN** (pas votre mot de passe GitHub)

**Option B : Dans l'URL (alternative)**

```bash
git remote set-url origin https://VOTRE_TOKEN@github.com/Support-Senedoo/TAL-migration.git
git push -u origin main
```

Remplacez `VOTRE_TOKEN` par le token que vous avez copié.

**Option C : Via Git Credential Manager**

Le token sera demandé automatiquement lors du premier push et sauvegardé.

## Après avoir créé le token

Exécutez simplement :
```bash
git push -u origin main
```

Quand Git demande le mot de passe, collez le **TOKEN** (pas votre mot de passe).


