#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFIER ET DIAGNOSTIQUER UN BLOCAGE
====================================

Ce script vérifie l'état actuel du script et diagnostique les problèmes.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import subprocess

FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'


def verifier_script_en_cours():
    """Vérifie si le script tourne."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'transferer_factures_documents_v2.py'],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except:
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            return 'transferer_factures_documents_v2.py' in result.stdout
        except:
            return False


def obtenir_progression():
    """Obtient la progression actuelle."""
    if not FICHIER_PROGRESSION.exists():
        return None
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None


def trouver_dernier_log():
    """Trouve le dernier fichier log."""
    log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
    if not log_files:
        return None
    return max(log_files, key=os.path.getmtime)


def analyser_blocage():
    """Analyse la situation pour diagnostiquer le blocage."""
    print("=" * 80)
    print("🔍 DIAGNOSTIC DE BLOCAGE")
    print("=" * 80)
    print()
    
    # 1. Vérifier si le script tourne
    print("1️⃣  Vérification si le script est en cours d'exécution...")
    script_en_cours = verifier_script_en_cours()
    if script_en_cours:
        print("   ✅ Le script est en cours d'exécution")
    else:
        print("   ❌ Le script n'est PAS en cours d'exécution")
    print()
    
    # 2. Vérifier la progression
    print("2️⃣  Vérification de la progression...")
    progression = obtenir_progression()
    if progression:
        nb_factures = len(progression.get('factures_traitees', []))
        derniere_id = progression.get('derniere_facture_id', 0)
        
        # Date de modification
        date_modif = datetime.fromtimestamp(os.path.getmtime(FICHIER_PROGRESSION))
        maintenant = datetime.now()
        delta = (maintenant - date_modif).total_seconds() / 60
        
        print(f"   📊 Factures traitées: {nb_factures}")
        print(f"   📋 Dernière facture ID: {derniere_id}")
        print(f"   📅 Dernière mise à jour: {date_modif.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   ⏱️  Il y a: {delta:.1f} minutes")
        
        if delta > 10:
            print(f"   ⚠️  ATTENTION: Pas de mise à jour depuis {delta:.1f} minutes")
        else:
            print(f"   ✅ Progression récente")
    else:
        print("   ❌ Fichier de progression non trouvé")
    print()
    
    # 3. Vérifier le dernier log
    print("3️⃣  Analyse du dernier log...")
    dernier_log = trouver_dernier_log()
    if dernier_log:
        date_modif_log = datetime.fromtimestamp(os.path.getmtime(dernier_log))
        maintenant = datetime.now()
        delta_log = (maintenant - date_modif_log).total_seconds() / 60
        
        print(f"   📄 Fichier: {dernier_log.name}")
        print(f"   📅 Dernière modification: {date_modif_log.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   ⏱️  Il y a: {delta_log:.1f} minutes")
        
        # Lire les dernières lignes
        try:
            with open(dernier_log, 'r', encoding='utf-8', errors='ignore') as f:
                lignes = f.readlines()
                
                print(f"   📊 Nombre de lignes: {len(lignes)}")
                
                # Chercher la dernière facture mentionnée
                print()
                print("   📋 Dernières lignes du log:")
                print("   " + "-" * 76)
                for ligne in lignes[-20:]:
                    ligne_clean = ligne.strip()
                    if ligne_clean:
                        print(f"   {ligne_clean[:76]}")
                print("   " + "-" * 76)
                
                # Chercher des erreurs
                erreurs = [l for l in lignes if 'ERREUR' in l.upper() or 'ERROR' in l.upper()]
                if erreurs:
                    print()
                    print(f"   ⚠️  {len(erreurs)} ligne(s) avec erreur trouvée(s):")
                    for err in erreurs[-5:]:
                        print(f"      {err.strip()[:70]}")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture log: {e}")
    else:
        print("   ❌ Aucun fichier log trouvé")
    print()
    
    # 4. Recommandations
    print("=" * 80)
    print("💡 RECOMMANDATIONS")
    print("=" * 80)
    print()
    
    if not script_en_cours:
        print("✅ Le script n'est pas en cours - vous pouvez le relancer")
    elif delta > 10:
        print("⚠️  Le script semble bloqué (pas de progression depuis plus de 10 min)")
        print()
        print("   Actions possibles:")
        print("   1. Arrêter le script:")
        print("      pkill -f transferer_factures_documents_v2.py")
        print()
        print("   2. Diagnostiquer la facture qui bloque:")
        print("      python3.10 diagnostiquer_facture.py FAC/2024/TAL1021652")
        print()
        print("   3. Voir les dernières lignes du log:")
        print(f"      tail -50 {dernier_log.name if dernier_log else 'transfert_detaille_*.log'}")
        print()
        print("   4. Relancer le script:")
        print("      python3.10 gestion_transfert.py")
    else:
        print("✅ Le script semble actif - surveiller la progression")
        print()
        print("   Pour suivre en temps réel:")
        print("   python3.10 afficher_progression.py --watch")


if __name__ == "__main__":
    analyser_blocage()

