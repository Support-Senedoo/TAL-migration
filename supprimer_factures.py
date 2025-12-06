#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE SUPPRESSION DES FACTURES CLIENTS
===========================================

⚠️  ATTENTION: Cette opération est IRRÉVERSIBLE!
Ce script supprime toutes les factures clients de la base.

Auteur: Assistant IA
Date: 2025-11-29
"""

from connexion_odoo import connecter_odoo
import time

def supprimer_toutes_factures_clients():
    """
    Supprime toutes les factures clients de la base Odoo.
    ⚠️  OPÉRATION IRRÉVERSIBLE!
    """
    # Connexion à Odoo
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    try:
        print("\n" + "=" * 60)
        print("⚠️  SUPPRESSION DE TOUTES LES FACTURES CLIENTS")
        print("=" * 60)
        print("⚠️  ATTENTION: Cette opération est IRRÉVERSIBLE!")
        print()
        
        # Compter d'abord le nombre total de factures clients
        total_factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_invoice']]]
        )
        
        print(f"📊 Nombre total de factures clients à supprimer: {total_factures}")
        
        if total_factures == 0:
            print("✅ Aucune facture client à supprimer.")
            return True
        
        # Récupérer toutes les factures clients avec leurs numéros
        print(f"\n🔍 Récupération des factures...")
        factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_read',
            [[['move_type', '=', 'out_invoice']]],
            {
                'fields': ['id', 'name', 'state', 'partner_id', 'amount_total'],
                'order': 'id asc'
            }
        )
        
        print(f"✅ {len(factures)} factures récupérées")
        
        # Créer un mapping ID -> numéro
        factures_map = {}
        factures_ids = []
        
        for facture in factures:
            facture_id = facture['id']
            facture_numero = facture.get('name', f'ID:{facture_id}')
            factures_map[facture_id] = facture_numero
            factures_ids.append(facture_id)
        
        # Afficher les premières factures
        print(f"\n📄 Premières factures à supprimer:")
        for i, facture in enumerate(factures[:10], 1):
            facture_numero = facture.get('name', 'N/A')
            facture_etat = facture.get('state', 'N/A')
            facture_partner = facture.get('partner_id', ['N/A', 'N/A'])[1] if facture.get('partner_id') else 'N/A'
            print(f"   {i}. {facture_numero} - {facture_etat} - {facture_partner}")
        
        if len(factures) > 10:
            print(f"   ... et {len(factures) - 10} autres factures")
        
        # Statistiques
        stats = {
            'total': len(factures_ids),
            'succes': 0,
            'echec': 0
        }
        
        factures_supprimees = []
        
        # Traiter par lots pour optimiser
        BATCH_SIZE = 200
        total_lots = (len(factures_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n" + "=" * 60)
        print("SUPPRESSION DES FACTURES")
        print("=" * 60)
        print(f"\n🔄 Suppression de {len(factures_ids)} factures...")
        print(f"   Traitement par lots de {BATCH_SIZE} factures ({total_lots} lots)")
        print(f"   ⚠️  Cette opération est IRRÉVERSIBLE!\n")
        
        for lot_num in range(total_lots):
            debut = lot_num * BATCH_SIZE
            fin = min(debut + BATCH_SIZE, len(factures_ids))
            lot_ids = factures_ids[debut:fin]
            
            try:
                # Supprimer par lot avec unlink
                models.execute_kw(
                    db, uid, password,
                    'account.move',
                    'unlink',
                    [lot_ids]
                )
                
                # Récupérer les numéros des factures supprimées dans ce lot
                lot_numeros = [factures_map.get(fid, f'ID:{fid}') for fid in lot_ids]
                factures_supprimees.extend(lot_numeros)
                stats['succes'] += len(lot_ids)
                
                progress = (lot_num + 1) * 100 // total_lots
                print(f"   Lot {lot_num + 1}/{total_lots}: ✅ {len(lot_ids)} factures supprimées ({stats['succes']}/{len(factures_ids)} - {progress}%)")
                
                # Afficher les numéros de factures supprimées (premiers et derniers du lot)
                if len(lot_numeros) <= 10:
                    print(f"      Numéros: {', '.join(lot_numeros)}")
                else:
                    print(f"      Numéros: {', '.join(lot_numeros[:5])} ... {', '.join(lot_numeros[-5:])}")
                
            except Exception as e:
                print(f"\n      ⚠️  Erreur sur le lot {lot_num + 1}: {str(e)[:100]}")
                # Essayer par sous-lots plus petits en cas d'erreur
                SUB_BATCH = 50
                for sub_start in range(0, len(lot_ids), SUB_BATCH):
                    sub_end = min(sub_start + SUB_BATCH, len(lot_ids))
                    sub_lot = lot_ids[sub_start:sub_end]
                    try:
                        models.execute_kw(
                            db, uid, password,
                            'account.move',
                            'unlink',
                            [sub_lot]
                        )
                        sub_numeros = [factures_map.get(fid, f'ID:{fid}') for fid in sub_lot]
                        factures_supprimees.extend(sub_numeros)
                        stats['succes'] += len(sub_lot)
                    except Exception as e2:
                        # En dernier recours, essayer une par une
                        for facture_id in sub_lot:
                            try:
                                models.execute_kw(
                                    db, uid, password,
                                    'account.move',
                                    'unlink',
                                    [[facture_id]]
                                )
                                factures_supprimees.append(factures_map.get(facture_id, f'ID:{facture_id}'))
                                stats['succes'] += 1
                            except Exception as e3:
                                stats['echec'] += 1
                                print(f"         ❌ Échec ID {facture_id}: {str(e3)[:80]}")
            
            # Petite pause entre les lots
            if lot_num < total_lots - 1:
                time.sleep(0.3)
        
        # Vérification finale
        print(f"\n" + "=" * 60)
        print("VÉRIFICATION FINALE")
        print("=" * 60)
        
        # Recompter les factures restantes
        factures_restantes = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_invoice']]]
        )
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   ✅ Succès: {stats['succes']} factures supprimées")
        print(f"   ❌ Échecs: {stats['echec']} factures")
        print(f"   📊 Factures restantes: {factures_restantes}")
        
        if factures_restantes == 0:
            print(f"\n✅ CONFIRMATION: Toutes les factures clients ont été supprimées!")
        elif factures_restantes < stats['total']:
            print(f"\n✅ CONFIRMATION: {stats['succes']} factures ont été supprimées avec succès!")
            print(f"   Il reste {factures_restantes} factures (peut-être protégées ou verrouillées)")
        else:
            print(f"\n⚠️  ATTENTION: Aucune facture n'a été supprimée")
        
        # Afficher les numéros de factures supprimées
        if factures_supprimees:
            print(f"\n📄 NUMÉROS DES FACTURES SUPPRIMÉES ({len(factures_supprimees)} factures):")
            if len(factures_supprimees) <= 50:
                # Afficher toutes si moins de 50
                for i, numero in enumerate(factures_supprimees, 1):
                    print(f"   {i}. {numero}")
            else:
                # Afficher les 25 premières et 25 dernières
                print(f"   (Affichage des 25 premières et 25 dernières)")
                for i, numero in enumerate(factures_supprimees[:25], 1):
                    print(f"   {i}. {numero}")
                print(f"   ... ({len(factures_supprimees) - 50} factures au milieu) ...")
                for i, numero in enumerate(factures_supprimees[-25:], len(factures_supprimees) - 24):
                    print(f"   {i}. {numero}")
        
        return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la suppression des factures: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("⚠️  SUPPRESSION DE TOUTES LES FACTURES CLIENTS - TAL-migration")
    print("=" * 60)
    print("⚠️  ATTENTION: Cette opération est IRRÉVERSIBLE!")
    print()
    
    supprimer_toutes_factures_clients()
    
    print("\n" + "=" * 60)

