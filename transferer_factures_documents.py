#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT
================================================================

Ce script transfère TOUTES les factures clients dans le module document
en créant un dossier par client. Il inclut un système de suivi de progression
pour pouvoir reprendre en cas d'interruption.
"""

from connexion_odoo import connecter_odoo
import base64
import time
import json
from datetime import datetime
from pathlib import Path

def obtenir_ou_creer_dossier_client(models, db, uid, password, nom_client, partner_id):
    """
    Obtient ou crée un dossier dans le module document pour un client.
    
    Args:
        models: Proxy XML-RPC pour les modèles Odoo
        db: Nom de la base de données
        uid: ID utilisateur
        password: Mot de passe
        nom_client: Nom du client
        partner_id: ID du partenaire client
    
    Returns:
        int: ID du dossier créé ou trouvé
    """
    # Nettoyer le nom du client pour éviter les caractères problématiques
    nom_dossier = nom_client.strip()
    # Remplacer les caractères interdits
    nom_dossier = nom_dossier.replace('/', '_').replace('\\', '_').replace(':', '_')
    nom_dossier = nom_dossier.replace('*', '_').replace('?', '_').replace('"', '_')
    nom_dossier = nom_dossier.replace('<', '_').replace('>', '_').replace('|', '_')
    
    # Chercher si le dossier existe déjà (utiliser documents.document avec type='folder')
    dossiers_existants = models.execute_kw(
        db, uid, password,
        'documents.document',
        'search',
        [[['name', '=', nom_dossier], ['type', '=', 'folder']]]
    )
    
    if dossiers_existants:
        return dossiers_existants[0]
    
    # Créer le dossier (utiliser documents.document avec type='folder')
    try:
        dossier_id = models.execute_kw(
            db, uid, password,
            'documents.document',
            'create',
            [{
                'name': nom_dossier,
                'type': 'folder',
                'res_model': 'res.partner',
                'res_id': partner_id,
            }]
        )
        return dossier_id
    except Exception as e:
        # Si la création échoue, essayer sans res_model et res_id
        try:
            dossier_id = models.execute_kw(
                db, uid, password,
                'documents.document',
                'create',
                [{
                    'name': nom_dossier,
                    'type': 'folder',
                }]
            )
            return dossier_id
        except Exception as e2:
            print(f"      ⚠️  Erreur lors de la création du dossier '{nom_dossier}': {str(e2)[:100]}")
            return None


def obtenir_pdf_facture(models, db, uid, password, facture_id, facture_numero):
    """
    Récupère le PDF d'une facture.
    
    Args:
        models: Proxy XML-RPC pour les modèles Odoo
        db: Nom de la base de données
        uid: ID utilisateur
        password: Mot de passe
        facture_id: ID de la facture
        facture_numero: Numéro de la facture
    
    Returns:
        tuple: (nom_fichier, contenu_base64, mimetype) ou (None, None, None) si erreur
    """
    try:
        # Chercher les pièces jointes PDF de la facture
        attachments = models.execute_kw(
            db, uid, password,
            'ir.attachment',
            'search_read',
            [[
                ['res_model', '=', 'account.move'],
                ['res_id', '=', facture_id],
                ['mimetype', '=', 'application/pdf']
            ]],
            {'fields': ['name', 'datas', 'mimetype'], 'limit': 1, 'order': 'id desc'}
        )
        
        if attachments and attachments[0].get('datas'):
            nom_fichier = attachments[0].get('name', f'{facture_numero}.pdf')
            if not nom_fichier.endswith('.pdf'):
                nom_fichier = f'{facture_numero}.pdf'
            return (
                nom_fichier,
                attachments[0].get('datas'),
                attachments[0].get('mimetype', 'application/pdf')
            )
        
        # Si pas de PDF trouvé, essayer de générer le PDF via l'action report
        try:
            # Chercher le rapport de facture par défaut
            reports = models.execute_kw(
                db, uid, password,
                'ir.actions.report',
                'search_read',
                [[['report_name', '=', 'account.report_invoice']]],
                {'fields': ['id', 'report_name'], 'limit': 1}
            )
            
            if reports:
                # Utiliser la méthode render_qweb_pdf via le modèle account.move
                # Note: Cette méthode peut nécessiter que la facture soit validée
                try:
                    # Essayer d'appeler la méthode directement sur account.move
                    pdf_data = models.execute_kw(
                        db, uid, password,
                        'account.move',
                        'render_qweb_pdf',
                        [[facture_id], 'account.report_invoice']
                    )
                    
                    if pdf_data:
                        nom_fichier = f'{facture_numero}.pdf'
                        return (nom_fichier, pdf_data, 'application/pdf')
                except:
                    # Si ça ne fonctionne pas, essayer via ir.actions.report
                    try:
                        report_id = reports[0]['id']
                        pdf_data = models.execute_kw(
                            db, uid, password,
                            'ir.actions.report',
                            'render_qweb_pdf',
                            [[report_id], [facture_id]]
                        )
                        
                        if pdf_data:
                            nom_fichier = f'{facture_numero}.pdf'
                            return (nom_fichier, pdf_data, 'application/pdf')
                    except:
                        pass
        except Exception as e_report:
            # Si la génération échoue, on continue sans PDF
            pass
        
        return None, None, None
        
    except Exception as e:
        print(f"      ⚠️  Erreur lors de la récupération du PDF: {str(e)[:100]}")
        return None, None, None


def creer_document_dans_dossier(models, db, uid, password, dossier_id, nom_fichier, contenu_base64, mimetype, facture_id):
    """
    Crée un document dans un dossier du module document.
    
    Args:
        models: Proxy XML-RPC pour les modèles Odoo
        db: Nom de la base de données
        uid: ID utilisateur
        password: Mot de passe
        dossier_id: ID du dossier
        nom_fichier: Nom du fichier
        contenu_base64: Contenu du fichier en base64
        mimetype: Type MIME du fichier
        facture_id: ID de la facture source
    
    Returns:
        int: ID du document créé ou None si erreur
    """
    try:
        document_id = models.execute_kw(
            db, uid, password,
            'documents.document',
            'create',
            [{
                'name': nom_fichier,
                'folder_id': dossier_id,
                'type': 'binary',
                'datas': contenu_base64,
                'mimetype': mimetype,
                'res_model': 'account.move',
                'res_id': facture_id,
            }]
        )
        return document_id
    except Exception as e:
        # Essayer sans res_model et res_id si la première tentative échoue
        try:
            document_id = models.execute_kw(
                db, uid, password,
                'documents.document',
                'create',
                [{
                    'name': nom_fichier,
                    'folder_id': dossier_id,
                    'type': 'binary',
                    'datas': contenu_base64,
                    'mimetype': mimetype,
                }]
            )
            return document_id
        except Exception as e2:
            print(f"      ⚠️  Erreur lors de la création du document: {str(e2)[:100]}")
            return None


def charger_progression():
    """
    Charge la progression sauvegardée depuis un fichier JSON.
    
    Returns:
        dict: Dictionnaire contenant les IDs des factures déjà traitées
    """
    fichier_progression = Path(__file__).parent / 'progression_transfert.json'
    if fichier_progression.exists():
        try:
            with open(fichier_progression, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'factures_traitees': [], 'derniere_facture_id': 0}
    return {'factures_traitees': [], 'derniere_facture_id': 0}


def sauvegarder_progression(progression):
    """
    Sauvegarde la progression dans un fichier JSON.
    
    Args:
        progression: Dictionnaire contenant la progression
    """
    fichier_progression = Path(__file__).parent / 'progression_transfert.json'
    try:
        with open(fichier_progression, 'w', encoding='utf-8') as f:
            json.dump(progression, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"      ⚠️  Erreur lors de la sauvegarde de la progression: {str(e)[:100]}")


def transferer_factures_vers_documents(limit=None, reprendre=True):
    """
    Transfère les factures clients vers le module document.
    
    Args:
        limit: Nombre maximum de factures à transférer (None = toutes les factures)
        reprendre: Si True, reprendre depuis la dernière progression sauvegardée
    """
    # Connexion à Odoo
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    # Charger la progression si on reprend
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
        
        # Compter le total de factures clients
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
        
        # Récupérer toutes les factures clients (sans limite ou avec limite)
        if limit:
            print(f"\n🔍 Récupération de {limit} factures clients...")
        else:
            print(f"\n🔍 Récupération de TOUTES les factures clients ({total_factures})...")
        
        # Construire le domaine de recherche
        domain = [['move_type', '=', 'out_invoice']]
        
        # Si on reprend, commencer après la dernière facture traitée
        derniere_id = progression.get('derniere_facture_id', 0)
        if reprendre and derniere_id > 0:
            domain.append(['id', '>', derniere_id])
            print(f"   Reprise depuis la facture ID > {derniere_id}")
        
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
            print("✅ Toutes les factures ont déjà été traitées ou aucune nouvelle facture trouvée.")
            return True
        
        # Filtrer les factures déjà traitées selon la progression
        factures_a_traiter = [f for f in factures if f['id'] not in factures_deja_traitees]
        
        if not factures_a_traiter:
            print(f"✅ Les {len(factures)} factures récupérées ont déjà été traitées (selon la progression).")
            return True
        
        # Vérifier dans la base de données quelles factures ont déjà un document
        # pour éviter de retraiter même si elles ne sont pas dans la progression
        print(f"\n🔍 Vérification dans la base de données des factures déjà transférées...")
        factures_ids_a_traiter = [f['id'] for f in factures_a_traiter]
        
        # Rechercher les documents existants pour ces factures
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
            print(f"   📋 {len(factures_avec_document)} factures ont déjà un document dans la base")
        
        # Filtrer à nouveau pour exclure celles qui ont déjà un document
        factures_a_traiter_final = [
            f for f in factures_a_traiter 
            if f['id'] not in factures_avec_document
        ]
        
        # Ajouter les factures avec document à la progression pour ne pas les retraiter
        if factures_avec_document:
            progression['factures_traitees'].extend(list(factures_avec_document))
            progression['factures_traitees'] = list(set(progression['factures_traitees']))  # Dédupliquer
            if factures_avec_document:
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    max(factures_avec_document)
                )
            print(f"   ✅ {len(factures_avec_document)} factures ajoutées à la progression")
        
        if not factures_a_traiter_final:
            print(f"✅ Toutes les factures ont déjà été transférées.")
            sauvegarder_progression(progression)
            return True
        
        print(f"✅ {len(factures)} factures récupérées")
        print(f"📋 {len(factures_a_traiter)} factures après filtrage progression")
        print(f"📋 {len(factures_a_traiter_final)} factures à traiter (après vérification dans la base)\n")
        
        # Statistiques
        stats = {
            'total': len(factures_a_traiter_final),
            'total_base': len(factures),
            'deja_traitees_progression': len(factures) - len(factures_a_traiter),
            'deja_traitees_base': len(factures_avec_document),
            'dossiers_crees': 0,
            'dossiers_existants': 0,
            'documents_crees': 0,
            'documents_deja_existants': 0,
            'erreurs': 0,
            'sans_pdf': 0
        }
        
        # Dictionnaire pour suivre les dossiers créés par client
        dossiers_clients = {}
        
        print("=" * 60)
        print("TRAITEMENT DES FACTURES")
        print("=" * 60)
        
        # S'assurer que la progression contient toutes les factures déjà traitées
        progression['factures_traitees'] = list(set(progression.get('factures_traitees', [])))
        
        for i, facture in enumerate(factures_a_traiter_final, 1):
            facture_id = facture['id']
            facture_numero = facture.get('name', 'N/A')
            partner_info = facture.get('partner_id', [])
            partner_id = partner_info[0] if partner_info else None
            partner_name = partner_info[1] if len(partner_info) > 1 else 'Client inconnu'
            
            print(f"\n[{i}/{len(factures_a_traiter_final)}] Facture {facture_numero} - Client: {partner_name}")
            
            if not partner_id:
                print(f"   ⚠️  Pas de client associé, ignorée")
                stats['erreurs'] += 1
                continue
            
            # Obtenir ou créer le dossier du client
            if partner_id not in dossiers_clients:
                dossier_id = obtenir_ou_creer_dossier_client(
                    models, db, uid, password, partner_name, partner_id
                )
                if dossier_id:
                    dossiers_clients[partner_id] = dossier_id
                    # Vérifier si c'était un nouveau dossier en vérifiant la date de création
                    try:
                        dossier_info = models.execute_kw(
                            db, uid, password,
                            'documents.document',
                            'read',
                            [[dossier_id]],
                            {'fields': ['name', 'create_date']}
                        )
                        if dossier_info:
                            # Si créé il y a moins de 5 secondes, c'est probablement nouveau
                            create_date_str = dossier_info[0].get('create_date', '')
                            if create_date_str:
                                try:
                                    create_date = datetime.strptime(create_date_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
                                    time_diff = (datetime.now() - create_date).total_seconds()
                                    if time_diff < 5:
                                        stats['dossiers_crees'] += 1
                                    else:
                                        stats['dossiers_existants'] += 1
                                except:
                                    stats['dossiers_existants'] += 1
                            else:
                                stats['dossiers_existants'] += 1
                            print(f"   📁 Dossier créé/trouvé: {dossier_info[0].get('name')}")
                    except:
                        stats['dossiers_existants'] += 1
                        print(f"   📁 Dossier créé/trouvé: {partner_name}")
                else:
                    print(f"   ❌ Impossible de créer/trouver le dossier")
                    stats['erreurs'] += 1
                    continue
            else:
                dossier_id = dossiers_clients[partner_id]
                stats['dossiers_existants'] += 1
            
            # Vérifier si le document existe déjà (double vérification)
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
                print(f"   ✅ Document déjà existant pour cette facture (ID: {documents_existants[0]})")
                stats['documents_deja_existants'] += 1
                # Marquer comme traitée même si déjà existant
                if facture_id not in progression['factures_traitees']:
                    progression['factures_traitees'].append(facture_id)
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    facture_id
                )
                # Sauvegarder immédiatement pour cette facture
                sauvegarder_progression(progression)
                continue
            
            # Récupérer le PDF de la facture
            print(f"   📄 Récupération du PDF...")
            nom_fichier, contenu_pdf, mimetype = obtenir_pdf_facture(
                models, db, uid, password, facture_id, facture_numero
            )
            
            if not contenu_pdf:
                print(f"   ⚠️  PDF non disponible pour cette facture")
                stats['sans_pdf'] += 1
                continue
            
            # Créer le document dans le dossier
            print(f"   📎 Création du document '{nom_fichier}'...")
            document_id = creer_document_dans_dossier(
                models, db, uid, password, dossier_id, nom_fichier, contenu_pdf, mimetype, facture_id
            )
            
            if document_id:
                print(f"   ✅ Document créé avec succès (ID: {document_id})")
                stats['documents_crees'] += 1
                # Marquer comme traitée immédiatement
                if facture_id not in progression['factures_traitees']:
                    progression['factures_traitees'].append(facture_id)
                progression['derniere_facture_id'] = max(
                    progression.get('derniere_facture_id', 0),
                    facture_id
                )
                # Sauvegarder immédiatement pour chaque facture réussie
                sauvegarder_progression(progression)
            else:
                print(f"   ❌ Échec de la création du document")
                stats['erreurs'] += 1
                # Ne pas marquer comme traitée en cas d'erreur pour pouvoir réessayer
            
            # Afficher la progression tous les 50 factures
            if i % 50 == 0:
                progress_pct = (i * 100) // len(factures_a_traiter_final)
                print(f"\n   📊 Progression: {i}/{len(factures_a_traiter_final)} ({progress_pct}%)")
                print(f"   💾 Total factures tracées: {len(progression['factures_traitees'])}")
            
            # Petite pause pour éviter de surcharger le serveur
            if i % 10 == 0:
                time.sleep(0.5)
        
        # Sauvegarder la progression finale
        sauvegarder_progression(progression)
        
        # Affichage du résumé
        print("\n" + "=" * 60)
        print("RÉSUMÉ DU TRANSFERT")
        print("=" * 60)
        print(f"📊 Total factures dans la base: {total_factures}")
        print(f"📋 Factures récupérées        : {stats['total_base']}")
        print(f"📋 Déjà traitées (progression): {stats['deja_traitees_progression']}")
        print(f"📋 Déjà traitées (base données): {stats['deja_traitees_base']}")
        print(f"📋 Factures traitées cette session: {stats['total']}")
        print(f"📁 Dossiers créés            : {stats['dossiers_crees']}")
        print(f"📁 Dossiers réutilisés       : {stats['dossiers_existants']}")
        print(f"📎 Documents créés           : {stats['documents_crees']}")
        print(f"📎 Documents déjà existants   : {stats['documents_deja_existants']}")
        print(f"⚠️  Factures sans PDF         : {stats['sans_pdf']}")
        print(f"❌ Erreurs                    : {stats['erreurs']}")
        print(f"📁 Total dossiers uniques     : {len(dossiers_clients)}")
        print(f"💾 Progression sauvegardée    : {len(progression['factures_traitees'])} factures")
        
        total_traitees = len(progression['factures_traitees'])
        if total_factures > 0:
            pourcentage = (total_traitees * 100) // total_factures
            print(f"\n📈 Progression globale: {total_traitees}/{total_factures} ({pourcentage}%)")
        
        if stats['documents_crees'] > 0 or stats['documents_deja_existants'] > 0:
            print(f"\n✅ Transfert terminé avec succès!")
            if total_traitees < total_factures:
                print(f"💡 Il reste {total_factures - total_traitees} factures à traiter.")
                print(f"   Relancez le script pour continuer le transfert.")
        else:
            print(f"\n⚠️  Aucun document n'a été créé. Vérifiez les erreurs ci-dessus.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du transfert: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT")
    print("TAL-migration - Base de PRODUCTION (tal-senegal)")
    print("=" * 60)
    print("⚠️  ATTENTION: Ce script va traiter TOUTES les factures clients")
    print("   La progression est sauvegardée automatiquement pour permettre la reprise")
    print()
    
    # Traiter toutes les factures (limit=None) et reprendre depuis la progression
    transferer_factures_vers_documents(limit=None, reprendre=True)
    
    print("\n" + "=" * 60)

