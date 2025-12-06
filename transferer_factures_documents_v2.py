#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT (VERSION OPTIMISÉE)
====================================================================================

Ce script transfère les factures clients dans le module document avec :
- Sélection automatique du modèle PDF selon les lignes de facture
- Stockage local des PDFs
- Système de suivi de progression
- Optimisations de performance
"""

from connexion_odoo import connecter_odoo
import base64
import time
import json
import requests
from datetime import datetime
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Dossier local pour stocker les PDFs
DOSSIER_PDF_LOCAL = Path(__file__).parent / 'Factures_pdf_TAL'
DOSSIER_PDF_LOCAL.mkdir(exist_ok=True)

# Cache des modèles de rapport pour éviter les recherches répétées
CACHE_MODELES = {}


def identifier_modele_pdf(models, db, uid, password, facture_id):
    """
    Identifie le modèle PDF à utiliser selon les lignes de facture.
    
    Critères (par ordre de priorité):
    1. "Export de Conteneur" → "Export EOLIS"
    2. "Livraison" → "Factures Livraisons"
    3. "Transfert" → "Factures Transferts"
    4. Par défaut → "Factures Transferts"
    
    Returns:
        tuple: (report_id, report_name) ou (None, None) si non trouvé
    """
    try:
        # Récupérer les lignes de facture avec le nom du produit
        lignes = models.execute_kw(
            db, uid, password,
            'account.move.line',
            'search_read',
            [[['move_id', '=', facture_id]]],
            {'fields': ['name', 'product_id']}
        )
        
        # Récupérer tous les IDs de produits en une seule fois (optimisation)
        product_ids = [ligne['product_id'][0] for ligne in lignes if ligne.get('product_id')]
        product_names = {}
        
        if product_ids:
            try:
                products = models.execute_kw(
                    db, uid, password,
                    'product.product',
                    'read',
                    [product_ids],
                    {'fields': ['name']}
                )
                product_names = {p['id']: p.get('name', '').upper() for p in products}
            except:
                pass
        
        # Vérifier chaque ligne pour identifier le type (par ordre de priorité)
        for ligne in lignes:
            nom_ligne = ligne.get('name', '').upper()
            product_name = ''
            
            # Récupérer le nom du produit depuis le cache
            if ligne.get('product_id'):
                product_name = product_names.get(ligne['product_id'][0], '')
            
            # Vérifier "Export de Conteneur" (priorité 1)
            if 'EXPORT DE CONTENEUR' in nom_ligne or 'EXPORT DE CONTENEUR' in product_name:
                result = trouver_modele_par_nom(models, db, uid, password, 'Export EOLIS')
                if result[0]:
                    return result
            
            # Vérifier "Livraison" (priorité 2)
            if 'LIVRAISON' in nom_ligne or 'LIVRAISON' in product_name:
                result = trouver_modele_par_nom(models, db, uid, password, 'Factures Livraisons')
                if result[0]:
                    return result
            
            # Vérifier "Transfert" (priorité 3)
            if 'TRANSFERT' in nom_ligne or 'TRANSFERT' in product_name:
                result = trouver_modele_par_nom(models, db, uid, password, 'Factures Transferts')
                if result[0]:
                    return result
        
        # Par défaut, utiliser "Factures Transferts"
        return trouver_modele_par_nom(models, db, uid, password, 'Factures Transferts')
        
    except Exception as e:
        # Par défaut, utiliser "Factures Transferts"
        return trouver_modele_par_nom(models, db, uid, password, 'Factures Transferts')


def trouver_modele_par_nom(models, db, uid, password, nom_modele):
    """
    Trouve un modèle de rapport par son nom.
    
    Args:
        models: Proxy XML-RPC
        db: Nom de la base
        uid: ID utilisateur
        password: Mot de passe
        nom_modele: Nom du modèle à chercher
    
    Returns:
        tuple: (report_id, report_name) ou (None, None)
    """
    # Utiliser le cache si disponible
    if nom_modele in CACHE_MODELES:
        return CACHE_MODELES[nom_modele]
    
    try:
        # Rechercher le modèle par nom
        reports = models.execute_kw(
            db, uid, password,
            'ir.actions.report',
            'search_read',
            [[
                ['model', '=', 'account.move'],
                ['name', 'ilike', nom_modele]
            ]],
            {'fields': ['id', 'name', 'report_name'], 'limit': 1}
        )
        
        if reports:
            report_id = reports[0]['id']
            report_name = reports[0].get('report_name', 'account.report_invoice')
            result = (report_id, report_name)
            CACHE_MODELES[nom_modele] = result
            return result
        
        # Si non trouvé, essayer avec des variations
        variations = [
            nom_modele.replace('Factures ', ''),
            nom_modele.replace(' ', ''),
            'account.report_invoice'  # Par défaut
        ]
        
        for variation in variations:
            reports = models.execute_kw(
                db, uid, password,
                'ir.actions.report',
                'search_read',
                [[
                    ['model', '=', 'account.move'],
                    ['name', 'ilike', variation]
                ]],
                {'fields': ['id', 'name', 'report_name'], 'limit': 1}
            )
            if reports:
                report_id = reports[0]['id']
                report_name = reports[0].get('report_name', 'account.report_invoice')
                result = (report_id, report_name)
                CACHE_MODELES[nom_modele] = result
                return result
        
        return None, None
        
    except Exception as e:
        print(f"      ⚠️  Erreur recherche modèle '{nom_modele}': {str(e)[:80]}")
        return None, None


# Session HTTP réutilisable pour éviter de se reconnecter à chaque fois
SESSION_HTTP = None


def initialiser_session_http():
    """
    Initialise une session HTTP réutilisable pour générer les PDFs.
    """
    global SESSION_HTTP
    
    if SESSION_HTTP is not None:
        return SESSION_HTTP
    
    from config import ODOO_CONFIG
    
    try:
        # Créer une session avec retry
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Obtenir le token CSRF
        login_page_url = f"{ODOO_CONFIG['URL']}web/login"
        login_page = session.get(login_page_url, verify=False, timeout=10)
        
        import re
        csrf_token_match = re.search(r'name="csrf_token"\s+value="([^"]+)"', login_page.text)
        if not csrf_token_match:
            csrf_token_match = re.search(r'"csrf_token":\s*"([^"]+)"', login_page.text)
        
        csrf_token = csrf_token_match.group(1) if csrf_token_match else None
        
        # Se connecter
        login_url = f"{ODOO_CONFIG['URL']}web/login"
        login_data = {
            'login': ODOO_CONFIG['USER'],
            'password': ODOO_CONFIG['PASS'],
            'db': ODOO_CONFIG['DB'],
        }
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        login_response = session.post(login_url, data=login_data, verify=False, allow_redirects=True, timeout=10)
        
        if 'login' in login_response.url.lower() or login_response.status_code != 200:
            return None
        
        SESSION_HTTP = session
        return session
        
    except Exception as e:
        return None


def generer_pdf_facture_http(facture_id, report_name, models, db, password):
    """
    Génère le PDF d'une facture via HTTP en réutilisant la session.
    
    Args:
        facture_id: ID de la facture
        report_name: Nom technique du rapport
        models: Proxy XML-RPC
        db: Nom de la base
        password: Mot de passe
    
    Returns:
        bytes: Contenu PDF ou None
    """
    from config import ODOO_CONFIG
    
    # Utiliser la session réutilisable
    session = initialiser_session_http()
    if not session:
        return None
    
    try:
        # Générer le PDF directement (la session est déjà authentifiée)
        pdf_url = f"{ODOO_CONFIG['URL']}report/pdf/{report_name}/{facture_id}"
        pdf_response = session.get(pdf_url, verify=False, timeout=30)
        
        if pdf_response.status_code == 200 and pdf_response.content.startswith(b'%PDF'):
            return pdf_response.content
        
        # Si la session a expiré, réinitialiser
        if pdf_response.status_code == 401 or pdf_response.status_code == 403:
            global SESSION_HTTP
            SESSION_HTTP = None
            session = initialiser_session_http()
            if session:
                pdf_response = session.get(pdf_url, verify=False, timeout=30)
                if pdf_response.status_code == 200 and pdf_response.content.startswith(b'%PDF'):
                    return pdf_response.content
        
        return None
        
    except Exception as e:
        return None


# Cache pour les dossiers Finance et Factures clients
CACHE_DOSSIERS = {
    'finance_id': None,
    'factures_clients_id': None
}


def obtenir_ou_creer_dossier_finance(models, db, uid, password):
    """
    Obtient ou crée le dossier 'Finance' dans le module document.
    """
    if CACHE_DOSSIERS['finance_id']:
        return CACHE_DOSSIERS['finance_id']
    
    # Chercher le dossier Finance
    dossiers = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search',
        [[['name', '=', 'Finance'], ['type', '=', 'folder']]]
    )
    
    if dossiers:
        CACHE_DOSSIERS['finance_id'] = dossiers[0]
        return dossiers[0]
    
    # Créer le dossier Finance
    try:
        dossier_id = models.execute_kw(
            db, uid, password,
            'documents.document',
            'create',
            [{
                'name': 'Finance',
                'type': 'folder',
                'folder_id': False,  # Dossier racine
                'owner_id': uid,  # REQUIRED: propriétaire du dossier
            }]
        )
        CACHE_DOSSIERS['finance_id'] = dossier_id
        return dossier_id
    except Exception as e:
        print(f"      ⚠️  Erreur création dossier Finance: {str(e)[:100]}")
        return None


def obtenir_ou_creer_dossier_factures_clients(models, db, uid, password):
    """
    Obtient ou crée le dossier 'Factures clients' dans Finance.
    """
    if CACHE_DOSSIERS['factures_clients_id']:
        return CACHE_DOSSIERS['factures_clients_id']
    
    # Obtenir le dossier Finance
    finance_id = obtenir_ou_creer_dossier_finance(models, db, uid, password)
    if not finance_id:
        return None
    
    # Chercher le dossier Factures clients dans Finance
    dossiers = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search',
        [[
            ['name', '=', 'Factures clients'],
            ['type', '=', 'folder'],
            ['folder_id', '=', finance_id]
        ]]
    )
    
    if dossiers:
        CACHE_DOSSIERS['factures_clients_id'] = dossiers[0]
        return dossiers[0]
    
    # Créer le dossier Factures clients dans Finance
    try:
        dossier_id = models.execute_kw(
            db, uid, password,
            'documents.document',
            'create',
            [{
                'name': 'Factures clients',
                'type': 'folder',
                'folder_id': finance_id,
                'owner_id': uid,  # REQUIRED: propriétaire du dossier
            }]
        )
        CACHE_DOSSIERS['factures_clients_id'] = dossier_id
        return dossier_id
    except Exception as e:
        print(f"      ⚠️  Erreur création dossier Factures clients: {str(e)[:100]}")
        return None


def obtenir_ou_creer_dossier_client(models, db, uid, password, nom_client, partner_id):
    """
    Obtient ou crée un dossier client dans Finance/Factures clients.
    """
    # Obtenir le dossier Factures clients
    factures_clients_id = obtenir_ou_creer_dossier_factures_clients(models, db, uid, password)
    if not factures_clients_id:
        return None
    
    # Nettoyer le nom du client
    nom_dossier = nom_client.strip()
    nom_dossier = nom_dossier.replace('/', '_').replace('\\', '_').replace(':', '_')
    nom_dossier = nom_dossier.replace('*', '_').replace('?', '_').replace('"', '_')
    nom_dossier = nom_dossier.replace('<', '_').replace('>', '_').replace('|', '_')
    
    # Chercher le dossier client dans Factures clients
    dossiers = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search',
        [[
            ['name', '=', nom_dossier],
            ['type', '=', 'folder'],
            ['folder_id', '=', factures_clients_id]
        ]]
    )
    
    if dossiers:
        return dossiers[0]
    
    # Créer le dossier client dans Factures clients
    try:
        # Essayer avec res_model et res_id
        dossier_id = models.execute_kw(
            db, uid, password,
            'documents.document',
            'create',
            [{
                'name': nom_dossier,
                'type': 'folder',
                'folder_id': factures_clients_id,
                'owner_id': uid,  # REQUIRED: propriétaire du dossier
                'res_model': 'res.partner',
                'res_id': partner_id,
            }]
        )
        return dossier_id
    except Exception as e1:
        # Si ça échoue, essayer sans res_model et res_id
        try:
            dossier_id = models.execute_kw(
                db, uid, password,
                'documents.document',
                'create',
                [{
                    'name': nom_dossier,
                    'type': 'folder',
                    'folder_id': factures_clients_id,
                    'owner_id': uid,  # REQUIRED: propriétaire du dossier
                }]
            )
            return dossier_id
        except Exception as e2:
            print(f"      ⚠️  Erreur création dossier client '{nom_dossier}': {str(e2)[:100]}")
            return None


def sauvegarder_pdf_local(facture_numero, contenu_pdf):
    """
    Sauvegarde le PDF localement.
    
    Args:
        facture_numero: Numéro de la facture
        contenu_pdf: Contenu PDF en bytes
    
    Returns:
        Path: Chemin du fichier sauvegardé ou None
    """
    try:
        # Nettoyer le numéro pour le nom de fichier
        import re
        nom_fichier = re.sub(r'[<>:"/\\|?*]', '_', facture_numero)
        if not nom_fichier.endswith('.pdf'):
            nom_fichier += '.pdf'
        
        chemin_fichier = DOSSIER_PDF_LOCAL / nom_fichier
        
        with open(chemin_fichier, 'wb') as f:
            f.write(contenu_pdf)
        
        return chemin_fichier
    except Exception as e:
        return None


def charger_progression():
    """Charge la progression sauvegardée."""
    fichier_progression = Path(__file__).parent / 'progression_transfert.json'
    if fichier_progression.exists():
        try:
            with open(fichier_progression, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'factures_traitees': [], 'derniere_facture_id': 0}
    return {'factures_traitees': [], 'derniere_facture_id': 0}


def sauvegarder_progression(progression):
    """Sauvegarde la progression."""
    fichier_progression = Path(__file__).parent / 'progression_transfert.json'
    try:
        with open(fichier_progression, 'w', encoding='utf-8') as f:
            json.dump(progression, f, indent=2, ensure_ascii=False)
    except Exception as e:
        pass


def transferer_factures_vers_documents(limit=None, reprendre=True, test_mode=False):
    """
    Transfère les factures clients vers le module document.
    
    Args:
        limit: Nombre maximum de factures (None = toutes)
        reprendre: Si True, reprendre depuis la progression
        test_mode: Si True, mode test avec statistiques de temps
    """
    debut_total = time.time()
    
    # Connexion à Odoo
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    # Vérifier que la base est bien "tal-senegal"
    if db != 'tal-senegal':
        print(f"⚠️  ATTENTION: La base de données est '{db}', pas 'tal-senegal'!")
        reponse = input("Continuer quand même ? (o/N): ").strip().lower()
        if reponse != 'o':
            return False
    
    # Charger la progression
    progression = {}
    factures_deja_traitees = set()
    if reprendre:
        progression = charger_progression()
        factures_deja_traitees = set(progression.get('factures_traitees', []))
        if factures_deja_traitees:
            print(f"📋 Progression chargée: {len(factures_deja_traitees)} factures déjà traitées")
    
    try:
        print("\n" + "=" * 60)
        print("TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT")
        print("=" * 60)
        print(f"Base de données: {db}")
        if test_mode:
            print(f"🔬 MODE TEST: Limité à {limit} factures")
        
        # Compter le total
        print(f"\n🔍 Comptage du total de factures clients...")
        total_factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_count',
            [[['move_type', '=', 'out_invoice']]]
        )
        
        print(f"📊 Total de factures clients dans la base: {total_factures}")
        
        if total_factures == 0:
            print("❌ Aucune facture client trouvée.")
            return False
        
        # Récupérer les factures
        domain = [['move_type', '=', 'out_invoice']]
        derniere_id = progression.get('derniere_facture_id', 0)
        if reprendre and derniere_id > 0:
            domain.append(['id', '>', derniere_id])
        
        if limit:
            print(f"\n🔍 Récupération de {limit} factures clients...")
        else:
            print(f"\n🔍 Récupération de TOUTES les factures clients...")
        
        factures = models.execute_kw(
            db, uid, password,
            'account.move',
            'search_read',
            [domain],
            {
                'fields': ['id', 'name', 'partner_id', 'invoice_date', 'amount_total', 'state'],
                'limit': limit,
                'order': 'id asc'
            }
        )
        
        if not factures:
            print("✅ Toutes les factures ont déjà été traitées.")
            return True
        
        # Filtrer les factures déjà traitées
        factures_a_traiter = [f for f in factures if f['id'] not in factures_deja_traitees]
        
        # Vérifier dans la base de données
        factures_ids_a_traiter = [f['id'] for f in factures_a_traiter]
        documents_existants = models.execute_kw(
            db, uid, password,
            'documents.document',
            'search_read',
            [[
                ['res_model', '=', 'account.move'],
                ['res_id', 'in', factures_ids_a_traiter]
            ]],
            {'fields': ['res_id']}
        )
        
        factures_avec_document = set()
        if documents_existants:
            factures_avec_document = {doc['res_id'] for doc in documents_existants if doc.get('res_id')}
        
        factures_a_traiter_final = [
            f for f in factures_a_traiter 
            if f['id'] not in factures_avec_document
        ]
        
        if factures_avec_document:
            progression['factures_traitees'].extend(list(factures_avec_document))
            progression['factures_traitees'] = list(set(progression['factures_traitees']))
            if factures_avec_document:
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    max(factures_avec_document)
                )
        
        if not factures_a_traiter_final:
            print(f"✅ Toutes les factures ont déjà été transférées.")
            sauvegarder_progression(progression)
            return True
        
        print(f"✅ {len(factures)} factures récupérées")
        print(f"📋 {len(factures_a_traiter_final)} factures à traiter\n")
        
        # Statistiques
        stats = {
            'total': len(factures_a_traiter_final),
            'dossiers_crees': 0,
            'dossiers_existants': 0,
            'documents_crees': 0,
            'documents_deja_existants': 0,
            'pdfs_locaux': 0,
            'erreurs': 0,
            'sans_pdf': 0,
            'temps_par_facture': []
        }
        
        dossiers_clients = {}
        progression['factures_traitees'] = list(set(progression.get('factures_traitees', [])))
        
        print("=" * 60)
        print("TRAITEMENT DES FACTURES")
        print("=" * 60)
        
        for i, facture in enumerate(factures_a_traiter_final, 1):
            debut_facture = time.time()
            facture_id = facture['id']
            facture_numero = facture.get('name', 'N/A')
            partner_info = facture.get('partner_id', [])
            partner_id = partner_info[0] if partner_info else None
            partner_name = partner_info[1] if len(partner_info) > 1 else 'Client inconnu'
            
            if not test_mode or i <= 10:
                print(f"\n[{i}/{len(factures_a_traiter_final)}] Facture {facture_numero} - Client: {partner_name}")
            
            if not partner_id:
                stats['erreurs'] += 1
                continue
            
            # Obtenir ou créer le dossier
            if partner_id not in dossiers_clients:
                dossier_id = obtenir_ou_creer_dossier_client(
                    models, db, uid, password, partner_name, partner_id
                )
                if dossier_id:
                    dossiers_clients[partner_id] = dossier_id
                    stats['dossiers_crees'] += 1
                else:
                    stats['erreurs'] += 1
                    continue
            else:
                dossier_id = dossiers_clients[partner_id]
                stats['dossiers_existants'] += 1
            
            # Vérifier si le document existe déjà
            documents_existants = models.execute_kw(
                db, uid, password,
                'documents.document',
                'search',
                [[
                    ['res_model', '=', 'account.move'],
                    ['res_id', '=', facture_id]
                ]]
            )
            
            if documents_existants:
                stats['documents_deja_existants'] += 1
                progression['factures_traitees'].append(facture_id)
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    facture_id
                )
                sauvegarder_progression(progression)
                continue
            
            # Identifier le modèle PDF
            report_id, report_name = identifier_modele_pdf(models, db, uid, password, facture_id)
            
            if not report_id or not report_name:
                if not test_mode or i <= 10:
                    print(f"   ⚠️  Modèle PDF non trouvé, utilisation du modèle par défaut")
                # Essayer de trouver le modèle par défaut
                default_result = trouver_modele_par_nom(models, db, uid, password, 'account.report_invoice')
                if default_result[0]:
                    report_id, report_name = default_result
                else:
                    report_name = 'account.report_invoice'
            
            if not test_mode or i <= 10:
                modele_info = models.execute_kw(
                    db, uid, password,
                    'ir.actions.report',
                    'read',
                    [[report_id]],
                    {'fields': ['name']}
                ) if report_id else None
                modele_nom = modele_info[0]['name'] if modele_info else 'Par défaut'
                print(f"   📄 Modèle PDF utilisé: {modele_nom}")
            
            # Générer le PDF
            contenu_pdf = generer_pdf_facture_http(facture_id, report_name, models, db, password)
            
            if not contenu_pdf:
                stats['sans_pdf'] += 1
                continue
            
            # Sauvegarder localement
            chemin_local = sauvegarder_pdf_local(facture_numero, contenu_pdf)
            if chemin_local:
                stats['pdfs_locaux'] += 1
            
            # Créer le document dans Odoo
            pdf_base64 = base64.b64encode(contenu_pdf).decode('utf-8')
            try:
                document_id = models.execute_kw(
                    db, uid, password,
                    'documents.document',
                    'create',
                    [{
                        'name': f"{facture_numero}.pdf",
                        'folder_id': dossier_id,
                        'type': 'binary',
                        'datas': pdf_base64,
                        'mimetype': 'application/pdf',
                        'res_model': 'account.move',
                        'res_id': facture_id,
                    }]
                )
                stats['documents_crees'] += 1
                if facture_id not in progression['factures_traitees']:
                    progression['factures_traitees'].append(facture_id)
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    facture_id
                )
                sauvegarder_progression(progression)
            except Exception as e:
                stats['erreurs'] += 1
                if not test_mode or i <= 10:
                    print(f"   ❌ Erreur création document: {str(e)[:80]}")
            
            # Mesurer le temps
            temps_facture = time.time() - debut_facture
            stats['temps_par_facture'].append(temps_facture)
            
            # Afficher la progression
            if i % 50 == 0:
                progress_pct = (i * 100) // len(factures_a_traiter_final)
                temps_moyen = sum(stats['temps_par_facture']) / len(stats['temps_par_facture'])
                temps_restant = (len(factures_a_traiter_final) - i) * temps_moyen
                print(f"\n   📊 Progression: {i}/{len(factures_a_traiter_final)} ({progress_pct}%)")
                print(f"   ⏱️  Temps moyen: {temps_moyen:.2f}s/facture | Temps restant estimé: {temps_restant/60:.1f} min")
            
            # Pas de pause systématique pour optimiser (la session HTTP est réutilisée)
        
        # Résumé final
        temps_total = time.time() - debut_total
        sauvegarder_progression(progression)
        
        print("\n" + "=" * 60)
        print("RÉSUMÉ DU TRANSFERT")
        print("=" * 60)
        print(f"📊 Factures traitées        : {stats['total']}")
        print(f"📁 Dossiers créés          : {stats['dossiers_crees']}")
        print(f"📁 Dossiers réutilisés      : {stats['dossiers_existants']}")
        print(f"📎 Documents créés          : {stats['documents_crees']}")
        print(f"💾 PDFs sauvegardés localement: {stats['pdfs_locaux']}")
        print(f"📎 Documents déjà existants: {stats['documents_deja_existants']}")
        print(f"⚠️  Factures sans PDF       : {stats['sans_pdf']}")
        print(f"❌ Erreurs                  : {stats['erreurs']}")
        print(f"⏱️  Temps total              : {temps_total/60:.2f} minutes")
        
        if stats['temps_par_facture']:
            temps_moyen = sum(stats['temps_par_facture']) / len(stats['temps_par_facture'])
            print(f"⏱️  Temps moyen par facture  : {temps_moyen:.2f} secondes")
            if test_mode and total_factures > limit:
                temps_estime_total = (total_factures * temps_moyen) / 60
                print(f"⏱️  Temps estimé pour toutes les factures: {temps_estime_total:.1f} minutes ({temps_estime_total/60:.1f} heures)")
        
        print(f"💾 Progression sauvegardée: {len(progression['factures_traitees'])} factures")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du transfert: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT")
    print("TAL-migration - Base de PRODUCTION (tal-senegal)")
    print("=" * 60)
    
    # Mode test par défaut si aucun argument
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        print("⚠️  MODE COMPLET: Traitement de TOUTES les factures")
        transferer_factures_vers_documents(limit=None, reprendre=True, test_mode=False)
    else:
        print("🔬 MODE TEST: Traitement de 100 factures pour évaluer le temps")
        print("   Utilisez 'python transferer_factures_documents_v2.py --all' pour traiter toutes les factures")
        transferer_factures_vers_documents(limit=100, reprendre=True, test_mode=True)
    
    print("\n" + "=" * 60)

