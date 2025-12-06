#!/bin/bash
# Script simple pour relancer le transfert

echo "🔄 RELANCE DU TRANSFERT"
echo "======================"
echo ""

cd "$(dirname "$0")"

# Arrêter le script s'il tourne déjà
echo "1️⃣  Arrêt du script existant (s'il tourne)..."
bash ARRETER_SCRIPT.sh > /dev/null 2>&1
sleep 2

# Lancer le script de gestion
echo "2️⃣  Lancement du transfert..."
echo ""
python3.10 gestion_transfert.py

