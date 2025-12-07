# 🚀 Solution rapide : Débloquer après FAC/2024/TAL1021652

## 📊 Situation

- ✅ **320 factures traitées** sur 1856
- ⚠️ **Script bloqué** après FAC/2024/TAL1021652

---

## ⚡ Solution rapide (copier-coller)

```bash
cd ~/TAL-migration && \
pkill -f transferer_factures_documents_v2.py && \
sleep 2 && \
git pull origin main && \
python3.10 gestion_transfert.py
```

---

## 🔍 Ou diagnostic complet

### Étape 1 : Vérifier l'état
```bash
python3.10 verifier_blocage.py
```

### Étape 2 : Voir la progression
```bash
python3.10 afficher_progression.py --resume
```

### Étape 3 : Diagnostiquer la facture bloquée
```bash
python3.10 diagnostiquer_facture.py FAC/2024/TAL1021652
```

### Étape 4 : Arrêter et relancer
```bash
pkill -f transferer_factures_documents_v2.py
sleep 2
git pull origin main
python3.10 gestion_transfert.py
```

---

## ⏭️ Si la facture bloque toujours

```bash
# Passer la facture bloquée
python3.10 passer_facture_bloquee.py FAC/2024/TAL1021652 --raison "Timeout PDF"

# Relancer
python3.10 gestion_transfert.py
```

---

## 📋 Suivre la progression

```bash
# En temps réel
python3.10 afficher_progression.py --watch

# Ou les logs
tail -f transfert_detaille_*.log
```

---

## 💡 Améliorations apportées

- ✅ Timeout PDF augmenté à 60 secondes (au lieu de 30)
- ✅ Outil de diagnostic (`verifier_blocage.py`)
- ✅ Sauvegarde immédiate de la progression après chaque facture
- ✅ Script pour passer les factures bloquées

Le script devrait maintenant mieux gérer les blocages et continuer automatiquement.

