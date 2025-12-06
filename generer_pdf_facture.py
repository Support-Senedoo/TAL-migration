#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE GÉNÉRATION DE PDF DE FACTURE
=======================================

Ce script trouve une facture client contenant une ligne "transfert"
et génère son PDF avec le modèle "Factures Transferts".

Auteur: Assistant IA
Date: 2025-11-29
"""

from connexion_odoo import connecter_odoo
import base64
import sys
from pathlib import Path
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def recuperer_factures_clients(limit=100):
    """
    Récupère les premières factures clients.
    
    Args:
        limit: Nombre maximum de factures à récupérer (défaut: 100)
    
    Returns:
        tuple: (liste de factures, models, db, password) ou (None, None, None, None) en cas d'erreur
    """
    print("=" * 60)
    print(f"RECUPERATION DES {limit} PREMIERES FACTURES CLIENTS")
    print("=" * 60)
    
    # Connexion à Odoo
    print(f"\nConnexion a Odoo...")
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("Impossible de se connecter a Odoo.")
        return None, None, None, None
    
    try:
        # Rechercher les factures clients
        print(f"\nRecherche des factures clients...")
        factures = models.execute_kw(
            db, uid, password,
            'account.move', 'search_read',
            [[['move_type', '=', 'out_invoice']]],
            {
                'fields': ['id', 'name', 'partner_id', 'invoice_date', 'amount_total'],
                'limit': limit,
                'order': 'id asc'
            }
        )
        
        print(f"   {len(factures)} factures clients trouvees")
        
        if not factures:
            print("   Aucune facture client trouvee")
            return None, None, None, None
        
        return factures, models, db, password
        
    except Exception as e:
        print(f"Erreur lors de la recherche: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None, None


def generer_pdf_facture(facture_id, models, db, password, report_id=988):
    """
    Génère le PDF d'une facture avec un modèle spécifique.
    
    Args:
        facture_id: ID de la facture
        models: Proxy XML-RPC pour les modèles
        db: Nom de la base de données
        password: Mot de passe
        report_id: ID du modèle de rapport (988 = Factures Transferts)
    """
    print(f"\n" + "=" * 60)
    print("GENERATION DU PDF")
    print("=" * 60)
    
    try:
        print(f"\nGeneration du PDF pour la facture ID: {facture_id}")
        print(f"Modele utilise: Factures Transferts (ID: {report_id})")
        
        # Récupérer l'UID pour l'appel
        from connexion_odoo import connecter_odoo
        uid, _, _, _ = connecter_odoo()
        
        if not uid:
            print("Erreur: Impossible de recuperer l'UID")
            return None
        
        # Récupérer les informations du rapport
        report = models.execute_kw(
            db, uid, password,
            'ir.actions.report', 'read',
            [[report_id]],
            {'fields': ['id', 'name', 'report_name']}
        )
        
        if not report:
            print("Erreur: Rapport non trouve")
            return None
        
        report_name = report[0]['report_name']
        print(f"   Nom technique du rapport: {report_name}")
        
        # Utiliser requests pour gérer la session et télécharger le PDF
        from config import ODOO_CONFIG
        
        try:
            print(f"   Generation du PDF via URL HTTP avec authentification...")
            
            # Créer une session requests
            session = requests.Session()
            
            # Configurer les retries
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            # Étape 1: Obtenir le token CSRF
            login_page_url = f"{ODOO_CONFIG['URL']}web/login"
            print(f"   Obtention du token CSRF...")
            login_page = session.get(login_page_url, verify=False)
            
            # Extraire le token CSRF depuis la page
            import re
            csrf_token_match = re.search(r'name="csrf_token"\s+value="([^"]+)"', login_page.text)
            if not csrf_token_match:
                # Essayer une autre méthode pour obtenir le token
                csrf_token_match = re.search(r'"csrf_token":\s*"([^"]+)"', login_page.text)
            
            csrf_token = csrf_token_match.group(1) if csrf_token_match else None
            
            if not csrf_token:
                print(f"   Avertissement: Token CSRF non trouve, tentative sans token...")
            
            # Étape 2: Se connecter
            login_url = f"{ODOO_CONFIG['URL']}web/login"
            login_data = {
                'login': ODOO_CONFIG['USER'],
                'password': ODOO_CONFIG['PASS'],
                'db': db,
            }
            if csrf_token:
                login_data['csrf_token'] = csrf_token
            
            print(f"   Authentification via session...")
            login_response = session.post(login_url, data=login_data, verify=False, allow_redirects=True)
            
            # Vérifier que la connexion a réussi
            if 'login' in login_response.url.lower() or login_response.status_code != 200:
                print(f"   Erreur: Echec de l'authentification (status: {login_response.status_code})")
                return None
            
            # Étape 3: Générer le PDF avec la session authentifiée
            pdf_url = f"{ODOO_CONFIG['URL']}report/pdf/{report_name}/{facture_id}"
            print(f"   Telechargement du PDF depuis: {pdf_url}")
            
            pdf_response = session.get(pdf_url, verify=False)
            pdf_content = pdf_response.content
            
            # Vérifier que c'est bien un PDF (commence par %PDF)
            if not pdf_content.startswith(b'%PDF'):
                # Si ce n'est pas un PDF, c'est probablement une page HTML d'erreur
                error_text = pdf_content[:500].decode('utf-8', errors='ignore')
                print(f"   Erreur: Le contenu n'est pas un PDF valide")
                print(f"   Status code: {pdf_response.status_code}")
                print(f"   Contenu recu: {error_text[:200]}")
                return None
            
            if not pdf_content or len(pdf_content) < 100:
                print(f"   Erreur: PDF vide ou invalide (taille: {len(pdf_content) if pdf_content else 0})")
                return None
            
            print(f"   PDF genere avec succes ({len(pdf_content)} octets)")
            
        except Exception as e:
            print(f"   Erreur lors de la generation du PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        # Récupérer les informations de la facture (nom et partenaire)
        facture_info = models.execute_kw(
            db, uid, password,
            'account.move', 'read',
            [[facture_id]],
            {'fields': ['name', 'partner_id']}
        )
        
        if not facture_info:
            print("Erreur: Impossible de recuperer les informations de la facture")
            return None
        
        numero_facture = facture_info[0].get('name', f'FACTURE_{facture_id}')
        partner_id = facture_info[0].get('partner_id')
        partner_name = partner_id[1] if partner_id else 'Client_Inconnu'
        
        # Nettoyer le numéro pour qu'il soit valide comme nom de fichier
        import re
        numero_facture_clean = re.sub(r'[<>:"/\\|?*]', '_', numero_facture)
        nom_fichier = f"{numero_facture_clean}.pdf"
        
        # Sauvegarder le PDF localement
        chemin_fichier = Path(__file__).parent / nom_fichier
        with open(chemin_fichier, 'wb') as f:
            f.write(pdf_content)
        
        print(f"\nPDF genere avec succes!")
        print(f"   Fichier local: {chemin_fichier}")
        print(f"   Taille: {len(pdf_content)} octets")
        
        # Créer le dossier dans le module Document et y mettre la facture
        print(f"\nUpload dans le module Document...")
        print(f"   Client: {partner_name}")
        
        try:
            # Les dossiers sont des documents avec type='folder'
            # 1. Chercher le dossier parent "Finance"
            print(f"   Recherche du dossier parent 'Finance'...")
            finance_ids = models.execute_kw(
                db, uid, password,
                'documents.document', 'search',
                [[['name', '=', 'Finance'], ['type', '=', 'folder']]]
            )
            
            if not finance_ids:
                print(f"   Erreur: Le dossier 'Finance' n'existe pas")
                raise Exception("Dossier 'Finance' introuvable")
            
            finance_id = finance_ids[0]
            print(f"   Dossier 'Finance' trouve (ID: {finance_id})")
            
            # 2. Chercher ou créer le sous-dossier "Factures Clients" dans "Finance"
            print(f"   Recherche du sous-dossier 'Factures Clients'...")
            factures_clients_ids = models.execute_kw(
                db, uid, password,
                'documents.document', 'search',
                [[['name', '=', 'Factures Clients'], ['type', '=', 'folder'], ['folder_id', '=', finance_id]]]
            )
            
            if factures_clients_ids:
                factures_clients_id = factures_clients_ids[0]
                print(f"   Sous-dossier 'Factures Clients' existant trouve (ID: {factures_clients_id})")
            else:
                # Créer le sous-dossier "Factures Clients"
                factures_clients_id = models.execute_kw(
                    db, uid, password,
                    'documents.document', 'create',
                    [{
                        'name': 'Factures Clients',
                        'type': 'folder',
                        'folder_id': finance_id
                    }]
                )
                print(f"   Sous-dossier 'Factures Clients' cree (ID: {factures_clients_id})")
            
            # 3. Chercher ou créer le dossier du client dans "Factures Clients"
            print(f"   Recherche du dossier client '{partner_name}'...")
            dossier_ids = models.execute_kw(
                db, uid, password,
                'documents.document', 'search',
                [[['name', '=', partner_name], ['type', '=', 'folder'], ['folder_id', '=', factures_clients_id]]]
            )
            
            if dossier_ids:
                dossier_id = dossier_ids[0]
                print(f"   Dossier client '{partner_name}' existant trouve (ID: {dossier_id})")
            else:
                # Créer le dossier du client
                dossier_id = models.execute_kw(
                    db, uid, password,
                    'documents.document', 'create',
                    [{
                        'name': partner_name,
                        'type': 'folder',
                        'folder_id': factures_clients_id
                    }]
                )
                print(f"   Dossier client '{partner_name}' cree (ID: {dossier_id})")
            
            # 4. Vérifier que le dossier existe bien
            dossier_verif = models.execute_kw(
                db, uid, password,
                'documents.document', 'read',
                [[dossier_id]],
                {'fields': ['name', 'type', 'folder_id']}
            )
            
            if dossier_verif:
                dossier_info = dossier_verif[0]
                parent_info = None
                if dossier_info.get('folder_id'):
                    parent_info = models.execute_kw(
                        db, uid, password,
                        'documents.document', 'read',
                        [[dossier_info['folder_id'][0]]],
                        {'fields': ['name']}
                    )
                print(f"   Verification: Dossier '{dossier_info['name']}' existe (ID: {dossier_id})")
                if parent_info:
                    print(f"   Parent: '{parent_info[0]['name']}' (ID: {dossier_info['folder_id'][0]})")
            
            # 2. Encoder le PDF en base64 pour l'upload
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            # 3. Créer le document PDF dans le dossier
            document_data = {
                'name': numero_facture_clean,
                'folder_id': dossier_id,
                'res_model': 'account.move',
                'res_id': facture_id,
                'type': 'binary',
                'datas': pdf_base64,
                'mimetype': 'application/pdf',
            }
            
            document_id = models.execute_kw(
                db, uid, password,
                'documents.document', 'create',
                [document_data]
            )
            
            print(f"   Document cree dans le dossier: {numero_facture_clean} (ID: {document_id})")
            
            print(f"   Lien avec la facture: account.move, ID {facture_id}")
            
        except Exception as e:
            print(f"   Erreur lors de l'upload dans le module Document: {str(e)}")
            import traceback
            traceback.print_exc()
            # Continuer même en cas d'erreur, le PDF local est déjà créé
            print(f"   Le PDF local reste disponible: {chemin_fichier}")
        
        return chemin_fichier
        
    except Exception as e:
        print(f"Erreur lors de la generation du PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    Fonction principale.
    """
    # Récupérer les 100 premières factures clients
    factures, models, db, password = recuperer_factures_clients(limit=100)
    
    if not factures:
        print("\nImpossible de recuperer les factures clients")
        return False
    
    print(f"\n" + "=" * 60)
    print(f"TRAITEMENT DE {len(factures)} FACTURES CLIENTS")
    print("=" * 60)
    
    # Statistiques
    stats = {
        'total': len(factures),
        'succes': 0,
        'echecs': 0,
        'deja_existants': 0
    }
    
    # Traiter chaque facture
    for i, facture in enumerate(factures, 1):
        facture_id = facture['id']
        facture_name = facture.get('name', f'FACTURE_{facture_id}')
        partner_name = facture.get('partner_id', ['', ''])[1] if facture.get('partner_id') else 'Client_Inconnu'
        
        print(f"\n[{i}/{len(factures)}] Traitement de {facture_name} - {partner_name}")
        print("-" * 60)
        
        try:
            # Vérifier si le document existe déjà dans le module Document
            facture_name = facture.get('name', f'FACTURE_{facture_id}')
            document_existant = models.execute_kw(
                db, uid, password,
                'documents.document', 'search',
                [[['res_model', '=', 'account.move'], ['res_id', '=', facture_id]]],
                {'limit': 1}
            )
            
            if document_existant:
                stats['deja_existants'] += 1
                print(f"   DEJA EXISTANT: Document deja present (ID: {document_existant[0]})")
                continue
            
            # Déterminer le modèle de rapport selon le type de facture
            # Par défaut, utiliser "Factures Transferts" (ID: 988)
            # Vous pouvez adapter cette logique selon vos besoins
            report_id = 988  # Factures Transferts
            
            # Générer le PDF et l'uploader
            pdf_file = generer_pdf_facture(facture_id, models, db, password, report_id=report_id)
            
            if pdf_file:
                stats['succes'] += 1
                print(f"   OK: PDF genere et uploade")
            else:
                stats['echecs'] += 1
                print(f"   ECHEC: Impossible de generer le PDF")
                
        except Exception as e:
            stats['echecs'] += 1
            print(f"   ERREUR: {str(e)[:100]}")
            import traceback
            traceback.print_exc()
        
        # Afficher la progression tous les 10 factures
        if i % 10 == 0:
            progress = (i * 100) // len(factures)
            print(f"\n   Progression: {i}/{len(factures)} ({progress}%) - Succes: {stats['succes']}, Echecs: {stats['echecs']}, Deja existants: {stats['deja_existants']}")
    
    # Résumé final
    print(f"\n" + "=" * 60)
    print("RESUME FINAL")
    print("=" * 60)
    print(f"   Total traite: {stats['total']}")
    print(f"   Succes: {stats['succes']}")
    print(f"   Deja existants: {stats['deja_existants']}")
    print(f"   Echecs: {stats['echecs']}")
    if stats['total'] > 0:
        taux = ((stats['succes'] + stats['deja_existants']) * 100) // stats['total']
        print(f"   Taux de reussite: {taux}%")
    
    return stats['succes'] > 0


if __name__ == "__main__":
    main()
    
    print("\n" + "=" * 60)

