#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT POUR AFFICHER LA PROGRESSION DU TRANSFERT
================================================

Ce script affiche la progression en temps réel du transfert des factures.
"""

import json
import time
from pathlib import Path
from datetime import datetime
import os

FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'


def obtenir_progression():
    """Obtient la progression actuelle."""
    if not FICHIER_PROGRESSION.exists():
        return {'factures_traitees': [], 'derniere_facture_id': 0}
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Erreur lecture progression: {e}")
        return {'factures_traitees': [], 'derniere_facture_id': 0}


def trouver_dernier_log():
    """Trouve le dernier fichier log."""
    log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
    if not log_files:
        return None
    return max(log_files, key=os.path.getmtime)


def afficher_progression():
    """Affiche la progression actuelle."""
    progression = obtenir_progression()
    nb_factures = len(progression.get('factures_traitees', []))
    derniere_id = progression.get('derniere_facture_id', 0)
    
    # Nettoyer l'écran
    os.system('clear' if os.name != 'nt' else 'cls')
    
    print("=" * 80)
    print("📊 PROGRESSION DU TRANSFERT DES FACTURES")
    print("=" * 80)
    print()
    print(f"✅ Factures traitées     : {nb_factures}")
    print(f"📋 Dernière facture ID   : {derniere_id}")
    print()
    
    # Afficher quelques dernières factures traitées
    factures_traitees = progression.get('factures_traitees', [])
    if factures_traitees:
        print("📝 5 dernières factures traitées:")
        print("-" * 80)
        for facture_id in factures_traitees[-5:]:
            print(f"   • Facture ID: {facture_id}")
        print("-" * 80)
        print()
    
    # Afficher le dernier log
    dernier_log = trouver_dernier_log()
    if dernier_log:
        print(f"📄 Dernier fichier log: {dernier_log.name}")
        
        # Afficher les 10 dernières lignes du log
        try:
            with open(dernier_log, 'r', encoding='utf-8', errors='ignore') as f:
                lignes = f.readlines()
                if lignes:
                    print()
                    print("📋 Dernières lignes du log:")
                    print("-" * 80)
                    for ligne in lignes[-10:]:
                        print(ligne.rstrip())
                    print("-" * 80)
        except Exception as e:
            print(f"⚠️  Erreur lecture log: {e}")
    
    print()
    print("💡 Actualisation automatique toutes les 5 secondes...")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")


def suivre_progression_temps_reel():
    """Suit la progression en temps réel."""
    try:
        while True:
            afficher_progression()
            time.sleep(5)  # Actualiser toutes les 5 secondes
    except KeyboardInterrupt:
        print("\n\n⚠️  Suivi interrompu par l'utilisateur")
        print("✅ La progression reste sauvegardée")


def afficher_resume_complet():
    """Affiche un résumé complet de la progression."""
    progression = obtenir_progression()
    nb_factures = len(progression.get('factures_traitees', []))
    derniere_id = progression.get('derniere_facture_id', 0)
    
    print("=" * 80)
    print("📊 RÉSUMÉ COMPLET DE LA PROGRESSION")
    print("=" * 80)
    print()
    print(f"✅ Nombre total de factures traitées: {nb_factures}")
    print(f"📋 ID de la dernière facture traitée: {derniere_id}")
    print()
    
    # Afficher toutes les factures traitées (si pas trop nombreuses)
    factures_traitees = progression.get('factures_traitees', [])
    if factures_traitees:
        if len(factures_traitees) <= 50:
            print("📝 Liste complète des factures traitées:")
            print("-" * 80)
            for i, facture_id in enumerate(factures_traitees, 1):
                print(f"   {i:4d}. Facture ID: {facture_id}")
            print("-" * 80)
        else:
            print(f"📝 {len(factures_traitees)} factures traitées au total")
            print("📝 10 premières factures:")
            print("-" * 80)
            for i, facture_id in enumerate(factures_traitees[:10], 1):
                print(f"   {i:4d}. Facture ID: {facture_id}")
            print("   ...")
            print("📝 10 dernières factures:")
            print("-" * 80)
            for i, facture_id in enumerate(factures_traitees[-10:], len(factures_traitees)-9):
                print(f"   {i:4d}. Facture ID: {facture_id}")
            print("-" * 80)
    
    # Afficher les informations du dernier log
    dernier_log = trouver_dernier_log()
    if dernier_log:
        print()
        print(f"📄 Fichier log le plus récent: {dernier_log.name}")
        
        # Vérifier la date de modification
        date_modif = datetime.fromtimestamp(os.path.getmtime(dernier_log))
        print(f"📅 Dernière modification: {date_modif.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Compter les lignes
        try:
            with open(dernier_log, 'r', encoding='utf-8', errors='ignore') as f:
                nb_lignes = sum(1 for _ in f)
                taille = os.path.getsize(dernier_log) / 1024  # Taille en KB
                print(f"📊 Nombre de lignes: {nb_lignes}")
                print(f"💾 Taille: {taille:.2f} KB")
        except:
            pass


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Afficher la progression du transfert')
    parser.add_argument('--resume', action='store_true', help='Afficher un résumé complet et quitter')
    parser.add_argument('--watch', action='store_true', help='Suivre en temps réel (actualisation toutes les 5 secondes)')
    args = parser.parse_args()
    
    if args.resume:
        afficher_resume_complet()
    elif args.watch:
        suivre_progression_temps_reel()
    else:
        # Mode par défaut: afficher une fois puis suivre
        afficher_progression()
        print("\n💡 Pour suivre en temps réel: python afficher_progression.py --watch")
        print("💡 Pour un résumé complet: python afficher_progression.py --resume")
