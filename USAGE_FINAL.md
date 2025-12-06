# 🚀 Utilisation Finale - Simple et Automatique

## ✅ UN SEUL SCRIPT À RETENIR

### Sur PythonAnywhere

```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py --watchdog
```

**C'est tout !** Le script va :
- ✅ Tester la connexion
- ✅ Lancer le transfert
- ✅ **Surveiller en continu** (vérifie toutes les 60 secondes)
- ✅ **Relancer automatiquement** si le script s'arrête
- ✅ Afficher la progression

### En Arrière-Plan (Recommandé)

```bash
cd ~/TAL-migration
bash LANCER_AVEC_WATCHDOG.sh
```

Ou manuellement :
```bash
cd ~/TAL-migration
nohup python3.10 gestion_transfert.py --watchdog > watchdog.log 2>&1 &
```

## 📊 Suivre la Progression

### Voir les Logs du Transfert
```bash
tail -f transfert_detaille_*.log
```

### Voir les Logs du Watchdog
```bash
tail -f watchdog.log
```

### Voir la Progression
```bash
python3.10 gestion_progression.py afficher
```

## 🛑 Arrêter

### Arrêter le Watchdog (le transfert continuera)
```bash
pkill -f "gestion_transfert.py --watchdog"
```

### Arrêter le Transfert
```bash
pkill -f transferer_factures_documents_v2.py
```

## ✅ Avantages du Mode Watchdog

- **Surveillance automatique** : vérifie toutes les 60 secondes
- **Relance automatique** : si le script s'arrête, il est relancé
- **Détection des blocages** : détecte si le script est bloqué et le relance
- **Pas d'intervention manuelle** : tout est automatique

## 📝 Résumé

**Une seule commande** :
```bash
python3.10 gestion_transfert.py --watchdog
```

Le reste est automatique ! Le script surveille et relance automatiquement.

