#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE GESTION DE FACTURES CLIENTS
======================================

Ce script met toutes les factures clients en brouillon
et confirme leur état.
"""

from connexion_odoo import connecter_odoo
import time

def mettre_toutes_factures_en_brouillon():
    """
    Met toutes les factures clients en brouillon
    et affiche un résumé des résultats.
    """
    # Connexion à Odoo
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    try:
        print("\n" + "=" * 60)
        print("RECHERCHE DE TOUTES LES FACTURES CLIENTS")
        print("=" * 60)
        
        # Compter d'abord le nombre total de factures clients
        total_factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_invoice']]]
        )
        
        print(f"\n📊 Nombre total de factures clients: {total_factures}")
        
        if total_factures == 0:
            print("❌ Aucune facture client trouvée dans la base.")
            return False
        
        # Récupérer toutes les factures clients
        print(f"\n🔍 Récupération des factures...")
        factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_read',
            [[['move_type', '=', 'out_invoice']]],
            {
                'fields': ['id', 'name', 'state', 'partner_id', 'amount_total', 'invoice_date'],
                'order': 'id asc'
            }
        )
        
        print(f"✅ {len(factures)} factures récupérées\n")
        
        # Statistiques initiales
        stats = {
            'total': len(factures),
            'deja_brouillon': 0,
            'posted': 0,
            'cancel': 0,
            'autres': 0,
            'succes': 0,
            'echec': 0
        }
        
        # Afficher les 5 premières factures
        print("📄 Premières factures trouvées:")
        for i, facture in enumerate(factures[:5], 1):
            facture_numero = facture.get('name', 'N/A')
            facture_etat = facture.get('state', 'N/A')
            facture_partner = facture.get('partner_id', ['N/A', 'N/A'])[1] if facture.get('partner_id') else 'N/A'
            print(f"   {i}. {facture_numero} - {facture_etat} - {facture_partner}")
        
        if len(factures) > 5:
            print(f"   ... et {len(factures) - 5} autres factures")
        
        # Traiter toutes les factures
        print(f"\n" + "=" * 60)
        print("TRAITEMENT DES FACTURES")
        print("=" * 60)
        
        factures_ids_a_traiter = []
        factures_deja_brouillon = []
        factures_map = {}  # Dictionnaire ID -> numéro pour affichage
        
        for facture in factures:
            facture_id = facture['id']
            facture_numero = facture.get('name', 'N/A')
            facture_etat = facture.get('state', 'N/A')
            
            # Stocker le mapping ID -> numéro
            factures_map[facture_id] = facture_numero
            
            # Compter par état
            if facture_etat == 'draft':
                stats['deja_brouillon'] += 1
                factures_deja_brouillon.append(facture_numero)
            elif facture_etat == 'posted':
                stats['posted'] += 1
                factures_ids_a_traiter.append(facture_id)
            elif facture_etat == 'cancel':
                stats['cancel'] += 1
            else:
                stats['autres'] += 1
                factures_ids_a_traiter.append(facture_id)
        
        print(f"\n📊 Répartition par état:")
        print(f"   ✅ Déjà en brouillon: {stats['deja_brouillon']}")
        print(f"   📝 Validées (posted): {stats['posted']}")
        print(f"   ❌ Annulées (cancel): {stats['cancel']}")
        print(f"   🔄 Autres états: {stats['autres']}")
        print(f"   📋 À traiter: {len(factures_ids_a_traiter)}")
        
        if not factures_ids_a_traiter:
            print(f"\n✅ Toutes les factures sont déjà en brouillon!")
            return True
        
        # Traiter par lots pour optimiser
        BATCH_SIZE = 200
        total_lots = (len(factures_ids_a_traiter) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n🔄 Mise en brouillon de {len(factures_ids_a_traiter)} factures...")
        print(f"   Traitement par lots de {BATCH_SIZE} factures ({total_lots} lots)")
        
        factures_traitees = []  # Liste des numéros de factures traitées
        
        for lot_num in range(total_lots):
            debut = lot_num * BATCH_SIZE
            fin = min(debut + BATCH_SIZE, len(factures_ids_a_traiter))
            lot_ids = factures_ids_a_traiter[debut:fin]
            
            try:
                # Mettre en brouillon par lot
                models.execute_kw(
                    db, uid, password,
                    'account.move',
                    'write',
                    [lot_ids, {'state': 'draft'}]
                )
                stats['succes'] += len(lot_ids)
                
                # Récupérer les numéros des factures traitées dans ce lot
                lot_numeros = [factures_map.get(fid, f'ID:{fid}') for fid in lot_ids]
                factures_traitees.extend(lot_numeros)
                
                progress = (lot_num + 1) * 100 // total_lots
                print(f"\n   Lot {lot_num + 1}/{total_lots}: ✅ {len(lot_ids)} factures traitées ({stats['succes']}/{len(factures_ids_a_traiter)} - {progress}%)")
                
                # Afficher les numéros de factures traitées (premiers et derniers du lot)
                if len(lot_numeros) <= 10:
                    print(f"      Numéros: {', '.join(lot_numeros)}")
                else:
                    print(f"      Numéros: {', '.join(lot_numeros[:5])} ... {', '.join(lot_numeros[-5:])}")
            except Exception as e:
                print(f"\n      ⚠️  Erreur sur le lot {lot_num + 1}: {str(e)[:100]}")
                # Essayer par sous-lots plus petits en cas d'erreur
                SUB_BATCH = 100
                for sub_start in range(0, len(lot_ids), SUB_BATCH):
                    sub_end = min(sub_start + SUB_BATCH, len(lot_ids))
                    sub_lot = lot_ids[sub_start:sub_end]
                    try:
                        models.execute_kw(
                            db, uid, password,
                            'account.move',
                            'write',
                            [sub_lot, {'state': 'draft'}]
                        )
                        stats['succes'] += len(sub_lot)
                    except Exception as e2:
                        # En dernier recours, essayer une par une
                        for facture_id in sub_lot:
                            try:
                                models.execute_kw(
                                    db, uid, password,
                                    'account.move',
                                    'write',
                                    [[facture_id], {'state': 'draft'}]
                                )
                                stats['succes'] += 1
                            except Exception as e3:
                                stats['echec'] += 1
                                print(f"\n         ❌ Échec ID {facture_id}: {str(e3)[:80]}")
        
        print()  # Nouvelle ligne après la barre de progression
        
        # Vérification finale
        print(f"\n" + "=" * 60)
        print("VÉRIFICATION FINALE")
        print("=" * 60)
        
        # Recompter les factures en brouillon
        factures_brouillon = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_invoice'], ['state', '=', 'draft']]]
        )
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   ✅ Succès: {stats['succes']} factures mises en brouillon")
        print(f"   ❌ Échecs: {stats['echec']} factures")
        print(f"   📋 Déjà en brouillon: {stats['deja_brouillon']}")
        print(f"   📊 Total en brouillon maintenant: {factures_brouillon}/{total_factures}")
        
        # Afficher les numéros de factures traitées
        if factures_traitees:
            print(f"\n📄 NUMÉROS DES FACTURES TRAITÉES ({len(factures_traitees)} factures):")
            if len(factures_traitees) <= 50:
                # Afficher toutes si moins de 50
                for i, numero in enumerate(factures_traitees, 1):
                    print(f"   {i}. {numero}")
            else:
                # Afficher les 25 premières et 25 dernières
                print(f"   (Affichage des 25 premières et 25 dernières)")
                for i, numero in enumerate(factures_traitees[:25], 1):
                    print(f"   {i}. {numero}")
                print(f"   ... ({len(factures_traitees) - 50} factures au milieu) ...")
                for i, numero in enumerate(factures_traitees[-25:], len(factures_traitees) - 24):
                    print(f"   {i}. {numero}")
        
        if factures_brouillon == total_factures:
            print(f"\n✅ CONFIRMATION: Toutes les factures clients sont en brouillon!")
        elif factures_brouillon == stats['deja_brouillon'] + stats['succes']:
            print(f"\n✅ CONFIRMATION: Toutes les factures traitées sont en brouillon!")
        else:
            print(f"\n⚠️  ATTENTION: Certaines factures ne sont pas en brouillon")
            print(f"   Vérifiez les factures annulées ou dans d'autres états")
        
        return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la gestion des factures: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("GESTION DE TOUTES LES FACTURES CLIENTS - TAL-migration")
    print("=" * 60)
    
    mettre_toutes_factures_en_brouillon()
    
    print("\n" + "=" * 60)

