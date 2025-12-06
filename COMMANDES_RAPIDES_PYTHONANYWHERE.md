# 🚀 Commandes rapides pour PythonAnywhere

## 📥 Mettre à jour depuis GitHub

### Option 1 : Script automatique complet (recommandé)

```bash
cd ~/TAL-migration
bash MISE_A_JOUR_ET_LANCER.sh
```

Ce script :
- ✅ Sauvegarde config.py
- ✅ Annule les modifications locales
- ✅ Met à jour depuis GitHub
- ✅ Restaure config.py
- ✅ Vérifie les fichiers
- ✅ Vous propose de relancer le script

### Option 2 : Script ultra-simple

```bash
cd ~/TAL-migration
bash MISE_A_JOUR_SIMPLE.sh
```

Script minimal qui fait juste la mise à jour.

### Option 3 : Commandes manuelles

```bash
cd ~/TAL-migration
[ -f config.py ] && cp config.py config.py.backup && rm config.py
git checkout -- .
git clean -fd
git pull origin main
[ -f config.py.backup ] && mv config.py.backup config.py
```

## 🚀 Relancer le script

### Après la mise à jour

```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py
```

### Ou avec le script de relance

```bash
cd ~/TAL-migration
bash RELANCE_SIMPLE.sh
```

## 📊 Voir la progression

```bash
cd ~/TAL-migration
python3.10 afficher_progression.py
```

## 🔍 Vérifier l'état

```bash
cd ~/TAL-migration
git status
ls -la transferer_factures_documents_v2.py
```

## ⚡ Commandes en une ligne

### Mise à jour + Relance

```bash
cd ~/TAL-migration && bash MISE_A_JOUR_SIMPLE.sh && python3.10 gestion_transfert.py
```

### Mise à jour seulement

```bash
cd ~/TAL-migration && bash MISE_A_JOUR_SIMPLE.sh
```

