#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour vérifier la structure des dossiers Documents
"""

from connexion_odoo import connecter_odoo

uid, models, db, password = connecter_odoo()

if uid:
    print("=" * 60)
    print("DIAGNOSTIC DES DOSSIERS DOCUMENTS")
    print("=" * 60)
    
    # 1. Chercher tous les champs du modèle documents.document
    print("\n1. Champs du modèle documents.document:")
    try:
        champs = models.execute_kw(
            db, uid, password,
            'ir.model.fields', 'search_read',
            [[['model', '=', 'documents.document']]],
            {'fields': ['name', 'field_description', 'ttype', 'required', 'readonly']}
        )
        
        champs_importants = [c for c in champs if any(mot in c['name'].lower() for mot in 
            ['folder', 'type', 'name', 'root', 'parent', 'tag', 'owner', 'company'])]
        
        for champ in champs_importants:
            req = "REQUIRED" if champ.get('required') else ""
            ro = "READONLY" if champ.get('readonly') else ""
            print(f"   - {champ['name']}: {champ['field_description']} ({champ.get('ttype', 'N/A')}) {req} {ro}")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # 2. Chercher un dossier existant et voir sa structure complète
    print("\n2. Structure d'un dossier existant:")
    try:
        dossiers = models.execute_kw(
            db, uid, password,
            'documents.document', 'search_read',
            [[['type', '=', 'folder']]],
            {'fields': [], 'limit': 1}
        )
        
        if dossiers:
            dossier = dossiers[0]
            print(f"   Dossier trouvé: {dossier.get('name', 'N/A')} (ID: {dossier.get('id')})")
            print(f"   Champs disponibles:")
            for key, value in sorted(dossier.items()):
                if key != 'id':
                    print(f"      - {key}: {value}")
        else:
            print("   Aucun dossier trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # 3. Chercher spécifiquement Finance et Factures clients
    print("\n3. Recherche des dossiers Finance et Factures clients:")
    try:
        finance = models.execute_kw(
            db, uid, password,
            'documents.document', 'search_read',
            [[['name', '=', 'Finance'], ['type', '=', 'folder']]],
            {'fields': [], 'limit': 1}
        )
        
        if finance:
            print(f"   Finance trouvé (ID: {finance[0].get('id')})")
            print(f"   Champs: {list(finance[0].keys())}")
        else:
            print("   Finance non trouvé")
        
        factures = models.execute_kw(
            db, uid, password,
            'documents.document', 'search_read',
            [[['name', 'ilike', 'Factures'], ['type', '=', 'folder']]],
            {'fields': [], 'limit': 5}
        )
        
        if factures:
            print(f"   {len(factures)} dossier(s) 'Factures' trouvé(s):")
            for f in factures:
                print(f"      - {f.get('name')} (ID: {f.get('id')}, folder_id: {f.get('folder_id')})")
        else:
            print("   Aucun dossier 'Factures' trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # 4. Vérifier les dossiers clients créés
    print("\n4. Dossiers clients dans Factures clients:")
    try:
        factures_clients = models.execute_kw(
            db, uid, password,
            'documents.document', 'search',
            [[['name', '=', 'Factures clients'], ['type', '=', 'folder']]]
        )
        
        if factures_clients:
            factures_clients_id = factures_clients[0]
            clients = models.execute_kw(
                db, uid, password,
                'documents.document', 'search_read',
                [[['folder_id', '=', factures_clients_id], ['type', '=', 'folder']]],
                {'fields': ['name', 'folder_id', 'type'], 'limit': 5}
            )
            
            if clients:
                print(f"   {len(clients)} dossier(s) client trouvé(s):")
                for c in clients:
                    print(f"      - {c.get('name')} (ID: {c.get('id')}, folder_id: {c.get('folder_id')})")
            else:
                print("   Aucun dossier client trouvé")
        else:
            print("   Dossier 'Factures clients' non trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print("\n" + "=" * 60)


