# 🔧 Résolution Conflit lors du Pull

## ⚠️ Problème

Git ne peut pas mettre à jour car le fichier `transferer_factures_documents_v2.py` a été modifié localement.

## ✅ Solution 1 : Sauvegarder et Appliquer (Recommandé)

```bash
cd ~/TAL-migration

# 1. Sauvegarder les modifications locales
git stash

# 2. Faire le pull
git pull origin main

# 3. Voir ce qui a été sauvegardé
git stash list

# 4. Si besoin, réappliquer les modifications (optionnel)
# git stash pop
```

## ✅ Solution 2 : Écraser avec la Version Distante

**⚠️ ATTENTION** : Cette solution supprime vos modifications locales !

Si vous êtes sûr que les modifications locales ne sont pas importantes :

```bash
cd ~/TAL-migration

# Sauvegarder le fichier actuel (au cas où)
cp transferer_factures_documents_v2.py transferer_factures_documents_v2.py.backup

# Écraser avec la version distante
git checkout -- transferer_factures_documents_v2.py

# Faire le pull
git pull origin main
```

## ✅ Solution 3 : Voir d'abord les Différences

Pour voir ce qui diffère :

```bash
cd ~/TAL-migration

# Voir les différences
git diff transferer_factures_documents_v2.py
```

Ensuite, décidez si vous voulez garder vos modifications locales ou utiliser la version distante.

## 🎯 Recommandation

Utilisez **Solution 1** (stash), car :
- ✅ Sauvegarde vos modifications
- ✅ Permet de les réappliquer si nécessaire
- ✅ Plus sûr

Après le pull, vous pourrez voir si vos modifications locales sont importantes ou si la version distante est meilleure.

