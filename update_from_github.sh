#!/bin/bash
# Script pour mettre à jour le projet depuis GitHub sur PythonAnywhere

echo "=========================================="
echo "Mise à jour TAL-migration depuis GitHub"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

echo "📥 Récupération des dernières modifications..."
git pull origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Mise à jour réussie!"
    echo ""
    echo "📦 Installation/mise à jour des dépendances..."
    pip3.10 install --user -r requirements.txt
    
    echo ""
    echo "✅ Terminé!"
else
    echo ""
    echo "❌ Erreur lors de la mise à jour"
    exit 1
fi


