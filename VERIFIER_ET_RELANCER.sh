#!/bin/bash
# Script pour vérifier le mode et relancer si nécessaire

echo "=========================================="
echo "Vérification du Mode du Script"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# Vérifier si le script tourne
echo "1️⃣  Vérification du script en cours..."
if pgrep -f transferer_factures_documents_v2.py > /dev/null; then
    echo "   ✅ Script en cours d'exécution"
    echo ""
    echo "   📋 Dernières lignes du log:"
    tail -n 5 transfert.log 2>/dev/null || tail -n 5 transfert_detaille_*.log 2>/dev/null | tail -n 5
    
    echo ""
    echo "   🔍 Recherche du mode..."
    if tail -n 50 transfert.log 2>/dev/null | grep -i "MODE TEST" > /dev/null; then
        echo "   ⚠️  MODE TEST DÉTECTÉ (100 factures seulement)"
        echo ""
        read -p "   Voulez-vous arrêter et relancer en mode complet ? (o/N): " reponse
        if [ "$reponse" = "o" ] || [ "$reponse" = "O" ]; then
            echo ""
            echo "2️⃣  Arrêt du script..."
            pkill -f transferer_factures_documents_v2.py
            sleep 2
            
            echo ""
            echo "3️⃣  Mise à jour..."
            bash UPDATE.sh
            
            echo ""
            echo "4️⃣  Relance en mode complet..."
            bash LANCER_TRANSFERT_COMPLET.sh
        else
            echo "   ✅ Script laissé en cours d'exécution"
        fi
    elif tail -n 50 transfert.log 2>/dev/null | grep -i "MODE COMPLET" > /dev/null; then
        echo "   ✅ MODE COMPLET DÉTECTÉ (toutes les factures)"
    else
        echo "   ℹ️  Mode non déterminé, vérifiez manuellement"
    fi
else
    echo "   ℹ️  Aucun script en cours d'exécution"
    echo ""
    echo "   Pour lancer le transfert complet:"
    echo "   bash LANCER_TRANSFERT_COMPLET.sh"
fi

echo ""
echo "=========================================="

