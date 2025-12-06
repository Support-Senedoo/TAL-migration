#!/bin/bash
# Script simple pour mettre à jour le projet

echo "=========================================="
echo "Mise à jour TAL-migration"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# Sauvegarder les modifications locales si nécessaire
if ! git diff --quiet; then
    echo "📦 Sauvegarde des modifications locales..."
    git stash
fi

# Faire le pull
echo "⬇️  Récupération des dernières modifications..."
git pull origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Mise à jour réussie!"
    echo ""
    echo "📝 Prochaines étapes:"
    echo "   - Relancez le script: python3.10 transferer_factures_documents_v2.py"
else
    echo ""
    echo "❌ Erreur lors de la mise à jour"
fi

