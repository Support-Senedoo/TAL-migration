#!/bin/bash
# Script pour réinitialiser la progression et relancer tout

echo "=========================================="
echo "Réinitialisation complète du transfert"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# 1. Arrêter le script en cours
echo "1️⃣  Arrêt du script en cours..."
pkill -f transferer_factures_documents_v2.py
sleep 2

# 2. Sauvegarder l'ancienne progression
if [ -f progression_transfert.json ]; then
    echo "2️⃣  Sauvegarde de l'ancienne progression..."
    cp progression_transfert.json progression_transfert_backup_$(date +%Y%m%d_%H%M%S).json
    echo "✅ Sauvegardé dans: progression_transfert_backup_$(date +%Y%m%d_%H%M%S).json"
fi

# 3. Réinitialiser la progression
echo "3️⃣  Réinitialisation de la progression..."
python3.10 gestion_progression.py reinitialiser

echo ""
echo "=========================================="
echo "✅ Réinitialisation terminée!"
echo "=========================================="
echo ""
echo "📝 Prochaines étapes:"
echo "   Pour relancer: bash LANCER_TRANSFERT_COMPLET.sh"
echo "   Ou manuellement: python3.10 transferer_factures_documents_v2.py"
echo ""

