# 🔄 Mettre à jour le projet sur PythonAnywhere

## Si le projet n'existe pas encore

```bash
cd ~
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration
pip3.10 install --user -r requirements.txt
cp config.py.template config.py
# Éditer config.py avec vos identifiants Odoo
```

## Si le projet existe déjà

### Option 1 : Script automatique
```bash
cd ~/TAL-migration
bash update_from_github.sh
```

### Option 2 : Manuellement
```bash
cd ~/TAL-migration
git pull origin main
```

## Vérifier que tout est à jour

```bash
cd ~/TAL-migration
ls -la afficher_progression.py
```

Si le fichier existe, vous pouvez l'exécuter :
```bash
python3.10 afficher_progression.py
```

