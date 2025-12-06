# 🔄 Mettre à Jour le Script sur PythonAnywhere

## ⚠️ Avertissements SSL Corrigés

Le script a été mis à jour pour désactiver les avertissements `InsecureRequestWarning`.

## 🔄 Mise à Jour sur PythonAnywhere

Sur PythonAnywhere, exécutez :

```bash
cd ~/TAL-migration
git pull origin main
```

## ✅ Vérification

Après la mise à jour, les avertissements SSL ne devraient plus apparaître dans les logs.

## 🔄 Si le Script est Déjà en Cours

Si le script est déjà en cours d'exécution :

1. **Arrêtez-le** (si nécessaire) :
   ```bash
   ps aux | grep transferer_factures_documents_v2.py
   # Notez le PID et exécutez: kill PID_NUMBER
   ```

2. **Mettez à jour** :
   ```bash
   cd ~/TAL-migration
   git pull origin main
   ```

3. **Relancez** :
   ```bash
   nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
   ```

Le script reprendra automatiquement là où il s'est arrêté grâce à `progression_transfert.json`.

