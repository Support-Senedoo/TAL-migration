# 🚀 Démarrage Simple - TAL-migration

## ✅ Un Seul Script pour Tout Gérer

Plus besoin de vérifier manuellement ! Un seul script fait tout automatiquement.

## 🎯 Sur PythonAnywhere

```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py
```

C'est tout ! Le script va :
- ✅ Tester la connexion Odoo automatiquement
- ✅ Vérifier si le script tourne
- ✅ Vérifier s'il est bloqué
- ✅ Le relancer automatiquement si nécessaire
- ✅ Afficher un résumé complet

## 📝 Sur Windows (Local)

Double-cliquez sur : **`START.bat`**

Ou en ligne de commande :
```bash
python gestion_transfert.py
```

## 📊 Suivre la Progression

```bash
# Voir les logs du gestionnaire
tail -f gestion_transfert.log

# Voir les logs du transfert
tail -f transfert_detaille_*.log

# Voir la progression
python3.10 gestion_progression.py afficher
```

## ✅ Avantages

- **Un seul script** : plus besoin de multiples commandes
- **Tests automatiques** : vérifie tout avant de lancer
- **Relance automatique** : détecte si bloqué et relance
- **Monitoring** : affiche un statut clair
- **Simple** : une seule commande à retenir

## 🔄 Relancer

Si vous voulez relancer à tout moment, exécutez simplement :

```bash
python3.10 gestion_transfert.py
```

Le script détectera automatiquement l'état et agira en conséquence.

## 📋 Ce qui est Fait Automatiquement

1. ✅ Test de connexion Odoo
2. ✅ Vérification si le script tourne
3. ✅ Vérification de l'activité récente (dernières 10 minutes)
4. ✅ Arrêt du script si bloqué
5. ✅ Relance automatique si arrêté
6. ✅ Affichage du statut complet

Plus besoin de vérifier manuellement !

