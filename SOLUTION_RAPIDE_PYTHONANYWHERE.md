# ⚡ Solution Rapide - Erreur Installation PythonAnywhere

## 🚨 Problème

Vous avez l'erreur :
```
fatal: destination path '.' already exists and is not an empty directory.
```

## ✅ Solution Immédiate

**Sur PythonAnywhere, exécutez simplement** :

```bash
cd ~/TAL-migration
git pull origin main
pip3.10 install --user -r requirements.txt
```

C'est tout ! Le projet est maintenant à jour.

## 📝 Continuer l'installation

1. **Vérifier config.py** :
   ```bash
   cat config.py
   ```

2. **Tester la connexion** :
   ```bash
   python3.10 connexion_odoo.py
   ```

3. **Lancer le transfert** :
   ```bash
   python3.10 transferer_factures_documents_v2.py
   ```

## 🔄 Si vous voulez tout recommencer

```bash
cd ~
rm -rf TAL-migration
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration
bash INSTALL_PYTHONANYWHERE.sh
```

Le script mis à jour vous proposera automatiquement de mettre à jour si le dossier existe déjà.

