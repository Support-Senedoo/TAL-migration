# 🚀 Lancer le Transfert Complet sur PythonAnywhere

## ✅ Prérequis

- ✅ Connexion Odoo testée et fonctionnelle
- ✅ Dossier `Factures_pdf_TAL/` créé
- ✅ Script `transferer_factures_documents_v2.py` prêt

## 🎯 Lancer le Transfert

### Option 1 : Exécution Simple (Console ouverte)

**⚠️ Important** : Gardez la console SSH ouverte pendant l'exécution.

```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

Le script va :
- ✅ Reprendre automatiquement là où il s'est arrêté (grâce à `progression_transfert.json`)
- ✅ Sauvegarder chaque facture transférée
- ✅ Créer les PDFs localement dans `Factures_pdf_TAL/`
- ✅ Afficher la progression en temps réel

### Option 2 : Exécution en Arrière-plan (Recommandé)

Pour que le script continue même si vous fermez la console :

```bash
cd ~/TAL-migration
nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
```

**Vérifier que ça tourne** :
```bash
ps aux | grep python3.10
```

**Voir les logs en temps réel** :
```bash
tail -f ~/TAL-migration/transfert.log
```

**Arrêter le suivi des logs** : `Ctrl+C`

**Voir les dernières lignes** :
```bash
tail -n 50 ~/TAL-migration/transfert.log
```

### Option 3 : Utiliser screen (Meilleur pour longues exécutions)

**Installer screen** (si pas déjà installé) :
```bash
pip3.10 install --user screen
```

**Créer une session screen** :
```bash
screen -S transfert_tal
```

**Lancer le script** :
```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

**Détacher la session** : `Ctrl+A` puis `D`

**Reconnecter à la session** :
```bash
screen -r transfert_tal
```

**Voir toutes les sessions** :
```bash
screen -ls
```

## 📊 Suivre la Progression

### Voir la progression sauvegardée

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

### Voir les statistiques

```bash
cat ~/TAL-migration/progression_transfert.json | python3.10 -m json.tool
```

### Voir les PDFs générés

```bash
ls -lh ~/TAL-migration/Factures_pdf_TAL/ | wc -l
```

## ⏸️ Arrêter le Script

Si vous devez arrêter le script :

**Si en exécution normale** : `Ctrl+C`

**Si en arrière-plan** :
```bash
ps aux | grep transferer_factures_documents_v2.py
# Notez le PID (premier nombre)
kill PID_NUMBER
```

**Si dans screen** :
- Reconnectez : `screen -r transfert_tal`
- Arrêtez : `Ctrl+C`

## 🔄 Reprendre après Arrêt

Le script reprend **automatiquement** là où il s'est arrêté grâce à `progression_transfert.json`.

**Relancez simplement** :
```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

Le script va :
- ✅ Lire `progression_transfert.json`
- ✅ Ignorer les factures déjà transférées
- ✅ Continuer avec les factures restantes

## 📈 Estimation du Temps

Le temps dépend du nombre de factures :
- **~100 factures** : 10-15 minutes
- **~1000 factures** : 2-3 heures
- **~5000 factures** : 10-15 heures

Le script peut être interrompu et repris à tout moment.

## ✅ Vérification Finale

Après le transfert complet :

1. **Vérifier le nombre de factures transférées** :
   ```bash
   python3.10 ~/TAL-migration/gestion_progression.py afficher
   ```

2. **Vérifier les PDFs locaux** :
   ```bash
   ls -lh ~/TAL-migration/Factures_pdf_TAL/ | wc -l
   ```

3. **Vérifier dans Odoo** :
   - Allez sur https://tal-senegal.odoo.com
   - Module Documents → Finance → Factures clients
   - Vérifiez que les dossiers clients et factures sont présents

## 🆘 Problèmes Courants

### Le script s'arrête

**Cause** : Timeout ou erreur réseau

**Solution** : Relancez simplement, le script reprendra automatiquement.

### Erreur "Module not found"

```bash
pip3.10 install --user -r requirements.txt
```

### Erreur de connexion Odoo

Vérifiez `config.py` :
```bash
cat ~/TAL-migration/config.py
```

### Script trop lent

C'est normal pour un grand nombre de factures. Le script est optimisé mais le transfert prend du temps.

## 📝 Notes Importantes

- ✅ Le script sauvegarde automatiquement la progression
- ✅ Les PDFs sont stockés localement dans `Factures_pdf_TAL/`
- ✅ Le script évite les doublons automatiquement
- ✅ Vous pouvez arrêter et reprendre à tout moment
- ✅ Les logs sont disponibles dans `transfert.log` (si utilisé avec nohup)

