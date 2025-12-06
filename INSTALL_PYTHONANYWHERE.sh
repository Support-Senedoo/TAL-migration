#!/bin/bash
# Script d'installation complète sur PythonAnywhere

echo "=========================================="
echo "Installation TAL-migration sur PythonAnywhere"
echo "=========================================="
echo ""

# Créer le dossier
echo "📁 Création du dossier..."
mkdir -p ~/TAL-migration
cd ~/TAL-migration || exit 1

# Cloner depuis GitHub
echo "📥 Clonage depuis GitHub..."
echo "⚠️  Remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub"
read -p "Nom d'utilisateur GitHub: " github_user

if [ -z "$github_user" ]; then
    echo "❌ Nom d'utilisateur requis"
    exit 1
fi

git clone https://github.com/${github_user}/TAL-migration.git .

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du clonage. Vérifiez l'URL du dépôt."
    exit 1
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
echo "   1. Modifiez config.py avec vos identifiants Odoo"
echo "   2. Testez la connexion: python3.10 connexion_odoo.py"
echo "   3. Lancez un test: python3.10 transferer_factures_documents_v2.py"
echo ""

