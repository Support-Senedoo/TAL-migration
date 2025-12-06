#!/bin/bash
# Script d'installation complète sur PythonAnywhere

echo "=========================================="
echo "Installation TAL-migration sur PythonAnywhere"
echo "=========================================="
echo ""

# Vérifier si le dossier existe déjà
if [ -d ~/TAL-migration ]; then
    echo "⚠️  Le dossier ~/TAL-migration existe déjà."
    echo ""
    echo "Options:"
    echo "1. Mettre à jour depuis GitHub (recommandé si déjà installé)"
    echo "2. Supprimer et réinstaller"
    echo "3. Annuler"
    echo ""
    read -p "Votre choix (1/2/3): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔄 Mise à jour depuis GitHub..."
            cd ~/TAL-migration || exit 1
            if [ -d .git ]; then
                git pull origin main
                if [ $? -eq 0 ]; then
                    echo "✅ Mise à jour terminée!"
                else
                    echo "❌ Erreur lors de la mise à jour."
                    exit 1
                fi
            else
                echo "❌ Ce n'est pas un dépôt Git. Supprimez le dossier et réessayez."
                exit 1
            fi
            ;;
        2)
            echo ""
            echo "🗑️  Suppression du dossier existant..."
            rm -rf ~/TAL-migration
            echo "✅ Dossier supprimé."
            ;;
        3)
            echo "❌ Installation annulée."
            exit 0
            ;;
        *)
            echo "❌ Choix invalide."
            exit 1
            ;;
    esac
fi

# Si le dossier n'existe pas ou a été supprimé, cloner
if [ ! -d ~/TAL-migration ]; then
    echo ""
    echo "📁 Création du dossier..."
    mkdir -p ~/TAL-migration
    cd ~/TAL-migration || exit 1
    
    # Cloner depuis GitHub
    echo "📥 Clonage depuis GitHub (Support-Senedoo)..."
    github_user="Support-Senedoo"
    git clone https://github.com/${github_user}/TAL-migration.git .
    
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors du clonage. Vérifiez l'URL du dépôt."
        exit 1
    fi
else
    cd ~/TAL-migration || exit 1
fi

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
pip3.10 install --user -r requirements.txt

# Créer les dossiers nécessaires
echo ""
echo "📁 Création des dossiers..."
mkdir -p Factures_pdf_TAL

# Créer config.py si n'existe pas
if [ ! -f config.py ]; then
    echo ""
    echo "⚙️  Création du fichier config.py..."
    cat > config.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION POUR TAL-migration
=================================

Fichier de configuration centralisé pour le projet TAL-migration.
Modifiez les valeurs ci-dessous selon votre environnement.
"""

# Configuration Odoo SaaS
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',  # URL de votre instance Odoo SaaS (PRODUCTION)
    'DB': 'tal-senegal',                      # Nom de la base de données (PRODUCTION)
    'USER': 'support@senedoo.com',             # Nom d'utilisateur
    'PASS': 'senedoo@2025'                      # Mot de passe
}

# Paramètres par défaut
DEFAULT_PARAMS = {
    'BATCH_SIZE': 100,          # Taille des lots pour les opérations en batch
    'TIMEOUT': 300,             # Timeout en secondes pour les opérations longues
    'RETRY_ATTEMPTS': 3,        # Nombre de tentatives en cas d'échec
    'RETRY_DELAY': 5,           # Délai entre les tentatives (secondes)
}

# Pour permettre l'importation
__all__ = ['ODOO_CONFIG', 'DEFAULT_PARAMS']
EOF
    echo "✅ Fichier config.py créé. ⚠️  Modifiez-le avec vos identifiants!"
else
    echo "ℹ️  Le fichier config.py existe déjà. Vérifiez qu'il contient les bons identifiants."
fi

# Rendre les scripts exécutables
echo ""
echo "🔧 Configuration des permissions..."
chmod +x *.py *.sh 2>/dev/null

echo ""
echo "=========================================="
echo "✅ Installation terminée!"
echo "=========================================="
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Modifiez config.py avec vos identifiants Odoo (si nécessaire)"
echo "   2. Testez la connexion: python3.10 connexion_odoo.py"
echo "   3. Lancez un test: python3.10 transferer_factures_documents_v2.py"
echo ""
