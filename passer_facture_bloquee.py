#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASSER UNE FACTURE BLOQUÉE
===========================

Ce script permet de marquer une facture comme "à ignorer" dans la progression
pour que le script principal puisse continuer.
"""

import sys
import json
from pathlib import Path
from connexion_odoo import connecter_odoo

FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'
FICHIER_FACTURES_IGNOREES = Path(__file__).parent / 'factures_ignorees.json'


def charger_progression():
    """Charge la progression."""
    if not FICHIER_PROGRESSION.exists():
        return {'factures_traitees': [], 'derniere_facture_id': 0}
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'factures_traitees': [], 'derniere_facture_id': 0}


def sauvegarder_progression(progression):
    """Sauvegarde la progression."""
    try:
        with open(FICHIER_PROGRESSION, 'w', encoding='utf-8') as f:
            json.dump(progression, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False


def charger_factures_ignorees():
    """Charge la liste des factures ignorées."""
    if not FICHIER_FACTURES_IGNOREES.exists():
        return []
    
    try:
        with open(FICHIER_FACTURES_IGNOREES, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('factures_ignorees', [])
    except:
        return []


def sauvegarder_factures_ignorees(factures_ignorees):
    """Sauvegarde la liste des factures ignorées."""
    try:
        data = {
            'factures_ignorees': factures_ignorees,
            'derniere_maj': str(Path(__file__).stat().st_mtime)
        }
        with open(FICHIER_FACTURES_IGNOREES, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False


def trouver_id_facture(numero_facture):
    """Trouve l'ID d'une facture à partir de son numéro."""
    try:
        uid, models, db, password = connecter_odoo()
        if not uid:
            return None
        
        factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search',
            [[['name', '=', numero_facture], ['move_type', '=', 'out_invoice']]]
        )
        
        if factures:
            return factures[0]
        return None
    except Exception as e:
        print(f"⚠️  Erreur recherche facture: {e}")
        return None


def passer_facture(numero_facture, raison=""):
    """Marque une facture comme à ignorer et l'ajoute à la progression."""
    print("=" * 80)
    print(f"⏭️  PASSER LA FACTURE: {numero_facture}")
    print("=" * 80)
    print()
    
    # Charger la progression
    progression = charger_progression()
    factures_ignorees = charger_factures_ignorees()
    
    # Trouver l'ID de la facture
    print(f"🔍 Recherche de la facture '{numero_facture}'...")
    facture_id = trouver_id_facture(numero_facture)
    
    if facture_id:
        print(f"✅ Facture trouvée (ID: {facture_id})")
    else:
        print("⚠️  Facture non trouvée dans Odoo, continuation quand même...")
        print("   (Elle sera marquée par son numéro)")
    
    # Ajouter à la progression si elle n'y est pas déjà
    if facture_id:
        if facture_id not in progression['factures_traitees']:
            progression['factures_traitees'].append(facture_id)
            progression['derniere_facture_id'] = max(
                progression.get('derniere_facture_id', 0),
                facture_id
            )
            print(f"✅ Facture ajoutée à la progression (ID: {facture_id})")
        else:
            print(f"ℹ️  Facture déjà dans la progression")
    
    # Ajouter à la liste des factures ignorées
    facture_ignoree = {
        'numero': numero_facture,
        'id': facture_id,
        'raison': raison or "Bloquée",
        'date': str(Path(__file__).stat().st_mtime)
    }
    
    # Vérifier si déjà dans la liste
    deja_presente = any(f['numero'] == numero_facture for f in factures_ignorees)
    
    if not deja_presente:
        factures_ignorees.append(facture_ignoree)
        print(f"✅ Facture ajoutée à la liste des factures ignorées")
    else:
        print(f"ℹ️  Facture déjà dans la liste des ignorées")
    
    # Sauvegarder
    print()
    print("💾 Sauvegarde...")
    if sauvegarder_progression(progression):
        print("✅ Progression sauvegardée")
    else:
        print("❌ Erreur sauvegarde progression")
    
    if sauvegarder_factures_ignorees(factures_ignorees):
        print("✅ Liste des factures ignorées sauvegardée")
    else:
        print("❌ Erreur sauvegarde liste ignorées")
    
    print()
    print("=" * 80)
    print("✅ FACTURE MARQUÉE COMME PASSÉE")
    print("=" * 80)
    print()
    print("📋 Le script principal pourra maintenant continuer avec la facture suivante.")
    print()
    
    return True


def lister_factures_ignorees():
    """Liste toutes les factures ignorées."""
    factures_ignorees = charger_factures_ignorees()
    
    print("=" * 80)
    print("📋 FACTURES IGNORÉES")
    print("=" * 80)
    print()
    
    if not factures_ignorees:
        print("✅ Aucune facture ignorée")
    else:
        for i, facture in enumerate(factures_ignorees, 1):
            print(f"{i}. {facture['numero']} (ID: {facture.get('id', 'N/A')})")
            print(f"   Raison: {facture.get('raison', 'Non spécifiée')}")
            print()
    
    print(f"Total: {len(factures_ignorees)} facture(s) ignorée(s)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Passer une facture bloquée')
    parser.add_argument('numero_facture', nargs='?', help='Numéro de la facture à passer (ex: FAC/2025/TAL0000272)')
    parser.add_argument('--raison', help='Raison pour laquelle la facture est ignorée')
    parser.add_argument('--liste', action='store_true', help='Lister toutes les factures ignorées')
    args = parser.parse_args()
    
    if args.liste:
        lister_factures_ignorees()
    elif args.numero_facture:
        passer_facture(args.numero_facture, args.raison or "Bloquée")
    else:
        print("Usage:")
        print("  python passer_facture_bloquee.py <NUMERO_FACTURE> [--raison RAISON]")
        print("  python passer_facture_bloquee.py --liste")
        print()
        print("Exemple:")
        print("  python passer_facture_bloquee.py FAC/2025/TAL0000272 --raison 'Timeout PDF'")

