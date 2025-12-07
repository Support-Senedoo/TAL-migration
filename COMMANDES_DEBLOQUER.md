# 🚀 Commandes pour débloquer la facture

## 📋 Situation actuelle

La facture **FAC/2025/TAL0000272** a été traitée avec succès, mais le script ne passe pas à la suivante.

---

## ✅ Correction appliquée

Le problème était que la progression n'était sauvegardée que toutes les 10 factures. Maintenant, elle est sauvegardée **immédiatement après chaque facture traitée**.

---

## 🔧 Commandes sur PythonAnywhere

### 1. Récupérer la correction

```bash
cd ~/TAL-migration
git pull origin main
```

### 2. Arrêter le script bloqué

```bash
pkill -f transferer_factures_documents_v2.py
sleep 2
```

### 3. Vérifier si la facture est dans la progression

```bash
# Voir si la facture FAC/2025/TAL0000272 est déjà dans la progression
python3.10 -c "
import json
with open('progression_transfert.json', 'r') as f:
    prog = json.load(f)
    print('Factures traitées:', len(prog.get('factures_traitees', [])))
    print('Dernière facture ID:', prog.get('derniere_facture_id', 0))
"
```

### 4. Si la facture n'est pas dans la progression, l'ajouter manuellement

```bash
# Trouver l'ID de la facture
python3.10 passer_facture_bloquee.py FAC/2025/TAL0000272 --raison "Déjà traitée"
```

### 5. Relancer le script

```bash
python3.10 gestion_transfert.py
```

---

## 🔍 Diagnostic complet

### Option 1 : Diagnostiquer la facture

```bash
python3.10 diagnostiquer_facture.py FAC/2025/TAL0000272
```

### Option 2 : Voir les dernières lignes du log

```bash
tail -50 $(ls -t transfert_detaille_*.log | head -1)
```

### Option 3 : Voir la progression actuelle

```bash
python3.10 afficher_progression.py --resume
```

---

## 🎯 Solution rapide (tout en un)

```bash
cd ~/TAL-migration && \
git pull origin main && \
pkill -f transferer_factures_documents_v2.py && \
sleep 2 && \
python3.10 gestion_transfert.py
```

---

## 📊 Vérification après relance

Une fois le script relancé, vérifiez :

```bash
# Suivre la progression en temps réel
python3.10 afficher_progression.py --watch

# Ou voir les logs
tail -f transfert_detaille_*.log
```

---

## ⚠️ Si le problème persiste

Si la facture continue de bloquer, utilisez :

```bash
# Passer la facture et continuer
python3.10 passer_facture_bloquee.py FAC/2025/TAL0000272 --raison "Bloquée après traitement"
```

Puis relancez le script.

