#!/bin/bash
# Script de démarrage simple - TAL-migration

echo "======================================================================"
echo "GESTION AUTOMATIQUE DU TRANSFERT DES FACTURES"
echo "======================================================================"
echo ""
echo "Ce script va :"
echo "  - Vérifier l'état du transfert"
echo "  - Tester la connexion Odoo"
echo "  - Lancer/relancer le transfert automatiquement"
echo "  - Surveiller et relancer si le script s'arrête (mode watchdog)"
echo ""
echo "======================================================================"
echo ""

cd "$(dirname "$0")"

# Mode watchdog par défaut - surveille et relance automatiquement
python3.10 gestion_transfert.py --watchdog

