# 📊 Commandes rapides pour voir la progression

## 🖥️ Depuis Cursor (Windows)

### 1. Voir la progression actuelle (une seule fois)
```bash
python afficher_progression.py
```

### 2. Suivre la progression en temps réel (actualisation toutes les 5 secondes)
```bash
python afficher_progression.py --watch
```

### 3. Voir un résumé complet
```bash
python afficher_progression.py --resume
```

---

## 🌐 Sur PythonAnywhere (via SSH)

### 1. Voir la progression actuelle
```bash
cd ~/TAL-migration
python3.10 afficher_progression.py
```

### 2. Suivre en temps réel
```bash
python3.10 afficher_progression.py --watch
```

### 3. Voir le résumé complet
```bash
python3.10 afficher_progression.py --resume
```

### 4. Voir le dernier log en temps réel
```bash
tail -f transfert_detaille_*.log
```

### 5. Voir les 50 dernières lignes du log
```bash
tail -50 $(ls -t transfert_detaille_*.log | head -1)
```

### 6. Voir le fichier de progression JSON (formaté)
```bash
cat progression_transfert.json | python3 -m json.tool
```

---

## 📊 Ce que vous verrez

### Affichage simple
- ✅ Nombre de factures traitées
- 📋 ID de la dernière facture
- 📝 Liste des 5 dernières factures traitées
- 📄 Dernières lignes du log

### Mode watch (--watch)
- Même affichage mais se met à jour automatiquement toutes les 5 secondes
- Parfait pour suivre la progression en continu

### Résumé complet (--resume)
- Toutes les informations
- Liste complète ou résumée des factures traitées
- Statistiques du fichier log

---

## 💡 Astuce

Pour voir la progression en continu sur PythonAnywhere, utilisez :
```bash
python3.10 afficher_progression.py --watch
```

Puis dans un autre terminal SSH, vous pouvez aussi suivre les logs :
```bash
tail -f transfert_detaille_*.log
```

---

## 📝 État actuel

D'après le fichier de progression :
- ✅ **219 factures** déjà traitées
- 📋 Dernière facture ID : **284**

---

## 🔄 Pour mettre à jour sur PythonAnywhere

Une fois que vous avez poussé les modifications sur GitHub, sur PythonAnywhere :

```bash
cd ~/TAL-migration
git pull origin main
python3.10 afficher_progression.py
```

