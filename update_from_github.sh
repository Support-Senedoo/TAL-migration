#!/bin/bash
# Script pour mettre à jour le projet depuis GitHub sur PythonAnywhere

echo "=========================================="
echo "Mise à jour TAL-migration depuis GitHub"
echo "=========================================="
echo ""

cd ~/TAL-migration || exit 1

# Sauvegarder config.py s'il existe
if [ -f config.py ]; then
    echo "💾 Sauvegarde de config.py..."
    cp config.py config.py.backup
    rm config.py
fi

echo "📥 Récupération des dernières modifications..."
git pull origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Mise à jour réussie!"
    
    # Restaurer config.py si sauvegardé
    if [ -f config.py.backup ]; then
        echo "🔄 Restauration de config.py..."
        mv config.py.backup config.py
    fi
    
    echo ""
    echo "📦 Installation/mise à jour des dépendances..."
    pip3.10 install --user -r requirements.txt
    
    echo ""
    echo "✅ Terminé!"
else
    # Restaurer config.py en cas d'erreur
    if [ -f config.py.backup ]; then
        mv config.py.backup config.py
    fi
    echo ""
    echo "❌ Erreur lors de la mise à jour"
    exit 1
fi




