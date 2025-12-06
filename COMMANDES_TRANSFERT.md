# 📋 Commandes Transfert - Copier/Coller

## 🚀 Lancer le Transfert (Simple)

```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

## 🚀 Lancer en Arrière-plan (Recommandé)

```bash
cd ~/TAL-migration
nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
```

## 📊 Voir les Logs

```bash
tail -f ~/TAL-migration/transfert.log
```

**Arrêter** : `Ctrl+C`

## 📊 Voir la Progression

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

## 🔍 Vérifier que ça Tourne

```bash
ps aux | grep transferer_factures_documents_v2.py
```

## ⏸️ Arrêter le Script

```bash
ps aux | grep transferer_factures_documents_v2.py
# Notez le PID (premier nombre de la ligne)
kill PID_NUMBER
```

## 🔄 Reprendre après Arrêt

```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_v2.py
```

## 📁 Voir les PDFs Générés

```bash
ls -lh ~/TAL-migration/Factures_pdf_TAL/ | wc -l
```

## 📄 Voir les Dernières Lignes du Log

```bash
tail -n 50 ~/TAL-migration/transfert.log
```

