#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFIER QUE TOUTES LES FACTURES ONT ÉTÉ TRAITÉES
==================================================

Ce script vérifie si toutes les factures clients ont été transférées vers le module Documents.
"""

import json
from pathlib import Path
from connexion_odoo import connecter_odoo

FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'


def charger_progression():
    """Charge la progression sauvegardée."""
    if not FICHIER_PROGRESSION.exists():
        return {'factures_traitees': [], 'derniere_facture_id': 0}
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Erreur lecture progression: {e}")
        return {'factures_traitees': [], 'derniere_facture_id': 0}


def compter_factures_odoo():
    """Compte toutes les factures clients dans Odoo."""
    print("🔍 Connexion à Odoo...")
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Erreur de connexion à Odoo")
        return None
    
    print("✅ Connecté à Odoo")
    print()
    
    print("📊 Comptage des factures clients dans Odoo...")
    try:
        # Utiliser search_count() si disponible, sinon compter manuellement
        try:
            # Essayer search_count() d'abord (méthode recommandée)
            total_factures = models.execute_kw(
                db, uid, password,
                'account.move',
                'search_count',
                [[['move_type', '=', 'out_invoice']]]
            )
        except:
            # Si search_count() n'existe pas, utiliser search() et compter
            factures_ids = models.execute_kw(
                db, uid, password,
                'account.move',
                'search',
                [[['move_type', '=', 'out_invoice']]]
            )
            total_factures = len(factures_ids)
        
        print(f"✅ Total de factures clients dans Odoo: {total_factures}")
        print()
        
        return total_factures
    except Exception as e:
        print(f"❌ Erreur lors du comptage: {e}")
        return None


def verifier_documents_existants(factures_ids_traitees):
    """Vérifie combien de factures ont effectivement un document dans Documents."""
    print("🔍 Vérification des documents existants dans le module Documents...")
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        return None
    
    try:
        # Utiliser search_count() si disponible, sinon compter manuellement
        try:
            # Essayer search_count() d'abord
            documents = models.execute_kw(
                db, uid, password,
                'documents.document',
                'search_count',
                [[
                    ['res_model', '=', 'account.move'],
                    ['res_id', 'in', factures_ids_traitees]
                ]]
            )
        except:
            # Si search_count() n'existe pas, utiliser search() et compter
            documents_ids = models.execute_kw(
                db, uid, password,
                'documents.document',
                'search',
                [[
                    ['res_model', '=', 'account.move'],
                    ['res_id', 'in', factures_ids_traitees]
                ]]
            )
            documents = len(documents_ids)
        
        return documents
    except Exception as e:
        print(f"⚠️  Erreur vérification documents: {e}")
        return None


def verifier_completude():
    """Vérifie si toutes les factures ont été traitées."""
    print("=" * 80)
    print("📋 VÉRIFICATION COMPLÉTUDE DU TRANSFERT")
    print("=" * 80)
    print()
    
    # 1. Charger la progression
    print("1️⃣  Chargement de la progression sauvegardée...")
    progression = charger_progression()
    factures_traitees = progression.get('factures_traitees', [])
    nb_factures_traitees = len(factures_traitees)
    derniere_id = progression.get('derniere_facture_id', 0)
    
    print(f"   ✅ Factures dans la progression: {nb_factures_traitees}")
    print(f"   📋 Dernière facture ID: {derniere_id}")
    print()
    
    # 2. Compter toutes les factures dans Odoo
    print("2️⃣  Comptage des factures dans Odoo...")
    total_factures_odoo = compter_factures_odoo()
    
    if total_factures_odoo is None:
        print("❌ Impossible de compter les factures dans Odoo")
        return
    
    print()
    
    # 3. Vérifier les documents existants
    print("3️⃣  Vérification des documents dans le module Documents...")
    if factures_traitees:
        nb_documents = verifier_documents_existants(factures_traitees)
        if nb_documents is not None:
            print(f"   ✅ Documents trouvés: {nb_documents}")
        else:
            print(f"   ⚠️  Impossible de vérifier les documents")
    else:
        nb_documents = 0
        print(f"   ℹ️  Aucune facture traitée pour vérifier")
    print()
    
    # 4. Calculer les statistiques
    print("=" * 80)
    print("📊 RÉSUMÉ")
    print("=" * 80)
    print()
    print(f"📦 Total de factures dans Odoo        : {total_factures_odoo}")
    print(f"✅ Factures dans la progression       : {nb_factures_traitees}")
    if nb_documents is not None:
        print(f"📎 Documents créés dans Documents    : {nb_documents}")
    print()
    
    # Calculer les différences
    factures_restantes = total_factures_odoo - nb_factures_traitees
    pourcentage_traite = (nb_factures_traitees * 100) / total_factures_odoo if total_factures_odoo > 0 else 0
    
    print(f"📊 Progression: {pourcentage_traite:.1f}%")
    print()
    
    if factures_restantes == 0:
        print("=" * 80)
        print("🎉 TOUTES LES FACTURES ONT ÉTÉ TRAITÉES !")
        print("=" * 80)
        print()
        print(f"✅ {nb_factures_traitees} factures traitées sur {total_factures_odoo}")
        if nb_documents is not None:
            print(f"📎 {nb_documents} documents créés dans le module Documents")
    else:
        print("=" * 80)
        print("⚠️  IL RESTE DES FACTURES À TRAITER")
        print("=" * 80)
        print()
        print(f"📋 Factures restantes: {factures_restantes}")
        print(f"⏱️  Temps estimé (à ~3-4s/facture): {factures_restantes * 3.5 / 60:.1f} minutes")
        print()
        print("💡 Pour continuer le transfert:")
        print("   python3.10 gestion_transfert.py")
    
    print()
    
    # 5. Vérifier la cohérence
    if nb_documents is not None and nb_documents < nb_factures_traitees:
        difference = nb_factures_traitees - nb_documents
        print("=" * 80)
        print("⚠️  ATTENTION: Incohérence détectée")
        print("=" * 80)
        print()
        print(f"   {difference} facture(s) sont dans la progression mais n'ont pas de document")
        print("   Cela peut signifier:")
        print("   - Des erreurs lors de la création des documents")
        print("   - Des documents supprimés manuellement")
        print("   - Des factures traitées mais sans PDF généré")
        print()
    
    # 6. Afficher les dernières factures traitées
    if factures_traitees:
        print("=" * 80)
        print("📝 10 dernières factures traitées")
        print("=" * 80)
        print()
        for facture_id in factures_traitees[-10:]:
            print(f"   • Facture ID: {facture_id}")
        print()


if __name__ == "__main__":
    verifier_completude()

