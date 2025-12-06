#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'IDENTIFICATION DES MODÈLES DE FACTURES CLIENTS
========================================================

Ce script identifie les modèles de factures clients disponibles en PDF
dans la base Odoo.

Auteur: Assistant IA
Date: 2025-11-29
"""

from connexion_odoo import connecter_odoo
import sys

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def identifier_modeles_factures():
    """
    Identifie les modèles de factures clients disponibles en PDF.
    """
    print("=" * 60)
    print("IDENTIFICATION DES MODELES DE FACTURES CLIENTS")
    print("=" * 60)
    
    # Connexion à Odoo
    print(f"\nConnexion a Odoo...")
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("Impossible de se connecter a Odoo.")
        return False
    
    try:
        # Rechercher les rapports liés aux factures clients
        print(f"\nRecherche des modeles de factures...")
        
        # Méthode 1: Rechercher dans ir.actions.report
        print(f"\n1. Recherche dans ir.actions.report...")
        reports = models.execute_kw(
            db, uid, password,
            'ir.actions.report', 'search_read',
            [[['model', '=', 'account.move'], ['report_type', 'in', ['qweb-pdf', 'qweb-text']]]],
            {'fields': ['id', 'name', 'report_name', 'report_type', 'model', 'binding_model_id', 'binding_type']}
        )
        
        print(f"   {len(reports)} rapports trouves pour account.move")
        
        if reports:
            print(f"\n   Modeles de factures trouves:")
            for i, report in enumerate(reports, 1):
                print(f"\n   {i}. {report.get('name', 'N/A')}")
                print(f"      - ID: {report.get('id')}")
                print(f"      - Nom technique: {report.get('report_name', 'N/A')}")
                print(f"      - Type: {report.get('report_type', 'N/A')}")
                print(f"      - Modele: {report.get('model', 'N/A')}")
                if report.get('binding_model_id'):
                    print(f"      - Modele lie: {report.get('binding_model_id')[1]}")
                
                # Essayer de récupérer plus d'informations sur le rapport
                try:
                    report_details = models.execute_kw(
                        db, uid, password,
                        'ir.actions.report', 'read',
                        [[report.get('id')]],
                        {'fields': ['paperformat_id', 'print_report_name', 'groups_id']}
                    )
                    if report_details:
                        details = report_details[0]
                        if details.get('paperformat_id'):
                            print(f"      - Format papier: {details.get('paperformat_id')[1]}")
                        if details.get('print_report_name'):
                            print(f"      - Nom impression: {details.get('print_report_name')}")
                except:
                    pass
        
        # Méthode 2: Rechercher les templates QWeb pour les factures
        print(f"\n2. Recherche des templates QWeb pour les factures...")
        templates = models.execute_kw(
            db, uid, password,
            'ir.ui.view', 'search_read',
            [[['model', '=', 'account.move'], ['type', '=', 'qweb'], ['name', 'ilike', 'invoice']]],
            {'fields': ['id', 'name', 'key', 'arch_db', 'model']}
        )
        
        print(f"   {len(templates)} templates QWeb trouves")
        
        if templates:
            print(f"\n   Templates QWeb trouves:")
            for i, template in enumerate(templates[:10], 1):  # Limiter à 10 pour l'affichage
                print(f"\n   {i}. {template.get('name', 'N/A')}")
                print(f"      - ID: {template.get('id')}")
                print(f"      - Cle: {template.get('key', 'N/A')}")
        
        # Méthode 3: Rechercher spécifiquement les rapports de factures clients
        print(f"\n3. Recherche specifique des rapports de factures clients...")
        invoice_reports = models.execute_kw(
            db, uid, password,
            'ir.actions.report', 'search_read',
            [[['model', '=', 'account.move'], ['report_name', 'ilike', 'invoice']]],
            {'fields': ['id', 'name', 'report_name', 'report_type', 'model']}
        )
        
        print(f"   {len(invoice_reports)} rapports de factures trouves")
        
        if invoice_reports:
            print(f"\n   Rapports de factures detailles:")
            for i, report in enumerate(invoice_reports, 1):
                print(f"\n   {i}. {report.get('name', 'N/A')}")
                print(f"      - ID: {report.get('id')}")
                print(f"      - Nom technique: {report.get('report_name', 'N/A')}")
                print(f"      - Type: {report.get('report_type', 'N/A')}")
        
        # Méthode 4: Rechercher les modèles de documents (account.move.line)
        print(f"\n4. Recherche des modeles de documents comptables...")
        doc_models = models.execute_kw(
            db, uid, password,
            'ir.actions.report', 'search_read',
            [[['model', 'in', ['account.move', 'account.invoice']]]],
            {'fields': ['id', 'name', 'report_name', 'report_type', 'model']}
        )
        
        print(f"   {len(doc_models)} modeles de documents comptables trouves")
        
        # Tester les modèles sur une facture client réelle
        print(f"\n5. Test des modeles sur une facture client reelle...")
        factures_clients = models.execute_kw(
            db, uid, password,
            'account.move', 'search',
            [[['move_type', '=', 'out_invoice']]],
            {'limit': 1}
        )
        
        if factures_clients:
            facture_id = factures_clients[0]
            facture_info = models.execute_kw(
                db, uid, password,
                'account.move', 'read',
                [[facture_id]],
                {'fields': ['name', 'move_type', 'state']}
            )
            
            if facture_info:
                print(f"   Facture test: {facture_info[0].get('name')} (ID: {facture_id})")
                print(f"   Type: {facture_info[0].get('move_type')}")
                print(f"   Etat: {facture_info[0].get('state')}")
                
                # Tester chaque modèle
                print(f"\n   Test de chaque modele:")
                modeles_valides = []
                for report in reports:
                    report_id = report.get('id')
                    report_name = report.get('name', 'N/A')
                    report_tech = report.get('report_name', 'N/A')
                    
                    try:
                        # Essayer de générer le PDF (sans vraiment le générer, juste vérifier l'accès)
                        # On peut juste vérifier si le rapport existe et est accessible
                        report_check = models.execute_kw(
                            db, uid, password,
                            'ir.actions.report', 'read',
                            [[report_id]],
                            {'fields': ['id', 'name', 'model']}
                        )
                        
                        if report_check:
                            modeles_valides.append({
                                'id': report_id,
                                'name': report_name,
                                'tech_name': report_tech,
                                'accessible': True
                            })
                            print(f"      OK: {report_name} (ID: {report_id})")
                    except Exception as e:
                        print(f"      ERREUR: {report_name} - {str(e)[:60]}")
        
        # Résumé
        print(f"\n" + "=" * 60)
        print("RESUME")
        print("=" * 60)
        print(f"\nTotal de modeles de factures identifies:")
        print(f"   - Rapports account.move: {len(reports)}")
        print(f"   - Templates QWeb: {len(templates)}")
        print(f"   - Rapports specifiques factures: {len(invoice_reports)}")
        print(f"   - Modeles documents comptables: {len(doc_models)}")
        
        # Lister les noms de tous les rapports uniques avec leurs IDs
        print(f"\nListe complete des modeles disponibles:")
        seen_names = {}
        for report in reports:
            name = report.get('name', 'N/A')
            report_id = report.get('id')
            tech_name = report.get('report_name', 'N/A')
            
            if name not in seen_names:
                seen_names[name] = []
            seen_names[name].append({
                'id': report_id,
                'tech_name': tech_name
            })
        
        for i, (name, versions) in enumerate(sorted(seen_names.items()), 1):
            print(f"\n   {i}. {name}")
            for version in versions:
                print(f"      - ID: {version['id']}, Nom technique: {version['tech_name']}")
        
        return True
        
    except Exception as e:
        print(f"\nErreur lors de l'identification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    identifier_modeles_factures()
    
    print("\n" + "=" * 60)

