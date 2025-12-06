#!/bin/bash
# Script qui capture toutes les erreurs dans un fichier

LOG_FILE="erreurs_$(date +%Y%m%d_%H%M%S).log"

echo "📝 Capture des erreurs dans: $LOG_FILE"
echo ""

cd ~/TAL-migration 2>&1 | tee -a "$LOG_FILE"

{
    echo "=========================================="
    echo "DIAGNOSTIC COMPLET"
    echo "Date: $(date)"
    echo "=========================================="
    echo ""
    
    echo "📁 Répertoire: $(pwd)"
    echo ""
    
    echo "📋 État Git:"
    git status 2>&1
    echo ""
    
    echo "📋 Branche:"
    git branch -a 2>&1
    echo ""
    
    echo "📋 Fichiers locaux modifiés:"
    git diff --name-only 2>&1
    echo ""
    
    echo "📋 Fichiers non suivis:"
    git ls-files --others --exclude-standard 2>&1
    echo ""
    
    echo "🔍 Test git pull (simulation):"
    git fetch origin main 2>&1
    echo ""
    
    echo "📋 Fichiers à mettre à jour:"
    git diff --name-only HEAD origin/main 2>&1
    echo ""
    
    echo "🔍 Vérification config.py:"
    if [ -f config.py ]; then
        echo "✅ config.py existe (taille: $(stat -f%z config.py 2>/dev/null || stat -c%s config.py 2>/dev/null))"
        ls -la config.py 2>&1
    else
        echo "❌ config.py n'existe pas"
    fi
    echo ""
    
    echo "🔍 Tentative de mise à jour:"
    if [ -f config.py ]; then
        echo "Sauvegarde config.py..."
        cp config.py config.py.backup.test 2>&1
        rm config.py 2>&1
    fi
    
    echo "Git pull..."
    git pull origin main 2>&1
    PULL_STATUS=$?
    
    echo "Code de retour: $PULL_STATUS"
    echo ""
    
    if [ -f config.py.backup.test ]; then
        echo "Restauration config.py..."
        mv config.py.backup.test config.py 2>&1
    fi
    
    echo ""
    echo "=========================================="
    echo "FIN DU DIAGNOSTIC"
    echo "=========================================="
    
} 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ Diagnostic terminé. Fichier créé: $LOG_FILE"
echo "📋 Affichez le contenu avec: cat $LOG_FILE"
echo ""
echo "💡 Copiez-collez ce fichier pour partager les erreurs"

