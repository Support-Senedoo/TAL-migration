# 🔄 Mettre à Jour pour Enlever les Warnings

## ⚠️ Le Script en Cours Utilise l'Ancienne Version

Pour enlever les warnings SSL, vous devez :

1. **Arrêter le script** (si en cours) :
   ```bash
   pkill -f transferer_factures_documents_v2.py
   ```

2. **Mettre à jour depuis GitHub** :
   ```bash
   cd ~/TAL-migration
   git pull origin main
   ```

3. **Vérifier que la mise à jour est OK** :
   ```bash
   git log --oneline -1
   ```
   Vous devriez voir : "Désactivation des avertissements SSL InsecureRequestWarning"

4. **Relancer le script** :
   ```bash
   nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
   ```

Le script reprendra automatiquement là où il s'est arrêté, mais **sans les warnings** cette fois ! ✅

## 📝 Note

Les warnings n'empêchent pas le script de fonctionner, mais c'est plus propre sans eux.

