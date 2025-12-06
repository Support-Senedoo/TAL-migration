#!/bin/bash
# Script pour diagnostiquer si le script est bloqué

echo "=========================================="
echo "Diagnostic : Script Bloqué ?"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# 1. Vérifier si le processus tourne
echo "1️⃣  Vérification du processus..."
if pgrep -f transferer_factures_documents_v2.py > /dev/null; then
    echo "   ✅ Processus actif"
    PID=$(pgrep -f transferer_factures_documents_v2.py)
    echo "   📋 PID: $PID"
else
    echo "   ❌ Processus arrêté"
    echo ""
    echo "   Le script ne tourne plus. Voir les dernières lignes du log:"
    echo ""
    tail -n 50 transfert_detaille_*.log 2>/dev/null | tail -20
    exit 0
fi

echo ""
echo "2️⃣  Dernière activité dans le log..."
LOG_FILE=$(ls -t transfert_detaille_*.log 2>/dev/null | head -1)
if [ -f "$LOG_FILE" ]; then
    LAST_LINE=$(tail -n 1 "$LOG_FILE")
    LAST_TIME=$(echo "$LAST_LINE" | grep -oP '\[\K[^\]]+' | head -1)
    echo "   📄 Fichier: $LOG_FILE"
    echo "   🕐 Dernière ligne: $LAST_TIME"
    echo ""
    echo "   Dernières lignes:"
    tail -n 10 "$LOG_FILE"
else
    echo "   ⚠️  Aucun fichier log trouvé"
fi

echo ""
echo "3️⃣  Recherche d'erreurs..."
if [ -f "$LOG_FILE" ]; then
    ERRORS=$(tail -n 100 "$LOG_FILE" | grep -i "erreur\|error\|exception\|❌" | tail -5)
    if [ -n "$ERRORS" ]; then
        echo "   ⚠️  Erreurs trouvées:"
        echo "$ERRORS" | sed 's/^/      /'
    else
        echo "   ✅ Aucune erreur récente"
    fi
fi

echo ""
echo "4️⃣  Progression actuelle..."
python3.10 gestion_progression.py afficher | grep -A 5 "traitées"

echo ""
echo "=========================================="
echo ""
echo "💡 Commandes utiles:"
echo "   Voir le log complet: tail -f $LOG_FILE"
echo "   Arrêter le script: bash ARRETER_SCRIPT.sh"
echo "   Relancer: bash LANCER_TRANSFERT_COMPLET.sh"
echo ""

