#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour supprimer tous les dossiers clients créés dans Factures clients
"""

from connexion_odoo import connecter_odoo

uid, models, db, password = connecter_odoo()

if not uid:
    print("❌ Impossible de se connecter à Odoo.")
    exit(1)

try:
    print("=" * 60)
    print("SUPPRESSION DES DOSSIERS CLIENTS")
    print("=" * 60)
    
    # 1. Trouver le dossier "Factures clients"
    print("\n🔍 Recherche du dossier 'Factures clients'...")
    factures_clients = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search',
        [[['name', '=', 'Factures clients'], ['type', '=', 'folder']]]
    )
    
    if not factures_clients:
        print("❌ Dossier 'Factures clients' non trouvé.")
        exit(1)
    
    factures_clients_id = factures_clients[0]
    print(f"✅ Dossier 'Factures clients' trouvé (ID: {factures_clients_id})")
    
    # 2. Trouver tous les dossiers clients dans "Factures clients"
    print("\n🔍 Recherche des dossiers clients...")
    dossiers_clients = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search_read',
        [[
            ['folder_id', '=', factures_clients_id],
            ['type', '=', 'folder']
        ]],
        {'fields': ['id', 'name']}
    )
    
    if not dossiers_clients:
        print("✅ Aucun dossier client à supprimer.")
        exit(0)
    
    print(f"📋 {len(dossiers_clients)} dossier(s) client trouvé(s):")
    for dossier in dossiers_clients:
        print(f"   - {dossier.get('name')} (ID: {dossier.get('id')})")
    
    # 3. Supprimer tous les dossiers clients
    print(f"\n🗑️  Suppression de {len(dossiers_clients)} dossier(s) client...")
    ids_a_supprimer = [d['id'] for d in dossiers_clients]
    
    try:
        models.execute_kw(
            db, uid, password,
            'documents.document',
            'unlink',
            [ids_a_supprimer]
        )
        print(f"✅ {len(ids_a_supprimer)} dossier(s) client supprimé(s) avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {str(e)}")
        # Essayer un par un
        print("\n🔄 Tentative de suppression un par un...")
        supprimes = 0
        for dossier_id in ids_a_supprimer:
            try:
                models.execute_kw(
                    db, uid, password,
                    'documents.document',
                    'unlink',
                    [[dossier_id]]
                )
                supprimes += 1
            except Exception as e2:
                print(f"   ⚠️  Erreur pour le dossier ID {dossier_id}: {str(e2)[:80]}")
        print(f"\n✅ {supprimes}/{len(ids_a_supprimer)} dossier(s) supprimé(s)")
    
    # 4. Vérification finale
    print("\n🔍 Vérification finale...")
    dossiers_restants = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search_count',
        [[
            ['folder_id', '=', factures_clients_id],
            ['type', '=', 'folder']
        ]]
    )
    
    if dossiers_restants == 0:
        print("✅ Tous les dossiers clients ont été supprimés!")
    else:
        print(f"⚠️  Il reste {dossiers_restants} dossier(s) client.")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ Erreur fatale: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

