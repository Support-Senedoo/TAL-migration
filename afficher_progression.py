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


def obtenir_date_modification_progression():
    """Obtient la date de modification du fichier de progression."""
    if not FICHIER_PROGRESSION.exists():
        return None
    return datetime.fromtimestamp(os.path.getmtime(FICHIER_PROGRESSION))


def obtenir_derniere_facture_depuis_log():
    """Extrait la dernière facture traitée depuis le log."""
    dernier_log = trouver_dernier_log()
    if not dernier_log:
        return None
    
    try:
        with open(dernier_log, 'r', encoding='utf-8', errors='ignore') as f:
            lignes = f.readlines()
            # Chercher la dernière ligne qui contient "Traitement facture"
            for ligne in reversed(lignes):
                if 'Traitement facture' in ligne or 'Facture' in ligne:
                    # Essayer d'extraire le numéro ou l'ID
                    import re
                    # Chercher "Facture XXX" ou "ID: XXX"
                    match = re.search(r'Facture\s+([A-Z0-9-]+)|ID:\s*(\d+)', ligne)
                    if match:
                        return match.group(1) or match.group(2)
        return None
    except:
        return None


def afficher_progression(ancienne_progression=None):
    """Affiche la progression actuelle."""
    progression = obtenir_progression()
    nb_factures = len(progression.get('factures_traitees', []))
    derniere_id = progression.get('derniere_facture_id', 0)
    
    # Vérifier si la progression a changé
    progression_changée = False
    if ancienne_progression:
        ancien_nb = len(ancienne_progression.get('factures_traitees', []))
        progression_changée = nb_factures != ancien_nb
    
    # Date de modification du fichier
    date_modif = obtenir_date_modification_progression()
    
    # Nettoyer l'écran
    os.system('clear' if os.name != 'nt' else 'cls')
    
    print("=" * 80)
    print("📊 PROGRESSION DU TRANSFERT DES FACTURES")
    print("=" * 80)
    print()
    print(f"✅ Factures traitées     : {nb_factures}")
    print(f"📋 Dernière facture ID   : {derniere_id}")
    
    # Afficher la date de dernière modification
    if date_modif:
        maintenant = datetime.now()
        delta = maintenant - date_modif
        minutes_ecoulees = delta.total_seconds() / 60
        
        if minutes_ecoulees < 1:
            statut = "🟢 TRÈS RÉCENT (< 1 min)"
        elif minutes_ecoulees < 5:
            statut = f"🟡 RÉCENT ({int(minutes_ecoulees)} min)"
        elif minutes_ecoulees < 30:
            statut = f"🟠 ANCIEN ({int(minutes_ecoulees)} min)"
        else:
            heures = minutes_ecoulees / 60
            statut = f"🔴 TRÈS ANCIEN ({heures:.1f} h)"
        
        print(f"📅 Dernière mise à jour : {date_modif.strftime('%Y-%m-%d %H:%M:%S')} ({statut})")
    
    if progression_changée:
        print("🔄 PROGRESSION DÉTECTÉE - Le script est actif !")
    
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
    
    # Afficher le dernier log avec plus d'infos
    dernier_log = trouver_dernier_log()
    if dernier_log:
        date_modif_log = datetime.fromtimestamp(os.path.getmtime(dernier_log))
        maintenant = datetime.now()
        delta_log = (maintenant - date_modif_log).total_seconds() / 60
        
        print(f"📄 Dernier fichier log: {dernier_log.name}")
        print(f"📅 Log modifié il y a: {delta_log:.1f} minutes")
        
        if delta_log > 10:
            print("⚠️  ATTENTION: Le log n'a pas été modifié récemment - le script est peut-être bloqué")
        elif delta_log < 5:
            print("✅ Le script semble actif")
        
        print()
        
        # Afficher les 15 dernières lignes du log
        try:
            with open(dernier_log, 'r', encoding='utf-8', errors='ignore') as f:
                lignes = f.readlines()
                if lignes:
                    print("📋 Dernières lignes du log:")
                    print("-" * 80)
                    # Afficher les 15 dernières lignes non vides
                    lignes_non_vides = [l for l in lignes if l.strip()]
                    for ligne in lignes_non_vides[-15:]:
                        print(ligne.rstrip())
                    print("-" * 80)
        except Exception as e:
            print(f"⚠️  Erreur lecture log: {e}")
    
    print()
    print("💡 Actualisation automatique toutes les 5 secondes...")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    
    return progression


def suivre_progression_temps_reel():
    """Suit la progression en temps réel."""
    ancienne_progression = obtenir_progression()
    
    try:
        while True:
            ancienne_progression = afficher_progression(ancienne_progression)
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
