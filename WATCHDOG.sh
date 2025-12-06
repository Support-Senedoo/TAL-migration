#!/bin/bash
# Script Watchdog - Surveille et relance automatiquement

echo "======================================================================"
echo "WATCHDOG MODE - Surveillance Automatique"
echo "======================================================================"
echo ""
echo "Ce script surveille le transfert et le relance automatiquement"
echo "s'il s'arrête ou se bloque."
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter le watchdog"
echo "   (le script de transfert continuera en arrière-plan)"
echo ""
echo "======================================================================"
echo ""

cd ~/TAL-migration || exit 1

# Mode watchdog avec vérification toutes les 60 secondes
python3.10 gestion_transfert.py --watchdog --interval 60

