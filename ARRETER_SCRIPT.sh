#!/bin/bash
# Script pour arrêter le script de transfert en cours

echo "=========================================="
echo "Arrêt du script de transfert"
echo "=========================================="
echo ""

# Arrêter le processus
pkill -f transferer_factures_documents_v2.py

if [ $? -eq 0 ]; then
    echo "✅ Script arrêté avec succès"
else
    echo "ℹ️  Aucun script en cours d'exécution trouvé"
fi

# Vérifier qu'il n'y a plus de processus
sleep 1
if pgrep -f transferer_factures_documents_v2.py > /dev/null; then
    echo "⚠️  Le script est toujours en cours..."
    echo "Tentative de force kill..."
    pkill -9 -f transferer_factures_documents_v2.py
else
    echo "✅ Confirmation: Aucun processus trouvé"
fi

echo ""
echo "Terminé!"



