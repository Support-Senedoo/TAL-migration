# 🔍 Vérifier si le Script Tourne sur PythonAnywhere

## ⚠️ Limitation PythonAnywhere

Sur PythonAnywhere, la commande `ps aux` n'est pas disponible. Utilisez ces alternatives :

## ✅ Méthode 1 : Vérifier les Logs

Si le script tourne, les logs sont mis à jour :

```bash
tail -f ~/TAL-migration/transfert.log
```

Si vous voyez de nouvelles lignes qui apparaissent, le script tourne ! ✅

**Arrêter le suivi** : `Ctrl+C`

## ✅ Méthode 2 : Vérifier le Fichier de Progression

Le script met à jour `progression_transfert.json` régulièrement :

```bash
ls -lh ~/TAL-migration/progression_transfert.json
```

Puis voir le contenu :
```bash
cat ~/TAL-migration/progression_transfert.json
```

Si le fichier est récent (dernière modification il y a quelques minutes), le script tourne probablement.

## ✅ Méthode 3 : Vérifier les PDFs Générés

```bash
ls -lt ~/TAL-migration/Factures_pdf_TAL/ | head -5
```

Si de nouveaux PDFs apparaissent régulièrement, le script tourne ! ✅

## ✅ Méthode 4 : Utiliser pgrep (si disponible)

```bash
pgrep -f transferer_factures_documents_v2.py
```

Si un numéro s'affiche, c'est le PID du processus.

## ⏸️ Arrêter le Script

Si vous devez arrêter le script :

### Option 1 : Si vous voyez le processus avec pgrep

```bash
pgrep -f transferer_factures_documents_v2.py
# Notez le PID affiché
kill PID_NUMBER
```

### Option 2 : Utiliser pkill

```bash
pkill -f transferer_factures_documents_v2.py
```

### Option 3 : Via le Dashboard PythonAnywhere

1. Allez sur https://www.pythonanywhere.com
2. Cliquez sur **"Tasks"**
3. Trouvez la tâche en cours et cliquez sur **"Kill"**

## 🔄 Relancer le Script

Après avoir arrêté, vous pouvez relancer :

```bash
cd ~/TAL-migration
nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
```

Le script reprendra automatiquement là où il s'est arrêté.

