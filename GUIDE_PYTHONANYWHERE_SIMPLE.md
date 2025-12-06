# 🐍 Guide Simple : Installation sur PythonAnywhere

## 📋 Prérequis

- Compte PythonAnywhere (gratuit ou payant)
- Accès SSH activé sur PythonAnywhere
- Dépôt GitHub : https://github.com/Support-Senedoo/TAL-migration

## 🚀 Installation en 5 étapes

### Étape 1 : Se connecter en SSH

Ouvrez votre terminal et connectez-vous :

```bash
ssh votre_username@ssh.pythonanywhere.com
```

Remplacez `votre_username` par votre nom d'utilisateur PythonAnywhere.

### Étape 2 : Installer automatiquement

Une fois connecté, exécutez :

```bash
cd ~
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Support-Senedoo/TAL-migration/main/INSTALL_PYTHONANYWHERE.sh)"
```

**OU** si vous préférez cloner d'abord :

```bash
cd ~
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration
bash INSTALL_PYTHONANYWHERE.sh
```

Le script va :
- ✅ Cloner le dépôt depuis GitHub
- ✅ Installer les dépendances Python
- ✅ Créer le dossier `Factures_pdf_TAL/`
- ✅ Créer un fichier `config.py` de base

### Étape 3 : Configurer config.py

Le script a créé un `config.py` avec les valeurs par défaut. Vérifiez/modifiez-le :

```bash
nano config.py
```

Les valeurs doivent être :
```python
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',
    'DB': 'tal-senegal',
    'USER': 'support@senedoo.com',
    'PASS': 'senedoo@2025'
}
```

**Pour sauvegarder dans nano** : `Ctrl+X` puis `Y` puis `Enter`

### Étape 4 : Tester la connexion

```bash
python3.10 connexion_odoo.py
```

Si vous voyez `✅ Connexion réussie!`, c'est bon ! ✅

### Étape 5 : Lancer le transfert

**Test sur quelques factures** (recommandé d'abord) :
```bash
python3.10 transferer_factures_documents_v2.py
```

**Transfert complet** (toutes les factures) :
```bash
python3.10 transferer_factures_documents_v2.py
```
(Le script reprend automatiquement là où il s'est arrêté grâce à `progression_transfert.json`)

## 🔄 Mettre à jour depuis GitHub

Si vous avez fait des modifications sur votre machine locale et les avez poussées sur GitHub :

```bash
cd ~/TAL-migration
bash update_from_github.sh
```

Ou manuellement :
```bash
cd ~/TAL-migration
git pull origin main
pip3.10 install --user -r requirements.txt
```

## 📊 Suivre la progression

Le script sauvegarde automatiquement sa progression dans `progression_transfert.json`.

**Voir la progression** :
```bash
python3.10 gestion_progression.py afficher
```

**Réinitialiser** (si vous voulez tout recommencer) :
```bash
python3.10 gestion_progression.py reinitialiser
```

## ⏰ Lancer automatiquement (Tâche planifiée)

1. Allez sur le **dashboard PythonAnywhere** : https://www.pythonanywhere.com
2. Cliquez sur **"Tasks"** dans le menu
3. Cliquez sur **"Create a new scheduled task"**
4. Remplissez :
   - **Command** : `cd ~/TAL-migration && python3.10 transferer_factures_documents_v2.py`
   - **Hour** : Choisissez l'heure (ex: 2)
   - **Minute** : Choisissez la minute (ex: 0)
   - **Enabled** : ✅ Cochez
5. Cliquez sur **"Create"**

Le script s'exécutera automatiquement chaque jour à l'heure choisie.

## 📁 Structure des fichiers

```
~/TAL-migration/
├── config.py                    # Configuration Odoo (NE PAS COMMITER)
├── transferer_factures_documents_v2.py  # Script principal
├── progression_transfert.json   # Progression (local uniquement)
├── Factures_pdf_TAL/           # PDFs générés (local uniquement)
├── connexion_odoo.py           # Test de connexion
└── gestion_progression.py      # Gestion de la progression
```

## 🆘 Problèmes courants

### Erreur "Module not found"

```bash
pip3.10 install --user --upgrade requests pandas openpyxl
```

### Erreur de connexion Odoo

1. Vérifiez `config.py` :
   ```bash
   cat config.py
   ```

2. Testez la connexion :
   ```bash
   python3.10 connexion_odoo.py
   ```

### Le script s'arrête

Le script reprend automatiquement là où il s'est arrêté grâce à `progression_transfert.json`.

Pour voir où il en est :
```bash
python3.10 gestion_progression.py afficher
```

### Erreur de permissions

```bash
chmod +x *.py *.sh
chmod 755 Factures_pdf_TAL
```

## ✅ Checklist

- [ ] Connexion SSH réussie
- [ ] Dépôt cloné depuis GitHub
- [ ] Dépendances installées
- [ ] `config.py` configuré correctement
- [ ] Test de connexion Odoo réussi
- [ ] Dossier `Factures_pdf_TAL/` créé
- [ ] Test sur quelques factures réussi
- [ ] Tâche planifiée configurée (optionnel)

## 📞 Commandes utiles

```bash
# Voir les fichiers
ls -la ~/TAL-migration

# Voir la progression
python3.10 gestion_progression.py afficher

# Tester la connexion
python3.10 connexion_odoo.py

# Mettre à jour depuis GitHub
cd ~/TAL-migration && bash update_from_github.sh

# Voir les logs en temps réel
python3.10 transferer_factures_documents_v2.py
```

