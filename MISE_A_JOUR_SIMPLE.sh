#!/bin/bash
# Script ultra-simple pour mettre à jour depuis GitHub

cd ~/TAL-migration || exit 1

echo "🔄 Mise à jour depuis GitHub..."

# Sauvegarder config.py
[ -f config.py ] && cp config.py config.py.backup && rm config.py

# Mettre à jour
git checkout -- . 2>/dev/null
git clean -fd 2>/dev/null
git fetch origin main
git pull origin main || git reset --hard origin/main

# Restaurer config.py
[ -f config.py.backup ] && mv config.py.backup config.py

echo "✅ Mise à jour terminée!"

