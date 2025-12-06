#!/bin/bash
# Script pour arrêter, réinitialiser et relancer le transfert complet avec logging détaillé

echo "=========================================="
echo "Lancement Transfert Complet avec Logging Détaillé"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# 1. Arrêter le script en cours
echo "1️⃣  Arrêt du script en cours..."
pkill -f transferer_factures_documents_v2.py
sleep 2

# 2. Réinitialiser la progression
echo "2️⃣  Réinitialisation de la progression..."
python3.10 gestion_progression.py reinitialiser

# 3. Créer un fichier log avec timestamp
LOG_FILE="transfert_detaille_$(date +%Y%m%d_%H%M%S).log"
echo "3️⃣  Fichier log: $LOG_FILE"

# 4. Lancer le script avec logging complet
echo "4️⃣  Lancement du transfert complet..."
echo ""
echo "Le script va tout traiter et logger chaque action dans: $LOG_FILE"
echo "Vous pouvez suivre en temps réel avec: tail -f $LOG_FILE"
echo ""

nohup python3.10 transferer_factures_documents_v2.py > "$LOG_FILE" 2>&1 &

echo "✅ Script lancé en arrière-plan"
echo ""
echo "📋 Commandes utiles:"
echo "   Suivre les logs: tail -f $LOG_FILE"
echo "   Voir la progression: python3.10 gestion_progression.py afficher"
echo "   Arrêter: bash ARRETER_SCRIPT.sh"
echo ""

