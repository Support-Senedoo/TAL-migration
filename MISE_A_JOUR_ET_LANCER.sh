#!/bin/bash
# Script automatique pour mettre à jour depuis GitHub et relancer le script

echo "🔄 Mise à jour automatique depuis GitHub..."
echo ""

cd ~/TAL-migration || {
    echo "❌ Erreur: Impossible d'accéder au répertoire ~/TAL-migration"
    exit 1
}

# 1. Sauvegarder config.py
echo "💾 Sauvegarde de config.py..."
if [ -f config.py ]; then
    cp config.py config.py.backup
    rm config.py
    echo "✅ config.py sauvegardé et retiré temporairement"
else
    echo "ℹ️ config.py n'existe pas"
fi

# 2. Annuler les modifications locales qui pourraient bloquer
echo ""
echo "🔄 Annulation des modifications locales..."
git checkout -- . 2>/dev/null
echo "✅ Modifications locales annulées"

# 3. Nettoyer les fichiers non suivis qui bloquent
echo ""
echo "🧹 Nettoyage des fichiers non suivis..."
git clean -fd 2>/dev/null
echo "✅ Nettoyage effectué"

# 4. Mettre à jour depuis GitHub
echo ""
echo "📥 Mise à jour depuis GitHub..."
git fetch origin main

# Essayer git pull d'abord
git pull origin main

if [ $? -ne 0 ]; then
    echo "⚠️ git pull a échoué, tentative de reset..."
    git reset --hard origin/main
fi

if [ $? -eq 0 ]; then
    echo "✅ Mise à jour réussie!"
else
    echo "❌ Erreur lors de la mise à jour"
    # Restaurer config.py en cas d'erreur
    if [ -f config.py.backup ]; then
        mv config.py.backup config.py
    fi
    exit 1
fi

# 5. Restaurer config.py
echo ""
if [ -f config.py.backup ]; then
    echo "🔄 Restauration de config.py..."
    mv config.py.backup config.py
    echo "✅ config.py restauré"
fi

# 6. Vérifier que les fichiers sont bien là
echo ""
echo "📋 Vérification des fichiers..."
if [ -f transferer_factures_documents_v2.py ]; then
    echo "✅ transferer_factures_documents_v2.py est présent"
else
    echo "❌ transferer_factures_documents_v2.py n'est pas présent"
fi

if [ -f gestion_transfert.py ]; then
    echo "✅ gestion_transfert.py est présent"
else
    echo "❌ gestion_transfert.py n'est pas présent"
fi

# 7. Demander si on veut relancer le script
echo ""
echo "=================================================================================="
echo "✅ Mise à jour terminée avec succès!"
echo "=================================================================================="
echo ""
echo "Voulez-vous relancer le script maintenant ? (o/N)"
read -t 10 -r REPONSE || REPONSE="n"

if [[ "$REPONSE" =~ ^[oO]$ ]]; then
    echo ""
    echo "🚀 Relance du script..."
    echo ""
    python3.10 gestion_transfert.py
else
    echo ""
    echo "💡 Pour relancer le script plus tard, exécutez :"
    echo "   python3.10 gestion_transfert.py"
    echo ""
    echo "   Ou utilisez :"
    echo "   bash RELANCE_SIMPLE.sh"
fi

