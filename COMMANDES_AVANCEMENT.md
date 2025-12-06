# 📋 Commandes Suivi Avancement - Copier/Coller

## 📊 Voir la Progression

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

## 📄 Voir les Logs en Temps Réel

```bash
tail -f ~/TAL-migration/transfert.log
```
**Arrêter** : `Ctrl+C`

## 📄 Voir les Dernières Lignes

```bash
tail -n 50 ~/TAL-migration/transfert.log
```

## 📁 Compter les PDFs

```bash
ls ~/TAL-migration/Factures_pdf_TAL/ | wc -l
```

## 📁 Voir les Derniers PDFs

```bash
ls -lt ~/TAL-migration/Factures_pdf_TAL/ | head -10
```

## 🔍 Résumé Complet (une commande)

```bash
cd ~/TAL-migration && echo "📊 PROGRESSION" && python3.10 gestion_progression.py afficher && echo "" && echo "📁 PDFs: $(ls Factures_pdf_TAL/ | wc -l)" && echo "" && echo "📄 LOGS:" && tail -n 5 transfert.log
```

## ✅ Vérifier si ça Tourne

```bash
tail -n 1 ~/TAL-migration/transfert.log
```
Si la ligne est récente, ça tourne ! ✅

