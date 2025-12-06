#!/bin/bash
# Script de démarrage - TAL-migration

cd "$(dirname "$0")"

echo "🚀 Lancement du transfert des factures..."
echo ""

# Lancer avec gestion automatique et mode watchdog
python3.10 gestion_transfert.py --watchdog

