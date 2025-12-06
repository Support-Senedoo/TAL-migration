#!/bin/bash
# Script pour lancer avec surveillance automatique (watchdog)

echo "======================================================================"
echo "Lancement avec Watchdog - Surveillance Automatique"
echo "======================================================================"
echo ""
echo "Ce script va :"
echo "  1. Vérifier l'état et lancer le transfert"
echo "  2. Surveiller en continu (vérification toutes les 60 secondes)"
echo "  3. Relancer automatiquement si le script s'arrête"
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter le watchdog"
echo "   (le script de transfert continuera en arrière-plan)"
echo ""
echo "======================================================================"
echo ""

cd ~/TAL-migration || exit 1

# Lancer en mode watchdog (surveille et relance automatiquement)
nohup python3.10 gestion_transfert.py --watchdog --interval 60 > watchdog.log 2>&1 &

WATCHDOG_PID=$!

echo "✅ Watchdog lancé (PID: $WATCHDOG_PID)"
echo ""
echo "📝 Le watchdog surveille maintenant le transfert"
echo "💡 Il relancera automatiquement si le script s'arrête"
echo ""
echo "📋 Commandes utiles:"
echo "   Voir les logs du watchdog: tail -f watchdog.log"
echo "   Voir la progression: python3.10 gestion_progression.py afficher"
echo "   Arrêter le watchdog: kill $WATCHDOG_PID"
echo ""

