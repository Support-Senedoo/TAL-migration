# Commandes exactes à copier-coller

## Relancer le script

```bash
python3.10 gestion_transfert.py
```

## Mettre à jour depuis GitHub

```bash
git pull origin main
```

## Si conflit avec config.py

```bash
cp config.py config.py.backup
git pull origin main
mv config.py.backup config.py
```

## Voir la progression

```bash
python3.10 afficher_progression.py
```

## Débloquer le script (bloqué après FAC/2024/TAL1021652)

```bash
# 1. Vérifier l'état
python3.10 verifier_blocage.py

# 2. Arrêter le script bloqué
pkill -f transferer_factures_documents_v2.py
sleep 2

# 3. Mettre à jour
git pull origin main

# 4. Relancer
python3.10 gestion_transfert.py
```

## Si une facture bloque spécifiquement

```bash
# Diagnostiquer la facture
python3.10 diagnostiquer_facture.py FAC/2024/TAL1021652

# Passer la facture bloquée
python3.10 passer_facture_bloquee.py FAC/2024/TAL1021652 --raison "Bloquée"

# Relancer
python3.10 gestion_transfert.py
```

## Suivre la progression en temps réel

```bash
python3.10 afficher_progression.py --watch
```

## Voir les logs en temps réel

```bash
tail -f transfert_detaille_*.log
```

## Se reconnecter après une déconnexion

```bash
# 1. Se reconnecter
ssh senedoo@ssh.pythonanywhere.com

# 2. Aller dans le dossier
cd ~/TAL-migration

# 3. Vérifier si le script tourne
python3.10 verifier_blocage.py

# 4. Voir la progression
python3.10 afficher_progression.py --resume
```

## Vérifier rapidement si le script tourne

```bash
# Vérifier les processus
ps aux | grep transferer_factures_documents_v2.py

# OU avec pgrep
pgrep -f transferer_factures_documents_v2.py
```

- **Si une ligne s'affiche** : Le script tourne ✅
- **Si rien** : Le script s'est arrêté ❌

## Vérifier que toutes les factures ont été traitées

```bash
cd ~/TAL-migration
python3.10 verifier_toutes_factures.py
```

Ce script affiche :
- ✅ Le nombre total de factures dans Odoo
- ✅ Le nombre de factures traitées (dans la progression)
- ✅ Le nombre de documents créés
- ✅ Les factures restantes à traiter
- ✅ Le pourcentage de progression

