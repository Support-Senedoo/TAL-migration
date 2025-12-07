# 🔧 Débloquer le script après FAC/2024/TAL1021652

## 📊 Situation actuelle

- ✅ **320 factures traitées** sur 1856
- ⚠️ **Script bloqué** après FAC/2024/TAL1021652

---

## 🔍 Étape 1 : Vérifier l'état actuel

### Sur PythonAnywhere :

```bash
cd ~/TAL-migration

# Vérifier si le script tourne
ps aux | grep transferer_factures_documents_v2.py

# Voir la progression actuelle
python3.10 afficher_progression.py --resume

# Voir les dernières lignes du log
tail -50 $(ls -t transfert_detaille_*.log | head -1)
```

---

## 🔍 Étape 2 : Diagnostiquer le blocage

```bash
# Diagnostiquer la facture qui bloque
python3.10 diagnostiquer_facture.py FAC/2024/TAL1021652

# Vérifier l'état général
python3.10 verifier_blocage.py
```

---

## ⏭️ Étape 3 : Passer la facture bloquée

Si la facture bloque, vous pouvez la passer et continuer :

```bash
# Passer la facture bloquée
python3.10 passer_facture_bloquee.py FAC/2024/TAL1021652 --raison "Bloquée après traitement"

# OU si c'est la facture SUIVANTE qui bloque, trouver son numéro d'abord
```

---

## 🛑 Étape 4 : Arrêter et relancer

```bash
# Arrêter le script bloqué
pkill -f transferer_factures_documents_v2.py

# Attendre 2 secondes
sleep 2

# Récupérer les dernières modifications
git pull origin main

# Relancer
python3.10 gestion_transfert.py
```

---

## 🚀 Solution rapide (tout en un)

```bash
cd ~/TAL-migration && \
pkill -f transferer_factures_documents_v2.py && \
sleep 2 && \
git pull origin main && \
python3.10 gestion_transfert.py
```

---

## 📋 Commandes utiles

### Voir la progression en temps réel
```bash
python3.10 afficher_progression.py --watch
```

### Suivre les logs en temps réel
```bash
tail -f transfert_detaille_*.log
```

### Voir combien de factures restent
```bash
python3.10 -c "
import json
with open('progression_transfert.json', 'r') as f:
    prog = json.load(f)
    nb_traitees = len(prog.get('factures_traitees', []))
    print(f'Factures traitées: {nb_traitees}')
    print(f'Restantes (approx): {1856 - nb_traitees}')
"
```

---

## 💡 Si le problème persiste

Si la même facture continue de bloquer après plusieurs tentatives :

1. **Diagnostiquer** : `python3.10 diagnostiquer_facture.py FAC/2024/TAL1021652`
2. **La passer** : `python3.10 passer_facture_bloquee.py FAC/2024/TAL1021652 --raison "Timeout PDF"`
3. **Relancer** : `python3.10 gestion_transfert.py`

Le script continuera avec la facture suivante.

