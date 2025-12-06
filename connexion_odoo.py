#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE CONNEXION À ODOO SAAS - TAL-migration
===============================================

Ce script permet de se connecter à la base Odoo SaaS TAL-migration
en utilisant l'API XML-RPC.

Auteur: Assistant IA
Date: 2025-11-29
"""

import xmlrpc.client
import ssl
from config import ODOO_CONFIG

# =============================================================================
# FONCTIONS DE CONNEXION
# =============================================================================

def lister_bases_disponibles():
    """
    Liste les bases de données disponibles sur le serveur Odoo.
    Note: Cette fonction nécessite que le serveur autorise cette opération.
    """
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        transport = xmlrpc.client.SafeTransport(context=ssl_context)
        common = xmlrpc.client.ServerProxy(
            f"{ODOO_CONFIG['URL']}/xmlrpc/2/common", 
            transport=transport
        )
        
        # Tenter de lister les bases (peut ne pas être autorisé)
        try:
            db_list = common.db_list()
            return db_list
        except:
            return None
    except Exception as e:
        print(f"⚠️  Impossible de lister les bases: {str(e)}")
        return None


def connecter_odoo():
    """
    Établit une connexion à Odoo via XML-RPC.
    
    Returns:
        tuple: (uid, models) si la connexion réussit, (None, None) sinon
    """
    try:
        # Configuration SSL pour les connexions HTTPS
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Création du transport sécurisé avec allow_none activé
        transport = xmlrpc.client.SafeTransport(context=ssl_context)
        transport.allow_none = True  # Permet de passer None dans XML-RPC
        
        # Connexion au serveur commun pour l'authentification
        common = xmlrpc.client.ServerProxy(
            f"{ODOO_CONFIG['URL']}/xmlrpc/2/common", 
            transport=transport,
            allow_none=True  # Permet de passer None dans XML-RPC
        )
        
        # Authentification
        print(f"🔐 Connexion à {ODOO_CONFIG['URL']}...")
        print(f"📊 Base de données: {ODOO_CONFIG['DB']}")
        print(f"👤 Utilisateur: {ODOO_CONFIG['USER']}")
        
        uid = common.authenticate(
            ODOO_CONFIG['DB'], 
            ODOO_CONFIG['USER'], 
            ODOO_CONFIG['PASS'], 
            {}
        )
        
        if uid:
            # Connexion au serveur d'objets pour les opérations
            models = xmlrpc.client.ServerProxy(
                f"{ODOO_CONFIG['URL']}/xmlrpc/2/object", 
                transport=transport,
                allow_none=True  # Permet de passer None dans XML-RPC
            )
            
            # Récupération des informations utilisateur
            user_info = models.execute_kw(
                ODOO_CONFIG['DB'], 
                uid, 
                ODOO_CONFIG['PASS'],
                'res.users', 
                'read', 
                [[uid]], 
                {'fields': ['name', 'login', 'email']}
            )
            
            print(f"✅ Connexion réussie!")
            print(f"   UID: {uid}")
            if user_info:
                print(f"   Nom: {user_info[0].get('name', 'N/A')}")
                print(f"   Email: {user_info[0].get('email', 'N/A')}")
            
            return uid, models, ODOO_CONFIG['DB'], ODOO_CONFIG['PASS']
        else:
            print("❌ Échec de l'authentification. Vérifiez vos identifiants.")
            return None, None, None, None
            
    except xmlrpc.client.Fault as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "database" in error_msg.lower():
            print(f"❌ Erreur: La base de données '{ODOO_CONFIG['DB']}' n'existe pas.")
            print(f"   Veuillez vérifier le nom de la base de données dans config.py")
            print(f"\n💡 Astuce: Le nom de la base peut être différent de l'URL.")
            print(f"   Exemple: Si l'URL est 'https://TAL-migration.odoo.com/',")
            print(f"   la base peut s'appeler 'tal-migration' ou 'tal-migration-xxxxx'")
            # Tenter de lister les bases disponibles
            print(f"\n🔍 Tentative de liste des bases disponibles...")
            db_list = lister_bases_disponibles()
            if db_list:
                print(f"   Bases disponibles: {', '.join(db_list[:10])}")
        else:
            print(f"❌ Erreur lors de la connexion: {error_msg}")
        return None, None, None, None
    except Exception as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "database" in error_msg.lower():
            print(f"❌ Erreur: La base de données '{ODOO_CONFIG['DB']}' n'existe pas.")
            print(f"   Veuillez vérifier le nom de la base de données dans config.py")
            print(f"\n💡 Astuce: Le nom de la base peut être différent de l'URL.")
        else:
            print(f"❌ Erreur lors de la connexion: {error_msg}")
        return None, None, None, None


def tester_connexion():
    """
    Teste la connexion et affiche quelques informations sur la base.
    """
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("\n❌ Impossible de se connecter à Odoo.")
        return False
    
    try:
        # Test de lecture d'un modèle simple
        print("\n📋 Test de lecture des données...")
        
        # Compter les utilisateurs
        user_count = models.execute_kw(
            db, uid, password,
            'res.users', 'search_count',
            [[]]
        )
        print(f"   Nombre d'utilisateurs: {user_count}")
        
        # Compter les partenaires
        partner_count = models.execute_kw(
            db, uid, password,
            'res.partner', 'search_count',
            [[]]
        )
        print(f"   Nombre de partenaires: {partner_count}")
        
        # Vérifier la version d'Odoo
        common = xmlrpc.client.ServerProxy(
            f"{ODOO_CONFIG['URL']}/xmlrpc/2/common"
        )
        version_info = common.version()
        print(f"\n📦 Version Odoo: {version_info.get('server_version', 'N/A')}")
        print(f"   Serveur: {version_info.get('server_serie', 'N/A')}")
        
        print("\n✅ Connexion et tests réussis!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {str(e)}")
        return False


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONNEXION À ODOO SAAS - TAL-migration")
    print("=" * 60)
    print()
    
    # Test de connexion
    tester_connexion()
    
    print("\n" + "=" * 60)


