# 📋 Commandes de Vérification - PythonAnywhere

## 🔍 Vérifier si le Script Tourne

### Voir les Logs en Temps Réel
```bash
tail -f ~/TAL-migration/transfert.log
```
**Arrêter** : `Ctrl+C`

### Voir les Dernières Lignes
```bash
tail -n 50 ~/TAL-migration/transfert.log
```

### Vérifier la Progression
```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

### Voir les PDFs Générés
```bash
ls -lt ~/TAL-migration/Factures_pdf_TAL/ | head -10
```

### Compter les PDFs
```bash
ls ~/TAL-migration/Factures_pdf_TAL/ | wc -l
```

## ⏸️ Arrêter le Script

### Méthode 1 : pkill
```bash
pkill -f transferer_factures_documents_v2.py
```

### Méthode 2 : pgrep puis kill
```bash
pgrep -f transferer_factures_documents_v2.py
# Notez le PID affiché, puis:
kill PID_NUMBER
```

## 🔄 Relancer

```bash
cd ~/TAL-migration
nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
```

