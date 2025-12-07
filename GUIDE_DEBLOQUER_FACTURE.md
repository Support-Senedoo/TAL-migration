# 🔧 Guide : Débloquer une facture bloquée

## 🎯 Problème : Facture bloquée sur FAC/2025/TAL0000272

Si le script est bloqué sur une facture spécifique, voici comment la contourner.

---

## 🔍 Étape 1 : Diagnostiquer la facture

Pour comprendre pourquoi la facture bloque :

```bash
cd ~/TAL-migration
python3.10 diagnostiquer_facture.py FAC/2025/TAL0000272
```

Ce script va :
- ✅ Vérifier si la facture existe dans Odoo
- ✅ Tester la connexion au client
- ✅ Vérifier le dossier client
- ✅ Tester la génération du PDF (avec timeout de 60 secondes)
- ✅ Identifier la cause du blocage

---

## ⏭️ Étape 2 : Passer la facture bloquée

Pour marquer la facture comme "à ignorer" et continuer :

```bash
python3.10 passer_facture_bloquee.py FAC/2025/TAL0000272 --raison "Timeout PDF"
```

Cette commande va :
- ✅ Trouver l'ID de la facture
- ✅ L'ajouter à la progression (comme "traité")
- ✅ L'ajouter à la liste des factures ignorées
- ✅ Sauvegarder les modifications

---

## 🔄 Étape 3 : Relancer le script

Après avoir passé la facture bloquée :

```bash
# Arrêter le script bloqué
pkill -f transferer_factures_documents_v2.py

# Attendre 2 secondes
sleep 2

# Relancer
python3.10 gestion_transfert.py
```

Le script va maintenant :
- ✅ Ignorer automatiquement la facture bloquée
- ✅ Continuer avec la facture suivante

---

## 📋 Voir les factures ignorées

Pour lister toutes les factures qui ont été ignorées :

```bash
python3.10 passer_facture_bloquee.py --liste
```

---

## 🛠️ Solutions automatiques

### Solution 1 : Script complet (tout en un)

```bash
# 1. Arrêter le script
pkill -f transferer_factures_documents_v2.py

# 2. Passer la facture bloquée
python3.10 passer_facture_bloquee.py FAC/2025/TAL0000272 --raison "Bloquée"

# 3. Relancer
python3.10 gestion_transfert.py
```

### Solution 2 : Vérifier d'abord, passer ensuite

```bash
# 1. Diagnostiquer
python3.10 diagnostiquer_facture.py FAC/2025/TAL0000272

# 2. Si bloquée, la passer
python3.10 passer_facture_bloquee.py FAC/2025/TAL0000272 --raison "Timeout PDF"

# 3. Relancer
pkill -f transferer_factures_documents_v2.py && sleep 2 && python3.10 gestion_transfert.py
```

---

## ⚠️ Important

- Les factures ignorées sont sauvegardées dans `factures_ignorees.json`
- Elles sont automatiquement sautées par le script principal
- Vous pouvez toujours les traiter manuellement plus tard si nécessaire

---

## 📝 Fichiers créés

- `factures_ignorees.json` : Liste des factures ignorées avec les raisons
- Le script principal vérifie automatiquement cette liste et ignore ces factures

---

## 💡 Astuce

Si plusieurs factures bloquent, vous pouvez les passer en une seule fois :

```bash
for facture in FAC/2025/TAL0000272 FAC/2025/TAL0000273 FAC/2025/TAL0000274; do
    python3.10 passer_facture_bloquee.py "$facture" --raison "Bloquée en série"
done
```

