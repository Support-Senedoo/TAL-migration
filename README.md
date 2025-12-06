# TAL-migration

Projet de migration TAL - Transfert des factures vers le module Document Odoo

## 🎯 Objectif

Transférer toutes les factures clients vers le module Document d'Odoo v19, avec sélection automatique du modèle PDF et stockage local.

## 🚀 Installation rapide

### Sur PythonAnywhere

```bash
# 1. Cloner le projet
cd ~
git clone https://github.com/Support-Senedoo/TAL-migration.git
cd TAL-migration

# 2. Installer les dépendances
pip3.10 install --user -r requirements.txt

# 3. Configurer config.py
cp config.py.template config.py
# Éditer config.py avec vos identifiants Odoo

# 4. Tester la connexion
python3.10 connexion_odoo.py

# 5. Lancer le transfert
bash START.sh
```

### Localement (Windows)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer config.py
# Copier config.py.template vers config.py et modifier avec vos identifiants

# 3. Tester la connexion
python connexion_odoo.py

# 4. Lancer le transfert
python gestion_transfert.py
```

## 📋 Configuration

Éditer `config.py` avec vos identifiants Odoo :
- `URL` : URL de votre instance Odoo SaaS
- `DB` : Nom de la base de données
- `USER` : Nom d'utilisateur
- `PASS` : Mot de passe

## 🔧 Scripts principaux

### Scripts Python

- **`transferer_factures_documents_v2.py`** : Script principal de transfert
- **`gestion_transfert.py`** : Gestion automatique (vérification, relance, monitoring)
- **`connexion_odoo.py`** : Connexion à Odoo
- **`gestion_progression.py`** : Gestion de la progression (afficher, réinitialiser)
- **`afficher_progression.py`** : Affichage de la progression en temps réel
- **`analyser_arret.py`** : Analyse les logs pour comprendre pourquoi le script s'arrête

### Scripts shell (Linux/PythonAnywhere)

- **`START.sh`** : Lance le transfert avec gestion automatique
- **`RELANCE_SIMPLE.sh`** : Relance rapide du transfert
- **`ARRETER_SCRIPT.sh`** : Arrête le script en cours
- **`update_from_github.sh`** : Met à jour depuis GitHub

### Scripts batch (Windows)

- **`START.bat`** : Lance le transfert sous Windows
- **`COMMIT_ET_PUSH.bat`** : Commit et push Git
- **`PUSH_VERS_GITHUB.bat`** : Push vers GitHub avec authentification

## 📖 Utilisation

### Lancer le transfert complet

```bash
# Sur PythonAnywhere
bash START.sh

# Ou avec relance automatique
python3.10 gestion_transfert.py --watchdog
```

### Voir la progression

```bash
# En temps réel
python3.10 afficher_progression.py

# Ou directement
tail -f transfert_detaille_*.log
```

### Arrêter le script

```bash
bash ARRETER_SCRIPT.sh
```

### Gérer la progression

```bash
# Afficher la progression
python3.10 gestion_progression.py afficher

# Réinitialiser la progression
python3.10 gestion_progression.py reinitialiser
```

## 🔍 Commandes utiles

### Vérifier l'état du script

```bash
python3.10 gestion_transfert.py --status
```

### Mettre à jour depuis GitHub

```bash
bash update_from_github.sh
```

### Analyser un arrêt

```bash
python3.10 analyser_arret.py
```

## 📁 Structure des dossiers

- `Finance/Factures clients/[Nom du client]/` : Dossiers clients dans Odoo Documents
- `Factures_pdf_TAL/` : PDFs stockés localement
- `progression_transfert.json` : État de la progression (ne pas modifier)
- `transfert_detaille_*.log` : Logs détaillés du transfert

## 🔐 Sélection automatique des modèles PDF

Le script sélectionne automatiquement le bon modèle PDF selon le contenu de la facture :
- **"Export EOLIS"** : Si la facture contient "Export de Conteneur"
- **"Factures Livraisons"** : Si la facture contient "Livraison"
- **"Factures Transferts"** : Si la facture contient "Transfert" (défaut)

## ⚠️ Notes importantes

- Le script reprend automatiquement là où il s'est arrêté grâce à `progression_transfert.json`
- Les PDFs sont stockés localement dans `Factures_pdf_TAL/`
- Les logs détaillés sont dans `transfert_detaille_*.log`
- Ne pas modifier `progression_transfert.json` manuellement

## 🐛 Dépannage

### Le script s'arrête

```bash
python3.10 analyser_arret.py
```

### Vérifier la connexion Odoo

```bash
python3.10 connexion_odoo.py
```

### Réinitialiser et recommencer

```bash
python3.10 gestion_progression.py reinitialiser
bash START.sh
```

## 📞 Support

Pour toute question, vérifier les logs dans `transfert_detaille_*.log` ou exécuter `python3.10 analyser_arret.py`.
