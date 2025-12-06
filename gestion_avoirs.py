#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE GESTION DES AVOIRS CLIENTS
=====================================

Ce script met tous les avoirs clients en brouillon puis les supprime.
⚠️  ATTENTION: La suppression est IRRÉVERSIBLE!

Auteur: Assistant IA
Date: 2025-11-29
"""

from connexion_odoo import connecter_odoo
import time

def mettre_avoirs_en_brouillon_et_supprimer():
    """
    Met tous les avoirs clients en brouillon puis les supprime.
    ⚠️  OPÉRATION IRRÉVERSIBLE!
    """
    # Connexion à Odoo
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    try:
        print("\n" + "=" * 60)
        print("GESTION DES AVOIRS CLIENTS")
        print("=" * 60)
        
        # Compter d'abord le nombre total d'avoirs clients
        total_avoirs = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_refund']]]
        )
        
        print(f"\n📊 Nombre total d'avoirs clients: {total_avoirs}")
        
        if total_avoirs == 0:
            print("✅ Aucun avoir client à traiter.")
            return True
        
        # Récupérer tous les avoirs clients
        print(f"\n🔍 Récupération des avoirs...")
        avoirs = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_read',
            [[['move_type', '=', 'out_refund']]],
            {
                'fields': ['id', 'name', 'state', 'partner_id', 'amount_total', 'invoice_date'],
                'order': 'id asc'
            }
        )
        
        print(f"✅ {len(avoirs)} avoirs récupérés")
        
        # Statistiques initiales
        stats = {
            'total': len(avoirs),
            'deja_brouillon': 0,
            'posted': 0,
            'cancel': 0,
            'autres': 0,
            'mis_brouillon': 0,
            'supprimes': 0,
            'echec': 0
        }
        
        # Créer un mapping ID -> numéro
        avoirs_map = {}
        avoirs_ids = []
        
        # Afficher les premiers avoirs
        print(f"\n📄 Premiers avoirs trouvés:")
        for i, avoir in enumerate(avoirs[:10], 1):
            avoir_numero = avoir.get('name', 'N/A')
            avoir_etat = avoir.get('state', 'N/A')
            avoir_partner = avoir.get('partner_id', ['N/A', 'N/A'])[1] if avoir.get('partner_id') else 'N/A'
            print(f"   {i}. {avoir_numero} - {avoir_etat} - {avoir_partner}")
        
        if len(avoirs) > 10:
            print(f"   ... et {len(avoirs) - 10} autres avoirs")
        
        # Analyser les états et préparer la liste
        for avoir in avoirs:
            avoir_id = avoir['id']
            avoir_numero = avoir.get('name', f'ID:{avoir_id}')
            avoir_etat = avoir.get('state', 'N/A')
            
            avoirs_map[avoir_id] = avoir_numero
            
            # Compter par état
            if avoir_etat == 'draft':
                stats['deja_brouillon'] += 1
            elif avoir_etat == 'posted':
                stats['posted'] += 1
            elif avoir_etat == 'cancel':
                stats['cancel'] += 1
            else:
                stats['autres'] += 1
            
            # Tous les avoirs seront traités (même ceux déjà en brouillon)
            avoirs_ids.append(avoir_id)
        
        print(f"\n📊 Répartition par état:")
        print(f"   ✅ Déjà en brouillon: {stats['deja_brouillon']}")
        print(f"   📝 Validés (posted): {stats['posted']}")
        print(f"   ❌ Annulés (cancel): {stats['cancel']}")
        print(f"   🔄 Autres états: {stats['autres']}")
        print(f"   📋 Total à traiter: {len(avoirs_ids)}")
        
        if not avoirs_ids:
            print(f"\n✅ Aucun avoir à traiter!")
            return True
        
        # =====================================================================
        # ÉTAPE 1: Mettre en brouillon
        # =====================================================================
        print(f"\n" + "=" * 60)
        print("ÉTAPE 1: MISE EN BROUILLON")
        print("=" * 60)
        
        # Identifier ceux qui ne sont pas déjà en brouillon
        avoirs_a_mettre_brouillon = []
        for avoir in avoirs:
            if avoir.get('state', '') != 'draft':
                avoirs_a_mettre_brouillon.append(avoir['id'])
        
        if avoirs_a_mettre_brouillon:
            print(f"\n🔄 Mise en brouillon de {len(avoirs_a_mettre_brouillon)} avoirs...")
            
            BATCH_SIZE = 200
            total_lots = (len(avoirs_a_mettre_brouillon) + BATCH_SIZE - 1) // BATCH_SIZE
            
            for lot_num in range(total_lots):
                debut = lot_num * BATCH_SIZE
                fin = min(debut + BATCH_SIZE, len(avoirs_a_mettre_brouillon))
                lot_ids = avoirs_a_mettre_brouillon[debut:fin]
                
                try:
                    models.execute_kw(
                        db, uid, password,
                        'account.move',
                        'write',
                        [lot_ids, {'state': 'draft'}]
                    )
                    stats['mis_brouillon'] += len(lot_ids)
                    progress = (lot_num + 1) * 100 // total_lots
                    print(f"   Lot {lot_num + 1}/{total_lots}: ✅ {len(lot_ids)} avoirs mis en brouillon ({stats['mis_brouillon']}/{len(avoirs_a_mettre_brouillon)} - {progress}%)")
                except Exception as e:
                    print(f"   ⚠️  Erreur sur le lot {lot_num + 1}: {str(e)[:100]}")
                    # Essayer un par un
                    for avoir_id in lot_ids:
                        try:
                            models.execute_kw(
                                db, uid, password,
                                'account.move',
                                'write',
                                [[avoir_id], {'state': 'draft'}]
                            )
                            stats['mis_brouillon'] += 1
                        except:
                            pass
                
                if lot_num < total_lots - 1:
                    time.sleep(0.2)
        else:
            print(f"\n✅ Tous les avoirs sont déjà en brouillon")
        
        # =====================================================================
        # ÉTAPE 2: Supprimer
        # =====================================================================
        print(f"\n" + "=" * 60)
        print("ÉTAPE 2: SUPPRESSION")
        print("=" * 60)
        print(f"⚠️  ATTENTION: Cette opération est IRRÉVERSIBLE!\n")
        
        avoirs_supprimes = []
        
        BATCH_SIZE = 200
        total_lots = (len(avoirs_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"🔄 Suppression de {len(avoirs_ids)} avoirs...")
        print(f"   Traitement par lots de {BATCH_SIZE} avoirs ({total_lots} lots)\n")
        
        for lot_num in range(total_lots):
            debut = lot_num * BATCH_SIZE
            fin = min(debut + BATCH_SIZE, len(avoirs_ids))
            lot_ids = avoirs_ids[debut:fin]
            
            try:
                # Supprimer par lot avec unlink
                models.execute_kw(
                    db, uid, password,
                    'account.move',
                    'unlink',
                    [lot_ids]
                )
                
                # Récupérer les numéros des avoirs supprimés dans ce lot
                lot_numeros = [avoirs_map.get(aid, f'ID:{aid}') for aid in lot_ids]
                avoirs_supprimes.extend(lot_numeros)
                stats['supprimes'] += len(lot_ids)
                
                progress = (lot_num + 1) * 100 // total_lots
                print(f"   Lot {lot_num + 1}/{total_lots}: ✅ {len(lot_ids)} avoirs supprimés ({stats['supprimes']}/{len(avoirs_ids)} - {progress}%)")
                
                # Afficher les numéros d'avoirs supprimés
                if len(lot_numeros) <= 10:
                    print(f"      Numéros: {', '.join(lot_numeros)}")
                else:
                    print(f"      Numéros: {', '.join(lot_numeros[:5])} ... {', '.join(lot_numeros[-5:])}")
                
            except Exception as e:
                print(f"\n      ⚠️  Erreur sur le lot {lot_num + 1}: {str(e)[:100]}")
                # Essayer par sous-lots plus petits
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
                        sub_numeros = [avoirs_map.get(aid, f'ID:{aid}') for aid in sub_lot]
                        avoirs_supprimes.extend(sub_numeros)
                        stats['supprimes'] += len(sub_lot)
                    except Exception as e2:
                        # En dernier recours, essayer un par un
                        for avoir_id in sub_lot:
                            try:
                                models.execute_kw(
                                    db, uid, password,
                                    'account.move',
                                    'unlink',
                                    [[avoir_id]]
                                )
                                avoirs_supprimes.append(avoirs_map.get(avoir_id, f'ID:{avoir_id}'))
                                stats['supprimes'] += 1
                            except Exception as e3:
                                stats['echec'] += 1
                                print(f"         ❌ Échec ID {avoir_id}: {str(e3)[:80]}")
            
            if lot_num < total_lots - 1:
                time.sleep(0.3)
        
        # Vérification finale
        print(f"\n" + "=" * 60)
        print("VÉRIFICATION FINALE")
        print("=" * 60)
        
        # Recompter les avoirs restants
        avoirs_restants = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_refund']]]
        )
        
        print(f"\n📊 RÉSULTATS:")
        print(f"   📝 Mis en brouillon: {stats['mis_brouillon']} avoirs")
        print(f"   ✅ Supprimés: {stats['supprimes']} avoirs")
        print(f"   ❌ Échecs: {stats['echec']} avoirs")
        print(f"   📊 Avoirs restants: {avoirs_restants}")
        
        if avoirs_restants == 0:
            print(f"\n✅ CONFIRMATION: Tous les avoirs clients ont été supprimés!")
        elif avoirs_restants < stats['total']:
            print(f"\n✅ CONFIRMATION: {stats['supprimes']} avoirs ont été supprimés avec succès!")
            print(f"   Il reste {avoirs_restants} avoirs (peut-être protégés ou verrouillés)")
        else:
            print(f"\n⚠️  ATTENTION: Aucun avoir n'a été supprimé")
        
        # Afficher les numéros d'avoirs supprimés
        if avoirs_supprimes:
            print(f"\n📄 NUMÉROS DES AVOIRS SUPPRIMÉS ({len(avoirs_supprimes)} avoirs):")
            if len(avoirs_supprimes) <= 50:
                for i, numero in enumerate(avoirs_supprimes, 1):
                    print(f"   {i}. {numero}")
            else:
                print(f"   (Affichage des 25 premiers et 25 derniers)")
                for i, numero in enumerate(avoirs_supprimes[:25], 1):
                    print(f"   {i}. {numero}")
                print(f"   ... ({len(avoirs_supprimes) - 50} avoirs au milieu) ...")
                for i, numero in enumerate(avoirs_supprimes[-25:], len(avoirs_supprimes) - 24):
                    print(f"   {i}. {numero}")
        
        return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la gestion des avoirs: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("GESTION DES AVOIRS CLIENTS - TAL-migration")
    print("=" * 60)
    print("⚠️  ATTENTION: La suppression est IRRÉVERSIBLE!")
    print()
    
    mettre_avoirs_en_brouillon_et_supprimer()
    
    print("\n" + "=" * 60)








