# 📊 Suivre l'Avancement du Transfert

## 🚀 Commandes Rapides

### 📋 Voir la Progression Sauvegardée

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

Affiche :
- Nombre de factures déjà transférées
- Dernière facture traitée
- Liste des IDs déjà traités

### 📄 Voir les Logs en Temps Réel

```bash
tail -f ~/TAL-migration/transfert.log
```

Affiche les dernières lignes et suit en temps réel. **Arrêter** : `Ctrl+C`

### 📄 Voir les Dernières Lignes des Logs

```bash
tail -n 50 ~/TAL-migration/transfert.log
```

Affiche les 50 dernières lignes du log.

### 📁 Compter les PDFs Générés

```bash
ls ~/TAL-migration/Factures_pdf_TAL/ | wc -l
```

Affiche le nombre total de PDFs générés localement.

### 📁 Voir les Derniers PDFs Générés

```bash
ls -lt ~/TAL-migration/Factures_pdf_TAL/ | head -10
```

Affiche les 10 derniers PDFs créés avec leurs dates.

### 📊 Voir le Résumé Détaillé

```bash
cat ~/TAL-migration/progression_transfert.json | python3.10 -m json.tool
```

Affiche le fichier de progression en format lisible (JSON formaté).

## 📈 Exemple de Suivi Complet

```bash
# 1. Voir la progression
echo "=== PROGRESSION ===" 
python3.10 ~/TAL-migration/gestion_progression.py afficher

# 2. Compter les PDFs
echo ""
echo "=== PDFs GÉNÉRÉS ==="
ls ~/TAL-migration/Factures_pdf_TAL/ | wc -l

# 3. Voir les dernières lignes du log
echo ""
echo "=== DERNIÈRES ACTIVITÉS ==="
tail -n 20 ~/TAL-migration/transfert.log
```

## 🎯 Vérifier si le Script Tourne

### Option 1 : Voir les Logs en Temps Réel
```bash
tail -f ~/TAL-migration/transfert.log
```
Si de nouvelles lignes apparaissent, le script tourne ! ✅

### Option 2 : Vérifier le Dernier PDF Généré
```bash
ls -lt ~/TAL-migration/Factures_pdf_TAL/ | head -1
```
Si le PDF est très récent (il y a quelques secondes/minutes), le script tourne ! ✅

### Option 3 : Vérifier le Fichier de Progression
```bash
stat ~/TAL-migration/progression_transfert.json
```
Regardez la date de "Modify". Si c'est très récent, le script tourne ! ✅

## 📊 Statistiques Détaillées

Pour avoir un résumé complet en une commande :

```bash
cd ~/TAL-migration && \
echo "📊 PROGRESSION" && \
python3.10 gestion_progression.py afficher && \
echo "" && \
echo "📁 PDFs générés: $(ls Factures_pdf_TAL/ | wc -l)" && \
echo "" && \
echo "📄 Dernières lignes du log:" && \
tail -n 5 transfert.log
```

## ⏱️ Estimation du Temps Restant

Le script affiche une estimation dans le résumé. Pour la voir :

```bash
tail -n 30 ~/TAL-migration/transfert.log | grep "Temps estimé"
```

## ✅ Vérification Finale

Après le transfert complet :

```bash
# Voir toutes les factures transférées
python3.10 ~/TAL-migration/gestion_progression.py afficher

# Compter tous les PDFs
ls ~/TAL-migration/Factures_pdf_TAL/ | wc -l

# Voir le résumé final dans les logs
tail -n 50 ~/TAL-migration/transfert.log | grep -A 15 "RÉSUMÉ"
```

## 🔍 Commandes Utiles

### Voir la Taille du Dossier PDFs
```bash
du -sh ~/TAL-migration/Factures_pdf_TAL/
```

### Voir l'Espace Disque Disponible
```bash
df -h ~
```

### Voir les Dernières Factures Traitées (depuis le log)
```bash
grep "Facture" ~/TAL-migration/transfert.log | tail -10
```

## 📝 Notes

- ✅ La progression est sauvegardée automatiquement
- ✅ Le script peut être arrêté et repris à tout moment
- ✅ Les logs sont dans `transfert.log`
- ✅ Les PDFs sont dans `Factures_pdf_TAL/`
- ✅ La progression est dans `progression_transfert.json`

