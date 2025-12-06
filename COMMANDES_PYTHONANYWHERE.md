# 📝 Commandes PythonAnywhere - Copier/Coller

## 🔐 Connexion SSH

```bash
ssh votre_username@ssh.pythonanywhere.com
```

## 📥 Installation complète (première fois)

```bash
cd ~
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration
bash INSTALL_PYTHONANYWHERE.sh
```

## ⚙️ Configuration

```bash
nano config.py
```

**Contenu à vérifier** :
```python
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',
    'DB': 'tal-senegal',
    'USER': 'support@senedoo.com',
    'PASS': 'senedoo@2025'
}
```

**Sauvegarder** : `Ctrl+X` puis `Y` puis `Enter`

## ✅ Test de connexion

```bash
python3.10 connexion_odoo.py
```

## 🚀 Lancer le transfert

**Test** :
```bash
python3.10 transferer_factures_documents_v2.py
```

**Transfert complet** :
```bash
python3.10 transferer_factures_documents_v2.py
```

## 📊 Voir la progression

```bash
python3.10 gestion_progression.py afficher
```

## 🔄 Mettre à jour depuis GitHub

```bash
cd ~/TAL-migration
bash update_from_github.sh
```

## 📦 Réinstaller les dépendances

```bash
cd ~/TAL-migration
pip3.10 install --user -r requirements.txt
```

## 🗑️ Réinitialiser la progression

```bash
cd ~/TAL-migration
python3.10 gestion_progression.py reinitialiser
```

## 📁 Voir les fichiers

```bash
ls -la ~/TAL-migration
```

## 📄 Voir le contenu de config.py

```bash
cat ~/TAL-migration/config.py
```

## 🔍 Voir les dernières lignes du script en cours

```bash
tail -f ~/TAL-migration/progression_transfert.json
```

