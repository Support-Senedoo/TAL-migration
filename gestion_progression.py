#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE GESTION DE LA PROGRESSION DU TRANSFERT
=================================================

Ce script permet de consulter, réinitialiser ou nettoyer la progression
du transfert des factures vers le module Document.
"""

import json
from pathlib import Path

FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'


def afficher_progression():
    """Affiche l'état actuel de la progression."""
    if not FICHIER_PROGRESSION.exists():
        print("📋 Aucun fichier de progression trouvé.")
        print("   Le transfert n'a pas encore été démarré.")
        return
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            progression = json.load(f)
        
        factures_traitees = progression.get('factures_traitees', [])
        derniere_id = progression.get('derniere_facture_id', 0)
        
        print("=" * 60)
        print("ÉTAT DE LA PROGRESSION")
        print("=" * 60)
        print(f"📊 Nombre de factures traitées: {len(factures_traitees)}")
        print(f"📋 Dernière facture ID traitée: {derniere_id}")
        
        if factures_traitees:
            print(f"\n📄 Premières factures traitées (max 10):")
            for i, facture_id in enumerate(factures_traitees[:10], 1):
                print(f"   {i}. Facture ID: {facture_id}")
            if len(factures_traitees) > 10:
                print(f"   ... et {len(factures_traitees) - 10} autres factures")
        
        return progression
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de la progression: {str(e)}")
        return None


def reinitialiser_progression():
    """Réinitialise la progression (supprime le fichier)."""
    if not FICHIER_PROGRESSION.exists():
        print("📋 Aucun fichier de progression à réinitialiser.")
        return
    
    try:
        # Afficher d'abord l'état actuel
        progression = afficher_progression()
        if progression:
            factures_traitees = len(progression.get('factures_traitees', []))
            if factures_traitees > 0:
                print(f"\n⚠️  ATTENTION: Vous allez supprimer la progression de {factures_traitees} factures traitées!")
                reponse = input("   Confirmez-vous la réinitialisation ? (oui/NON): ").strip().lower()
                if reponse != 'oui':
                    print("   ❌ Réinitialisation annulée.")
                    return
        
        FICHIER_PROGRESSION.unlink()
        print(f"\n✅ Progression réinitialisée avec succès!")
        print("   Le prochain transfert repartira depuis le début.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {str(e)}")


def nettoyer_progression():
    """Nettoie la progression en gardant seulement les 1000 dernières factures."""
    if not FICHIER_PROGRESSION.exists():
        print("📋 Aucun fichier de progression à nettoyer.")
        return
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            progression = json.load(f)
        
        factures_traitees = progression.get('factures_traitees', [])
        
        if len(factures_traitees) <= 1000:
            print(f"📋 La progression contient seulement {len(factures_traitees)} factures.")
            print("   Aucun nettoyage nécessaire (limite: 1000 factures).")
            return
        
        print(f"📋 Nettoyage de la progression...")
        print(f"   Avant: {len(factures_traitees)} factures")
        
        # Garder seulement les 1000 dernières
        progression['factures_traitees'] = factures_traitees[-1000:]
        progression['derniere_facture_id'] = max(progression['factures_traitees']) if progression['factures_traitees'] else 0
        
        with open(FICHIER_PROGRESSION, 'w', encoding='utf-8') as f:
            json.dump(progression, f, indent=2, ensure_ascii=False)
        
        print(f"   Après: {len(progression['factures_traitees'])} factures")
        print(f"✅ Progression nettoyée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")


def main():
    """Fonction principale."""
    import sys
    
    print("=" * 60)
    print("GESTION DE LA PROGRESSION DU TRANSFERT")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        commande = sys.argv[1].lower()
        
        if commande == 'afficher' or commande == 'show':
            afficher_progression()
        elif commande == 'reinitialiser' or commande == 'reset':
            reinitialiser_progression()
        elif commande == 'nettoyer' or commande == 'clean':
            nettoyer_progression()
        else:
            print(f"❌ Commande inconnue: {commande}")
            print("\nCommandes disponibles:")
            print("   afficher / show     - Affiche l'état de la progression")
            print("   reinitialiser / reset - Réinitialise la progression")
            print("   nettoyer / clean    - Nettoie la progression (garde 1000 dernières)")
    else:
        # Par défaut, afficher la progression
        afficher_progression()
        print("\n💡 Utilisation:")
        print("   python gestion_progression.py afficher")
        print("   python gestion_progression.py reinitialiser")
        print("   python gestion_progression.py nettoyer")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()


