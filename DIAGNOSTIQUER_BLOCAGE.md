# 🔍 Diagnostiquer si le script est bloqué

## 🎯 Problème : "Cela affiche toujours la même facture"

Si l'affichage de progression montre toujours la même facture, cela peut signifier :

1. ✅ **Le script n'a pas progressé** (bloqué)
2. ✅ **Le fichier de progression ne se met pas à jour**
3. ✅ **Le script n'est pas en cours d'exécution**

---

## 🔍 Vérifications à faire

### 1. Vérifier si le script tourne (sur PythonAnywhere)

```bash
# Vérifier les processus Python
ps aux | grep transferer_factures_documents_v2.py

# Ou avec pgrep
pgrep -f transferer_factures_documents_v2.py
```

### 2. Vérifier la date de modification du fichier de progression

```bash
cd ~/TAL-migration
ls -lh progression_transfert.json
stat progression_transfert.json
```

### 3. Vérifier le dernier log

```bash
# Trouver le dernier log
ls -lth transfert_detaille_*.log | head -1

# Voir les 50 dernières lignes
tail -50 $(ls -t transfert_detaille_*.log | head -1)

# Voir la date de dernière modification
stat $(ls -t transfert_detaille_*.log | head -1)
```

### 4. Voir si le log avance en temps réel

```bash
# Suivre le log en temps réel
tail -f transfert_detaille_*.log
```

Si aucune nouvelle ligne n'apparaît après quelques minutes, le script est probablement bloqué.

---

## 🛠️ Solutions

### Solution 1 : Script amélioré d'affichage

Le script `afficher_progression.py` a été amélioré pour :

- ✅ Afficher la date de dernière modification du fichier
- ✅ Indiquer si le fichier est récent ou ancien
- ✅ Détecter si la progression a changé
- ✅ Afficher quand le log a été modifié pour la dernière fois

**Utilisation :**
```bash
python afficher_progression.py --watch
```

### Solution 2 : Vérifier directement sur PythonAnywhere

```bash
cd ~/TAL-migration

# Voir le statut
python3.10 afficher_progression.py

# Voir la progression en temps réel
python3.10 afficher_progression.py --watch
```

### Solution 3 : Redémarrer le script si bloqué

Si le script est bloqué :

```bash
# Arrêter le script
pkill -f transferer_factures_documents_v2.py

# Attendre 2 secondes
sleep 2

# Relancer
python3.10 gestion_transfert.py
```

---

## 📊 Indicateurs que le script est actif

### ✅ Script actif (tout va bien)
- Le fichier `progression_transfert.json` est modifié récemment (< 5 minutes)
- Le fichier log est mis à jour régulièrement
- Les dernières lignes du log montrent de nouvelles factures

### ⚠️ Script bloqué (problème)
- Le fichier `progression_transfert.json` n'a pas été modifié depuis plus de 10 minutes
- Le fichier log n'a pas été modifié depuis plus de 10 minutes
- Les dernières lignes du log sont anciennes

### ❌ Script arrêté
- Aucun processus `transferer_factures_documents_v2.py` en cours
- Le fichier log n'a pas été modifié depuis très longtemps

---

## 🎯 Utilisation du script amélioré

Le script amélioré `afficher_progression.py` affiche maintenant :

```
================================================================================
📊 PROGRESSION DU TRANSFERT DES FACTURES
================================================================================

✅ Factures traitées     : 219
📋 Dernière facture ID   : 284
📅 Dernière mise à jour : 2024-12-01 15:30:45 (🟡 RÉCENT (3 min))

📝 5 dernières factures traitées:
--------------------------------------------------------------------------------
   • Facture ID: 280
   • Facture ID: 281
   • Facture ID: 282
   • Facture ID: 283
   • Facture ID: 284
--------------------------------------------------------------------------------

📄 Dernier fichier log: transfert_detaille_20241201_143022.log
📅 Log modifié il y a: 3.5 minutes
✅ Le script semble actif
```

**Codes couleur :**
- 🟢 TRÈS RÉCENT (< 1 min) : Le script vient de progresser
- 🟡 RÉCENT (X min) : Le script a progressé récemment
- 🟠 ANCIEN (X min) : Attention, le script pourrait être ralenti
- 🔴 TRÈS ANCIEN (X h) : Le script est probablement bloqué ou arrêté

---

## 💡 Commandes rapides

### Voir la progression avec détection de blocage
```bash
python afficher_progression.py --watch
```

### Vérifier manuellement si le script tourne
```bash
ps aux | grep transferer_factures_documents_v2.py
```

### Voir les dernières lignes du log
```bash
tail -50 transfert_detaille_*.log
```

### Voir si le log avance
```bash
tail -f transfert_detaille_*.log
```

