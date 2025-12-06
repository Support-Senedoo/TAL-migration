#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier les modèles disponibles dans le module documents
"""

from connexion_odoo import connecter_odoo

uid, models, db, password = connecter_odoo()

if uid:
    # Chercher tous les modèles qui commencent par "documents."
    modeles_docs = models.execute_kw(
        db, uid, password,
        'ir.model', 'search_read',
        [[['model', 'like', 'documents.%']]],
        {'fields': ['name', 'model']}
    )
    
    print("Modeles disponibles dans le module documents:")
    for modele in modeles_docs:
        print(f"  - {modele['model']}: {modele['name']}")
        
    # Chercher aussi les champs de documents.document pour voir comment lier aux dossiers
    try:
        champs_doc = models.execute_kw(
            db, uid, password,
            'ir.model.fields', 'search_read',
            [[['model', '=', 'documents.document']]],
            {'fields': ['name', 'field_description', 'relation', 'ttype']}
        )
        
        print("\nChamps de documents.document (pertinents pour les dossiers):")
        for champ in champs_doc:
            if any(mot in champ['name'].lower() for mot in ['folder', 'directory', 'type', 'is_folder', 'parent']):
                print(f"  - {champ['name']}: {champ['field_description']} (type: {champ.get('ttype', 'N/A')}, relation: {champ.get('relation', 'N/A')})")
        
        # Chercher un exemple de dossier existant
        print("\nRecherche d'un dossier existant:")
        dossiers = models.execute_kw(
            db, uid, password,
            'documents.document', 'search_read',
            [[['type', '=', 'folder']]],
            {'fields': ['name', 'type', 'folder_id'], 'limit': 5}
        )
        if dossiers:
            print(f"  {len(dossiers)} dossier(s) trouve(s):")
            for d in dossiers:
                print(f"    - {d.get('name')} (ID: {d.get('id')}, type: {d.get('type')})")
        else:
            print("  Aucun dossier trouve avec type='folder'")
            
    except Exception as e:
        print(f"Erreur: {e}")

