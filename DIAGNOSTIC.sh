#!/bin/bash
# Script de diagnostic pour identifier les problèmes

echo "=========================================="
echo "DIAGNOSTIC - État du projet"
echo "=========================================="
echo ""

cd ~/TAL-migration 2>&1 || { echo "❌ Erreur: Impossible d'accéder à ~/TAL-migration"; exit 1; }

echo "📁 Répertoire actuel: $(pwd)"
echo ""

echo "📋 Fichiers présents:"
ls -la | head -20
echo ""

echo "🔍 Vérification Git:"
git status 2>&1
echo ""

echo "🔍 Vérification config.py:"
if [ -f config.py ]; then
    echo "✅ config.py existe"
    ls -la config.py
else
    echo "❌ config.py n'existe pas"
fi
echo ""

echo "🔍 Fichiers Python présents:"
ls -la *.py 2>&1 | head -10
echo ""

echo "🔍 Scripts shell présents:"
ls -la *.sh 2>&1 | head -10
echo ""

echo "=========================================="
echo "Test de mise à jour:"
echo "=========================================="
echo ""

# Test sans exécuter
echo "Tentative de git pull (simulation)..."
git fetch origin main 2>&1
echo ""
echo "Fichiers distants à mettre à jour:"
git diff HEAD origin/main --name-only 2>&1 | head -10

