#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC D'UNE FACTURE SPÉCIFIQUE
====================================

Ce script permet de diagnostiquer pourquoi une facture spécifique bloque.
"""

import sys
from connexion_odoo import connecter_odoo
from transferer_factures_documents_v2 import (
    identifier_modele_pdf,
    generer_pdf_facture_http,
    obtenir_ou_creer_dossier_finance,
    obtenir_ou_creer_dossier_client
)

def diagnostiquer_facture(numero_facture):
    """Diagnostique une facture spécifique."""
    print("=" * 80)
    print(f"🔍 DIAGNOSTIC DE LA FACTURE: {numero_facture}")
    print("=" * 80)
    print()
    
    # Connexion
    print("1️⃣  Connexion à Odoo...")
    try:
        uid, models, db, password = connecter_odoo()
        if not uid:
            print("❌ Erreur de connexion")
            return False
        print("✅ Connecté avec succès")
        print()
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Chercher la facture
    print(f"2️⃣  Recherche de la facture '{numero_facture}'...")
    try:
        factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_read',
            [[['name', '=', numero_facture], ['move_type', '=', 'out_invoice']]],
            {'fields': ['id', 'name', 'partner_id', 'state', 'invoice_date']}
        )
        
        if not factures:
            print(f"❌ Facture '{numero_facture}' non trouvée")
            return False
        
        facture = factures[0]
        facture_id = facture['id']
        partner_info = facture.get('partner_id', [])
        partner_id = partner_info[0] if partner_info else None
        partner_name = partner_info[1] if len(partner_info) > 1 else 'Inconnu'
        
        print(f"✅ Facture trouvée:")
        print(f"   - ID: {facture_id}")
        print(f"   - Numéro: {facture.get('name')}")
        print(f"   - Client: {partner_name} (ID: {partner_id})")
        print(f"   - État: {facture.get('state')}")
        print(f"   - Date: {facture.get('invoice_date')}")
        print()
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        return False
    
    # Vérifier le client
    print("3️⃣  Vérification du client...")
    if not partner_id:
        print("❌ Pas de client associé à la facture")
        return False
    print(f"✅ Client: {partner_name} (ID: {partner_id})")
    print()
    
    # Vérifier le dossier client
    print("4️⃣  Vérification/création du dossier client...")
    try:
        dossier_id = obtenir_ou_creer_dossier_client(
            models, db, uid, password, partner_name, partner_id
        )
        if dossier_id:
            print(f"✅ Dossier client OK (ID: {dossier_id})")
        else:
            print("❌ Impossible de créer/obtenir le dossier client")
            return False
        print()
    except Exception as e:
        print(f"❌ Erreur dossier client: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Identifier le modèle PDF
    print("5️⃣  Identification du modèle PDF...")
    try:
        report_id, report_name = identifier_modele_pdf(models, db, uid, password, facture_id)
        if report_id and report_name:
            print(f"✅ Modèle PDF trouvé:")
            print(f"   - ID: {report_id}")
            print(f"   - Nom: {report_name}")
        else:
            print("⚠️  Modèle PDF non trouvé, utilisation du modèle par défaut")
            report_name = 'account.report_invoice'
        print()
    except Exception as e:
        print(f"❌ Erreur identification modèle: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Générer le PDF (avec timeout)
    print("6️⃣  Génération du PDF (test avec timeout de 60 secondes)...")
    import signal
    
    class TimeoutError(Exception):
        pass
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Timeout dépassé")
    
    try:
        # Définir un timeout de 60 secondes
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(60)  # 60 secondes
        
        contenu_pdf = generer_pdf_facture_http(facture_id, report_name, models, db, password)
        
        signal.alarm(0)  # Annuler le timeout
        
        if contenu_pdf:
            taille = len(contenu_pdf) / 1024  # KB
            print(f"✅ PDF généré avec succès ({taille:.2f} KB)")
        else:
            print("❌ Impossible de générer le PDF")
            return False
        print()
    except TimeoutError:
        signal.alarm(0)
        print("❌ TIMEOUT: La génération du PDF dépasse 60 secondes")
        print("   → C'est probablement la cause du blocage")
        return False
    except Exception as e:
        signal.alarm(0)
        print(f"❌ Erreur génération PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Vérifier si le document existe déjà
    print("7️⃣  Vérification si le document existe déjà...")
    try:
        documents_existants = models.execute_kw(
            db, uid, password,
            'documents.document',
            'search',
            [[
                ['res_model', '=', 'account.move'],
                ['res_id', '=', facture_id],
                ['folder_id', '=', dossier_id]
            ]]
        )
        
        if documents_existants:
            print(f"⚠️  Document déjà existant (ID: {documents_existants[0]})")
        else:
            print("✅ Aucun document existant, prêt pour la création")
        print()
    except Exception as e:
        print(f"⚠️  Erreur vérification document: {e}")
        print()
    
    print("=" * 80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("=" * 80)
    print()
    print("📋 RÉSUMÉ:")
    print(f"   - Facture ID: {facture_id}")
    print(f"   - Client: {partner_name}")
    print(f"   - Dossier: {dossier_id}")
    print(f"   - Modèle PDF: {report_name}")
    print(f"   - PDF généré: {'✅ Oui' if contenu_pdf else '❌ Non'}")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnostiquer_facture.py <NUMERO_FACTURE>")
        print("Exemple: python diagnostiquer_facture.py FAC/2025/TAL0000272")
        sys.exit(1)
    
    numero_facture = sys.argv[1]
    diagnostiquer_facture(numero_facture)

