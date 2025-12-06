# TAL-migration

Projet de migration TAL - Transfert des factures vers le module Document Odoo

## Description

Ce projet contient les scripts et configurations nécessaires pour transférer toutes les factures clients vers le module Document d'Odoo v19, avec sélection automatique du modèle PDF et stockage local.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### Connexion à Odoo

1. Modifiez le fichier `config.py` avec vos identifiants Odoo :
   - URL de votre instance Odoo SaaS
   - Nom de la base de données
   - Nom d'utilisateur
   - Mot de passe

2. Testez la connexion :
   ```bash
   python connexion_odoo.py
   ```

## Scripts principaux

### Transfert des factures vers le module Document

Le script `transferer_factures_documents_v2.py` transfère **TOUTES** les factures clients vers le module Document d'Odoo.

**Fonctionnalités :**
- ✅ Traitement de toutes les factures (pas de limite)
- ✅ Sélection automatique du modèle PDF selon les lignes de facture
  - "Export de Conteneur" → Export EOLIS
  - "Livraison" → Factures Livraisons
  - "Transfert" → Factures Transferts
- ✅ Stockage local des PDFs dans `Factures_pdf_TAL/`
- ✅ Structure correcte : Finance/Factures clients/[Client]
- ✅ Système de suivi de progression automatique
- ✅ Reprise en cas d'interruption
- ✅ Vérification dans la base de données pour éviter les doublons
- ✅ Sauvegarde automatique après chaque facture transférée
- ✅ Optimisations de performance (session HTTP réutilisable)

**Utilisation :**
```bash
# Test sur 100 factures
python transferer_factures_documents_v2.py

# Transfert complet de toutes les factures
python transferer_factures_documents_v2.py --all
```

**Système de progression :**
- Le script sauvegarde automatiquement la progression dans `progression_transfert.json`
- Chaque facture transférée est enregistrée immédiatement
- Le script peut être relancé à tout moment : il reprendra automatiquement là où il s'est arrêté
- Les factures déjà transférées ne seront pas retraitées

**Gestion de la progression :**
```bash
# Afficher l'état de la progression
python gestion_progression.py afficher

# Réinitialiser la progression (pour tout recommencer)
python gestion_progression.py reinitialiser

# Nettoyer la progression (garde les 1000 dernières factures)
python gestion_progression.py nettoyer
```

## 🚀 Déploiement sur PythonAnywhere

Pour exécuter les scripts depuis PythonAnywhere, consultez le guide complet :
**[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)**

### Installation rapide sur PythonAnywhere

```bash
# 1. Cloner le dépôt
cd ~
git clone https://github.com/VOTRE_USERNAME/TAL-migration.git
cd TAL-migration

# 2. Installer les dépendances
pip3.10 install --user -r requirements.txt

# 3. Configurer
# Modifiez config.py avec vos identifiants Odoo

# 4. Tester
python3.10 connexion_odoo.py
python3.10 transferer_factures_documents_v2.py
```

## 📤 Synchronisation avec GitHub

### Sur votre machine locale

1. **Double-cliquez sur** `COMMIT_ET_PUSH.bat`
   - Ou en ligne de commande :
     ```bash
     git add -A
     git commit -F COMMIT_MESSAGE.txt
     git push origin main
     ```

2. **Mettre à jour depuis GitHub** (sur PythonAnywhere)
   ```bash
   cd ~/TAL-migration
   git pull origin main
   ```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Documentation principale |
| `DEPLOIEMENT_PYTHONANYWHERE.md` | Guide complet de déploiement |
| `DEMARRAGE_RAPIDE.md` | Guide de démarrage rapide |
| `SYNCHRONISATION_GITHUB.md` | Guide de synchronisation GitHub |

## Structure du projet

```
TAL-migration/
├── README.md
├── DEPLOIEMENT_PYTHONANYWHERE.md    # Guide déploiement
├── DEMARRAGE_RAPIDE.md              # Démarrage rapide
├── SYNCHRONISATION_GITHUB.md       # Guide GitHub
├── requirements.txt
├── config.py.template               # Template de configuration
├── config.py                        # Configuration (non commité)
├── connexion_odoo.py                # Connexion à Odoo
├── transferer_factures_documents_v2.py  # Script principal optimisé
├── gestion_progression.py           # Gestion de la progression
├── supprimer_dossiers_clients.py    # Nettoyage dossiers
├── diagnostic_dossiers.py           # Diagnostic structure
├── COMMIT_ET_PUSH.bat               # Sauvegarde GitHub (Windows)
├── COMMIT_MESSAGE.txt               # Message de commit
├── update_from_github.sh            # Mise à jour (Linux/PythonAnywhere)
├── INSTALL_PYTHONANYWHERE.sh        # Installation complète
├── Factures_pdf_TAL/                # PDFs sauvegardés localement (non commité)
├── progression_transfert.json       # Progression (généré, non commité)
└── src/
    └── __init__.py
```

## 🔒 Fichiers non commités (sécurité)

Les fichiers suivants sont dans `.gitignore` et ne seront PAS synchronisés :
- `config.py` (contient les mots de passe)
- `progression_transfert.json` (données locales)
- `Factures_pdf_TAL/` (PDFs locaux)
- `*.pdf` (fichiers PDF)

