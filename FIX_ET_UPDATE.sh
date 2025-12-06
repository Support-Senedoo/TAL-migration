#!/bin/bash
# Script unique pour réparer et mettre à jour automatiquement

cd ~/TAL-migration || exit 1

echo "🔧 Réparation et mise à jour automatique..."
echo ""

# Sauvegarder config.py si existe
[ -f config.py ] && cp config.py config.py.backup && rm config.py && echo "✅ config.py sauvegardé"

# Mettre à jour
echo "📥 Mise à jour depuis GitHub..."
git pull origin main

# Restaurer config.py
[ -f config.py.backup ] && mv config.py.backup config.py && echo "✅ config.py restauré"

# Installer dépendances
echo "📦 Installation des dépendances..."
pip3.10 install --user -r requirements.txt

echo ""
echo "✅ Terminé ! Vous pouvez maintenant utiliser :"
echo "   python3.10 afficher_progression.py"
echo "   ou"
echo "   bash START.sh"

