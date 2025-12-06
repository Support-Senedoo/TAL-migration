#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour analyser pourquoi le script s'est arrêté
"""

from pathlib import Path
import re
from datetime import datetime

def analyser_logs():
    """Analyse les logs pour trouver la cause de l'arrêt."""
    print("=" * 80)
    print("ANALYSE DES LOGS - POURQUOI LE SCRIPT S'EST ARRÊTÉ")
    print("=" * 80)
    print()
    
    # Trouver le dernier fichier log
    log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
    if not log_files:
        print("❌ Aucun fichier log trouvé")
        return
    
    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 Analyse du fichier: {latest_log.name}")
    print()
    
    # Lire le fichier
    try:
        with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return
    
    if not lines:
        print("❌ Fichier vide")
        return
    
    # Analyser les dernières lignes
    print("=" * 80)
    print("DERNIÈRES LIGNES DU LOG")
    print("=" * 80)
    print()
    
    # Afficher les 30 dernières lignes
    for line in lines[-30:]:
        print(line.rstrip())
    
    print()
    print("=" * 80)
    print("RECHERCHE D'ERREURS")
    print("=" * 80)
    print()
    
    # Chercher des erreurs
    erreurs = []
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        if any(mot in line_lower for mot in ['erreur', 'error', 'exception', 'traceback', 'failed', '❌', 'fatal']):
            erreurs.append((i, line.rstrip()))
    
    if erreurs:
        print(f"⚠️  {len(erreurs)} erreur(s) trouvée(s):")
        print()
        for num, erreur in erreurs[-10:]:  # Dernières 10 erreurs
            print(f"Ligne {num}: {erreur}")
    else:
        print("✅ Aucune erreur explicite trouvée dans les logs")
    
    print()
    print("=" * 80)
    print("ANALYSE DE LA DERNIÈRE FACTURE")
    print("=" * 80)
    print()
    
    # Chercher la dernière facture traitée
    dernier_succes = None
    derniere_facture_en_cours = None
    
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if '✅ Facture' in line and 'traitée avec succès' in line:
            dernier_succes = (i + 1, line.rstrip())
            break
        if 'Traitement facture' in line:
            derniere_facture_en_cours = (i + 1, line.rstrip())
    
    if dernier_succes:
        print(f"✅ Dernière facture traitée avec succès:")
        print(f"   Ligne {dernier_succes[0]}: {dernier_succes[1]}")
    else:
        print("⚠️  Aucune facture traitée avec succès trouvée")
    
    if derniere_facture_en_cours:
        print()
        print(f"🔄 Dernière facture en cours:")
        print(f"   Ligne {derniere_facture_en_cours[0]}: {derniere_facture_en_cours[1]}")
    
    # Chercher ce qui s'est passé après la dernière facture
    print()
    print("=" * 80)
    print("CE QUI S'EST PASSÉ APRÈS")
    print("=" * 80)
    print()
    
    if dernier_succes:
        idx = dernier_succes[0] - 1
        lignes_apres = lines[idx:idx+20]
        print("Lignes après le dernier succès:")
        for i, line in enumerate(lignes_apres, idx + 1):
            print(f"{i}: {line.rstrip()}")
    
    print()
    print("=" * 80)
    print("CAUSES POSSIBLES")
    print("=" * 80)
    print()
    
    # Analyser la dernière ligne
    derniere_ligne = lines[-1].rstrip() if lines else ""
    
    causes = []
    
    if not derniere_ligne or derniere_ligne == "":
        causes.append("⚠️  Le fichier se termine brutalement (crash probable)")
    
    if any(mot in derniere_ligne.lower() for mot in ['timeout', 'timed out']):
        causes.append("⏱️  Timeout réseau détecté")
    
    if any(mot in derniere_ligne.lower() for mot in ['memory', 'killed', 'oom']):
        causes.append("💾 Problème de mémoire (OOM)")
    
    if 'traceback' in derniere_ligne.lower() or 'exception' in derniere_ligne.lower():
        causes.append("🐍 Exception Python non gérée")
    
    if not causes:
        causes.append("ℹ️  Cause indéterminée - le script s'est arrêté sans message d'erreur visible")
        causes.append("   Possible: crash silencieux, timeout, ou erreur réseau")
    
    for cause in causes:
        print(f"  {cause}")
    
    print()
    print("=" * 80)
    print("RECOMMANDATION")
    print("=" * 80)
    print()
    print("✅ Utilisez le mode watchdog pour relancer automatiquement:")
    print("   python3.10 gestion_transfert.py --watchdog")
    print()
    print("   Le script reprendra automatiquement après la dernière facture traitée.")


if __name__ == "__main__":
    analyser_logs()



