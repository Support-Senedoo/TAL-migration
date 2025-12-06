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
echo ""
echo "======================================================================"
echo ""

cd "$(dirname "$0")"
python3.10 gestion_transfert.py

echo ""
echo "Appuyez sur Entrée pour continuer..."
read

