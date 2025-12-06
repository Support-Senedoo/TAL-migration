#!/bin/bash
# Relance rapide du transfert

cd "$(dirname "$0")"

echo "🔄 Relance du transfert..."
echo ""

# Arrêter le script existant s'il tourne
pkill -f transferer_factures_documents_v2.py 2>/dev/null
sleep 2

# Relancer
python3.10 gestion_transfert.py

