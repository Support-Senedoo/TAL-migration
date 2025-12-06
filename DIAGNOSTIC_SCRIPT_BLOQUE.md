# 🔍 Diagnostic : Script Bloqué

## 📋 Commandes de Diagnostic

### 1. Vérifier si le script tourne encore

```bash
tail -n 1 ~/TAL-migration/transfert_detaille_*.log
```

Si la dernière ligne est ancienne (il y a plusieurs minutes), le script est peut-être bloqué.

### 2. Voir les dernières lignes du log (erreurs)

```bash
tail -n 50 ~/TAL-migration/transfert_detaille_*.log | tail -50
```

Cherchez des erreurs comme :
- `❌ ERREUR`
- `Exception`
- `Error`
- `Timeout`

### 3. Vérifier la progression actuelle

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

### 4. Voir si le processus tourne encore

```bash
pgrep -f transferer_factures_documents_v2.py
```

Si rien ne s'affiche, le script s'est arrêté.

## ✅ Solutions

### Si le script s'est arrêté

1. **Voir la dernière erreur** :
   ```bash
   tail -n 100 ~/TAL-migration/transfert_detaille_*.log | grep -i "erreur\|error\|exception"
   ```

2. **Relancer** :
   ```bash
   cd ~/TAL-migration
   bash LANCER_TRANSFERT_COMPLET.sh
   ```

Le script reprendra automatiquement là où il s'est arrêté.

### Si le script est bloqué (tourne mais n'avance pas)

1. **Arrêter le script** :
   ```bash
   bash ~/TAL-migration/ARRETER_SCRIPT.sh
   ```

2. **Vérifier les erreurs** :
   ```bash
   tail -n 200 ~/TAL-migration/transfert_detaille_*.log
   ```

3. **Relancer** :
   ```bash
   cd ~/TAL-migration
   bash LANCER_TRANSFERT_COMPLET.sh
   ```

## 🔍 Causes Possibles

1. **Timeout réseau** : Connexion à Odoo interrompue
2. **Erreur de génération PDF** : Certaines factures peuvent causer des problèmes
3. **Problème de mémoire** : Si trop de factures en mémoire
4. **Erreur Odoo** : Problème côté serveur Odoo

